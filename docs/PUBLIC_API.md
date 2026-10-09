# Optional public chat API

The public website can be connected to `project_nova.public_api`, a small
opt-in HTTP API. This is **not deployed** and does not create a model.

Requirements: an authorized server, an already-configured local or hosted
language model, a trusted HTTPS reverse proxy, and operator-managed quotas.

```sh
NOVA_LOCAL_MODEL=your-installed-model NOVA_PUBLIC_CHAT=YES \
NOVA_ALLOWED_ORIGIN=https://woutswouts2004-sudo.github.io \
python -m project_nova.public_api
```

The server binds to localhost by default. A deployment proxy may forward
HTTPS requests to it. Never expose raw HTTP on the internet.

Endpoint: POST /v1/chat, JSON body with `message` and optional `history`.
Success: `{"reply":"...","mode":"model"}`. Failure: an error JSON and HTTP
status. GET /health reports availability. No database or personal messages
are stored by this server.

The rate limiter is **per process and in memory**, not sufficient for a
production public service with multiple replicas, shared NAT addresses,
proxy headers, or hostile traffic. A real deployment needs a proxy-side
rate limiter, abuse protection, model token quotas, moderation, and hard
provider spending caps. No credentials are sent to browsers.

Do not run this on GitHub Pages; Pages only serves static files.
