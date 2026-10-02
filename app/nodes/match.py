from __future__ import annotations
from ..config import POLICY_PATH
from ..models import UserIntent, WeatherSnapshot
from ..sop_loader import load_sops
from ..sop_matcher import match_sops, select_sop
from ..state import GraphState


def match_node(state: GraphState) -> GraphState:
    sops, policy_hash = load_sops(POLICY_PATH)
    intent = UserIntent.model_validate(state["intent"])
    weather = WeatherSnapshot.model_validate(state["weather"])
    matches = match_sops(sops, intent, weather)
    selected = select_sop(matches)
    decision = {
        "status": "matched" if selected else "no_match",
        "selected": selected.model_dump() if selected else None,
        "all_matches": [m.model_dump() for m in matches],
        "policy_set_hash": policy_hash,
    }
    trace = list(state.get("trace", []))
    trace.append(f"policy: selected={selected.sop.id if selected else None}; matches={[m.sop.id for m in matches]}")
    return {"decision": decision, "trace": trace}
