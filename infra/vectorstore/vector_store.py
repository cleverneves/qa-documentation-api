from langchain_community.vectorstores import FAISS
import os

VECTOR_DB_PATH = "data/vectorstore"


def save_vectorstore(vectorstore):
    os.makedirs(VECTOR_DB_PATH, exist_ok=True)
    vectorstore.save_local(VECTOR_DB_PATH)


def load_vectorstore(embeddings):
    if not os.path.exists(VECTOR_DB_PATH):
        raise FileNotFoundError(
            f"Vector store não encontrado em '{VECTOR_DB_PATH}'. "
            "Execute a ingestão antes de iniciar a API:\n"
            "  python -m ingestion.indexer --file data/sample.txt"
        )
    return FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
