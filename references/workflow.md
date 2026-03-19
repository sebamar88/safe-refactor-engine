# Refactor Workflow

## Goal
Keep refactors behavior-preserving, incremental, and easy to validate.

## Guiding Principles

- apply KISS to prefer the least-complex structure that solves the current problem
- apply DRY only to proven duplication, not superficial similarity
- apply YAGNI to avoid future-proofing layers that have no present need
- apply SRP so each extracted unit has one clear reason to change
- apply separation of concerns to keep policy, orchestration, and side effects distinct

## Sequence

1. Ask clarifying questions only if the refactor target is not already unambiguous.
2. Resolve technical uncertainty with local inspection, native tooling, official docs, or MCPs before involving the user.
3. Fingerprint the local area.
4. Identify the overloaded responsibility.
5. Name the target structure.
6. Create a seam before moving behavior.
7. Move one responsibility at a time.
8. Verify after each move.
9. Remove dead paths only after callers are migrated.

## Good Slice Properties

- touches few files
- preserves one clear invariant
- has one obvious rollback point
- can be verified with one command or probe

## Bad Slice Properties

- mixes rename, logic rewrite, and architecture move
- changes public contracts and internal structure together
- forces full-repo revalidation for a local change
- depends on future slices to compile or make sense
- introduces abstractions that exist only for hypothetical future reuse

## Preferred Slice Order

1. extraction without behavior change
2. caller migration
3. dependency cleanup
4. dead code removal

## Stop Conditions

Stop and re-plan if:

- the user intent or allowed behavior change is still unclear
- technical behavior remains unclear after reasonable tool-based grounding
- the next slice requires behavior changes the user did not request
- you find hidden side effects or undocumented contracts
- verification no longer covers the changed surface
- the diff grows beyond what you can reason about locally
