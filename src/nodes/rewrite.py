from src.states.graphstate import GraphState
from src.llms.geminillm import create_geminillm

llm = create_geminillm()

REWRITE_PROMPT = (
    "look at the input and try to reason about the underlying semantic intent / meaning. \n"
    "Here is the initial quation:"
    "\n---------\n"
    "{question}"
    "\n---------\n"
    "Formulate an improved question: "
)


def rewrite_question(state: GraphState):
    """ Rewrite the original user question"""
    from langchain_core.messages import HumanMessage
    
    messages = state["messages"]
    questoin = messages[0].content
    prompt = REWRITE_PROMPT.format(question=questoin)
    response = llm.invoke([{"role":"user", "content": prompt}])
    return {"messages" : [HumanMessage(content=response.content)]}