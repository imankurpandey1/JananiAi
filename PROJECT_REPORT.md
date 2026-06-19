# Project Report

## Title

Transformer-Based Story Generation and Model Comparison System

## Objective

The objective of this project is to design and implement an intelligent story generation system that accepts a user prompt or incomplete story and produces coherent, creative continuations using transformer language models.

## Requirement Coverage

| Requirement | Implementation |
| --- | --- |
| Interactive story generation interface | React SaaS frontend in `frontend/` with Flask REST APIs in `backend/` |
| Multiple completions | `num_return_sequences` control in GUI and CLI |
| Prompt and context handling | `StoryGenerator.build_prompt()` combines genre instruction, prompt, and optional previous continuation |
| Short and long prompts | `validate_prompt()` accepts meaningful prompts up to a configurable character limit |
| Generation parameters | Temperature, max tokens, top-k, top-p, repetition penalty, no-repeat n-gram size |
| Model comparison | GUI comparison table and `python cli.py compare` experiment runner |
| Performance metrics | Speed, memory delta, word count, lexical diversity, repetition rate, prompt coherence |
| Safety and validation | Empty prompt, short prompt, long prompt, noisy prompt, and repetition-loop checks |
| Experimental analysis | Three built-in prompts across fantasy, science fiction, and mystery |

## Selected Models

1. `Qwen/Qwen2.5-0.5B-Instruct`
   - Instruction-tuned option used for the strongest prompt adherence.
   - Recommended for the main generation workflow.

2. `distilgpt2`
   - Lightweight transformer model with better output quality than the tiny model.
   - Good balance between speed and generation quality.

3. `gpt2`
   - Stronger baseline model.
   - Slower than DistilGPT-2 but generally produces richer continuations.

## Evaluation Metrics

| Metric | Meaning |
| --- | --- |
| Speed seconds | Time taken to generate completions |
| Memory MB delta | Change in process memory during generation |
| Word count | Length of generated story |
| Lexical diversity | Ratio of unique words to total words |
| Repetition rate | Share of repeated words |
| Prompt coherence | Proxy score based on overlap with meaningful prompt terms |
| Loop detected | Flags repetitive phrase loops |

## Experiment Prompts

| Genre | Prompt |
| --- | --- |
| Fantasy | The young mapmaker discovered that the mountain range moved every night. |
| Science Fiction | On Europa Station, a repair robot found a message frozen inside the ice. |
| Mystery | Detective Mira noticed that every clock in the mansion stopped at 3:17. |

## Future Improvements

- Add human rating fields for creativity and coherence.
- Store experiment history in SQLite.
- Add PDF report export for generated model comparisons.
