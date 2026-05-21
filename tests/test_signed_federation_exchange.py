from signed_federation_exchange import (
    create_exchange_packet,
    sign_exchange_packet,
    verify_exchange_packet,
)


SECRET = "hc-fed-secret"


def build_signed_packet():
    packet = create_exchange_packet(
        "node-a",
        "node-b",
        "hash123",
        "nonce-1",
        "2026-05-21T00:00:00Z",
    )
    return sign_exchange_packet(packet, SECRET)


def test_valid_exchange_packet():
    result = verify_exchange_packet(
        build_signed_packet(),
        SECRET,
        now="2026-05-21T00:02:00Z",
    )

    assert result["verified"] is True


def test_replay_detection():
    signed = build_signed_packet()

    result = verify_exchange_packet(
        signed,
        SECRET,
        now="2026-05-21T00:02:00Z",
        seen_nonces={"nonce-1"},
    )

    assert result["verified"] is False


def test_expired_exchange_packet():
    result = verify_exchange_packet(
        build_signed_packet(),
        SECRET,
        now="2026-05-21T01:00:00Z",
    )

    assert result["verified"] is False


def test_signature_mismatch():
    signed = build_signed_packet()
    signed["packet"]["payload_hash"] = "tampered"

    result = verify_exchange_packet(
        signed,
        SECRET,
        now="2026-05-21T00:02:00Z",
    )

    assert result["verified"] is False
