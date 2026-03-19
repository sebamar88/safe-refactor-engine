# Verification Guide

Use this file to choose the smallest trustworthy check after each slice.

## Verification Priority

Run the cheapest useful signal first:

1. syntax or compile check
2. type-check for typed stacks
3. targeted test for the changed contract
4. focused manual probe when automation is absent
5. broader suite only when risk justifies it

## Match Checks to Change Type

### Rename or move with stable behavior

- compile or type-check
- run targeted tests for imports or public entrypoints if available

### Pure logic extraction

- targeted unit tests
- type-check if the language supports it

### Side-effect isolation

- tests around persistence, network calls, file writes, or emitted events
- manual probe if the project lacks coverage

### Public contract touch

- run the narrowest test that exercises the public boundary
- inspect response shapes, return values, and side effects explicitly

## When the Repo Has No Useful Tests

Use a focused manual probe and record it explicitly:

- command or action executed
- input or trigger used
- expected observable result
- observed result

Good examples:

- invoke one CLI command with a representative argument
- call one HTTP endpoint with a stable fixture
- run one UI flow that reaches the changed branch
- execute one worker or job path with known sample data

Do not use vague statements like "looks fine" or "should still work" as verification.

## Failure Rules

- stop on the first contradictory signal
- make at most 1 to 2 focused repair attempts
- if still failing, revert that slice to the last verified state
- do not continue stacking changes on top of a red state

## Reporting

After each slice, summarize:

- what changed
- what contract was preserved
- what verification ran
- whether the slice is green, repaired, or rolled back

## Contract Checklist

When checking contract drift, inspect the relevant subset of:

- public APIs and entrypoints
- data shapes and serialization format
- error behavior and exception paths
- side effects such as writes, emits, logs, and network calls
- persistence semantics
- imports, exports, and callable names
