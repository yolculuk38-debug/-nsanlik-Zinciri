from revision_chain import (
    GENESIS_REVISION_PARENT,
    RevisionChainStatus,
    create_revision,
    verify_revision_chain,
)


def test_valid_revision_chain():
    rev1 = create_revision(
        "HC-1",
        1,
        "hash-1",
        "2026-05-21T00:00:00Z",
        previous_revision_hash=GENESIS_REVISION_PARENT,
    )

    rev2 = create_revision(
        "HC-1",
        2,
        "hash-2",
        "2026-05-21T00:10:00Z",
        previous_revision_hash=rev1["revision_hash"],
    )

    result = verify_revision_chain([rev1, rev2])

    assert result["status"] == RevisionChainStatus.VERIFIED


def test_broken_revision_chain():
    rev1 = create_revision(
        "HC-2",
        1,
        "hash-a",
        "2026-05-21T00:00:00Z",
    )

    rev2 = create_revision(
        "HC-2",
        2,
        "hash-b",
        "2026-05-21T00:10:00Z",
        previous_revision_hash="tampered-parent",
    )

    result = verify_revision_chain([rev1, rev2])

    assert result["status"] == RevisionChainStatus.BROKEN


def test_invalid_empty_chain():
    result = verify_revision_chain([])

    assert result["status"] == RevisionChainStatus.INVALID
