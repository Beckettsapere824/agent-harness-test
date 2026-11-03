# MEMORY.md — Persistent Project Memory

Newest entries at the **top** of each section.

---

## Status

### Current focus

- Bootstrap evaluation program in `agent-harness-test`.
- Establish baseline structural scores; then multi-session task scores.

### Done

- Harness core files copied from `agent-harness`.
- `TASKS.md` solidified for long-running optimization loop.
- Initial `eval/` suite: structural harness checks + synthetic multi-session tasks.

### Next

- Run structural suite; record baseline in `eval/scores/`.
- Implement / harden first multi-session task package.
- Iterate harness based on failures; pull patterns from frontier open source.

---

## Pitfalls / decisions

- External full SWE-bench / Terminal-Bench runs need container infra; treat them as **aspirational / offline** targets. Primary loop = structural + in-repo multi-session tasks that Grok can execute via GitHub + sandbox.
- Optimize for: cross-session continuity, verification gates, scope discipline, progressive disclosure — not token bloat.
- Prefer small pure-Python / shell tasks so verification is deterministic.

---

## Log

### 2026-11-03

- Initialized test repo with harness + evaluation program.
- Benchmark references: TraceTrial-Bench (7 components), Harness-Bench, Doc2Harness, Terminal-Bench / SWE-bench as external yardsticks; learn-harness five subsystems as internal rubric.
