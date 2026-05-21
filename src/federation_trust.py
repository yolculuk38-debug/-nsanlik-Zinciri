"""HC:// federation trust layer."""

from __future__ import annotations

from typing import Any


FEDERATION_TRUST_VERSION = "HC-FEDERATION-TRUST-V1"


class FederationStatus:
    TRUSTED = "TRUSTED"
    LIMITED = "LIMITED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    SUSPENDED = "SUSPENDED"
    REVOKED = "REVOKED"
    UNKNOWN = "UNKNOWN"


def build_federation_profile(
    *,
    federation_id: str,
    status: str = FederationStatus.UNKNOWN,
    trust_weight: int = 0,
    capabilities: list[str] | None = None,
    risk_flags: list[str] | None = None,
) -> dict[str, Any]:
    """Build a federation trust profile."""

    return {
        "federation_trust_version": FEDERATION_TRUST_VERSION,
        "federation_id": federation_id,
        "status": status,
        "trust_weight": int(trust_weight),
        "capabilities": sorted(set(capabilities or [])),
        "risk_flags": sorted(set(risk_flags or [])),
    }


def evaluate_federation_profile(profile: dict[str, Any]) -> dict[str, Any]:
    """Evaluate federation trust state."""

    if not isinstance(profile, dict):
        return _result(False, "INVALID", 0, ["invalid_federation_profile"])

    status = profile.get("status", FederationStatus.UNKNOWN)
    weight = int(profile.get("trust_weight", 0) or 0)
    risk_flags = list(profile.get("risk_flags", []) or [])

    if status == FederationStatus.REVOKED:
        return _result(False, "INVALID", 0, risk_flags + ["federation_revoked"])

    if status == FederationStatus.SUSPENDED:
        return _result(False, "REVIEW_REQUIRED", 0, risk_flags + ["federation_suspended"])

    if risk_flags:
        return _result(False, "REVIEW_REQUIRED", weight, risk_flags)

    if status == FederationStatus.TRUSTED and weight >= 70:
        return _result(True, "TRUSTED", weight, [])

    if status == FederationStatus.LIMITED and weight >= 40:
        return _result(False, "LIMITED", weight, [])

    return _result(False, "REVIEW_REQUIRED", weight, ["federation_review_required"])


def _result(trusted: bool, decision: str, trust_weight: int, reasons: list[str]) -> dict[str, Any]:
    return {
        "federation_trust_version": FEDERATION_TRUST_VERSION,
        "trusted": trusted,
        "decision": decision,
        "trust_weight": trust_weight,
        "reasons": sorted(set(reasons)),
    }


__all__ = [
    "FEDERATION_TRUST_VERSION",
    "FederationStatus",
    "build_federation_profile",
    "evaluate_federation_profile",
]
