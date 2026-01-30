from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from rag import load_story, chunk_text, store_story, chat

app = FastAPI(title="RAG Chatbot API")

# ---------- Request Models ----------
class ChatRequest(BaseModel):
    question: str

# ---------- Routes ----------

@app.get("/")
def root():
    return {"message": "RAG Chatbot API is running"}

@app.post("/upload")
async def upload_story(file: UploadFile = File(...)):
    story = load_story(file.file)
    chunks = chunk_text(story)
    store_story(chunks)
    return {"status": "Story uploaded and indexed successfully"}

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    answer = chat(req.question)
    return {"answer": answer}
