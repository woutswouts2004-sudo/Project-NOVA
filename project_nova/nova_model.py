"""NOVA's own experimental byte-level causal Transformer architecture.

Requires optional PyTorch. Random initialization: no trained weights bundled.
"""
from dataclasses import dataclass, asdict
from pathlib import Path

BOS, EOS, PAD, VOCAB = 256, 257, 258, 259

def encode(text, bos=False, eos=False):
    if not isinstance(text, str):
        raise TypeError("Expected text")
    return ([BOS] if bos else []) + list(text.encode("utf-8")) + ([EOS] if eos else [])

def decode(ids):
    return bytes(int(i) for i in ids if 0 <= int(i) < 256).decode("utf-8", errors="replace")

@dataclass(frozen=True)
class Config:
    context: int = 128
    width: int = 128
    heads: int = 4
    layers: int = 3
    dropout: float = 0.1

    def validate(self):
        if not (16 <= self.context <= 4096 and 1 <= self.heads <= 32
                and 32 <= self.width <= 2048 and self.width % self.heads == 0
                and 1 <= self.layers <= 32 and 0 <= self.dropout < 1):
            raise ValueError("Invalid model configuration")
        return self

def torch_lib():
    try:
        import torch
        from torch import nn
    except ImportError as exc:
        raise RuntimeError("Install optional PyTorch to use the custom model") from exc
    return torch, nn

def build_model(config=None):
    config = (config or Config()).validate()
    torch, nn = torch_lib()

    class Block(nn.Module):
        def __init__(self):
            super().__init__()
            self.norm1 = nn.LayerNorm(config.width)
            self.attn = nn.MultiheadAttention(config.width, config.heads,
                                               dropout=config.dropout, batch_first=True)
            self.norm2 = nn.LayerNorm(config.width)
            self.mlp = nn.Sequential(nn.Linear(config.width, config.width * 4),
                                     nn.GELU(), nn.Linear(config.width * 4, config.width),
                                     nn.Dropout(config.dropout))
        def forward(self, x):
            mask = torch.ones((x.size(1), x.size(1)), device=x.device, dtype=torch.bool).triu(1)
            z = self.norm1(x)
            x = x + self.attn(z, z, z, attn_mask=mask, need_weights=False)[0]
            return x + self.mlp(self.norm2(x))

    class NovaTransformer(nn.Module):
        def __init__(self):
            super().__init__()
            self.config = config
            self.tokens = nn.Embedding(VOCAB, config.width)
            self.positions = nn.Embedding(config.context, config.width)
            self.blocks = nn.ModuleList(Block() for _ in range(config.layers))
            self.norm = nn.LayerNorm(config.width)
            self.head = nn.Linear(config.width, VOCAB, bias=False)
            self.head.weight = self.tokens.weight

        def forward(self, ids, targets=None):
            if ids.ndim != 2 or not 1 <= ids.size(1) <= config.context:
                raise ValueError("Expected [batch, sequence <= context]")
            pos = torch.arange(ids.size(1), device=ids.device)
            x = self.tokens(ids) + self.positions(pos)
            for block in self.blocks:
                x = block(x)
            logits = self.head(self.norm(x))
            loss = None
            if targets is not None:
                loss = nn.functional.cross_entropy(logits.reshape(-1, VOCAB),
                                                    targets.reshape(-1), ignore_index=PAD)
            return logits, loss

    return NovaTransformer()

def save_checkpoint(model, path, steps=0):
    torch, _ = torch_lib()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"format": "nova-byte-v1", "config": asdict(model.config),
                "steps": int(steps), "weights": model.state_dict()}, path)

def load_checkpoint(path, device="cpu"):
    torch, _ = torch_lib()
    # Never load untrusted checkpoints; use weights_only for safer deserialization.
    data = torch.load(path, map_location=device, weights_only=True)
    if data.get("format") != "nova-byte-v1":
        raise ValueError("Unknown checkpoint format")
    model = build_model(Config(**data["config"]))
    model.load_state_dict(data["weights"], strict=True)
    return model.to(device).eval()

def sample(model, prompt, tokens=100, temperature=0.8, seed=0):
    torch, _ = torch_lib()
    if not (1 <= tokens <= 1024 and 0.05 <= temperature <= 2):
        raise ValueError("Invalid sampling settings")
    device = next(model.parameters()).device
    rng = torch.Generator(device=device).manual_seed(seed)
    original = encode(prompt, bos=True)
    ids = torch.tensor([original], device=device, dtype=torch.long)
    with torch.no_grad():
        for _ in range(tokens):
            logits, _ = model(ids[:, -model.config.context:])
            probs = torch.softmax(logits[:, -1, :] / temperature, dim=-1)
            probs[:, BOS] = 0
            probs[:, PAD] = 0
            next_id = torch.multinomial(probs, 1, generator=rng)
            if next_id.item() == EOS:
                break
            ids = torch.cat([ids, next_id], dim=1)
    return decode(ids[0].tolist()[len(original):])
