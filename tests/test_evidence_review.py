from evidence_review import (
    EvidenceStatus,
    create_evidence,
    review_evidence,
)


def valid_evidence():
    return create_evidence(
        "evidence-1",
        "news_article",
        "https://example.org/article",
        "2026-05-21T00:00:00Z",
        metadata={"title": "Example"},
    )


def test_verified_evidence():
    result = review_evidence(valid_evidence())
    assert result["status"] == EvidenceStatus.VERIFIED


def test_review_required_for_media():
    evidence = create_evidence(
        "evidence-2",
        "image",
        "https://example.org/image.png",
        "2026-05-21T00:00:00Z",
        metadata={"camera": "device"},
    )

    result = review_evidence(evidence)
    assert result["status"] == EvidenceStatus.REVIEW_REQUIRED


def test_invalid_hash_detection():
    evidence = valid_evidence()
    evidence["source_url"] = "https://tampered.example"

    result = review_evidence(evidence)
    assert result["status"] == EvidenceStatus.INVALID


def test_unsafe_protocol():
    evidence = create_evidence(
        "evidence-3",
        "document",
        "http://unsafe.local/doc",
        "2026-05-21T00:00:00Z",
    )

    result = review_evidence(evidence)
    assert result["status"] == EvidenceStatus.UNSAFE
