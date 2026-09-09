
from pathlib import Path

from app.services.ai_service import ask_ai


KNOWLEDGE_DIR = Path("knowledge")


def load_knowledge() -> str:
    knowledge_file = KNOWLEDGE_DIR / "plant_operations.txt"

    return knowledge_file.read_text(encoding="utf-8")


def retrieve_knowledge(question: str) -> str:
    knowledge = load_knowledge()

    paragraphs = knowledge.split("\n\n")

    stop_words = {
        "what", "is", "the", "for", "a", "an",
        "of", "to", "in", "on", "and", "or",
        "does", "do", "how", "why", "when"
    }

    question_words = {
        word.strip("?,.!").lower()
        for word in question.split()
        if word.strip("?,.!").lower() not in stop_words
    }

    scored_paragraphs = []

    for paragraph in paragraphs:
        paragraph_words = {
            word.strip("?,.!").lower()
            for word in paragraph.split()
        }

        score = len(question_words & paragraph_words)

        if score > 2:
            scored_paragraphs.append((score, paragraph))

    scored_paragraphs.sort(
        reverse=True,
        key=lambda item: item[0]
    )

    top_paragraphs = scored_paragraphs[:2]

    if not top_paragraphs:
        return ""

    return "\n\n".join(
        paragraph for score, paragraph in top_paragraphs
    )


def ask_with_rag(question: str):
    context = retrieve_knowledge(question)

    prompt = f"""
Answer the user's question using the provided context.

Context:
{context}

User question:
{question}

If the answer cannot be found in the context, say:
"I don't have enough information in the knowledge base to answer this."
"""

    answer = ask_ai(prompt)

    return {
        "answer": answer,
        "evidence": context
    }

