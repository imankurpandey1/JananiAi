from __future__ import annotations

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]


def _get_default_db_path() -> Path:
    if os.environ.get("STORYCRAFT_DB_PATH"):
        return Path(os.environ["STORYCRAFT_DB_PATH"])
    data_dir = Path("/data")
    if data_dir.exists() and data_dir.is_dir():
        try:
            test_file = data_dir / ".write_test"
            test_file.touch()
            test_file.unlink()
            return data_dir / "storycraft.db"
        except Exception:
            pass
    return BASE_DIR / "backend" / "database" / "storycraft.db"


class Settings:
    SECRET_KEY = os.environ.get("STORYCRAFT_SECRET_KEY", "storycraft-dev-secret-key-32bytes-long-super-secure!!")
    HOST = os.environ.get("STORYCRAFT_HOST", "127.0.0.1")
    PORT = int(os.environ.get("STORYCRAFT_PORT", "5000"))
    DEBUG = os.environ.get("STORYCRAFT_DEBUG", "1") == "1"
    DB_PATH = _get_default_db_path()
    MODEL_CACHE_DIR = Path(os.environ.get("STORYCRAFT_MODEL_CACHE_DIR", BASE_DIR / "backend" / "models"))
    MAX_PROMPT_CHARS = int(os.environ.get("STORYCRAFT_MAX_PROMPT_CHARS", "5000"))
    FRONTEND_ORIGIN = os.environ.get("STORYCRAFT_FRONTEND_ORIGIN", "*")
    CORS_ORIGINS = "*"
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "618003048467-libua714ra4mdbe0tk2qqb915gorovoh.apps.googleusercontent.com")

    GENRES = [
        "Fantasy",
        "Mystery",
        "Horror",
        "Sci-Fi",
        "Adventure",
        "Romance",
        "Mythology",
        "Children's Stories",
    ]

    MODEL_REGISTRY = {
        "gpt2": {
            "label": "GPT-2",
            "hf_id": "gpt2",
            "description": "GPT-2 baseline for richer long-form generation.",
        },
        "distilgpt2": {
            "label": "DistilGPT-2",
            "hf_id": "distilgpt2",
            "description": "Compact distilled GPT-2 model optimized for faster inference.",
        },
        "qwen2.5-0.5b-instruct": {
            "label": "Qwen2.5 0.5B Instruct",
            "hf_id": "Qwen/Qwen2.5-0.5B-Instruct",
            "description": "Instruction-tuned model with stronger prompt adherence and story planning.",
            "chat_template": True,
        },
    }
