"""HC:// revision chain to status engine integration."""

from __future__ import annotations

from typing import Any

from revision_chain import RevisionChainStatus, verify_revision_chain
from verification_status_engine import determine_verification_status


INTEGRATION_VERSION = "HC-REVISION-STATUS-INTEGRATION-V1"


def verify_revision_status(
    revisions: list[dict[str, Any]],
    *,
    base_signals: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Verify revision chain and map result into centralized status engine."""

    chain_result = verify_revision_chain(revisions)
    signals = dict(base_signals or {})

    if chain_result.get("status") != RevisionChainStatus.VERIFIED:
        signals["invalid"] = True
        signals.setdefault("risk_flags", [])
        signals["risk_flags"] = list(signals["risk_flags"]) + ["revision_chain_broken"]
    else:
        signals["provenance_locked"] = True
        signals.setdefault("hash_verified", True)

    status_result = determine_verification_status(signals)

    return {
        "integration_version": INTEGRATION_VERSION,
        "chain_result": chain_result,
        "status_result": status_result,
    }


__all__ = ["INTEGRATION_VERSION", "verify_revision_status"]
