from unittest.mock import MagicMock, patch
from domain.services.qa_service import QAService


def _make_service(answer: str, metadata: dict) -> QAService:
    mock_doc = MagicMock()
    mock_doc.metadata = metadata

    mock_chain = MagicMock()
    mock_chain.invoke.return_value = {"answer": answer, "context": [mock_doc]}

    with patch("domain.services.qa_service.build_rag_pipeline", return_value=mock_chain):
        return QAService()


def test_ask_retorna_answer():
    service = _make_service("30 dias.", {"source": "data/sample.txt"})
    result = service.ask("Quantos dias de férias?")
    assert result["answer"] == "30 dias."


def test_ask_retorna_sources():
    service = _make_service("ok", {"source": "data/sample.txt", "page": 1})
    result = service.ask("Pergunta")
    assert result["sources"][0]["source"] == "data/sample.txt"
    assert result["sources"][0]["page"] == 1


def test_ask_source_sem_metadado_page():
    service = _make_service("ok", {"source": "data/sample.txt"})
    result = service.ask("Pergunta")
    assert result["sources"][0]["page"] is None


def test_ask_source_sem_metadado_source():
    service = _make_service("ok", {})
    result = service.ask("Pergunta")
    assert result["sources"][0]["source"] == "desconhecido"
