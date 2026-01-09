# RAG CV Demo

A simple Retrieval-Augmented Generation (RAG) system for searching CV/resume documents using semantic search.

## Files

### ingest.py

Loads CV text files from the `data/` folder and stores them in a ChromaDB vector database. Uses ChromaDB's default embedding function for semantic search.

### retrieve.py

Queries the vector database with natural language questions and retrieves the most semantically similar CV documents. Runs through a set of demo questions defined in `questions.py` and displays results with source information.

### answer.py

Uses OpenAI's GPT-4o-mini to generate grounded answers based on retrieved CV documents. Implements a system prompt that prevents hallucinations by constraining the model to only use provided context.

## Usage

1. Run `python ingest.py` to index the CVs
2. Run `python retrieve.py` to run demo queries against the indexed documents
3. Use `answer.py` module to generate LLM-based answers from retrieved documents

## Requirements

- Python packages: `chromadb`, `openai` (for answer.py)
