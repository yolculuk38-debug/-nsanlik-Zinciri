from certificate_verifier import verify_certificate


def test_valid_certificate():
    result = verify_certificate(
        {
            "certificate_version": "HC-CERTIFICATE-V1",
            "issuer": "HC://",
            "decision": "VERIFIED",
            "verified": True,
            "risk_flags": [],
        }
    )

    assert result["trusted"] is True


def test_certificate_review_required():
    result = verify_certificate(
        {
            "certificate_version": "HC-CERTIFICATE-V1",
            "issuer": "HC://",
            "decision": "VERIFIED",
            "verified": True,
            "risk_flags": ["spoof_risk"],
        }
    )

    assert result["decision"] == "REVIEW_REQUIRED"
