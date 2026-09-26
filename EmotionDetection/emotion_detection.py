"""Emotion detection helpers using IBM Watson Natural Language Understanding."""

import os
from typing import Any

try:
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    from ibm_watson import NaturalLanguageUnderstandingV1
    from ibm_watson.natural_language_understanding_v1 import (
        EmotionOptions,
        Features,
    )
except ImportError:  # pragma: no cover - optional dependency for local fallback
    IAMAuthenticator = None
    NaturalLanguageUnderstandingV1 = None
    EmotionOptions = None
    Features = None

EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def _empty_result() -> dict[str, Any]:
    """Return the required shape for invalid or empty input."""
    return {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
    }


def _normalize_score(value: Any) -> float:
    """Convert IBM or heuristic values into a float score."""
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _dominant_emotion(scores: dict[str, float]) -> str | None:
    """Return the name of the highest-scoring emotion."""
    if not scores or all(score == 0.0 for score in scores.values()):
        return None
    return max(scores, key=scores.get)


def _parse_watson_response(raw_response: Any) -> dict[str, Any] | None:
    """Convert IBM Watson output into a dictionary of emotion scores."""
    if raw_response is None:
        return None

    if hasattr(raw_response, "status_code") and raw_response.status_code == 400:
        return _empty_result()

    if hasattr(raw_response, "get_result"):
        raw_response = raw_response.get_result()
    if hasattr(raw_response, "result"):
        raw_response = raw_response.result

    if not isinstance(raw_response, dict):
        return None

    if raw_response.get("status") == 400 or raw_response.get("status_code") == 400:
        return _empty_result()

    emotion_data = raw_response.get("emotion", {})
    if isinstance(emotion_data, dict):
        document = emotion_data.get("document", {})
        if isinstance(document, dict):
            emotion_values = document.get("emotion", {})
        else:
            emotion_values = {}
    else:
        emotion_values = {}

    if not isinstance(emotion_values, dict):
        return None

    scores = {emotion: _normalize_score(emotion_values.get(emotion, 0.0)) for emotion in EMOTIONS}
    dominant = _dominant_emotion(scores)
    return {
        "anger": scores.get("anger"),
        "disgust": scores.get("disgust"),
        "fear": scores.get("fear"),
        "joy": scores.get("joy"),
        "sadness": scores.get("sadness"),
        "dominant_emotion": dominant,
    }


def _keyword_fallback(text: str) -> dict[str, Any]:
    """Match a few common emotion phrases when no Watson service is configured."""
    lowered = text.lower()
    keyword_map = {
        "joy": ["glad", "happy", "joyful", "delighted", "excited", "pleased", "great"],
        "anger": ["mad", "angry", "furious", "rage", "annoyed", "upset"],
        "fear": ["afraid", "scared", "fear", "panic", "nervous", "terrified"],
        "disgust": ["disgusted", "gross", "nasty", "repulsed", "revolted"],
        "sadness": ["sad", "depressed", "unhappy", "miserable", "upset", "crying"],
    }

    scores = {emotion: 0.0 for emotion in EMOTIONS}
    for emotion, keywords in keyword_map.items():
        for keyword in keywords:
            if keyword in lowered:
                scores[emotion] = 0.95
                break

    if not any(value > 0 for value in scores.values()):
        scores = {emotion: 0.1 for emotion in EMOTIONS}

    dominant = _dominant_emotion(scores)
    return {
        "anger": scores.get("anger"),
        "disgust": scores.get("disgust"),
        "fear": scores.get("fear"),
        "joy": scores.get("joy"),
        "sadness": scores.get("sadness"),
        "dominant_emotion": dominant,
    }


def _call_watson_api(text_to_analyze: str) -> Any:
    """Attempt to use IBM Watson Natural Language Understanding if credentials exist."""
    api_key = os.getenv("WATSON_API_KEY") or os.getenv("IBM_API_KEY")
    service_url = os.getenv("WATSON_URL") or os.getenv("IBM_URL")

    if not api_key or not service_url or IAMAuthenticator is None or NaturalLanguageUnderstandingV1 is None:
        return None

    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version="2022-04-07",
        authenticator=authenticator,
    )
    natural_language_understanding.set_service_url(service_url)

    try:
        return natural_language_understanding.analyze(
            text=text_to_analyze,
            features=Features(emotion=EmotionOptions()),
        )
    except Exception:  # pragma: no cover - depends on external service state
        return None


def emotion_detector(text_to_analyze: str) -> dict[str, Any]:
    """Analyze text sentiment and return the five emotion scores and dominant emotion."""
    if text_to_analyze is None or not str(text_to_analyze).strip():
        return _empty_result()

    text_to_analyze = str(text_to_analyze).strip()
    watson_response = _call_watson_api(text_to_analyze)

    if watson_response is not None:
        parsed = _parse_watson_response(watson_response)
        if parsed is not None:
            if parsed.get("dominant_emotion") is None and any(
                value is not None for value in parsed.values() if value is not None
            ):
                return _keyword_fallback(text_to_analyze)
            return parsed

    return _keyword_fallback(text_to_analyze)
