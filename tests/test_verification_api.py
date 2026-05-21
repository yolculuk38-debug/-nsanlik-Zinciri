from verification_api import VerificationDecision, build_verification_response


def test_verified_response():
    result = build_verification_response(
        "HC-2026-0001",
        {
            "hash": True,
            "qr": True,
            "consensus": True,
            "audit": True,
            "signature": True,
            "trust_score": 90,
        },
        checked_at="2026-05-21T00:00:00Z",
    )

    assert result["decision"] == VerificationDecision.VERIFIED
    assert result["trusted"] is True


def test_partial_response():
    result = build_verification_response(
        "HC-2026-0001",
        {
            "hash": True,
            "qr": True,
            "consensus": True,
            "trust_score": 70,
        },
        checked_at="2026-05-21T00:00:00Z",
    )

    assert result["decision"] == VerificationDecision.PARTIAL
    assert result["trusted"] is False


def test_untrusted_missing_hash():
    result = build_verification_response(
        "HC-2026-0001",
        {"hash": False, "trust_score": 90},
        checked_at="2026-05-21T00:00:00Z",
    )

    assert result["decision"] == VerificationDecision.UNTRUSTED


def test_invalid_response():
    result = build_verification_response("", {}, checked_at="2026-05-21T00:00:00Z")
    assert result["decision"] == VerificationDecision.INVALID


def test_trust_score_clamped():
    result = build_verification_response(
        "HC-2026-0001",
        {"hash": True, "trust_score": 999},
        checked_at="2026-05-21T00:00:00Z",
    )

    assert result["signals"]["trust_score"] == 100
