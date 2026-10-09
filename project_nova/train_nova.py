"""Bounded local trainer for NOVA's own experimental Transformer."""
import argparse
from pathlib import Path
from .nova_model import Config, encode, build_model, save_checkpoint, torch_lib
from .dataset_manifest import load_manifest

def read_corpus(path):
    path = Path(path)
    if not path.is_file() or path.stat().st_size > 5_000_000:
        raise ValueError("Corpus must be a UTF-8 file smaller than 5 MB")
    text = path.read_text(encoding="utf-8")
    if len(text.encode("utf-8")) < 512:
        raise ValueError("At least 512 UTF-8 bytes are required")
    return text

def train(corpus, output, steps=100, batch_size=8, seed=7, config=None, manifest=None):
    if not manifest:
        raise ValueError('Training requires an approved dataset manifest')
    load_manifest(manifest)
    torch, _ = torch_lib()
    config = (config or Config()).validate()
    if not (1 <= steps <= 100000 and 1 <= batch_size <= 64):
        raise ValueError("Training budget outside allowed range")
    data = torch.tensor(encode(read_corpus(corpus)), dtype=torch.long)
    if len(data) < config.context + 2:
        raise ValueError("Corpus too short for context")
    torch.manual_seed(seed)
    model = build_model(config)
    model.train()
    opt = torch.optim.AdamW(model.parameters(), lr=0.0003)
    for step in range(steps):
        starts = torch.randint(0, len(data) - config.context - 1, (batch_size,))
        offsets = torch.arange(config.context)
        x = data[starts[:, None] + offsets]
        y = data[starts[:, None] + offsets + 1]
        _, loss = model(x, y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        if step == 0 or (step + 1) % 10 == 0:
            print("step={} loss={:.4f}".format(step + 1, loss.item()))
    model.eval()
    save_checkpoint(model, output, steps=steps)
    return output

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--corpus", required=True)
    p.add_argument("--manifest", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--steps", type=int, default=100)
    p.add_argument("--batch-size", type=int, default=8)
    p.add_argument("--context", type=int, default=128)
    args = p.parse_args()
    train(args.corpus, args.output, steps=args.steps, batch_size=args.batch_size,
          config=Config(context=args.context), manifest=args.manifest)

if __name__ == "__main__":
    main()
