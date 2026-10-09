"""Adapter for NOVA's locally trained experimental language model."""
from .nova_model import load_checkpoint, sample

class OwnModel:
    def __init__(self, checkpoint, device="cpu", max_tokens=200):
        self.model = load_checkpoint(checkpoint, device=device)
        self.max_tokens = max_tokens
        self.enabled = True

    def respond(self, system, prompt):
        return sample(self.model, system[-400:] + "\n" + prompt[-400:],
                      tokens=self.max_tokens)
