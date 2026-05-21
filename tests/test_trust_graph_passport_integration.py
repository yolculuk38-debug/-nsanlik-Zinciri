from trust_graph import build_trust_graph, create_graph_edge
from trust_graph_passport_integration import build_graph_trust_passport


def test_low_risk_graph_passport():
    graph = build_trust_graph(
        "graph-1",
        [create_graph_edge("a", "b", "references", "2026-05-21T00:00:00Z")],
    )

    passport = build_graph_trust_passport(
        "HC-1",
        {
            "hash_verified": True,
            "witness_count": 4,
            "provenance_locked": True,
            "trust_score": 95,
        },
        graph,
    )

    assert passport["status_engine"]["state"] in {"VERIFIED", "PARTIAL"}


def test_high_risk_graph_passport():
    graph = build_trust_graph(
        "graph-2",
        [
            create_graph_edge(f"src-{i}", "target", "mirrors", "2026-05-21T00:00:00Z")
            for i in range(6)
        ],
    )

    passport = build_graph_trust_passport(
        "HC-2",
        {
            "hash_verified": True,
            "witness_count": 3,
            "trust_score": 80,
        },
        graph,
    )

    assert "manipulation_review_required" in passport["risk_flags"]
