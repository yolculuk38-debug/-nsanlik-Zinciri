import hashlib
import hmac
import json
from typing import Dict


SIGNATURE_VERSION = "hc-signature-v1-experimental"


def canonical_payload(payload: Dict) -> str:
    """Return deterministic JSON for signing and verification."""

    if not isinstance(payload, dict):
        raise ValueError("payload must be a dictionary")

    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sign_payload(payload: Dict, secret: str) -> Dict:
    """Sign a payload with an HMAC-SHA256 signature envelope."""

    if not isinstance(secret, str) or not secret:
        raise ValueError("secret must be a non-empty string")

    canonical = canonical_payload(payload)
    signature = hmac.new(secret.encode("utf-8"), canonical.encode("utf-8"), hashlib.sha256).hexdigest()

    return {
        "signature_version": SIGNATURE_VERSION,
        "algorithm": "HMAC-SHA256",
        "signature": signature,
        "payload": payload,
        "experimental": True,
    }


def verify_signed_payload(envelope: Dict, secret: str) -> bool:
    """Verify an HMAC-SHA256 signed payload envelope."""

    if not isinstance(envelope, dict):
        return False

    if envelope.get("signature_version") != SIGNATURE_VERSION:
        return False

    payload = envelope.get("payload")
    signature = envelope.get("signature")

    if not isinstance(payload, dict) or not isinstance(signature, str):
        return False

    expected = sign_payload(payload, secret)["signature"]
    return hmac.compare_digest(signature, expected)
