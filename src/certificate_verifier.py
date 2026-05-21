"""HC:// certificate verification layer."""

from __future__ import annotations

from typing import Any


CERTIFICATE_VERIFIER_VERSION = "HC-CERTIFICATE-VERIFIER-V1"


def verify_certificate(certificate: dict[str, Any]) -> dict[str, Any]:
    """Verify portable HC:// verification certificate shape and trust signals."""

    reasons: list[str] = []
    risk_flags: list[str] = []

    if not isinstance(certificate, dict):
        return _result(False, ["invalid_certificate_structure"])

    if certificate.get("certificate_version") != "HC-CERTIFICATE-V1":
        reasons.append("unsupported_certificate_version")

    if not certificate.get("issuer"):
        reasons.append("missing_issuer")

    if certificate.get("decision") != "VERIFIED":
        reasons.append("certificate_not_verified")

    if certificate.get("verified") is not True:
        reasons.append("verified_flag_false")

    if certificate.get("risk_flags"):
        risk_flags.extend(certificate.get("risk_flags", []))

    trusted = not reasons and not risk_flags

    return _result(trusted, reasons, risk_flags=risk_flags)


def _result(
    trusted: bool,
    reasons: list[str],
    *,
    risk_flags: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "certificate_verifier_version": CERTIFICATE_VERIFIER_VERSION,
        "trusted": trusted,
        "decision": "VERIFIED" if trusted else "REVIEW_REQUIRED",
        "reasons": sorted(set(reasons)),
        "risk_flags": sorted(set(risk_flags or [])),
    }


__all__ = [
    "CERTIFICATE_VERIFIER_VERSION",
    "verify_certificate",
]
