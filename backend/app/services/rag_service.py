from pathlib import Path

import numpy as np

from app.services.ai_service import ask_ai
from app.services.embedding_service import create_embedding


KNOWLEDGE_DIR = Path("knowledge")
knowledge_paragraphs = []
knowledge_embeddings = []


def load_knowledge() -> str:
    knowledge_file = KNOWLEDGE_DIR / "plant_operations.txt"

    return knowledge_file.read_text(encoding="utf-8")

def calculate_similarity(embedding1, embedding2):
    return np.dot(
        embedding1,
        embedding2
    ) / (
        np.linalg.norm(embedding1)
        * np.linalg.norm(embedding2)
    )

def prepare_knowledge():
    global knowledge_paragraphs
    global knowledge_embeddings

    knowledge = load_knowledge()

    knowledge_paragraphs = [
        paragraph.strip()
        for paragraph in knowledge.split("\n\n")
        if paragraph.strip()
    ]

    knowledge_embeddings = [
        create_embedding(paragraph)
        for paragraph in knowledge_paragraphs
    ]


prepare_knowledge()


def retrieve_knowledge(question: str) -> str:
    question_embedding = create_embedding(question)

    scored_paragraphs = []

    for paragraph, paragraph_embedding in zip(
        knowledge_paragraphs,
        knowledge_embeddings
    ):
        similarity = calculate_similarity(
    question_embedding,
    paragraph_embedding
    )

        scored_paragraphs.append(
            (similarity, paragraph)
        )

    scored_paragraphs.sort(
        reverse=True,
        key=lambda item: item[0]
    )

    if not scored_paragraphs:
      return ""

    best_score = scored_paragraphs[0][0]

    if best_score < 0.35:
        return ""

    top_paragraphs = [
        paragraph
        for score, paragraph in scored_paragraphs[:3]
        if score >= 0.45
    ]

    return "\n\n".join(top_paragraphs)


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