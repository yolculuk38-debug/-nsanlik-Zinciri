from manipulation_detection import detect_coordinated_manipulation
from trust_graph import build_trust_graph, create_graph_edge


def test_repost_cluster_detection():
    edges = [
        create_graph_edge(f"source-{i}", f"target-{i}", "repost_of", "2026-05-21T00:02:00Z")
        for i in range(6)
    ]

    graph = build_trust_graph("graph-repost", edges)
    result = detect_coordinated_manipulation(graph)

    assert "repost_cluster" in result["risk_flags"]


def test_self_reference_loop_detection():
    graph = build_trust_graph(
        "graph-loop",
        [create_graph_edge("same", "same", "references", "2026-05-21T00:03:00Z")],
    )

    result = detect_coordinated_manipulation(graph)

    assert "self_reference_loop" in result["risk_flags"]
