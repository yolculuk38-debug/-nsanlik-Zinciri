"""HC:// signed federation exchange core.

Signs federation exchange packets and verifies replay-resistant metadata.
This layer does not trust remote nodes automatically.
"""

from __future__ import annotations

import hashlib
import hmac
import json
from datetime import datetime, timezone
from typing import Any


EXCHANGE_VERSION = "HC-FED-EXCHANGE-V1"


def canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def parse_iso8601(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def create_exchange_packet(
    source_node: str,
    target_node: str,
    payload_hash: str,
    nonce: str,
    issued_at: str,
) -> dict[str, str]:
    return {
        "exchange_version": EXCHANGE_VERSION,
        "source_node": source_node,
        "target_node": target_node,
        "payload_hash": payload_hash,
        "nonce": nonce,
        "issued_at": issued_at,
    }


def sign_exchange_packet(packet: dict[str, Any], secret_key: str) -> dict[str, Any]:
    signature = hmac.new(
        secret_key.encode("utf-8"),
        canonical_json(packet).encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return {"packet": packet, "signature": signature}


def verify_exchange_packet(
    signed_packet: dict[str, Any],
    secret_key: str,
    *,
    now: str,
    max_age_seconds: int = 300,
    seen_nonces: set[str] | None = None,
) -> dict[str, Any]:
    if not isinstance(signed_packet, dict):
        return {"verified": False, "reason": "signed packet must be an object"}

    packet = signed_packet.get("packet")
    signature = signed_packet.get("signature")
    if not isinstance(packet, dict) or not signature:
        return {"verified": False, "reason": "missing packet or signature"}

    required = {"exchange_version", "source_node", "target_node", "payload_hash", "nonce", "issued_at"}
    missing = required.difference(packet)
    if missing:
        return {"verified": False, "reason": f"missing required field(s): {', '.join(sorted(missing))}"}

    if packet["exchange_version"] != EXCHANGE_VERSION:
        return {"verified": False, "reason": "unsupported exchange version"}

    if seen_nonces is not None and packet["nonce"] in seen_nonces:
        return {"verified": False, "reason": "replay detected"}

    try:
        issued = parse_iso8601(str(packet["issued_at"]))
        current = parse_iso8601(now)
    except ValueError as exc:
        return {"verified": False, "reason": f"invalid timestamp: {exc}"}

    age_seconds = abs((current - issued).total_seconds())
    if age_seconds > max_age_seconds:
        return {"verified": False, "reason": "exchange packet expired", "age_seconds": int(age_seconds)}

    expected = hmac.new(
        secret_key.encode("utf-8"),
        canonical_json(packet).encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    verified = hmac.compare_digest(str(signature), expected)
    if not verified:
        return {"verified": False, "reason": "signature mismatch"}

    return {"verified": True, "reason": "exchange packet verified", "age_seconds": int(age_seconds)}


__all__ = [
    "EXCHANGE_VERSION",
    "create_exchange_packet",
    "sign_exchange_packet",
    "verify_exchange_packet",
]
