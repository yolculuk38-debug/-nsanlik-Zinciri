from evidence_review import create_evidence
from evidence_trust_graph_integration import integrate_evidence_with_trust_graph


def test_integrates_verified_evidence_into_graph():
    evidence = create_evidence(
        "evidence-1",
        "news_article",
        "https://example.org/article",
        "2026-05-21T00:00:00Z",
        metadata={"title": "Example"},
    )

    result = integrate_evidence_with_trust_graph(
        "graph-1",
        [evidence],
        target_id="record-1",
        observed_at="2026-05-21T00:00:00Z",
    )

    assert result["linked_evidence_count"] == 1
    assert result["graph_validation"]["status"] == "VALID"


def test_invalid_evidence_not_linked():
    evidence = create_evidence(
        "evidence-2",
        "document",
        "https://example.org/doc",
        "2026-05-21T00:00:00Z",
        metadata={"name": "Doc"},
    )

    evidence["source_url"] = "https://tampered.example"

    result = integrate_evidence_with_trust_graph(
        "graph-2",
        [evidence],
        target_id="record-2",
        observed_at="2026-05-21T00:00:00Z",
    )

    assert result["linked_evidence_count"] == 0


def test_review_required_evidence_still_traceable():
    evidence = create_evidence(
        "evidence-3",
        "image",
        "https://example.org/image.png",
        "2026-05-21T00:00:00Z",
        metadata={"edited": True},
    )

    result = integrate_evidence_with_trust_graph(
        "graph-3",
        [evidence],
        target_id="record-3",
        observed_at="2026-05-21T00:00:00Z",
    )

    assert result["linked_evidence_count"] == 1
