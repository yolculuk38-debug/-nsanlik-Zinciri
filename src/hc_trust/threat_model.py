from typing import Dict, List


THREAT_MODEL_VERSION = "hc-threat-model-v1-experimental"

THREAT_SEVERITY = {
    "qr_spoofing": "HIGH",
    "payload_tampering": "CRITICAL",
    "witness_collusion": "HIGH",
    "replay_attack": "HIGH",
    "unsigned_payload": "HIGH",
    "unverified_source": "MEDIUM",
    "timestamp_anomaly": "MEDIUM",
    "duplicate_witnesses": "MEDIUM",
}


def classify_threats(signals: List[str]) -> Dict:
    """Classify HC:// security signals into a compact threat summary."""

    if signals is None:
        signals = []

    if not isinstance(signals, list):
        raise ValueError("signals must be a list")

    threats = []
    unknown_signals = []

    for signal in signals:
        if not isinstance(signal, str):
            unknown_signals.append("invalid_signal_shape")
            continue

        normalized = signal.strip().lower()
        severity = THREAT_SEVERITY.get(normalized)

        if severity:
            threats.append({"signal": normalized, "severity": severity})
        else:
            unknown_signals.append(normalized)

    critical = any(threat["severity"] == "CRITICAL" for threat in threats)
    high = any(threat["severity"] == "HIGH" for threat in threats)

    if critical:
        posture = "BLOCK"
    elif high:
        posture = "REVIEW_REQUIRED"
    elif threats:
        posture = "MONITOR"
    else:
        posture = "CLEAR"

    return {
        "threat_model_version": THREAT_MODEL_VERSION,
        "posture": posture,
        "threats": threats,
        "threat_count": len(threats),
        "unknown_signals": unknown_signals,
        "experimental": True,
    }
