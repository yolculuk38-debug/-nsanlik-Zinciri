"""HC:// SDK/API verification response standard."""

from __future__ import annotations

from typing import Any


SDK_RESPONSE_VERSION = "HC-SDK-RESPONSE-V1"


def build_sdk_verification_response(
    verification_result: dict[str, Any],
    *,
    request_id: str | None = None,
    platform: str = "SDK",
) -> dict[str, Any]:
    """Build standardized SDK/API verification response."""

    validation = verification_result.get("validation", {})

    return {
        "sdk_response_version": SDK_RESPONSE_VERSION,
        "request_id": request_id,
        "platform": platform,
        "decision": validation.get("decision"),
        "verified": validation.get("verified", False),
        "verification_level": validation.get("verification_level"),
        "risk_flags": validation.get("risk_flags", []),
        "reasons": validation.get("reasons", []),
        "portable": True,
        "explainable": True,
    }


__all__ = [
    "SDK_RESPONSE_VERSION",
    "build_sdk_verification_response",
]
