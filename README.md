# HC:// TRUST LAYER

[![Humanity Chain Validation](../../actions/workflows/validate.yml/badge.svg)](../../actions/workflows/validate.yml) [![CodeQL](../../actions/workflows/codeql.yml/badge.svg)](../../actions/workflows/codeql.yml)

> The visible architecture of digital trust.

## What Is HC:// TRUST LAYER

HC:// TRUST LAYER is an experimental verification and provenance infrastructure for digital content in the AI era.

It provides open, auditable records so people can check whether content is consistent across time, sources, and distribution channels.

## Why It Exists

Digital content is easier to create, remix, and manipulate at scale. Synthetic media, altered documents, and context loss can make trust decisions harder.

HC:// TRUST LAYER exists to make verification workflows transparent instead of relying on unsupported claims.

## Core Verification Concept

HC:// TRUST LAYER focuses on verifiable records, not narrative authority.

A record can be checked by comparing:

- record identifier
- content hash
- validation status
- witness and provenance context

Verification is reproducible: anyone using the same input and rules should reach the same technical result.

## Verification Example

Sample verification values:

- sample record id: `HC-EXAMPLE-2026-0001`
- sample hash: `9f3a3fb4f7c21ab3a89d4f7db0bf75db6ea9cc57f398a7db53f4a62f5a4d8d57`
- sample validation result: `PASS (schema + hash)`

## Quick Start

```bash
pip install -r requirements.txt
python src/validator.py examples
python src/hash.py examples/ai_witness_example.json
# Demo: text-only QR verification path example (do not commit generated image files)
python src/qr.py HC-CHATGPT-2026-0001 --output qr/HC-CHATGPT-2026-0001-demo.png
# Example output path only: qr/HC-CHATGPT-2026-0001-demo.png
```

## Documentation And Examples

- docs: [`docs/`](docs/)
- QR verification: [`docs/qr-verification.md`](docs/qr-verification.md)
- Witness layer: [`docs/witness-layer.md`](docs/witness-layer.md)
- Trust scoring: [`docs/trust-scoring.md`](docs/trust-scoring.md)
- Limitations and risks: [`docs/limitations-and-risks.md`](docs/limitations-and-risks.md)
- Record format: [`docs/record-format.md`](docs/record-format.md)
- Architecture roadmap (planned): [`docs/architecture-roadmap.md`](docs/architecture-roadmap.md)
- examples: [`examples/`](examples/)
- AI witness example: [`examples/ai_witness_example.json`](examples/ai_witness_example.json)

## Project Context

HC:// TRUST LAYER is the primary name for this repository.

Humanity Chain may appear as historical project context only.
