# Verification Flow

## Overview

Humanity Chain uses a layered verification workflow designed to improve transparency, traceability, and archival consistency.

This process helps preserve interaction records in a structured and verifiable format.

---

## Basic Verification Process

### Step 1 — Record Creation

An interaction record is created and archived.

Example:

- Human-AI interaction
- Verification event
- Structured observation

Stored in:

records/

---

### Step 2 — Hash Generation

A SHA-256 hash reference may be generated for the archived record.

Purpose:

- Integrity verification
- Tamper detection
- Reference validation

Stored in:

hash/

---

### Step 3 — Timeline Registration

The event is added to the chronological archive timeline.

Purpose:

- Historical traceability
- Event ordering
- Archive continuity

Stored in:

timeline/

---

### Step 4 — QR Reference

Optional QR references may be attached for easier access and verification.
For repository demos, keep this step text-only: document the QR command and expected output path, but do not commit generated PNG/JPG/binary QR files.

Purpose:

- Mobile archive access
- External reference linking
- Simplified verification workflows

Stored in:

qr/

---

### Step 5 — Witness References

Witness references may be attached to support verification context.

Possible witness types:

- Human witness
- AI witness
- External archive
- Independent observer

Stored in:

witness/

---

## Verification Status

Records may include different verification states.

Examples:

- Pending
- Verified
- Archived
- Experimental

---

## Experimental Structure

Humanity Chain is an experimental protocol system.

Verification standards and workflows may evolve over time.
