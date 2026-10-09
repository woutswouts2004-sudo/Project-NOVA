"""Deterministic next-byte validation for trusted NOVA checkpoints."""
import argparse
import math
from .nova_model import encode, load_checkpoint, torch_lib
from .train_nova import read_corpus

def evaluate(model, text, *, stride=64):
    torch, _ = torch_lib()
    if not 1 <= stride <= model.config.context:
        raise ValueError("Invalid stride")
    ids = encode(text)
    if len(ids) < model.config.context + 1:
        raise ValueError("Validation text is too short")
    total, count = 0.0, 0
    model.eval()
    with torch.no_grad():
        for offset in range(0, len(ids) - model.config.context, stride):
            window = ids[offset:offset + model.config.context + 1]
            if len(window) != model.config.context + 1:
                continue
            x = torch.tensor([window[:-1]], dtype=torch.long,
                             device=next(model.parameters()).device)
            y = torch.tensor([window[1:]], dtype=torch.long, device=x.device)
            _, loss = model(x, y)
            total += float(loss.item()) * model.config.context
            count += model.config.context
    if count == 0:
        raise ValueError("No evaluation windows")
    average = total / count
    return {"cross_entropy_nats": average,
            "perplexity": math.exp(min(average, 80)),
            "evaluated_bytes": count}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--validation", required=True)
    args = parser.parse_args()
    print(evaluate(load_checkpoint(args.checkpoint), read_corpus(args.validation)))

if __name__ == "__main__":
    main()
