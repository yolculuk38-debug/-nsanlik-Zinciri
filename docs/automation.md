# CI Automation Flow

When a pull request is opened, GitHub Actions starts the validation workflow.

The workflow installs dependencies from `requirements.txt`, validates records against the schema, and verifies content hashes.

CodeQL security scans also run.

A pull request can be merged only after all required checks pass.
