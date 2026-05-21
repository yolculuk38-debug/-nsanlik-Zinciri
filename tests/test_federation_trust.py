from federation_trust import (
    FederationStatus,
    build_federation_profile,
    evaluate_federation_profile,
)


def test_trusted_federation():
    profile = build_federation_profile(
        federation_id="fed-1",
        status=FederationStatus.TRUSTED,
        trust_weight=90,
    )

    result = evaluate_federation_profile(profile)

    assert result["trusted"] is True


def test_suspended_federation():
    profile = build_federation_profile(
        federation_id="fed-2",
        status=FederationStatus.SUSPENDED,
        trust_weight=80,
    )

    result = evaluate_federation_profile(profile)

    assert result["decision"] == "REVIEW_REQUIRED"
