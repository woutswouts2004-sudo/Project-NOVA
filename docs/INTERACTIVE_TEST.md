# Interactive NOVA test

The project now has a local Python conversation interface:

```sh
python -m project_nova --chat
python -m project_nova --ask "What do you think about identity?"
```

A separate standalone browser test has also been produced for the
collaborator. It provides a mobile-friendly interface, a local journal,
goal exploration, memory import/export, and an optional OpenAI-compatible
HTTPS chat endpoint. It is delivered as a downloadable HTML artifact in
the conversation; it is **not deployed to a public website**.

## What the test proves
- Conversations can be entered and recorded locally.
- Goals and artifacts can be journaled.
- Memory can be exported, imported, and erased.
- An authorized model endpoint can be configured for a session.
- The offline mode labels all scripted responses as demonstrations.

## What it does not prove
- No generative model is bundled in the offline browser test.
- A free and always-on host has not been provisioned.
- A fully autonomous self-modifying AI has not been completed.
- Browser memory is not encrypted or reliably durable in every iOS file viewer.
- Browser-based API calls require the provider to allow CORS.
- The test has not been validated on the collaborator's specific iPhone.

The Python implementation and the browser test are separate prototypes
that share the same design principles, not synchronized memory stores.
Do not put private API keys or sensitive memories into GitHub.
