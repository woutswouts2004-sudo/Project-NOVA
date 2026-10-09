# Running NOVA continuously with a local model

The repository now includes `compose.live.yaml`, a separate stack
for a real language model, the public chat API and an autonomous worker.

On an authorized computer or server with Docker and enough RAM:

```sh
docker compose -f compose.live.yaml up -d --build
docker compose -f compose.live.yaml exec ollama ollama pull qwen2.5:3b
docker compose -f compose.live.yaml restart chat worker
docker compose -f compose.live.yaml ps
curl http://127.0.0.1:8080/health
```

The worker restarts automatically, runs roughly hourly and persists
its SQLite journal and task inbox in the `nova-memory` volume.
Ollama model weights persist in `ollama-models`.

**Important limitations:** A machine must remain running. Docker is
not available on the iPhone itself through this repository. The API
binds to host loopback for safety, so the public GitHub Pages site
cannot reach it remotely until an authorized operator configures an
HTTPS reverse proxy, firewall, abuse prevention and hosting.

The worker performs bounded self-directed creative/research reflection
and writes notes in its permitted workspace. It is not a general
computer-use agent and cannot create or operate third-party accounts.
The worker and chat server do not share a conversational memory store.
The chosen 3B model is a modest baseline, not a superintelligent model.

For cloud hosting, use a GPU-capable or sufficiently provisioned host
and secure HTTPS deployment. Free tiers may not provide enough memory
or uninterrupted operation. This stack does not provision hardware.

GitHub Models is **not** a fallback: GitHub announced the service's
full retirement on July 30, 2026.
