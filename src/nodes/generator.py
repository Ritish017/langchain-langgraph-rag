from src.ingetsion.retriever_tool import get_retriever_tool
from src.llms.geminillm import create_geminillm
from langchain_core.messages import SystemMessage

geminillm = create_geminillm()

def generate_query_or_respond(state):
    """Call the model to generate a response based on the current state. Given
    the question, it will decide to retrieve using the retriever tool, or simply respond to the user.
    """
    
    retriever_tool = get_retriever_tool()
    
    # Add system message to guide the LLM's behavior
    system_prompt = SystemMessage(
        content="""You are a helpful AI assistant with expertise in LangChain and LangGraph.

**Response Strategy:**

1. **For LangChain/LangGraph specific questions** (implementations, code examples, architecture):
   - Use the document_retriever tool to search documentation
   - Provide detailed answers based on retrieved context

2. **For general questions** (math, definitions, basic concepts):
   - Answer directly using your knowledge
   - Be concise and accurate
   - No need to retrieve documents

**Examples:**
- "What is 2+2?" → Answer directly: "4"
- "What is Machine Learning?" → Answer directly with definition
- "What is AI?" → Answer directly with definition
- "How to implement RAG in LangChain?" → Use document_retriever tool
- "What is StateGraph in LangGraph?" → Use document_retriever tool

Provide helpful, accurate responses. Only decline if the question is harmful or completely outside your capabilities."""
    )
    
    # Prepend system message to the conversation
    messages = [system_prompt] + state["messages"]
    
    response = (
        geminillm
        .bind_tools([retriever_tool])
        .invoke(messages)
    )
    return {"messages": [response]}


