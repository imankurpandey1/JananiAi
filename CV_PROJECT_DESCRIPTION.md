# StoryCraft

Full-stack NLP story-generation application built with React, Flask, SQLite, and Hugging Face Transformers. It supports prompt-based generation, unfinished-story continuation, model comparison, saved-story management, ratings, analytics, and PDF/TXT export.

## Resume entry

**StoryCraft | React, Flask, SQLite, Hugging Face Transformers, PyTorch**

- Built a full-stack story-generation application with configurable sampling controls, prompt validation, and support for both new-story generation and continuation workflows.
- Integrated an instruction-tuned language model for stronger prompt adherence alongside GPT-2 and DistilGPT-2 baselines for quality and performance comparison.
- Implemented a Flask REST API with validated inputs, controlled cross-origin access, safe error handling, and SQLite-backed story persistence.
- Developed an interactive React dashboard for model comparison, ratings, searchable story history, generation analytics, and PDF/TXT export.
- Added automated tests covering validation, text-quality safeguards, API input handling, CORS behavior, and generation-scoring logic.

## Interview summary

The project focuses on the complete lifecycle of a lightweight NLP product: input validation, transformer inference, output-quality safeguards, persistent storage, analytics, and a responsive user interface. Quality-oriented generation uses an instruction-tuned model, while the GPT-2 variants remain available as reproducible baselines for comparison.
