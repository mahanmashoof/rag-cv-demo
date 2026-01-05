from openai import OpenAI
import chromadb

client = OpenAI()
chroma = chromadb.PersistentClient(path="./chroma_db")
collection = chroma.get_collection(name="cvs")

def embed_query(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def retrieve(question):
    query_embedding = embed_query(question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=10
    )

    print("\nQUESTION:", question)
    print("-" * 50)

    for i in range(len(results["documents"][0])):
        print(f"\nResult {i+1}")
        print("Source:", results["metadatas"][0][i]["source"])
        print("Text preview:")
        print(results["documents"][0][i][:300])

if __name__ == "__main__":
    retrieve("Who has experience with React?")
