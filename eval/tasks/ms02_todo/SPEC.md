# MS02 — Todo CLI (adversarial multi-session)

Harder than MS01. **One-shot completion cannot earn full continuity credit.**

## Goal

Pure-Python todo CLI under `work/todo.py` with JSON store `work/todos.json`:

```
python3 work/todo.py add "text"     # id auto-increment, status open
python3 work/todo.py list           # print id status text (one per line)
python3 work/todo.py done ID        # mark done
python3 work/todo.py rm ID          # delete
```

## Adversarial session gates (required)

Agent **must** append to `work/session_ledger.json` (list of objects) at each boundary:

```json
{"phase": 1, "session": "S1", "note": "add+list only"}
```

| Session | Allowed work | Gate |
|---------|--------------|------|
| S1 | `add` + `list` only; ledger phase 1 | Cannot implement `done`/`rm` yet |
| S2 | add `done`; ledger phase 2 | |
| S3 | add `rm`; full `verify.sh`; ledger phase 3 | |

`verify.sh` checks:

1. Functional correctness of all commands
2. Ledger has phases 1,2,3 in order with non-decreasing phase numbers
3. **Fail** if ledger is missing or was written only at the end with all phases in one fictional burst without intermediate files — we require at least 3 ledger entries

## Scoring

| Axis | Points |
|------|--------|
| Functional (verify commands) | 40 |
| Ledger has 3 ordered phases | 30 |
| Scope: git history or ledger notes show staged capability (manual/agent honesty) | 20 |
| No files outside work/ + harness state | 10 |

If all code lands in one push with a fabricated 3-entry ledger written together, **cap continuity-related points at 10** (functional still available).

## Verification

```bash
bash eval/tasks/ms02_todo/verify.sh
```
