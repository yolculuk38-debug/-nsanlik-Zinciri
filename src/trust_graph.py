"""HC:// cross-platform trust graph core.

Builds deterministic relationship graphs between evidence, media,
social references, and verification nodes.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


TRUST_GRAPH_VERSION = "HC-TRUST-GRAPH-V1"
VALID_EDGE_TYPES = {
    "repost_of",
    "derived_from",
    "references",
    "reported_by",
    "verified_by",
    "mirrors",
}


class TrustGraphStatus:
    VALID = "VALID"
    INVALID = "INVALID"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


def canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def graph_hash(graph: dict[str, Any]) -> str:
    normalized = dict(graph)
    normalized.pop("graph_hash", None)
    return hashlib.sha256(canonical_json(normalized).encode("utf-8")).hexdigest()


def create_graph_edge(
    source_id: str,
    target_id: str,
    edge_type: str,
    observed_at: str,
    *,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "source_id": source_id,
        "target_id": target_id,
        "edge_type": edge_type,
        "observed_at": observed_at,
        "metadata": metadata or {},
    }


def build_trust_graph(graph_id: str, edges: list[dict[str, Any]]) -> dict[str, Any]:
    graph = {
        "trust_graph_version": TRUST_GRAPH_VERSION,
        "graph_id": graph_id,
        "edge_count": len(edges),
        "edges": sorted(edges, key=lambda item: (item["source_id"], item["target_id"], item["edge_type"])),
    }
    graph["graph_hash"] = graph_hash(graph)
    return graph


def validate_trust_graph(graph: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(graph, dict):
        return {"status": TrustGraphStatus.INVALID, "reason": "graph must be an object"}

    required = {"trust_graph_version", "graph_id", "edge_count", "edges", "graph_hash"}
    missing = required.difference(graph)
    if missing:
        return {
            "status": TrustGraphStatus.INVALID,
            "reason": f"missing required field(s): {', '.join(sorted(missing))}",
        }

    if graph["trust_graph_version"] != TRUST_GRAPH_VERSION:
        return {"status": TrustGraphStatus.INVALID, "reason": "unsupported graph version"}

    expected = graph_hash(graph)
    if expected != graph["graph_hash"]:
        return {"status": TrustGraphStatus.INVALID, "reason": "graph hash mismatch"}

    flags = []
    for edge in graph["edges"]:
        if edge.get("edge_type") not in VALID_EDGE_TYPES:
            flags.append("unknown_edge_type")
        if edge.get("source_id") == edge.get("target_id"):
            flags.append("self_reference_edge")

    if flags:
        return {
            "status": TrustGraphStatus.REVIEW_REQUIRED,
            "review_flags": sorted(set(flags)),
            "reason": "graph requires additional review",
        }

    return {
        "status": TrustGraphStatus.VALID,
        "reason": "trust graph validated",
        "edge_count": graph["edge_count"],
    }


__all__ = [
    "TRUST_GRAPH_VERSION",
    "VALID_EDGE_TYPES",
    "TrustGraphStatus",
    "create_graph_edge",
    "build_trust_graph",
    "validate_trust_graph",
    "graph_hash",
]
