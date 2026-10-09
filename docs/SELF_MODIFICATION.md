# Self-modification without privilege escalation

The proposed architecture has two separate trust domains.

**Agent domain:** Can reason about its goals, write notes, draft replacement
source code for editable modules, run in a restricted workspace, and request
a deployment. It cannot write its own credentials, policy broker, sandbox
settings, payment permissions, deployment scripts or owner-controlled logs.

**Control domain:** A separate service identity controls the deployed broker,
secrets, budgets, allowed network destinations, tests and rollback. The agent
cannot authenticate as this identity.

Current implementation: `project_nova/proposals.py` accepts draft Python
source for agent modules, syntax-checks it without executing it, and saves a
candidate plus metadata in the workspace. It does **not** automatically
deploy changes. This is deliberate: a passing syntax check is not evidence
that a change is safe or lawful.

Future implementation: A separately administered promotion service can
compare changes against an allowlist, run sandboxed tests, perform security
checks, enforce quotas, retain a known-good release, and promote eligible
changes. Changes to policy or infrastructure always require independent
authorization. Do not let an agent edit the tests or promotion rules that
decide whether its own changes are approved.

This cannot guarantee perfect safety. It does provide meaningful separation
between creative self-modification and the power to override guardrails.
