from fastapi import APIRouter
from schemas.ask_schema import AskRequest, AskResponse
from domain.services.qa_service import QAService

router = APIRouter()
service = QAService()


@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    return service.ask(request.question)
