# MEMORY.md — Persistent Project Memory

Newest entries at the **top** of each section.

---

## Status

### Current focus

- Scores are partly inflated: structural is file-contract heavy; MS01 was completed in one shot (not true multi-dialog).
- Next: T007 harden eval + T004 harder multi-session pack.

### Done

- T001–T003, T006.
- MS01 implementation + score file (70/100 with honesty notes).

### Next

- T007: negative structural tests + adversarial multi-session so ceiling is not free.
- T004: harder todo CLI pack.

---

## Pitfalls / decisions

- **Score inflation risk is real.** High structural scores do not imply Terminal-Bench-class skill.
- Collapsing multi-session packs into one agent turn must be penalized (MS01 did so → 70 not 100).
- Primary value is continuity under dialog reset; tests must force that.

---

## Scores

| When | Suite | Score | Notes |
|------|-------|-------|-------|
| 2026-11-03 | structural | 88.24 | baseline; easy file contracts |
| 2026-11-03 | ms01_counter | 70 | impl+verify ok; session/scope partial |
| 2026-11-03 | **aggregate (equal weight)** | **79.12** | not frontier-hard |

---

## Log

### 2026-11-03

- MS01 completed in single push; scored honestly below 100.
- Acknowledged eval too easy; queued T007.
