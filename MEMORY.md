# MEMORY.md — Persistent Project Memory

Newest entries at the **top** of each section.

---

## Status

### Current focus

- T003: Multi-session pack MS01 (counter) — implement under harness discipline.

### Done

- Harness bootstrapped in agent-harness-test.
- Structural suite live; first baseline **88.24** (scorer had duplicate checks; fixed toward 100).
- TASKS.md + docs/benchmarks.md + MS01 SPEC/verify committed.

### Next

- Implement MS01 across simulated sessions (S1→S2→S3) using only repo state between sessions.
- Record MS01 score; then iterate harness on failures (T005).

---

## Pitfalls / decisions

- External Terminal-Bench / SWE-bench need containers → secondary yardsticks; primary loop is structural + `eval/tasks/ms*`.
- Structural scorer must not double-`add` the same check (fixed).
- Keep task code under `work/` pure Python for sandbox determinism.

---

## Scores

| When | Suite | Score | Notes |
|------|-------|-------|-------|
| 2026-11-03 | structural | 88.24 | baseline pre-fix |

---

## Log

### 2026-11-03

- Bootstrap + baseline + MS01 pack added.
- Benchmark refs: TraceTrial-Bench, Harness-Bench, Doc2Harness, Terminal-Bench, SWE-bench, learn-harness five subsystems.
