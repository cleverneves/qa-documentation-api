import argparse
from ingestion.loaders.document_loader import load_documents
from ingestion.processors.chunker import get_chunker
from infra.embeddings.embedding_provider import get_embeddings
from infra.vectorstore.vector_store import save_vectorstore
from langchain_community.vectorstores import FAISS


def run_indexing(file_path: str):
    print(f"Carregando documento: {file_path}")
    docs = load_documents(file_path)

    chunker = get_chunker()
    chunks = chunker.split_documents(docs)
    print(f"{len(chunks)} chunks gerados.")

    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)

    save_vectorstore(vectorstore)
    print("Vector store salvo em data/vectorstore/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Indexa um documento no vector store.")
    parser.add_argument(
        "--file",
        default="data/sample.txt",
        help="Caminho para o arquivo a indexar (padrão: data/sample.txt)",
    )
    args = parser.parse_args()
    run_indexing(args.file)