from registry_revocation_integration import apply_registry_revocation_policy
from trust_registry import RegistryStatus, build_registry_entry


def test_registry_trusted_result():
    registry_entry = build_registry_entry(
        entity_id="issuer-1",
        entity_type="ISSUER",
        status=RegistryStatus.TRUSTED,
        trust_score=95,
    )

    result = apply_registry_revocation_policy(
        {
            "decision": "VERIFIED",
            "verified": True,
            "reasons": [],
        },
        registry_entry,
    )

    assert result["trusted"] is True


def test_missing_registry_entry():
    result = apply_registry_revocation_policy(
        {
            "decision": "VERIFIED",
            "verified": True,
            "reasons": [],
        },
        None,
    )

    assert result["decision"] == "REVIEW_REQUIRED"
