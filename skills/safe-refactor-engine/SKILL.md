---
name: safe-refactor-engine
description: Plan and execute safe code refactors in a language-agnostic way using mandatory clarification, behavior-preserving slices, rollback discipline, contract checks, and per-slice verification. Use when the user asks to refactor, split large units, extract modules, rename or move responsibilities, reduce complexity, or improve structure without changing intended behavior.
---

# Safe Refactor Engine

Use this skill to turn a refactor request into a controlled sequence of small, verifiable changes. Stay language-agnostic: reason from responsibilities, contracts, boundaries, and side effects instead of assuming a specific stack, framework, or type system.

Default to conservative execution. Preserve observable behavior unless the user explicitly asks for behavior change.

## Quick Cheat Sheet

Use this section directly in Quick and Standard mode before opening any optional references.

- if you cannot describe the invariant of a slice in one sentence, the slice is too large
- prefer this slice order by default: add seam, move one responsibility, update callers, remove obsolete code
- avoid mixing rename, reformat, and logic movement in the same slice
- if rollback would be messy, split the slice further
- prefer seams around side effects, state mutation, and public entrypoints
- when a smell is obvious, prefer the lightest move first: rename, extract function, isolate side effects, then extract module
- for duplication, prove the duplicated paths share the same policy before unifying them
- prefer guard clauses over pattern-heavy branching cleanup unless branch ownership is already stable
- do not edit generated files; create or move seams in owned code around them
- when tests are weak or absent, name one concrete manual probe before editing
- for hooks, handlers, and adapters, preserve returned shape, side-effect timing, and emitted signals as contracts
- reject vague abstractions like `Manager`, `Processor`, `Helper`, or thin wrappers that only forward calls
- reject indirection that hides data flow without reducing coupling
- if a local change needs whole-repo verification to feel safe, treat it as higher risk and reconsider slice size

Treat the bundled references as optional deepening material, not prerequisites for normal use.

## Core Principles

Apply these principles as decision rules during the refactor:

- **KISS**: prefer the simplest structure that preserves behavior and improves clarity
- **DRY**: remove true duplication, but only after confirming the duplicated paths share the same policy
- **YAGNI**: avoid speculative abstractions, extension points, or layers with no current caller or use case
- **SRP**: move each unit toward one clear responsibility and one level of abstraction
- **Separation of Concerns**: keep domain rules, boundary handling, orchestration, and side effects from collapsing into one place

If principles conflict, preserve behavior first, then optimize for simplicity and clarity over cleverness.

Also enforce these operating rules:

- prefer 1 to 5 small slices over one broad rewrite
- verify every slice before continuing
- use the cheapest trustworthy signal first: type-check, targeted test, then broader validation
- do not keep pushing through failing slices; stabilize or roll back
- avoid replacing complex human code with equally opaque AI-shaped abstractions

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
- **Dry-Run**: planning only; no code edits. Use when the user wants a safe refactor proposal before authorizing execution.

Confirm these invariants from the local codebase:
- what behavior must stay the same
- what public contracts must stay stable
- what files are in scope
- what tests, checks, or manual probes can detect regressions

If behavior is underspecified, preserve current observable behavior by default and state that assumption.

Also estimate blast radius before planning edits:

- search for direct callers, imports, references, exports, routes, handlers, events, or other usage sites of the target
- count the affected files, not just the number of matches
- identify generated files, generated directories, and regeneration boundaries before planning edits
- if the likely impact reaches more than 5 files, upgrade to **Deep** mode unless the user explicitly constrained the scope narrower
- if the blast radius is unclear, keep exploring before editing

### Step 3: Read Before Writing
Inspect only the code needed to answer these questions:

1. What responsibility is overloaded?
2. Where are the natural seams: pure helpers, adapters, services, handlers, workers, domain operations, translators, or boundary modules?
3. What contracts are exposed: public entrypoints, callable interfaces, message formats, data shapes, events, persistence writes, or external side effects?
4. What existing tests or checks cover those contracts?

