from typing import Type
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from .state import GraphState
from .nodes import llm_node, parse_node, repair_node

MAX_RETRIES = 2

def should_retry(state: GraphState):
    if state["parsed"] is not None:
        return "end"
    if state["retries"] >= MAX_RETRIES:
        return "end"
    return "repair"

def build_graph(llm, schema: Type[BaseModel]):
    graph = StateGraph(GraphState)

    graph.add_node("llm", lambda s : llm_node(s, llm))
    graph.add_node("parse", lambda s: parse_node(s, schema))
    graph.add_node("repair", lambda s: repair_node(s, llm, schema))

    graph.set_entry_point("llm")
    graph.add_edge("llm", "parse")

    graph.add_conditional_edges(
        "parse",
        should_retry,
        {"repair": "repair", "end": END},
    )

    graph.add_edge("repair", "parse")

    return graph.compile()