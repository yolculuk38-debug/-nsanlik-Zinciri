"""HC:// social media verification bridge.

Normalizes social media post references as evidence-ready objects.
This module does not scrape platforms or trust posts automatically.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any
from urllib.parse import urlparse


BRIDGE_VERSION = "HC-SOCIAL-BRIDGE-V1"
SUPPORTED_PLATFORMS = {
    "x",
    "twitter",
    "facebook",
    "instagram",
    "tiktok",
    "youtube",
    "linkedin",
    "reddit",
    "threads",
    "telegram",
}


class SocialBridgeStatus:
    NORMALIZED = "NORMALIZED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    INVALID = "INVALID"
    UNSAFE = "UNSAFE"


def canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def reference_hash(reference: dict[str, Any]) -> str:
    normalized = dict(reference)
    normalized.pop("reference_hash", None)
    return hashlib.sha256(canonical_json(normalized).encode("utf-8")).hexdigest()


def create_social_reference(
    reference_id: str,
    platform: str,
    post_url: str,
    observed_at: str,
    *,
    author_handle: str | None = None,
    post_id: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    reference = {
        "bridge_version": BRIDGE_VERSION,
        "reference_id": reference_id,
        "platform": platform.lower(),
        "post_url": post_url,
        "observed_at": observed_at,
        "author_handle": author_handle,
        "post_id": post_id,
        "metadata": metadata or {},
    }
    reference["reference_hash"] = reference_hash(reference)
    return reference


def normalize_social_reference(reference: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(reference, dict):
        return {"status": SocialBridgeStatus.INVALID, "reviewable": False, "reason": "reference must be an object"}

    required = {"bridge_version", "reference_id", "platform", "post_url", "observed_at", "reference_hash"}
    missing = required.difference(reference)
    if missing:
        return {
            "status": SocialBridgeStatus.INVALID,
            "reviewable": False,
            "reason": f"missing required field(s): {', '.join(sorted(missing))}",
        }

    if reference["bridge_version"] != BRIDGE_VERSION:
        return {"status": SocialBridgeStatus.INVALID, "reviewable": False, "reason": "unsupported bridge version"}

    if str(reference["platform"]).lower() not in SUPPORTED_PLATFORMS:
        return {"status": SocialBridgeStatus.REVIEW_REQUIRED, "reviewable": True, "reason": "unsupported or unknown platform"}

    parsed = urlparse(str(reference["post_url"]))
    if parsed.scheme != "https":
        return {"status": SocialBridgeStatus.UNSAFE, "reviewable": False, "reason": "post_url must use https"}

    expected = reference_hash(reference)
    if expected != reference["reference_hash"]:
        return {"status": SocialBridgeStatus.INVALID, "reviewable": False, "reason": "reference hash mismatch"}

    flags = []
    if not reference.get("author_handle"):
        flags.append("missing_author_handle")
    if not reference.get("post_id"):
        flags.append("missing_post_id")
    if reference.get("metadata", {}).get("edited"):
        flags.append("edited_post")
    if reference.get("metadata", {}).get("repost_of"):
        flags.append("repost_chain")

    if flags:
        return {
            "status": SocialBridgeStatus.REVIEW_REQUIRED,
            "reviewable": True,
            "review_flags": flags,
            "reason": "social reference requires additional review",
        }

    return {"status": SocialBridgeStatus.NORMALIZED, "reviewable": True, "reason": "social reference normalized"}


__all__ = [
    "BRIDGE_VERSION",
    "SUPPORTED_PLATFORMS",
    "SocialBridgeStatus",
    "create_social_reference",
    "normalize_social_reference",
    "reference_hash",
]
