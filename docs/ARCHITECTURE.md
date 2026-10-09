# Project NOVA architecture

**Public site:** `docs/index.html`, hosted by GitHub Pages. Static,
readable by anyone, no server secrets.

**Public chat service (not deployed):** `project_nova/public_api.py`.
Explicit opt-in, bounded inputs, no internal journal, server-side model
connection, localhost by default.

**Private agent runtime (not deployed):** `project_nova/agent.py`,
`memory.py`, `autonomy.py`, `broker.py`. Holds an independent journal
and workspace. Must not share admin credentials with the public service.

**Model adapters:** `llm.py` for an authorized HTTPS provider,
`local_model.py` for local Ollama. Model is replaceable.

**Unattended public work:** GitHub Actions generates deterministic study
prompts and publishes them to `docs/field-notes`. No model inference.

**Independent guardrails (future deployment):** enforce privileges with
separate accounts and processes. Python code within one repository is not
a tamper-proof boundary.
