# agent-harness-test

Test bed for the portable agent harness.

- Harness files at repo root (`AGENT.md`, …).
- Long-running program: `TASKS.md`.
- Evaluation: `eval/` (structural suite + multi-session task packs).
- Benchmark notes: `docs/benchmarks.md`.

## Quick start

```bash
chmod +x init.sh
./init.sh
python3 -m eval.run_suite --suite structural
```

Any agent: read `AGENT.md` first, then continue from `session-handoff.md`.
