from sdk_response import build_sdk_verification_response


def test_sdk_response_build():
    response = build_sdk_verification_response(
        {
            "validation": {
                "decision": "VERIFIED",
                "verified": True,
                "verification_level": "LEVEL_3_MULTI_WITNESS_VERIFIED",
                "risk_flags": [],
                "reasons": [],
            }
        },
        request_id="REQ-1",
    )

    assert response["decision"] == "VERIFIED"
    assert response["verified"] is True
    assert response["portable"] is True
    assert response["explainable"] is True
