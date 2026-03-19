#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL_MD = ROOT / "SKILL.md"
OPENAI_YAML = ROOT / "agents" / "openai.yaml"
SCRIPTS_DIR = ROOT / "scripts"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def ok(message: str) -> None:
    print(f"OK: {message}")


def validate_frontmatter(skill_text: str) -> None:
    match = re.match(r"^---\n(.*?)\n---\n", skill_text, re.DOTALL)
    if not match:
        fail("SKILL.md is missing YAML frontmatter")

    frontmatter = match.group(1)
    if not re.search(r"(?m)^name:\s+\S", frontmatter):
        fail("SKILL.md frontmatter is missing a name field")
    if not re.search(r"(?m)^description:\s+.+", frontmatter):
        fail("SKILL.md frontmatter is missing a description field")
    ok("SKILL.md frontmatter has name and description")


def validate_openai_yaml(yaml_text: str) -> None:
    required_patterns = [
        r"(?m)^interface:\s*$",
        r'(?m)^\s{2}display_name:\s+".+"\s*$',
        r'(?m)^\s{2}short_description:\s+".+"\s*$',
        r'(?m)^\s{2}default_prompt:\s+".+"\s*$',
    ]
    for pattern in required_patterns:
        if not re.search(pattern, yaml_text):
            fail(f"agents/openai.yaml is missing required content matching: {pattern}")
    ok("agents/openai.yaml contains required interface fields")


def validate_references(skill_text: str) -> None:
    refs = sorted(set(re.findall(r"`(references/[^`]+\.md)`", skill_text)))
    if not refs:
        ok("No inline reference files declared in SKILL.md")
        return

    for ref in refs:
        path = ROOT / ref
        if not path.is_file():
            fail(f"Referenced file does not exist: {ref}")
    ok(f"All referenced files exist ({len(refs)})")


def validate_structure() -> None:
    if not SKILL_MD.is_file():
        fail("Missing SKILL.md")
    ok("Found SKILL.md")

    if not OPENAI_YAML.is_file():
        fail("Missing agents/openai.yaml")
    ok("Found agents/openai.yaml")


def validate_scripts() -> None:
    expected = [
        SCRIPTS_DIR / "quick_validate.py",
        SCRIPTS_DIR / "score_evaluation.py",
    ]
    for path in expected:
        if not path.is_file():
            fail(f"Missing script: {path.relative_to(ROOT)}")
    ok(f"Expected scripts exist ({len(expected)})")


def main() -> None:
    validate_structure()
    validate_scripts()

    skill_text = SKILL_MD.read_text(encoding="utf-8")
    yaml_text = OPENAI_YAML.read_text(encoding="utf-8")

    validate_frontmatter(skill_text)
    validate_openai_yaml(yaml_text)
    validate_references(skill_text)

    print("PASS: safe-refactor-engine skill structure is valid")


if __name__ == "__main__":
    main()
