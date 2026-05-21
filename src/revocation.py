"""HC:// revocation layer."""

from __future__ import annotations

from typing import Any


REVOCATION_VERSION = "HC-REVOCATION-V1"


class RevocationStatus:
    ACTIVE = "ACTIVE"
    REVOKED = "REVOKED"
    SUSPENDED = "SUSPENDED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


def build_revocation_record(
    *,
    target_id: str,
    target_type: str,
    status: str,
    reason: str,
    revoked_by: str | None = None,
) -> dict[str, Any]:
    """Build a revocation record for proofs, certificates, or issuers."""

    return {
        "revocation_version": REVOCATION_VERSION,
        "target_id": target_id,
        "target_type": target_type,
        "status": status,
        "reason": reason,
        "revoked_by": revoked_by,
    }


def apply_revocation_check(
    verification_result: dict[str, Any],
    revocation_record: dict[str, Any] | None,
) -> dict[str, Any]:
    """Apply revocation state to a verification result."""

    if not revocation_record:
        return {
            "revocation_version": REVOCATION_VERSION,
            "revoked": False,
            "decision": verification_result.get("decision", "UNTRUSTED"),
            "reasons": verification_result.get("reasons", []),
        }

    status = revocation_record.get("status")

    if status == RevocationStatus.REVOKED:
        return {
            "revocation_version": REVOCATION_VERSION,
            "revoked": True,
            "decision": "INVALID",
            "reasons": ["revoked", revocation_record.get("reason")],
        }

    if status in {RevocationStatus.SUSPENDED, RevocationStatus.REVIEW_REQUIRED}:
        return {
            "revocation_version": REVOCATION_VERSION,
            "revoked": False,
            "decision": "REVIEW_REQUIRED",
            "reasons": ["revocation_review_required", revocation_record.get("reason")],
        }

    return {
        "revocation_version": REVOCATION_VERSION,
        "revoked": False,
        "decision": verification_result.get("decision", "UNTRUSTED"),
        "reasons": verification_result.get("reasons", []),
    }


__all__ = [
    "REVOCATION_VERSION",
    "RevocationStatus",
    "build_revocation_record",
    "apply_revocation_check",
]
