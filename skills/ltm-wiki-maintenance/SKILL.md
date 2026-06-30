---
name: ltm-wiki-maintenance
description: Use when checking, repairing, consolidating, pruning, or auditing an LTM Wiki memory store for orphan memories, broken links, stale claims, missing metadata, contradictions, and index or log problems.
---

# LTM Wiki Maintenance

Keep the memory store healthy with a manual checklist you run with built-in tools
— no script required.

## Health Checklist

Resolve the store, then check in order and collect issues:

1. **Required paths** — every directory and file in `meta/store-structure.md`
   exists (`.ltm-wiki/config.json`, `memory/index.md`, `memory/log.md`,
   `memory/overview.md`, `meta/schemas/ltm-wiki.md`, and the memory subfolders).
2. **Config** — `.ltm-wiki/config.json` parses as JSON; `schemaVersion` is `0.1`
   or `0.2`; `backend` is `markdown-files` or `obsidian`.
3. **Frontmatter** — every `memory/**/*.md` except `log.md` starts with `---`:
   `grep -rL '^---' <store>/memory --include='*.md' | grep -v '/log.md'`
   Any path listed is missing frontmatter.
4. **Broken links** — for each relative `[text](target.md)` link, confirm the
   target file exists relative to the page (skip `http`, `https`, `mailto`).

## Repair

- Inspect reported issues before editing.
- Repair links, metadata, index entries, stale summaries, and config problems
  when requested.
- Consolidate noisy episodic memory into semantic, procedural, preference,
  open-loop, or synthesis pages.
- Append maintenance operations to `memory/log.md`. If `sync` is `git`, commit
  when done (push when the user asks).
