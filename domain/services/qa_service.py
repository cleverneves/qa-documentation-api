from infra.rag.rag_pipeline import build_rag_pipeline


class QAService:

    def __init__(self):
        self.qa_chain = build_rag_pipeline()

    def ask(self, question: str):
        result = self.qa_chain.invoke({"input": question})

        return {
            "answer": result["answer"],
            "sources": [
                doc.metadata for doc in result["context"]
            ]
        }
