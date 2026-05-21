from certificate_chain import (
    build_certificate_chain_entry,
    verify_certificate_chain,
)


def test_valid_certificate_chain():
    entry = build_certificate_chain_entry(
        {
            "certificate_version": "HC-CERTIFICATE-V1",
            "verified": True,
        },
        previous_certificate_hash="prev-hash",
    )

    result = verify_certificate_chain(entry)

    assert result["trusted"] is True


def test_invalid_certificate_chain():
    result = verify_certificate_chain(
        {
            "chain_integrity": False,
        }
    )

    assert result["decision"] == "INVALID"
