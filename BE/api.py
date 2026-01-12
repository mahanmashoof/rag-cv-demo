import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ingest import ingest
from retrieve import retrieve, generate_answer

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Run ingestion
    ingest()
    yield
    # Shutdown: Add cleanup code here if needed

app = FastAPI(lifespan=lifespan)

# Configure CORS
frontend_urls = os.getenv("FRONTEND_URL", "http://localhost:5173")
allowed_origins = [url.strip() for url in frontend_urls.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Demo questions - single source of truth
DEMO_QUESTIONS = [
    "Who has experience with React?",
    "Who has worked remotely?",
    "Who is the most intelligent?",
]

class Question(BaseModel):
    question: str

@app.get("/questions")
def get_questions():
    """Returns the list of demo questions"""
    return {"questions": DEMO_QUESTIONS}

@app.post("/ask")
def ask_question(q: Question):
    documents, sources, confidence = retrieve(q.question)

    if confidence == "Low" or not documents:
        return {
            "answer": "Not enough reliable information in the documents.",
            "confidence": confidence,
            "sources": []
        }

    answer = generate_answer(q.question, documents)

    return {
        "answer": answer,
        "confidence": confidence,
        "sources": sources
    }