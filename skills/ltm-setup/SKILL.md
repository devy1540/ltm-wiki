---
name: ltm-setup
description: Use when the user invokes $ltm-setup or asks to download, install, set up, initialize, bootstrap, configure, connect, or start using LTM Wiki, long-term memory, AI memory, second brain, Obsidian memory, "ltm-wiki 초기셋팅", "장기기억 세팅", or "AI memory 설정".
---

# LTM Setup

Set up LTM Wiki from either `$ltm-setup` or a natural-language setup request.

## Workflow

1. Choose the memory root:
   - Use the current workspace by default.
   - Use an Obsidian vault when the user asks for Obsidian.
2. Choose backend:
   - Use `markdown-files` by default.
   - Use `obsidian` for Obsidian contexts.
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
python3 "$LTM_WIKI_HOME/scripts/setup.py" <memory-root> --agent codex --backend <backend> --store-name "LTM Wiki"
```

Use `--agent all` when the user wants Codex, Claude, and generic AI instructions installed together.

5. Confirm the memory root, backend, installed files, and `doctor=ok`.

Never store secrets, credentials, private keys, tokens, or content the user says not to remember.
