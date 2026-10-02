from __future__ import annotations
from ..state import GraphState


def error_node(state: GraphState) -> GraphState:
    error = state.get("error", "Unknown error")
    if error.startswith("AMBIGUOUS_LOCATION:"):
        return {"response": error.replace("AMBIGUOUS_LOCATION:", "I found more than one plausible location. Please specify the state or country, for example: ")}
    if error.startswith("LOCATION:"):
        return {"response": error.replace("LOCATION:", "I couldn't resolve that location. Please provide a city and, if needed, a state or country. ")}
    if error.startswith("WEATHER:"):
        return {"response": error.replace("WEATHER:", "I couldn't retrieve live weather data for that request. I won't guess at the weather or provide an ungrounded safety recommendation. ")}
    if error.startswith("POLICY:"):
        return {"response": "I couldn't evaluate the safety policies reliably, so I won't provide a safety recommendation. Please try again shortly."}
    return {"response": "I couldn't answer safely because a required data step failed. Please try again shortly."}
