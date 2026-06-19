import math
import re
from collections import Counter


def tokenize(text: str) -> list[str]:
    return re.findall(r"\b[\w']+\b", text.lower())


def lexical_diversity(text: str) -> float:
    tokens = tokenize(text)
    if not tokens:
        return 0.0
    return round(len(set(tokens)) / len(tokens), 3)


def repetition_rate(text: str) -> float:
    tokens = tokenize(text)
    if not tokens:
        return 0.0
    counts = Counter(tokens)
    repeated = sum(count - 1 for count in counts.values() if count > 1)
    return round(repeated / len(tokens), 3)


def average_sentence_length(text: str) -> float:
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    if not sentences:
        return 0.0
    lengths = [len(tokenize(sentence)) for sentence in sentences]
    return round(sum(lengths) / len(lengths), 2)


def coherence_proxy(prompt: str, story: str) -> float:
    prompt_terms = set(tokenize(prompt))
    story_terms = set(tokenize(story))
    if not prompt_terms:
        return 0.0
    overlap = len(prompt_terms & story_terms) / math.sqrt(len(prompt_terms))
    return round(min(overlap, 1.0), 3)


def score_story(prompt: str, story: str) -> dict:
    return {
        "word_count": len(tokenize(story)),
        "lexical_diversity": lexical_diversity(story),
        "repetition_rate": repetition_rate(story),
        "avg_sentence_length": average_sentence_length(story),
        "prompt_coherence": coherence_proxy(prompt, story),
    }
