from ingestion.loaders.document_loader import load_documents
from ingestion.processors.chunker import get_chunker
from infra.embeddings.embedding_provider import get_embeddings
from infra.vectorstore.vector_store import save_vectorstore
from langchain_community.vectorstores import FAISS

def run_indexing(file_path: str):
    docs = load_documents(file_path)

    chunker = get_chunker()
    chunks = chunker.split_documents(docs)

    embeddings = get_embeddings()

    vectorstore = FAISS.from_documents(chunks, embeddings)

    save_vectorstore(vectorstore)

if __name__ == "__main__":
    run_indexing("data/sample.txt")