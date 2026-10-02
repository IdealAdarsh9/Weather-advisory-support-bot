from __future__ import annotations

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests

from .config import REQUEST_TIMEOUT_SECONDS
from .models import Location, WeatherSnapshot

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

HOURLY_FIELDS = ",".join(
    [
        "temperature_2m",
        "wind_speed_10m",
        "precipitation",
        "precipitation_probability",
        "uv_index",
        "weather_code",
    ]
)

DAILY_FIELDS = "precipitation_sum,weather_code,wind_speed_10m_max"


def _safe_zoneinfo(name: str | None) -> ZoneInfo:
    try:
        return ZoneInfo(name or "UTC")
    except Exception:
        return ZoneInfo("UTC")


def _pick_hour_index(times: list[str], period: str, timezone_name: str) -> int:
    if not times:
        raise ValueError("Open-Meteo returned no hourly timestamps")

    tz = _safe_zoneinfo(timezone_name)
    now = datetime.now(tz)
    parsed: list[datetime] = []

    for raw in times:
        try:
            value = datetime.fromisoformat(raw)
            if value.tzinfo is None:
                value = value.replace(tzinfo=tz)
            parsed.append(value)
        except ValueError as exc:
            raise ValueError(f"Invalid Open-Meteo timestamp: {raw!r}") from exc

    if period == "this_evening":
        target = now.replace(hour=19, minute=0, second=0, microsecond=0)
        if target < now:
            target += timedelta(days=1)
    elif period == "tomorrow":
        target = (now + timedelta(days=1)).replace(
            hour=12, minute=0, second=0, microsecond=0
        )
    else:
        target = now

    candidates = [
        (abs((timestamp - target).total_seconds()), index)
        for index, timestamp in enumerate(parsed)
        if timestamp >= now - timedelta(minutes=30)
    ]
    if not candidates:
        candidates = [
            (abs((timestamp - target).total_seconds()), index)
            for index, timestamp in enumerate(parsed)
        ]

    return min(candidates, key=lambda pair: pair[0])[1]


def fetch_weather(location: Location, period: str) -> WeatherSnapshot:
    """Fetch live Open-Meteo data. No LLM is involved in this step."""
    params = {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "hourly": HOURLY_FIELDS,
        "daily": DAILY_FIELDS,
        "timezone": "auto",
        "forecast_days": 3,
    }

    try:
        response = requests.get(
            FORECAST_URL,
            params=params,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        raise RuntimeError(f"network error: {exc}") from exc
    except ValueError as exc:
        raise RuntimeError("Open-Meteo returned invalid JSON") from exc

    timezone_name = data.get("timezone") or location.timezone or "UTC"
    hourly = data.get("hourly")
    if not isinstance(hourly, dict):
        raise RuntimeError("Open-Meteo response has no valid hourly data")

    times = hourly.get("time")
    if not isinstance(times, list) or not times:
        raise RuntimeError("Open-Meteo returned no hourly forecast timestamps")

    idx = _pick_hour_index(times, period, timezone_name)

    def value(key: str):
        values = hourly.get(key)
        if not isinstance(values, list) or idx >= len(values):
            return None
        return values[idx]

    daily = data.get("daily") or {}
    daily_precip = daily.get("precipitation_sum") or []
    daily_index = 1 if period == "tomorrow" else 0
    daily_total = (
        daily_precip[daily_index]
        if isinstance(daily_precip, list) and daily_index < len(daily_precip)
        else None
    )

    return WeatherSnapshot(
        location=location,
        period=period,
        timestamp=times[idx],
        temperature_c=value("temperature_2m"),
        wind_speed_kmh=value("wind_speed_10m"),
        precipitation_mm=value("precipitation"),
        precipitation_probability_pct=value("precipitation_probability"),
        uv_index=value("uv_index"),
        weather_code=value("weather_code"),
        daily_precipitation_mm=daily_total,
        source="Open-Meteo",
        fetched_at_utc=datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
    )
