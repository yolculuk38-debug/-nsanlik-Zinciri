from status_passport_integration import build_status_passport


def test_verified_status_passport():
    passport = build_status_passport(
        "HC-1",
        {
            "hash_verified": True,
            "witness_count": 4,
            "provenance_locked": True,
            "federated_verified": True,
            "trust_score": 95,
        },
    )

    assert passport["status_engine"]["state"] == "VERIFIED"
    assert passport["verification_level"] == "LEVEL_5_FEDERATED_VERIFIED"


def test_review_required_passport():
    passport = build_status_passport(
        "HC-2",
        {
            "hash_verified": True,
            "witness_count": 1,
            "trust_score": 55,
            "risk_flags": ["edited_media"],
        },
    )

    assert passport["status_engine"]["state"] == "REVIEW_REQUIRED"
