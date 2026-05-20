# HC:// Experimental Trust Engine v1

> Status: **Experimental / Draft Specification**
>
> This document defines the first experimental trust engine model for HC://. It is a forward-looking scoring and interpretation layer. It does **not** modify existing schemas, record formats, or current verification workflows.

## Purpose

HC:// needs an explainable trust computation model that can evolve while preserving simple and auditable verification foundations.

The experimental trust engine v1 is designed to:

- define dynamic trust calculation
- support future AI + human reviewer weighting
- prepare API compatibility
- support manipulation detection
- remain append-only compatible

## Design Principles

- **Experimental by default:** scores are guidance signals, not absolute truth declarations.
- **Layered scoring:** each trust signal is computed independently and then combined.
- **Explainability:** every score should be accompanied by score components and indicators.
- **Backward compatibility:** existing verification and schema behavior remains unchanged.
- **Append-only continuity:** new trust observations are written as new events.

## Trust Score Layers

The v1 model computes a composite trust score using the following layers:

1. **Hash integrity**
   - checks whether canonical content hash matches expected value.
2. **Witness diversity**
   - checks plurality and distribution of witness origins.
3. **Reviewer reputation**
   - checks historical reliability of participating reviewers.
4. **Signature validity**
   - checks validity and provenance of available signatures.
5. **Timestamp consistency**
   - checks timeline coherence across records and verification events.
6. **Append-only consistency**
   - checks whether event history is additive and non-destructive.
7. **Source reputation**
   - checks provenance quality and verifiability of source references.
8. **AI consensus**
   - checks agreement level among independent AI reviewers.
9. **Human consensus**
   - checks agreement level among independent human reviewers.

## Dynamic Trust Calculation (Experimental)

The trust score is normalized to `0-100` and recomputed whenever new verification evidence is appended.

Conceptual computation:

`trust_score = weighted_sum(layer_scores) - manipulation_penalties`

Where:

- each `layer_score` is in `0-100`
- each layer has a configurable weight profile
- penalties are derived from manipulation indicators
- recomputation is append-only event driven

### Future AI + Human Weighting

Weight profiles are intentionally configurable so HC:// can support different operational contexts later, including:

- balanced AI/human weighting
- human-priority weighting for governance-sensitive records
- AI-priority weighting for high-volume preliminary triage
- mixed weighting based on reviewer confidence and reputation

This is planned behavior and not a production-locked policy.

## Score Interpretation Ranges

Trust score ranges are interpreted as:

- `0-25` = **HIGH RISK**
- `26-50` = **REVIEW REQUIRED**
- `51-75` = **PARTIAL TRUST**
- `76-90` = **VERIFIED**
- `91-100` = **STRONG VERIFIED**

These ranges are experimental calibration defaults and may evolve in future versions.

## Manipulation Indicators (v1)

The engine should track and surface manipulation indicators as structured signals:

- hash mismatch
- reviewer collusion
- duplicate witnesses
- suspicious timestamp changes
- unverifiable source
- replayed verification attempts

Indicators can reduce trust scores and increase reviewer escalation priority.

## Append-Only Compatibility

The trust engine remains append-only compatible by design:

- trust calculations are represented as new verification/trust events
- previous trust events are preserved for historical audit trails
- score transitions are tracked across time without mutating older records

This preserves provenance and enables independent re-analysis.

## Future Architecture Alignment

The v1 trust engine is designed as a compatibility layer for future HC:// capabilities.

### API Integration

Planned API responses can expose trust results as stable, machine-readable objects with layer-level explainability.

### Browser Extension

Future browser verification tools can display trust score bands and manipulation indicators for end users.

### QR Trust Verification

QR scan flows can resolve to trust summaries that include current score, risk band, and evidence status.

### Public Verification Portal

A future public portal can present append-only trust timelines, reviewer participation, and consensus evolution.

### Enterprise Trust Layer

Enterprise contexts can apply policy-specific weighting profiles while preserving common HC:// trust signal semantics.

## Example Data

- Trust score example payload: [`examples/trust_score_example.json`](../examples/trust_score_example.json)

## Compatibility Statement

This specification is additive and experimental.

- It does not replace existing schemas.
- It does not change current verification workflows.
- It prepares structured interoperability for future trust-layer implementations.

## Related Documentation

- Verification result standard: [Verification Result Standard](./verification-result-standard.md)
- Architecture roadmap: [Architecture Roadmap](./architecture-roadmap.md)
- Experimental trust score foundation: [HC:// Experimental Trust Score Foundation](./trust-score.md)
- Trust scoring overview: [Trust Scoring](./trust-scoring.md)
