from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT = """
You are an assistant that answers questions ONLY using the provided CV excerpts.
- Do NOT use outside knowledge.
- If the information is missing or unclear, say you don't have enough information.
- Keep answers short and factual.
- Mention candidate names explicitly if possible.
"""

def answer_question(question: str, retrieved_docs: list[str]) -> str:
    """
    Uses retrieved CV text to generate a grounded answer.

    Args:
        question: The user question
        retrieved_docs: List of CV text snippets

    Returns:
        LLM-generated answer string
    """

    context = "\n\n".join(retrieved_docs)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
Context:
{context}

Question:
{question}

Answer using only the context above.
"""
            }
        ],
        temperature=0  # critical: reduces hallucinations
    )

    return response.choices[0].message.content.strip()
