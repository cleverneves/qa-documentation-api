import pytest
from ingestion.loaders.document_loader import load_documents


def test_extensao_nao_suportada():
    with pytest.raises(ValueError, match=".csv"):
        load_documents("relatorio.csv")


def test_mensagem_lista_formatos_suportados():
    with pytest.raises(ValueError, match=".txt"):
        load_documents("arquivo.xls")


def test_carrega_txt(tmp_path):
    f = tmp_path / "doc.txt"
    f.write_text("Conteúdo de teste para indexação.", encoding="utf-8")
    docs = load_documents(str(f))
    assert len(docs) >= 1
    assert "indexação" in docs[0].page_content


def test_carrega_md(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# Título\n\nConteúdo em markdown.", encoding="utf-8")
    docs = load_documents(str(f))
    assert len(docs) >= 1
