from typing import Dict


MIN_SCORE = 0
MAX_SCORE = 100


def normalize_trust_score(
    base_score: int,
    *,
    risk_flags: Dict | None = None,
    witness_summary: Dict | None = None,
) -> Dict:
    """Normalize a trust score using risk flags and witness summary signals."""

    if not isinstance(base_score, int):
        raise ValueError("base_score must be an integer")

    score = max(MIN_SCORE, min(base_score, MAX_SCORE))
    adjustments = []

    risk_flags = risk_flags or {}
    witness_summary = witness_summary or {}

    if risk_flags.get("high_risk") is True:
        score -= 35
        adjustments.append("high_risk_penalty")

    risk_flag_count = int(risk_flags.get("risk_flag_count", 0))
    if risk_flag_count > 0:
        penalty = min(risk_flag_count * 5, 20)
        score -= penalty
        adjustments.append("risk_flag_penalty")

    if witness_summary.get("has_independent_mix") is True:
        score += 10
        adjustments.append("independent_witness_bonus")

    witness_count = int(witness_summary.get("witness_count", 0))
    if witness_count >= 3:
        score += 5
        adjustments.append("witness_count_bonus")

    score = max(MIN_SCORE, min(score, MAX_SCORE))

    return {
        "normalized_score": score,
        "adjustments": adjustments,
        "experimental": True,
    }
