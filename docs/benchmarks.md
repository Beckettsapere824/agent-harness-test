# Benchmark alignment

## What we run in this repository

| Suite | Location | Purpose |
|-------|----------|---------|
| Structural | `eval/run_suite.py --suite structural` | Five subsystems + file contracts (TraceTrial-inspired, learn-harness mapped) |
| Multi-session packs | `eval/tasks/ms*` | Continuity, handoff, verification under dialog resets |

## External yardsticks (not executed by default)

| Benchmark | Why it matters | Our mapping |
|-----------|----------------|-------------|
| Terminal-Bench | End-to-end terminal agent skill | Long-horizon execution + verification |
| SWE-bench / SWE-bench Verified / Pro | Issue→patch reliability | Scope + evidence + test gates |
| TraceTrial-Bench | Harness component reliability | Structural checks expand toward 7 axes |
| Harness-Bench | Realistic workflows | Multi-session packs |
| Doc2Harness | Building harnesses from specs | Meta: improving this repo’s harness |

Full containerized runs require Harbor/Docker-class infra. Until available, optimize on structural + multi-session packs and keep this mapping updated.
