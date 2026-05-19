# HC:// Witness Layer

> Status: **Documentation / Conceptual guidance**
>
> Witness information is supporting context for verification and auditability.

## Purpose

The witness layer records who/what observed, validated, or attested to a record event.

Witnesses do not replace cryptographic validation. They add traceability, context, and review depth.

## Witness Types

## 1) Human Witness

A human witness is a person-based attestation.

Typical role:

- confirms that a record, statement, or artifact was reviewed by a human actor
- may provide role/context metadata (reviewer, maintainer, operator)
- can strengthen accountability for governance and audit trails

## 2) AI Witness

An AI witness is a model-generated witness statement or review artifact.

Typical role:

- records model-level assessment of consistency, structure, or claims
- may provide comparative analysis across versions/sources
- supports multi-model review when used with other witness types

## 3) System Witness

A system witness is produced by automated infrastructure.

Typical role:

- records machine verification outcomes (schema checks, hash checks, pipeline checks)
- captures reproducible technical observations
- helps maintain continuity across frequent validation runs

## 4) Commit/Timestamp Witness

A commit/timestamp witness links a record state to source-control or time evidence.

Typical role:

- binds verification context to commit identifiers and timestamps
- supports audit reconstruction across repository history
- improves temporal traceability for "what was known, when"

## Practical Guidance

- Prefer mixed witness sets (human + AI + system) when possible.
- Preserve witness metadata in stable, machine-readable formats.
- Keep witness entries attributable and time-bounded.
- Use witness context as a complement to hash/provenance validation.

## Related Drafts

- [Experimental Signed Witness Record Format](./signed-witness-format.md)
