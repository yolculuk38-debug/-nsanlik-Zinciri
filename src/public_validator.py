"""HC:// public validator core.

Portable proof validation layer for exported HC:// verification records.
"""

from __future__ import annotations

from typing import Any


VALIDATOR_VERSION = "HC-PUBLIC-VALIDATOR-V1"


class PublicValidatorDecision:
    VERIFIED = "VERIFIED"
    PARTIAL = "PARTIAL"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    INVALID = "INVALID"
    UNTRUSTED = "UNTRUSTED"


def validate_public_proof(proof: dict[str, Any]) -> dict[str, Any]:
    """Validate exported HC:// proof structures."""

    reasons: list[str] = []
    risk_flags: list[str] = []

    if not isinstance(proof, dict):
        return _response(PublicValidatorDecision.INVALID, ["invalid proof structure"])

    required_fields = [
        "record_id",
        "content_hash",
        "verification_level",
        "trust_passport",
    ]

    for field in required_fields:
        if not proof.get(field):
            reasons.append(f"missing_{field}")

    revision_chain = proof.get("revision_chain", {})
    if revision_chain.get("broken"):
        reasons.append("broken_revision_chain")

    if not proof.get("content_hash_valid", False):
        reasons.append("invalid_content_hash")

    witnesses = proof.get("witnesses", []) or []

    valid_witnesses = 0
    conflicting_witnesses = 0

    for witness in witnesses:
        if not isinstance(witness, dict):
            continue

        if witness.get("conflict"):
            conflicting_witnesses += 1

        if not witness.get("witness_signature"):
            risk_flags.append("missing_witness_signature")
            continue

        if not witness.get("provenance_reference"):
            risk_flags.append("missing_provenance_reference")
            continue

        valid_witnesses += 1

    if conflicting_witnesses:
        reasons.append("conflicting_witnesses")

    verification_level = proof.get("verification_level")

    if reasons:
        decision = PublicValidatorDecision.INVALID
    elif risk_flags:
        decision = PublicValidatorDecision.REVIEW_REQUIRED
    elif valid_witnesses >= 2 and verification_level:
        decision = PublicValidatorDecision.VERIFIED
    elif valid_witnesses == 1:
        decision = PublicValidatorDecision.PARTIAL
    else:
        decision = PublicValidatorDecision.UNTRUSTED

    return _response(
        decision,
        reasons,
        risk_flags=risk_flags,
        verification_level=verification_level,
        record_id=proof.get("record_id"),
    )


def _response(
    decision: str,
    reasons: list[str],
    *,
    risk_flags: list[str] | None = None,
    verification_level: str | None = None,
    record_id: str | None = None,
) -> dict[str, Any]:
    return {
        "validator_version": VALIDATOR_VERSION,
        "record_id": record_id,
        "decision": decision,
        "verified": decision == PublicValidatorDecision.VERIFIED,
        "verification_level": verification_level,
        "reasons": sorted(set(reasons)),
        "risk_flags": sorted(set(risk_flags or [])),
    }


__all__ = [
    "VALIDATOR_VERSION",
    "PublicValidatorDecision",
    "validate_public_proof",
]
