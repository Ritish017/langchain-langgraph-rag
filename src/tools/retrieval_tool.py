from langchain_classic.tools.retriever import create_retriever_tool
from src.ingetsion.retriever import create_vectorstore

def get_retriever_tool():
    retriever = create_vectorstore()
    retriever_tool = create_retriever_tool(
        retriever=retriever,
        name="Document Retriever",
        description="Useful for retrieving documents relevant to a user's query.",
    )
    return retriever_tool
