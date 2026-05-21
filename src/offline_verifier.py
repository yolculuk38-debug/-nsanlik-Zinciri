"""HC:// offline verification flow."""

from __future__ import annotations

from typing import Any

from exported_proof import build_exported_proof
from public_validator import validate_public_proof


OFFLINE_VERIFIER_VERSION = "HC-OFFLINE-VERIFIER-V1"


def verify_offline_proof_package(
    proof_package: dict[str, Any],
) -> dict[str, Any]:
    """Verify exported HC:// proof package without network dependency."""

    validation = validate_public_proof(proof_package)

    return {
        "offline_verifier_version": OFFLINE_VERIFIER_VERSION,
        "offline_capable": True,
        "network_required": False,
        "validation": validation,
    }


def create_demo_offline_package(record_id: str) -> dict[str, Any]:
    """Create a portable offline verification package."""

    return build_exported_proof(
        record_id=record_id,
        content_hash="offline-demo-hash",
        verification_level="LEVEL_3_MULTI_WITNESS_VERIFIED",
        trust_passport={"status": "VERIFIED"},
        witnesses=[
            {
                "witness_signature": "offline-sig-1",
                "provenance_reference": "offline-prov-1",
            },
            {
                "witness_signature": "offline-sig-2",
                "provenance_reference": "offline-prov-2",
            },
        ],
        revision_chain={"broken": False},
    )


__all__ = [
    "OFFLINE_VERIFIER_VERSION",
    "verify_offline_proof_package",
    "create_demo_offline_package",
]
