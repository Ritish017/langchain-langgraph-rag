from src.llms.geminillm import create_geminillm
from src.states.graphstate import GraphState


def generate_answer(state: GraphState):
    """ Generate an answer"""
    from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
    
    question = state["messages"][0].content
    
    # Check if we have valid context
    if len(state["messages"]) > 1 and state["messages"][-1].content:
        context = state["messages"][-1].content
    else:
        context = "No relevant context found."
    
    # Skip if context is empty or just whitespace
    if not context.strip():
        return {"messages": [AIMessage(content="I'm sorry, I couldn't find relevant information to answer your question.")]}
    
    # Build the user message with context and question
    user_message = f"Context: {context}\n\nQuestion: {question}"
    
    llm = create_geminillm()
    
    try:
        # Use system message + human message pattern for better results
        system_prompt = (
            "You are a helpful assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer the question clearly and concisely. "
            "Provide a well-structured, human-readable response. "
            "If you don't know the answer, just say that you don't know. "
            "Format your response in clear paragraphs with proper spacing."
        )
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message)
        ])
        return {"messages": [AIMessage(content=response.content)]}
    except Exception as e:
        return {"messages": [AIMessage(content=f"I encountered an error while generating the response: {str(e)}")]}
