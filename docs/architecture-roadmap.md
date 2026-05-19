# Architecture Roadmap (v0.2 / v0.3)

> Status: **Planned / Future Work**
>
> This document captures future protocol architecture decisions for HC:// TRUST LAYER.
> None of the items below are current production features.

## What Should Remain Simple

In the current phase, the project should intentionally stay simple:

- simple record ingestion
- simple `record-v1` schema
- Git-based development storage
- minimal QR payloads

These constraints are deliberate to keep verification flows understandable and auditable while the foundation is still evolving.

## What Should Not Be Overengineered Yet

The project should **not** build the following yet (planned/future only):

- decentralized consensus
- high-throughput streaming systems
- automated dispute arbitration
- dynamic ML-based trust weighting

Avoiding these now helps prevent premature complexity before core data integrity and verification interfaces are fully stabilized.

## Future-Proof Architecture Decisions

The architecture should remain modular so future upgrades are possible without disrupting existing records.

Planned/future design directions:

- clear separation between record creation, canonicalization, hashing, and signatures
- clear separation between integrity, provenance, and trust interpretation
- future RFC 8785 JSON canonicalization alignment
- future client-side verification capabilities

## v0.2 Priorities (Planned)

- RFC 8785 canonical JSON research and implementation planning
- partitioned records directory layout design
- witness signature array design (see [Experimental Signed Witness Record Format](./signed-witness-format.md))
- client-side verification prototype

## v0.3 Priorities (Planned)

- revocation/dispute certificate model
- storage decoupling research
- trust matrix formalization
- scalable record indexing plan

## Scope Reminder

All items in this roadmap are planned/future work.

They are explicitly not implemented production behavior in the current HC:// TRUST LAYER version.
