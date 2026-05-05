# Markdown Files Backend

The `markdown-files` backend is the baseline LTM Wiki storage backend.

## Link Style

Use standard relative markdown links:

```markdown
[Memory Index](../index.md)
```

## Metadata

Use YAML frontmatter on memory pages:

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

## Required Files

- `.ltm-wiki/config.json`
- `memory/index.md`
- `memory/log.md`
- `memory/overview.md`
- `meta/schemas/ltm-wiki.md`
