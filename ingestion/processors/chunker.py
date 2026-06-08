from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_chunker():
    return RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
