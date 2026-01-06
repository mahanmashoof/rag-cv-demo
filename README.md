# RAG CV Demo

A simple Retrieval-Augmented Generation (RAG) system for searching CV/resume documents using semantic search.

## Files

### ingest.py

Loads CV text files from the `data/` folder and stores them in a ChromaDB vector database. Uses ChromaDB's default embedding function for semantic search.

### retrieve.py

Queries the vector database with natural language questions and retrieves the most semantically similar CV documents. Runs through a set of demo questions defined in `questions.py` and displays results with source information.

## Usage

1. Run `python ingest.py` to index the CVs
2. Run `python retrieve.py` to run demo queries against the indexed documents

## Requirements

- Python packages: `chromadb`
