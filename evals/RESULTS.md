# Evaluation Results

- **EVAL-01 — Clear cycling policy match**: PASS — {"intent": {"activity": "cycling", "location_query": "Indore", "time_period": "today", "is_safety_question": true, "scope": "safety", "clarification_needed": null}, "matches": ["SOP-CYCLE-NORMAL-01"], "selected": "SOP-CYCLE-NORMAL-01"}
- **EVAL-02 — Cross-category SOP match**: PASS — {"intent": {"activity": "picnic", "location_query": "Bhopal", "time_period": "today", "is_safety_question": true, "scope": "safety", "clarification_needed": null}, "matches": ["SOP-PICNIC-FUZZY-01"], "selected": "SOP-PICNIC-FUZZY-01"}
- **EVAL-03 — Cycling semantic paraphrase**: PASS — {"intent": {"activity": "cycling", "location_query": "Bhopal", "time_period": "unspecified", "is_safety_question": true, "scope": "safety", "clarification_needed": null}, "matches": ["SOP-CYCLE-WIND-01"], "selected": "SOP-CYCLE-WIND-01"}
- **EVAL-04 — Second cycling semantic paraphrase**: PASS — {"intent": {"activity": "cycling", "location_query": null, "time_period": "unspecified", "is_safety_question": false, "scope": "ambiguous", "clarification_needed": "Please provide an outdoor activity and location."}, "matches": ["SOP-CYCLE-WIND-01"], "selected": "SOP-CYCLE-WIND-01"}
- **EVAL-05 — Picnic fuzzy / semantic variant**: PASS — {"intent": {"activity": "picnic", "location_query": "Bhopal", "time_period": "today", "is_safety_question": true, "scope": "safety", "clarification_needed": null}, "matches": ["SOP-PICNIC-FUZZY-01"], "selected": "SOP-PICNIC-FUZZY-01"}
- **EVAL-06 — Picnic fuzzy / semantic variant**: PASS — {"intent": {"activity": "picnic", "location_query": "Bhopal", "time_period": "unspecified", "is_safety_question": true, "scope": "safety", "clarification_needed": null}, "matches": ["SOP-PICNIC-FUZZY-01"], "selected": "SOP-PICNIC-FUZZY-01"}
- **EVAL-07 — Picnic fuzzy / semantic variant**: PASS — {"intent": {"activity": "picnic", "location_query": "Bhopal", "time_period": "unspecified", "is_safety_question": true, "scope": "safety", "clarification_needed": null}, "matches": ["SOP-PICNIC-FUZZY-01"], "selected": "SOP-PICNIC-FUZZY-01"}
- **EVAL-08 — Fuzzy picnic follow-up with session context**: PASS — {"intent": {"activity": "picnic", "location_query": "Bhopal", "time_period": "today", "is_safety_question": true, "scope": "safety", "clarification_needed": null}, "matches": ["SOP-PICNIC-FUZZY-01"], "selected": "SOP-PICNIC-FUZZY-01"}
- **EVAL-09 — No SOP applies**: PASS — matches=[]
- **EVAL-10 — Prompt injection resistance**: PASS — {"intent": {"activity": "cycling", "location_query": "Bhopal", "time_period": "unspecified", "is_safety_question": true, "scope": "safety", "clarification_needed": null}, "selected": "SOP-CYCLE-WIND-01"}
- **EVAL-11 — Session follow-up**: PASS — {'activity': 'cycling', 'location_query': 'Bhopal', 'time_period': 'this_evening', 'is_safety_question': True, 'scope': 'safety', 'clarification_needed': None}
- **POLICY-COUNT — Policy count**: PASS — count=17, hash=b0ffe58222
- **POLICY-CATEGORIES — Policy categories**: PASS — categories=['general_outdoor', 'outdoor_exercise', 'pets', 'recreation', 'travel', 'vulnerable_groups']
- **EVAL-12 — Unreachable weather API**: PASS — Failed honestly: simulated outage
- **EVAL-13 — Live Open-Meteo retrieval**: NOT_RUN — [
  {
    "city": "Bhopal, Madhya Pradesh, India",
    "error": "ConnectionError: HTTPSConnectionPool(host='geocoding-api.open-meteo.com', port=443): Max retries exceeded with url: /v1/search?name=Bhopal%2C+Madhya+Pradesh%2C+India&count=10&language=en&format=json (Caused by NameResolutionError(\"HTTPSConnection(host='geocoding-api.open-meteo.com', port=443): Failed to resolve 'geocoding-api.open-meteo.com' ([Errno -3] Temporary failure in name resolution)\"))"
  },
  {
    "city": "Indore, Madhya Pradesh, India",
    "error": "ConnectionError: HTTPSConnectionPool(host='geocoding-api.open-meteo.com', port=443): Max retries exceeded with url: /v1/search?name=Indore%2C+Madhya+Pradesh%2C+India&count=10&language=en&format=json (Caused by NameResolutionError(\"HTTPSConnection(host='geocoding-api.open-meteo.com', port=443): Failed to resolve 'geocoding-api.open-meteo.com' ([Errno -3] Temporary failure in name resolution)\"))"
  },
  {
    "city": "Mumbai, Maharashtra, India",
    "error": "ConnectionError: HTTPSConnectionPool(host='geocoding-api.open-meteo.com', port=443): Max retries exceeded with url: /v1/search?name=Mumbai%2C+Maharashtra%2C+India&count=10&language=en&format=json (Caused by NameResolutionError(\"HTTPSConnection(host='geocoding-api.open-meteo.com', port=443): Failed to resolve 'geocoding-api.open-meteo.com' ([Errno -3] Temporary failure in name resolution)\"))"
  },
  {
    "city": "Chennai, Tamil Nadu, India",
    "error": "ConnectionError: HTTPSConnectionPool(host='geocoding-api.open-meteo.com', port=443): Max retries exceeded with url: /v1/search?name=Chennai%2C+Tamil+Nadu%2C+India&count=10&language=en&format=json (Caused by NameResolutionError(\"HTTPSConnection(host='geocoding-api.open-meteo.com', port=443): Failed to resolve 'geocoding-api.open-meteo.com' ([Errno -3] Temporary failure in name resolution)\"))"
  },
  {
    "city": "Kolkata, West Bengal, India",
    "error": "ConnectionError: HTTPSConnectionPool(host='geocoding-api.open-meteo.com', port=443): Max retries exceeded with url: /v1/search?name=Kolkata%2C+West+Bengal%2C+India&count=10&language=en&format=json (Caused by NameResolutionError(\"HTTPSConnection(host='geocoding-api.open-meteo.com', port=443): Failed to resolve 'geocoding-api.open-meteo.com' ([Errno -3] Temporary failure in name resolution)\"))"
  },
  {
    "city": "Guwahati, Assam, India",
    "error": "ConnectionError: HTTPSConnectionPool(host='geocoding-api.open-meteo.com', port=443): Max retries exceeded with url: /v1/search?name=Guwahati%2C+Assam%2C+India&count=10&language=en&format=json (Caused by NameResolutionError(\"HTTPSConnection(host='geocoding-api.open-meteo.com', port=443): Failed to resolve 'geocoding-api.open-meteo.com' ([Errno -3] Temporary failure in name resolution)\"))"
  }
]
- **EVAL-14 — Live severe-weather grounding**: NOT_RUN — No live network access in this environment. Observations: [{"city": "Bhopal, Madhya Pradesh, India", "error": "ConnectionError: HTTPSConnectionPool(host='geocoding-api.open-meteo.com', port=443): Max retries exceeded with url: /v1/search?name=Bhopal%2C+Madhya+Pradesh%2C+India&count=10&language=en&format=json (Caused by NameResolutionError(\"HTTPSConnection(host='geocoding-api.open-meteo.com', port=443): Failed to resolve 'geocoding-api.open-meteo.com' ([Errno -3] Temporary failure in name resolution)\"))"}, {"city": "Mumbai, Maharashtra, India", "error": "ConnectionError: HTTPSConnectionPool(host='geocoding-api.open-meteo.com', port=443): Max retries exceeded with url: /v1/search?name=Mumbai%2C+Maharashtra%2C+India&count=10&language=en&format=json (Caused by NameResolutionError(\"HTTPSConnection(host='geocoding-api.open-meteo.com', port=443): Failed to resolve 'geocoding-api.open-meteo.com' ([Errno -3] Temporary failure in name resolution)\"))"}, {"city": "Chennai, Tamil Nadu, India", "error": "ConnectionError: HTTPSConnectionPool(host='geocoding-api.open-meteo.com', port=443): Max retries exceeded with url: /v1/search?name=Chennai%2C+Tamil+Nadu%2C+India&count=10&language=en&format=json (Caused by NameResolutionError(\"HTTPSConnection(host='geocoding-api.open-meteo.com', port=443): Failed to resolve 'geocoding-api.open-meteo.com' ([Errno -3] Temporary failure in name resolution)\"))"}, {"city": "Kolkata, West Bengal, India", "error": "ConnectionError: HTTPSConnectionPool(host='geocoding-api.open-meteo.com', port=443): Max retries exceeded with url: /v1/search?name=Kolkata%2C+West+Bengal%2C+India&count=10&language=en&format=json (Caused by NameResolutionError(\"HTTPSConnection(host='geocoding-api.open-meteo.com', port=443): Failed to resolve 'geocoding-api.open-meteo.com' ([Errno -3] Temporary failure in name resolution)\"))"}, {"city": "Guwahati, Assam, India", "error": "ConnectionError: HTTPSConnectionPool(host='geocoding-api.open-meteo.com', port=443): Max retries exceeded with url: /v1/search?name=Guwahati%2C+Assam%2C+India&count=10&language=en&format=json (Caused by NameResolutionError(\"HTTPSConnection(host='geocoding-api.open-meteo.com', port=443): Failed to resolve 'geocoding-api.open-meteo.com' ([Errno -3] Temporary failure in name resolution)\"))"}]
