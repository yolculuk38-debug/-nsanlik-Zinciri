from supply_chain_risk import (
    SupplyChainStatus,
    evaluate_supply_chain_artifact,
)


def test_low_risk_artifact():
    result = evaluate_supply_chain_artifact(
        {
            "artifact_id": "pkg-1",
            "artifact_type": "package",
            "source_url": "https://example.org/pkg",
            "version": "1.0.0",
            "signed": True,
            "pinned_version": True,
            "provenance_verified": True,
        }
    )

    assert result["status"] == SupplyChainStatus.LOW_RISK


def test_review_required_artifact():
    result = evaluate_supply_chain_artifact(
        {
            "artifact_id": "ext-1",
            "artifact_type": "extension",
            "source_url": "https://example.org/ext",
            "version": "2.0.0",
            "signed": False,
            "pinned_version": False,
            "provenance_verified": True,
        }
    )

    assert result["status"] == SupplyChainStatus.REVIEW_REQUIRED


def test_high_risk_artifact():
    result = evaluate_supply_chain_artifact(
        {
            "artifact_id": "wf-1",
            "artifact_type": "workflow",
            "source_url": "https://example.org/workflow",
            "version": "3.0.0",
            "signed": False,
            "pinned_version": False,
            "network_access": True,
            "exec_permissions": True,
            "provenance_verified": False,
        }
    )

    assert result["status"] == SupplyChainStatus.HIGH_RISK


def test_invalid_artifact():
    result = evaluate_supply_chain_artifact({})
    assert result["status"] == SupplyChainStatus.INVALID
