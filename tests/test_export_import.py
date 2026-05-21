import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import json
from src.export_package import build_export_package, export_package
from src.import_verify import verify_package_dict, verify_package_file


def test_export_package_creation(tmp_path: Path):
    verified = tmp_path / "records" / "verified"
    verified.mkdir(parents=True)
    record = {
        "record_id": "HC-TEST-1",
        "content": "hello",
        "content_hash": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
    }
    (verified / "record.json").write_text(json.dumps(record), encoding="utf-8")

    snapshots = tmp_path / "audit"
    snapshots.mkdir(parents=True)
    (snapshots / "snapshot.json").write_text(json.dumps({"snapshot_id": "s1"}), encoding="utf-8")

    package = build_export_package(tmp_path)
    assert package["records_count"] == 1
    assert package["snapshot_count"] == 1
    assert "package_hash" in package and len(package["package_hash"]) == 64


def test_package_hash_recalculation(tmp_path: Path):
    package = build_export_package(tmp_path)
    ok, errors = verify_package_dict(package)
    assert ok is True
    assert errors == []


def test_valid_import_verification(tmp_path: Path):
    out = tmp_path / "pkg.json"
    export_package(out, tmp_path)
    ok, errors = verify_package_file(out)
    assert ok is True
    assert errors == []


def test_tampered_package_fails(tmp_path: Path):
    out = tmp_path / "pkg.json"
    package = export_package(out, tmp_path)
    package["records_count"] = 999
    out.write_text(json.dumps(package), encoding="utf-8")

    ok, errors = verify_package_file(out)
    assert ok is False
    assert any("mismatch" in err or "does not match" in err for err in errors)


def test_missing_required_fields_fail():
    ok, errors = verify_package_dict({"package_id": "x"})
    assert ok is False
    assert any("missing required fields" in err for err in errors)
