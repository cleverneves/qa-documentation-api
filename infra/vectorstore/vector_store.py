from langchain_community.vectorstores import FAISS
import os

VECTOR_DB_PATH = "data/vectorstore"


def save_vectorstore(vectorstore):
    os.makedirs(VECTOR_DB_PATH, exist_ok=True)
    vectorstore.save_local(VECTOR_DB_PATH)


def load_vectorstore(embeddings):
    return FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
