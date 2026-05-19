# Contributing to Humanity Chain

Thank you for contributing to Humanity Chain.

This project focuses on transparent archival systems, verification workflows, and documented human-AI interaction research.

---

## Contribution Principles

All contributions should aim to support:

- Transparency
- Traceability
- Verification
- Open documentation
- Constructive collaboration

---

## Record Standards

When submitting a new interaction record:

- Use clear and consistent formatting.
- Include date references when possible.
- Avoid manipulated or unverifiable content.
- Preserve the original context of responses.
- Do not modify archived responses after verification.

---

## File Naming

Recommended naming format:

HC-[MODEL]-[YEAR]-[NUMBER].md

Example:

HC-CHATGPT-2026-0002.md

---

## Verification Process

Records may include:

- SHA-256 hash references
- QR verification links
- Timeline references
- Witness references
- Archive metadata

---

## Conduct

Contributors are expected to follow the Humanity Chain Code of Conduct.

Respectful, evidence-based, and transparent collaboration is required.

---

## Experimental Status

Humanity Chain is an experimental research protocol.

Structures, workflows, and standards may evolve over time.

---

## Pull Request Merge Policy (Security-First)

Humanity Chain uses a **security-first default** for pull requests:

- PRs are treated as **manual-review required** unless they are clearly documentation-only.
- PRs that touch code, schemas, automation/workflows, source, or tooling paths are labeled `manual-review` and must be reviewed by a maintainer before merge.

### Docs-Only Auto-Merge

Documentation-only pull requests are eligible for automatic merge:

- Eligible PRs are labeled `docs-auto`.
- Auto-merge is enabled only after GitHub required checks pass.
- Merge method is squash merge.

### Manual Review Triggers

Any PR that changes sensitive or executable surfaces is labeled `manual-review`, including but not limited to:

- `src/`
- `schema/`
- `.github/workflows/`
- `SECURITY.md`
- `CODEOWNERS`
- dependency/runtime files (`requirements.txt`, `package.json`, `pnpm-lock.yaml`)

If a PR includes both documentation changes and protected-path changes, `manual-review` takes precedence and the PR must not be auto-merged.

If there is uncertainty, the policy defaults to `manual-review`.
