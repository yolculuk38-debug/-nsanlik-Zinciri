import hashlib
import json
from typing import Dict, Optional


AUDIT_EVENT_VERSION = "hc-audit-event-v1-experimental"


def canonical_event(event: Dict) -> str:
    """Return deterministic JSON for audit event hashing."""

    if not isinstance(event, dict):
        raise ValueError("event must be a dictionary")

    return json.dumps(event, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def hash_event(event: Dict) -> str:
    """Hash a canonical audit event with SHA-256."""

    canonical = canonical_event(event)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def build_audit_event(
    *,
    event_id: str,
    event_type: str,
    record_id: str,
    payload_hash: str,
    timestamp: str,
    previous_event_hash: Optional[str] = None,
) -> Dict:
    """Build a tamper-evident audit event."""

    required = {
        "event_id": event_id,
        "event_type": event_type,
        "record_id": record_id,
        "payload_hash": payload_hash,
        "timestamp": timestamp,
    }

    for field, value in required.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be a non-empty string")

    event = {
        "audit_event_version": AUDIT_EVENT_VERSION,
        "event_id": event_id.strip(),
        "event_type": event_type.strip(),
        "record_id": record_id.strip(),
        "payload_hash": payload_hash.strip(),
        "timestamp": timestamp.strip(),
        "previous_event_hash": previous_event_hash,
        "experimental": True,
    }

    event["event_hash"] = hash_event(event)
    return event


def verify_audit_event(event: Dict) -> bool:
    """Verify an audit event hash against its canonical event body."""

    if not isinstance(event, dict):
        return False

    event_hash = event.get("event_hash")
    if not isinstance(event_hash, str) or not event_hash:
        return False

    body = dict(event)
    body.pop("event_hash", None)

    return hash_event(body) == event_hash
