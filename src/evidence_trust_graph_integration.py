"""HC:// evidence review to trust graph integration.

Converts reviewed external evidence into deterministic trust graph nodes/edges.
This keeps external evidence traceable without granting automatic trust.
"""

from __future__ import annotations

from typing import Any

from evidence_review import EvidenceStatus, review_evidence
from trust_graph import build_trust_graph, create_graph_edge, validate_trust_graph


INTEGRATION_VERSION = "HC-EVIDENCE-GRAPH-INTEGRATION-V1"


def evidence_to_graph_edge(evidence: dict[str, Any], target_id: str, observed_at: str) -> dict[str, Any]:
    """Create a graph edge from an evidence object to a target record/content id."""

    return create_graph_edge(
        evidence.get("evidence_id", "unknown-evidence"),
        target_id,
        "references",
        observed_at,
        metadata={
            "integration_version": INTEGRATION_VERSION,
            "evidence_type": evidence.get("evidence_type"),
            "source_url": evidence.get("source_url"),
            "evidence_hash": evidence.get("evidence_hash"),
        },
    )


def integrate_evidence_with_trust_graph(
    graph_id: str,
    evidence_items: list[dict[str, Any]],
    *,
    target_id: str,
    observed_at: str,
) -> dict[str, Any]:
    """Review evidence items and map reviewable evidence into a trust graph."""

    edges = []
    review_results = []

    for evidence in evidence_items:
        review = review_evidence(evidence)
        review_results.append({
            "evidence_id": evidence.get("evidence_id") if isinstance(evidence, dict) else None,
            "review": review,
        })

        if review.get("status") in {EvidenceStatus.VERIFIED, EvidenceStatus.REVIEW_REQUIRED} and review.get("reviewable"):
            edges.append(evidence_to_graph_edge(evidence, target_id, observed_at))

    graph = build_trust_graph(graph_id, edges)
    validation = validate_trust_graph(graph)

    return {
        "integration_version": INTEGRATION_VERSION,
        "graph": graph,
        "graph_validation": validation,
        "review_results": review_results,
        "linked_evidence_count": len(edges),
        "total_evidence_count": len(evidence_items),
    }


__all__ = ["INTEGRATION_VERSION", "evidence_to_graph_edge", "integrate_evidence_with_trust_graph"]
