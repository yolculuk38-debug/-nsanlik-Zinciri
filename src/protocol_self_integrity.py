"""HC:// protocol self-integrity core.

Verifies HC:// internal protocol module inventory before external trust decisions.
Self-integrity is the foundation for evaluating other systems.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


SELF_INTEGRITY_VERSION = "HC-SELF-INTEGRITY-V1"

REQUIRED_CORE_MODULES = {
    "verification_api",
    "verification_orchestrator",
    "zero_trust_gateway",
    "trust_score",
    "consensus_rules",
    "signed_witness",
    "audit_snapshots_v2",
    "federation_sync",
    "node_registry",
    "signed_federation_exchange",
    "evidence_review",
    "social_media_bridge",
    "media_provenance",
    "trust_graph",
}


class SelfIntegrityStatus:
    VERIFIED = "VERIFIED"
    DEGRADED = "DEGRADED"
    INVALID = "INVALID"


def canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def manifest_hash(manifest: dict[str, Any]) -> str:
    unsigned = dict(manifest)
    unsigned.pop("manifest_hash", None)
    return hashlib.sha256(canonical_json(unsigned).encode("utf-8")).hexdigest()


def build_self_integrity_manifest(modules: dict[str, str]) -> dict[str, Any]:
    """Build deterministic self-integrity manifest.

    modules maps module name to hash/version identifier.
    """

    manifest = {
        "self_integrity_version": SELF_INTEGRITY_VERSION,
        "module_count": len(modules),
        "modules": dict(sorted(modules.items())),
    }
    manifest["manifest_hash"] = manifest_hash(manifest)
    return manifest


def verify_self_integrity_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(manifest, dict):
        return {"status": SelfIntegrityStatus.INVALID, "verified": False, "reason": "manifest must be an object"}

    required = {"self_integrity_version", "module_count", "modules", "manifest_hash"}
    missing = required.difference(manifest)
    if missing:
        return {
            "status": SelfIntegrityStatus.INVALID,
            "verified": False,
            "reason": f"missing required field(s): {', '.join(sorted(missing))}",
        }

    if manifest["self_integrity_version"] != SELF_INTEGRITY_VERSION:
        return {"status": SelfIntegrityStatus.INVALID, "verified": False, "reason": "unsupported self-integrity version"}

    expected = manifest_hash(manifest)
    if expected != manifest["manifest_hash"]:
        return {"status": SelfIntegrityStatus.INVALID, "verified": False, "reason": "manifest hash mismatch"}

    modules = manifest.get("modules", {})
    if not isinstance(modules, dict):
        return {"status": SelfIntegrityStatus.INVALID, "verified": False, "reason": "modules must be an object"}

    missing_modules = sorted(REQUIRED_CORE_MODULES.difference(modules))
    if missing_modules:
        return {
            "status": SelfIntegrityStatus.DEGRADED,
            "verified": False,
            "missing_modules": missing_modules,
            "reason": "required core modules missing",
        }

    return {
        "status": SelfIntegrityStatus.VERIFIED,
        "verified": True,
        "module_count": manifest["module_count"],
        "reason": "protocol self-integrity verified",
    }


__all__ = [
    "SELF_INTEGRITY_VERSION",
    "REQUIRED_CORE_MODULES",
    "SelfIntegrityStatus",
    "build_self_integrity_manifest",
    "verify_self_integrity_manifest",
    "manifest_hash",
]
