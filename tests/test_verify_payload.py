import pytest

from hc_trust.verify_payload import build_verification_payload


def test_build_verification_payload_verified_response():
    response = {
        "record_id": "HC-TEST-2026-0001",
        "trust_score": 91,
        "trust_level": "STRONG_VERIFIED",
        "indicators": [],
        "verified_at": "2026-05-20T13:00:00+00:00",
    }

    payload = build_verification_payload(response)

    assert payload == {
        "record_id": "HC-TEST-2026-0001",
        "verified": True,
        "trust_level": "STRONG_VERIFIED",
        "score": 91,
        "hash_valid": True,
        "witness_count": 0,
        "timestamp": "2026-05-20T13:00:00+00:00",
        "experimental": True,
    }


def test_build_verification_payload_hash_mismatch():
    response = {
        "record_id": "HC-TEST-2026-0002",
        "trust_score": 60,
        "trust_level": "PARTIAL_TRUST",
        "indicators": ["hash_mismatch"],
        "verified_at": "2026-05-20T13:00:00+00:00",
    }

    payload = build_verification_payload(response)

    assert payload["verified"] is False
    assert payload["hash_valid"] is False
    assert payload["score"] == 60


def test_build_verification_payload_requires_fields():
    with pytest.raises(ValueError, match="missing required verification response fields"):
        build_verification_payload({"record_id": "HC-TEST-2026-0003"})
