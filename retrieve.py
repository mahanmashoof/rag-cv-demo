import chromadb
# 'from module import name' imports specific items from a module
from questions import DEMO_QUESTIONS  # Import the DEMO_QUESTIONS list

# -----------------------------
# Setup persistent Chroma client
# -----------------------------
chroma = chromadb.PersistentClient(path="./chroma_db")
# Get existing collection (unlike get_or_create, this will error if not found)
collection = chroma.get_collection(name="cvs")


# Type hints: Specify expected types (question: str, k: int)
# Default parameter: k=3 means k is optional and defaults to 3
def retrieve(question: str, k: int = 3):
    """
    Docstring: Multi-line string describing the function.
    Triple quotes allow strings to span multiple lines.

    Args:
        question: Natural language question
        k: Number of results to return

    Returns:
        List of retrieved documents with metadata
    """
    # Call the query method and store returned value
    results = collection.query(
        # List with one element: [question]
        query_texts=[question],
        # Named argument with variable value
        n_results=k
    )

    return results


# -----------------------------
# Run demo questions
# -----------------------------
# For loop: Iterate through each item in DEMO_QUESTIONS list
for question in DEMO_QUESTIONS:
    # String concatenation with + operator
    # "\n" is newline character, "*" repeats strings
    print("\n" + "=" * 60)  # Prints 60 equal signs
    # f-string: Embed variables directly in strings
    print(f"QUESTION: {question}")
    print("-" * 60)  # Prints 60 dashes

    # Function call with argument
    results = retrieve(question)

    # Dictionary access: results["key"] gets value for that key
    # [0] accesses first element of the list
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # enumerate() returns both index and value
    # zip() pairs elements from two lists together
    # start=1 makes enumerate begin counting at 1 instead of 0
    for idx, (doc, meta) in enumerate(zip(documents, metadatas), start=1):
        print(f"\nResult {idx}")
        # Access nested dictionary: meta is dict, access its 'source' key
        print(f"Source: {meta['source']}")
        print("Text preview:")
        # String slicing: doc[:300] gets first 300 characters
        print(doc[:300])
