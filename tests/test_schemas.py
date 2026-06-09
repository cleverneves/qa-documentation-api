import pytest
from pydantic import ValidationError
from schemas.ask_schema import AskRequest, AskResponse, SourceDocument


def test_ask_request_valid():
    req = AskRequest(question="Quantos dias de férias tenho?")
    assert req.question == "Quantos dias de férias tenho?"


def test_ask_request_missing_question():
    with pytest.raises(ValidationError):
        AskRequest()


def test_source_document_sem_pagina():
    s = SourceDocument(source="data/sample.txt")
    assert s.source == "data/sample.txt"
    assert s.page is None


def test_source_document_com_pagina():
    s = SourceDocument(source="data/doc.pdf", page=3)
    assert s.page == 3


def test_ask_response_valido():
    resp = AskResponse(
        answer="30 dias de férias.",
        sources=[{"source": "data/sample.txt", "page": None}],
    )
    assert resp.answer == "30 dias de férias."
    assert resp.sources[0].source == "data/sample.txt"


def test_ask_response_sources_invalido():
    with pytest.raises(ValidationError):
        AskResponse(answer="ok", sources=["string_invalida"])
