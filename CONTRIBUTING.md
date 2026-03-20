# Contributing

## Goal

Keep this repository easy to publish, easy to review, and easy to install as a standalone skill.

## Repository Rules

- keep the installable artifact under `skills/safe-refactor-engine/`
- keep `SKILL.md` self-contained for normal use
- treat bundled references as optional deepening material, not startup dependencies
- keep root-level docs focused on packaging, publishing, and repository maintenance
- avoid adding tool-specific assumptions unless they are clearly isolated in metadata or docs

## Content Guidelines

When editing the skill:

- preserve the language-agnostic framing
- prefer operational instructions over theory
- make the default workflow work without requiring extra agents
- keep clarification rules strict about user intent, not technical uncertainty
- prefer small, explicit rules over broad aspirational prose

When adding references:

- add only material that supports a concrete decision point in the skill
- place install-time references under `skills/safe-refactor-engine/references/`
- place repository-maintenance references under `references/`
- avoid duplicating large sections between root references and bundled references unless the duplication is intentional

## Packaging Expectations

Before publishing or tagging a release, confirm:

- `skills/safe-refactor-engine/SKILL.md` has valid frontmatter
- `skills/safe-refactor-engine/agents/openai.yaml` has the required interface fields
- referenced markdown files actually exist
- root docs still describe the current repository layout
- `llms.txt` still matches the repository contents

## Validation

Run:

```bash
python3 skills/safe-refactor-engine/scripts/quick_validate.py
```

If you dogfood the skill against example prompts, record scores with:

```bash
python3 skills/safe-refactor-engine/scripts/score_evaluation.py scores.json --prompt 1
```

To create a reusable run folder with scorecards and an aggregate summary:

```bash
python3 skills/safe-refactor-engine/scripts/dogfood_runner.py --prompts 1-6 --label baseline
```

To score a run interactively and emit `summary.json` automatically:

```bash
python3 skills/safe-refactor-engine/scripts/dogfood_runner.py --prompts 1-6 --label baseline --interactive
```

## Pull Request Standard

Changes should explain:

- what changed
- whether the change affects packaging, skill behavior, or only documentation
- how the change was validated
