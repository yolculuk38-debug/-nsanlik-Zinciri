"""HC:// node registry core.

Tracks federation nodes without granting automatic trust.
Node status is an operational signal, not authority.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import urlparse


REGISTRY_VERSION = "HC-NODE-REGISTRY-V1"


class NodeStatus:
    ACTIVE = "ACTIVE"
    OBSERVED = "OBSERVED"
    SUSPENDED = "SUSPENDED"
    REVOKED = "REVOKED"
    INVALID = "INVALID"


REQUIRED_NODE_FIELDS = {"node_id", "source_url", "public_key", "registered_at"}
VALID_STATUSES = {NodeStatus.ACTIVE, NodeStatus.OBSERVED, NodeStatus.SUSPENDED, NodeStatus.REVOKED}


def validate_node_entry(entry: dict[str, Any]) -> dict[str, Any]:
    """Validate one federation node registry entry."""

    if not isinstance(entry, dict):
        return {"valid": False, "status": NodeStatus.INVALID, "reason": "node entry must be an object"}

    missing = REQUIRED_NODE_FIELDS.difference(entry)
    if missing:
        return {
            "valid": False,
            "status": NodeStatus.INVALID,
            "reason": f"missing required field(s): {', '.join(sorted(missing))}",
        }

    parsed = urlparse(str(entry["source_url"]))
    if parsed.scheme != "https":
        return {"valid": False, "status": NodeStatus.INVALID, "reason": "node source_url must use https"}

    status = entry.get("status", NodeStatus.OBSERVED)
    if status not in VALID_STATUSES:
        return {"valid": False, "status": NodeStatus.INVALID, "reason": "invalid node status"}

    return {
        "valid": True,
        "status": status,
        "trusted": status == NodeStatus.ACTIVE and bool(entry.get("verified", False)),
        "reason": "node entry valid",
    }


def build_registry(nodes: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a deterministic node registry summary."""

    valid_nodes = []
    invalid_nodes = []

    seen: set[str] = set()
    for node in nodes:
        node_id = str(node.get("node_id", "")) if isinstance(node, dict) else ""
        result = validate_node_entry(node)
        if not result["valid"] or not node_id or node_id in seen:
            invalid_nodes.append({"node_id": node_id, "reason": result.get("reason", "duplicate or invalid node")})
            continue
        seen.add(node_id)
        valid_nodes.append(node)

    return {
        "registry_version": REGISTRY_VERSION,
        "node_count": len(valid_nodes),
        "invalid_count": len(invalid_nodes),
        "nodes": sorted(valid_nodes, key=lambda item: item["node_id"]),
        "invalid_nodes": invalid_nodes,
    }


__all__ = ["REGISTRY_VERSION", "NodeStatus", "validate_node_entry", "build_registry"]
