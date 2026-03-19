---
name: safe-refactor-engine
description: Plan and execute safe code refactors in a language-agnostic way using mandatory clarification, behavior-preserving slices, contract checks, and lightweight verification. Use when the user asks to refactor, split large units, extract modules, rename or move responsibilities, reduce complexity, or improve structure without changing intended behavior.
---

# Safe Refactor Engine

Use this skill to turn a refactor request into a controlled sequence of small, verifiable changes. Stay language-agnostic: reason from responsibilities, contracts, boundaries, and side effects instead of assuming a specific stack, framework, or type system.

## Core Principles

Apply these principles as decision rules during the refactor:

- **KISS**: prefer the simplest structure that preserves behavior and improves clarity
- **DRY**: remove true duplication, but only after confirming the duplicated paths share the same policy
- **YAGNI**: avoid speculative abstractions, extension points, or layers with no current caller or use case
- **SRP**: move each unit toward one clear responsibility and one level of abstraction
- **Separation of Concerns**: keep domain rules, boundary handling, orchestration, and side effects from collapsing into one place

If principles conflict, preserve behavior first, then optimize for simplicity and clarity over cleverness.

## Workflow

### Step 1: Mandatory Clarification Gate
The principal agent must clarify the user's intent before planning or editing whenever there is meaningful ambiguity about scope, desired outcome, constraints, or whether behavior may change. If the request is already explicit and operationally clear, do not ask redundant questions.

Separate user ambiguity from technical ambiguity:

- ask the user only about intent, scope, constraints, priorities, and acceptable behavior change
- resolve technical uncertainty about libraries, APIs, framework behavior, versions, commands, or tool usage with the agent's own tools first
- prefer local inspection, native tooling, official documentation, and MCPs before turning technical uncertainty into a user question

When clarification is needed, ask the minimum questions required to remove uncertainty. At minimum, clarify:

- what the user wants improved
- what must remain unchanged
- what files or subsystem are in scope
- whether the goal is cleanup, extraction, simplification, restructuring, or behavior change
- what risks or regressions are unacceptable

If the request is underspecified, stop and ask follow-up questions until the target refactor is unambiguous enough to execute without guessing. The agent must not work while carrying unresolved doubt about what the user wants.

### Step 2: Establish Refactor Boundaries
After clarification, classify the request before proposing edits:

- **Local**: one file or one narrow behavior.
- **Slice**: several related files in one subsystem.
- **Architectural**: cross-cutting move, layering cleanup, or ownership redistribution.

Confirm these invariants from the local codebase:
- what behavior must stay the same
- what public contracts must stay stable
- what files are in scope
- what tests, checks, or manual probes can detect regressions

If behavior is underspecified, preserve current observable behavior by default and state that assumption.

### Step 3: Read Before Writing
Inspect only the code needed to answer these questions:

1. What responsibility is overloaded?
2. Where are the natural seams: pure helpers, adapters, services, handlers, workers, domain operations, translators, or boundary modules?
3. What contracts are exposed: public entrypoints, callable interfaces, message formats, data shapes, events, persistence writes, or external side effects?
4. What existing tests or checks cover those contracts?

Do not widen the scan unless local evidence shows cross-cutting impact.
If the refactor depends on uncertain library or API behavior, use the agent's own tools or relevant MCPs to ground that knowledge before planning the change.

### Step 4: Choose the Smallest Safe Transformation
Prefer one of these moves before inventing a bigger rewrite:

- extract function
- extract module
- split overloaded unit
- isolate side effects
- introduce adapter or facade
- separate domain logic from I/O
- rename for intent
- delete dead code after confirming no live references

Avoid cosmetic churn. Do not reformat unrelated code just because the file is open.
Reject transformations that add indirection without reducing real complexity, or that centralize unrelated responsibilities in the name of reuse.

For slicing guidance, read `../../references/slicing.md`.
For common transformations, read `../../references/patterns.md`.

