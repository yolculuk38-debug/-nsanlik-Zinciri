import pytest

from hc_trust.deterministic_export import (
    build_export_digest,
    build_export_package,
    canonical_export,
    verify_export_package,
)


def test_canonical_export_is_deterministic():
    first = canonical_export({"b": 2, "a": 1})
    second = canonical_export({"a": 1, "b": 2})

    assert first == second
    assert first == '{"a":1,"b":2}'


def test_build_export_digest_is_stable():
    first = build_export_digest({"record_id": "HC-001", "score": 91})
    second = build_export_digest({"score": 91, "record_id": "HC-001"})

    assert first == second
    assert len(first) == 64


def test_build_export_package_verifies():
    package = build_export_package({"record_id": "HC-001", "score": 91})

    assert package["deterministic"] is True
    assert verify_export_package(package) is True


def test_verify_export_package_rejects_tampered_digest():
    package = build_export_package({"record_id": "HC-001", "score": 91})
    package["export_digest"] = "0" * 64

    assert verify_export_package(package) is False


def test_canonical_export_rejects_non_dict():
    with pytest.raises(ValueError, match="data must be a dictionary"):
        canonical_export(["not", "a", "dict"])
