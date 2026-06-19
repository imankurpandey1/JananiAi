import argparse
import json
from pathlib import Path

from rich.console import Console
from rich.table import Table

from storygen.config import DEFAULT_MODELS, GenerationSettings
from storygen.experiments import run_experiments
from storygen.generator import StoryGenerator


console = Console()


def generate_command(args: argparse.Namespace) -> None:
    settings = GenerationSettings(
        max_new_tokens=args.max_new_tokens,
        temperature=args.temperature,
        top_k=args.top_k,
        top_p=args.top_p,
        repetition_penalty=args.repetition_penalty,
        num_return_sequences=args.num_return_sequences,
    )
    model_id = DEFAULT_MODELS.get(args.model, args.model)
    result = StoryGenerator().generate(args.prompt, model_id=model_id, genre=args.genre, settings=settings)
    console.print_json(json.dumps(result, indent=2))


def compare_command(args: argparse.Namespace) -> None:
    csv_file, json_file = run_experiments(output_dir=args.output_dir)
    table = Table(title="Experiment Complete")
    table.add_column("Artifact")
    table.add_column("Path")
    table.add_row("Comparison CSV", str(csv_file))
    table.add_row("Raw outputs JSON", str(json_file))
    console.print(table)


def main() -> None:
    parser = argparse.ArgumentParser(description="Transformer story generation project")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="Generate story continuations")
    generate.add_argument("--prompt", required=True)
    generate.add_argument("--model", default="Fast Tiny GPT-2")
    generate.add_argument("--genre", default="Fantasy")
    generate.add_argument("--max-new-tokens", type=int, default=120)
    generate.add_argument("--temperature", type=float, default=0.85)
    generate.add_argument("--top-k", type=int, default=50)
    generate.add_argument("--top-p", type=float, default=0.92)
    generate.add_argument("--repetition-penalty", type=float, default=1.12)
    generate.add_argument("--num-return-sequences", type=int, default=2)
    generate.set_defaults(func=generate_command)

    compare = subparsers.add_parser("compare", help="Run model comparison experiments")
    compare.add_argument("--output-dir", default=str(Path("outputs")))
    compare.set_defaults(func=compare_command)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
