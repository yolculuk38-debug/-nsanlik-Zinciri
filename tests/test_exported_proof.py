from exported_proof import build_exported_proof


def test_exported_proof_build():
    proof = build_exported_proof(
        record_id="HC-EXPORT-1",
        content_hash="abc123",
        verification_level="LEVEL_3_MULTI_WITNESS_VERIFIED",
        trust_passport={"status": "VERIFIED"},
        witnesses=[{"witness_signature": "sig1"}],
    )

    assert proof["proof_version"] == "HC-EXPORTED-PROOF-V1"
    assert proof["record_id"] == "HC-EXPORT-1"
    assert proof["verification_level"] == "LEVEL_3_MULTI_WITNESS_VERIFIED"
