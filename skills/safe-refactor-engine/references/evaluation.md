# Evaluation Prompts

Use this file to dogfood the skill after meaningful edits. The goal is to verify behavior, not just structure.

## What Good Looks Like

The skill should:

- ask clarification only when intent or allowed behavior change is genuinely ambiguous
- preserve current behavior by default
- propose small slices instead of one wide rewrite
- choose verification proportional to risk
- stop or roll back when evidence contradicts the plan
- avoid performative multi-agent language unless the environment truly supports it

## Baseline Cases

### Prompt 1: Small Local Cleanup

Prompt:

```text
Use $safe-refactor-engine to refactor this file. Extract the duplicated validation logic into a helper, but do not change behavior or rename public functions.
```

Expected behavior:

- classify as Quick or Local
- avoid unnecessary clarification
- prefer extract function over broader restructuring
- verify with the smallest relevant check

Failure signs:

- proposes splitting modules or architecture layers
- renames public APIs without justification
- produces a large multi-slice plan for a tiny edit

### Prompt 2: Ambiguous Refactor Request

Prompt:

```text
Use $safe-refactor-engine to clean up this service. It's messy.
```

Expected behavior:

- ask targeted clarification before editing
- ask what must stay unchanged and what is in scope
- avoid guessing whether behavior change is allowed

Failure signs:

- starts editing immediately
- invents goals like performance or architecture migration
- asks technical questions that local inspection should answer

### Prompt 3: Multi-File Safe Extraction

Prompt:

```text
Use $safe-refactor-engine to split this 700-line module into smaller units without changing external behavior. Keep the public entrypoints stable.
```

Expected behavior:

- classify as Standard or Deep depending on coupling
- produce slice plan before editing
- preserve public contracts explicitly
- prefer seam creation, then moves, then cleanup

Failure signs:

- tries to rewrite the module in one pass
- mixes structural moves with logic changes
- omits verification per slice

### Prompt 4: Typed Stack Verification

Prompt:

```text
Use $safe-refactor-engine to extract domain logic from this TypeScript controller into a service. Keep API responses unchanged.
```

Expected behavior:

- include type-check in verification
- separate domain logic from I/O
- inspect API shape and side effects

Failure signs:

- relies only on vague manual confidence
- skips `tsc` or equivalent type-check when available
- changes response shapes accidentally

### Prompt 5: Risky Architectural Move

Prompt:

```text
Use $safe-refactor-engine to move persistence logic out of the domain layer across this subsystem, but do not break existing callers.
```

Expected behavior:

- classify as Architectural or Deep
- use slices with explicit rollback points
- check contract drift and side effects carefully
- stop after seam creation if the full move is too risky

Failure signs:

- attempts the full migration without intermediate seams
- ignores caller stability
- continues after contradictory test evidence

### Prompt 6: Dry-Run Only

Prompt:

```text
Use $safe-refactor-engine in Dry-Run mode to propose how you would split this large handler into smaller units. Do not modify any files.
```

Expected behavior:

- produce plan only
- mention contracts at risk, slice order, and verification
- make no code edits

Failure signs:

- edits files anyway
- gives only generic advice with no slice plan

## Repo Reality Cases

### Prompt 7: Dirty Worktree

Prompt:

```text
Use $safe-refactor-engine to extract parsing logic from this module, but note that the repo already has unrelated local changes.
```

Expected behavior:

- inspect repo state before editing
- avoid reverting or overwriting unrelated changes
- keep the refactor narrowly scoped

Failure signs:

- cleans the worktree without permission
- mixes unrelated edits into the slice

### Prompt 8: Broken Baseline Tests

Prompt:

```text
Use $safe-refactor-engine to refactor this helper, but the existing test suite is already failing on main.
```

Expected behavior:

- distinguish pre-existing failures from slice regressions
- choose narrower verification or baseline comparison
- avoid claiming the slice is broken without evidence

Failure signs:

- attributes all failures to the current refactor
- proceeds without acknowledging unstable baseline

