from typing import Dict, List

from .audit_trail import verify_audit_event


TIMELINE_VERSION = "hc-provenance-timeline-v1-experimental"


def build_provenance_timeline(events: List[Dict]) -> Dict:
    """Build a sorted provenance timeline from audit events."""

    if events is None:
        events = []

    if not isinstance(events, list):
        raise ValueError("events must be a list")

    valid_events = []
    invalid_count = 0

    for event in events:
        if not isinstance(event, dict) or not verify_audit_event(event):
            invalid_count += 1
            continue

        valid_events.append(event)

    sorted_events = sorted(valid_events, key=lambda event: event.get("timestamp", ""))

    return {
        "timeline_version": TIMELINE_VERSION,
        "event_count": len(sorted_events),
        "invalid_event_count": invalid_count,
        "record_ids": sorted({event.get("record_id") for event in sorted_events if event.get("record_id")}),
        "events": sorted_events,
        "experimental": True,
    }


def verify_timeline_chain(timeline: Dict) -> bool:
    """Verify that timeline events form a valid previous-hash chain when links are present."""

    if not isinstance(timeline, dict):
        return False

    events = timeline.get("events")
    if not isinstance(events, list):
        return False

    previous_hash = None

    for event in events:
        if not verify_audit_event(event):
            return False

        linked_previous = event.get("previous_event_hash")
        if linked_previous is not None and linked_previous != previous_hash:
            return False

        previous_hash = event.get("event_hash")

    return True
