from manipulation_detection import (
    ManipulationRiskLevel,
    detect_coordinated_manipulation,
)
from trust_graph import build_trust_graph, create_graph_edge


def test_low_risk_graph():
    graph = build_trust_graph(
        "graph-low",
        [create_graph_edge("a", "b", "references", "2026-05-21T00:00:00Z")],
    )

    result = detect_coordinated_manipulation(graph)
    assert result["risk_level"] == ManipulationRiskLevel.LOW


def test_high_risk_mirror_cluster():
    edges = [
        create_graph_edge(f"source-{i}", "target", "mirrors", "2026-05-21T00:00:00Z")
        for i in range(6)
    ]
    graph = build_trust_graph("graph-high", edges)

    result = detect_coordinated_manipulation(graph)
    assert result["risk_level"] == ManipulationRiskLevel.HIGH
    assert "mirror_cluster" in result["risk_flags"]
    assert "single_target_amplification" in result["risk_flags"]


def test_synchronized_timing_detected():
    edges = [
        create_graph_edge(f"a-{i}", f"b-{i}", "repost_of", "2026-05-21T00:01:30Z")
        for i in range(5)
    ]
    graph = build_trust_graph("graph-sync", edges)

    result = detect_coordinated_manipulation(graph)
    assert "synchronized_timing" in result["risk_flags"]


def test_invalid_graph():
    result = detect_coordinated_manipulation({})
    assert result["risk_level"] == ManipulationRiskLevel.INVALID
