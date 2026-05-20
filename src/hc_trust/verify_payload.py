from typing import Dict


def build_verification_payload(response: Dict) -> Dict:
    """Build a lightweight HC:// verification payload for QR and public verification flows."""

    required_fields = {
        "record_id",
        "trust_score",
        "trust_level",
        "verified_at",
    }

    missing = required_fields - set(response.keys())
    if missing:
        raise ValueError(f"missing required verification response fields: {sorted(missing)}")

    trust_score = int(response["trust_score"])

    return {
        "record_id": response["record_id"],
        "verified": trust_score >= 76,
        "trust_level": response["trust_level"],
        "score": trust_score,
        "hash_valid": "hash_mismatch" not in response.get("indicators", []),
        "witness_count": len(response.get("indicators", [])),
        "timestamp": response["verified_at"],
        "experimental": True,
    }
