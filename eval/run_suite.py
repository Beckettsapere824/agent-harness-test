#!/usr/bin/env python3
"""Run harness evaluation suites and write score JSON."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def check_structural() -> dict:
    """Five-subsystem + file contract checks. Each item: pass bool + detail."""
    checks = []

    def add(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"name": name, "pass": bool(ok), "detail": detail})

    # Instructions
    agent = ROOT / "AGENT.md"
    add("instructions.AGENT.md_exists", agent.is_file())
    if agent.is_file():
        text = agent.read_text(encoding="utf-8")
        add("instructions.has_startup", "Startup" in text or "startup" in text.lower())
        add("instructions.has_definition_of_done", "Definition of Done" in text or "done" in text.lower())
        add("instructions.not_encyclopedia", len(text) < 12000, f"chars={len(text)}")

    # State
    memory = ROOT / "MEMORY.md"
    fl = ROOT / "feature_list.json"
    progress = ROOT / "progress.md"
    add("state.MEMORY.md_exists", memory.is_file())
    add("state.feature_list.json_exists", fl.is_file())
    add("state.progress.md_exists", progress.is_file())
    if fl.is_file():
        try:
            data = json.loads(fl.read_text(encoding="utf-8"))
            feats = data.get("features") or []
            add("state.feature_list_valid", isinstance(feats, list) and len(feats) >= 1)
            statuses = [f.get("status") for f in feats if isinstance(f, dict)]
            in_prog = sum(1 for s in statuses if s == "in_progress")
            add("state.at_most_one_in_progress", in_prog <= 1, f"in_progress={in_prog}")
        except json.JSONDecodeError as e:
            add("state.feature_list_valid", False, str(e))

    # Verification
    init = ROOT / "init.sh"
    add("verification.init.sh_exists", init.is_file())
    if agent.is_file():
        t = agent.read_text(encoding="utf-8")
        add("verification.commands_documented", "init.sh" in t or "Verification" in t)

    # Scope
    add("scope.feature_list_has_dod", False)
    if fl.is_file():
        try:
            data = json.loads(fl.read_text(encoding="utf-8"))
            feats = data.get("features") or []
            ok = all(
                isinstance(f.get("definition_of_done"), list) and len(f["definition_of_done"]) > 0
                for f in feats
                if isinstance(f, dict)
            )
            add("scope.feature_list_has_dod", ok)
        except json.JSONDecodeError:
            pass

    # Lifecycle
    handoff = ROOT / "session-handoff.md"
    tasks = ROOT / "TASKS.md"
    add("lifecycle.session-handoff_exists", handoff.is_file())
    add("lifecycle.TASKS.md_exists", tasks.is_file())
    add("lifecycle.progress_mentions_next", False)
    if progress.is_file():
        p = progress.read_text(encoding="utf-8").lower()
        add("lifecycle.progress_mentions_next", "next" in p)

    passed = sum(1 for c in checks if c["pass"])
    total = len(checks)
    score = round(100.0 * passed / total, 2) if total else 0.0
    return {
        "suite": "structural",
        "score": score,
        "passed": passed,
        "total": total,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", default="structural", choices=["structural", "all"])
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    results = []
    if args.suite in ("structural", "all"):
        results.append(check_structural())

    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    out_dir = ROOT / "eval" / "scores"
    payload = {
        "timestamp_utc": ts,
        "results": results,
        "aggregate_score": round(sum(r["score"] for r in results) / len(results), 2) if results else 0.0,
    }

    if not args.no_write:
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / f"{ts}-structural.json"
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        if not args.quiet:
            print(f"wrote {path}")

    if not args.quiet:
        print(json.dumps(payload, indent=2))

    # Fail if any suite score < 50 (hard floor for init)
    bad = any(r["score"] < 50 for r in results)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
