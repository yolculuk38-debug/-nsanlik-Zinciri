import pytest

from hc_trust.consensus_engine import (
    CONSENSUS_MIXED,
    CONSENSUS_NONE,
    CONSENSUS_STRONG,
    CONSENSUS_WEAK,
    evaluate_consensus,
)


def test_evaluate_consensus_no_witnesses():
    result = evaluate_consensus([])

    assert result["consensus_level"] == CONSENSUS_NONE
    assert result["support_count"] == 0
    assert result["dispute_count"] == 0


def test_evaluate_consensus_weak_support():
    result = evaluate_consensus([
        {"type": "ai", "decision": "support"},
    ])

    assert result["consensus_level"] == CONSENSUS_WEAK
    assert result["support_count"] == 1


def test_evaluate_consensus_strong_multi_type_support():
    result = evaluate_consensus([
        {"type": "ai", "decision": "support"},
        {"type": "human", "decision": "support"},
        {"type": "system", "decision": "support"},
    ])

    assert result["consensus_level"] == CONSENSUS_STRONG
    assert result["support_count"] == 3
    assert result["witness_type_count"] == 3


def test_evaluate_consensus_mixed_support_and_dispute():
    result = evaluate_consensus([
        {"type": "ai", "decision": "support"},
        {"type": "human", "decision": "dispute"},
    ])

    assert result["consensus_level"] == CONSENSUS_MIXED
    assert result["support_count"] == 1
    assert result["dispute_count"] == 1


def test_evaluate_consensus_counts_invalid_witnesses():
    result = evaluate_consensus([
        {"type": "unknown", "decision": "support"},
        {"type": "ai", "decision": "unknown"},
        "not-a-dict",
    ])

    assert result["consensus_level"] == CONSENSUS_NONE
    assert result["invalid_witness_count"] == 3


def test_evaluate_consensus_rejects_non_list_input():
    with pytest.raises(ValueError, match="witnesses must be a list"):
        evaluate_consensus({"type": "ai", "decision": "support"})
