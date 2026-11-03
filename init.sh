#!/usr/bin/env bash
set -euo pipefail

echo "== agent-harness-test init =="

required_files=(
  "AGENT.md"
  "MEMORY.md"
  "feature_list.json"
  "progress.md"
  "TASKS.md"
)

missing=0
for f in "${required_files[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "MISSING: $f"
    missing=1
  else
    echo "OK: $f"
  fi
done

if [[ $missing -ne 0 ]]; then
  echo "init failed: required files missing"
  exit 1
fi

if command -v python3 >/dev/null 2>&1; then
  python3 -c "import json; json.load(open('feature_list.json'))" \
    && echo "OK: feature_list.json valid JSON" \
    || { echo "FAIL: feature_list.json invalid"; exit 1; }

  if [[ -d eval ]]; then
    python3 -m eval.run_suite --suite structural --quiet \
      && echo "OK: structural suite passed" \
      || { echo "FAIL: structural suite"; exit 1; }
  fi
else
  echo "WARN: python3 not found; skipped JSON/suite checks"
fi

echo "== init complete =="
