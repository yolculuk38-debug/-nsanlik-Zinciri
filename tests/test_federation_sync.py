from federation_sync import FederationStatus, validate_federation_packet


def valid_packet():
    return {
        "federation_version": "HC-FEDERATION-V1",
        "node_id": "node-1",
        "snapshot_hash": "abc123",
        "source_url": "https://example.org/hc/snapshot.json",
        "export_verified": True,
        "snapshot_verified": True,
        "signed": True,
        "consensus": False,
    }


def test_verified_federation_packet():
    result = validate_federation_packet(valid_packet())
    assert result["status"] == FederationStatus.VERIFIED
    assert result["trusted"] is True


def test_untrusted_packet_with_low_signals():
    packet = valid_packet()
    packet["snapshot_verified"] = False
    packet["signed"] = False

    result = validate_federation_packet(packet)
    assert result["status"] == FederationStatus.UNTRUSTED


def test_invalid_packet_missing_fields():
    result = validate_federation_packet({})
    assert result["status"] == FederationStatus.INVALID


def test_unsafe_protocol_rejected():
    packet = valid_packet()
    packet["source_url"] = "http://unsafe.local"

    result = validate_federation_packet(packet)
    assert result["status"] == FederationStatus.UNSAFE
