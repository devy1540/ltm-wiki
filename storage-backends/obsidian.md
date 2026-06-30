# Obsidian Backend

The `obsidian` backend stores LTM Wiki memory as Obsidian-compatible markdown. The
store is a normal vault — open `<store>` directly in Obsidian.

## Link Style

Use Obsidian wikilinks for internal memory references:

```markdown
[[index]]
[[memory/concepts/Long Term Memory]]
```

Use relative markdown links for raw source files and assets.

## Metadata

Use YAML frontmatter compatible with Dataview (full schema: `meta/store-structure.md`):

```yaml
---
type: preference
status: active
created: 2026-05-04
updated: 2026-05-04
sources: []
tags:
  - ltm
aliases: []
confidence: high
provenance: user-stated
last_reviewed: 2026-05-04
---
```

## Recommended Vault Settings

- Set the attachment folder to `raw/assets`.
- Use graph view to review memory clusters and orphan pages.
- Install the Dataview plugin and use the ready-made views in
  `meta/obsidian-queries.md` (active-by-type, open loops, needs-review, stale).
- Daily notes: jot quick captures in the daily note, then promote the durable
  ones into `memory/<category>/` with full frontmatter (see `meta/conventions.md`).

## Sync

`sync: obsidian` — replication is handled by Obsidian Sync, iCloud, or your chosen
mechanism. No git actions are required.

## Human Review

Use Obsidian graph view to inspect hubs, orphan memories, and dense research clusters.
