from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from core import config


def get_llm():
    return ChatOpenAI(model=config.MODEL_NAME, temperature=0)


def get_embeddings():
    return OpenAIEmbeddings()
