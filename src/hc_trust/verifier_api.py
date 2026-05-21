from typing import Dict, List

from .consensus_engine import evaluate_consensus
from .evidence_weight import calculate_evidence_weight
from .policy_engine import evaluate_trust_policy
from .risk_flags import build_risk_flags
from .score_normalizer import normalize_trust_score
from .verify_gateway import build_verify_response
from .verify_payload import build_verification_payload
from .witness_summary import build_witness_summary


VERIFIER_API_VERSION = "hc-verifier-api-v1-experimental"


def build_verifier_api_response(
    *,
    record_id: str,
    evidence: Dict,
    evidence_items: List[Dict] | None = None,
    witnesses: List[Dict] | None = None,
) -> Dict:
    """Build a unified HC:// verifier API response from evidence and witnesses."""

    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record_id must be a non-empty string")

    if not isinstance(evidence, dict):
        raise ValueError("evidence must be a dictionary")

    evidence_items = evidence_items or []
    witnesses = witnesses or []

    if not isinstance(evidence_items, list):
        raise ValueError("evidence_items must be a list")

    if not isinstance(witnesses, list):
        raise ValueError("witnesses must be a list")

    verification_response = build_verify_response(record_id, evidence)
    verification_payload = build_verification_payload(verification_response)
    risk_summary = build_risk_flags(verification_response.get("indicators", []))
    witness_summary = build_witness_summary(witnesses)
    consensus = evaluate_consensus(witnesses)
    evidence_weight = calculate_evidence_weight(evidence_items)

    normalized = normalize_trust_score(
        verification_response["trust_score"],
        risk_flags=risk_summary,
        witness_summary=witness_summary,
    )

    policy = evaluate_trust_policy(
        normalized_score=normalized["normalized_score"],
        risk_flags=risk_summary,
        witness_summary=witness_summary,
    )

    return {
        "api_version": VERIFIER_API_VERSION,
        "record_id": record_id.strip(),
        "verification_response": verification_response,
        "verification_payload": verification_payload,
        "risk_summary": risk_summary,
        "witness_summary": witness_summary,
        "consensus": consensus,
        "evidence_weight": evidence_weight,
        "normalized_score": normalized,
        "policy": policy,
        "experimental": True,
    }
