"""HC:// exported proof format core."""

from __future__ import annotations

from typing import Any


EXPORTED_PROOF_VERSION = "HC-EXPORTED-PROOF-V1"


def build_exported_proof(
    *,
    record_id: str,
    content_hash: str,
    verification_level: str,
    trust_passport: dict[str, Any],
    witnesses: list[dict[str, Any]] | None = None,
    revision_chain: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build portable HC:// exported proof package."""

    return {
        "proof_version": EXPORTED_PROOF_VERSION,
        "record_id": record_id,
        "content_hash": content_hash,
        "content_hash_valid": True,
        "verification_level": verification_level,
        "trust_passport": trust_passport,
        "witnesses": witnesses or [],
        "revision_chain": revision_chain or {},
        "metadata": metadata or {},
    }


__all__ = [
    "EXPORTED_PROOF_VERSION",
    "build_exported_proof",
]
