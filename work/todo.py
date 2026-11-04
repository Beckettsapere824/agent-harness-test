#!/usr/bin/env python3
"""Todo CLI — MS02. Session S1: add + list only."""

from __future__ import annotations

import json
import sys
from pathlib import Path

STORE = Path(__file__).resolve().parent / "todos.json"


def load() -> list:
    if not STORE.is_file():
        return []
    return json.loads(STORE.read_text(encoding="utf-8"))


def save(items: list) -> None:
    STORE.parent.mkdir(parents=True, exist_ok=True)
    STORE.write_text(json.dumps(items, indent=2) + "\n", encoding="utf-8")


def next_id(items: list) -> int:
    if not items:
        return 1
    return max(int(x["id"]) for x in items) + 1


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: todo.py {add TEXT|list}", file=sys.stderr)
        return 2
    cmd = argv[1]
    items = load()

    if cmd == "add":
        if len(argv) < 3:
            print("usage: todo.py add TEXT", file=sys.stderr)
            return 2
        text = " ".join(argv[2:])
        items.append({"id": next_id(items), "status": "open", "text": text})
        save(items)
        return 0

    if cmd == "list":
        for it in items:
            print(f"{it['id']} {it['status']} {it['text']}")
        return 0

    # S1 boundary: done/rm not implemented yet
    print(
        f"unknown or not-yet-implemented in S1: {cmd}\n"
        "S1 allows only: add, list",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
