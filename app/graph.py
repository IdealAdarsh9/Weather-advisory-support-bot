from __future__ import annotations

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from .state import GraphState
from .nodes.intent import intent_node
from .nodes.scope import scope_node
from .nodes.location import location_node
from .nodes.weather import weather_node
from .nodes.match import match_node
from .nodes.response import response_node
from .nodes.error import error_node


def route_after_intent(state: GraphState) -> str:
    scope = state.get("intent", {}).get("scope")
    if scope == "safety":
        return "location"
    return "scope"


def route_after_location(state: GraphState) -> str:
    return "error" if state.get("error") else "weather"


def route_after_weather(state: GraphState) -> str:
    return "error" if state.get("error") else "match"


def build_graph():
    graph = StateGraph(GraphState)
    graph.add_node("intent", intent_node)
    graph.add_node("scope", scope_node)
    graph.add_node("location", location_node)
    graph.add_node("weather", weather_node)
    graph.add_node("match", match_node)
    graph.add_node("response", response_node)
    graph.add_node("error", error_node)

    graph.add_edge(START, "intent")
    graph.add_conditional_edges("intent", route_after_intent, {"location": "location", "scope": "scope"})
    graph.add_conditional_edges("location", route_after_location, {"weather": "weather", "error": "error"})
    graph.add_conditional_edges("weather", route_after_weather, {"match": "match", "error": "error"})
    graph.add_edge("match", "response")
    graph.add_edge("scope", END)
    graph.add_edge("response", END)
    graph.add_edge("error", END)

    return graph.compile(checkpointer=MemorySaver())


GRAPH = build_graph()


def invoke(message: str, thread_id: str) -> dict:
    result = GRAPH.invoke(
        {"user_message": message, "trace": []},
        {"configurable": {"thread_id": thread_id}},
    )
    return result
