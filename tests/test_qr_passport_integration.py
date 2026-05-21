from qr_passport_integration import verify_qr_trust_passport


def test_verified_qr_passport():
    payload = {
        "record_id": "HC-1",
        "short_hash": "abc123",
    }

    result = verify_qr_trust_passport(
        payload,
        signals={
            "hash_verified": True,
            "trust_score": 95,
            "witness_count": 4,
            "provenance_locked": True,
            "federated_verified": True,
        },
    )

    assert result["status_engine"]["state"] in {"VERIFIED", "PARTIAL"}


def test_invalid_qr_passport():
    result = verify_qr_trust_passport(
        "invalid-payload",
        signals={
            "hash_verified": False,
            "trust_score": 0,
        },
    )

    assert result["status_engine"]["state"] in {"INVALID", "UNTRUSTED"}
