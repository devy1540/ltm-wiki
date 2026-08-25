# Lint And Repair Workflow

Lint is read-only. Separate mechanical and semantic findings.

Run all checks inside the one resolved `projectRoot`. Do not lint sibling project
Wikis or the rest of the Obsidian Vault.

## Mechanical Checks

- Required directories and `schema.md`, `index.md`, and `operations.md` exist.
- `.llm-wiki.json`, when present, matches the resolved project key and identity.
- Every managed page has valid `title` and `type` frontmatter.
- Source notes have a valid `source_path` and SHA-256 `source_digest`.
- Imported source notes have a valid `source_id` and a content-addressed path whose
  digest directory matches the snapshot bytes.
- `source_path` values are relative, begin with `sources/`, and contain no parent
  traversal. Evidence paths may traverse from a wiki page to the root, but must
  resolve canonically to regular files inside `sources/`. Absolute targets and
  canonical or symlink escapes are findings and must not be read.
- Source paths, Markdown links, claim anchors, and evidence locators resolve.
- Claim IDs are unique.
- Index entries do not point to missing pages and managed pages are discoverable.

## Semantic Checks

- Important sourced claims have evidence that actually supports the statement.
- Duplicate topic pages or meaningfully duplicate claims are identified.
- Contradictory claims have explicit state and mutual links.
- Superseded or disputed inputs propagate `stale` to dependent derived claims.
- Syntheses distinguish facts, conclusions, disagreements, and missing evidence.
- Sources changed since their recorded digest are flagged for re-ingest.
- Replaced sources have no removed evidence left as `current`, and dependent
  derived claims are marked `stale` when required.

## Report

Give every finding a stable ID, severity, affected page or claim, rule, evidence,
and proposed repair. Report `mechanical` and `semantic` sections separately.

Do not modify anything during lint. If the user approves specific finding IDs,
apply only that scope, append one `repair` entry to `operations.md`, and show a
reviewable diff.
