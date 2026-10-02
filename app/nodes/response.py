from __future__ import annotations
from ..llm import generate_response
from ..models import Decision, UserIntent, WeatherSnapshot
from ..state import GraphState


def response_node(state: GraphState) -> GraphState:
    intent = UserIntent.model_validate(state["intent"])
    weather = WeatherSnapshot.model_validate(state["weather"])
    decision = Decision.model_validate(state["decision"])
    response = generate_response(state["user_message"], intent, weather, decision)
    trace = list(state.get("trace", []))
    trace.append("response: generated from trusted policy/weather facts")
    return {"response": response, "trace": trace}
