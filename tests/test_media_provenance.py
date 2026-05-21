from media_provenance import (
    MediaProvenanceStatus,
    create_media_provenance,
    scan_media_provenance,
)


def valid_record():
    return create_media_provenance(
        "media-1",
        "image",
        "hash123",
        "2026-05-21T00:00:00Z",
        metadata={"camera": "device"},
    )


def test_provenance_ready():
    result = scan_media_provenance(valid_record())
    assert result["status"] == MediaProvenanceStatus.PROVENANCE_READY


def test_review_required_for_ai_generated():
    record = create_media_provenance(
        "media-2",
        "video",
        "hash456",
        "2026-05-21T00:00:00Z",
        metadata={"ai_generated": True},
    )

    result = scan_media_provenance(record)
    assert result["status"] == MediaProvenanceStatus.REVIEW_REQUIRED


def test_hash_mismatch_detection():
    record = valid_record()
    record["file_hash"] = "tampered"

    result = scan_media_provenance(record)
    assert result["status"] == MediaProvenanceStatus.HASH_MISMATCH


def test_review_required_for_derived_chain():
    record = create_media_provenance(
        "media-3",
        "image",
        "hash789",
        "2026-05-21T00:00:00Z",
        metadata={"edited": True},
        parent_media_hash="parent-hash",
    )

    result = scan_media_provenance(record)
    assert result["status"] == MediaProvenanceStatus.REVIEW_REQUIRED
