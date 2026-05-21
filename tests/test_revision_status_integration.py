from revision_chain import create_revision
from revision_status_integration import verify_revision_status


def test_verified_revision_status():
    rev1 = create_revision(
        "HC-1",
        1,
        "hash-1",
        "2026-05-21T00:00:00Z",
    )

    result = verify_revision_status(
        [rev1],
        base_signals={
            "hash_verified": True,
            "witness_count": 3,
            "trust_score": 90,
        },
    )

    assert result["status_result"]["state"] in {"PARTIAL", "VERIFIED"}


def test_broken_revision_chain_forces_invalid():
    rev1 = create_revision(
        "HC-2",
        1,
        "hash-a",
        "2026-05-21T00:00:00Z",
    )

    rev1["revision_hash"] = "tampered"

    result = verify_revision_status(
        [rev1],
        base_signals={
            "hash_verified": True,
            "witness_count": 5,
            "trust_score": 99,
        },
    )

    assert result["status_result"]["state"] == "INVALID"
