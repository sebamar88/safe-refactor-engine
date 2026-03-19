# Refactor Patterns

Use this file when multiple safe transformations are possible and you need to choose the smallest one.

## Default Preference Order

Prefer these transformations from least disruptive to most disruptive:

1. rename for intent
2. extract function
3. extract module
4. isolate side effects
5. split overloaded unit
6. introduce adapter or facade
7. delete dead code after proving no live references

## Pattern Selection

### Extract function

Use when:

- one function mixes levels of abstraction
- a branch or loop has a clear name
- logic can move without changing surrounding ownership

Avoid when:

- the extracted function would need a long parameter list with no clarity gain

### Extract module

Use when:

- one file contains multiple responsibilities
- helpers are reused by more than one unit
- a cohesive concept exists but is buried inside a larger file

Avoid when:

- the split would only scatter tightly coupled logic across files

### Isolate side effects

Use when:

- business logic and I/O are entangled
- testing is difficult because state changes and decisions are mixed

Avoid when:

- the new boundary would be purely ceremonial and not reduce coupling

### Split overloaded unit

Use when:

- one class, service, or module owns unrelated reasons to change
- reads and writes follow different policies

Avoid when:

- the split is based on hypothetical future growth instead of present complexity

### Introduce adapter or facade

Use when:

- callers depend on unstable or noisy dependencies
- you need a seam before a larger move

Avoid when:

- it adds an extra layer with no testability or boundary benefit

## AI Debt Checks

Reject the refactor direction if it creates:

- vague abstractions with generic names like `Manager`, `Processor`, or `Helper` without a precise responsibility
- thin wrapper chains that only forward calls
- excessive indirection that hides data flow
- larger diffs than the structural gain justifies
