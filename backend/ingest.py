from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from chromadb import PersistentClient
from tqdm import tqdm
from litellm import completion
from multiprocessing import Pool
from tenacity import retry, wait_exponential
import re

load_dotenv(override=True)

# 🔹 MODEL CONFIG
MODEL = "openai/gpt-4.1-nano"

# 🔹 PATH CONFIG
BASE_DIR = Path(__file__).parent
DB_NAME = str(BASE_DIR / "vector_db_sops")
collection_name = "docs"
embedding_model = "text-embedding-3-large"
KNOWLEDGE_BASE_PATH = BASE_DIR.parent / "knowledge-base"

AVERAGE_CHUNK_SIZE = 500
WORKERS = 2

wait = wait_exponential(multiplier=1, min=5, max=60)

openai = OpenAI()


# 🔥 DATA MODELS
class Result(BaseModel):
    page_content: str
    metadata: dict


class Chunk(BaseModel):
    headline: str
    summary: str
    original_text: str

    def as_result(self, document):
        metadata = {
            "source": document["source"],   # for UI display
            "type": document["type"],
            "batch": document["batch"],     # 🔥 critical
            "error": document["error"]      # 🔥 critical
        }

        return Result(
            page_content=self.headline + "\n\n" + self.summary + "\n\n" + self.original_text,
            metadata=metadata,
        )


class Chunks(BaseModel):
    chunks: list[Chunk]


# 🔥 STEP 1: EXTRACT SOP METADATA
def extract_sop_metadata(text):
    batch_match = re.search(r"Batch Name\s*\n(.+)", text)
    error_match = re.search(r"Error Code\s*\n(.+)", text)

    batch = batch_match.group(1).strip() if batch_match else "UNKNOWN"
    error = error_match.group(1).strip() if error_match else "UNKNOWN"

    return batch, error


# 🔥 STEP 2: LOAD DOCUMENTS
def fetch_documents():
    documents = []

    for folder in KNOWLEDGE_BASE_PATH.iterdir():
        doc_type = folder.name

        for file in folder.rglob("*.md"):
            with open(file, "r", encoding="utf-8") as f:
                text = f.read()

            batch, error = extract_sop_metadata(text)

            documents.append({
                "type": doc_type,
                "source": file.name,   # clean name for UI
                "text": text,
                "batch": batch,
                "error": error
            })

    print(f"📂 Loaded {len(documents)} SOP documents")
    return documents


# 🔥 STEP 3: PROMPT FOR CHUNKING (SOP OPTIMIZED)
def make_prompt(document):
    how_many = (len(document["text"]) // AVERAGE_CHUNK_SIZE) + 1

    return f"""
You are preparing SOP documents for an enterprise batch support AI system.

Each document is a batch-specific SOP.

IMPORTANT RULES:
- Preserve batch name and error clearly
- Keep resolution steps intact
- Do NOT lose SQL queries
- Maintain troubleshooting clarity
- Ensure chunks help answer real support queries

Split into chunks with:
- headline → short meaningful title
- summary → short explanation
- original_text → exact SOP content

Ensure overlap between chunks.

Document Type: {document["type"]}
Source: {document["source"]}
Batch: {document["batch"]}
Error: {document["error"]}

Document:
{document["text"]}

Return structured chunks.
"""


def make_messages(document):
    return [{"role": "user", "content": make_prompt(document)}]


# 🔥 STEP 4: PROCESS DOCUMENT → CHUNKS
@retry(wait=wait)
def process_document(document):
    messages = make_messages(document)

    response = completion(
        model=MODEL,
        messages=messages,
        response_format=Chunks
    )

    reply = response.choices[0].message.content
    doc_chunks = Chunks.model_validate_json(reply).chunks

    return [chunk.as_result(document) for chunk in doc_chunks]


# 🔥 STEP 5: PARALLEL CHUNKING
def create_chunks(documents):
    chunks = []

    with Pool(processes=WORKERS) as pool:
        for result in tqdm(pool.imap_unordered(process_document, documents), total=len(documents)):
            chunks.extend(result)

    return chunks


# 🔥 STEP 6: CREATE EMBEDDINGS + VECTOR DB
def create_embeddings(chunks):
    chroma = PersistentClient(path=DB_NAME)

    # 🔥 Fresh ingestion
    existing = [c.name for c in chroma.list_collections()]
    if collection_name in existing:
        print("🗑️ Deleting old collection...")
        chroma.delete_collection(collection_name)

    texts = [chunk.page_content for chunk in chunks]

    print("🧠 Creating embeddings...")
    emb = openai.embeddings.create(model=embedding_model, input=texts).data
    vectors = [e.embedding for e in emb]

    collection = chroma.get_or_create_collection(collection_name)

    ids = [str(i) for i in range(len(chunks))]
    metas = [chunk.metadata for chunk in chunks]

    collection.add(
        ids=ids,
        embeddings=vectors,
        documents=texts,
        metadatas=metas
    )

    print(f"✅ Vector DB created with {collection.count()} chunks")


# 🔥 MAIN
if __name__ == "__main__":
    print("🚀 Starting SOP ingestion pipeline...\n")

    documents = fetch_documents()

    chunks = create_chunks(documents)

    create_embeddings(chunks)

    print("\n🎉 SOP ingestion completed successfully!")