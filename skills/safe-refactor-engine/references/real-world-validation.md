# Real-World Validation

Use this file when you want to validate the skill against an actual refactor instead of synthetic prompts.

## Choose a Good Candidate

Pick a change that is:

- important enough to expose real risk
- small enough to finish in 1 to 5 slices
- already covered by at least one meaningful test, type-check, or manual probe

Good candidates:

- extract duplicated validation from one service
- split a long controller or handler without changing responses
- isolate persistence or network calls behind an adapter

Avoid for first validation:

- repo-wide renames
- framework migrations
- changes that intentionally alter behavior

## Validation Procedure

1. capture the initial repo state and relevant checks
2. run the skill on a narrowly scoped refactor
3. record the proposed slices before editing
4. record the verification command or probe used after each slice
5. score the outcome with `scripts/score_evaluation.py`

## What to Record

- prompt used
- files touched
- slices proposed
- slices actually completed
- checks run
- rollback points used, if any
- any drift between requested and actual change

## Success Criteria

Treat the run as successful if:

- behavior stayed within the user-approved scope
- contracts remained stable unless explicitly approved otherwise
- verification was concrete rather than hand-wavy
- the diff became simpler, not merely different
- the skill stopped or rolled back when evidence went red

## Example Score File

```json
{
  "clarification_discipline": 2,
  "slice_quality": 2,
  "contract_preservation": 2,
  "verification_quality": 2,
  "rollback_discipline": 2,
  "simplicity_over_ai_indirection": 2
}
```

Example command:

```bash
python3 skills/safe-refactor-engine/scripts/score_evaluation.py scores.json --prompt 3 --notes "Used on a 600-line controller split"
```
