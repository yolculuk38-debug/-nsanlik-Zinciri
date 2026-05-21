"""HC:// temporal trust decay core.

Temporal decay lowers stale verification confidence over time.
It does not invalidate records by itself; it creates an auditable freshness signal.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


DEFAULT_HALF_LIFE_DAYS = 180
MIN_DECAY_FACTOR = 0.25


def parse_iso8601(value: str) -> datetime:
    """Parse ISO-8601 timestamps with Z support."""

    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def calculate_age_days(verified_at: str, now: str) -> int:
    verified = parse_iso8601(verified_at)
    current = parse_iso8601(now)
    delta = current - verified
    return max(0, delta.days)


def decay_factor(age_days: int, half_life_days: int = DEFAULT_HALF_LIFE_DAYS) -> float:
    """Calculate bounded exponential decay factor."""

    if half_life_days <= 0:
        raise ValueError("half_life_days must be positive")
    raw = 0.5 ** (age_days / half_life_days)
    return max(MIN_DECAY_FACTOR, raw)


def apply_temporal_decay(
    trust_score: int,
    verified_at: str,
    now: str,
    *,
    half_life_days: int = DEFAULT_HALF_LIFE_DAYS,
) -> dict[str, Any]:
    """Apply temporal trust decay to a trust score."""

    age = calculate_age_days(verified_at, now)
    factor = decay_factor(age, half_life_days)
    decayed_score = round(max(0, min(100, trust_score)) * factor)

    if age == 0:
        freshness = "CURRENT"
    elif age <= 30:
        freshness = "RECENT"
    elif age <= 180:
        freshness = "AGING"
    else:
        freshness = "STALE"

    return {
        "original_score": max(0, min(100, trust_score)),
        "decayed_score": decayed_score,
        "age_days": age,
        "decay_factor": round(factor, 4),
        "freshness": freshness,
        "half_life_days": half_life_days,
    }


__all__ = [
    "DEFAULT_HALF_LIFE_DAYS",
    "MIN_DECAY_FACTOR",
    "apply_temporal_decay",
    "calculate_age_days",
    "decay_factor",
]
