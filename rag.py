from groq import Groq
from dotenv import load_dotenv
import os
from docx import Document
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# ===== Load API Key =====
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY missing in .env")

client = Groq(api_key=api_key)

# ===== Embedding Model =====
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# ===== Chroma DB =====
chroma_client = chromadb.Client(Settings(persist_directory="./chroma_db"))
collection = chroma_client.get_or_create_collection(name="story_rag")

# ===== Load + Chunk =====
def load_story(file):
    doc = Document(file)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

def chunk_text(text, chunk_size=300):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# ===== Store in Chroma =====
def store_story(chunks):
    if collection.count() == 0:
        embeddings = embedder.encode(chunks).tolist()
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        collection.add(documents=chunks, embeddings=embeddings, ids=ids)

# ===== Retrieve =====
def retrieve_context(query, k=3):
    q_emb = embedder.encode([query]).tolist()
    results = collection.query(query_embeddings=q_emb, n_results=k)
    return "\n".join(results["documents"][0])

# ===== Chat =====
memory = [
    {
        "role": "system",
        "content": "You are a RAG chatbot. Answer strictly from the story. "
                   "If answer is not in the story, say you don't know."
                   "tone: philopohical"
                   "character: Friedrich Nietzsche"
    }
]

def chat(user_input):
    context = retrieve_context(user_input)

    rag_prompt = f"""
Use the following story context to answer.

Story Context:
{context}

Question:
{user_input}
"""

    memory.append({"role": "user", "content": rag_prompt})

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=memory,
        temperature=0.3,
        max_tokens=400,
    )

    reply = response.choices[0].message.content
    memory.append({"role": "assistant", "content": reply})
    return reply
