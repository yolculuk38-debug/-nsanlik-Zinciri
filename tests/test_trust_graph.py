from trust_graph import (
    TrustGraphStatus,
    build_trust_graph,
    create_graph_edge,
    validate_trust_graph,
)


def valid_graph():
    edge = create_graph_edge(
        "post-a",
        "post-b",
        "repost_of",
        "2026-05-21T00:00:00Z",
    )
    return build_trust_graph("graph-1", [edge])


def test_valid_graph():
    result = validate_trust_graph(valid_graph())
    assert result["status"] == TrustGraphStatus.VALID


def test_invalid_hash_detection():
    graph = valid_graph()
    graph["graph_id"] = "tampered"

    result = validate_trust_graph(graph)
    assert result["status"] == TrustGraphStatus.INVALID


def test_review_required_unknown_edge():
    edge = create_graph_edge(
        "a",
        "b",
        "unknown",
        "2026-05-21T00:00:00Z",
    )

    graph = build_trust_graph("graph-2", [edge])
    result = validate_trust_graph(graph)

    assert result["status"] == TrustGraphStatus.REVIEW_REQUIRED


def test_review_required_self_reference():
    edge = create_graph_edge(
        "same",
        "same",
        "references",
        "2026-05-21T00:00:00Z",
    )

    graph = build_trust_graph("graph-3", [edge])
    result = validate_trust_graph(graph)

    assert result["status"] == TrustGraphStatus.REVIEW_REQUIRED
