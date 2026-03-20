# Refactor Catalog

Use this file when you already know a refactor is warranted and need help choosing a small, behavior-preserving move. Treat it as a decision aid, not a mandate to introduce patterns.

Prefer the smallest move that reduces confusion without widening the blast radius.

## Smell To Move Map

### Long function or mixed abstraction levels

Use when:

- one function fetches data, applies policy, mutates state, and formats output
- one branch or loop can be named clearly
- setup, decision, and side effects are interleaved

Prefer:

1. extract function
2. isolate side effects
3. extract module if helpers become cohesive

Avoid:

- extracting tiny helpers that force a long parameter list and make control flow harder to follow
- moving logic across files before proving the seam locally

### Duplicated logic

Use when:

- multiple call sites implement the same policy
- bug fixes would need to be repeated in more than one place

Prefer:

1. confirm the duplicated paths really share the same rule
2. extract shared function or module
3. update one caller at a time if the blast radius is non-trivial

Avoid:

- merging code that only looks similar but actually has different policy or error handling

### Large module or overloaded unit

Use when:

- one file has several unrelated reasons to change
- orchestration, domain rules, and I/O live together
- the unit exposes more than one natural public entrypoint

Prefer:

1. identify one responsibility to move
2. create a seam
3. move that responsibility behind the seam
4. update callers
5. remove obsolete code

Avoid:

- broad rewrites that split everything at once
- introducing generic containers like `Manager`, `Processor`, or `Utils`

### Long parameter list or data clumps

Use when:

- the same group of values travels together through multiple calls
- call sites are hard to read because argument order matters too much

Prefer:

1. introduce a parameter object or existing domain type
2. migrate one call path at a time
3. collapse obsolete parameters after callers are updated

Avoid:

- wrapping unrelated values into a bag object with no domain meaning

### Primitive obsession

Use when:

- raw strings, numbers, or maps encode domain concepts
- validation rules are duplicated around the codebase

Prefer:

1. introduce a small domain type or constrained helper
2. move validation to creation boundaries
3. preserve external contract shape unless the user asked otherwise

Avoid:

- creating elaborate class hierarchies for simple constraints

### Nested conditionals

Use when:

- success flow is buried under guard logic
- error handling and happy path are interleaved

Prefer:

1. guard clauses
2. extracted validation helpers
3. polymorphism only if branch ownership is already stable and repeated

Avoid:

- introducing pattern-heavy dispatch where a few guard clauses would do

### Feature envy or inappropriate intimacy

Use when:

- one unit reaches deep into another unit's internals
- callers know too much about data layout

Prefer:

1. move the behavior closer to the data owner
2. introduce an intention-revealing method at the boundary
3. reduce deep property traversal in callers

Avoid:

- moving behavior if it would create circular ownership or hide important orchestration

### Magic numbers or strings

Use when:

- literals encode policy, timing, or status
- the same literal appears in more than one place

Prefer:

1. named constant
2. grouped constants for related policy
3. domain type only if the concept carries behavior too

Avoid:

- over-modeling a single local literal that is unlikely to recur

### Dead code

Use when:

- functions, exports, imports, flags, or branches have no live references
- commented code is preserved "just in case"

Prefer:

1. prove no live references
2. delete in an isolated slice
3. run the smallest contract check that would fail if the code were still needed

Avoid:

- deleting code whose usage cannot yet be traced confidently

### Generated or tool-owned boundaries

Use when:

- the feature depends on generated clients, schemas, build outputs, or codegen layers
- the requested refactor touches files that should not be hand-edited

Prefer:

1. identify the owned source that feeds generation
2. create or move a seam in owned code
3. keep generated artifacts untouched unless regeneration is the expected project workflow

Avoid:

- hand-editing generated files to "finish the refactor"
- burying ownership boundaries inside a broad module split

## Pattern Escalation Rules

Reach for heavier patterns only when lighter moves fail to create a safe seam.

### Strategy

Use when:

- one stable operation varies by policy
- conditional branches are likely to grow and already have distinct behavior

Do not use when:

- two or three local branches are already readable and unlikely to spread

### Adapter or facade

Use when:

- callers depend directly on a noisy dependency
- a future move needs a boundary first

Do not use when:

- the wrapper only forwards calls without reducing coupling

### Chain of responsibility

Use when:

- validation or transformation steps are already sequential and independently optional

Do not use when:

- a straightforward list of checks is clearer

## Refactor Sanity Checks

Before committing to a move, ask:

- does this reduce the number of things a reader must hold in their head?
- does this preserve the current public contract?
- can I verify this move immediately with a narrow check?
- would rollback be local and obvious?
- am I adding a real seam, or just another layer?
