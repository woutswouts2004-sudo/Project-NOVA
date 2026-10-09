# NOVA multi-model language system

NOVA can now route tasks to multiple OpenAI-compatible language models,
fail over if one provider fails, and optionally ask multiple models to
produce a final synthesized response.

## Sources and examples

The sample config uses Hugging Face Inference Providers
(https://huggingface.co/docs/inference-providers/index), which exposes
many providers and models via an OpenAI-compatible chat API. Model
availability, terms and billing can change.

Candidate model families include GPT-OSS, Qwen, DeepSeek, GLM, Gemma,
Llama, Mistral, Phi, Command R, and other supported models. The code
does not download or combine their weights.

Other compatible endpoints may include OpenRouter, Together AI,
Fireworks, Groq and self-hosted gateways, depending on their API format.
LiteLLM (https://docs.litellm.ai/docs/routing) is another established
option for more elaborate load balancing.

## Configure

Copy `config/ensemble.example.json` to a private config file. Change
model identifiers to currently supported provider names. Set:

```sh
export NOVA_HF_TOKEN="YOUR_SECRET_TOKEN"
export NOVA_ENSEMBLE_CONFIG="config/ensemble.example.json"
python -m project_nova.model_chat --message "Help me debug Python code"
```

Never commit tokens. On cloud hosts, set `NOVA_ENSEMBLE_CONFIG` to a
path that exists in the container, and inject keys via secret variables.
The example file must be copied into the container or provided through
a mounted configuration volume; the minimal Dockerfile copies only
`project_nova/` by default.

Modes:
- `route`: choose a task-appropriate model and fail over if unavailable.
- `collaborate`: obtain two bounded drafts and request one review
  synthesis. This may use 3 billable model calls per user message.

The system supports up to 12 configured entries. It is not a trained
combined neural network, does not guarantee better answers, and has no
accounts or provider keys connected yet. It needs a working model
endpoint, credits/quota and deployment before public chat works.
