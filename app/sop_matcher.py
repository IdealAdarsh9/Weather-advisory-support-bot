from __future__ import annotations

from typing import Any
from .models import SOP, SOPMatch, UserIntent, WeatherSnapshot

SEVERITY_ORDER = {"LOW": 1, "MODERATE": 2, "HIGH": 3, "EXTREME": 4}


def _normalize_activity(activity: str | None) -> str:
    if not activity:
        return ""
    a = activity.lower().strip()
    aliases = {
        "bicycle": "cycling", "bike": "cycling", "biking": "cycling", "cycling": "cycling",
        "jogging": "running", "run": "running", "running": "running",
        "walk": "walking", "walking": "walking", "hike": "hiking", "hiking": "hiking",
        "commute": "travel", "commuting": "travel", "travel": "travel",
        "picnic": "picnic", "park": "park", "children": "children", "kids": "children",
        "elderly": "elderly", "pet": "pets", "pets": "pets",
    }
    return aliases.get(a, a)


def _activity_matches(intent: UserIntent, sop: SOP) -> bool:
    activity = _normalize_activity(intent.activity)
    if not sop.intent_any:
        return True
    candidates = {_normalize_activity(x) for x in sop.intent_any}
    if activity in candidates:
        return True
    if activity == "travel" and "commute" in candidates:
        return True
    return False


def _compare(actual: Any, op: str, expected: Any) -> bool:
    if actual is None:
        return False
    if op == ">=": return actual >= expected
    if op == ">": return actual > expected
    if op == "<=": return actual <= expected
    if op == "<": return actual < expected
    if op == "==": return actual == expected
    if op == "!=": return actual != expected
    if op == "in": return actual in expected
    if op == "not_in": return actual not in expected
    return False


def _weather_value(weather: WeatherSnapshot, field: str):
    mapping = {
        "temperature": weather.temperature_c,
        "temperature_c": weather.temperature_c,
        "wind_speed": weather.wind_speed_kmh,
        "wind_speed_kmh": weather.wind_speed_kmh,
        "precipitation": weather.precipitation_mm,
        "precipitation_mm": weather.precipitation_mm,
        "precipitation_probability": weather.precipitation_probability_pct,
        "precipitation_probability_pct": weather.precipitation_probability_pct,
        "uv_index": weather.uv_index,
        "weather_code": weather.weather_code,
        "daily_precipitation": weather.daily_precipitation_mm,
    }
    return mapping.get(field)


def match_sops(sops: list[SOP], intent: UserIntent, weather: WeatherSnapshot) -> list[SOPMatch]:
    matches: list[SOPMatch] = []
    for sop in sops:
        if not _activity_matches(intent, sop):
            continue
        reasons: list[str] = []
        ok = True
        for condition in sop.weather_all:
            field = condition.get("field")
            op = condition.get("op")
            expected = condition.get("value")
            actual = _weather_value(weather, field)
            if not _compare(actual, op, expected):
                ok = False
                break
            reasons.append(f"{field} {op} {expected} (actual {actual})")
        if ok:
            matches.append(SOPMatch(sop=sop, matched_conditions=reasons))
    return matches


def select_sop(matches: list[SOPMatch]) -> SOPMatch | None:
    if not matches:
        return None
    return sorted(matches, key=lambda m: (SEVERITY_ORDER[m.sop.severity], m.sop.priority), reverse=True)[0]
