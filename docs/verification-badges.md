# HC:// Verification Result Badges

This document defines a simple verification result badge model for HC:// TRUST LAYER.

## Badge States

### `VERIFIED`
Record verification checks passed for integrity and required verification signals under current HC:// rules.

### `UNVERIFIED`
Record has not completed verification yet, or verification evidence is missing/incomplete.

### `DISPUTED`
Verification outcome is being challenged due to conflicting evidence, review disagreement, or unresolved claims.

### `REVOKED`
A previously issued verification result is withdrawn because it is no longer considered valid.

### `EXPERIMENTAL`
Verification result was produced using an experimental method, workflow, or policy that is not yet stabilized.

## Badge Rendering (Example)

- VERIFIED: `🟢 VERIFIED`
- UNVERIFIED: `⚪ UNVERIFIED`
- DISPUTED: `🟠 DISPUTED`
- REVOKED: `🔴 REVOKED`
- EXPERIMENTAL: `🧪 EXPERIMENTAL`

## Sample Verification Card

```md
Record ID: HC-TEST-2026-0001
Badge: 🟢 VERIFIED
Integrity: PASS
Provenance: AVAILABLE
Witness Review: COMPLETED
Last Updated: 2026-05-20
Notes: Verification checks passed under current HC:// verification flow.
```

Alternative disputed example:

```md
Record ID: HC-TEST-2026-0002
Badge: 🟠 DISPUTED
Integrity: PASS
Provenance: AVAILABLE
Witness Review: CONFLICTING
Last Updated: 2026-05-20
Notes: Technical checks passed, but witness review is under dispute.
```
