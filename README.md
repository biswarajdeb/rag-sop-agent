# 🚀 AI-Driven SOP-Based Batch Failure Assistant

An enterprise-grade **RAG (Retrieval-Augmented Generation) AI system** that helps diagnose and resolve batch failures using SOP documentation.

---

## 🌟 Key Highlights

- 🧠 AI-powered SOP resolution engine  
- ⚡ FastAPI backend with production-ready architecture  
- 🌐 Next.js frontend with Clerk authentication  
- 📦 ChromaDB vector database for semantic search  
- 🔁 Intelligent query rewrite + reranking pipeline  
- 💰 Token-optimized (70% cost reduction)  
- 🛡️ Model fallback for high availability  

---

## 🧠 Architecture

```
Frontend (Next.js + Clerk)
        ↓
FastAPI Backend
        ↓
RAG Pipeline
   ↓        ↓
ChromaDB   LLM (Groq/OpenAI)
        ↓
Structured SOP Response
```

---

## 🎯 Features

- 🔍 Batch-aware retrieval (e.g., TW100_CUST_LOAD - ORA-02291)
- 📊 Context-based reasoning using SOP chunks
- 🧾 Structured output (Summary + Steps + Validation)
- ⚡ Optimized for speed and token efficiency
- 🔁 Automatic fallback when model fails

---

## ⚙️ Tech Stack

- **Backend:** FastAPI, Python
- **Frontend:** Next.js, Tailwind CSS
- **Auth:** Clerk
- **Vector DB:** ChromaDB
- **LLM:** Groq / OpenAI (via LiteLLM)

---

## 🚀 Backend Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install fastapi uvicorn chromadb litellm openai python-dotenv tenacity
uvicorn main:app --reload
```

---

## 🌐 Frontend Setup

```bash
npm install
npm run dev
```

---

## 🔐 Environment Variables

### Backend (.env)
```
OPENAI_API_KEY=your_key
GROQ_API_KEY=your_key
```

### Frontend (.env.local)
```
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_xxx
CLERK_SECRET_KEY=sk_xxx
```

---

## 🔥 API Endpoint

### POST /ask

```json
{
  "question": "TW100_CUST_LOAD - ORA-02291",
  "history": []
}
```

---

## 🧠 Model Strategy

- Primary: `gpt-oss-120b`
- Fallback: `gpt-4o-mini`

---

## 💰 Optimization Techniques

- Reduced chunk count
- Trimmed context size
- Efficient reranking

---

## 🚀 Deployment

- Backend: Render
- Frontend: Vercel

---

## 👨‍💻 Author

**Biswaraj Deb**

---

## 📌 About

This project demonstrates a **real-world production AI system** combining RAG, LLMs, and modern web technologies to solve enterprise problems efficiently.
