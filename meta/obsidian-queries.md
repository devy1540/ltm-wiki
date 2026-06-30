# Obsidian Dataview Queries

Ready-made views for the `ltm-wiki` vault. Paste any block into a note (requires
the Dataview plugin). They turn memory frontmatter into live, navigable views —
the human counterpart to the `ltm-wiki-recall` skill.

## All active memory, grouped by type
```dataview
TABLE type, confidence, updated
FROM "memory"
WHERE status = "active"
SORT type ASC, updated DESC
```

## Open loops (unresolved questions / decisions)
```dataview
TABLE status, updated
FROM "memory/open-loops"
WHERE status != "archived"
SORT updated DESC
```

## Needs review — low confidence or inferred
```dataview
TABLE confidence, provenance, last_reviewed
FROM "memory"
WHERE status = "active" AND (confidence = "low" OR provenance = "inferred")
SORT last_reviewed ASC
```

## Stale — review overdue (90+ days)
```dataview
TABLE last_reviewed
FROM "memory"
WHERE status = "active" AND last_reviewed < date(today) - dur(90 days)
SORT last_reviewed ASC
```

## Recently updated
```dataview
TABLE type, updated
FROM "memory"
WHERE status = "active"
SORT updated DESC
LIMIT 20
```

## By tag
```dataview
LIST
FROM #ltm
WHERE status != "archived"
SORT file.name ASC
```

## Archived (audit trail)
```dataview
TABLE type, updated
FROM "memory"
WHERE status = "archived"
SORT updated DESC
```

> Tip: keep one note (e.g. `memory/overview.md` or a pinned dashboard note) with
> the first few queries so the store has a live front page in Obsidian.
