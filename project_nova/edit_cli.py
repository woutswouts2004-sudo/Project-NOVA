"""Command-line interface for NOVA workspace file changes.

Use --content-file to supply full replacement text. No model is required.
"""
import argparse
import json
from pathlib import Path
from .workspace_editor import write_project_file

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--path", required=True)
    parser.add_argument("--content-file", required=True)
    args = parser.parse_args()
    source = Path(args.content_file)
    if not source.is_file() or source.stat().st_size > 200000:
        parser.error("Content file must be a text file under 200 KB")
    content = source.read_text(encoding="utf-8")
    print(json.dumps(write_project_file(args.workspace, args.path, content), indent=2))

if __name__ == "__main__":
    main()
