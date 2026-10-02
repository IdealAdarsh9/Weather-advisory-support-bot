from __future__ import annotations
from typing import Any, TypedDict


class GraphState(TypedDict, total=False):
    user_message: str
    intent: dict[str, Any]
    location: dict[str, Any]
    weather: dict[str, Any]
    decision: dict[str, Any]
    response: str
    error: str
    trace: list[str]