### Step 5: Plan the Refactor as Slices
Express the refactor as 1 to 5 behavior-preserving slices. Each slice must have:

- a narrow goal
- the files it touches
- the invariant it preserves
- the verification to run immediately after the slice

Prefer sequences like:

1. add seam
2. move logic behind seam
3. update callers
4. remove obsolete code

Do not mix structural moves with logic changes unless the user explicitly asked for both.

### Step 6: Run a Pre-Write Check
Before editing, verify:

- the target location matches the project structure
- the refactor reduces complexity instead of redistributing confusion
- naming matches local conventions
- new abstractions pay for themselves
- there is a concrete regression check for each changed contract
- the change respects KISS, DRY, YAGNI, SRP, and separation of concerns

If syntax-aware tooling exists for the current stack, prefer it. Otherwise do a guarded manual refactor and keep the diff smaller.
If stack behavior is unclear, inspect manifests, lockfiles, local configs, or official docs through the available tools instead of asking the user to explain the library unless the project has a custom rule the tools cannot reveal.

### Step 7: Activate the Smallest Agent Mesh
Use the capability-oriented mesh defined in `../../references/agents/registry.md`. Activate only the smallest set needed for the current depth:

1. **Observability Agent**: use `../../references/agents/observability.md` to extract structural telemetry, dependency edges, hotspots, and quality signals.
2. **Blueprint Architect**: use `../../references/agents/blueprint_architect.md` when requirements or target structure are still unclear and you need a concrete refactor blueprint first.
3. **Refactoring Engine**: use `../../references/agents/refactoring_engine.md` to execute paradigm-aware, syntax-aware transformations while preserving behavior.
4. **Regression Sentinel**: use `../../references/agents/regression_sentinel.md` to compare state A and state B for interface drift, contract changes, or side-effect changes.
5. **Execution Orchestrator**: use `../../references/agents/execution_orchestrator.md` to run the smallest meaningful verification command and normalize failures.
6. **Governance & Compliance**: use `../../references/agents/governance_validator.md` to enforce KISS, DRY, YAGNI, SRP, lint-like rules, and architecture policies.
7. **Synthesis Reporting**: use `../../references/agents/synthesis_reporting.md` to turn the other agents' outputs into a concise report for terminal or chat.

In Quick mode, two or three agents are usually enough. In Standard mode, use only the agents needed by the current slice. In Deep mode, build the full mesh if the refactor crosses contracts, boundaries, or architectural layers.

### Step 8: Execute and Verify Per Slice
After each slice:

- run the smallest meaningful test or check
- inspect interface and contract drift
- confirm side effects still happen in the right place
- stop if the evidence contradicts the plan

For verification guidance, read `../../references/verification.md`.

### Step 9: Summarize Refactor State
Return a concise refactor summary that includes:

- scope handled
- slices completed
- contracts preserved or intentionally changed
- verification run
- remaining follow-up refactors, if any

If the refactor is too risky to complete safely in one pass, stop after the safe seam-creation slice and say what remains.

### Step 10: Report the Outcome
Prefer reports that are directly readable in the terminal or chat. Do not target Slack, dashboards, or external presentation layers unless the user explicitly asks for them.

## Modes

### Quick
Use for one-file cleanup or a small extraction. Ask clarification questions only if the request leaves material uncertainty, then keep the plan implicit unless the change is risky.

### Standard
Use for multi-file refactors inside one subsystem. Clarify the target outcome only when needed, then write the slices briefly before editing.

### Deep
Use for architecture-sensitive or repo-wide refactors. Clarify goals and non-goals whenever they are not already explicit, map contracts first, then execute in stages with explicit verification after each stage.

## Output Shape

Use the lightest output that fits the task:

- **Quick**: short summary plus verification
- **Standard**: slice plan plus summary of applied changes
- **Deep**: slice plan, contract deltas, agent findings, and explicit remaining risks

If you discover debt instead of a clean refactor path, hand off conceptually to audit mode and surface the blockers before changing code.
