"""
Simplified Graph Builder without document grading
This version always proceeds to answer generation after retrieval
"""

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from src.states.graphstate import GraphState
from src.nodes.generate import generate_answer
from src.ingetsion.retriever_tool import get_retriever_tool
from src.nodes.generator import generate_query_or_respond

# Create the workflow
workflow = StateGraph(GraphState)

# Add nodes
workflow.add_node("generate_query_or_respond", generate_query_or_respond)
workflow.add_node("retrieve", ToolNode([get_retriever_tool()]))
workflow.add_node("generate_answer", generate_answer)

# Add edges
workflow.add_edge(START, "generate_query_or_respond")

# Conditional edge: either use tools (retrieve) or end
workflow.add_conditional_edges(
    "generate_query_or_respond",
    tools_condition,
    {
        "tools": "retrieve",
        END: END,
    },
)

# After retrieval, always go to answer generation
workflow.add_edge("retrieve", "generate_answer")
workflow.add_edge("generate_answer", END)

# Compile the graph
simple_graph = workflow.compile()

print("✅ Simplified graph created successfully (without grader)")