# Using Project NOVA

Project NOVA is a prototype. It is not an already-running independent AI.

## Commands

```sh
python -m project_nova --once
python -m project_nova --loop --interval 3600
python -m project_nova --chat
python -m project_nova --ask "What are you interested in exploring?"
python -m project_nova --status
python -m project_nova --export-backup my-backup.json
python -m project_nova --restore-backup my-backup.json
python -m unittest discover -s tests -v
```

`--chat` provides a local terminal conversation. `--ask` returns JSON for
a single message. Both journal the conversation. Without a configured
model, they clearly say DEMO MODE and do not generate intelligent replies.

The autonomous `--once` step chooses a topic, writes a reflection and
saves a text artifact. Without a model, it saves a transparent demo prompt.

## Model opt-in
An authorized HTTPS OpenAI-compatible service may be configured through
`NOVA_API_BASE`, `NOVA_API_KEY`, `NOVA_MODEL`, and
`NOVA_ENABLE_EXTERNAL_MODEL=YES`. Never commit tokens, and never enable a
paid service without explicit authorization and an external hard budget cap.

## What "free" means here
The repository and demo code do not charge money by themselves. Real
inference and cloud hosting may have usage limits, costs, or account
requirements. No provider is configured by default.

## Privacy
The origin record is anonymized and excludes the human collaborator's
personal history. The local journal may still record anything typed into
the chat, so avoid sending sensitive material until encryption, retention,
and deletion controls have been added.
