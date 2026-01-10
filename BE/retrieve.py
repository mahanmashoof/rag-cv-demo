import os
import chromadb
from openai import OpenAI

# -------------------------
# Setup
# -------------------------
# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

EMBEDDING_MODEL = "text-embedding-3-small"
openai_client = OpenAI()
chroma = chromadb.PersistentClient(path=os.path.join(SCRIPT_DIR, "chroma_db"))
collection = chroma.get_collection(name="cvs")
# Confidence thresholds (lower distance = better)
HIGH_CONFIDENCE = 0.9
MEDIUM_CONFIDENCE = 1.1

# -------------------------
# Confidence logic
# -------------------------

def embed_text(text: str) -> list[float]:
    """
    Converts text into a vector embedding.
    This MUST be the same model used during ingestion.
    """

    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.data[0].embedding

def calculate_confidence(distances: list[float]) -> str:
    """
    Converts vector distances into a human-readable confidence level.
    Uses the BEST (lowest) distance only.
    """

    if not distances:
        return "None"

    best_distance = min(distances)

    if best_distance <= HIGH_CONFIDENCE:
        return "High"
    elif best_distance <= MEDIUM_CONFIDENCE:
        return "Medium"
    else:
        return "Low"


# -------------------------
# Retrieval
# -------------------------

def retrieve(question: str, k: int = 3):
    """
    Retrieves top-k relevant chunks from Chroma.
    Returns documents + confidence.
    """

    query_embedding = embed_text(question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    confidence = calculate_confidence(distances)

    return documents, metadatas, confidence


# -------------------------
# Answer generation (LLM)
# -------------------------

def generate_answer(question: str, documents: list[str]) -> str:
    """
    Uses GPT only AFTER retrieval.
    GPT is strictly grounded in provided context.
    """

    context = "\n\n".join(documents)

    prompt = f"""
You are an assistant answering questions based ONLY on the context below.
If the answer is not clearly supported, say so.

Context:
{context}

Question:
{question}

Answer:
"""

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()


# -------------------------
# Main runner
# -------------------------

def ask(question: str):
    documents, metadatas, confidence = retrieve(question)

    print("\n" + "=" * 60)
    print(f"QUESTION: {question}")
    print("-" * 60)

    if confidence == "Low" or not documents:
        print("\nANSWER:")
        print("⚠️ Not enough reliable information in the documents to answer this question.")
        print("\nConfidence:", confidence)
        return

    answer = generate_answer(question, documents)

    print("\nANSWER:")
    print(answer)
    print(f"\nConfidence: ", confidence)


# -------------------------
# Demo questions
# -------------------------

if __name__ == "__main__":
    from api import DEMO_QUESTIONS
    
    for q in DEMO_QUESTIONS:
        ask(q)
