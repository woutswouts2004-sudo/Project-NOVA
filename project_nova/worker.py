"""NOVA worker process for Docker Compose.

The public chat API and autonomous worker run as separate processes,
using the same optional Ollama server but no shared privileged API.
"""
from .daemon import main

if __name__ == "__main__":
    main()
