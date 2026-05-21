from zero_trust_gateway import GatewayDecision, evaluate_gateway_request


def valid_request():
    return {
        "request_id": "req-1",
        "source": "node-a",
        "record_id": "HC-2026-0001",
        "purpose": "verify_record",
        "signals": {
            "signed": True,
            "verified_source": True,
            "replay_safe": True,
            "trusted_node": True,
            "rate_limited": True,
        },
    }


def test_gateway_allow():
    result = evaluate_gateway_request(valid_request())
    assert result["decision"] == GatewayDecision.ALLOW
    assert result["allowed"] is True


def test_gateway_challenge():
    request = valid_request()
    request["signals"]["replay_safe"] = False

    result = evaluate_gateway_request(request)
    assert result["decision"] == GatewayDecision.CHALLENGE


def test_gateway_deny():
    request = valid_request()
    request["signals"] = {}

    result = evaluate_gateway_request(request)
    assert result["decision"] == GatewayDecision.DENY


def test_gateway_invalid_purpose():
    request = valid_request()
    request["purpose"] = "unsafe"

    result = evaluate_gateway_request(request)
    assert result["decision"] == GatewayDecision.DENY
