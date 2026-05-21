"""HC:// QR verification hardening utilities.

This module validates QR verification payloads without granting automatic trust.
A QR scan is only a pointer to verification data; it is not proof by itself.
"""

from __future__ import annotations

import hashlib
import json
import re
from enum import Enum
from typing import Any
from urllib.parse import urlparse


TRUSTED_QR_DOMAINS = {"github.com", "yolculuk38-debug.github.io"}
TRUSTED_PATH_HINTS = ("HC-TRUST-LAYER", "Insanlik-Zinciri", "records", "verify", "docs")
SHA256_RE = re.compile(r"^[a-fA-F0-9]{64}$")


class QRStatus(str, Enum):
    """Machine-readable QR verification status values."""

    VERIFIED = "VERIFIED"
    HASH_MISMATCH = "HASH_MISMATCH"
    INVALID_QR = "INVALID_QR"
    UNSAFE_URL = "UNSAFE_URL"
    UNSIGNED = "UNSIGNED"


REQUIRED_FIELDS = ("record_id", "content_hash", "verification_url", "created_at")


def canonical_json(data: Any) -> str:
    """Return deterministic JSON for QR payload hashing and comparison."""

    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_text(value: str) -> str:
    """Return SHA-256 hex digest for UTF-8 text."""

    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _load_payload(payload: str | dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    if isinstance(payload, dict):
        return payload, None
    if isinstance(payload, str):
        try:
            decoded = json.loads(payload)
        except json.JSONDecodeError as exc:
            return None, f"QR payload is not valid JSON: {exc}"
        if not isinstance(decoded, dict):
            return None, "QR payload JSON must be an object"
        return decoded, None
    return None, "QR payload must be a JSON string or object"


def _safe_verification_url(url: str) -> tuple[bool, str | None]:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        return False, "verification_url must use https"
    if parsed.netloc not in TRUSTED_QR_DOMAINS:
        return False, f"untrusted verification_url domain: {parsed.netloc}"
    if not any(hint in parsed.path for hint in TRUSTED_PATH_HINTS):
        return False, "verification_url path does not match HC verification paths"
    return True, None


def verify_qr_payload(payload: str | dict[str, Any]) -> dict[str, Any]:
    """Verify a QR payload without automatically trusting it.

    Expected payload fields:
    - record_id
    - content_hash
    - verification_url
    - created_at
    - signature: optional
    - content: optional; when present, SHA-256 must match content_hash
    """

    data, error = _load_payload(payload)
    if error:
        return {"status": QRStatus.INVALID_QR.value, "trusted": False, "reason": error}
    assert data is not None

    missing = [field for field in REQUIRED_FIELDS if not data.get(field)]
    if missing:
        return {
            "status": QRStatus.INVALID_QR.value,
            "trusted": False,
            "reason": f"missing required field(s): {', '.join(missing)}",
        }

    content_hash = str(data["content_hash"])
    if not SHA256_RE.match(content_hash):
        return {
            "status": QRStatus.HASH_MISMATCH.value,
            "trusted": False,
            "reason": "content_hash is not a valid SHA-256 hex digest",
        }

    is_safe_url, url_error = _safe_verification_url(str(data["verification_url"]))
    if not is_safe_url:
        return {"status": QRStatus.UNSAFE_URL.value, "trusted": False, "reason": url_error}

    content = data.get("content")
    if content is not None:
        content_text = content if isinstance(content, str) else canonical_json(content)
        calculated_hash = sha256_text(content_text)
        if calculated_hash.lower() != content_hash.lower():
            return {
                "status": QRStatus.HASH_MISMATCH.value,
                "trusted": False,
                "reason": "content hash does not match QR payload content",
                "calculated_hash": calculated_hash,
            }

    if not data.get("signature"):
        return {
            "status": QRStatus.UNSIGNED.value,
            "trusted": False,
            "reason": "QR payload is structurally valid but unsigned",
        }

    return {
        "status": QRStatus.VERIFIED.value,
        "trusted": True,
        "reason": "QR payload passed structural, hash, URL, and signature presence checks",
    }


__all__ = [
    "QRStatus",
    "TRUSTED_QR_DOMAINS",
    "verify_qr_payload",
    "canonical_json",
    "sha256_text",
]
