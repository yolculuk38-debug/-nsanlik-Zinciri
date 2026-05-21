from social_media_bridge import (
    SocialBridgeStatus,
    create_social_reference,
    normalize_social_reference,
)


def valid_reference():
    return create_social_reference(
        "ref-1",
        "x",
        "https://x.com/example/status/1",
        "2026-05-21T00:00:00Z",
        author_handle="example",
        post_id="1",
    )


def test_normalized_reference():
    result = normalize_social_reference(valid_reference())
    assert result["status"] == SocialBridgeStatus.NORMALIZED


def test_review_required_for_missing_metadata():
    reference = create_social_reference(
        "ref-2",
        "x",
        "https://x.com/example/status/2",
        "2026-05-21T00:00:00Z",
    )

    result = normalize_social_reference(reference)
    assert result["status"] == SocialBridgeStatus.REVIEW_REQUIRED


def test_invalid_hash_detection():
    reference = valid_reference()
    reference["post_url"] = "https://tampered.example"

    result = normalize_social_reference(reference)
    assert result["status"] == SocialBridgeStatus.INVALID


def test_unsafe_url_detection():
    reference = create_social_reference(
        "ref-3",
        "reddit",
        "http://unsafe.local/post",
        "2026-05-21T00:00:00Z",
    )

    result = normalize_social_reference(reference)
    assert result["status"] == SocialBridgeStatus.UNSAFE
