from temporal_trust_decay import apply_temporal_decay


def test_current_record_no_major_decay():
    result = apply_temporal_decay(
        90,
        "2026-05-21T00:00:00Z",
        "2026-05-21T00:00:00Z",
    )

    assert result["decayed_score"] == 90
    assert result["freshness"] == "CURRENT"


def test_recent_record_decay():
    result = apply_temporal_decay(
        100,
        "2026-04-21T00:00:00Z",
        "2026-05-21T00:00:00Z",
    )

    assert result["decayed_score"] <= 100
    assert result["freshness"] == "RECENT"


def test_stale_record_decay():
    result = apply_temporal_decay(
        100,
        "2024-01-01T00:00:00Z",
        "2026-05-21T00:00:00Z",
    )

    assert result["freshness"] == "STALE"
    assert result["decayed_score"] < 100


def test_decay_never_negative():
    result = apply_temporal_decay(
        -50,
        "2024-01-01T00:00:00Z",
        "2026-05-21T00:00:00Z",
    )

    assert result["decayed_score"] >= 0


def test_decay_clamped_maximum():
    result = apply_temporal_decay(
        999,
        "2026-01-01T00:00:00Z",
        "2026-05-21T00:00:00Z",
    )

    assert result["original_score"] <= 100
