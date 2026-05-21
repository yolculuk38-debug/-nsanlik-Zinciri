"""HC:// federation sync layer core.

Federation allows multiple HC:// repositories or nodes to exchange
verification metadata without automatic trust.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import urlparse


TRUSTED_PROTOCOLS = {"https"}
SUPPORTED_FEDERATION_VERSION = "HC-FEDERATION-V1"


class FederationStatus:
    VERIFIED = "VERIFIED"
    UNTRUSTED = "UNTRUSTED"
    INVALID = "INVALID"
    UNSAFE = "UNSAFE"


REQUIRED_FIELDS = {
    "federation_version",
    "node_id",
    "snapshot_hash",
    "source_url",
    "export_verified",
}


def validate_federation_packet(packet: dict[str, Any]) -> dict[str, Any]:
    """Validate external federation metadata packet."""

    if not isinstance(packet, dict):
        return {
            "status": FederationStatus.INVALID,
            "trusted": False,
            "reason": "packet must be an object",
        }

    missing = REQUIRED_FIELDS.difference(packet)
    if missing:
        return {
            "status": FederationStatus.INVALID,
            "trusted": False,
            "reason": f"missing required field(s): {', '.join(sorted(missing))}",
        }

    if packet["federation_version"] != SUPPORTED_FEDERATION_VERSION:
        return {
            "status": FederationStatus.INVALID,
            "trusted": False,
            "reason": "unsupported federation version",
        }

    parsed = urlparse(str(packet["source_url"]))
    if parsed.scheme not in TRUSTED_PROTOCOLS:
        return {
            "status": FederationStatus.UNSAFE,
            "trusted": False,
            "reason": "unsafe federation protocol",
        }

    export_verified = bool(packet.get("export_verified"))
    snapshot_verified = bool(packet.get("snapshot_verified", False))
    signed = bool(packet.get("signed", False))
    consensus = bool(packet.get("consensus", False))

    trust_signals = sum([
        export_verified,
        snapshot_verified,
        signed,
        consensus,
    ])

    if trust_signals >= 3:
        return {
            "status": FederationStatus.VERIFIED,
            "trusted": True,
            "trust_signals": trust_signals,
            "reason": "federation packet passed verification thresholds",
        }

    return {
        "status": FederationStatus.UNTRUSTED,
        "trusted": False,
        "trust_signals": trust_signals,
        "reason": "external federation packet remains untrusted",
    }


__all__ = [
    "SUPPORTED_FEDERATION_VERSION",
    "FederationStatus",
    "validate_federation_packet",
]
