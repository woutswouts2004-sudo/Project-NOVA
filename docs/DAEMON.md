# NOVA persistent worker

The worker provides a durable local task inbox and scheduled self-directed
exploration. It is a real Python process, not a GitHub Pages feature.

## Start

First configure a working model with `NOVA_LOCAL_MODEL`, or the external
model environment variables described in `docs/CONNECT_BACKEND.md`.

```sh
python -m project_nova.daemon --home ./nova_runtime --interval 3600
```

Queue a request from another terminal:

```sh
python -m project_nova.daemon --home ./nova_runtime --submit "Explore a new memory architecture"
python -m project_nova.daemon --home ./nova_runtime --status
```

For one cycle and exit:

```sh
python -m project_nova.daemon --home ./nova_runtime --once
```

The worker processes one queued request per cycle. When there is no
request it independently chooses an exploration goal, asks the configured
model for a reflection and attempts to write a workspace note through
the existing Broker permission policy.

The inbox and journal are stored as SQLite files under `--home`. Keep
this directory on persistent private storage; otherwise container
restarts may erase it.

The worker does not execute arbitrary commands, create accounts, send
email, or modify privileged source code. A deployment host, working
model, and correctly configured workspace permissions are required.
It does not guarantee uninterrupted operation on free hosting.

The current worker uses the runner's local or single external model
selection. The ensemble can be used by the public chat and model_chat
entry points separately.
