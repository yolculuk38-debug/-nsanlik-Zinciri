# Reviewer Registry and Independent Review Pool (HC:// TRUST LAYER)

> Status: **Experimental / Governance Support Layer**
>
> This document defines how reviewers are listed for trust interpretation support. It does **not** modify validation logic, workflows, or schema structure.

## Purpose

The reviewer registry provides a transparent, auditable list of approved reviewers that may contribute to trust interpretation and review workflows.

Goals:

- define how approved human, AI, institutional, and system reviewers may be listed
- prevent uncontrolled reviewer capture
- support independent multi-perspective verification
- keep verified records immutable while allowing review layers to evolve

## Core Model

HC:// TRUST LAYER separates immutable verification records from evolving review interpretation layers.

### 1) Core records are immutable-style

Core verification records (for example record identity, hash evidence, and recorded verification context) must not be silently changed after publication.

If changes are needed, they should be represented as new append operations or superseding records with clear audit traceability.

### 2) Reviewer pools may evolve over time

The reviewer registry is intentionally evolvable. Approved reviewer entries may be added, suspended, retired, or reclassified over time as governance and risk posture evolve.

### 3) Reviews are append-only

Review events should be appended as time-ordered entries. Prior review history is preserved for auditability.

### 4) Old reviews are not deleted

Historical reviews are never silently removed from history. They may be:

- disputed
- revoked
- superseded
- retired

This preserves traceability while allowing correction and accountability.

## Reviewer Types

The registry may contain the following reviewer types:

- **human expert reviewer**: identified individual reviewer with domain expertise.
- **AI reviewer**: named model/system reviewer used for analysis support.
- **institutional reviewer**: recognized organization or institution acting as reviewer.
- **system reviewer**: deterministic or policy-bound verification system.

## Reviewer Status

Each reviewer entry should include one status:

- **active**: approved and currently eligible for selection.
- **suspended**: temporarily ineligible pending review or remediation.
- **retired**: no longer selected for new reviews; historical reviews remain visible.
- **experimental**: limited-scope use for pilot evaluation, clearly marked.

## Reviewer Metadata Fields

Minimum recommended metadata fields for approved reviewer entries:

- `reviewer_id`
- `reviewer_type`
- `display_name`
- `specialization`
- `independence_level`
- `status`
- `public_key_optional`
- `conflict_of_interest_notes`
- `added_at`
- `retired_at`

## Example: Approved Reviewer Registry (JSON)

```json
{
  "registry_version": "2026-05-01",
  "reviewers": [
    {
      "reviewer_id": "hr-001",
      "reviewer_type": "human_expert",
      "display_name": "Independent OSINT Analyst A",
      "specialization": ["provenance", "open-source verification"],
      "independence_level": "high",
      "status": "active",
      "public_key_optional": "ed25519:ABC123EXAMPLE",
      "conflict_of_interest_notes": "No declared funding or direct stake in reviewed publisher.",
      "added_at": "2026-05-01T00:00:00Z",
      "retired_at": null
    },
    {
      "reviewer_id": "ai-004",
      "reviewer_type": "ai_reviewer",
      "display_name": "Model Review Node X",
      "specialization": ["consistency checks", "cross-document discrepancy detection"],
      "independence_level": "medium",
      "status": "experimental",
      "public_key_optional": null,
      "conflict_of_interest_notes": "Model provider relationship disclosed in governance docs.",
      "added_at": "2026-05-03T00:00:00Z",
      "retired_at": null
    }
  ]
}
```

## Independent Review Pool Principles

To reduce capture risk and improve review quality, reviewer pool management should follow these principles:

- **No random unrestricted reviewer injection:** reviewer admission must be explicit and auditable.
- **No single reviewer should control trust interpretation:** interpretation should not depend on one authority.
- **Mixed human + AI review is preferred for high-impact records:** combine contextual judgment and scalable analysis.
- **Conflicts of interest must be declared:** reviewer context must be visible before interpretation weighting.
- **Reviewer selection should be transparent:** selection rationale and reviewer identity class should be inspectable.

## Reviewer Registry Is Not Governance Capture

The reviewer registry supports transparent reviewer selection and auditability.

It is **not** a mechanism for centralized narrative control.

Key distinction:

- the registry defines who is eligible for review participation under transparent criteria,
- while trust interpretation remains open to independent scrutiny, disputes, and multi-perspective review.

In this model, accountability is increased through visibility of reviewer identity, status, and review history, rather than reduced through hidden authority.

## Scope Reminder

This document is a documentation and governance-layer definition only.

- No workflow behavior is changed here.
- No validation logic is changed here.
- No schema structure is changed here.


## Related Documentation

- Signed witness model: [Signed Witness Model](./signed-witness-model.md)
- Reviewer selection principles: [Reviewer Selection Principles](./reviewer-selection.md)
- Trust score foundation: [HC:// Experimental Trust Score Foundation](./trust-score.md)
- Append-only review chain model: [Append-Only Review Chain Model](./append-only-review-chain.md)

