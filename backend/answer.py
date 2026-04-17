from openai import OpenAI
from dotenv import load_dotenv
from chromadb import PersistentClient
from litellm import completion
from pydantic import BaseModel, Field
from pathlib import Path
from tenacity import retry, wait_exponential
import re

load_dotenv(override=True)

# 🔹 MODEL CONFIG
MODEL = "groq/openai/gpt-oss-120b"

# 🔹 PATH CONFIG (IMPORTANT: use your SOP DB)
#DB_NAME = str(Path(__file__).parent.parent / "vector_db_sops")
BASE_DIR = Path(__file__).parent
DB_NAME = str(BASE_DIR / "vector_db_sops")

collection_name = "docs"
embedding_model = "text-embedding-3-large"
wait = wait_exponential(multiplier=1, min=5, max=60)

openai = OpenAI()

chroma = PersistentClient(path=DB_NAME)
collection = chroma.get_or_create_collection(collection_name)

RETRIEVAL_K = 30
FINAL_K = 3


# 🔥 SYSTEM PROMPT (L2 ENGINEER STYLE)
SYSTEM_PROMPT = """
You are an expert L2 support engineer for batch processing systems.

Your job is to strictly follow SOP-style responses.

MANDATORY RESPONSE FORMAT:

1. **Resolution Summary**
- One short paragraph explaining the issue and fix

2. **Steps to Resolve**
- Follow the exact batch-specific SOP steps to resolve the issue
- Provide numbered steps (Step 1, Step 2, etc.) and no deviations required from sop
- Each step must be actionable
- If SQL is needed, include it clearly in code blocks 

3. **Validation**
- Follow the SOP validation steps if applicable to confirm the issue is resolved
- No generic validation steps, only SOP-specific ones


STRICT RULES:
- If batch is mentioned → ONLY use that batch SOP
- DO NOT mix other batch solutions
- DO NOT give generic explanation
- ALWAYS convert context into step-by-step instructions
- Keep answer crisp and practical

Context:
{context}
"""


# 🔹 DATA MODELS
class Result(BaseModel):
    page_content: str
    metadata: dict


class RankOrder(BaseModel):
    order: list[int] = Field(
        description="Ranked chunk ids from most relevant to least"
    )


# 🔥 ENTITY EXTRACTION (BATCH + ERROR)
def extract_entities(query: str):
    batch_match = re.search(r"(TW\d{3}_[A-Z_]+|TW\d{3})", query)
    error_match = re.search(r"(ORA-\d+)", query)

    batch = batch_match.group(0) if batch_match else None
    error = error_match.group(0) if error_match else None

    return batch, error


# 🔥 RERANK FUNCTION (UNCHANGED CORE)
@retry(wait=wait)
def rerank(question, chunks):
    system_prompt = """
You are a document re-ranker.
Rank the provided chunks based on relevance to the question.
Return ONLY a list of chunk ids in ranked order.
"""

    user_prompt = f"Question:\n{question}\n\nChunks:\n\n"

    for index, chunk in enumerate(chunks):
        user_prompt += f"# CHUNK ID: {index + 1}\n{chunk.page_content}\n\n"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    response = completion(model=MODEL, messages=messages, response_format=RankOrder)
    order = RankOrder.model_validate_json(response.choices[0].message.content).order

    return [chunks[i - 1] for i in order]


# 🔥 QUERY REWRITE (UNCHANGED)
@retry(wait=wait)
def rewrite_query(question, history=[]):
    message = f"""
Rewrite the user question into a short, precise search query.

History:
{history}

Question:
{question}

Return ONLY the refined query.
"""

    response = completion(model=MODEL, messages=[{"role": "system", "content": message}])
    return response.choices[0].message.content


# 🔥 MERGE RESULTS
def merge_chunks(chunks, reranked):
    merged = chunks[:]
    existing = [c.page_content for c in chunks]

    for chunk in reranked:
        if chunk.page_content not in existing:
            merged.append(chunk)

    return merged


# 🔥 SMART RETRIEVAL (CORE UPGRADE)
def fetch_context_unranked(question):
    batch, error = extract_entities(question)

    query_embedding = openai.embeddings.create(
        model=embedding_model,
        input=[question]
    ).data[0].embedding

    # 🎯 STEP 1: Batch-specific retrieval
    if batch:
        print(f"🎯 Batch detected: {batch}")

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=RETRIEVAL_K,
            where={"batch": batch}
        )

        if results["documents"][0]:
            print("✅ Using batch-filtered retrieval")
        else:
            print("⚠️ No batch match → fallback")
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=RETRIEVAL_K
            )
    else:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=RETRIEVAL_K
        )

    chunks = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        chunks.append(Result(page_content=doc, metadata=meta))

    return chunks


# 🔥 FINAL CONTEXT FETCH
def fetch_context(original_question):
    rewritten_question = rewrite_query(original_question)

    chunks1 = fetch_context_unranked(original_question)
    chunks2 = fetch_context_unranked(rewritten_question)

    chunks = merge_chunks(chunks1, chunks2)

    reranked = rerank(original_question, chunks)

    return reranked[:FINAL_K]


# 🔥 BUILD PROMPT
def make_rag_messages(question, history, chunks):
    context_parts = []

    for chunk in chunks:
        batch = chunk.metadata.get("batch", "UNKNOWN")
        error = chunk.metadata.get("error", "UNKNOWN")

        context_parts.append(
            f"[Batch: {batch} | Error: {error}]\n{chunk.page_content}"
        )

    context = "\n\n".join(context_parts)

    system_prompt = SYSTEM_PROMPT.format(context=context)

    return (
        [{"role": "system", "content": system_prompt}]
        + history
        + [{"role": "user", "content": question}]
    )

def trim_chunks(chunks, max_chars=500):
    for chunk in chunks:
        if hasattr(chunk, "page_content"):
            chunk.page_content = chunk.page_content[:max_chars]
    return chunks

# 🔥 MAIN ANSWER FUNCTION
@retry(wait=wait)
def answer_question(question: str, history: list[dict] = []):
    print("\n🚀 Processing query:", question)

    chunks = fetch_context(question)
    chunks = trim_chunks(chunks)

    messages = make_rag_messages(question, history, chunks)

    response = completion(model=MODEL, messages=messages)

    answer = response.choices[0].message.content

    return answer, chunks