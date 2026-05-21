from verification_certificate import build_verification_certificate


def test_certificate_build():
    certificate = build_verification_certificate(
        {
            "decision": "VERIFIED",
            "verified": True,
            "verification_level": "LEVEL_4_PROVENANCE_LOCKED",
            "risk_flags": [],
            "reasons": [],
        }
    )

    assert certificate["verified"] is True
    assert certificate["portable"] is True
    assert certificate["human_readable"] is True
