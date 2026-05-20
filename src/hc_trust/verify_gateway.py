from typing import Dict

from .api_schema import to_api_response, validate_verify_response
from .result_formatter import format_trust_result
from .trust_engine import ExperimentalTrustEngine


def build_verify_response(record_id: str, evidence: Dict) -> Dict:
    """Build an API-ready HC:// verification response from record evidence."""

    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record_id must be a non-empty string")

    if not isinstance(evidence, dict):
        raise ValueError("evidence must be a dictionary")

    engine = ExperimentalTrustEngine()
    trust_result = engine.calculate(evidence)
    formatted_result = format_trust_result(record_id.strip(), trust_result)
    api_response = to_api_response(formatted_result)

    if not validate_verify_response(api_response):
        raise ValueError("generated verification response is invalid")

    return api_response
