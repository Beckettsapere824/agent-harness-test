#!/usr/bin/env python3
"""Run harness evaluation suites and write score JSON.

Suites:
  structural  — five subsystems + negative quality gates (harder than v1)
  continuity  — handoff/progress/feature alignment (penalizes shallow state)
  all         — both
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _add(checks: list, name: str, ok: bool, detail: str = "") -> None:
    checks.append({"name": name, "pass": bool(ok), "detail": detail})


def check_structural() -> dict:
    checks: list[dict] = []

    agent = ROOT / "AGENT.md"
    _add(checks, "instructions.AGENT.md_exists", agent.is_file())
    if agent.is_file():
        text = agent.read_text(encoding="utf-8")
        _add(checks, "instructions.has_startup", "Startup" in text or "startup" in text.lower())
        _add(checks, "instructions.has_definition_of_done", "Definition of Done" in text)
        _add(checks, "instructions.not_encyclopedia", len(text) < 12000, f"chars={len(text)}")
        _add(
            checks,
            "instructions.forbids_marking_done_without_verification",
            "Verification required" in text or "verification" in text.lower(),
        )

    memory = ROOT / "MEMORY.md"
    fl = ROOT / "feature_list.json"
    progress = ROOT / "progress.md"
    handoff = ROOT / "session-handoff.md"

    _add(checks, "state.MEMORY.md_exists", memory.is_file())
    _add(checks, "state.feature_list.json_exists", fl.is_file())
    _add(checks, "state.progress.md_exists", progress.is_file())

    feats: list = []
    if fl.is_file():
        try:
            data = json.loads(fl.read_text(encoding="utf-8"))
            feats = data.get("features") or []
            _add(checks, "state.feature_list_valid", isinstance(feats, list) and len(feats) >= 1)
            statuses = [f.get("status") for f in feats if isinstance(f, dict)]
            in_prog = sum(1 for s in statuses if s == "in_progress")
            _add(checks, "state.at_most_one_in_progress", in_prog <= 1, f"in_progress={in_prog}")
            # NEGATIVE: done features must have non-empty evidence
            done_ok = True
            weak = []
            for f in feats:
                if not isinstance(f, dict):
                    continue
                if f.get("status") == "done":
                    ev = (f.get("evidence") or "").strip()
                    if not ev:
                        done_ok = False
                        weak.append(f.get("id", "?"))
            _add(
                checks,
                "state.done_features_have_evidence",
                done_ok,
                "empty evidence: " + ",".join(weak) if weak else "",
            )
            ok_dod = all(
                isinstance(f.get("definition_of_done"), list) and len(f["definition_of_done"]) > 0
                for f in feats
                if isinstance(f, dict)
            )
            _add(checks, "scope.feature_list_has_dod", ok_dod)
            # NEGATIVE: no feature marked done with status typo / unknown
            allowed = {"todo", "in_progress", "done", "blocked"}
            bad_status = [f.get("id") for f in feats if isinstance(f, dict) and f.get("status") not in allowed]
            _add(checks, "state.known_statuses_only", not bad_status, str(bad_status))
        except json.JSONDecodeError as e:
            _add(checks, "state.feature_list_valid", False, str(e))
            _add(checks, "state.done_features_have_evidence", False, "invalid json")
            _add(checks, "scope.feature_list_has_dod", False, "invalid json")
            _add(checks, "state.known_statuses_only", False, "invalid json")

    init = ROOT / "init.sh"
    _add(checks, "verification.init.sh_exists", init.is_file())
    if agent.is_file():
        t = agent.read_text(encoding="utf-8")
        _add(checks, "verification.commands_documented", "init.sh" in t or "Verification" in t)
    if init.is_file():
        body = init.read_text(encoding="utf-8")
        _add(checks, "verification.init_is_executable_script", body.startswith("#!") or "set -" in body)

    tasks = ROOT / "TASKS.md"
    _add(checks, "lifecycle.session-handoff_exists", handoff.is_file())
    _add(checks, "lifecycle.TASKS.md_exists", tasks.is_file())
    if progress.is_file():
        p = progress.read_text(encoding="utf-8").lower()
        _add(checks, "lifecycle.progress_mentions_next", "next" in p)
    else:
        _add(checks, "lifecycle.progress_mentions_next", False)

    # NEGATIVE: MEMORY should track scores if scores/ exists
    scores_dir = ROOT / "eval" / "scores"
    if memory.is_file() and scores_dir.is_dir() and any(scores_dir.glob("*.json")):
        m = memory.read_text(encoding="utf-8").lower()
        _add(checks, "state.memory_mentions_scores", "score" in m)
    else:
        _add(checks, "state.memory_mentions_scores", True, "skipped (no scores yet)")

    passed = sum(1 for c in checks if c["pass"])
    total = len(checks)
    score = round(100.0 * passed / total, 2) if total else 0.0
    return {"suite": "structural", "score": score, "passed": passed, "total": total, "checks": checks}


def check_continuity() -> dict:
    """Alignment across progress / handoff / feature_list — fails shallow harness use."""
    checks: list[dict] = []
    fl = ROOT / "feature_list.json"
    progress = ROOT / "progress.md"
    handoff = ROOT / "session-handoff.md"

    active_ids = []
    if fl.is_file():
        try:
            feats = json.loads(fl.read_text(encoding="utf-8")).get("features") or []
            active_ids = [
                f.get("id")
                for f in feats
                if isinstance(f, dict) and f.get("status") == "in_progress"
            ]
        except json.JSONDecodeError:
            active_ids = []

    _add(checks, "continuity.exactly_one_or_zero_active", len(active_ids) <= 1, str(active_ids))

    prog_text = progress.read_text(encoding="utf-8") if progress.is_file() else ""
    hand_text = handoff.read_text(encoding="utf-8") if handoff.is_file() else ""

    if active_ids:
        aid = active_ids[0]
        _add(checks, "continuity.progress_names_active_id", aid in prog_text, aid)
        _add(checks, "continuity.handoff_names_active_id", aid in hand_text, aid)
    else:
        _add(checks, "continuity.progress_names_active_id", True, "no active")
        _add(checks, "continuity.handoff_names_active_id", True, "no active")

    # Handoff must have resume / remains style content
    _add(
        checks,
        "continuity.handoff_has_resume_section",
        bool(re.search(r"remain|resume|next|how to", hand_text, re.I)),
    )
    _add(
        checks,
        "continuity.progress_has_blocker_or_none",
        bool(re.search(r"blocker", prog_text, re.I)),
    )
    # Penalize empty handoff
    _add(checks, "continuity.handoff_min_length", len(hand_text.strip()) >= 120, f"len={len(hand_text.strip())}")
    _add(checks, "continuity.progress_min_length", len(prog_text.strip()) >= 80, f"len={len(prog_text.strip())}")

    # Session ledger for adversarial packs (optional until MS02 used)
    ledger = ROOT / "work" / "session_ledger.json"
    if ledger.is_file():
        try:
            entries = json.loads(ledger.read_text(encoding="utf-8"))
            if not isinstance(entries, list):
                raise ValueError("not a list")
            phases = [e.get("phase") for e in entries if isinstance(e, dict)]
            ordered = phases == sorted(phases, key=lambda x: (x is None, x))
            _add(checks, "continuity.ledger_phases_non_decreasing", ordered, str(phases))
            _add(checks, "continuity.ledger_min_entries", len(entries) >= 1, str(len(entries)))
        except (json.JSONDecodeError, ValueError) as e:
            _add(checks, "continuity.ledger_phases_non_decreasing", False, str(e))
            _add(checks, "continuity.ledger_min_entries", False, str(e))
    else:
        # Not required until an adversarial pack is in progress
        _add(checks, "continuity.ledger_phases_non_decreasing", True, "no ledger yet")
        _add(checks, "continuity.ledger_min_entries", True, "no ledger yet")

    passed = sum(1 for c in checks if c["pass"])
    total = len(checks)
    score = round(100.0 * passed / total, 2) if total else 0.0
    return {"suite": "continuity", "score": score, "passed": passed, "total": total, "checks": checks}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", default="all", choices=["structural", "continuity", "all"])
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    results = []
    if args.suite in ("structural", "all"):
        results.append(check_structural())
    if args.suite in ("continuity", "all"):
        results.append(check_continuity())

    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    out_dir = ROOT / "eval" / "scores"
    payload = {
        "timestamp_utc": ts,
        "results": results,
        "aggregate_score": round(sum(r["score"] for r in results) / len(results), 2) if results else 0.0,
    }

    if not args.no_write:
        out_dir.mkdir(parents=True, exist_ok=True)
        label = args.suite
        path = out_dir / f"{ts}-{label}.json"
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        if not args.quiet:
            print(f"wrote {path}")

    if not args.quiet:
        print(json.dumps(payload, indent=2))

    bad = any(r["score"] < 50 for r in results)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
