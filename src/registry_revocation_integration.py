"""HC:// registry and revocation integration."""

from __future__ import annotations

from typing import Any

from trust_registry import RegistryStatus, evaluate_registry_entry
from revocation import apply_revocation_check


REGISTRY_REVOCATION_VERSION = "HC-REGISTRY-REVOCATION-V1"


def apply_registry_revocation_policy(
    verification_result: dict[str, Any],
    registry_entry: dict[str, Any] | None,
    revocation_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Apply registry and revocation policy to verification output."""

    revocation_result = apply_revocation_check(verification_result, revocation_record)

    if revocation_result.get("decision") == "INVALID":
        return _result("INVALID", False, revocation_result.get("reasons", []))

    if not registry_entry:
        return _result(
            "REVIEW_REQUIRED",
            False,
            ["missing_registry_entry"],
        )

    registry_result = evaluate_registry_entry(registry_entry)

    if registry_result.get("decision") == "INVALID":
        return _result("INVALID", False, registry_result.get("reasons", []))

    if registry_result.get("decision") == RegistryStatus.REVIEW_REQUIRED:
        return _result("REVIEW_REQUIRED", False, registry_result.get("reasons", []))

    return _result(
        verification_result.get("decision", "UNTRUSTED"),
        bool(verification_result.get("verified", False)) and bool(registry_result.get("trusted", False)),
        verification_result.get("reasons", []),
    )


def _result(decision: str, trusted: bool, reasons: list[str]) -> dict[str, Any]:
    return {
        "registry_revocation_version": REGISTRY_REVOCATION_VERSION,
        "decision": decision,
        "trusted": trusted,
        "reasons": sorted(set(reasons)),
    }


__all__ = [
    "REGISTRY_REVOCATION_VERSION",
    "apply_registry_revocation_policy",
]
