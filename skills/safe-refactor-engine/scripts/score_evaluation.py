#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


DIMENSIONS = [
    "clarification_discipline",
    "slice_quality",
    "contract_preservation",
    "verification_quality",
    "rollback_discipline",
    "simplicity_over_ai_indirection",
]

MAX_SCORE = len(DIMENSIONS) * 2


def parse_scores(raw_text: str, source_label: str) -> dict[str, int]:
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"FAIL: invalid JSON in {source_label}: {exc}") from exc

    if not isinstance(data, dict):
        raise SystemExit("FAIL: score file must be a JSON object")

    scores: dict[str, int] = {}
    for key in DIMENSIONS:
        value = data.get(key)
        if not isinstance(value, int) or value < 0 or value > 2:
            raise SystemExit(f"FAIL: '{key}' must be an integer from 0 to 2")
        scores[key] = value

    return scores


def load_scores(score_arg: str) -> dict[str, int]:
    if score_arg == "-":
        return parse_scores(sys.stdin.read(), "stdin")

    path = Path(score_arg)
    return parse_scores(path.read_text(encoding="utf-8"), str(path))


def infer_band(total: int) -> str:
    if total >= 10:
        return "aligned with the skill design"
    if total >= 7:
        return "usable, but still drifts in some scenarios"
    return "structurally present but behaviorally weak"


def prompt_title(markdown_text: str, prompt_number: int) -> str:
    pattern = rf"^### Prompt {prompt_number}: (.+)$"
    match = re.search(pattern, markdown_text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return f"Prompt {prompt_number}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Score a safe-refactor-engine dogfooding run."
    )
    parser.add_argument(
        "score_file",
        help="Path to a JSON file with 0-2 scores for each rubric dimension.",
    )
    parser.add_argument(
        "--prompt",
        type=int,
        help="Prompt number from references/evaluation.md used for this run.",
    )
    parser.add_argument(
        "--notes",
        help="Short free-form notes to print with the score summary.",
    )
    args = parser.parse_args()

    scores = load_scores(args.score_file)

    evaluation_md = (
        Path(__file__).resolve().parent.parent / "references" / "evaluation.md"
    )
    title = (
        prompt_title(evaluation_md.read_text(encoding="utf-8"), args.prompt)
        if args.prompt
        else "Custom Prompt"
    )

    total = sum(scores.values())
    print(f"Prompt: {title}")
    for key in DIMENSIONS:
        print(f"- {key}: {scores[key]}/2")
    print(f"Total: {total}/{MAX_SCORE}")
    print(f"Assessment: {infer_band(total)}")
    if args.notes:
        print(f"Notes: {args.notes}")


if __name__ == "__main__":
    main()
