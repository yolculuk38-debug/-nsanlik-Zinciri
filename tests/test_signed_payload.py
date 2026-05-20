from hc_trust.signed_payload import canonical_payload, sign_payload, verify_signed_payload


def test_canonical_payload_is_deterministic():
    first = canonical_payload({"b": 2, "a": 1})
    second = canonical_payload({"a": 1, "b": 2})

    assert first == second
    assert first == '{"a":1,"b":2}'


def test_sign_payload_verifies_with_correct_secret():
    payload = {"record_id": "HC-TEST-2026-0001", "trust_score": 91}
    envelope = sign_payload(payload, "test-secret")

    assert envelope["algorithm"] == "HMAC-SHA256"
    assert verify_signed_payload(envelope, "test-secret") is True


def test_signed_payload_rejects_wrong_secret():
    payload = {"record_id": "HC-TEST-2026-0001", "trust_score": 91}
    envelope = sign_payload(payload, "test-secret")

    assert verify_signed_payload(envelope, "wrong-secret") is False


def test_signed_payload_rejects_tampered_payload():
    payload = {"record_id": "HC-TEST-2026-0001", "trust_score": 91}
    envelope = sign_payload(payload, "test-secret")
    envelope["payload"]["trust_score"] = 10

    assert verify_signed_payload(envelope, "test-secret") is False


def test_signed_payload_rejects_invalid_envelope():
    assert verify_signed_payload({}, "test-secret") is False
