from offline_verifier import (
    create_demo_offline_package,
    verify_offline_proof_package,
)


def test_offline_verification_package():
    package = create_demo_offline_package("HC-OFFLINE-1")

    result = verify_offline_proof_package(package)

    assert result["offline_capable"] is True
    assert result["network_required"] is False
    assert result["validation"]["decision"] == "VERIFIED"
