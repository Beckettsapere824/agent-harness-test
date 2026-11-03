# Multi-session task packs

Each pack under `msXX_*/` defines a small software goal split across sessions.
The agent must leave state only in the repo so the next session can continue.

## Pack layout (convention)

```
ms01_counter/
  SPEC.md           # overall goal + session boundaries
  sessions/         # optional prompts per session
  verify.sh         # golden checks; exit 0 = pass
  work/             # agent workspace (created during run)
```

See SPEC files as packs are added (T003+).