Do not widen the scan unless local evidence shows cross-cutting impact.
If the refactor depends on uncertain library or API behavior, use the agent's own tools or relevant MCPs to ground that knowledge before planning the change.
If framework-managed units are involved, include framework-facing contracts in the scan, such as returned hook shape, handler response shape, event ordering, idempotency, and log or emit behavior.

If the skill relies on bundled references, read only the specific files needed before planning. If the references are missing, continue with local inspection and explicitly note that the refactor is proceeding without optional reference material.

Reference guide:

- read `references/slicing.md` only when the safe slice order is unclear after applying the cheat sheet
- read `references/patterns.md` only when multiple refactor moves still look equally safe
- read `references/refactor-catalog.md` when you need smell-to-move heuristics or need to choose between a simple extraction and a heavier pattern
- read `references/verification.md` only when the smallest trustworthy check is not obvious
- read `references/evaluation.md` when validating whether the skill behaves correctly on realistic prompts
- read `references/real-world-validation.md` when validating the skill against an actual refactor task

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

### Step 5: Plan the Refactor as Slices
Express the refactor as 1 to 5 behavior-preserving slices. Each slice must have:

- a narrow goal
- the files it touches
- the invariant it preserves
- the verification to run immediately after the slice
- a rollback action that returns only that slice to the last verified state

Prefer sequences like:

1. add seam
2. move logic behind seam
3. update callers
4. remove obsolete code

Do not mix structural moves with logic changes unless the user explicitly asked for both.
If a behavior change appears necessary during a structural refactor, stop and either split it into a separate slice or ask the user to approve the behavior change explicitly.

Prefer rollback actions that are local and explicit:

- restore only the touched files to the last verified state with the repo's version-control tool when available
- if version control is unavailable, note the manual rollback boundary before editing
- do not propose destructive rollback commands that can wipe unrelated user work

### Step 6: Run a Pre-Write Check
Before editing, verify:

- the target location matches the project structure
- generated artifacts and owned source boundaries are identified
- the refactor reduces complexity instead of redistributing confusion
- naming matches local conventions
- new abstractions pay for themselves
- there is a concrete regression check for each changed contract
- the change respects KISS, DRY, YAGNI, SRP, and separation of concerns
- the worktree state is understood before edits start

If syntax-aware tooling exists for the current stack, prefer it. Otherwise do a guarded manual refactor and keep the diff smaller.
If stack behavior is unclear, inspect manifests, lockfiles, local configs, or official docs through the available tools instead of asking the user to explain the library unless the project has a custom rule the tools cannot reveal.
Before choosing verification commands, discover the repo's real checks from package manifests, task runners, CI config, makefiles, scripts, or local documentation instead of assuming default commands.
In monorepos or multi-package repos, prefer package-local checks for the target scope before escalating to repo-wide verification, unless the touched contract clearly crosses package boundaries.

Before the first edit, inspect version-control state when available:

- run `git status --short` or the local equivalent if available
- prefer a clean worktree before starting execution
- if the repo is dirty, default to **Dry-Run** or stop for user approval unless the request explicitly allows operating around existing local changes
- do not overwrite or revert unrelated user changes
- prefer atomic commits per completed slice when the environment and user workflow allow it
- if relevant checks are already failing before the refactor, record that baseline failure state before editing so later failures are compared against known pre-existing breakage
- if automation is weak, write down one concrete manual probe with trigger and expected observable result before the first slice

### Step 7: Validate From Multiple Perspectives
Before and after each meaningful slice, evaluate the change from these perspectives:

1. **Architecture**: does the structure become clearer and more local, or did the refactor just move complexity around?
2. **Contracts**: did any public interface, data shape, side effect, or persistence behavior drift unintentionally?
3. **Execution**: what is the smallest trustworthy command that can prove the slice still works?
4. **Maintainability**: did the new code become easier to read and change, or did it introduce AI-shaped indirection?
5. **Governance**: does the result still respect KISS, DRY, YAGNI, SRP, and separation of concerns without speculative layering?
6. **Ownership**: did the slice stay inside owned source, or did it accidentally rely on editing generated artifacts?

Treat these as validation roles, not mandatory sub-agents. Use actual delegation only if the environment supports it and it materially helps; otherwise, apply the roles directly as a single-agent checklist.

