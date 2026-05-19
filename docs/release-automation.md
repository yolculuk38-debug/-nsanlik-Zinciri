# Release Automation Plan

This document describes the current manual release process and a proposed automation plan for **HC:// TRUST LAYER**.

## Scope

- This is a planning document only.
- It does **not** modify workflows in this phase.
- It does **not** create a release.
- It does **not** change schema definitions.

## Current Manual Release Process

Today, releases are prepared manually with the following sequence:

1. Merge the release PR into the default branch.
2. Ensure all required GitHub Actions checks are green.
3. Update `VERSION` and `CHANGELOG` with the intended release information.
4. Create a GitHub Release entry.
5. Tag the version in Git (for example `v0.1.1`) and publish.

This process works, but relies on maintainers to remember each step and keep release metadata consistent.

## Proposed Future Automation

The target state is a guarded release pipeline that automates repeatable validation while keeping human control for publication.

### Planned Automation Controls

- **Auto-generate release notes** from merged PRs and categorized commits.
- **Require changelog updates** before a release can proceed.
- **Verify `VERSION` matches the release tag** (for example, `VERSION=0.2.0` must match tag `v0.2.0`).
- **Block release if validation fails**, including metadata mismatches or missing release notes/changelog requirements.
- **Keep manual approval for final publish**, so a maintainer explicitly confirms the final release action.

### Why Keep Manual Approval

A manual final approval step reduces risk for experimental and trust-critical infrastructure by preserving human review at the publication boundary.

## Release Types

### Patch Release

- Purpose: backward-compatible fixes and documentation/validation improvements.
- Typical version movement: `x.y.Z` (increment patch number).
- Example: `v0.1.0` → `v0.1.1`.

### Minor Release

- Purpose: backward-compatible features and protocol improvements.
- Typical version movement: `x.Y.0` (increment minor number, reset patch).
- Example: `v0.1.3` → `v0.2.0`.

### Experimental Release

- Purpose: publish unstable or trial capabilities for early feedback.
- Typical convention: pre-release tags (for example `v0.3.0-rc.1`, `v0.3.0-beta.1`) or clearly labeled release notes.
- Notes: should explicitly declare constraints, risk level, and migration expectations.

### Security Release

- Purpose: urgent fixes for vulnerabilities or integrity-impacting issues.
- Typical behavior: accelerated review and publication timeline.
- Notes: should include clear remediation notes, impact statement, and upgrade guidance.

## Suggested Implementation Phases

1. Add release validation jobs (dry-run mode first).
2. Enforce changelog and version/tag checks as required gates.
3. Add release note generation.
4. Keep final publish behind maintainer approval.

This phased approach allows validation hardening without disrupting existing manual release operations.
