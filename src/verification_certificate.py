"""HC:// verification certificate layer."""

from __future__ import annotations

from typing import Any


CERTIFICATE_VERSION = "HC-CERTIFICATE-V1"


def build_verification_certificate(
    sdk_response: dict[str, Any],
    *,
    issuer: str = "HC://",
) -> dict[str, Any]:
    """Build portable verification certificate."""

    return {
        "certificate_version": CERTIFICATE_VERSION,
        "issuer": issuer,
        "decision": sdk_response.get("decision"),
        "verified": sdk_response.get("verified", False),
        "verification_level": sdk_response.get("verification_level"),
        "risk_flags": sdk_response.get("risk_flags", []),
        "reasons": sdk_response.get("reasons", []),
        "portable": True,
        "explainable": True,
        "human_readable": True,
    }


__all__ = [
    "CERTIFICATE_VERSION",
    "build_verification_certificate",
]
