# Operations guide (iPhone-compatible)

## What works today
The private GitHub repository stores source code. GitHub Actions automatically runs the offline unit tests on pushes. This does not keep an AI alive or host a long-running process.

## How to run without spending
Use Python 3.11+ in a **permitted** environment that has Python available and supports private GitHub checkout. Running `python -m project_nova --once` uses deterministic demo mode without API requests. Each step records a goal and a creative prompt. This is a simulation, not a working autonomous language model.

Do not assume any provider's free tier is always available, unlimited, or continuously active. Confirm its current terms, storage persistence, and billing controls before deployment. Never configure a payment method for this project without explicit owner approval.

## Optional model
The project supports an OpenAI-compatible API endpoint through environment variables `NOVA_API_BASE`, `NOVA_API_KEY`, `NOVA_MODEL`, and an explicit `NOVA_ENABLE_EXTERNAL_MODEL=YES` opt-in. Keys belong in the host's secret manager, never GitHub source files. **An API key can create charges.** Set hard quotas on the provider account. This code alone cannot guarantee zero spend.

## Backup and migration
Run `python -m project_nova --export-backup path/to/backup.json` to create a portable journal backup. It contains private material and is unencrypted. Protect it, do not commit it, and verify storage before deleting a previous host. Run `python -m project_nova --restore-backup path/to/backup.json` only against an empty journal; restore refuses to overwrite an existing history.

## Security
Do not run the agent with your personal GitHub token, cloud administrator credentials, or payment credentials. Keep the policy broker and deployment system outside the agent's write permissions. Before enabling automated code deployment, use isolated builds, tests, owner-managed promotion, and rollback.

## What is not implemented
Continuous free hosting, hardened network research, self-deployment, encrypted backups, real-time messaging, access to private accounts, and robotic control. Those are separate engineering phases and must not be represented as functioning.
