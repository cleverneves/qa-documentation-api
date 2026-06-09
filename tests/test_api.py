from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from app import app
from api.routes.ask import get_qa_service


def _mock_service():
    service = MagicMock()
    service.ask.return_value = {
        "answer": "30 dias de férias.",
        "sources": [{"source": "data/sample.txt", "page": None}],
    }
    return service


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ask_retorna_200():
    app.dependency_overrides[get_qa_service] = _mock_service
    response = client.post("/ask", json={"question": "Quantos dias de férias?"})
    app.dependency_overrides.clear()
    assert response.status_code == 200


def test_ask_retorna_answer():
    app.dependency_overrides[get_qa_service] = _mock_service
    response = client.post("/ask", json={"question": "Quantos dias de férias?"})
    app.dependency_overrides.clear()
    assert response.json()["answer"] == "30 dias de férias."


def test_ask_retorna_sources():
    app.dependency_overrides[get_qa_service] = _mock_service
    response = client.post("/ask", json={"question": "Quantos dias de férias?"})
    app.dependency_overrides.clear()
    sources = response.json()["sources"]
    assert sources[0]["source"] == "data/sample.txt"


def test_ask_body_invalido():
    response = client.post("/ask", json={})
    assert response.status_code == 422


def test_ask_question_vazia():
    app.dependency_overrides[get_qa_service] = _mock_service
    response = client.post("/ask", json={"question": ""})
    app.dependency_overrides.clear()
    assert response.status_code == 200
