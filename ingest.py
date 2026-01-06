# Import statements: Bring in external libraries
import os  # Operating system functions (file/directory operations)
import chromadb  # Vector database library for semantic search

# Create a persistent ChromaDB client (saves data to disk)
chroma = chromadb.PersistentClient(path="./chroma_db")
# Get or create a collection (like a table in a database)
collection = chroma.get_or_create_collection(name="cvs")

# Constants: Variables in UPPERCASE by convention (not truly constant in Python)
DATA_DIR = "data"

# Function definition: 'def' keyword, followed by function name and parentheses
def load_cvs():
    # Initialize an empty list to store documents
    docs = []
    # Loop through all files in the DATA_DIR directory
    for file in os.listdir(DATA_DIR):
        # Context manager: 'with' ensures file is properly closed after use
        # os.path.join() creates proper file paths for any OS
        with open(os.path.join(DATA_DIR, file), "r", encoding="utf-8") as f:
            # Append a dictionary to the list
            # Dictionary: key-value pairs enclosed in curly braces {}
            docs.append({
                "id": file,  # Dictionary key: value
                "text": f.read()  # f.read() reads entire file content
            })
    # Return statement: sends data back to the caller
    return docs

def ingest():
    # Call the load_cvs function and store result in variable
    cvs = load_cvs()

    # Call collection method with named arguments
    collection.add(
        # List comprehension: compact way to create lists
        # [expression for item in iterable]
        documents=[cv["text"] for cv in cvs],  # Extract 'text' from each CV dict
        ids=[cv["id"] for cv in cvs],  # Extract 'id' from each CV dict
        metadatas=[{"source": cv["id"]} for cv in cvs]  # Create new dict for each CV
    )

    # f-string: formatted string literal (prefix with f)
    # {variable} gets replaced with variable's value
    # len() returns the number of items in a collection
    print(f"Ingested {len(cvs)} CVs.")

# if __name__ == "__main__": ensures code only runs when script is executed directly
# (not when imported as a module)
if __name__ == "__main__":
    ingest()