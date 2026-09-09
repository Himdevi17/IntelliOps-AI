from fastapi import APIRouter
from app.schemas.ai import AIRequest
from app.services.rag_service import ask_with_rag


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.post("/ask")
def ask_question(request: AIRequest):
    result = ask_with_rag(request.prompt)

    return {
        "question": request.prompt,
        "answer": result["answer"],
        "evidence": result["evidence"]
    }