# HC:// Experimental Trust Score Foundation

> Status: **Experimental / Interpretation Layer**
>
> HC:// trust scores are experimental interpretation layers, **not objective truth measurements**.

## Purpose

This document defines a simple, human-readable foundation for trust interpretation in HC:// TRUST LAYER.

It explains concepts only. It does **not** implement automated scoring, does **not** modify validation logic, and does **not** change schema structure.

## Trust Signal Categories

HC:// separates trust-related signals into distinct categories so they are not mixed together.

### 1) Integrity Score

Integrity score is an interpretation of technical consistency checks, such as whether the content hash matches expected material.

- Strong integrity signal: valid hash match
- Weak integrity signal: missing or mismatched hash

Integrity answers: "Is the artifact internally consistent with its recorded fingerprint?"

### 2) Provenance Confidence

Provenance confidence reflects how clearly the origin and chain-of-custody can be traced.

- Higher provenance confidence: source links are clear, stable, and verifiable
- Lower provenance confidence: origin is unclear or references are missing

Provenance answers: "Do we have reliable origin context for this artifact?"

### 3) Witness Confidence

Witness confidence reflects confidence in witness context (for example, whether there are multiple independent witnesses and whether witness records are reviewable).

- Higher witness confidence: multiple independent witness entries with consistent context
- Lower witness confidence: single or weakly documented witness context

Witness confidence answers: "How strong is corroboration around this artifact?"

### 4) Verification Status

Verification status reflects the current technical validation state.

Typical states include:

- pass
- fail
- pending

Verification status answers: "What is the current validation outcome under current rules?"

### 5) Dispute / Revocation Impact

Dispute or revocation metadata can lower confidence even when technical integrity checks pass.

- Dispute impact: open disputes may reduce confidence until resolved
- Revocation impact: revocation notices may significantly reduce confidence depending on scope and evidence

This category answers: "Is there an active challenge or withdrawal signal affecting interpretation?"

## Simple Example Trust Model

A simple future-ready interpretation model:

- valid hash
- verified provenance
- multiple witnesses
- no dispute flag

→ higher confidence interpretation.

This is an interpretation pattern only, not an objective truth guarantee.

## Why Valid Hash Alone Is Insufficient

A valid hash confirms consistency with a specific content state, but it does not prove full trust context.

Examples:

1. Authenticity gap:
   - Content may be hashed correctly, but original source identity may still be unknown.
2. Context gap:
   - Content may be untampered after capture, but could still be misleading without provenance context.
3. Dispute gap:
   - Hash may validate while a legitimate dispute or revocation process is active.
4. Corroboration gap:
   - Hash alone does not provide multi-party witness corroboration.

## Future Considerations

Future versions may expand this foundation while keeping interpretation client-visible and reviewable:

- witness weighting
- signed witness records
- dispute handling
- revocation impact
- independent client interpretation

## Scope Reminder

This document defines conceptual foundations only.

- No automated trust scoring is implemented here.
- No validation logic is changed.
- No schema structure is changed.
