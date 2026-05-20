import pytest

from hc_trust.score_normalizer import normalize_trust_score


def test_normalize_trust_score_keeps_clean_score():
    result = normalize_trust_score(80)

    assert result["normalized_score"] == 80
    assert result["adjustments"] == []


def test_normalize_trust_score_applies_high_risk_penalty():
    result = normalize_trust_score(
        90,
        risk_flags={"high_risk": True, "risk_flag_count": 1},
    )

    assert result["normalized_score"] == 50
    assert "high_risk_penalty" in result["adjustments"]
    assert "risk_flag_penalty" in result["adjustments"]


def test_normalize_trust_score_applies_witness_bonuses():
    result = normalize_trust_score(
        70,
        witness_summary={"has_independent_mix": True, "witness_count": 3},
    )

    assert result["normalized_score"] == 85
    assert "independent_witness_bonus" in result["adjustments"]
    assert "witness_count_bonus" in result["adjustments"]


def test_normalize_trust_score_clamps_to_range():
    assert normalize_trust_score(150)["normalized_score"] == 100
    assert normalize_trust_score(-10)["normalized_score"] == 0


def test_normalize_trust_score_rejects_non_integer_score():
    with pytest.raises(ValueError, match="base_score must be an integer"):
        normalize_trust_score("90")
