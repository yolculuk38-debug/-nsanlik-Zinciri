from typing import Dict, List


DEFAULT_EVIDENCE_WEIGHTS = {
    "hash": 40,
    "signature": 25,
    "ai_witness": 10,
    "human_witness": 15,
    "system_witness": 5,
    "institution_witness": 15,
}


def calculate_evidence_weight(evidence_items: List[Dict]) -> Dict:
    """Calculate a bounded evidence weight score for HC:// trust evaluation."""

    if evidence_items is None:
        evidence_items = []

    if not isinstance(evidence_items, list):
        raise ValueError("evidence_items must be a list")

    score = 0
    accepted = []
    rejected = []

    for item in evidence_items:
        if not isinstance(item, dict):
            rejected.append("invalid_evidence_shape")
            continue

        evidence_type = str(item.get("type", "")).lower()
        verified = item.get("verified") is True

        if evidence_type not in DEFAULT_EVIDENCE_WEIGHTS:
            rejected.append("unsupported_evidence_type")
            continue

        if not verified:
            rejected.append(f"unverified_{evidence_type}")
            continue

        score += DEFAULT_EVIDENCE_WEIGHTS[evidence_type]
        accepted.append(evidence_type)

    bounded_score = max(0, min(score, 100))

    return {
        "evidence_score": bounded_score,
        "accepted_evidence": accepted,
        "rejected_evidence": rejected,
        "evidence_count": len(accepted),
        "experimental": True,
    }
