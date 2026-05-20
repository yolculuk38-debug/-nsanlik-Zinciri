from typing import Dict, List


CONSENSUS_NONE = "NO_CONSENSUS"
CONSENSUS_WEAK = "WEAK_CONSENSUS"
CONSENSUS_MIXED = "MIXED_CONSENSUS"
CONSENSUS_STRONG = "STRONG_CONSENSUS"


def evaluate_consensus(witnesses: List[Dict]) -> Dict:
    """Evaluate multi-witness consensus strength for HC:// records."""

    if witnesses is None:
        witnesses = []

    if not isinstance(witnesses, list):
        raise ValueError("witnesses must be a list")

    valid_support = []
    valid_dispute = []
    invalid_count = 0
    witness_types = set()

    for witness in witnesses:
        if not isinstance(witness, dict):
            invalid_count += 1
            continue

        witness_type = str(witness.get("type", "")).lower()
        decision = str(witness.get("decision", "")).lower()

        if witness_type not in {"ai", "human", "system", "institution"}:
            invalid_count += 1
            continue

        if decision == "support":
            valid_support.append(witness)
            witness_types.add(witness_type)
        elif decision == "dispute":
            valid_dispute.append(witness)
            witness_types.add(witness_type)
        else:
            invalid_count += 1

    support_count = len(valid_support)
    dispute_count = len(valid_dispute)
    total_decisive = support_count + dispute_count

    if total_decisive == 0:
        level = CONSENSUS_NONE
    elif dispute_count > 0 and support_count > 0:
        level = CONSENSUS_MIXED
    elif support_count >= 3 and len(witness_types) >= 2:
        level = CONSENSUS_STRONG
    elif support_count >= 1:
        level = CONSENSUS_WEAK
    else:
        level = CONSENSUS_NONE

    return {
        "consensus_level": level,
        "support_count": support_count,
        "dispute_count": dispute_count,
        "witness_type_count": len(witness_types),
        "invalid_witness_count": invalid_count,
        "experimental": True,
    }
