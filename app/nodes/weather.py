from __future__ import annotations

from ..models import Location
from ..state import GraphState
from ..weather import fetch_weather


def weather_node(state: GraphState) -> GraphState:
    """Fetch weather using the trusted Location model reconstructed from graph state."""
    intent = state["intent"]
    raw_location = state.get("location")

    if not raw_location:
        return {"error": "LOCATION:No resolved location is available."}

    try:
        # GraphState stores serializable dictionaries, while fetch_weather expects
        # a Pydantic Location model. Reconstruct it at the trust boundary.
        location = Location.model_validate(raw_location)
        weather = fetch_weather(
            location,
            intent.get("time_period", "unspecified"),
        )
    except Exception as exc:
        return {
            "error": (
                "WEATHER:Open-Meteo request failed "
                f"({type(exc).__name__}): {exc}"
            )
        }

    trace = list(state.get("trace", []))
    trace.append(f"weather: {weather.model_dump()}")
    return {"weather": weather.model_dump(), "trace": trace}
