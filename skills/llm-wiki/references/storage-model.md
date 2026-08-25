# LLM Wiki Storage Model

This is the canonical storage and claim-evidence contract for the skills-first MVP.

## Directory Layout

```text
<Obsidian Vault>/
  LLM Wiki/
    projects/
      <project-key>/        # one isolated project root
        .llm-wiki.json      # resolver-owned project identity marker
        sources/
          imported/         # immutable content-addressed source snapshots
        wiki/
          schema.md
          index.md
          operations.md
          source-notes/
          topics/
          syntheses/
```

Inside a resolved project root, the logical contract remains:

```text
<project-root>/
  .llm-wiki.json
  sources/                  # user-owned local sources and imported snapshots
    imported/
  wiki/
    schema.md               # local rules and supported formats
    index.md                # human-readable navigation entry point
    operations.md           # append-only record of completed writes
    source-notes/           # one note per ingested source
    topics/                 # accumulated entities, concepts, and relationships
    syntheses/              # approved comparisons and conclusions
```

The project root is isolated even though multiple roots share one Obsidian Vault.
The machine-global resolver chooses a root; it is not a global memory store. Never
search sibling projects. Indexes or caches added in the future must be fully
rebuildable from this project's `sources/` and `wiki/` and must not become the
source of truth.

## File Names

Use short lowercase kebab-case slugs. A source note should normally reuse the
source filename without its extension. Search titles, aliases, source paths, and
claim IDs before choosing a new slug.

## Page Frontmatter

Every source note, topic, and synthesis starts with:

```yaml
---
title: Retry policy
type: topic
---
```

Valid `type` values are `source-note`, `topic`, and `synthesis`.

A source note also requires:

```yaml
source_path: sources/retry-spec.md
source_digest: sha256:<hex-digest>
```

An immutable imported snapshot also requires its logical identity:

```yaml
source_id: <24-hex-id>
source_path: sources/imported/<source-id>/<digest>/<safe-basename>
source_digest: sha256:<hex-digest>
```

Paths are relative to the wiki root. Compute SHA-256 with an available native
command such as `sha256sum` or `shasum -a 256`.

## Source Path Boundary

Only user-selected files inside `<root>/sources/` are valid evidence.

For `source_path` frontmatter, reject absolute paths and any `..` segment, and
require the path to begin with `sources/`.

Evidence links are relative to their wiki page and normally contain `../` segments
to reach the root `sources/` directory. Reject absolute evidence targets, then
canonicalize both `<root>/sources/` and the resolved evidence target. Require the
canonical target to be a regular file inside the canonical sources directory.
Reject symlink escapes and non-file targets.

Do not read a rejected target. Report it as an untrusted or invalid evidence path
during query and lint.

An external file crosses the boundary only through the bundled importer after the
user explicitly selects it as durable evidence. The verified snapshot—not the
external path—becomes the source of truth for later ingest and query. Never write
the external absolute path or raw project remote into the Vault.

Do not add timestamps, authors, UUIDs, confidence scores, or tags unless a concrete
domain need is agreed later. Git and `operations.md` record change history.

## Claim Blocks

Use claim blocks for important facts and derived conclusions that future queries,
updates, or contradictions may depend on.

Claim ownership is strict:

- `source-note` pages summarize only their own source and link each important
  source assertion to the corresponding claim in a topic page. They do not own
  reconciled claim blocks and must not gain evidence from another source.
- `topic` pages own reconciled `sourced` claim blocks. A topic claim may accumulate
  evidence from several source notes and is where conflict or supersession state is
  represented.
- `synthesis` pages own user-approved `derived` claim blocks.

```markdown
<a id="claim-transport-default-protocol"></a>
### Claim: transport-default-protocol

- **Kind:** sourced
- **State:** current
- **Statement:** The default transport is HTTP.
- **Evidence:**
  - **Source:** [Architecture v1](../../sources/architecture-v1.md)
  - **Locator:** heading "Transport", lines 12-16
```

Required fields:

