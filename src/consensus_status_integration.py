"""HC:// consensus to verification status integration."""

from __future__ import annotations

from typing import Any

from consensus_rules import ConsensusStatus
from verification_status_engine import determine_verification_status


INTEGRATION_VERSION = "HC-CONSENSUS-STATUS-INTEGRATION-V1"


def consensus_to_status(
    consensus_result: dict[str, Any],
    *,
    base_signals: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Map consensus result into centralized verification status signals."""

    signals = dict(base_signals or {})
    risk_flags = list(signals.get("risk_flags", []) or [])

    status = consensus_result.get("status") if isinstance(consensus_result, dict) else None
    witness_count = int(consensus_result.get("witness_count", 0) or 0) if isinstance(consensus_result, dict) else 0

    signals["witness_count"] = max(int(signals.get("witness_count", 0) or 0), witness_count)

    if status == ConsensusStatus.CONSENSUS_REACHED.value:
        signals.setdefault("hash_verified", True)
        signals.setdefault("trust_score", 85)
    elif status == ConsensusStatus.PARTIAL_CONSENSUS.value:
        signals.setdefault("hash_verified", True)
        signals.setdefault("trust_score", 60)
        risk_flags.append("partial_consensus")
    elif status == ConsensusStatus.CONFLICT.value:
        signals["invalid"] = True
        risk_flags.append("consensus_conflict")
    elif status == ConsensusStatus.INSUFFICIENT_WITNESSES.value:
        signals.setdefault("hash_verified", True)
        risk_flags.append("insufficient_witnesses")
    else:
        signals["invalid"] = True
        risk_flags.append("invalid_consensus_result")

    signals["risk_flags"] = risk_flags
    status_result = determine_verification_status(signals)

    return {
        "integration_version": INTEGRATION_VERSION,
        "consensus_result": consensus_result,
        "status_result": status_result,
    }


__all__ = ["INTEGRATION_VERSION", "consensus_to_status"]
