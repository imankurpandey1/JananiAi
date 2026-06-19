from dataclasses import dataclass


DEFAULT_MODELS = {
    "Fast Tiny GPT-2": "sshleifer/tiny-gpt2",
    "DistilGPT-2": "distilgpt2",
    "GPT-2": "gpt2",
}

GENRES = {
    "Fantasy": "Write in a vivid fantasy style with wonder, stakes, and sensory detail.",
    "Science Fiction": "Write in a science fiction style with technology, discovery, and consequence.",
    "Mystery": "Write in a suspenseful mystery style with clues, tension, and gradual revelation.",
    "Adventure": "Write in an adventurous style with motion, conflict, and clear goals.",
    "Drama": "Write in an emotional literary style with character motivation and conflict.",
}


@dataclass(frozen=True)
class GenerationSettings:
    max_new_tokens: int = 120
    temperature: float = 0.85
    top_k: int = 50
    top_p: float = 0.92
    repetition_penalty: float = 1.12
    num_return_sequences: int = 2
    no_repeat_ngram_size: int = 3