- Stable ID: unique lowercase kebab-case ID, prefixed by the topic when useful.
- `Kind`: `sourced` or `derived`.
- `State`: `current`, `disputed`, `superseded`, or `stale`.
- `Statement`: one independently reviewable assertion.
- `Evidence`: at least one source link and precise locator for a sourced claim.

Add these relations only when applicable:

- `Contradicts`
- `Supersedes`
- `Superseded by`
- `Derived from`

Relations use ordinary Markdown links to explicit claim anchors. A derived claim
must link to the input claims and retain links to the underlying sources.

Locator conventions:

- Markdown or text: section heading and line range.
- PDF: page number and section when available.
- Audio or video: timestamp range.
- Code: commit or revision, path, and line range.

The source digest determines whether locators need revalidation after a source
changes.

## Reconciliation Rules

- Same logical `source_id` (or legacy source path) and same digest: do not create a new page or claim. Record a
  no-op only when the user requested ingest and the result is meaningful.
- Same conclusion with additional evidence: add the new source and locator to the
  existing topic claim. Keep each source note limited to its own source.
- Conflicting evidence: preserve both claims, mark both `disputed`, and add mutual
  `Contradicts` links in the relevant topic page.
- Explicit supersession in a source or a user-approved resolution: keep the selected
  claim `current`, mark the older claim `superseded`, and add both relation links.
- A derived claim depending on a disputed or superseded claim becomes `stale` until
  reviewed.

### Same Logical Source, Changed Digest

When a source note has the same imported `source_id` or legacy `source_path` but a
different digest:

1. Treat it as a new immutable snapshot of one logical source, not as an unrelated
   source. Never delete the older snapshot.
2. Find every topic and synthesis evidence entry that points to the prior snapshot.
3. Re-read the replacement and revalidate every old locator and assertion.
4. Remove evidence no longer supported by the replacement. Preserve the prior
   digest and locator under `Former evidence` in the affected claim and in the
   operation entry.
5. If a sourced claim loses all current evidence, keep the claim visible but mark
   it `stale`. If other evidence still supports it, retain the appropriate state.
6. Mark every derived claim that depends on newly stale, disputed, or superseded
   input as `stale`.
7. Rewrite the source note in place with the same `source_id`, new project-relative
   snapshot path, current assertions, and new digest. Do not create a second source
   note.
8. Re-evaluate contradiction and supersession relations; do not infer a new winner
   merely from the changed file.

The operation log records `source_id`, old digest, new digest, removed evidence,
and every claim whose state changed. It never records the external origin path.

Do not choose a winner merely because a source is newer. Recency is evidence, not
automatic authority.

## Navigation And Operations

`index.md` links to every source note, topic, and synthesis with a one-line
description. It is curated navigation, not a generated database dump.

A source note contains a concise source-only summary followed by a list of its
important assertions. Each assertion includes the locator in that source and links
to the topic claim that reconciles it with other evidence.

Append completed writes to `operations.md` using:

```markdown
## YYYY-MM-DD | ingest | sources/architecture-v2.md

- Created: wiki/source-notes/architecture-v2.md
- Updated: wiki/topics/transport.md
- Result: reconciled one superseding claim
```

Use `setup`, `ingest`, `crystallize`, or `repair` as the operation. Never log a
query or read-only lint pass as a write operation.

## Write Boundaries

- With `autoProvision=true`, resolver activation may create only the project marker,
  empty `sources/imported/`, Wiki directories, seed files, and one setup operation.
  This authorization comes from installation/configuration and does not include
  source ingestion or conversation capture.
- An explicit ingest request authorizes updates derived from the named source.
- Query is read-only.
- Crystallize writes only after an explicit request or approval of the proposed
  page and scope.
- Lint is read-only; repair requires approval of the findings and affected files.

Except for automatic skeleton creation and immutable snapshots produced by the
importer, managed content writes stay under `wiki/`. The skill never edits or
deletes original external files or prior snapshots.
Show the resulting diff or changed-file summary and leave version-control actions
to the user unless asked.
