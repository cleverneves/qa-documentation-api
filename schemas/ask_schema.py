from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str


class SourceDocument(BaseModel):
    source: str
    page: int | None = None


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceDocument]
