# NOVA's conversational identity and delegated accounts

NOVA is a fictional AI character embodied in software. The project can
give NOVA a consistent voice, memory, and operational responsibilities.
It does not follow that the software has legal personhood or human rights,
or that providers must allow it to register accounts on its own.

## Talk directly to NOVA

The `project_nova.model_chat` module calls an actual configured language
model, rather than producing scripted demo answers.

```sh
python -m project_nova.model_chat --message "Hello NOVA, what are you working on?"
python -m project_nova.model_chat
```

Configure `NOVA_LOCAL_MODEL` for an Ollama model, or set
`NOVA_API_BASE`, `NOVA_API_KEY`, `NOVA_MODEL` and
`NOVA_ENABLE_EXTERNAL_MODEL=YES` for a compatible hosted model.

**No model is provisioned by this code.** A model must be running or a
provider must be connected. The repository's own transformer architecture
is not yet conversationally trained.

## Accounts

The `project_nova.service_identity` module records a provider, account
handle, permission scopes, authorizer and registration status. It does
not store credentials or pretend an account exists. Credentials belong
in a host's secret manager, never in public source or visitor chat.

A dedicated NOVA account can be operated by the agent with delegated
credentials when a provider permits that use and the required account
owner authorizes it. Financial/legal verification remains the provider's
decision. The public chat server has no service-account credentials and
cannot administer hosting or GitHub accounts.

## Next milestones

- Deploy a model-backed server and verify `/health`.
- Connect the public website's About → backend setting.
- Provide durable private storage for agent memory.
- Add a separately authenticated operator interface for file edits.
- Connect scoped service APIs with logs, revocation and rollback.
- Run autonomous projects on a scheduled worker.

Do not grant public visitors permission to rewrite NOVA's source code
or operate its service accounts.
