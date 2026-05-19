# Experimental Signed Witness Record Format

> Status: **Documentation-only / Planned for v0.2**
>
> Witness signatures are planned for **v0.2**. This page defines a proposed experimental structure for discussion and implementation planning.

## Purpose

This document describes a potential witness signature representation that can be attached to witness data in future protocol iterations.

It is intended to support:

- stronger witness attribution
- tamper-evidence for witness statements
- clearer audit and verification workflows

## Experimental Witness Signature Structure

A witness signature entry is expected to include:

- `witness_id`
- `witness_type`
- `public_key`
- `signature`
- `signed_hash`
- `timestamp`
- `verification_method`

### Field Notes

- `witness_id`: stable identifier for the witness entity producing the signature
- `witness_type`: witness category (for example `human`, `ai`, or `system`)
- `public_key`: witness public key material or reference
- `signature`: signature generated over a defined canonical payload/hash
- `signed_hash`: hash value that the signature attests to
- `timestamp`: signing timestamp in machine-readable format
- `verification_method`: method/algorithm descriptor used for signature verification

## Minimal JSON Example

```json
{
  "witness_id": "witness:human:maintainer-01",
  "witness_type": "human",
  "public_key": "ed25519:9f8c2a...",
  "signature": "base64:MEUCIQDn...",
  "signed_hash": "sha256:3f786850e387550fdab836ed7e6dc881de23001b",
  "timestamp": "2026-05-19T00:00:00Z",
  "verification_method": "ed25519-sha256"
}
```

## Implementation Status

This specification is **documentation only** at this time.

It is **not active cryptographic enforcement** in the current version, and does not change current validation behavior, record schema structure, or workflow requirements.
