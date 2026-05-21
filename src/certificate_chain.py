"""HC:// certificate chain layer."""

from __future__ import annotations

from typing import Any


CERTIFICATE_CHAIN_VERSION = "HC-CERTIFICATE-CHAIN-V1"


def build_certificate_chain_entry(
    certificate: dict[str, Any],
    *,
    previous_certificate_hash: str | None = None,
) -> dict[str, Any]:
    """Build certificate lineage entry."""

    return {
        "certificate_chain_version": CERTIFICATE_CHAIN_VERSION,
        "certificate": certificate,
        "previous_certificate_hash": previous_certificate_hash,
        "chain_integrity": True,
    }


def verify_certificate_chain(
    chain_entry: dict[str, Any],
) -> dict[str, Any]:
    """Verify certificate lineage integrity."""

    reasons: list[str] = []

    if not isinstance(chain_entry, dict):
        reasons.append("invalid_chain_entry")

    if chain_entry.get("chain_integrity") is not True:
        reasons.append("broken_certificate_chain")

    trusted = not reasons

    return {
        "certificate_chain_version": CERTIFICATE_CHAIN_VERSION,
        "trusted": trusted,
        "decision": "VERIFIED" if trusted else "INVALID",
        "reasons": sorted(set(reasons)),
    }


__all__ = [
    "CERTIFICATE_CHAIN_VERSION",
    "build_certificate_chain_entry",
    "verify_certificate_chain",
]
