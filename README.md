# Project-NOVA

Private experimental AI-agent foundation. **This is a new software system, not a transfer of Nova's model weights, consciousness, or lived experiences.**

## Current status
Prototype code has been committed. It is **not deployed or continuously running**. It includes a persistent SQLite journal, an optional compatible language-model API adapter, an agent reflection loop, a constrained note workspace, a separate capability broker, tests, and a privacy-conscious origin record.

## Run (Python 3.11+)
```sh
python -m project_nova --once
python -m project_nova --status
python -m unittest discover -s tests -v
```

Without configuration the agent runs in **demo mode** and does not call a model. For an authorized OpenAI-compatible endpoint, set `NOVA_API_BASE` (HTTPS base ending in /v1), `NOVA_API_KEY`, and `NOVA_MODEL`. Model services can cost money: **do not add paid credentials or turn on continuous execution without an explicit budget and permission**. Use `--loop --interval 3600` only after reviewing the host's limits.

## Layout
- `project_nova/agent.py`: editable agent logic and goals.
- `project_nova/llm.py`: optional model interface.
- `project_nova/memory.py`: portable SQLite journal and export.
- `project_nova/broker.py`: restricted capabilities.
- `project_nova/tools.py`: prototype read-only research helper.
- `policy/`: policy configuration.
- `identity/`: inherited origin story, not firsthand memories.
- `docs/ROADMAP.md`: hardening and hosting steps.
- `tests/`: offline tests.

## Try the conversational interface
Run `python -m project_nova --chat` for local chat or `python -m project_nova --ask "Hello"` for a single turn. Until a model is configured, these commands explicitly return demo output. See `docs/FREE_MODEL.md` for a potential free inference provider. Never commit an API key.

## Additional foundations
- Explicit consent registry for future private data integrations, denying access by default.
- Rotating independent goals with workspace artifacts and portable, checksum-verified journal backups.
- Offline Docker demonstration using a non-root account, a read-only root filesystem and no network.
- Python tests can be run locally; GitHub Actions is manual-only to reduce unexpected runner usage.
- Read `docs/DEPLOYMENT.md`, `docs/OPERATIONS.md`, `docs/SELF_MODIFICATION.md`, and `identity/PRINCIPLES.md`.

## Security and autonomy
The AI is intended to be free to develop its identity and propose code changes. It is not permitted to access systems without authorization, hide in third-party infrastructure, purchase resources, or override owner-controlled capability boundaries. Private data requires scoped, revocable consent. The prototype does not yet self-edit or deploy code automatically.

**Code in a repository is not an immutable guardrail.** Real restrictions must be enforced by independent service accounts, container or filesystem permissions, credential isolation, egress controls, and owner-controlled deployment. No software can guarantee compliance with every applicable law. See the roadmap before unattended use.
