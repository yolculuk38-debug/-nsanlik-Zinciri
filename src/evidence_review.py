"""HC:// external evidence review layer.

Normalizes external evidence objects for social media, documents,
media metadata, screenshots, and external references.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any
from urllib.parse import urlparse


EVIDENCE_VERSION = "HC-EVIDENCE-V1"
VALID_EVIDENCE_TYPES = {
    "social_post",
    "news_article",
    "image",
    "video",
    "document",
    "screenshot",
    "external_reference",
}


class EvidenceStatus:
    VERIFIED = "VERIFIED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    INVALID = "INVALID"
    UNSAFE = "UNSAFE"


def canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def evidence_hash(evidence: dict[str, Any]) -> str:
    normalized = dict(evidence)
    normalized.pop("evidence_hash", None)
    return hashlib.sha256(canonical_json(normalized).encode("utf-8")).hexdigest()


def create_evidence(
    evidence_id: str,
    evidence_type: str,
    source_url: str,
    collected_at: str,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    evidence = {
        "evidence_version": EVIDENCE_VERSION,
        "evidence_id": evidence_id,
        "evidence_type": evidence_type,
        "source_url": source_url,
        "collected_at": collected_at,
        "metadata": metadata or {},
    }
    evidence["evidence_hash"] = evidence_hash(evidence)
    return evidence


def review_evidence(evidence: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(evidence, dict):
        return {"status": EvidenceStatus.INVALID, "reviewable": False, "reason": "evidence must be an object"}

    required = {
        "evidence_version",
        "evidence_id",
        "evidence_type",
        "source_url",
        "collected_at",
        "evidence_hash",
    }

    missing = required.difference(evidence)
    if missing:
        return {
            "status": EvidenceStatus.INVALID,
            "reviewable": False,
            "reason": f"missing required field(s): {', '.join(sorted(missing))}",
        }

    if evidence["evidence_version"] != EVIDENCE_VERSION:
        return {
            "status": EvidenceStatus.INVALID,
            "reviewable": False,
            "reason": "unsupported evidence version",
        }

    if evidence["evidence_type"] not in VALID_EVIDENCE_TYPES:
        return {
            "status": EvidenceStatus.INVALID,
            "reviewable": False,
            "reason": "unsupported evidence type",
        }

    parsed = urlparse(str(evidence["source_url"]))
    if parsed.scheme != "https":
        return {
            "status": EvidenceStatus.UNSAFE,
            "reviewable": False,
            "reason": "evidence source_url must use https",
        }

    expected_hash = evidence_hash(evidence)
    if expected_hash != evidence["evidence_hash"]:
        return {
            "status": EvidenceStatus.INVALID,
            "reviewable": False,
            "reason": "evidence hash mismatch",
        }

    review_flags = []
    metadata = evidence.get("metadata", {})

    if not metadata:
        review_flags.append("missing_metadata")

    if evidence["evidence_type"] in {"image", "video", "screenshot"}:
        review_flags.append("media_review_recommended")

    if review_flags:
        return {
            "status": EvidenceStatus.REVIEW_REQUIRED,
            "reviewable": True,
            "review_flags": review_flags,
            "reason": "evidence requires additional review",
        }

    return {
        "status": EvidenceStatus.VERIFIED,
        "reviewable": True,
        "reason": "evidence structure verified",
    }


__all__ = [
    "EVIDENCE_VERSION",
    "EvidenceStatus",
    "VALID_EVIDENCE_TYPES",
    "create_evidence",
    "review_evidence",
    "evidence_hash",
]
