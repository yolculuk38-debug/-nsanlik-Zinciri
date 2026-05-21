"""HC:// zero-trust verification gateway core.

Default deny gateway for verification requests. Every request must present
auditable signals before it is allowed to proceed.
"""

from __future__ import annotations

from typing import Any


GATEWAY_VERSION = "HC-ZERO-TRUST-GATEWAY-V1"


class GatewayDecision:
    ALLOW = "ALLOW"
    CHALLENGE = "CHALLENGE"
    DENY = "DENY"
    INVALID = "INVALID"


REQUIRED_REQUEST_FIELDS = {"request_id", "source", "record_id", "purpose"}
SAFE_PURPOSES = {"verify_record", "verify_qr", "verify_federation", "audit_lookup"}


def evaluate_gateway_request(request: dict[str, Any]) -> dict[str, Any]:
    """Evaluate a verification request using default-deny rules."""

    if not isinstance(request, dict):
        return {"decision": GatewayDecision.INVALID, "allowed": False, "reason": "request must be an object"}

    missing = REQUIRED_REQUEST_FIELDS.difference(request)
    if missing:
        return {
            "decision": GatewayDecision.INVALID,
            "allowed": False,
            "reason": f"missing required field(s): {', '.join(sorted(missing))}",
        }

    if request.get("purpose") not in SAFE_PURPOSES:
        return {"decision": GatewayDecision.DENY, "allowed": False, "reason": "unsafe or unsupported purpose"}

    signals = request.get("signals", {})
    if not isinstance(signals, dict):
        return {"decision": GatewayDecision.INVALID, "allowed": False, "reason": "signals must be an object"}

    signed = bool(signals.get("signed"))
    verified_source = bool(signals.get("verified_source"))
    replay_safe = bool(signals.get("replay_safe"))
    rate_limited = bool(signals.get("rate_limited", True))
    trusted_node = bool(signals.get("trusted_node", False))

    if not rate_limited:
        return {"decision": GatewayDecision.DENY, "allowed": False, "reason": "request is not rate limited"}

    strong_signals = sum([signed, verified_source, replay_safe, trusted_node])

    if signed and verified_source and replay_safe:
        return {
            "gateway_version": GATEWAY_VERSION,
            "decision": GatewayDecision.ALLOW,
            "allowed": True,
            "strong_signals": strong_signals,
            "reason": "request passed zero-trust gateway checks",
        }

    if strong_signals >= 2:
        return {
            "gateway_version": GATEWAY_VERSION,
            "decision": GatewayDecision.CHALLENGE,
            "allowed": False,
            "strong_signals": strong_signals,
            "reason": "additional verification required",
        }

    return {
        "gateway_version": GATEWAY_VERSION,
        "decision": GatewayDecision.DENY,
        "allowed": False,
        "strong_signals": strong_signals,
        "reason": "insufficient zero-trust signals",
    }


__all__ = ["GATEWAY_VERSION", "GatewayDecision", "evaluate_gateway_request"]
