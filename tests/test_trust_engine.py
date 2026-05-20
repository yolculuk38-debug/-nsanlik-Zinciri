from hc_trust.trust_engine import ExperimentalTrustEngine


def test_trust_engine_strong_verified_clean_input():
    engine = ExperimentalTrustEngine()

    result = engine.calculate({"hash_valid": True})

    assert result.score == 100
    assert result.level == "STRONG_VERIFIED"
    assert result.indicators == []


def test_trust_engine_detects_hash_mismatch():
    engine = ExperimentalTrustEngine()

    result = engine.calculate({"hash_valid": False})

    assert result.score == 60
    assert result.level == "PARTIAL_TRUST"
    assert "hash_mismatch" in result.indicators


def test_trust_engine_detects_multiple_risk_indicators():
    engine = ExperimentalTrustEngine()

    result = engine.calculate(
        {
            "hash_valid": False,
            "duplicate_witnesses": True,
            "timestamp_inconsistent": True,
            "unverified_source": True,
        }
    )

    assert result.score == 0
    assert result.level == "HIGH_RISK"
    assert result.indicators == [
        "hash_mismatch",
        "duplicate_witnesses",
        "timestamp_inconsistency",
        "unverified_source",
    ]
