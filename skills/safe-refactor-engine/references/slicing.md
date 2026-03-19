# Slicing Guide

Use this file when the refactor is bigger than one obvious edit and you need a safe sequence.

## Goal

Break a refactor into slices that are:

- behavior-preserving
- independently verifiable
- small enough to debug without widening scope

## Preferred Slice Order

Use this order unless local constraints force a different one:

1. identify the seam
2. add the seam without changing behavior
3. move one responsibility behind the seam
4. update callers incrementally
5. remove obsolete code after verification

## Good Slice Shapes

- extract a pure helper from an overloaded function
- move I/O behind an adapter while preserving call shape
- split read logic from write logic
- separate parsing or validation from orchestration
- introduce a narrow facade before moving internals

## Bad Slice Shapes

- rename, reformat, and restructure in the same slice
- move multiple responsibilities at once
- change contracts while also moving files unless the user asked for both
- delete old code before callers are proven to use the new path

## Heuristics

- if you cannot describe the invariant of the slice in one sentence, it is too large
- if the verification for the slice requires the whole test suite, the slice may be too broad
- if rollback would be messy, split the slice further
- prefer seams around side effects, state mutation, and public entrypoints

## Example Slice Plans

### Local extraction

1. extract a pure helper from the long function
2. replace inline logic with helper calls
3. remove duplicated branches once tests still pass

### Module split

1. create the new module with identical signatures
2. move one cohesive responsibility
3. repoint imports or callers
4. remove dead exports

### Architecture-sensitive move

1. add facade or adapter
2. route callers through the new boundary
3. move internals behind the boundary
4. verify contract stability
5. delete obsolete coupling
