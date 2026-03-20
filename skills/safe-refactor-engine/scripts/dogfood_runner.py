#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from score_evaluation import DIMENSIONS, MAX_SCORE, infer_band


ROOT = Path(__file__).resolve().parent.parent
EVALUATION_MD = ROOT / "references" / "evaluation.md"
RUNS_DIR = ROOT / "dogfood-runs"


@dataclass(frozen=True)
class PromptCase:
    number: int
    title: str
    prompt: str


def parse_prompt_cases(markdown_text: str) -> list[PromptCase]:
    pattern = re.compile(
        r"^### Prompt (\d+): (.+?)\n\nPrompt:\n\n```text\n(.*?)\n```",
        re.MULTILINE | re.DOTALL,
    )
    cases: list[PromptCase] = []
    for match in pattern.finditer(markdown_text):
        cases.append(
            PromptCase(
                number=int(match.group(1)),
                title=match.group(2).strip(),
                prompt=match.group(3).strip(),
            )
        )
    return cases


def parse_prompt_selection(raw: str, available_numbers: set[int]) -> list[int]:
    selected: list[int] = []
    for chunk in raw.split(","):
        item = chunk.strip()
        if not item:
            continue
        if "-" in item:
            start_raw, end_raw = item.split("-", 1)
            start = int(start_raw)
            end = int(end_raw)
            if start > end:
                raise SystemExit(f"FAIL: invalid prompt range '{item}'")
            selected.extend(range(start, end + 1))
        else:
            selected.append(int(item))

    deduped: list[int] = []
    seen: set[int] = set()
    for number in selected:
        if number not in available_numbers:
            raise SystemExit(f"FAIL: prompt {number} not found in evaluation.md")
        if number not in seen:
            deduped.append(number)
            seen.add(number)
    return deduped


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return normalized or "run"


def timestamp_slug() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def ensure_run_dir(path_arg: str | None, label: str | None) -> Path:
    if path_arg:
        run_dir = Path(path_arg)
    else:
        slug = slugify(label) if label else "dogfood"
        run_dir = RUNS_DIR / f"{timestamp_slug()}-{slug}"
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def scorecard_path(run_dir: Path, prompt_number: int) -> Path:
    return run_dir / "scorecards" / f"prompt-{prompt_number:02d}.json"


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def make_scorecard_template(case: PromptCase) -> dict[str, object]:
    return {
        "prompt_number": case.number,
        "prompt_title": case.title,
        "prompt_text": case.prompt,
        "scores": {key: None for key in DIMENSIONS},
        "notes": "",
        "completed": False,
    }


def prompt_for_score(prompt_label: str, dimension: str) -> int:
    while True:
        raw = input(f"{prompt_label} | {dimension} (0-2): ").strip()
        if raw in {"0", "1", "2"}:
            return int(raw)
        print("Enter 0, 1, or 2.")


def prompt_for_notes(prompt_label: str) -> str:
    return input(f"{prompt_label} | notes (optional): ").strip()


def collect_interactive_scorecard(case: PromptCase) -> dict[str, object]:
    prompt_label = f"Prompt {case.number}: {case.title}"
    print()
    print(prompt_label)
    print(case.prompt)
    scores = {key: prompt_for_score(prompt_label, key) for key in DIMENSIONS}
    notes = prompt_for_notes(prompt_label)
    return {
        "prompt_number": case.number,
        "prompt_title": case.title,
        "prompt_text": case.prompt,
        "scores": scores,
        "notes": notes,
        "completed": True,
    }


