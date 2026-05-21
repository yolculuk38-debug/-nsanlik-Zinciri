import argparse
import json
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List


REQUIRED_FIELDS = {
    "package_id",
    "created_at",
    "protocol_version",
    "source_repo",
    "records_count",
    "snapshot_count",
    "records",
    "snapshots",
    "package_hash",
}


def _canonical_json(data: Dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha256_text(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def _verify_record_hashes(records: List[Dict[str, Any]]) -> List[str]:
    failures: List[str] = []
    for idx, item in enumerate(records):
        data = item.get("data", {}) if isinstance(item, dict) else {}
        if not isinstance(data, dict):
            failures.append(f"record[{idx}] has invalid data structure")
            continue

        if "content" in data and "content_hash" in data:
            calculated = _sha256_text(
                data["content"] if isinstance(data["content"], str) else _canonical_json(data["content"])
            )
            if data["content_hash"] != calculated:
                failures.append(f"record[{idx}] content_hash mismatch")
    return failures


def _verify_snapshot_references(snapshots: List[Dict[str, Any]]) -> List[str]:
    failures: List[str] = []
    for idx, item in enumerate(snapshots):
        if not isinstance(item, dict):
            failures.append(f"snapshot[{idx}] invalid structure")
            continue
        data = item.get("data")
        if data is not None and not isinstance(data, dict):
            failures.append(f"snapshot[{idx}] data must be object when present")
    return failures


def verify_package_dict(package: Dict[str, Any]) -> tuple[bool, List[str]]:
    errors: List[str] = []
    missing = sorted(REQUIRED_FIELDS - set(package.keys()))
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")
        return False, errors

    copy_without_hash = dict(package)
    declared_hash = copy_without_hash.pop("package_hash")
    calculated_hash = _sha256_text(_canonical_json(copy_without_hash))
    if declared_hash != calculated_hash:
        errors.append("package_hash mismatch")

    if package.get("records_count") != len(package.get("records", [])):
        errors.append("records_count does not match records length")
    if package.get("snapshot_count") != len(package.get("snapshots", [])):
        errors.append("snapshot_count does not match snapshots length")

    errors.extend(_verify_record_hashes(package.get("records", [])))
    errors.extend(_verify_snapshot_references(package.get("snapshots", [])))

    return len(errors) == 0, errors


def verify_package_file(path: Path) -> tuple[bool, List[str]]:
    try:
        package = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return False, [f"unable to read package: {exc}"]

    if not isinstance(package, dict):
        return False, ["package root must be a JSON object"]

    return verify_package_dict(package)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify an HC:// export package")
    parser.add_argument("package_file", help="Path to package JSON file")
    args = parser.parse_args()

    ok, errors = verify_package_file(Path(args.package_file))
    if ok:
        print("PASS: package verification succeeded")
        return 0

    print("FAIL: package verification failed")
    for err in errors:
        print(f"- {err}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
