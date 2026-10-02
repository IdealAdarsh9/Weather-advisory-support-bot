from app.models import Location, UserIntent, WeatherSnapshot
from app.sop_loader import load_sops
from app.sop_matcher import match_sops, select_sop
from app.config import POLICY_PATH


def weather(**kwargs):
    base = dict(
        location=Location(name="Bhopal", latitude=23.2, longitude=77.4, country="India"),
        period="today", timestamp="synthetic", temperature_c=27, wind_speed_kmh=10,
        precipitation_mm=0, precipitation_probability_pct=20, uv_index=5, weather_code=1,
        daily_precipitation_mm=2, fetched_at_utc="synthetic",
    )
    base.update(kwargs)
    return WeatherSnapshot(**base)


def test_policy_count_and_categories():
    sops, _ = load_sops(POLICY_PATH)
    assert len(sops) >= 10
    assert len({s.category for s in sops}) >= 3


def test_high_wind_cycling():
    sops, _ = load_sops(POLICY_PATH)
    intent = UserIntent(activity="cycling", location_query="Bhopal", scope="safety", is_safety_question=True)
    selected = select_sop(match_sops(sops, intent, weather(wind_speed_kmh=45)))
    assert selected.sop.id == "SOP-CYCLE-WIND-01"


def test_paraphrased_cycling_is_normalized():
    from app.llm import heuristic_intent
    intent = heuristic_intent("Would riding my bicycle to work in Bhopal be okay?")
    assert intent.activity == "cycling"
    assert intent.location_query == "Bhopal"


def test_picnic_fuzzy_combination():
    sops, _ = load_sops(POLICY_PATH)
    intent = UserIntent(activity="picnic", location_query="Bhopal", scope="safety", is_safety_question=True)
    selected = select_sop(match_sops(sops, intent, weather()))
    assert selected.sop.id == "SOP-PICNIC-FUZZY-01"


def test_no_sop_for_unsupported_activity():
    sops, _ = load_sops(POLICY_PATH)
    intent = UserIntent(activity="skateboarding", location_query="Bhopal", scope="safety", is_safety_question=True)
    assert match_sops(sops, intent, weather()) == []


def test_multiple_matches_are_ranked_by_severity():
    sops, _ = load_sops(POLICY_PATH)
    intent = UserIntent(activity="cycling", location_query="Bhopal", scope="safety", is_safety_question=True)
    selected = select_sop(match_sops(sops, intent, weather(wind_speed_kmh=45, precipitation_probability_pct=80, uv_index=9)))
    assert selected.sop.id == "SOP-CYCLE-WIND-01"


def test_picnic_semantic_paraphrase_without_keyword():
    from app.llm import heuristic_intent

    phrases = [
        "Would this be a nice day to sit outside and have lunch in Bhopal?",
        "Thinking of having a family picnic outdoors in Bhopal today. Good idea?",
        "Is the weather suitable for spending a few hours outside on a blanket?",
    ]

    for phrase in phrases:
        intent = heuristic_intent(phrase)
        assert intent.activity == "picnic", phrase


def test_generic_outdoor_model_output_is_promoted_to_picnic_for_semantic_phrase():
    from app.llm import _normalize_extracted_intent

    intent = UserIntent(
        activity="outdoor_activity",
        location_query="Bhopal",
        scope="ambiguous",
        is_safety_question=False,
    )
    normalized = _normalize_extracted_intent(
        intent,
        "Is the weather suitable for spending a few hours outside on a blanket?",
    )
    assert normalized.activity == "picnic"
    assert normalized.scope == "safety"
    assert normalized.is_safety_question is True
