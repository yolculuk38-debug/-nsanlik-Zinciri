#!/usr/bin/env python3
"""Normalize Humanity Chain record files."""

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path


def generate_hash(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def normalize_record(record_path):
    with open(record_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = False

    if "timestamp" not in data:
        data["timestamp"] = datetime.utcnow().isoformat() + "Z"
        updated = True

    if "status" not in data:
        data["status"] = "draft"
        updated = True

    if "content" in data:
        calculated_hash = generate_hash(data["content"])
        if data.get("content_hash") != calculated_hash:
            data["content_hash"] = calculated_hash
            updated = True

    if "metadata" not in data:
        data["metadata"] = {}
        updated = True

    if updated:
        with open(record_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[UPDATED] {record_path}")
    else:
        print(f"[OK] {record_path}")


def run(records_dir="records"):
    records_path = Path(records_dir)
    if not records_path.exists():
        print("records directory not found.")
        return 1

    for record_file in records_path.rglob("*.json"):
        normalize_record(record_file)

    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        description="Normalize records by filling missing defaults and refreshing content_hash."
    )
    parser.add_argument(
        "records_dir",
        nargs="?",
        default="records",
        help="Directory containing JSON records (default: records)",
    )
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    return run(args.records_dir)


if __name__ == "__main__":
    raise SystemExit(main())
