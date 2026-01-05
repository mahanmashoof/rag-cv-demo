import os
import chromadb
from openai import OpenAI

client = OpenAI()

chroma = chromadb.PersistentClient(path="./chroma_db")
collection = chroma.get_or_create_collection(name="cvs")

DATA_DIR = "data"

def load_cvs():
    docs = []
    for file in os.listdir(DATA_DIR):
        with open(os.path.join(DATA_DIR, file), "r", encoding="utf-8") as f:
            docs.append({
                "id": file,
                "text": f.read()
            })
    return docs

def embed(texts):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [e.embedding for e in response.data]

def ingest():
    cvs = load_cvs()
    embeddings = embed([cv["text"] for cv in cvs])

    collection.add(
        documents=[cv["text"] for cv in cvs],
        embeddings=embeddings,
        ids=[cv["id"] for cv in cvs],
        metadatas=[{"source": cv["id"]} for cv in cvs]
    )

    print(f"Ingested {len(cvs)} CVs.")

if __name__ == "__main__":
    ingest()