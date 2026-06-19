import re
from dataclasses import dataclass


MAX_PROMPT_CHARS = 4000
MIN_PROMPT_WORDS = 3


@dataclass
class ValidationResult:
    ok: bool
    cleaned_prompt: str = ""
    message: str = ""


def normalize_prompt(prompt: str) -> str:
    prompt = re.sub(r"\s+", " ", str(prompt or "")).strip()
    return prompt


def validate_prompt(prompt: str, max_chars: int = MAX_PROMPT_CHARS) -> ValidationResult:
    cleaned = normalize_prompt(prompt)
    if not cleaned:
        return ValidationResult(False, message="Prompt cannot be empty.")
    if len(cleaned) > max_chars:
        return ValidationResult(False, message=f"Prompt is too long. Keep it under {max_chars} characters.")
    if len(cleaned.split()) < MIN_PROMPT_WORDS:
        return ValidationResult(False, message="Prompt is too short. Add a character, setting, or conflict.")
    if re.search(r"(.)\1{20,}", cleaned):
        return ValidationResult(False, message="Prompt contains excessive repeated characters.")
    return ValidationResult(True, cleaned_prompt=cleaned)


def has_repetitive_loop(text: str, min_phrase_words: int = 3, threshold: int = 4) -> bool:
    words = re.findall(r"\b\w+\b", text.lower())
    if len(words) < min_phrase_words * threshold:
        return False
    phrases = [" ".join(words[i : i + min_phrase_words]) for i in range(len(words) - min_phrase_words + 1)]
    counts = {}
    for phrase in phrases:
        counts[phrase] = counts.get(phrase, 0) + 1
        if counts[phrase] >= threshold:
            return True
    return False


def trim_repetitive_tail(text: str) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    if len(sentences) < 4:
        return text.strip()

    cleaned = []
    seen = set()
    for sentence in sentences:
        key = re.sub(r"\W+", " ", sentence.lower()).strip()
        if key and key in seen:
            break
        seen.add(key)
        cleaned.append(sentence)
    return " ".join(cleaned).strip()
