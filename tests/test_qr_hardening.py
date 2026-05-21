import json

from qr_hardening import QRStatus, sha256_text, verify_qr_payload


SAFE_URL = "https://github.com/yolculuk38-debug/HC-TRUST-LAYER/blob/main/docs/index.md"


def build_payload(content="HC:// TRUST", signed=True):
    payload = {
        "record_id": "HC-QR-2026-0001",
        "content": content,
        "content_hash": sha256_text(content),
        "verification_url": SAFE_URL,
        "created_at": "2026-05-21T09:20:00Z",
    }
    if signed:
        payload["signature"] = "HC-SIGNATURE"
    return payload


def test_verified_qr_payload():
    result = verify_qr_payload(build_payload())
    assert result["status"] == QRStatus.VERIFIED.value
    assert result["trusted"] is True


def test_unsigned_qr_payload():
    result = verify_qr_payload(build_payload(signed=False))
    assert result["status"] == QRStatus.UNSIGNED.value
    assert result["trusted"] is False


def test_tampered_qr_payload_hash_mismatch():
    payload = build_payload()
    payload["content"] = "tampered"
    result = verify_qr_payload(payload)
    assert result["status"] == QRStatus.HASH_MISMATCH.value


def test_unsafe_qr_url():
    payload = build_payload()
    payload["verification_url"] = "https://evil.example/phishing"
    result = verify_qr_payload(payload)
    assert result["status"] == QRStatus.UNSAFE_URL.value


def test_invalid_qr_missing_fields():
    payload = {"record_id": "HC"}
    result = verify_qr_payload(payload)
    assert result["status"] == QRStatus.INVALID_QR.value


def test_invalid_qr_json_string():
    result = verify_qr_payload("not-json")
    assert result["status"] == QRStatus.INVALID_QR.value


def test_valid_json_payload_input():
    payload = build_payload()
    result = verify_qr_payload(json.dumps(payload))
    assert result["status"] == QRStatus.VERIFIED.value
