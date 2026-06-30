# Markdown Files Backend

The `markdown-files` backend is the baseline LTM Wiki storage backend: portable,
editor-agnostic plain markdown.

## Link Style

Use standard relative markdown links:

```markdown
[Memory Index](../index.md)
```

## Metadata

Use YAML frontmatter on memory pages (full schema: `meta/store-structure.md`):

```yaml
---
type: concept
status: active
created: 2026-05-04
updated: 2026-05-04
sources: []
tags: []
aliases: []
confidence: high
provenance: user-stated
last_reviewed: 2026-05-04
---
```

## Sync

- `sync: git` — the store directory is a git repository with a remote. Pull
  before a session that relies on memory; commit after durable writes; push when
  the user asks.
- `sync: none` — local to one machine. Can be upgraded to git later by adding a
  remote and switching the pointer's `sync` to `git`.

## Required Files

- `.ltm-wiki/config.json`
- `memory/index.md`, `memory/log.md`, `memory/overview.md`
- `meta/schemas/ltm-wiki.md`
