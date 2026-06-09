from functools import lru_cache
from fastapi import APIRouter, Depends
from schemas.ask_schema import AskRequest, AskResponse
from domain.services.qa_service import QAService

router = APIRouter()


@lru_cache(maxsize=1)
def get_qa_service() -> QAService:
    return QAService()


@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest, service: QAService = Depends(get_qa_service)):
    return service.ask(request.question)
