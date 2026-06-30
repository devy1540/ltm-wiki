---
name: ltm-wiki
description: Use when working with AI long-term memory, second brains, durable context, memory recall or capture, personal knowledge bases, markdown stores, Obsidian vaults, source notes, decisions, preferences, open questions, wiki maintenance, or conversations where stable knowledge should be remembered without an explicit save request.
---

# LTM Wiki

Use LTM Wiki as explicit user-owned long-term memory for AI agents. There is no
external runtime: read and write markdown directly with your built-in tools.

## Resolve The Store

Find the active store, stopping at the first hit:

1. Local `.ltm-wiki/config.json` in the working directory or a parent.
2. Else `defaultStore` from `~/.ltm-wiki/config.json` (the global pointer).
3. If neither exists:
   - to install, configure, or set up LTM Wiki, use `ltm-setup`.
   - for a bare store with no global wiring, use `ltm-wiki-bootstrap`.

If the resolved config has `sync: git`, pull before relying on memory.

## Orient

Read `.ltm-wiki/config.json`, `memory/index.md`, and recent `memory/log.md` entries.

## Classify The Request

Recall, ingest, ambient capture, maintenance, query, or schema update.

- Targeted recall before answering → `ltm-wiki-recall`.
- Health check, repair, consolidation, or pruning → `ltm-wiki-maintenance`.

## Write Durable Knowledge

Follow `meta/conventions.md` for naming, deduplication, indexing, and recall.

- **Check for duplicates first**: `grep -ril "<topic>" <store>/memory`; update an
  existing page instead of duplicating.
- Name the file with a short kebab-case slug under the matching `memory/<category>/`.
- Write with complete frontmatter and the backend's links (relative for
  `markdown-files`, wikilinks for `obsidian`). Full spec: `meta/store-structure.md`.
- **Update `memory/index.md`**: add a link under the matching area for notable pages.
- Preserve `raw/` unless the user explicitly asks to add or import a source.
- Append meaningful operations to `memory/log.md`.
- If `sync` is `git`, commit after durable writes; push when the user asks.

## Ambient Capture

Capture stable and useful knowledge without requiring the user to say "save this"
when it is low-risk. Ask first for sensitive, personal, ambiguous, or high-volume
writes.

**Scan content for secrets before writing** — API keys, tokens, passwords,
private keys, connection strings (`AKIA…`, `sk-…`, `-----BEGIN … KEY-----`, etc.).
Redact or omit any match. Never store secrets, credentials, or content the user
says not to remember.
