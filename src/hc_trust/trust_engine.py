from dataclasses import dataclass
from typing import Dict, List


@dataclass
class TrustResult:
    score: int
    level: str
    indicators: List[str]


class ExperimentalTrustEngine:
    """Experimental trust engine for HC://"""

    LEVELS = {
        (0, 25): "HIGH_RISK",
        (26, 50): "REVIEW_REQUIRED",
        (51, 75): "PARTIAL_TRUST",
        (76, 90): "VERIFIED",
        (91, 100): "STRONG_VERIFIED",
    }

    def calculate(self, data: Dict) -> TrustResult:
        score = 100
        indicators = []

        if not data.get("hash_valid", False):
            score -= 40
            indicators.append("hash_mismatch")

        if data.get("duplicate_witnesses", False):
            score -= 15
            indicators.append("duplicate_witnesses")

        if data.get("timestamp_inconsistent", False):
            score -= 20
            indicators.append("timestamp_inconsistency")

        if data.get("unverified_source", False):
            score -= 25
            indicators.append("unverified_source")

        score = max(0, min(score, 100))

        level = self._resolve_level(score)

        return TrustResult(
            score=score,
            level=level,
            indicators=indicators,
        )

    def _resolve_level(self, score: int) -> str:
        for score_range, level in self.LEVELS.items():
            low, high = score_range
            if low <= score <= high:
                return level

        return "UNKNOWN"
