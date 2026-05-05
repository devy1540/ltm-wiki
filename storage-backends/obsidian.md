# Obsidian Backend

The `obsidian` backend stores LTM Wiki memory as Obsidian-compatible markdown.

## Link Style

Use Obsidian wikilinks for internal memory references:

```markdown
[[index]]
[[memory/concepts/Long Term Memory]]
```

Use relative markdown links for raw source files and assets.

## Metadata

Use YAML frontmatter compatible with Dataview:

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

## Human Review

Use Obsidian graph view to inspect hubs, orphan memories, and dense research clusters.
