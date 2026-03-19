# Slicing Guide

## Choose Scope

### Local
Use when the problem is a large routine, overloaded unit, duplicated helper, or misplaced side effect.

Typical moves:
- extract function
- extract helper
- extract helper module
- rename misleading symbols

### Slice
Use when several files share one responsibility that needs clearer ownership.

Typical moves:
- move domain logic out of delivery or boundary code
- isolate transport or persistence adapters
- split shared contracts from implementation
- introduce a facade to reduce coupling

### Architectural
Use when dependency direction or subsystem boundaries are wrong.

Typical moves:
- invert dependency direction
- split package responsibilities
- add ports and adapters
- move orchestration out of leaf modules

## What To Freeze

During a refactor, freeze as much as possible:

- public entrypoints
- input and output shapes
- persisted data layout
- observable runtime behavior
- log and error semantics when relied on operationally

Change these only when the user explicitly asks for a behavior change.

## What To Separate First

Prefer separating:

- pure computation from side effects
- orchestration from implementation details
- boundary handling from state transitions
- domain rules from transport or framework code
- reusable utilities from feature-specific policy

## Principle Checks During Slicing

- **KISS**: each slice should make the result easier to explain
- **DRY**: merge duplication only when semantics truly match
- **YAGNI**: avoid creating extension seams with no immediate consumer
- **SRP**: avoid slices that move multiple unrelated reasons to change together
