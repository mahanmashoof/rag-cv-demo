# RAG CV Demo (Backend)

Semantic search over CVs with grounded answers and confidence scores.

## What Problem This Solves

- Finding the right candidates in a pile of CVs is slow and error‑prone.
- Keyword search misses relevant candidates due to phrasing differences.
- This project lets you ask natural questions (e.g., “Who has experience with React?”) and returns the most relevant CV excerpts with sources and a confidence score.

## Why RAG > ChatGPT for This Use Case

- ChatGPT alone can hallucinate or invent facts not present in your CVs.
- RAG constrains the model to answer using retrieved CV text only.
- You get traceable answers with source citations and an explicit confidence level.
- Separation of retrieval and generation allows auditing and tuning each stage.

## Architecture

```
Browser (Vercel FE)
	|
	|  HTTP: /questions, /ask
	v
FastAPI (Render BE)
	|
	|  Ingestion at startup -> ChromaDB collection (cvs)
	|  Retrieval: embed question -> query collection -> distances
	|  Generation: OpenAI (gpt-4o-mini) grounded on retrieved docs
	v
ChromaDB (PersistentClient on disk)   OpenAI APIs (Embeddings + Chat)
```

Data flow:

- `ingest.py`: reads CVs from `data/`, embeds with `text-embedding-3-small`, stores in Chroma.
- `retrieve.py`: embeds the question, queries Chroma, computes confidence from distances, returns docs + sources.
- `api.py`: exposes `/questions` and `/ask` endpoints used by the frontend.

## Files

- `ingest.py`: Load CVs from `data/` and insert into ChromaDB collection.
- `retrieve.py`: Retrieve top‑k CV snippets and generate grounded answers.
- `api.py`: FastAPI server with CORS and lifespan startup ingestion.
- `requirements.txt`: Backend dependencies.

## How To Run (Local)

Prereqs:

- Python 3.10+ and an OpenAI API key in `.env` (same folder as backend).

Create venv and install deps:

```bash
cd BE
python -m venv venv
./venv/Scripts/Activate.ps1   # Windows PowerShell
pip install -r requirements.txt
```

Set environment variables (in `BE/.env`):

```env
OPENAI_API_KEY=sk-...
FRONTEND_URL=http://localhost:5173
```

Ingest CVs and start API:

```bash
python ingest.py
uvicorn api:app --reload
```

Frontend (from the FE app):

```bash
cd FE
npm install
npm run dev
```

## Tech Stack

- Backend: FastAPI, `chromadb`, `python-dotenv`
- AI: OpenAI `text-embedding-3-small`, `gpt-4o-mini`
- Data: ChromaDB PersistentClient (on disk)
