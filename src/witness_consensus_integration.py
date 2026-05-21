"""HC:// witness standard to consensus integration."""

from __future__ import annotations

from typing import Any

from consensus_rules import evaluate_consensus
from witness_standard import WitnessStandardStatus, validate_witness_record


INTEGRATION_VERSION = "HC-WITNESS-CONSENSUS-INTEGRATION-V1"


def witness_to_consensus_item(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "witness_id": record.get("witness_id"),
        "witness_type": record.get("witness_type"),
        "verdict": record.get("verdict"),
        "content_hash": record.get("provenance_reference"),
        "confidence_score": record.get("confidence_score"),
    }


def evaluate_witness_consensus(
    witness_records: list[dict[str, Any]],
    *,
    min_witnesses: int = 3,
    threshold: float = 0.67,
) -> dict[str, Any]:
    """Validate expanded witness records and evaluate consensus."""

    valid_items = []
    validation_results = []

    for record in witness_records:
        validation = validate_witness_record(record)
        validation_results.append({
            "witness_id": record.get("witness_id") if isinstance(record, dict) else None,
            "validation": validation,
        })

        if validation.get("status") in {WitnessStandardStatus.VALID, WitnessStandardStatus.REVIEW_REQUIRED} and validation.get("valid"):
            valid_items.append(witness_to_consensus_item(record))

    consensus = evaluate_consensus(
        valid_items,
        min_witnesses=min_witnesses,
        threshold=threshold,
    )

    return {
        "integration_version": INTEGRATION_VERSION,
        "valid_witness_count": len(valid_items),
        "total_witness_count": len(witness_records),
        "validation_results": validation_results,
        "consensus": consensus,
    }


__all__ = ["INTEGRATION_VERSION", "witness_to_consensus_item", "evaluate_witness_consensus"]
