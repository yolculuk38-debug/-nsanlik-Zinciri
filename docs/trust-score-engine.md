# HC:// Trust Score Engine

## Purpose

The HC:// trust score engine converts multiple verification signals into a structured trust indicator.

Trust scores are not absolute truth.
They are transparent, auditable heuristic signals.

---

## Verification Signals

Current inputs may include:

- verified hashes
- QR verification
- signed verification records
- audit snapshots
- export/import verification
- multi-witness consensus
- witness participation
- conflict detection
- unsafe verification flags

---

## Trust Levels

| Score | Level |
|---|---|
| 85–100 | HIGH |
| 60–84 | MODERATE |
| 35–59 | LOW |
| 0–34 | UNTRUSTED |

---

## Security Principles

- Scores must remain deterministic
- Inputs must remain auditable
- Unsafe signals reduce trust
- Conflicts reduce trust
- Duplicate witness amplification must be prevented
- Trust scores are advisory, not authority

---

## Threat Model

Designed to reduce:

- fake trust amplification
- manipulated witness inflation
- weak verification signaling
- unsafe verification reuse
- hidden conflict masking

---

## Future Expansion

- weighted witness trust
- temporal trust decay
- signed witness weighting
- institutional verification tiers
- decentralized federation scoring