def load_scorecard(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def completed_scorecards(run_dir: Path) -> list[dict[str, object]]:
    cards_dir = run_dir / "scorecards"
    if not cards_dir.is_dir():
        return []
    cards: list[dict[str, object]] = []
    for path in sorted(cards_dir.glob("prompt-*.json")):
        card = load_scorecard(path)
        if card.get("completed") is True:
            cards.append(card)
    return cards


def summarize(cards: Iterable[dict[str, object]]) -> dict[str, object]:
    card_list = list(cards)
    completed = len(card_list)
    if completed == 0:
        return {
            "completed_prompts": 0,
            "average_total": 0.0,
            "average_percent": 0.0,
            "assessment": "no completed scorecards yet",
            "dimension_averages": {key: 0.0 for key in DIMENSIONS},
        }

    totals: list[int] = []
    dimension_totals = {key: 0 for key in DIMENSIONS}
    prompt_summaries: list[dict[str, object]] = []

    for card in card_list:
        scores = card["scores"]
        assert isinstance(scores, dict)
        total = sum(int(scores[key]) for key in DIMENSIONS)
        totals.append(total)
        for key in DIMENSIONS:
            dimension_totals[key] += int(scores[key])
        prompt_summaries.append(
            {
                "prompt_number": card["prompt_number"],
                "prompt_title": card["prompt_title"],
                "total": total,
                "max_score": MAX_SCORE,
                "assessment": infer_band(total),
                "notes": card.get("notes", ""),
            }
        )

    average_total = sum(totals) / completed
    average_percent = (average_total / MAX_SCORE) * 100
    rounded_total = round(average_total)
    return {
        "completed_prompts": completed,
        "average_total": round(average_total, 2),
        "average_percent": round(average_percent, 2),
        "assessment": infer_band(rounded_total),
        "dimension_averages": {
            key: round(dimension_totals[key] / completed, 2) for key in DIMENSIONS
        },
        "prompts": prompt_summaries,
    }


def print_summary(summary: dict[str, object], run_dir: Path) -> None:
    print(f"Run directory: {run_dir}")
    print(f"Completed prompts: {summary['completed_prompts']}")
    print(f"Average total: {summary['average_total']}/{MAX_SCORE}")
    print(f"Average percent: {summary['average_percent']}%")
    print(f"Assessment: {summary['assessment']}")
    print("Dimension averages:")
    averages = summary["dimension_averages"]
    assert isinstance(averages, dict)
    for key in DIMENSIONS:
        print(f"- {key}: {averages[key]}/2")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create and summarize scorecards for safe-refactor-engine dogfooding runs."
    )
    parser.add_argument(
        "--prompts",
        default="1-6",
        help="Comma-separated prompt numbers or ranges, for example '2,9,18' or '1-6'.",
    )
    parser.add_argument(
        "--label",
        help="Optional label to include in the generated run directory name.",
    )
    parser.add_argument(
        "--run-dir",
        help="Optional explicit output directory for the run.",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Prompt for rubric scores and notes, then write completed scorecards.",
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Skip prompt generation and summarize an existing run directory.",
    )
    args = parser.parse_args()

    if args.summary_only and not args.run_dir:
        raise SystemExit("FAIL: --summary-only requires --run-dir")

    markdown_text = EVALUATION_MD.read_text(encoding="utf-8")
    cases = parse_prompt_cases(markdown_text)
    if not cases:
        raise SystemExit("FAIL: no prompts found in evaluation.md")

    run_dir = ensure_run_dir(args.run_dir, args.label)

    if not args.summary_only:
        selected_numbers = parse_prompt_selection(
            args.prompts, {case.number for case in cases}
        )
        selected_cases = [case for case in cases if case.number in selected_numbers]

        manifest = {
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "label": args.label or "",
            "selected_prompts": [
                {
                    "prompt_number": case.number,
                    "prompt_title": case.title,
                }
                for case in selected_cases
            ],
            "interactive": args.interactive,
        }
        write_json(run_dir / "manifest.json", manifest)

        for case in selected_cases:
            path = scorecard_path(run_dir, case.number)
            payload = (
                collect_interactive_scorecard(case)
                if args.interactive
                else make_scorecard_template(case)
            )
            write_json(path, payload)

    summary = summarize(completed_scorecards(run_dir))
    write_json(run_dir / "summary.json", summary)
    print_summary(summary, run_dir)


if __name__ == "__main__":
    main()
