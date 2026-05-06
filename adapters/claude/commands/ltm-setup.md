# /ltm-setup

Use this command when the user invokes `/ltm-setup` or asks in natural language to set up LTM Wiki, long-term memory, AI memory, second brain memory, Obsidian memory, or says phrases such as "ltm-wiki 초기셋팅", "장기기억 세팅", or "AI memory 설정".

## Workflow

1. Choose the memory root:
   - Use the current workspace by default.
   - Use the user's Obsidian vault when they ask for Obsidian.
2. Choose backend:
   - Use `markdown-files` by default.
   - Use `obsidian` when the user asks for Obsidian or is working in an Obsidian vault.
3. Locate, download, or update LTM Wiki:

```bash
if [ -f scripts/setup.py ]; then
  LTM_WIKI_HOME="$(pwd)"
else
  LTM_WIKI_HOME="${LTM_WIKI_HOME:-$HOME/.local/share/ltm-wiki}"
  if [ -d "$LTM_WIKI_HOME/.git" ]; then
    git -C "$LTM_WIKI_HOME" pull --ff-only
  else
    git clone https://github.com/devy1540/ltm-wiki.git "$LTM_WIKI_HOME"
  fi
fi
```

4. Run setup:

```bash
python3 "$LTM_WIKI_HOME/scripts/setup.py" . --agent claude --backend markdown-files --store-name "LTM Wiki"
```

For Obsidian:

```bash
python3 "$LTM_WIKI_HOME/scripts/setup.py" /path/to/vault --agent claude --backend obsidian --store-name "LTM Wiki"
```

5. Report the memory root, backend, installed instruction files, and doctor result.

Do not store secrets, credentials, private keys, tokens, or content the user says not to remember.
