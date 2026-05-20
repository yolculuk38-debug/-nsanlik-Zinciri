# Append-Only Review Chain Model (HC:// TRUST LAYER)

> Status: **Conceptual / Trust Infrastructure Foundation**
>
> This document defines an append-only review chain model for long-term trust interpretation. It does **not** modify workflows, schema definitions, or validation logic.

## Purpose

This model defines how HC:// TRUST LAYER can preserve immutable-style verified core records while allowing review interpretation layers to evolve over time.

Primary goals:

- prevent silent post-verification mutation of core record history
- support transparent review evolution through append-only events
- preserve long-term auditability and provenance traceability
- prepare architecture for future trust infrastructure upgrades

## Core Model

### 1) Immutable-style core records

Core records should not be silently modified after verification.

In practice, this means:

- verified record identity should remain stable
- hash-linked verification context should remain inspectable
- corrections should be represented through additional events or superseding records, not hidden edits

### 2) Evolving review layers

Review interpretation can evolve, but changes must be appended as explicit review events.

This allows additional context over time without rewriting prior history.

### 3) Visible, auditable review history

Reviews, disputes, revocations, and annotations are append-only.

Historical review entries must remain visible so observers can inspect:

- what was claimed
- who submitted the event
- when the event occurred
- how trust interpretation changed over time

## Review Event Types

The append-only chain should support at least these event types:

- **verification**: records that a verifier confirmed integrity or related checks.
- **annotation**: adds contextual notes without overriding prior events.
- **dispute**: signals a challenge to interpretation, provenance, or validity context.
- **revocation**: withdraws trust assertions under defined conditions.
- **superseded**: indicates a prior event or interpretation has been replaced by a newer event while retaining history.
- **reviewer-retired**: marks reviewer retirement for future selection while preserving historical events.

## Simple Append-Only Review Flow Example

Record Created  
↓  
Hash Verified  
↓  
AI Review Added  
↓  
Human Review Added  
↓  
Dispute Added  
↓  
Resolution Added

In this flow, no earlier entry is deleted. Resolution is additive and traceable.

## Why Append-Only Review Chains Matter

### Auditability

Append-only history enables complete audit trails across the lifecycle of each record and review interpretation state.

### Transparency

Observers can see trust-affecting changes directly rather than relying on hidden state transitions.

### Anti-manipulation

Prohibiting silent rewrites raises the cost of history tampering and reduces narrative manipulation risk.

### Historical traceability

Long-term provenance analysis depends on being able to reconstruct sequence, authorship, and timing of events.

## Changing trust interpretation is not the same as changing historical records.

Trust interpretation may legitimately change as new evidence appears.

However, interpretation updates must be represented as new appended events, while historical records remain intact and inspectable.

This distinction is essential for accountable governance and defensible provenance.

## Simple JSON Event Example

```json
{
  "event_id": "evt-2026-05-20-0001",
  "event_type": "annotation",
  "reviewer_id": "ai-004",
  "timestamp": "2026-05-20T10:30:00Z",
  "target_record": "HC-TEST-2026-0001",
  "notes": "Cross-source context note added for follow-up human review."
}
```

## Scope Reminder

This is a documentation-level model definition only.

- No workflows are modified.
- No schemas are modified.
- No validation logic is modified.

## Related Documentation

- Signed witness model: [Signed Witness Model](./signed-witness-model.md)
- Trust score foundation: [HC:// Experimental Trust Score Foundation](./trust-score.md)
- Reviewer registry: [Reviewer Registry and Independent Review Pool](./reviewer-registry.md)
- Verify center overview: [HC:// Verify Center](./verify.md)
- Future architecture planning: [Architecture Roadmap](./architecture-roadmap.md)
