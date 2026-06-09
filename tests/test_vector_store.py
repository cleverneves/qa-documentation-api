import pytest
from unittest.mock import MagicMock
from infra.vectorstore import vector_store as vs_module
from infra.vectorstore.vector_store import load_vectorstore


def test_load_vectorstore_raises_when_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(vs_module, "VECTOR_DB_PATH", str(tmp_path / "nonexistent"))
    with pytest.raises(FileNotFoundError, match="python -m ingestion.indexer"):
        load_vectorstore(MagicMock())


def test_load_vectorstore_mensagem_inclui_caminho(tmp_path, monkeypatch):
    missing = str(tmp_path / "nonexistent")
    monkeypatch.setattr(vs_module, "VECTOR_DB_PATH", missing)
    with pytest.raises(FileNotFoundError, match=missing):
        load_vectorstore(MagicMock())
