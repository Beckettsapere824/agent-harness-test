# TASKS.md — Solidified Long-Running Program

This document freezes the multi-session optimization program. Agents must follow it; humans review scores, not ad-hoc goals.

---

## Objective

Raise measurable harness reliability on:

1. **Structural suite** (always on, fast) — five subsystems + file contracts.
2. **Multi-session in-repo tasks** (primary training loop) — agent must continue across simulated dialog boundaries using only repo files.
3. **External yardsticks** (offline / aspirational) — map progress to Terminal-Bench, SWE-bench family, TraceTrial-Bench dimensions when infrastructure allows.

---

## Selected frontier references (test sets & rubrics)

| Reference | What we take |
|-----------|----------------|
| **TraceTrial-Bench** (7 components: context, execution, governance, lifecycle, observability, tools, verification) | Mechanism-oriented reliability axes; failure attribution mindset |
| **Harness-Bench** | Realistic workflow delivery under constraints |
| **Doc2Harness** | Long-horizon harness *construction* evaluation |
| **learn-harness-engineering five subsystems** | Instructions / State / Verification / Scope / Lifecycle |
| **Anthropic effective harnesses** | Initializer + coding agent; progress file; one feature; clean git state |
| **Terminal-Bench / SWE-bench** | External coding-agent yardsticks (containerized; not primary CI here) |
| **mini-SWE-agent / Codex / Claude Code open patterns** | Patterns to copy when our scores lag |

Primary executable suite lives under `eval/`. External benches are documented in `docs/benchmarks.md` (T006).

---

## Loop (repeat until scores plateau at frontier-competitive levels)

```
1. Pick exactly one unfinished feature from feature_list.json
2. Implement under harness discipline (AGENT.md)
3. Run verification (init.sh / eval.run_suite)
4. Record scores under eval/scores/YYYYMMDD-HHMMSS-*.json
5. Analyze failures → update MEMORY.md pitfalls
6. Optimize harness (copy from open frontier code or fix real failure mode)
7. Re-run; require measurable lift before marking done
8. Update progress.md + session-handoff.md; commit
```

---

## Score targets (v1)

| Suite | Baseline (start) | Target |
|-------|------------------|--------|
| Structural (0–100) | measure first run | ≥ 90 |
| Multi-session pack MS01 | measure first agent run | ≥ 80 |
| Multi-session pack MS02 | measure first agent run | ≥ 75 |
| External (Terminal-Bench etc.) | N/A in this env | document parity mapping only |

---

## Non-goals

- Full Harbor / Docker Terminal-Bench runs inside Grok sandbox (unless infra becomes available).
- Training models; only harness artifacts and task packs.

---

## Ownership

Any agent may continue from `session-handoff.md`. The human owner reviews score trends and may reprioritize features in `feature_list.json`.
