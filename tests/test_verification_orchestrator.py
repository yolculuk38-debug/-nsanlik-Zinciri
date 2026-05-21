from verification_api import VerificationDecision
from verification_orchestrator import orchestrate_verification


def test_orchestrator_verified_response():
    result = orchestrate_verification(
        "HC-2026-0001",
        hash_result={"verified": True},
        qr_result={"trusted": True},
        consensus_result={"trusted": True},
        audit_result={"verified": True},
        signature_result={"verified": True},
        trust_score_result={"trust_score": 95},
        checked_at="2026-05-21T00:00:00Z",
    )

    assert result["decision"] == VerificationDecision.VERIFIED
    assert result["trusted"] is True
    assert result["orchestrator_version"] == "HC-ORCHESTRATOR-V1"


def test_orchestrator_untrusted_without_hash():
    result = orchestrate_verification(
        "HC-2026-0001",
        hash_result={"verified": False},
        trust_score_result={"trust_score": 95},
        checked_at="2026-05-21T00:00:00Z",
    )

    assert result["decision"] == VerificationDecision.UNTRUSTED
    assert result["trusted"] is False


def test_orchestrator_partial_response():
    result = orchestrate_verification(
        "HC-2026-0001",
        hash_result={"verified": True},
        qr_result={"trusted": True},
        consensus_result={"trusted": True},
        trust_score_result={"trust_score": 70},
        checked_at="2026-05-21T00:00:00Z",
    )

    assert result["decision"] == VerificationDecision.PARTIAL


def test_orchestrator_uses_decayed_score():
    result = orchestrate_verification(
        "HC-2026-0001",
        hash_result={"verified": True},
        qr_result={"trusted": True},
        consensus_result={"trusted": True},
        audit_result={"verified": True},
        trust_score_result={"decayed_score": 88},
        checked_at="2026-05-21T00:00:00Z",
    )

    assert result["signals"]["trust_score"] == 88
