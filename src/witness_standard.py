"""HC:// expanded witness standard."""

from __future__ import annotations

from typing import Any

WITNESS_STANDARD_VERSION = "HC-WITNESS-STANDARD-V1"
VALID_WITNESS_TYPES = {"AI", "HUMAN", "SYSTEM", "FEDERATION"}
VALID_VERDICTS = {"PASS", "FAIL", "ABSTAIN", "REVIEW_REQUIRED"}


class WitnessStandardStatus:
    VALID = "VALID"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    INVALID = "INVALID"


def create_witness_record(
    witness_id: str,
    witness_type: str,
    verdict: str,
    checked_at: str,
    *,
    verification_method: str,
    confidence_score: int,
    provenance_reference: str | None = None,
    model_name: str | None = None,
    model_version: str | None = None,
    reviewer_id: str | None = None,
    witness_signature: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "witness_standard_version": WITNESS_STANDARD_VERSION,
        "witness_id": witness_id,
        "witness_type": witness_type.upper(),
        "verdict": verdict.upper(),
        "checked_at": checked_at,
        "verification_method": verification_method,
        "confidence_score": max(0, min(100, int(confidence_score))),
        "provenance_reference": provenance_reference,
        "model_name": model_name,
        "model_version": model_version,
        "reviewer_id": reviewer_id,
        "witness_signature": witness_signature,
        "metadata": metadata or {},
    }


def validate_witness_record(record: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(record, dict):
        return {"status": WitnessStandardStatus.INVALID, "valid": False, "reason": "bad object"}

    required = {
        "witness_standard_version",
        "witness_id",
        "witness_type",
        "verdict",
        "checked_at",
        "verification_method",
        "confidence_score",
    }
    if required.difference(record):
        return {"status": WitnessStandardStatus.INVALID, "valid": False, "reason": "missing fields"}

    if record["witness_standard_version"] != WITNESS_STANDARD_VERSION:
        return {"status": WitnessStandardStatus.INVALID, "valid": False, "reason": "bad version"}

    if record["witness_type"] not in VALID_WITNESS_TYPES:
        return {"status": WitnessStandardStatus.INVALID, "valid": False, "reason": "bad type"}

    if record["verdict"] not in VALID_VERDICTS:
        return {"status": WitnessStandardStatus.INVALID, "valid": False, "reason": "bad verdict"}

    flags = []
    if record["witness_type"] == "AI" and not record.get("model_name"):
        flags.append("missing_model_name")
    if record["witness_type"] == "HUMAN" and not record.get("reviewer_id"):
        flags.append("missing_reviewer_id")
    if not record.get("witness_signature"):
        flags.append("unsigned_witness")
    if not record.get("provenance_reference"):
        flags.append("missing_provenance_reference")

    if flags:
        return {"status": WitnessStandardStatus.REVIEW_REQUIRED, "valid": True, "review_flags": flags}

    return {"status": WitnessStandardStatus.VALID, "valid": True, "reason": "valid"}


__all__ = [
    "WITNESS_STANDARD_VERSION",
    "VALID_WITNESS_TYPES",
    "VALID_VERDICTS",
    "WitnessStandardStatus",
    "create_witness_record",
    "validate_witness_record",
]
