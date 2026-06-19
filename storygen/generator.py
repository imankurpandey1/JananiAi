from __future__ import annotations

import time
from dataclasses import asdict

import psutil
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from .config import GENRES, GenerationSettings
from .metrics import score_story
from .safety import has_repetitive_loop, trim_repetitive_tail, validate_prompt


class StoryGenerator:
    def __init__(self) -> None:
        self._pipelines = {}

    def load_pipeline(self, model_id: str):
        if model_id in self._pipelines:
            return self._pipelines[model_id]

        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        device = 0 if torch.cuda.is_available() else -1
        text_generator = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=device,
        )
        self._pipelines[model_id] = text_generator
        return text_generator

    @staticmethod
    def build_prompt(prompt: str, genre: str = "Fantasy", previous_story: str = "") -> str:
        genre_instruction = GENRES.get(genre, GENRES["Fantasy"])
        context = f"\nPrevious continuation:\n{previous_story.strip()}\n" if previous_story.strip() else ""
        return (
            f"{genre_instruction}\n"
            f"Continue the story with coherent plot, character motivation, and a satisfying next scene."
            f"{context}\nStory beginning:\n{prompt.strip()}\nContinuation:"
        )

    def generate(
        self,
        prompt: str,
        model_id: str,
        genre: str = "Fantasy",
        settings: GenerationSettings | None = None,
        previous_story: str = "",
    ) -> dict:
        settings = settings or GenerationSettings()
        validation = validate_prompt(prompt)
        if not validation.ok:
            return {"ok": False, "error": validation.message}

        full_prompt = self.build_prompt(validation.cleaned_prompt, genre, previous_story)
        text_generator = self.load_pipeline(model_id)
        process = psutil.Process()
        memory_before = process.memory_info().rss / (1024 * 1024)
        start = time.perf_counter()

        outputs = text_generator(
            full_prompt,
            max_new_tokens=settings.max_new_tokens,
            temperature=settings.temperature,
            top_k=settings.top_k,
            top_p=settings.top_p,
            repetition_penalty=settings.repetition_penalty,
            num_return_sequences=settings.num_return_sequences,
            no_repeat_ngram_size=settings.no_repeat_ngram_size,
            do_sample=True,
            pad_token_id=text_generator.tokenizer.eos_token_id,
        )

        elapsed = time.perf_counter() - start
        memory_after = process.memory_info().rss / (1024 * 1024)
        stories = []
        for item in outputs:
            generated = item["generated_text"].replace(full_prompt, "", 1).strip()
            generated = trim_repetitive_tail(generated)
            stories.append(
                {
                    "text": generated,
                    "loop_detected": has_repetitive_loop(generated),
                    "metrics": score_story(validation.cleaned_prompt, generated),
                }
            )

        return {
            "ok": True,
            "model_id": model_id,
            "genre": genre,
            "settings": asdict(settings),
            "elapsed_seconds": round(elapsed, 3),
            "memory_mb_delta": round(memory_after - memory_before, 2),
            "device": "cuda" if torch.cuda.is_available() else "cpu",
            "stories": stories,
        }
