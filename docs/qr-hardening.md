# HC:// QR Verification Hardening

## Purpose

HC:// QR verification must resist spoofing, tampering, unsafe redirects, and misleading trust assumptions.

A QR scan is not automatic proof.
It is only a transport mechanism for verification metadata.

---

## Security Principles

- QR payloads are untrusted until verified
- Only canonical HC verification URLs are allowed
- Unknown domains must be rejected
- Hash verification is mandatory
- Signature presence must be checked
- Unsafe redirects are forbidden
- Verification results must be explicit

---

## Supported Verification Status

- VERIFIED
- HASH_MISMATCH
- INVALID_QR
- UNSAFE_URL
- UNSIGNED

---

## Required QR Payload Fields

```json
{
  "record_id": "HC-QR-2026-0001",
  "content_hash": "SHA256",
  "verification_url": "https://github.com/...",
  "created_at": "2026-05-21T00:00:00Z",
  "signature": "OPTIONAL"
}
```

---

## Threat Model

This layer is designed to reduce:

- QR spoofing
- malicious redirect abuse
- fake verification pages
- modified payload attacks
- trust confusion
- silent integrity failures

---

## Future Expansion

- Signed QR payloads
- Offline QR verification
- Multi-witness QR consensus
- Hardware-backed signatures
- Time-bound QR verification
