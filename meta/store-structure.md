# LTM Wiki Store Structure

This is the canonical specification for a memory store. Any agent can create or
repair a store by following it directly — no scripts required. Create directories
with `mkdir -p` and write each seed file with the contents below. Replace
`<TODAY>` with today's date in `YYYY-MM-DD` form and `<STORE_NAME>` with the
store name.

## Directory Layout

```
<store>/
  .ltm-wiki/config.json          # store config (backend, storeName, schemaVersion)
  memory/
    index.md                     # entry index (type: index)
    log.md                       # append-only operation log (type: log)
    overview.md                  # operating notes + policy (type: overview)
    sources/                     # source-backed memory
    episodes/                    # conversation and decision records
    preferences/                 # stable user preferences
    procedures/                  # reusable workflows
    open-loops/                  # questions, hypotheses, unresolved decisions
    entities/                    # people, organizations, projects, objects
    concepts/                    # definitions and durable concepts
    syntheses/                   # cross-source conclusions and theses
    questions/                   # durable answers and explorations
  raw/
    sources/                     # user-owned original sources (do not rewrite)
    assets/                      # attachments and binaries
  meta/
    prompts/                     # reusable prompt snippets
    schemas/ltm-wiki.md          # schema reference (written below)
```

`raw/` is user-owned. Never rewrite or delete its contents unless the user
explicitly asks to add or import a source.

## Frontmatter Schema

Every memory page (except `memory/log.md`) starts with YAML frontmatter:

```yaml
---
type: concept            # one of the memory types below
status: active           # active | archived | draft
created: <TODAY>
updated: <TODAY>
sources: []              # relative paths or URLs backing this memory
tags: []
aliases: []
confidence: high         # high | medium | low
provenance: user-stated  # user-stated | inferred | source-backed | system-generated
last_reviewed: <TODAY>
---
# <Page Title>
```

Required keys: `type, status, created, updated, sources, tags, aliases,
confidence, provenance, last_reviewed`.

Memory types: `source, semantic, episodic, procedural, preference, open-loop,
synthesis, question, entity, concept` (plus structural `index, log, overview`).

## Backend Link Style

- `markdown-files`: relative markdown links, e.g. `[Index](../index.md)`.
- `obsidian`: wikilinks for memory pages, e.g. `[[index]]`; relative links for
  files under `raw/`.

## Seed Files

### `.ltm-wiki/config.json`
```json
{
  "schemaVersion": "0.2",
  "backend": "markdown-files",
  "storeName": "<STORE_NAME>"
}
```
Set `backend` to `obsidian` for Obsidian stores.

### `memory/index.md`
```markdown
---
type: index
status: active
created: <TODAY>
updated: <TODAY>
sources: []
tags: []
aliases: []
confidence: high
provenance: system-generated
last_reviewed: <TODAY>
---
# Memory Index

`<STORE_NAME>` long-term memory index.

## Core Pages

- [Overview](overview.md) - Store overview and operating notes.
- [Log](log.md) - Append-only memory operation log.

## Memory Areas

- [Sources](sources/) - Source-backed memory.
- [Episodes](episodes/) - Conversation and decision records.
- [Preferences](preferences/) - Stable user preferences.
- [Procedures](procedures/) - Reusable workflows.
- [Open Loops](open-loops/) - Questions, hypotheses, and unresolved decisions.
- [Entities](entities/) - People, organizations, projects, and objects.
- [Concepts](concepts/) - Definitions and durable concepts.
- [Syntheses](syntheses/) - Cross-source conclusions and theses.
- [Questions](questions/) - Durable answers and explorations.
```

### `memory/log.md`
`log.md` has no frontmatter. It is an append-only operation log.
```markdown
# Memory Log

## [<TODAY>] bootstrap | Memory store initialized

- Operation: bootstrap
- Result: created initial LTM Wiki memory store structure.
```

### `memory/overview.md`
```markdown
---
type: overview
status: active
created: <TODAY>
updated: <TODAY>
sources: []
tags: []
aliases: []
confidence: high
provenance: system-generated
last_reviewed: <TODAY>
---
# Memory Overview

`<STORE_NAME>` uses the `<BACKEND>` backend.

## Start Here

- [Index](index.md)
- [Log](log.md)

## Policy

- Raw sources are user-owned and should not be rewritten unless explicitly requested.
- Memory pages are agent-maintained and must preserve provenance and confidence.
- Sensitive data, secrets, and credentials are not stored.
```
For the `obsidian` backend, use `[[index]]` and `[[log]]` under "Start Here".

### `meta/schemas/ltm-wiki.md`
```markdown
# LTM Wiki Memory Schema

Backend: `<BACKEND>`

Required memory metadata: type, status, created, updated, sources, tags,
aliases, confidence, provenance, last_reviewed.

Memory types: source, semantic, episodic, procedural, preference, open-loop,
synthesis, question, entity, concept.
```
