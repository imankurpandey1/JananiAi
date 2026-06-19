from __future__ import annotations

import re
from collections import Counter
from datetime import datetime, timezone


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def words(text: str) -> list[str]:
    return re.findall(r"\b[\w']+\b", text.lower())


def word_count(text: str) -> int:
    return len(words(text))


def reading_time_minutes(text: str) -> float:
    return round(max(word_count(text) / 220, 0.1), 2)


def lexical_diversity(text: str) -> float:
    tokens = words(text)
    return round(len(set(tokens)) / len(tokens), 3) if tokens else 0.0


def repetition_rate(text: str) -> float:
    tokens = words(text)
    if not tokens:
        return 0.0
    counts = Counter(tokens)
    repeated = sum(count - 1 for count in counts.values() if count > 1)
    return round(repeated / len(tokens), 3)


def overlap_score(source: str, target: str) -> float:
    source_terms = set(words(source))
    target_terms = set(words(target))
    if not source_terms:
        return 0.0
    return round(min(len(source_terms & target_terms) / max(len(source_terms), 1), 1.0), 3)


def estimate_story_scores(prompt: str, story: str, generation_time: float, memory_mb: float) -> dict:
    diversity = lexical_diversity(story)
    repetition = repetition_rate(story)
    retention = overlap_score(prompt, story)
    length = word_count(story)
    return {
        "coherence": round(min(0.45 + retention + (0.15 if length > 80 else 0), 1.0), 3),
        "creativity": round(min(0.25 + diversity, 1.0), 3),
        "story_length": length,
        "context_retention": retention,
        "response_speed": round(generation_time, 3),
        "memory_usage": round(memory_mb, 2),
        "lexical_diversity": diversity,
        "repetition_rate": repetition,
    }


def generate_title(prompt: str, story: str) -> str:
    text = clean_text(story or prompt)
    first_sentence = re.split(r"[.!?]", text)[0]
    title_words = [w.capitalize() for w in words(first_sentence)[:7]]
    if not title_words:
        title_words = ["Untitled", "Story"]
    return " ".join(title_words)


def generate_summary(story: str) -> str:
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", clean_text(story)) if s.strip()]
    if not sentences:
        return "No summary available."
    return " ".join(sentences[:2])
