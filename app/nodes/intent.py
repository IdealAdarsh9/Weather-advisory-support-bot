from __future__ import annotations
from ..llm import extract_intent
from ..state import GraphState


def intent_node(state: GraphState) -> GraphState:
    current = extract_intent(state["user_message"])
    previous = state.get("intent") or {}

    # Session context: fill missing follow-up details from the previous turn.
    if current.location_query is None:
        current.location_query = previous.get("location_query")
    if current.activity is None:
        current.activity = previous.get("activity")
    if current.time_period == "unspecified" and previous.get("time_period"):
        # Keep unspecified only when the follow-up truly has no temporal phrase.
        current.time_period = previous.get("time_period")

    if current.activity and current.location_query:
        current.scope = "safety"
        current.is_safety_question = True
        current.clarification_needed = None

    trace = list(state.get("trace", []))
    trace.append(f"intent: {current.model_dump()}")
    return {"intent": current.model_dump(), "error": None, "response": None, "weather": None, "decision": None, "trace": trace}
