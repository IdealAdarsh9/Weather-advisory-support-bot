from __future__ import annotations

from typing import Any, Literal, Optional
from pydantic import BaseModel, Field


Severity = Literal["LOW", "MODERATE", "HIGH", "EXTREME"]


class UserIntent(BaseModel):
    activity: Optional[str] = None
    location_query: Optional[str] = None
    time_period: Literal["now", "today", "this_evening", "tomorrow", "unspecified"] = "unspecified"
    is_safety_question: bool = False
    scope: Literal["safety", "general_weather", "unsupported", "ambiguous"] = "ambiguous"
    clarification_needed: Optional[str] = None


class Location(BaseModel):
    name: str
    latitude: float
    longitude: float
    country: Optional[str] = None
    country_code: Optional[str] = None
    admin1: Optional[str] = None
    timezone: str = "auto"
    candidates: list[dict[str, Any]] = Field(default_factory=list)


class WeatherSnapshot(BaseModel):
    location: Location
    period: str
    timestamp: str
    temperature_c: Optional[float] = None
    wind_speed_kmh: Optional[float] = None
    precipitation_mm: Optional[float] = None
    precipitation_probability_pct: Optional[float] = None
    uv_index: Optional[float] = None
    weather_code: Optional[int] = None
    daily_precipitation_mm: Optional[float] = None
    source: str = "Open-Meteo"
    fetched_at_utc: str


class SOP(BaseModel):
    id: str
    name: str
    category: str
    description: str
    severity: Severity
    priority: int = 0
    intent_any: list[str] = Field(default_factory=list)
    weather_all: list[dict[str, Any]] = Field(default_factory=list)
    advice: str
    rationale: str


class SOPMatch(BaseModel):
    sop: SOP
    matched_conditions: list[str] = Field(default_factory=list)


class Decision(BaseModel):
    status: Literal["matched", "no_match"]
    selected: Optional[SOPMatch] = None
    all_matches: list[SOPMatch] = Field(default_factory=list)
    policy_set_hash: str


class BotState(BaseModel):
    user_message: str
    intent: Optional[UserIntent] = None
    location: Optional[Location] = None
    weather: Optional[WeatherSnapshot] = None
    decision: Optional[Decision] = None
    response: Optional[str] = None
    error: Optional[str] = None
    trace: list[str] = Field(default_factory=list)
