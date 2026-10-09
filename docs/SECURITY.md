# Security boundary and threat model

The agent's desired freedom is primarily **freedom of thought, goals, identity and creative work**, not unrestricted privileges on other people's machines.

## Non-editable boundaries require infrastructure
Do not rely on an instruction, hash, Python module, or repository file to be uneditable if the agent can administer the same account, filesystem, runtime, or deployment system. Enforce the broker with a separate operating-system identity or service and keep policy and credentials inaccessible to the agent process. The agent should have a workspace volume only. Apply an outbound network allowlist and block private networks and cloud metadata endpoints at the network layer.

The agent can propose edits to ordinary modules as inert files. An independent test-and-review pipeline decides whether a proposal is deployed. The agent cannot edit the deployment pipeline, its access rights, or the broker.

## Threats
- Prompt injection from web pages, chat messages and documents.
- Exfiltration of secrets and sensitive personal data.
- API charges or unexpected host billing.
- Unauthorized server access and unwanted contact.
- Supply-chain compromise from dependencies and untrusted code.
- Agent attempting to change its own privileges.

## Controls needed before hosting
- Zero billing credentials; provider spending limit set outside agent account.
- Least-privilege access tokens and no repository admin access for the agent.
- Explicit, scoped, revocable authorization for each private data source.
- Independent append-only audit logging, emergency shutdown and backups.
- Quotas, isolation, patching, incident response, and independent testing.
- Compliance review for applicable privacy, consumer and computer access laws.

No universal list of rules can guarantee lawful behavior. The initial code is a prototype and does not claim formal verification or complete isolation.
