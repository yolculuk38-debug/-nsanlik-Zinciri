# HC:// Verification Result Standard (v1)

> Status: **Foundational / Backward-Compatible Standardization Layer**
>
> This document defines a reusable verification result structure for HC:// outputs. It does **not** replace existing record schemas or alter current verification workflows.

## Why Standardized Verification Results Matter

Standardized verification results improve consistency across tools, interfaces, and reviewers.

Without a shared result format, each integration can describe outcomes differently, which makes comparisons, audit trails, and automation harder.

A common structure helps HC:// keep outputs:

- machine-readable
- reviewer-comparable
- append-only friendly
- stable across implementations

This supports long-term transparency while preserving simple current flows.

## Standard Scope

The `verification-result-v1` structure is designed to represent verification outcomes after record checks are performed.

It captures both technical checks (for example hash and signature validation) and trust interpretation fields (for example consensus and manipulation risk).

It does not redefine the record format itself.

## Canonical Fields (v1)

- `verification_id`
- `target_record`
- `verification_status`
- `hash_match`
- `signature_valid`
- `reviewer_pool`
- `consensus_score`
- `manipulation_risk`
- `timestamp`
- `verification_version`

Reference schema:

- [`schema/verification-result-v1.schema.json`](../schema/verification-result-v1.schema.json)

Example payload:

- [`examples/verification_result_example.json`](../examples/verification_result_example.json)

## Verification Status Enum

`verification_status` supports:

- `VERIFIED`
- `REVIEW_REQUIRED`
- `DISPUTED`
- `REVOKED`
- `EXPERIMENTAL`

## Manipulation Risk Enum

`manipulation_risk` supports:

- `LOW`
- `MEDIUM`
- `HIGH`
- `UNKNOWN`

## Future API Usage

This structure is designed so future API responses can return a stable verification object without changing the meaning of existing records.

Potential future API patterns:

- `GET /verification/{verification_id}` returning one `verification-result-v1` object.
- `GET /records/{record_id}/verifications` returning an append-only list of verification result objects.
- streaming or event feeds that emit the same object shape for clients.

By stabilizing field names now, clients can integrate once and stay compatible as transport layers evolve.

## Trust Layer Compatibility

The structure directly supports planned trust-layer concerns:

- **QR verification support:** `target_record` and `verification_status` can map to QR scan result pages.
- **Trust scoring support:** `consensus_score` and `manipulation_risk` provide normalized trust signal fields.
- **Reviewer systems support:** `reviewer_pool` enables multi-reviewer attribution and analysis.

This aligns with witness, trust-scoring, and reviewer registry documents without requiring immediate workflow changes.

## Append-Only Compatibility

The standard is append-only friendly by design:

- each event has its own `verification_id`
- each event is timestamped
- status transitions (`VERIFIED` → `DISPUTED` → `REVOKED`, etc.) can be represented as additional events rather than overwriting prior entries

This preserves historical verification context and supports auditability.

## Validation Example Command

You can validate the example payload against the schema with Python `jsonschema`:

```bash
python -m jsonschema -i examples/verification_result_example.json schema/verification-result-v1.schema.json
```

## Backward Compatibility Statement

This standard is additive.

- Existing record schemas are unchanged.
- Existing verification workflows remain unchanged.
- Existing record IDs and hash-based flows remain valid.

## Related Documentation

- Verify center: [HC:// Verify Center](./verify.md)
- Trust layer docs: [HC:// TRUST LAYER](./TRUST_LAYER.md)
- Architecture planning: [Architecture Roadmap](./architecture-roadmap.md)
- Signed witness concepts: [Signed Witness Model](./signed-witness-model.md)
- Append-only review model: [Append-Only Review Chain Model](./append-only-review-chain.md)
