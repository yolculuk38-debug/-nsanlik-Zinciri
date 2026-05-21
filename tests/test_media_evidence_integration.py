from media_evidence_integration import integrate_media_with_evidence_review
from media_provenance import create_media_provenance


def valid_media_record():
    return create_media_provenance(
        "media-1",
        "image",
        "hash123",
        "2026-05-21T00:00:00Z",
        metadata={"camera": "device"},
    )


def test_media_converted_to_reviewable_evidence():
    result = integrate_media_with_evidence_review(
        valid_media_record(),
        source_url="https://example.org/image.png",
        collected_at="2026-05-21T00:00:00Z",
    )

    assert result["linked"] is True
    assert result["evidence_review"]["reviewable"] is True


def test_invalid_media_not_linked():
    media = valid_media_record()
    media["file_hash"] = "tampered"

    result = integrate_media_with_evidence_review(
        media,
        source_url="https://example.org/image.png",
        collected_at="2026-05-21T00:00:00Z",
    )

    assert result["linked"] is False


def test_ai_generated_media_requires_review():
    media = create_media_provenance(
        "media-2",
        "video",
        "hash456",
        "2026-05-21T00:00:00Z",
        metadata={"ai_generated": True},
    )

    result = integrate_media_with_evidence_review(
        media,
        source_url="https://example.org/video.mp4",
        collected_at="2026-05-21T00:00:00Z",
    )

    assert result["linked"] is True
    assert result["media_scan"]["status"] == "REVIEW_REQUIRED"
