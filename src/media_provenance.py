"""HC:// media provenance scanner core.

Creates deterministic media provenance fingerprints from metadata and file hashes.
This module does not claim media authenticity by itself.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


MEDIA_PROVENANCE_VERSION = "HC-MEDIA-PROVENANCE-V1"
SUPPORTED_MEDIA_TYPES = {"image", "video", "audio", "document", "archive"}


class MediaProvenanceStatus:
    PROVENANCE_READY = "PROVENANCE_READY"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    INVALID = "INVALID"
    HASH_MISMATCH = "HASH_MISMATCH"


def canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def provenance_hash(record: dict[str, Any]) -> str:
    unsigned = dict(record)
    unsigned.pop("provenance_hash", None)
    return sha256_text(canonical_json(unsigned))


def create_media_provenance(
    media_id: str,
    media_type: str,
    file_hash: str,
    observed_at: str,
    *,
    metadata: dict[str, Any] | None = None,
    parent_media_hash: str | None = None,
) -> dict[str, Any]:
    record = {
        "media_provenance_version": MEDIA_PROVENANCE_VERSION,
        "media_id": media_id,
        "media_type": media_type,
        "file_hash": file_hash,
        "observed_at": observed_at,
        "metadata": metadata or {},
        "parent_media_hash": parent_media_hash,
    }
    record["provenance_hash"] = provenance_hash(record)
    return record


def scan_media_provenance(record: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(record, dict):
        return {"status": MediaProvenanceStatus.INVALID, "reviewable": False, "reason": "record must be an object"}

    required = {
        "media_provenance_version",
        "media_id",
        "media_type",
        "file_hash",
        "observed_at",
        "provenance_hash",
    }
    missing = required.difference(record)
    if missing:
        return {
            "status": MediaProvenanceStatus.INVALID,
            "reviewable": False,
            "reason": f"missing required field(s): {', '.join(sorted(missing))}",
        }

    if record["media_provenance_version"] != MEDIA_PROVENANCE_VERSION:
        return {"status": MediaProvenanceStatus.INVALID, "reviewable": False, "reason": "unsupported media provenance version"}

    if record["media_type"] not in SUPPORTED_MEDIA_TYPES:
        return {"status": MediaProvenanceStatus.INVALID, "reviewable": False, "reason": "unsupported media type"}

    expected = provenance_hash(record)
    if expected != record["provenance_hash"]:
        return {"status": MediaProvenanceStatus.HASH_MISMATCH, "reviewable": False, "reason": "provenance hash mismatch"}

    flags = []
    metadata = record.get("metadata", {})
    if not metadata:
        flags.append("missing_metadata")
    if metadata.get("edited"):
        flags.append("edited_media")
    if metadata.get("ai_generated"):
        flags.append("ai_generated_signal")
    if record.get("parent_media_hash"):
        flags.append("derived_media_chain")

    if flags:
        return {
            "status": MediaProvenanceStatus.REVIEW_REQUIRED,
            "reviewable": True,
            "review_flags": flags,
            "reason": "media provenance requires additional review",
        }

    return {"status": MediaProvenanceStatus.PROVENANCE_READY, "reviewable": True, "reason": "media provenance ready"}


__all__ = [
    "MEDIA_PROVENANCE_VERSION",
    "SUPPORTED_MEDIA_TYPES",
    "MediaProvenanceStatus",
    "create_media_provenance",
    "scan_media_provenance",
    "provenance_hash",
]
