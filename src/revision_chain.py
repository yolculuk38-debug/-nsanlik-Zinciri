"""HC:// revision chain engine."""

from __future__ import annotations

import hashlib
import json
from typing import Any

REVISION_CHAIN_VERSION = "HC-REVISION-CHAIN-V1"
GENESIS_REVISION_PARENT = "GENESIS"


class RevisionChainStatus:
    VERIFIED = "VERIFIED"
    BROKEN = "BROKEN"
    INVALID = "INVALID"


def canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def revision_hash(revision: dict[str, Any]) -> str:
    unsigned = dict(revision)
    unsigned.pop("revision_hash", None)
    return hashlib.sha256(canonical_json(unsigned).encode("utf-8")).hexdigest()


def create_revision(
    record_id: str,
    revision_number: int,
    content_hash: str,
    changed_at: str,
    *,
    previous_revision_hash: str = GENESIS_REVISION_PARENT,
    change_summary: str = "",
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    revision = {
        "revision_chain_version": REVISION_CHAIN_VERSION,
        "record_id": record_id,
        "revision_number": revision_number,
        "content_hash": content_hash,
        "previous_revision_hash": previous_revision_hash,
        "changed_at": changed_at,
        "change_summary": change_summary,
        "metadata": metadata or {},
    }
    revision["revision_hash"] = revision_hash(revision)
    return revision


def verify_revision(revision: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(revision, dict):
        return {"status": RevisionChainStatus.INVALID, "verified": False, "reason": "revision must be an object"}

    required = {
        "revision_chain_version",
        "record_id",
        "revision_number",
        "content_hash",
        "previous_revision_hash",
        "changed_at",
        "revision_hash",
    }
    missing = required.difference(revision)
    if missing:
        return {"status": RevisionChainStatus.INVALID, "verified": False, "reason": "missing fields"}

    if revision["revision_chain_version"] != REVISION_CHAIN_VERSION:
        return {"status": RevisionChainStatus.INVALID, "verified": False, "reason": "unsupported version"}

    if revision_hash(revision) != revision["revision_hash"]:
        return {"status": RevisionChainStatus.BROKEN, "verified": False, "reason": "hash mismatch"}

    return {"status": RevisionChainStatus.VERIFIED, "verified": True, "reason": "revision verified"}


def verify_revision_chain(revisions: list[dict[str, Any]]) -> dict[str, Any]:
    if not isinstance(revisions, list) or not revisions:
        return {"status": RevisionChainStatus.INVALID, "verified": False, "reason": "invalid chain"}

    expected_parent = GENESIS_REVISION_PARENT
    expected_number = 1
    record_id = revisions[0].get("record_id")

    for revision in revisions:
        result = verify_revision(revision)
        if not result["verified"]:
            return {"status": RevisionChainStatus.BROKEN, "verified": False, "reason": result["reason"]}

        if revision.get("record_id") != record_id:
            return {"status": RevisionChainStatus.BROKEN, "verified": False, "reason": "record mismatch"}

        if revision.get("revision_number") != expected_number:
            return {"status": RevisionChainStatus.BROKEN, "verified": False, "reason": "number mismatch"}

        if revision.get("previous_revision_hash") != expected_parent:
            return {"status": RevisionChainStatus.BROKEN, "verified": False, "reason": "parent mismatch"}

        expected_parent = revision["revision_hash"]
        expected_number += 1

    return {
        "status": RevisionChainStatus.VERIFIED,
        "verified": True,
        "revision_count": len(revisions),
        "latest_revision_hash": expected_parent,
        "reason": "revision chain verified",
    }


__all__ = [
    "REVISION_CHAIN_VERSION",
    "GENESIS_REVISION_PARENT",
    "RevisionChainStatus",
    "create_revision",
    "verify_revision",
    "verify_revision_chain",
    "revision_hash",
]
