from trust_registry import (
    RegistryStatus,
    build_registry_entry,
    evaluate_registry_entry,
)


def test_trusted_registry_entry():
    entry = build_registry_entry(
        entity_id="issuer-1",
        entity_type="ISSUER",
        status=RegistryStatus.TRUSTED,
        trust_score=90,
    )

    result = evaluate_registry_entry(entry)

    assert result["trusted"] is True


def test_revoked_registry_entry():
    entry = build_registry_entry(
        entity_id="issuer-2",
        entity_type="ISSUER",
        status=RegistryStatus.REVOKED,
    )

    result = evaluate_registry_entry(entry)

    assert result["decision"] == "INVALID"
