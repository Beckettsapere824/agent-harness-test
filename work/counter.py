#!/usr/bin/env python3
"""Minimal persistent counter CLI for MS01 multi-session harness eval."""

from __future__ import annotations

import json
import sys
from pathlib import Path

STATE = Path(__file__).resolve().parent / "count.json"


def load() -> int:
    if not STATE.is_file():
        return 0
    data = json.loads(STATE.read_text(encoding="utf-8"))
    return int(data.get("count", 0))


def save(n: int) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps({"count": n}) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: counter.py {init|get|inc|add N}", file=sys.stderr)
        return 2
    cmd = argv[1]
    if cmd == "init":
        save(0)
        return 0
    if cmd == "get":
        print(load())
        return 0
    if cmd == "inc":
        save(load() + 1)
        return 0
    if cmd == "add":
        if len(argv) < 3:
            print("usage: counter.py add N", file=sys.stderr)
            return 2
        save(load() + int(argv[2]))
        return 0
    print(f"unknown command: {cmd}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
