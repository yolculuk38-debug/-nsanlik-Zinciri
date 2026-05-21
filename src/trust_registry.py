"""HC:// trust registry foundation."""

from __future__ import annotations

from typing import Any


TRUST_REGISTRY_VERSION = "HC-TRUST-REGISTRY-V1"


class RegistryStatus:
    TRUSTED = "TRUSTED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    SUSPENDED = "SUSPENDED"
    REVOKED = "REVOKED"
    UNKNOWN = "UNKNOWN"


def build_registry_entry(
    *,
    entity_id: str,
    entity_type: str,
    status: str = RegistryStatus.UNKNOWN,
    trust_score: int = 0,
    reasons: list[str] | None = None,
) -> dict[str, Any]:
    """Build a registry entry for issuer, witness, or federation entities."""

    return {
        "trust_registry_version": TRUST_REGISTRY_VERSION,
        "entity_id": entity_id,
        "entity_type": entity_type,
        "status": status,
        "trust_score": int(trust_score),
        "reasons": sorted(set(reasons or [])),
    }


def evaluate_registry_entry(entry: dict[str, Any]) -> dict[str, Any]:
    """Evaluate registry trust state."""

    if not isinstance(entry, dict):
        return {
            "trust_registry_version": TRUST_REGISTRY_VERSION,
            "trusted": False,
            "decision": RegistryStatus.REVIEW_REQUIRED,
            "reasons": ["invalid_registry_entry"],
        }

    status = entry.get("status", RegistryStatus.UNKNOWN)
    trust_score = int(entry.get("trust_score", 0) or 0)
    reasons = list(entry.get("reasons", []) or [])

    if status == RegistryStatus.REVOKED:
        return _result(False, "INVALID", reasons + ["registry_entity_revoked"])

    if status == RegistryStatus.SUSPENDED:
        return _result(False, RegistryStatus.REVIEW_REQUIRED, reasons + ["registry_entity_suspended"])

    if status == RegistryStatus.TRUSTED and trust_score >= 70:
        return _result(True, RegistryStatus.TRUSTED, reasons)

    return _result(False, RegistryStatus.REVIEW_REQUIRED, reasons + ["registry_review_required"])


def _result(trusted: bool, decision: str, reasons: list[str]) -> dict[str, Any]:
    return {
        "trust_registry_version": TRUST_REGISTRY_VERSION,
        "trusted": trusted,
        "decision": decision,
        "reasons": sorted(set(reasons)),
    }


__all__ = [
    "TRUST_REGISTRY_VERSION",
    "RegistryStatus",
    "build_registry_entry",
    "evaluate_registry_entry",
]
