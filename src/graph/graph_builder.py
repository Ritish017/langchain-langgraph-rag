from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from src.states.graphstate import GraphState
from src.nodes.generate import generate_answer
from src.nodes.grader import grade_documents    
from src.ingetsion.retriever_tool import get_retriever_tool
from src.nodes.generator import generate_query_or_respond
from src.nodes.rewrite import rewrite_question
from src.ingetsion.retriever_tool import get_retriever_tool

workflow = StateGraph(GraphState)

workflow.add_node("generate_query_or_respond", generate_query_or_respond)
workflow.add_node("retrieve", ToolNode([get_retriever_tool()]))
workflow.add_node("rewrite_question", rewrite_question)
workflow.add_node("generate_answer", generate_answer)

workflow.add_edge(START, "generate_query_or_respond")
workflow.add_conditional_edges(
    "generate_query_or_respond",
    tools_condition,
    {
        "tools": "retrieve",
        END: END,
    },
)

workflow.add_conditional_edges(
    "retrieve",
    grade_documents,
    {
        "generate_answer": "generate_answer",
        "rewrite_question": "rewrite_question",
    },
)
workflow.add_edge("generate_answer", END)
workflow.add_edge("rewrite_question", "generate_query_or_respond")
graph = workflow.compile()

# Optional: Display graph visualization (uncomment if needed in Jupyter)
# from IPython.display import Image, display
# display(Image(graph.get_graph().draw_mermaid_png()))