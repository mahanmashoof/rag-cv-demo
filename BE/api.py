import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from retrieve import retrieve, generate_answer

load_dotenv()
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],
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
