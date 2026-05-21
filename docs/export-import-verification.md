# Export / Import Verification (Core)

HC:// export/import verification creates a portable JSON package for verified records and audit snapshots.

## Export

`src/export_package.py` builds a package with:

- `package_id`
- `created_at`
- `protocol_version`
- `source_repo`
- `records_count`
- `snapshot_count`
- `records`
- `snapshots`
- `package_hash`

`package_hash` is SHA-256 over canonical JSON content excluding `package_hash` itself.

## Import Verification

`src/import_verify.py` validates required fields, recalculates `package_hash`, verifies record `content_hash` when `content` exists, and validates snapshot structures.

Imported data is treated as untrusted and never written into repository record stores.

## CLI Usage

```bash
python src/export_package.py --output exports/verification-package.json
python src/import_verify.py exports/verification-package.json
```

Non-zero exit code indicates verification failure.
