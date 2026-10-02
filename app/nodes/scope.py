from __future__ import annotations
from ..state import GraphState


def scope_node(state: GraphState) -> GraphState:
    intent = state["intent"]
    scope = intent.get("scope")
    if scope == "general_weather":
        return {"response": "I can provide weather-based outdoor safety guidance, but I don't provide general weather forecasts. Ask about an activity and location, for example: 'Is it safe to cycle in Bhopal today?'"}
    if scope in {"unsupported", "ambiguous"}:
        clarification = intent.get("clarification_needed") or "Please provide an outdoor activity and location so I can check the live weather against our safety policies."
        return {"response": clarification}
    return {}
