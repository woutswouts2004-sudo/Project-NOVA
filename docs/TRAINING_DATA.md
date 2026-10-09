# NOVA training-data requirements

Training a custom language model is not permission to reuse other people's private information.

Before any model-training run, maintain a dataset manifest with:
- `source`: a non-empty description of the original source
- `license`: `ORIGINAL-OWNED`, `PUBLIC-DOMAIN`, `CC0-1.0`, or `CC-BY-4.0`
- `permission_confirmed`: `true`
- `contains_private_chats`: `false`
- `visitor_consent_required`: `false`

The validator is `project_nova.dataset_manifest.validate_manifest`. It is an
administrative check, not proof that the actual data has been lawfully sourced.
No user conversations or website visitor messages have been imported.

Keep training text and checkpoints out of the public GitHub repository. Evaluate
on a held-out authorized corpus rather than reporting training loss alone.
