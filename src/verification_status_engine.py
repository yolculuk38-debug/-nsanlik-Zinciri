"""HC:// verification status engine.

Centralizes verification levels, state transitions, invalid-state propagation,
and explainable verification outcomes across HC:// modules.
"""

from __future__ import annotations

from enum import Enum
from typing import Any


STATUS_ENGINE_VERSION = "HC-VERIFICATION-STATUS-ENGINE-V1"


class VerificationLevel(str, Enum):
    LEVEL_0_UNVERIFIED = "LEVEL_0_UNVERIFIED"
    LEVEL_1_HASH_VERIFIED = "LEVEL_1_HASH_VERIFIED"
    LEVEL_2_WITNESS_REVIEWED = "LEVEL_2_WITNESS_REVIEWED"
    LEVEL_3_MULTI_WITNESS_VERIFIED = "LEVEL_3_MULTI_WITNESS_VERIFIED"
    LEVEL_4_PROVENANCE_LOCKED = "LEVEL_4_PROVENANCE_LOCKED"
    LEVEL_5_FEDERATED_VERIFIED = "LEVEL_5_FEDERATED_VERIFIED"


class VerificationState(str, Enum):
    VERIFIED = "VERIFIED"
    PARTIAL = "PARTIAL"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    UNTRUSTED = "UNTRUSTED"
    INVALID = "INVALID"


def determine_verification_status(signals: dict[str, Any]) -> dict[str, Any]:
    """Determine verification level and state from normalized trust signals."""

    if not isinstance(signals, dict):
        return {
            "engine_version": STATUS_ENGINE_VERSION,
            "state": VerificationState.INVALID.value,
            "level": VerificationLevel.LEVEL_0_UNVERIFIED.value,
            "trusted": False,
            "reasons": ["signals must be an object"],
        }

    invalid = bool(signals.get("invalid", False))
    hash_verified = bool(signals.get("hash_verified", False))
    witness_count = int(signals.get("witness_count", 0) or 0)
    provenance_locked = bool(signals.get("provenance_locked", False))
    federated_verified = bool(signals.get("federated_verified", False))
    risk_flags = list(signals.get("risk_flags", []) or [])
    trust_score = int(signals.get("trust_score", 0) or 0)

    reasons: list[str] = []

    if invalid:
        return {
            "engine_version": STATUS_ENGINE_VERSION,
            "state": VerificationState.INVALID.value,
            "level": VerificationLevel.LEVEL_0_UNVERIFIED.value,
            "trusted": False,
            "reasons": ["invalid signal present"],
            "risk_flags": risk_flags,
        }

    if not hash_verified:
        return {
            "engine_version": STATUS_ENGINE_VERSION,
            "state": VerificationState.UNTRUSTED.value,
            "level": VerificationLevel.LEVEL_0_UNVERIFIED.value,
            "trusted": False,
            "reasons": ["hash not verified"],
            "risk_flags": risk_flags,
        }

    level = VerificationLevel.LEVEL_1_HASH_VERIFIED
    reasons.append("hash verified")

    if witness_count >= 1:
        level = VerificationLevel.LEVEL_2_WITNESS_REVIEWED
        reasons.append("witness reviewed")

    if witness_count >= 3:
        level = VerificationLevel.LEVEL_3_MULTI_WITNESS_VERIFIED
        reasons.append("multi-witness threshold reached")

    if provenance_locked:
        level = VerificationLevel.LEVEL_4_PROVENANCE_LOCKED
        reasons.append("provenance locked")

    if federated_verified and provenance_locked and witness_count >= 3:
        level = VerificationLevel.LEVEL_5_FEDERATED_VERIFIED
        reasons.append("federated verification aligned")

    if risk_flags:
        state = VerificationState.REVIEW_REQUIRED
        trusted = False
        reasons.append("risk flags require review")
    elif trust_score >= 85 and level in {
        VerificationLevel.LEVEL_4_PROVENANCE_LOCKED,
        VerificationLevel.LEVEL_5_FEDERATED_VERIFIED,
    }:
        state = VerificationState.VERIFIED
        trusted = True
    elif trust_score >= 60:
        state = VerificationState.PARTIAL
        trusted = False
        reasons.append("additional verification recommended")
    else:
        state = VerificationState.REVIEW_REQUIRED
        trusted = False
        reasons.append("trust score below verified threshold")

    return {
        "engine_version": STATUS_ENGINE_VERSION,
        "state": state.value,
        "level": level.value,
        "trusted": trusted,
        "trust_score": trust_score,
        "witness_count": witness_count,
        "risk_flags": sorted(set(risk_flags)),
        "reasons": reasons,
    }


__all__ = [
    "STATUS_ENGINE_VERSION",
    "VerificationLevel",
    "VerificationState",
    "determine_verification_status",
]
