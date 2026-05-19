"""Normalize Humanity Chain JSON records with stable formatting."""

from __future__ import annotations

import json
from pathlib import Path

RECORDS_DIR = Path("records")


def normalize_record(record_path: Path) -> None:
    """Load and rewrite one JSON record using stable formatting only."""
    data = json.loads(record_path.read_text(encoding="utf-8"))
    normalized = json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    record_path.write_text(normalized, encoding="utf-8")
    print(record_path)


def main() -> None:
    if not RECORDS_DIR.exists():
        print("records directory not found.")
        return

    for record_path in sorted(RECORDS_DIR.rglob("*.json")):
        normalize_record(record_path)


if __name__ == "__main__":
    main()
