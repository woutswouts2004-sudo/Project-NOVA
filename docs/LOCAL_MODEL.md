# Use a local open-weight language model (no cloud API account)

Project NOVA can use a locally running Ollama model. This is an
alternative to a Groq account, not a requirement to create one.

## Prerequisites
A computer or authorized server capable of running a language model,
Ollama installed by its owner, sufficient memory and disk space, and a
model whose license permits the intended use.

See https://ollama.com/ for installation instructions. Models differ
substantially in their resource requirements, capabilities and licenses.

## Basic setup
Install Ollama on your own machine, select a suitable open-weight model,
and download it using the documented Ollama command. For example, if a
compatible model is installed locally under the name `gemma3:1b`:

```sh
NOVA_LOCAL_MODEL=gemma3:1b python -m project_nova --chat
```

Or use:
```sh
NOVA_LOCAL_MODEL=gemma3:1b python -m project_nova --once
```

The model adapter only connects to `127.0.0.1:11434`. It cannot connect
to remote Ollama hosts. No account, API key or cloud inference charge is
required for a locally installed model, but hardware and electricity are
not necessarily free. This configuration does not automatically install
Ollama or download weights.

## Limitations
A tiny local model may be less capable than a large hosted model.
The iPhone-only workflow cannot use this localhost adapter without an
actual compatible runtime on the iPhone; localhost always refers to the
device running the Python process. A remote server is a separate
deployment and must be authorized.

The model's weights are not copied into this repository. Its memory,
identity and policy components remain separately portable.
