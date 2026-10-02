from __future__ import annotations
from ..location import AmbiguousLocationError, resolve_location
from ..state import GraphState


def location_node(state: GraphState) -> GraphState:
    intent = state["intent"]
    query = intent.get("location_query")
    if not query:
        return {"error": "LOCATION:I need a location before I can check live weather."}
    try:
        location = resolve_location(query)
    except AmbiguousLocationError as exc:
        candidates = "; ".join(exc.candidates[:4])
        return {"error": f"AMBIGUOUS_LOCATION:{candidates}"}
    except Exception as exc:
        return {"error": f"LOCATION:location lookup failed ({type(exc).__name__})"}
    trace = list(state.get("trace", []))
    trace.append(f"location: {location.name}, {location.admin1}, {location.country}")
    return {"location": location.model_dump(), "trace": trace}
