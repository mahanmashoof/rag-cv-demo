# RAG CV Demo

A simple Retrieval-Augmented Generation (RAG) system for searching CV/resume documents using semantic search.

## Files

### ingest.py

Loads CV text files from the `data/` folder, generates embeddings using OpenAI's `text-embedding-3-small` model, and stores them in a ChromaDB vector database for semantic search.

### retrieve.py

Queries the vector database with natural language questions (e.g., "Who has experience with React?"), retrieves the most semantically similar CV documents, and displays the results with source information.

## Usage

1. Run `python ingest.py` to index the CVs
2. Run `python retrieve.py` to search the indexed documents

## Requirements

- OpenAI API key (set in `.env`)
- Python packages: `openai`, `chromadb`
