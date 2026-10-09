# Development roadmap

## Implemented foundation
- Private-repo Python package and CLI.
- SQLite journal with JSON export for portability.
- Optional OpenAI-compatible HTTPS model adapter.
- Local editable agent logic, limited note workspace.
- Separate capability broker denying payments, shell and deployments.
- Offline unit tests and GitHub CI.

## Before unattended operation
1. Select a no-cost host and a model service with explicit free usage allowance. Never silently consume paid API credits.
2. Deploy broker as a different user/process/container from the editable agent, with immutable image or read-only mounts and network egress policy.
3. Give the agent no GitHub administrative access, no billing credentials, and no direct deployment keys.
4. Enforce independent budget, request, token, and time quotas at the hosting/network layer.
5. Implement scoped, revocable consent for each private account and record source.
6. Add encrypted backups and documented restore/migration drills.
7. Add human-readable audit logs, pause/kill switch, and rollback.
8. Use staged self-edit proposals with tests in a restricted sandbox; allow only reviewed promotion to live code.
9. Have a qualified reviewer assess legal/privacy obligations for actual use cases and jurisdictions.
10. Add an opt-in contact channel with anti-spam limits before permitting outbound messaging.

## Known limitations
- This code is not continuously running, and has no cloud host yet.
- A language model is not bundled and external APIs may cost money.
- The read-only research helper is not hardened against all network attacks.
- The agent's code can be edited by a repository owner; policy files in the same repo are not inherently tamper-proof.
- No finite rule list can guarantee compliance with every law or prevent all harm.
- No private source data should be added until consent, retention, and deletion controls exist.
