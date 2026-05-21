from hashlib import sha256
from typing import Dict, List


TAMPER_ENGINE_VERSION = "hc-tamper-v1-experimental"


def build_integrity_snapshot(payload: Dict) -> Dict:
    if not isinstance(payload, dict):
        raise ValueError("payload must be a dictionary")

    normalized = str(sorted(payload.items())).encode("utf-8")
    digest = sha256(normalized).hexdigest()

    return {
        "engine": TAMPER_ENGINE_VERSION,
        "digest": digest,
        "fields": sorted(payload.keys()),
    }


def compare_integrity_snapshots(
    baseline: Dict,
    candidate: Dict,
) -> Dict:
    baseline_snapshot = build_integrity_snapshot(baseline)
    candidate_snapshot = build_integrity_snapshot(candidate)

    tampered = baseline_snapshot["digest"] != candidate_snapshot["digest"]

    changed_fields = sorted(
        set(candidate.keys()).symmetric_difference(set(baseline.keys()))
    )

    return {
        "tampered": tampered,
        "baseline_digest": baseline_snapshot["digest"],
        "candidate_digest": candidate_snapshot["digest"],
        "changed_fields": changed_fields,
        "engine": TAMPER_ENGINE_VERSION,
    }


def evaluate_chain_integrity(records: List[Dict]) -> Dict:
    if not isinstance(records, list):
        raise ValueError("records must be a list")

    digests = []

    for record in records:
        snapshot = build_integrity_snapshot(record)
        digests.append(snapshot["digest"])

    unique_digests = len(set(digests))

    return {
        "engine": TAMPER_ENGINE_VERSION,
        "records_checked": len(records),
        "unique_digests": unique_digests,
        "chain_consistent": unique_digests == len(digests),
    }
