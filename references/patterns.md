# Refactor Patterns

## Large Function to Focused Pipeline

Use when one routine validates, transforms, persists, and reports.
Why: improves SRP and separation of concerns without inventing a new abstraction model.

Pattern:
1. extract pure helpers
2. keep orchestration in the original entrypoint
3. move side effects behind named calls

## Overloaded Unit to Coordinator Plus Parts

Use when one unit owns input handling, state transitions, formatting, and output generation.
Why: keeps the public contract stable while simplifying local reasoning under KISS.

Pattern:
1. extract pure transformation pieces
2. extract derived-state helpers
3. extract controller or coordinator for side effects
4. keep the public contract stable

## Mixed Domain and I/O to Service Boundary

Use when boundary code and business rules live together.
Why: clarifies ownership and prevents side effects from leaking into policy decisions.

Pattern:
1. isolate framework or transport code
2. move business rules into plain functions or services
3. inject dependencies rather than reaching globally

## Duplicate Logic to Shared Module

Use when the same transformation appears in several files.
Why: applies DRY only after confirming the duplication is semantic, not accidental.

Pattern:
1. confirm the logic is truly the same
2. extract a shared function with intention-revealing name
3. migrate one caller at a time
4. delete inline duplicates only after all callers move

## Rename With Guardrails

Use when names are the main source of confusion.
Why: improves clarity with minimal risk and usually satisfies KISS better than bigger rewrites.

Pattern:
1. rename without changing behavior
2. keep public compatibility if needed
3. update references mechanically
4. verify external contracts before removing aliases
