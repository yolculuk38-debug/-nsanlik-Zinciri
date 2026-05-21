"""HC:// media provenance to evidence review integration.

Converts media provenance records into external evidence objects so media
lineage can enter the standard evidence review and trust graph pipeline.
"""

from __future__ import annotations

from typing import Any

from evidence_review import create_evidence, review_evidence
from media_provenance import MediaProvenanceStatus, scan_media_provenance


INTEGRATION_VERSION = "HC-MEDIA-EVIDENCE-INTEGRATION-V1"
MEDIA_TYPE_TO_EVIDENCE_TYPE = {
    "image": "image",
    "video": "video",
    "audio": "external_reference",
    "document": "document",
    "archive": "external_reference",
}


def media_provenance_to_evidence(
    media_record: dict[str, Any],
    *,
    source_url: str,
    collected_at: str,
) -> dict[str, Any]:
    """Convert a media provenance record into a normalized evidence object."""

    media_type = media_record.get("media_type", "external_reference")
    evidence_type = MEDIA_TYPE_TO_EVIDENCE_TYPE.get(media_type, "external_reference")
    metadata = {
        "integration_version": INTEGRATION_VERSION,
        "media_id": media_record.get("media_id"),
        "media_type": media_type,
        "file_hash": media_record.get("file_hash"),
        "provenance_hash": media_record.get("provenance_hash"),
        "parent_media_hash": media_record.get("parent_media_hash"),
        "media_metadata": media_record.get("metadata", {}),
    }

    return create_evidence(
        f"evidence:{media_record.get('media_id', 'unknown-media')}",
        evidence_type,
        source_url,
        collected_at,
        metadata=metadata,
    )


def integrate_media_with_evidence_review(
    media_record: dict[str, Any],
    *,
    source_url: str,
    collected_at: str,
) -> dict[str, Any]:
    """Scan media provenance, convert to evidence, and review the evidence."""

    media_scan = scan_media_provenance(media_record)
    if media_scan.get("status") in {MediaProvenanceStatus.INVALID, MediaProvenanceStatus.HASH_MISMATCH}:
        return {
            "integration_version": INTEGRATION_VERSION,
            "linked": False,
            "media_scan": media_scan,
            "reason": "media provenance failed before evidence conversion",
        }

    evidence = media_provenance_to_evidence(
        media_record,
        source_url=source_url,
        collected_at=collected_at,
    )
    evidence_review = review_evidence(evidence)

    return {
        "integration_version": INTEGRATION_VERSION,
        "linked": bool(evidence_review.get("reviewable")),
        "media_scan": media_scan,
        "evidence": evidence,
        "evidence_review": evidence_review,
    }


__all__ = [
    "INTEGRATION_VERSION",
    "MEDIA_TYPE_TO_EVIDENCE_TYPE",
    "media_provenance_to_evidence",
    "integrate_media_with_evidence_review",
]
