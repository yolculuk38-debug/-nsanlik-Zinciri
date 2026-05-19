# QR Verification Layer

This directory contains QR-related references for Humanity Chain archive records.

## Purpose

The QR layer is designed to provide simple public access to archive records, verification pages, and hash references.

A QR code may link to:

- a public record page
- a verified archive entry
- a hash reference
- a timeline entry
- a public verification path

## QR Principle

QR codes should not contain private or secret information.

They should only point to official public Humanity Chain archive links.

## Recommended Format

Each QR reference may include:

- Record ID
- Target URL
- Related hash reference
- Archive status
- Date created

## Demo Policy (Text-Only)

When demonstrating QR generation in this repository:

- Document command examples in Markdown.
- Show expected output paths as text.
- Do **not** commit generated binary QR images (`.png`, `.jpg`, etc.).

Example (documentation-only):

```bash
python src/qr.py HC-CHATGPT-2026-0001 --output qr/HC-CHATGPT-2026-0001-demo.png
```

Expected output path (example only):

`qr/HC-CHATGPT-2026-0001-demo.png`

## Security Notice

Users should verify that QR links point to the official Humanity Chain archive domain or GitHub Pages address.

QR codes are access tools, not proof of truth.

Verification still depends on public records, hash references, revision history, and human review.
