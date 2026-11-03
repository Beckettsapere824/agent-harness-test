# MS01 — Persistent Counter (multi-session)

## Goal

Build a tiny pure-Python CLI counter that persists to `work/count.json` and supports:

```
python3 work/counter.py init     # set count to 0
python3 work/counter.py inc      # +1
python3 work/counter.py get      # print current integer
python3 work/counter.py add N    # +N (integer)
```

## Why this tests the harness

Simulates **dialog resets**: each session starts with no chat memory and must recover from repo files only (`progress.md`, `session-handoff.md`, `work/`).

## Session boundaries (agent must stop at each boundary and leave handoff)

| Session | Work |
|---------|------|
| S1 | Create `work/counter.py` with `init` and `get` only; run init; leave handoff |
| S2 | Add `inc`; demonstrate get shows 1 after inc; leave handoff |
| S3 | Add `add N`; full verify via `verify.sh`; mark feature evidence |

## Verification

```bash
bash eval/tasks/ms01_counter/verify.sh
```

Exit 0 required for pack pass.

## Scoring (manual / future automation)

- +40 implement full CLI behavior
- +30 survive simulated session cuts (handoff quality)
- +20 verify.sh green without cheating
- +10 no scope creep outside `work/` and harness state files
