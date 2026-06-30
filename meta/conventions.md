# LTM Wiki Conventions

Operational conventions for naming, deduplication, indexing, and recall ranking.
These keep the store navigable as memory grows. Skills reference this file.

## File Naming (Slugs)

- One memory per file under the matching `memory/<category>/` folder.
- File name: a short, stable kebab-case slug derived from the title, e.g.
  `prefers-obsidian-vault.md`. The human-readable title goes in the `# Heading`
  and `aliases`.
- For the `obsidian` backend the slug is also the wikilink target, so avoid
  spaces and keep it unique across the store.

## Deduplication (before writing)

Before creating a new page, check for an existing one on the same topic:

```bash
grep -ril "<key phrase or alias>" <store>/memory
```

- If a close match exists, **update** it (refine the body, bump `updated` /
  `last_reviewed`) instead of creating a duplicate.
- Create a new page only when the topic is genuinely distinct.
- Prefer consolidating several episodic notes into one semantic / preference page.

## Index Maintenance

`memory/index.md` lists the areas. When you add a notable page, add a bullet link
under the matching area so it stays discoverable:

- markdown-files: `- [Title](preferences/prefers-obsidian-vault.md)`
- obsidian: `- [[prefers-obsidian-vault]]`

Keep `index.md` curated (hubs and notable pages), not an exhaustive dump — the
folder itself is the full list.

## Recall Ranking

When recalling, prefer pages in this order:

1. **Status** — `active` first; skip `archived` unless explicitly asked.
2. **Type / tag match** — narrow by frontmatter first, e.g.
   `grep -rl "type: preference" <store>/memory`, then search within.
3. **Confidence** — `high` over `medium` / `low` when they conflict.
4. **Recency** — newer `updated` / `last_reviewed`, and recent `memory/log.md`
   entries, win ties.

Open the smallest useful set; cite a memory only when it materially affects the
answer.

## Associative Recall (1 hop)

After the first-pass hits, expand once along relationships to catch related memory
that keyword search alone misses:

- **Links** — open pages referenced by `[[wikilinks]]` in the top hits, and pages
  that link back to them.
- **Tags** — pull siblings sharing a tag: `grep -ril "<tag>" <store>/memory`.
- Stop at one hop; rank the expanded set the same way and keep only what helps.

## Curation Policy

Keep stored memory trustworthy as it ages:

- **Confidence decay** — an `active` page left unreviewed past its horizon loses
  one confidence step and is flagged for re-confirmation. Suggested: `high`→`medium`
  after ~180 days, `medium`→`low` after ~180 more. Re-confirming resets
  `last_reviewed` and restores confidence.
- **Contradictions** — two `active` pages on the same topic must not assert
  opposite facts. On conflict, surface both, keep the user-confirmed one, and
  `archive` (not delete) the other.
- **Consolidation** — prefer one durable page over many episodic notes (see the
  maintenance skill's Consolidation steps).
