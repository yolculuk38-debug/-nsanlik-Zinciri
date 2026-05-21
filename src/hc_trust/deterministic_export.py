import json
from hashlib import sha256
from typing import Dict


EXPORT_ENGINE_VERSION = "hc-deterministic-export-v1-experimental"


def canonical_export(data: Dict) -> str:
    if not isinstance(data, dict):
        raise ValueError("data must be a dictionary")

    return json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def build_export_digest(data: Dict) -> str:
    canonical = canonical_export(data)
    return sha256(canonical.encode("utf-8")).hexdigest()


def build_deterministic_export(data: Dict) -> Dict:
    canonical = canonical_export(data)
    digest = build_export_digest(data)

    return {
        "engine": EXPORT_ENGINE_VERSION,
        "canonical_export": canonical,
        "export_digest": digest,
        "export_size": len(canonical.encode("utf-8")),
        "deterministic": True,
    }


def verify_export_integrity(export_package: Dict) -> bool:
    if not isinstance(export_package, dict):
        return False

    canonical = export_package.get("canonical_export")
    digest = export_package.get("export_digest")

    if not isinstance(canonical, str) or not isinstance(digest, str):
        return False

    calculated = sha256(canonical.encode("utf-8")).hexdigest()
    return calculated == digest
