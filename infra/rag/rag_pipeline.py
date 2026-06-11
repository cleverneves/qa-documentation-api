from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from infra.providers import get_llm, get_embeddings
from infra.vectorstore.vector_store import load_vectorstore

_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "Use apenas o contexto abaixo para responder à pergunta. "
        "Se a resposta não estiver no contexto, diga que não sabe.\n\n{context}",
    ),
    ("human", "{input}"),
])


def build_rag_pipeline():
    embeddings = get_embeddings()
    vectorstore = load_vectorstore(embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    llm = get_llm()
    combine_docs_chain = create_stuff_documents_chain(llm, _PROMPT)
    return create_retrieval_chain(retriever, combine_docs_chain)
