# AGENT.md — Operating Contract for Any Agent

This file is the **entry point**. Any coding agent (Grok, Claude, Codex, etc.) working in this repository must read it first.

Read order: `AGENT.md` → `MEMORY.md` → `feature_list.json` → `progress.md` (and `session-handoff.md` if present) → run `./init.sh`.

---

## Mission

Evolve and measure a portable repo-native agent harness. Use structured multi-session coding tasks and harness-component checks to raise reliability scores; optimize by adopting patterns from frontier open harnesses and by fixing observed failure modes.

---

## Startup Workflow (mandatory)

Before writing code or claiming progress:

1. Confirm working directory / repo context.
2. Read this file completely.
3. Read `MEMORY.md` (status, pitfalls, recent log).
4. Run `./init.sh`. Fix failures before new scope.
5. Read `feature_list.json`. Select **exactly one** unfinished feature.
6. Read `progress.md` and `session-handoff.md` if they exist.
7. Load `eval/` or `docs/` only when needed for the chosen feature.

If baseline verification fails, repair that first.

---

## Working Rules (invariants)

- **One feature at a time.** Do not start a second feature until the current one has evidence of done.
- **Verification required.** Do not mark done without running verification and recording evidence.
- **Repo is the system of record.** Chat history is ephemeral.
- **Stay in scope.** Do not rewrite the feature list to hide unfinished work.
- **Leave clean state.** Next session must run `./init.sh` immediately.
- **Honest reporting.** Mark drafts unfinished; report failures as failures.

---

## Definition of Done

A feature is done only when **all** are true:

- [ ] Target behavior implemented
- [ ] Required verification ran
- [ ] Evidence recorded in `feature_list.json` or `progress.md`
- [ ] Repo restartable from standard startup path

---

## End of Session / Dialog

1. Update `progress.md` (state + next concrete step).
2. Update `feature_list.json` status and evidence.
3. If incomplete, refresh `session-handoff.md`.
4. Commit only when tree is restartable.

---

## Verification Commands

```bash
./init.sh
# Full structural suite (after Python deps available):
python3 -m eval.run_suite --suite structural
```

---

## Pointers

| Path | Role |
|------|------|
| `MEMORY.md` | Status, pitfalls, log |
| `feature_list.json` | Scope + evidence |
| `progress.md` | Live continuity |
| `session-handoff.md` | Handoff |
| `init.sh` | Startup + verification |
| `eval/` | Benchmarks, tasks, runner, scores |
| `TASKS.md` | Long-running program (solidified) |
| `docs/` | On-demand detail |
