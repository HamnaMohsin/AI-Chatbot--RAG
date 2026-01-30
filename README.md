# AI-Chatbot--RAG
RAG chatbot with FastAPI backend, Streamlit frontend, and Groq-powered LLM inference.
# RAG Chatbot (FastAPI + Streamlit + Groq)

A Retrieval-Augmented Generation (RAG) chatbot built using:

- FastAPI (backend)
- Streamlit (UI)
- Groq LLM API
- Sentence Transformers
- FAISS / ChromaDB

## Features
- Upload `.docx` story
- Ask questions based on the document
- In-chat memory
- Clean backend/frontend separation

## Tech Stack
- Python
- FastAPI
- Streamlit
- Groq
- SentenceTransformers
- FAISS / Chroma
**
How to Run**

 1. Install dependencies
```bash
uv sync

**2. Add environment variables**

Create a .env file:

GROQ_API_KEY=your_key_here
HF_TOKEN=optional

3. Start backend
uvicorn api:app --reload

4. Start UI
streamlit run app.py
