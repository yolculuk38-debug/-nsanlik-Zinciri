import types

from qr_hardening import sha256_text
from qr_orchestrator_integration import verify_qr_with_orchestrator


SAFE_URL = "https://github.com/yolculuk38-debug/HC-TRUST-LAYER/blob/main/docs/index.md"


def build_payload(content="HC:// TRUST", signed=True):
    payload = {
        "record_id": "HC-QR-2026-0001",
        "content": content,
        "content_hash": sha256_text(content),
        "verification_url": SAFE_URL,
        "created_at": "2026-05-21T09:20:00Z",
    }
    if signed:
        payload["signature"] = "HC-SIGNATURE"
    return payload


def install_stub_orchestrator(monkeypatch):
    def _orchestrate_verification(
        record_id,
        hash_result=None,
        qr_result=None,
        consensus_result=None,
        audit_result=None,
        signature_result=None,
        trust_score_result=None,
        checked_at=None,
    ):
        decision = "PARTIAL"
        trusted = False
        score = (trust_score_result or {}).get("trust_score")
        if qr_result and qr_result.get("trusted") and score and score >= 90:
            decision = "VERIFIED"
            trusted = True
        elif score and score < 50:
            decision = "UNTRUSTED"

        return {
            "record_id": record_id,
            "decision": decision,
            "trusted": trusted,
            "checked_at": checked_at,
            "layer_results": {},
        }

    stub = types.SimpleNamespace(orchestrate_verification=_orchestrate_verification)
    monkeypatch.setitem(__import__("sys").modules, "verification_orchestrator", stub)


def test_valid_signed_qr_returns_verified_or_partial(monkeypatch):
    install_stub_orchestrator(monkeypatch)
    result_verified = verify_qr_with_orchestrator(
        build_payload(), trust_score_result={"trust_score": 95}, checked_at="2026-05-21T00:00:00Z"
    )
    assert result_verified["decision"] == "VERIFIED"

    result_partial = verify_qr_with_orchestrator(
        build_payload(), trust_score_result={"trust_score": 70}, checked_at="2026-05-21T00:00:00Z"
    )
    assert result_partial["decision"] == "PARTIAL"


def test_unsafe_qr_returns_untrusted(monkeypatch):
    install_stub_orchestrator(monkeypatch)
    payload = build_payload()
    payload["verification_url"] = "https://evil.example/phishing"

    result = verify_qr_with_orchestrator(payload, trust_score_result={"trust_score": 99})

    assert result["decision"] == "UNTRUSTED"
    assert result["trusted"] is False


def test_tampered_qr_returns_untrusted(monkeypatch):
    install_stub_orchestrator(monkeypatch)
    payload = build_payload()
    payload["content"] = "tampered"

    result = verify_qr_with_orchestrator(payload, trust_score_result={"trust_score": 99})

    assert result["decision"] == "UNTRUSTED"


def test_unsigned_qr_not_auto_trusted(monkeypatch):
    install_stub_orchestrator(monkeypatch)

    partial = verify_qr_with_orchestrator(build_payload(signed=False), trust_score_result={"trust_score": 70})
    assert partial["decision"] == "PARTIAL"
    assert partial["trusted"] is False

    untrusted = verify_qr_with_orchestrator(build_payload(signed=False), trust_score_result={"trust_score": 40})
    assert untrusted["decision"] == "UNTRUSTED"
    assert untrusted["trusted"] is False


def test_response_includes_original_qr_result(monkeypatch):
    install_stub_orchestrator(monkeypatch)

    result = verify_qr_with_orchestrator(build_payload(signed=False), trust_score_result={"trust_score": 70})

    assert "qr_result" in result["layer_results"]
    assert result["layer_results"]["qr_result"]["status"] == "UNSIGNED"
