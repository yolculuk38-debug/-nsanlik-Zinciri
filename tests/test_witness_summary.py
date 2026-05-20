import pytest

from hc_trust.witness_summary import build_witness_summary


def test_build_witness_summary_empty_list():
    summary = build_witness_summary([])

    assert summary["witness_count"] == 0
    assert summary["invalid_witness_count"] == 0
    assert summary["has_human_witness"] is False
    assert summary["has_ai_witness"] is False
    assert summary["has_independent_mix"] is False


def test_build_witness_summary_ai_human_mix():
    summary = build_witness_summary(
        [
            {"id": "ai-1", "type": "ai"},
            {"id": "human-1", "type": "human"},
            {"id": "system-1", "type": "system"},
        ]
    )

    assert summary["witness_count"] == 3
    assert summary["witness_types"]["ai"] == 1
    assert summary["witness_types"]["human"] == 1
    assert summary["witness_types"]["system"] == 1
    assert summary["has_independent_mix"] is True


def test_build_witness_summary_counts_invalid_witnesses():
    summary = build_witness_summary(
        [
            {"id": "ai-1", "type": "ai"},
            {"id": "unknown-1", "type": "unknown"},
            "not-a-dict",
        ]
    )

    assert summary["witness_count"] == 1
    assert summary["invalid_witness_count"] == 2


def test_build_witness_summary_rejects_non_list_input():
    with pytest.raises(ValueError, match="witnesses must be a list"):
        build_witness_summary({"id": "ai-1", "type": "ai"})
