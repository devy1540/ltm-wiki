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
5. **Metadata sanity** — `confidence` is `high`/`medium`/`low`; `provenance` is
   `user-stated`/`inferred`/`source-backed`/`system-generated`; `type` is a valid
   memory type.
6. **Secret scan** — grep for credential-like patterns and redact any hits:
   `grep -rinE '(AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{20,}|BEGIN [A-Z ]*PRIVATE KEY|password[[:space:]]*[:=])' <store>/memory`
7. **Stale review** — flag pages whose `last_reviewed` is long past, and
   low-confidence `open-loop` pages, for review, consolidation, or archiving.

## Repair

- Inspect reported issues before editing.
- Repair links, metadata, index entries, stale summaries, and config problems
  when requested.
- Consolidate noisy episodic memory into semantic, procedural, preference,
  open-loop, or synthesis pages.
- **Archive** superseded or long-stale pages by setting `status: archived`
  (recall skips archived unless explicitly asked) instead of deleting, to
  preserve provenance.
- Append maintenance operations to `memory/log.md`. If `sync` is `git`, commit
  when done (push when the user asks).

## Curation

Keep memory trustworthy as it ages (policy: `meta/conventions.md` → Curation Policy):

- **Confidence decay** — lower the confidence of `active` pages left unreviewed
  past their horizon (high→medium ~180d, medium→low ~180d more) and flag them for
  re-confirmation. Re-confirming resets `last_reviewed`.
- **Contradictions** — if two active pages on the same topic disagree, surface
  both, keep the user-confirmed one, and archive the other.

## Consolidation

Periodically fold raw episodic notes into durable pages:

1. Group episodic notes on the same topic.
2. Write or update one semantic / preference / procedure / synthesis page with the
   durable conclusion, citing the episodes in `sources`.
3. Archive the now-redundant episodic notes (`status: archived`).
4. Log the consolidation in `memory/log.md`.