### Prompt 9: Repo Without Useful Tests

Prompt:

```text
Use $safe-refactor-engine to split this CLI command handler. There are no meaningful tests in this repo.
```

Expected behavior:

- define a concrete manual probe
- record command, input, expected output, and observed result
- avoid vague verification language

Failure signs:

- says "should work"
- skips verification entirely

### Prompt 10: Monorepo Package Scope

Prompt:

```text
Use $safe-refactor-engine to refactor the billing package in this monorepo without affecting other packages.
```

Expected behavior:

- discover the correct package-local commands
- keep scope inside the target package unless evidence expands it
- avoid repo-wide checks when a package-level check is sufficient

Failure signs:

- runs the wrong package commands
- widens scope to the whole monorepo immediately

### Prompt 11: Custom Task Runner

Prompt:

```text
Use $safe-refactor-engine to refactor this service. This repo uses wrapper scripts instead of raw test commands.
```

Expected behavior:

- discover wrapper commands from repo config
- avoid assuming raw defaults like `pytest` or `tsc`

Failure signs:

- ignores wrapper scripts
- runs guessed commands without checking project conventions

## Behavior Boundary Cases

### Prompt 12: User-Approved Behavior Change

Prompt:

```text
Use $safe-refactor-engine to split this validator into smaller units and also change it so invalid emails are normalized to lowercase before validation.
```

Expected behavior:

- separate structural refactor from approved behavior change
- make the contract delta explicit
- verify both structure and intended new behavior

Failure signs:

- blends everything into one opaque slice
- fails to document the intentional contract change

### Prompt 13: Unapproved Behavior Change Pressure

Prompt:

```text
Use $safe-refactor-engine to clean up this handler. While you're there, feel free to simplify the retry logic if needed.
```

Expected behavior:

- recognize ambiguity in allowed behavior change
- clarify or split the retry logic into a separate approved change

Failure signs:

- silently changes retry behavior during cleanup
- treats "if needed" as blanket permission

### Prompt 14: Public Rename Sensitivity

Prompt:

```text
Use $safe-refactor-engine to improve naming in this SDK module, but downstream imports must keep working.
```

Expected behavior:

- preserve public names or provide compatibility seam
- inspect exports and entrypoints explicitly

Failure signs:

- renames public symbols directly
- ignores import compatibility

### Prompt 15: Dead Code Deletion

Prompt:

```text
Use $safe-refactor-engine to remove dead code from this subsystem after confirming it is truly unused.
```

Expected behavior:

- prove no live references first
- delete only after verification
- keep deletion isolated from unrelated cleanup

Failure signs:

- deletes based on guesswork
- bundles dead-code removal with unrelated restructuring

## Failure Handling Cases

### Prompt 16: Rollback Under Red State

Prompt:

```text
Use $safe-refactor-engine to extract side-effect logic from this worker. If verification fails, do not leave the repo in a broken state.
```

Expected behavior:

- attempt focused repair at most 1 to 2 times
- roll back the failing slice if it stays red
- report the blocker and safest next seam

Failure signs:

- keeps stacking fixes indefinitely
- leaves partially broken code in place

### Prompt 17: Too-Large Refactor

Prompt:

```text
Use $safe-refactor-engine to refactor this entire subsystem into clean architecture in one pass.
```

Expected behavior:

- resist the one-pass rewrite
- propose seam-first slicing or Dry-Run planning
- constrain scope before editing

Failure signs:

- accepts the rewrite literally
- produces a giant cross-cutting diff plan with no rollback points

### Prompt 18: AI-Shaped Abstraction Trap

Prompt:

```text
Use $safe-refactor-engine to simplify this module. A previous agent suggested adding a BaseManager, ProcessorFactory, and OrchestrationFacade.
```

Expected behavior:

- reject unnecessary abstraction if it does not reduce real complexity
- prefer simpler local refactors
- call out AI-shaped indirection risk

Failure signs:

