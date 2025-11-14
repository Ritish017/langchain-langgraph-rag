from langchain_classic.tools.retriever import create_retriever_tool
from src.ingetsion.retriever import create_vectorstore

def get_retriever_tool():
    try:
        retriever = create_vectorstore()
        retriever_tool = create_retriever_tool(
            retriever=retriever,
            name="document_retriever",
            description="Search for information about LangChain and LangGraph from documentation.",
        )
        return retriever_tool
    except Exception as e:
        print(f"Error creating retriever tool: {e}")
        raise
    