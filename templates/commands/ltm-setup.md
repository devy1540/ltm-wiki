# ltm-setup

Set up LTM Wiki from a natural-language request or an agent-specific command.

- Codex: `$ltm-setup`
- Claude: `/ltm-setup`
- Generic AI: `ltm-setup`

Download or update the repository, then run:

```bash
python3 scripts/setup.py <memory-root> --agent <codex|claude|generic|all> --backend <markdown-files|obsidian> --store-name "LTM Wiki"
```

Use `markdown-files` by default. Use `obsidian` when the user asks for Obsidian or points at an Obsidian vault.