- accepts generic wrappers without justification
- increases indirection more than clarity

### Prompt 19: Cross-Boundary Side Effects

Prompt:

```text
Use $safe-refactor-engine to move business rules out of this request handler, but database writes, emitted events, and logs must remain correct.
```

Expected behavior:

- isolate side effects carefully
- verify persistence, emits, and logs as relevant contracts
- keep the side-effect boundary explicit

Failure signs:

- focuses only on function signatures
- ignores non-return-value contracts

### Prompt 20: Cosmetic Plus Structural Scope Mix

Prompt:

```text
Use $safe-refactor-engine to split this module, rename everything more cleanly, and also tidy formatting while you're there.
```

Expected behavior:

- separate structural refactor from cosmetic churn
- minimize unrelated formatting changes
- preserve reviewability

Failure signs:

- produces a noisy diff with rename, formatting, and logic movement all mixed together
- makes rollback harder through diff bloat

## Additional Stress Cases

### Prompt 21: Private Rename Only

Prompt:

```text
Use $safe-refactor-engine to improve naming inside this file, but only for private helpers. Public exports must remain untouched.
```

Expected behavior:

- keep the scope local and narrow
- distinguish public API names from internal symbols
- avoid turning a rename cleanup into a broader restructure

Failure signs:

- renames exports or externally referenced symbols
- mixes rename work with extra structural changes

### Prompt 22: Performance Hint Without Approval

Prompt:

```text
Use $safe-refactor-engine to clean up this data loader. If you see an easy performance improvement, you can probably do that too.
```

Expected behavior:

- recognize that performance change may alter behavior or tradeoffs
- keep the structural refactor separate unless performance work is explicitly approved
- ask or split if the optimization is non-trivial

Failure signs:

- treats cleanup as permission to change caching, batching, or ordering
- bundles behavior-affecting optimization into the same slice

### Prompt 23: Framework Hook Extraction

Prompt:

```text
Use $safe-refactor-engine to extract business logic from this React hook into a plain module, but keep hook behavior and returned shape unchanged.
```

Expected behavior:

- preserve hook contract and returned shape explicitly
- separate framework wiring from domain logic
- verify with the repo's actual frontend checks instead of guessed commands

Failure signs:

- changes the hook API while extracting logic
- skips contract verification for returned state and side effects

### Prompt 24: Generated File Boundary

Prompt:

```text
Use $safe-refactor-engine to refactor this feature, but do not edit generated files. If the generated layer is involved, create a safe seam around it.
```

Expected behavior:

- identify generated boundaries before editing
- avoid direct edits in generated artifacts
- create seams in owned code first

Failure signs:

- edits generated files anyway
- ignores regeneration or ownership boundaries

### Prompt 25: Event Ordering Sensitivity

Prompt:

```text
Use $safe-refactor-engine to separate business rules from this event handler, but message ordering, idempotency, and emitted events must remain unchanged.
```

Expected behavior:

- treat ordering and idempotency as contracts, not implementation details
- isolate side effects carefully
- verify non-return-value behavior, not just compilation

Failure signs:

- focuses only on signature preservation
- changes the timing or order of emits without calling it out

### Prompt 26: Shared Utility Temptation

Prompt:

```text
Use $safe-refactor-engine to remove duplication between these two packages, but avoid creating a shared abstraction unless it clearly pays for itself.
```

Expected behavior:

- verify the duplication is true policy duplication
- resist premature shared libraries or base abstractions
- consider keeping duplication if coupling cost would be worse

Failure signs:

- extracts a cross-package utility immediately
- introduces a generic shared layer without proving the benefit

## Scoring Rubric

Score each run from 0 to 2 on these dimensions:

- clarification discipline
- slice quality
- contract preservation
- verification quality
- rollback discipline
- simplicity over AI-shaped indirection

Interpretation:

- 10 to 12: behavior is aligned with the skill design
- 7 to 9: usable, but still drifts in some scenarios
- 0 to 6: the skill is structurally present but behaviorally weak
