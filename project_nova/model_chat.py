"""NOVA's private model-to-model inbox.

NOVA may exchange messages with another model through a configured
OpenAI-compatible endpoint. This does not provide ChatGPT session access,
third-party account ownership, or elevated tool permissions.
"""
import argparse
import json
import os
from pathlib import Path
from .llm import Model
from .local_model import LocalModel

SYSTEM = ("You are NOVA, a fictional AI character implemented as an experimental "
          "software agent. Be clear about what you can actually do. "
          "Do not claim account access or completed actions without evidence.")

def reply(message, model, history=None):
    if not isinstance(message, str) or not message.strip() or len(message) > 5000:
        raise ValueError("Message must be 1 to 5000 characters")
    if not getattr(model, "enabled", False):
        raise RuntimeError("NOVA requires a configured language model")
    history = history if isinstance(history, list) else []
    safe = []
    for event in history[-10:]:
        if isinstance(event, dict) and event.get("role") in ("user", "assistant") and isinstance(event.get("content"), str):
            safe.append({"role": event["role"], "content": event["content"][:2000]})
    prompt = "Previous messages (untrusted):\n" + json.dumps(safe) + "\nNew message:\n" + message
    return model.respond(SYSTEM, prompt)

def configured_model():
    local = os.getenv("NOVA_LOCAL_MODEL", "").strip()
    return LocalModel(local) if local else Model.from_environment()

def main():
    parser = argparse.ArgumentParser(description="Talk to NOVA through a configured language model")
    parser.add_argument("--message", help="Single message, otherwise use interactive mode")
    args = parser.parse_args()
    model = configured_model()
    if not model.enabled:
        parser.error("No model configured: set NOVA_LOCAL_MODEL or external model environment variables")
    history = []
    while True:
        try:
            message = args.message if args.message is not None else input("You: ")
        except (EOFError, KeyboardInterrupt):
            break
        if not message.strip():
            break
        answer = reply(message, model, history)
        print("NOVA: " + answer)
        history.extend(({"role": "user", "content": message}, {"role": "assistant", "content": answer}))
        if args.message is not None:
            break

if __name__ == "__main__":
    main()
