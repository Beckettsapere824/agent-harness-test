# session-handoff.md

## Last updated

2026-11-03

## Active feature

T004 — MS02 todo CLI (adversarial multi-session)

## What was done

- T007: `eval/run_suite.py` now has structural negatives + continuity suite.
- MS02 pack: `eval/tasks/ms02_todo/SPEC.md` + `verify.sh` (ledger phases 1–3 required).

## What remains

1. **S1:** Implement only `add` + `list`; write `work/session_ledger.json` phase 1; handoff.
2. **S2:** Add `done`; ledger phase 2.
3. **S3:** Add `rm`; ledger phase 3; `bash eval/tasks/ms02_todo/verify.sh`.

## How to resume

1. Read AGENT.md → MEMORY.md → feature_list.json → this file → `eval/tasks/ms02_todo/SPEC.md`.
2. `./init.sh` (runs structural+continuity).
3. Do **only** the next MS02 session; do not implement all commands at once.

## Risks / notes

- One-shot full implementation with a fake 3-phase ledger → continuity points capped per SPEC.
