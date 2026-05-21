"""HC:// multi-witness consensus rules.

Consensus is not automatic truth. It is a structured verification signal
computed from independent witness results.
"""

from __future__ import annotations

from collections import Counter
from enum import Enum
from typing import Any


class ConsensusStatus(str, Enum):
    CONSENSUS_REACHED = "CONSENSUS_REACHED"
    PARTIAL_CONSENSUS = "PARTIAL_CONSENSUS"
    CONFLICT = "CONFLICT"
    INSUFFICIENT_WITNESSES = "INSUFFICIENT_WITNESSES"
    INVALID_INPUT = "INVALID_INPUT"


VALID_VERDICTS = {"PASS", "FAIL", "ABSTAIN"}
DEFAULT_MIN_WITNESSES = 3
DEFAULT_THRESHOLD = 0.67


def _normalize_witness(witness: dict[str, Any]) -> dict[str, Any] | None:
    witness_id = witness.get("witness_id") or witness.get("id")
    witness_type = witness.get("witness_type") or witness.get("type") or "unknown"
    verdict = str(witness.get("verdict", "")).upper()
    content_hash = witness.get("content_hash")

    if not witness_id or verdict not in VALID_VERDICTS:
        return None

    return {
        "witness_id": str(witness_id),
        "witness_type": str(witness_type),
        "verdict": verdict,
        "content_hash": content_hash,
    }


def evaluate_consensus(
    witnesses: list[dict[str, Any]],
    *,
    min_witnesses: int = DEFAULT_MIN_WITNESSES,
    threshold: float = DEFAULT_THRESHOLD,
) -> dict[str, Any]:
    """Evaluate witness consensus for a record.

    Rules:
    - Duplicate witness IDs are ignored after first valid entry.
    - ABSTAIN does not count toward PASS/FAIL agreement.
    - Conflicting content hashes reduce consensus confidence.
    - Consensus requires minimum witnesses and threshold agreement.
    """

    if not isinstance(witnesses, list):
        return {"status": ConsensusStatus.INVALID_INPUT.value, "trusted": False, "reason": "witnesses must be a list"}
    if min_witnesses < 1 or not (0 < threshold <= 1):
        return {"status": ConsensusStatus.INVALID_INPUT.value, "trusted": False, "reason": "invalid consensus parameters"}

    normalized: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for witness in witnesses:
        if not isinstance(witness, dict):
            continue
        item = _normalize_witness(witness)
        if item is None or item["witness_id"] in seen_ids:
            continue
        seen_ids.add(item["witness_id"])
        normalized.append(item)

    if len(normalized) < min_witnesses:
        return {
            "status": ConsensusStatus.INSUFFICIENT_WITNESSES.value,
            "trusted": False,
            "witness_count": len(normalized),
            "required_witnesses": min_witnesses,
            "reason": "not enough independent valid witnesses",
        }

    active = [w for w in normalized if w["verdict"] != "ABSTAIN"]
    if not active:
        return {"status": ConsensusStatus.CONFLICT.value, "trusted": False, "reason": "all witnesses abstained"}

    verdict_counts = Counter(w["verdict"] for w in active)
    top_verdict, top_count = verdict_counts.most_common(1)[0]
    agreement_ratio = top_count / len(active)

    hashes = {w["content_hash"] for w in active if w.get("content_hash")}
    hash_conflict = len(hashes) > 1

    result = {
        "trusted": False,
        "witness_count": len(normalized),
        "active_witness_count": len(active),
        "top_verdict": top_verdict,
        "agreement_ratio": round(agreement_ratio, 4),
        "threshold": threshold,
        "hash_conflict": hash_conflict,
        "verdict_counts": dict(verdict_counts),
    }

    if hash_conflict:
        result.update({"status": ConsensusStatus.CONFLICT.value, "reason": "witnesses disagree on content_hash"})
        return result

    if top_verdict == "PASS" and agreement_ratio >= threshold:
        result.update({"status": ConsensusStatus.CONSENSUS_REACHED.value, "trusted": True, "reason": "PASS consensus reached"})
        return result

    if agreement_ratio >= threshold:
        result.update({"status": ConsensusStatus.CONFLICT.value, "reason": f"{top_verdict} consensus reached"})
        return result

    result.update({"status": ConsensusStatus.PARTIAL_CONSENSUS.value, "reason": "agreement below threshold"})
    return result


__all__ = ["ConsensusStatus", "evaluate_consensus"]
