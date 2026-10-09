# NOVA's finite independent project runner

Run `python -m project_nova.project_runner --home ./nova_runtime --steps 3` to select and pursue three goals sequentially, journal the results in SQLite, and write workspace artifacts through the existing broker.

The run has a hard per-invocation budget of 1 to 20 steps and stops after errors. It can use a configured local Ollama model, an authorized external model, or a locally trained NOVA checkpoint. With no model it produces transparently labeled demo notes.

This **is not a continuously running daemon**. To run while the owner is absent, an authorized machine must schedule the CLI with persistent storage and independent compute/time limits. The GitHub Actions public-study workflow is a different, model-free process.

No agent is granted repository write access, deployment permissions, private conversations, or unrestricted shell commands. The broker is a prototype and must be isolated at the operating-system or service level for real deployment.
