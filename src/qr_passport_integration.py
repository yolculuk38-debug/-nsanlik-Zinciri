"""HC:// QR verification to trust passport integration."""

from __future__ import annotations

from typing import Any

from qr_orchestrator_integration import verify_qr_with_orchestrator
from status_passport_integration import build_status_passport


INTEGRATION_VERSION = "HC-QR-PASSPORT-INTEGRATION-V1"


def verify_qr_trust_passport(
    payload: str | dict[str, Any],
    *,
    signals: dict[str, Any] | None = None,
    trust_score_result: dict[str, Any] | None = None,
    audit_result: dict[str, Any] | None = None,
    consensus_result: dict[str, Any] | None = None,
    signature_result: dict[str, Any] | None = None,
    checked_at: str | None = None,
) -> dict[str, Any]:
    """Verify QR payload and return a user-facing trust passport."""

    verification_response = verify_qr_with_orchestrator(
        payload,
        trust_score_result=trust_score_result,
        audit_result=audit_result,
        consensus_result=consensus_result,
        signature_result=signature_result,
        checked_at=checked_at,
    )

    record_id = None
    if isinstance(payload, dict):
        record_id = payload.get("record_id")
    record_id = record_id or verification_response.get("record_id") or "UNKNOWN"

    merged_signals = dict(signals or {})
    response_signals = verification_response.get("signals", {}) if isinstance(verification_response, dict) else {}

    merged_signals.setdefault("hash_verified", bool(response_signals.get("hash", False)))
    merged_signals.setdefault("trust_score", int(response_signals.get("trust_score", 0) or 0))
    merged_signals.setdefault("witness_count", 3 if response_signals.get("consensus") else 0)
    merged_signals.setdefault("provenance_locked", bool(response_signals.get("audit", False)))

    if verification_response.get("decision") in {"UNTRUSTED", "INVALID"}:
        merged_signals["invalid"] = True
        merged_signals.setdefault("risk_flags", [])
        merged_signals["risk_flags"] = list(merged_signals["risk_flags"]) + ["qr_verification_failed"]

    passport = build_status_passport(
        record_id,
        merged_signals,
        verification_response=verification_response,
    )
    passport["integration_version"] = INTEGRATION_VERSION
    passport["qr_verification"] = verification_response
    return passport


__all__ = ["INTEGRATION_VERSION", "verify_qr_trust_passport"]
