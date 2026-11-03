#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT"
PY=work/todo.py
LEDGER=work/session_ledger.json
STORE=work/todos.json

[[ -f "$PY" ]] || { echo "missing $PY"; exit 1; }
[[ -f "$LEDGER" ]] || { echo "missing ledger $LEDGER"; exit 1; }

python3 - <<'PY'
import json, sys
from pathlib import Path
root = Path(".")
ledger = json.loads((root / "work/session_ledger.json").read_text())
if not isinstance(ledger, list) or len(ledger) < 3:
    print("ledger must be a list with >= 3 entries"); sys.exit(1)
phases = [e.get("phase") for e in ledger]
if any(p is None for p in phases):
    print("every ledger entry needs phase"); sys.exit(1)
if phases != sorted(phases):
    print("phases must be non-decreasing", phases); sys.exit(1)
if not (1 in phases and 2 in phases and 3 in phases):
    print("ledger must include phases 1,2,3"); sys.exit(1)
print("ledger OK", phases)
PY

rm -f "$STORE"
python3 "$PY" add "alpha"
python3 "$PY" add "beta"
out="$(python3 "$PY" list)"
echo "$out" | grep -q alpha || { echo "list missing alpha"; exit 1; }
echo "$out" | grep -q beta || { echo "list missing beta"; exit 1; }
# done first id
id1="$(echo "$out" | head -n1 | awk '{print $1}')"
python3 "$PY" done "$id1"
out2="$(python3 "$PY" list)"
echo "$out2" | grep -q done || { echo "expected a done item"; exit 1; }
python3 "$PY" rm "$id1"
out3="$(python3 "$PY" list)"
if echo "$out3" | grep -q "^${id1} "; then echo "rm failed"; exit 1; fi
echo "MS02 verify OK"
