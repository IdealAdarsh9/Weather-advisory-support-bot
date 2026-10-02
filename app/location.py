from __future__ import annotations

import re
import requests
from .config import REQUEST_TIMEOUT_SECONDS
from .models import Location

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"

STATE_ALIASES = {
    # States
    "andhra pradesh": "Andhra Pradesh",
    "arunachal pradesh": "Arunachal Pradesh",
    "assam": "Assam",
    "bihar": "Bihar",
    "chhattisgarh": "Chhattisgarh",
    "goa": "Goa",
    "gujarat": "Gujarat",
    "haryana": "Haryana",
    "himachal pradesh": "Himachal Pradesh",
    "jharkhand": "Jharkhand",
    "karnataka": "Karnataka",
    "kerala": "Kerala",
    "madhya pradesh": "Madhya Pradesh",
    "maharashtra": "Maharashtra",
    "manipur": "Manipur",
    "meghalaya": "Meghalaya",
    "mizoram": "Mizoram",
    "nagaland": "Nagaland",
    "odisha": "Odisha",
    "punjab": "Punjab",
    "rajasthan": "Rajasthan",
    "sikkim": "Sikkim",
    "tamil nadu": "Tamil Nadu",
    "telangana": "Telangana",
    "tripura": "Tripura",
    "uttar pradesh": "Uttar Pradesh",
    "uttarakhand": "Uttarakhand",
    "west bengal": "West Bengal",

    # Union Territories
    "andaman and nicobar islands": "Andaman and Nicobar Islands",
    "andaman & nicobar islands": "Andaman and Nicobar Islands",
    "chandigarh": "Chandigarh",
    "dadra and nagar haveli and daman and diu": (
        "Dadra and Nagar Haveli and Daman and Diu"
    ),
    "dadra & nagar haveli and daman & diu": (
        "Dadra and Nagar Haveli and Daman and Diu"
    ),
    "delhi": "Delhi",
    "jammu and kashmir": "Jammu and Kashmir",
    "jammu & kashmir": "Jammu and Kashmir",
    "ladakh": "Ladakh",
    "lakshadweep": "Lakshadweep",
    "puducherry": "Puducherry",

    # Common abbreviations
    "ap": "Andhra Pradesh",
    "ar": "Arunachal Pradesh",
    "as": "Assam",
    "br": "Bihar",
    "cg": "Chhattisgarh",
    "ga": "Goa",
    "gj": "Gujarat",
    "hr": "Haryana",
    "hp": "Himachal Pradesh",
    "jh": "Jharkhand",
    "ka": "Karnataka",
    "kl": "Kerala",
    "mp": "Madhya Pradesh",
    "mh": "Maharashtra",
    "mn": "Manipur",
    "ml": "Meghalaya",
    "mz": "Mizoram",
    "nl": "Nagaland",
    "od": "Odisha",
    "pb": "Punjab",
    "rj": "Rajasthan",
    "sk": "Sikkim",
    "tn": "Tamil Nadu",
    "ts": "Telangana",
    "tr": "Tripura",
    "up": "Uttar Pradesh",
    "uk": "Uttarakhand",
    "wb": "West Bengal",
}


def _state_hint(text: str) -> str | None:
    lowered = text.lower()
    for alias, state in STATE_ALIASES.items():
        if re.search(rf"\b{re.escape(alias)}\b", lowered):
            return state
    return None


def resolve_location(query: str) -> Location:
    # Strip common activity/time language if the caller passes the full user message.
    response = requests.get(GEOCODE_URL, params={"name": query, "count": 10, "language": "en", "format": "json"}, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    results = response.json().get("results", [])
    if not results:
        raise LookupError(f"Could not resolve location: {query}")

    state_hint = _state_hint(query)
    country_candidates = [r for r in results if (r.get("country_code") or "").upper() == "IN"]
    candidates = country_candidates or results

    if state_hint:
        state_matches = [r for r in candidates if (r.get("admin1") or "").lower() == state_hint.lower()]
        if state_matches:
            candidates = state_matches

    exact = [r for r in candidates if (r.get("name") or "").lower() == query.strip().lower()]
    candidates = exact or candidates

    # If multiple plausible Indian cities remain and no state hint was supplied,
    # don't silently choose a potentially wrong safety location.
    if len(candidates) > 1 and not state_hint:
        top = candidates[:5]
        labels = [f"{r.get('name')}, {r.get('admin1')}, {r.get('country')}" for r in top]
        raise AmbiguousLocationError(query, labels)

    r = candidates[0]
    return Location(
        name=r.get("name", query),
        latitude=float(r["latitude"]),
        longitude=float(r["longitude"]),
        country=r.get("country"),
        country_code=r.get("country_code"),
        admin1=r.get("admin1"),
        timezone=r.get("timezone") or "auto",
        candidates=[{
            "name": x.get("name"), "admin1": x.get("admin1"), "country": x.get("country"),
            "latitude": x.get("latitude"), "longitude": x.get("longitude")
        } for x in candidates[:5]],
    )


class AmbiguousLocationError(LookupError):
    def __init__(self, query: str, candidates: list[str]):
        self.query = query
        self.candidates = candidates
        super().__init__(f"Ambiguous location '{query}': " + "; ".join(candidates))
