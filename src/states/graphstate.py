from langgraph.graph.message import add_messages
from typing_extensions import TypedDict, Annotated
from typing import List


class GraphState(TypedDict):
    """
    Represnt the state of graph with messages.
    """
    messages: Annotated[List, add_messages]
    documents: List = []
    query: str = ""
    context: str = ""
