# LTM Wiki

LTM Wiki is an AI-agent-agnostic long-term memory wiki. It gives agents one
user-owned memory store that is reachable from **every session, project, and
environment** — with **no external runtime**. Pure markdown, driven by skills.

`ltm` means long-term memory.

## What It Does

- Remembers durable context without requiring you to say "save this" every time.
- Recalls relevant memory before answering when prior context matters.
- Keeps memory in user-owned files you can open in any editor.
- Reaches the same store from any session through a global pointer.
- Lets you choose how the store syncs: Git, Obsidian, or none.

## How It Stays Reachable Everywhere

Memory **data** and memory **tooling** are separated and joined by one global
pointer:

```
Global entry points (installed once per agent, load in every session)
  Claude Code : ~/.claude/skills/  +  block in ~/.claude/CLAUDE.md
  Codex       : block in ~/.codex/AGENTS.md
  Generic     : AI_MEMORY.md in the project
        |
        v  reads
Global pointer  ~/.ltm-wiki/config.json   (store path + sync mode)
        |
        v  points to
Memory store (single source of truth)  ~/ltm-wiki | Obsidian vault | fixed path
        synced by Git remote or Obsidian Sync
```

No Python, no per-session install, no `git clone` at runtime. Recall is `grep`;
health checks are a checklist (see `skills/ltm-wiki-maintenance`).

## Storage Backends

- `markdown-files` (default): portable plain markdown, synced via Git.
- `obsidian`: wikilinks, graph view, Dataview-friendly metadata, synced via
  Obsidian Sync / iCloud.

## Setup

### Install once

- **Claude Code** — add the marketplace, then install the plugin:
  ```
  /plugin marketplace add devy1540/ltm-wiki
  /plugin install ltm-wiki@ltm-wiki
  ```
  Or copy `skills/` into `~/.claude/skills/`.
- **Codex** — install as a Codex plugin, or add the block from
  `entrypoints/codex/AGENTS.block.md` to `~/.codex/AGENTS.md`.

### Run setup

Trigger setup from your agent:

- Codex: `$ltm-setup`
- Claude: `/ltm-setup`
- Generic AI: `ltm-setup`

Natural-language requests work too:

- "ltm-wiki 초기셋팅하고 싶어"
- "장기기억 저장소 만들어줘"
- "Obsidian으로 AI memory 연결해줘"

Setup asks for the store location and sync mode, creates the store, writes the
global pointer, and installs the entry points you want.

## How An Agent Uses It

1. Resolve the store: local `.ltm-wiki/config.json`, else `defaultStore` from
   `~/.ltm-wiki/config.json`.
2. If `sync: git`, pull.
3. Recall (grep `memory/`), answer, capture durable knowledge, append to
   `memory/log.md`.
4. If `sync: git`, commit (push on request).

## Repository Layout

- `skills/` — five skills: `ltm-wiki` (router), `ltm-setup`,
  `ltm-wiki-bootstrap`, `ltm-wiki-recall`, `ltm-wiki-maintenance`.
- `entrypoints/` — global entry-point blocks for Claude, Codex, and generic agents.
- `meta/store-structure.md` — canonical store layout, frontmatter, and seed files.
- `meta/global-config.md` — global pointer specification.
- `meta/conventions.md` — naming, deduplication, indexing, and recall ranking.
- `meta/obsidian-queries.md` — ready-made Dataview views for the vault.
- `meta/migration.md` — schema version migration guide.
- `storage-backends/` — backend conventions and sync notes.
- `hooks/` — optional sync / reminder hooks (not required).
- `.codex-plugin/plugin.json` — Codex plugin manifest.

## Memory Lifecycle

```text
Observe -> Triage -> Store -> Link -> Recall -> Consolidate -> Prune
```

## Safety

LTM Wiki must not store secrets, credentials, private keys, tokens, or content the
user says not to remember.
