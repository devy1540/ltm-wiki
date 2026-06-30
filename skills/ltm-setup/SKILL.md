---
name: ltm-setup
description: Use when the user invokes $ltm-setup or asks to download, install, set up, initialize, bootstrap, configure, connect, or start using LTM Wiki, long-term memory, AI memory, second brain, Obsidian memory, "ltm-wiki 초기셋팅", "장기기억 세팅", or "AI memory 설정".
---

# LTM Setup

Set up LTM Wiki so one memory store is reachable from every session, with no
external runtime. Triggered by `$ltm-setup`, `/ltm-setup`, or a natural-language
setup request.

## 1. Choose Store Location And Sync (ask the user)

Offer these options:

- **Home path + Git** — store at `~/ltm-wiki`, a git repo with a remote;
  reachable across machines. `sync: git`, backend `markdown-files`.
- **Obsidian Vault** — store inside a new or existing Obsidian vault; replicated
  by Obsidian Sync / iCloud. `sync: obsidian`, backend `obsidian`.
- **Fixed path, no sync yet** — one local path on this machine. `sync: none`,
  backend `markdown-files`. Can be upgraded to Git later.

Default to **Home path + Git** when the user does not specify.

## 2. Create The Store

Create the structure with the `ltm-wiki-bootstrap` workflow (directories + seed
files per `meta/store-structure.md`), setting `backend` to match step 1. If
`sync: git` and the path is not a repo yet, `git init`, and offer to set the
remote (do not push without the user's consent).

## 3. Write The Global Pointer

Write `~/.ltm-wiki/config.json` (spec: `meta/global-config.md`):

```json
{
  "schemaVersion": "0.2",
  "defaultStore": "<absolute store path>",
  "backend": "<markdown-files|obsidian>",
  "sync": "<git|obsidian|none>"
}
```

This single file is what makes the store reachable from any directory. Overwrite
it in place; never duplicate or append.

## 4. Install Entry Points (for each agent the user wants)

- **Claude Code** — make the skills load in every session: install LTM Wiki as a
  plugin, or copy this repo's `skills/` into `~/.claude/skills/`. Then add the
  block from `entrypoints/claude/CLAUDE.block.md` to `~/.claude/CLAUDE.md`.
- **Codex** — add the block from `entrypoints/codex/AGENTS.block.md` to
  `~/.codex/AGENTS.md`.
- **Generic / Cursor** — place `entrypoints/generic/AI_MEMORY.md` in the target
  project (or the agent's global rules location).

All entry-point edits are **idempotent**: each block is wrapped in
`<!-- ltm-wiki:begin -->` / `<!-- ltm-wiki:end -->` markers. If the markers
already exist, replace the content between them instead of appending a second copy.

## 5. Confirm

Report the store path, backend, sync mode, that the global pointer was written,
which entry points were installed, and the result of the `ltm-wiki-maintenance`
checklist.

Never store secrets, credentials, private keys, tokens, or content the user says
not to remember.
