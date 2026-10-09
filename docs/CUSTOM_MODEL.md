# NOVA's custom language model

The repository now contains an **original implementation of a small byte-level causal Transformer**, with causal attention, token and position embeddings, feed-forward blocks, weight tying, a next-token loss, checkpointing, and sampling. It implements standard Transformer concepts. **No trained weights are bundled**, and it is not a production-quality conversational model.

To experiment on a machine with PyTorch installed:

```bash
python -m pip install torch
python -m project_nova.train_nova --corpus approved_original_text.txt --manifest approved_manifest.json --output nova.pt --steps 100
```

Use only original, public-domain, or appropriately licensed and consented text. Do not train on private chats or visitors' conversations without permission. The bounded demo trainer requires 512 bytes to 5 MB of UTF-8 text. Its outputs will initially be low quality. A competitive custom foundation model needs substantially more data, compute, evaluation, and safety work.

To sample:

```python
from project_nova.nova_model import load_checkpoint, sample
model = load_checkpoint("nova.pt")
print(sample(model, "Once upon a time", tokens=100))
```

To use the checkpoint in the agent loop, set `NOVA_OWN_CHECKPOINT` to the file path, then run `python -m project_nova.project_runner --steps 2`. Keep checkpoints and training data outside public source control.

Next research tasks: held-out validation, perplexity, licensed datasets, reproducibility, larger models, evaluation, and model cards.

The trainer now requires a provenance manifest, described in [Training Data](TRAINING_DATA.md). The manifest is a declaration by the operator, not cryptographic proof of data ownership.
