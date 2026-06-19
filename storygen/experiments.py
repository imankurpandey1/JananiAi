from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .config import DEFAULT_MODELS, GenerationSettings
from .generator import StoryGenerator


EXPERIMENT_PROMPTS = {
    "Fantasy": "The young mapmaker discovered that the mountain range moved every night.",
    "Science Fiction": "On Europa Station, a repair robot found a message frozen inside the ice.",
    "Mystery": "Detective Mira noticed that every clock in the mansion stopped at 3:17.",
}


def run_experiments(
    output_dir: str | Path = "outputs",
    model_names: list[str] | None = None,
    settings: GenerationSettings | None = None,
) -> tuple[Path, Path]:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    settings = settings or GenerationSettings(max_new_tokens=90, num_return_sequences=1)
    selected = model_names or ["Fast Tiny GPT-2", "DistilGPT-2"]
    generator = StoryGenerator()
    rows = []
    raw = []

    for genre, prompt in EXPERIMENT_PROMPTS.items():
        for name in selected:
            model_id = DEFAULT_MODELS[name]
            result = generator.generate(prompt, model_id=model_id, genre=genre, settings=settings)
            raw.append({"genre": genre, "prompt": prompt, "model_name": name, "result": result})
            if result["ok"]:
                story = result["stories"][0]
                rows.append(
                    {
                        "genre": genre,
                        "model": name,
                        "model_id": model_id,
                        "speed_seconds": result["elapsed_seconds"],
                        "memory_mb_delta": result["memory_mb_delta"],
                        "word_count": story["metrics"]["word_count"],
                        "lexical_diversity": story["metrics"]["lexical_diversity"],
                        "repetition_rate": story["metrics"]["repetition_rate"],
                        "prompt_coherence": story["metrics"]["prompt_coherence"],
                        "loop_detected": story["loop_detected"],
                    }
                )

    csv_file = output_path / "model_comparison.csv"
    json_file = output_path / "experiment_outputs.json"
    pd.DataFrame(rows).to_csv(csv_file, index=False)
    json_file.write_text(json.dumps(raw, indent=2), encoding="utf-8")
    return csv_file, json_file
