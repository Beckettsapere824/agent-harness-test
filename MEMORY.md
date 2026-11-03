# MEMORY.md — Persistent Project Memory

Newest entries at the **top** of each section.

---

## Status

### Current focus

- T004: implement MS02 todo CLI under adversarial session ledger rules.

### Done

- T007: hardened structural (negative evidence/status checks) + continuity suite + MS02 pack definition.
- T001–T003, T006.

### Next

- Run hardened suites; record new scores (expect structural may still be high; continuity is the real gate).
- Implement MS02 S1 only in a dedicated step (ledger phase 1).

---

## Pitfalls / decisions

- Easy structural scores are not enough; continuity suite + ledger gates address inflation.
- Fabricating a full ledger in one push must be scored down on T004.

---

## Scores

| When | Suite | Score | Notes |
|------|-------|------:|-------|
| 2026-11-03 | structural v1 | 88.24 → 100 | too easy |
| 2026-11-03 | ms01 | 70 | one-shot penalty |
| 2026-11-03 | structural v2 + continuity | *measure after T007* | |

---

## Log

### 2026-11-03

- T007 landed: negative structural checks, continuity audit, MS02 adversarial SPEC.
