from pathlib import Path
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader

_LOADERS = {
    ".txt": lambda p: TextLoader(p, encoding="utf-8"),
    ".md":  lambda p: TextLoader(p, encoding="utf-8"),
    ".pdf": lambda p: PyPDFLoader(p),
    ".docx": lambda p: Docx2txtLoader(p),
}


def load_documents(path: str):
    ext = Path(path).suffix.lower()
    if ext not in _LOADERS:
        supported = ", ".join(_LOADERS)
        raise ValueError(
            f"Formato '{ext}' não suportado. Formatos aceitos: {supported}"
        )
    return _LOADERS[ext](path).load()