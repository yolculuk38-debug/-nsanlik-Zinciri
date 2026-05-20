from typing import Dict, List


GRAPH_VERSION = "hc-trust-graph-v1-experimental"


def build_trust_graph(
    *,
    record_id: str,
    witnesses: List[Dict] | None = None,
    audit_events: List[Dict] | None = None,
) -> Dict:
    """Build a lightweight trust graph for record, witness, and audit relationships."""

    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record_id must be a non-empty string")

    witnesses = witnesses or []
    audit_events = audit_events or []

    if not isinstance(witnesses, list):
        raise ValueError("witnesses must be a list")

    if not isinstance(audit_events, list):
        raise ValueError("audit_events must be a list")

    nodes = [
        {
            "id": record_id.strip(),
            "type": "record",
        }
    ]
    edges = []

    for index, witness in enumerate(witnesses):
        if not isinstance(witness, dict):
            continue

        witness_id = str(witness.get("id") or f"witness-{index + 1}")
        witness_type = str(witness.get("type", "unknown")).lower()

        nodes.append(
            {
                "id": witness_id,
                "type": "witness",
                "witness_type": witness_type,
            }
        )
        edges.append(
            {
                "from": witness_id,
                "to": record_id.strip(),
                "relationship": "attests_to",
            }
        )

    for index, event in enumerate(audit_events):
        if not isinstance(event, dict):
            continue

        event_id = str(event.get("event_id") or f"audit-event-{index + 1}")
        nodes.append(
            {
                "id": event_id,
                "type": "audit_event",
                "event_type": event.get("event_type"),
                "event_hash": event.get("event_hash"),
            }
        )
        edges.append(
            {
                "from": event_id,
                "to": record_id.strip(),
                "relationship": "records_history_for",
            }
        )

    return {
        "graph_version": GRAPH_VERSION,
        "record_id": record_id.strip(),
        "nodes": nodes,
        "edges": edges,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "experimental": True,
    }
