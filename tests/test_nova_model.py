import tempfile
import unittest
from pathlib import Path
from project_nova.nova_model import BOS, EOS, Config, encode, decode
from project_nova.train_nova import read_corpus

class NovaModelTests(unittest.TestCase):
    def test_utf8(self):
        for text in ("Hello NOVA", "🎨 世界", "", "line\nbreak"):
            self.assertEqual(decode(encode(text)), text)
    def test_special_tokens(self):
        self.assertEqual(encode("a", bos=True, eos=True), [BOS, 97, EOS])
    def test_config(self):
        Config().validate()
        for config in (Config(width=127), Config(heads=0), Config(context=4)):
            with self.assertRaises(ValueError):
                config.validate()
    def test_corpus_limits(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "approved.txt"
            path.write_text("short")
            with self.assertRaises(ValueError):
                read_corpus(path)
            path.write_text("Original text " * 60)
            self.assertIn("Original", read_corpus(path))
    def test_torch_forward(self):
        try:
            import torch
        except ImportError:
            self.skipTest("Optional PyTorch not installed")
        from project_nova.nova_model import build_model, VOCAB
        model = build_model(Config(context=16, width=32, heads=4, layers=1, dropout=0))
        x = torch.randint(0, 256, (2, 16))
        logits, loss = model(x, x)
        self.assertEqual(tuple(logits.shape), (2, 16, VOCAB))
        self.assertTrue(torch.isfinite(loss).item())
