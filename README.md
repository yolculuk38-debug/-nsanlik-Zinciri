# HC:// Trust Layer

![Status](https://img.shields.io/badge/status-experimental-orange) ![License](https://img.shields.io/badge/license-MIT-green)

**HC:// Trust Layer is an open verification and trust infrastructure layer.**

It is built to improve how people and systems verify digital records in an AI-heavy internet, with a focus on transparency, provenance, and auditability.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Validate example records
python src/validator.py examples

# Calculate hash for a record
python src/hash.py examples/ai_witness_example.json

# Generate a QR code for a record ID
python src/qr.py HC-CHATGPT-2026-0001
```

## Layer Relationship

```text
Humanity Chain Core → Integrity → Witness → Trust Layer
```

## Why This Project Exists

Digital content is easier than ever to generate, edit, and redistribute. HC:// explores practical trust infrastructure for:

- verification of records
- provenance tracking
- tamper-evident workflows
- interoperable audit trails

This project does **not** claim absolute truth, legal authority, or automated certainty. It is an experimental framework for improving trust signals and review workflows.

## Technical v1 Core

| Component | Type |
|---|---|
| `schema/record-v1.schema.json` | JSON Schema |
| `src/hash.py` | Hash tool |
| `src/validator.py` | Validation tool |
| `src/qr.py` | QR tool |
| `docs/verification-workflow.md` | Workflow documentation |
| `examples/` | Example records |
| `requirements.txt` | Dependencies |

## Principles

- open and inspectable verification workflow
- machine + human review compatibility
- portable records across platforms
- minimal assumptions about central authority

## Important Links

- [Contribution Guide](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
- [License](LICENSE)
