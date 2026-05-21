import argparse
import json
import subprocess
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List


PROTOCOL_VERSION = "hc-export-package-v1"


def _canonical_json(data: Dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha256_text(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def _load_json_file(path: Path) -> Dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _collect_records(repo_root: Path) -> List[Dict[str, Any]]:
    verified_dir = repo_root / "records" / "verified"
    if not verified_dir.exists() or not verified_dir.is_dir():
        return []

    records: List[Dict[str, Any]] = []
    for record_path in sorted(verified_dir.rglob("*.json")):
        record = _load_json_file(record_path)
        if isinstance(record, dict):
            records.append({"path": str(record_path.relative_to(repo_root)), "data": record})
    return records


def _collect_snapshots(repo_root: Path) -> List[Dict[str, Any]]:
    snapshots: List[Dict[str, Any]] = []
    for dirname in ("audit", "snapshots"):
        directory = repo_root / dirname
        if not directory.exists() or not directory.is_dir():
            continue
        for snapshot_path in sorted(directory.rglob("*.json")):
            snapshot = _load_json_file(snapshot_path)
            if isinstance(snapshot, dict):
                snapshots.append({"path": str(snapshot_path.relative_to(repo_root)), "data": snapshot})
    return snapshots


def _detect_source_repo(repo_root: Path) -> str:
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo_root), "config", "--get", "remote.origin.url"],
            capture_output=True,
            text=True,
            check=False,
        )
        value = completed.stdout.strip()
        return value or "unknown"
    except OSError:
        return "unknown"


def build_export_package(repo_root: Path) -> Dict[str, Any]:
    records = _collect_records(repo_root)
    snapshots = _collect_snapshots(repo_root)

    package: Dict[str, Any] = {
        "package_id": f"hc-pkg-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "protocol_version": PROTOCOL_VERSION,
        "source_repo": _detect_source_repo(repo_root),
        "records_count": len(records),
        "snapshot_count": len(snapshots),
        "records": records,
        "snapshots": snapshots,
    }

    package["package_hash"] = _sha256_text(_canonical_json(package))
    return package


def export_package(output_path: Path, repo_root: Path) -> Dict[str, Any]:
    package = build_export_package(repo_root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(package, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    return package


def main() -> int:
    parser = argparse.ArgumentParser(description="Build an HC:// export verification package")
    parser.add_argument("--output", default="exports/verification-package.json", help="Output JSON path")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    args = parser.parse_args()

    package = export_package(Path(args.output), Path(args.repo_root))
    print(f"PASS: export package created -> {args.output}")
    print(f"records={package['records_count']} snapshots={package['snapshot_count']}")
    print(f"package_hash={package['package_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
