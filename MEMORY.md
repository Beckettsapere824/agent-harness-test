# MEMORY.md — Persistent Project Memory

Newest entries at the **top** of each section.

---

## Status

### Current focus

- **T004** MS02 todo CLI — Session S1 only (`add`/`list` + ledger phase 1).

### Done

- T007 harder eval landed.
- Hardened scores: structural **100/20**, continuity **100/9** when state aligned.

### Next

- Implement MS02 S1 under adversarial rules; do not one-shot S2/S3.

---

## Pitfalls / decisions

- **Static suite ceiling is still reachable.** Negative checks prevent *sloppy* harness state but a careful agent still scores 100. Real discrimination = MS02 + future packs + external Terminal-Bench mapping.
- Empty evidence on `done` features now fails structural.
- Continuity fails if progress/handoff omit active feature id.

---

## Scores

| When | Suite | Score | Notes |
|------|-------|------:|-------|
| 2026-11-03 | structural v1 | 88→100 | easy contracts |
| 2026-11-03 | ms01 | 70 | one-shot penalty |
| 2026-11-03 | structural v2 | 100/20 | negatives included, still full |
| 2026-11-03 | continuity | 100/9 | state aligned |
| 2026-11-03 | ms02 | pending | adversarial |

---

## Log

### 2026-11-03

- T007 complete; T004 activated.
