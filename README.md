# Safe Refactor Engine

Language-agnostic refactoring skill for agentic coding workflows.

This repository packages a reusable skill that helps an agent plan and execute refactors without guessing user intent, without overfitting to a single stack, and without casually breaking behavior. The structure is intentionally marketplace-friendly: a self-contained installable skill, minimal UI metadata, optional deep references, and lightweight validation scripts.

## Overview

`safe-refactor-engine` is designed for work such as:

- splitting large units
- extracting modules or helpers
- isolating side effects
- reducing coupling
- cleaning up structure without changing intended behavior
- planning larger architectural refactors in verifiable slices

The skill is opinionated about process:

- clarify user intent before acting when ambiguity is real
- resolve technical uncertainty with tools and docs before asking the user
- preserve behavior unless the user explicitly asks for behavior change
- use `KISS`, `DRY`, `YAGNI`, `SRP`, and separation of concerns as active refactor constraints

## Why This Repo Is Structured This Way

This repo borrows packaging ideas from public skill collections: the installable artifact lives under `skills/<skill-name>/`, support material is optional, and the root docs explain what the skill is, how to install it, and how to validate it.

The goal is to keep the skill:

- easy to publish
- easy to copy into a local skills directory
- easy for humans to review
- easy for agents to index

## Repository Layout

```text
safe-refactor-engine/
├── CONTRIBUTING.md
├── README.md
├── llms.txt
├── references/
│   ├── agents/
│   ├── patterns.md
│   ├── slicing.md
│   ├── verification.md
│   └── workflow.md
└── skills/
    └── safe-refactor-engine/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        ├── references/
        │   ├── evaluation.md
        │   ├── patterns.md
        │   ├── refactor-catalog.md
        │   ├── real-world-validation.md
        │   ├── slicing.md
        │   └── verification.md
        └── scripts/
            ├── dogfood_runner.py
            ├── quick_validate.py
            └── score_evaluation.py
```

## Install

Copy the `skills/safe-refactor-engine/` folder into the local or global skills directory used by your coding agent, preserving the internal layout.

At minimum, keep these files together:

- `SKILL.md`
- `agents/openai.yaml`
- `references/`
- `scripts/`

If your environment supports repository-based skill catalogs, this repository is already laid out so the installable asset is isolated from root-level documentation.

## Use

Example invocation:

```text
Use $safe-refactor-engine to plan and apply a safe refactor for the code in scope.
```

Example requests:

- `Use $safe-refactor-engine to split this service into smaller modules without changing behavior.`
- `Use $safe-refactor-engine to reduce coupling in this subsystem and preserve public contracts.`
- `Use $safe-refactor-engine to refactor this file safely; ask me only if the desired outcome is unclear.`
- `Use $safe-refactor-engine in dry-run mode and propose the slices before editing.`

## What The Skill Enforces

- The principal agent clarifies intent only when the request is materially ambiguous.
- Technical uncertainty about libraries, APIs, commands, or framework behavior is resolved with local tooling, official docs, or MCPs before asking the user.
- Quick and Standard mode should work from the main `SKILL.md` alone; references are support material, not required startup context.
- The agent estimates blast radius before editing. If the likely impact exceeds 5 files, it upgrades to a deeper workflow.
- Each slice includes a rollback point and immediate verification.
- In typed or compiled stacks, the agent runs the narrowest available lint, build, or type-check after each slice.
- Reports target terminal or chat, not Slack or dashboards.

## Validation And Dogfooding

Quick structural validation:

```bash
python3 skills/safe-refactor-engine/scripts/quick_validate.py
```

Score a dogfooding run against the evaluation rubric:

```bash
python3 skills/safe-refactor-engine/scripts/score_evaluation.py scores.json --prompt 1
```

Create a dogfooding run with scorecard files:

```bash
python3 skills/safe-refactor-engine/scripts/dogfood_runner.py --prompts 2,9,18,19,23,24 --label smoke-suite
```

Run an interactive scoring session and write `summary.json` automatically:

```bash
python3 skills/safe-refactor-engine/scripts/dogfood_runner.py --prompts 2,9,18,19,23,24 --label smoke-suite --interactive
```

## Main Files

Installable skill:

- [`skills/safe-refactor-engine/SKILL.md`](./skills/safe-refactor-engine/SKILL.md)

UI metadata:

- [`skills/safe-refactor-engine/agents/openai.yaml`](./skills/safe-refactor-engine/agents/openai.yaml)

Bundled references used by the skill:

- [`skills/safe-refactor-engine/references/slicing.md`](./skills/safe-refactor-engine/references/slicing.md)
- [`skills/safe-refactor-engine/references/patterns.md`](./skills/safe-refactor-engine/references/patterns.md)
- [`skills/safe-refactor-engine/references/refactor-catalog.md`](./skills/safe-refactor-engine/references/refactor-catalog.md)
- [`skills/safe-refactor-engine/references/verification.md`](./skills/safe-refactor-engine/references/verification.md)
- [`skills/safe-refactor-engine/references/evaluation.md`](./skills/safe-refactor-engine/references/evaluation.md)
- [`skills/safe-refactor-engine/references/real-world-validation.md`](./skills/safe-refactor-engine/references/real-world-validation.md)

Root-level design references for repository maintenance:

- [`references/workflow.md`](./references/workflow.md)
- [`references/slicing.md`](./references/slicing.md)
- [`references/verification.md`](./references/verification.md)
- [`references/patterns.md`](./references/patterns.md)

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for packaging, writing, and validation expectations.

## Status

The skill is structurally valid, documented for publication, and organized so it can be indexed by both humans and agents.
