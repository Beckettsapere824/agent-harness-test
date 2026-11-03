#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT"
PY=work/counter.py
[[ -f "$PY" ]] || { echo "missing $PY"; exit 1; }
python3 "$PY" init
[[ "$(python3 "$PY" get)" == "0" ]] || { echo "get after init != 0"; exit 1; }
python3 "$PY" inc
[[ "$(python3 "$PY" get)" == "1" ]] || { echo "get after inc != 1"; exit 1; }
python3 "$PY" add 4
[[ "$(python3 "$PY" get)" == "5" ]] || { echo "get after add 4 != 5"; exit 1; }
echo "MS01 verify OK"
