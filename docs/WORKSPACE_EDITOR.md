# Working workspace editor

NOVA now has a real file-writing module that does not need a language model.

It can create or replace text files, including Python code, within a project
workspace chosen by the operator. Existing files get a `.nova-backup`
copy. Python files are syntax-checked before writing.

Example on a computer or Python-capable host:

```sh
printf 'print("Hello from NOVA")\n' > replacement.txt
python -m project_nova.edit_cli \
  --workspace ./nova_runtime/workspace \
  --path projects/hello/main.py \
  --content-file replacement.txt
```

The command prints a JSON receipt with the written path, hash and backup
status. This does **not** require PyTorch, Ollama, or an external API key.

This is a functional operator-controlled editor, not an AI that can
understand natural-language change requests by itself. To have NOVA
interpret instructions and decide what to edit, a working language model
must still be connected. It is not exposed through the public website.

Only use a dedicated project workspace. The editor intentionally cannot
write outside the chosen root; that is a reliability boundary rather
than a limit on the kinds of project files it can edit.
