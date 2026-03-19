# Verification Guide

## Principle
Run the smallest check that can falsify the slice you just applied.

## Verification Ladder

### Level 1: Static
- parse, compile, or type-check if the stack supports it
- run targeted static analysis or linting if available
- build or package the affected unit if applicable

### Level 2: Behavioral
- focused unit tests
- focused integration tests
- approval, golden, or snapshot checks if already present

### Level 3: Manual Probe
- exercise the changed entrypoint
- run the command, operation, or workflow whose behavior was moved
- inspect the observable result where automated checks are absent

## Contract Checks

Always look for drift in:

- public entrypoints
- callable interfaces
- input and output shapes
- message or payload names
- side-effect timing
- persistence writes

## When Tests Are Weak

If coverage is missing:

1. prefer seam-creation refactors first
2. keep slices smaller
3. add a minimal regression test if it is cheaper than reasoning blindly
4. state the verification gap explicitly