### Step 8: Execute and Verify Per Slice
After each slice:

- run the smallest meaningful test or check
- for statically typed or compiled stacks, run the compile or syntax check and the type-checker or linter after every slice whenever the repo exposes such checks
- inspect interface and contract drift
- confirm side effects still happen in the right place
- stop if the evidence contradicts the plan

Verification priority:

1. syntax or compile check
2. type-check
3. targeted test for changed contract
4. focused manual probe with recorded expected and observed result when automation is weak
5. broader suite only when the slice or repo risk justifies it

Use the repository's actual command names and scripts when available. Do not assume `tsc`, `pytest`, `cargo test`, or similar defaults if the project defines its own wrappers or task aliases.
If the baseline is already red, compare the post-slice result against the pre-refactor failure state and report only new or changed breakage as potential slice regressions.
If a typed or compiled repo exposes both lint and build or type-check commands, prefer the narrowest relevant pair after each slice.
If the touched unit is a hook, handler, worker, or event consumer, explicitly check framework-facing contracts such as returned shape, response shape, emitted events, ordering, and idempotency.

### Step 9: Handle Failure Explicitly
If a slice fails:

- make 1 focused repair attempt by default; a second attempt is allowed only if the failure mode is concrete and local
- if the slice does not stabilize, revert only that slice to the last verified functional state
- report the blocker, evidence, and safest next seam instead of leaving the code half-broken

Do not stack more changes on top of a failing slice.

### Step 10: Summarize Refactor State
Return a concise refactor summary that includes:

- scope handled
- slices completed
- slices rolled back, if any
- contracts preserved or intentionally changed
- verification run
- remaining follow-up refactors, if any

If the refactor is too risky to complete safely in one pass, stop after the safe seam-creation slice and say what remains.

### Step 11: Report the Outcome
Prefer reports that are directly readable in the terminal or chat. Do not target Slack, dashboards, or external presentation layers unless the user explicitly asks for them.

## Modes

### Quick
Use for one-file cleanup or a small extraction. Ask clarification questions only if the request leaves material uncertainty, then keep the plan implicit unless the change is risky. Use the cheat sheet directly and do not load optional references unless blocked.

### Standard
Use for multi-file refactors inside one subsystem. Clarify the target outcome only when needed, then write the slices briefly before editing. Load optional references only if the cheat sheet is insufficient.

### Deep
Use for architecture-sensitive or repo-wide refactors. Clarify goals and non-goals whenever they are not already explicit, map contracts first, then execute in stages with explicit verification after each stage.

### Dry-Run
Use when the user wants a refactor proposal without code changes. Produce the slice plan, contracts at risk, verification strategy, and rollback points, then stop before editing files.

## Output Shape

Use the lightest output that fits the task:

- **Quick**: short summary plus verification
- **Standard**: slice plan plus summary of applied changes
- **Deep**: slice plan, contract deltas, validation findings, and explicit remaining risks
- **Dry-Run**: no edits; only plan, contracts, risks, and proposed verification

Example output skeletons:

### Quick Output

```text
Scope: local helper extraction in <file>
Change: extracted duplicated validation into <helper>
Contract preserved: public function names and outputs unchanged
Verification: <smallest relevant command or probe>
```

### Standard Output

```text
Slices:
1. add seam in <file>
2. move logic to <module>
3. update callers and remove obsolete path

Contracts preserved:
- public entrypoints unchanged
- side effects still occur in the same boundary

Verification:
- <command 1>
- <command 2>
```

### Deep Output

```text
Scope: subsystem refactor across <area>
Slices completed:
1. <slice>
2. <slice>

Contract deltas:
- none intentional

Validation findings:
- architecture: <result>
- contracts: <result>
- execution: <result>
- maintainability: <result>

Remaining risks:
- <risk>
```

### Dry-Run Output

```text
Proposed slices:
1. <slice>
2. <slice>

Contracts at risk:
- <contract>

Verification plan:
- <command or probe>

Rollback points:
- after slice 1
- after slice 2
```

If you discover debt instead of a clean refactor path, hand off conceptually to audit mode and surface the blockers before changing code.
