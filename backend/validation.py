from __future__ import annotations

from backend.config.settings import Settings
from backend.utils import clean_text


def validate_prompt(value: str, field: str = "prompt") -> tuple[str | None, str | None]:
    text = clean_text(value)
    if not text:
        return None, f"{field} cannot be empty."
    if len(text.split()) < 4:
        return None, f"{field} is too short. Add a character, setting, and conflict."
    if len(text) > Settings.MAX_PROMPT_CHARS:
        return None, f"{field} is too long. Keep it under {Settings.MAX_PROMPT_CHARS} characters."
    return text, None


def validate_generation_params(payload: dict) -> tuple[dict | None, str | None]:
    model = str(payload.get("model", "distilgpt2")).lower().strip()
    genre = str(payload.get("genre", "Fantasy")).strip()
    if model not in Settings.MODEL_REGISTRY:
        return None, "Invalid model. Choose one of the available models."
    if genre not in Settings.GENRES:
        return None, "Invalid genre."

    try:
        temperature = float(payload.get("temperature", 0.85))
        top_k = int(payload.get("top_k", 50))
        top_p = float(payload.get("top_p", 0.92))
        max_tokens = int(payload.get("max_tokens", 180))
    except (TypeError, ValueError):
        return None, "Generation parameters must be numeric."

    if not 0.1 <= temperature <= 1.8:
        return None, "Temperature must be between 0.1 and 1.8."
    if not 1 <= top_k <= 100:
        return None, "Top-K must be between 1 and 100."
    if not 0.1 <= top_p <= 1.0:
        return None, "Top-P must be between 0.1 and 1.0."
    if not 30 <= max_tokens <= 500:
        return None, "Max tokens must be between 30 and 500."

    return {
        "model": model,
        "genre": genre,
        "temperature": temperature,
        "top_k": top_k,
        "top_p": top_p,
        "max_tokens": max_tokens,
    }, None


def validate_rating(value: int) -> tuple[int | None, str | None]:
    try:
        rating = int(value)
    except (TypeError, ValueError):
        return None, "Rating must be a number."
    if rating < 1 or rating > 5:
        return None, "Rating must be between 1 and 5."
    return rating, None


def validate_story_id(value: object) -> tuple[int | None, str | None]:
    try:
        story_id = int(value)
    except (TypeError, ValueError):
        return None, "Story id must be a positive integer."
    if story_id < 1:
        return None, "Story id must be a positive integer."
    return story_id, None
