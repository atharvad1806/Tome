"""
Builds a prompt from retrieved chunks and queries Groq (free tier).
"""
import os
from openai import OpenAI

CHAT_MODEL = "llama-3.3-70b-versatile"  # strong free Groq model

client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1",
)


def build_context_block(retrieved_chunks: list[dict]) -> str:
    parts = []
    for chunk in retrieved_chunks:
        parts.append(f"[Chapter: {chunk['chapter_title']}]\n{chunk['text']}")
    return "\n\n---\n\n".join(parts)


def ask_question(question: str, retrieved_chunks: list[dict], book_title: str = "the book") -> str:
    context = build_context_block(retrieved_chunks)

    system_prompt = (
        f"You are an assistant answering questions about a book called '{book_title}'. "
        "Use ONLY the excerpts provided below to answer. If the excerpts don't contain "
        "enough information to answer confidently, say so rather than guessing. "
        "When relevant, mention which chapter the information comes from.\n\n"
        f"BOOK EXCERPTS:\n\n{context}"
    )

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
    )

    return response.choices[0].message.content