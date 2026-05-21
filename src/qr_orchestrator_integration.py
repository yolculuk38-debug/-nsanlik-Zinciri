"""Integration between QR hardening and the verification orchestrator."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from qr_hardening import QRStatus, verify_qr_payload


_TERMINAL_QR_FAILURES = {
    QRStatus.INVALID_QR.value,
    QRStatus.UNSAFE_URL.value,
    QRStatus.HASH_MISMATCH.value,
}


def _checked_at_value(checked_at: str | None) -> str:
    if checked_at:
        return checked_at
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _to_orchestrator_qr_result(qr_result: dict[str, Any]) -> dict[str, Any]:
    return {
        "trusted": qr_result.get("status") == QRStatus.VERIFIED.value,
        "status": qr_result.get("status"),
        "reason": qr_result.get("reason"),
    }


def verify_qr_with_orchestrator(
    payload: str | dict[str, Any],
    trust_score_result: dict[str, Any] | None = None,
    audit_result: dict[str, Any] | None = None,
    consensus_result: dict[str, Any] | None = None,
    signature_result: dict[str, Any] | None = None,
    checked_at: str | None = None,
) -> dict[str, Any]:
    """Verify QR payload first, then merge it into orchestrator decisioning."""

    qr_result = verify_qr_payload(payload)
    orchestrator_qr_result = _to_orchestrator_qr_result(qr_result)

    record_id = payload.get("record_id") if isinstance(payload, dict) else "QR-UNKNOWN"
    if not record_id:
        record_id = "QR-UNKNOWN"

    from verification_orchestrator import orchestrate_verification

    result = orchestrate_verification(
        record_id,
        qr_result=orchestrator_qr_result,
        consensus_result=consensus_result,
        audit_result=audit_result,
        signature_result=signature_result,
        trust_score_result=trust_score_result,
        checked_at=_checked_at_value(checked_at),
    )

    layer_results = result.setdefault("layer_results", {})
    layer_results["qr_result"] = qr_result

    if qr_result.get("status") in _TERMINAL_QR_FAILURES:
        result["decision"] = "UNTRUSTED"
        result["trusted"] = False

    return result
