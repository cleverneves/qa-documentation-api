import argparse
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ingestion.loaders.document_loader import load_documents
from infra.providers import get_embeddings
from infra.vectorstore.vector_store import save_vectorstore
from langchain_community.vectorstores import FAISS

_CHUNKER = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)


def run_indexing(file_path: str):
    print(f"Carregando documento: {file_path}")
    docs = load_documents(file_path)

    chunks = _CHUNKER.split_documents(docs)
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