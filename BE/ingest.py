import os
import chromadb
from openai import OpenAI

# -------------------------------
# CONFIGURATION (explicit & shared)
# -------------------------------

EMBEDDING_MODEL = "text-embedding-3-small"
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "cvs"
DATA_PATH = "./data"   # folder with CV text files

openai_client = OpenAI()

# -------------------------------
# EMBEDDING FUNCTION
# -------------------------------

def embed_text(text: str) -> list[float]:
    """
    Converts text into a numerical vector embedding.
    This MUST match the embedding used at query time.
    """

    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.data[0].embedding


# -------------------------------
# INGESTION LOGIC
# -------------------------------

def ingest():
    """
    Reads CV files, embeds them, and stores them in Chroma.
    """

    # Persistent Chroma client (disk-backed)
    chroma = chromadb.PersistentClient(path=CHROMA_PATH)

    # Create or load collection
    collection = chroma.get_or_create_collection(
        name=COLLECTION_NAME
    )

    documents = []
    metadatas = []
    embeddings = []
    ids = []

    # Read all CV files
    for idx, filename in enumerate(os.listdir(DATA_PATH)):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(DATA_PATH, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read().strip()

        # Skip empty files
        if not text:
            continue

        # Create embedding
        embedding = embed_text(text)

        documents.append(text)
        embeddings.append(embedding)
        metadatas.append({"source": filename})
        ids.append(f"cv_{idx}")

    # Store everything in Chroma
    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

    print(f"Ingested {len(documents)} documents.")


if __name__ == "__main__":
    ingest()
