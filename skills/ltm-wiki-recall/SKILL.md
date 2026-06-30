---
name: ltm-wiki-recall
description: Use when the user asks to remember, recall, use previous context, continue a thread, apply preferences, revisit decisions, or answer a question where long-term memory may affect the response.
---

# LTM Wiki Recall

Recall targeted long-term memory before answering. No script — search with your
built-in grep tools.

## Workflow

1. Resolve the store: local `.ltm-wiki/config.json`, else `defaultStore` from
   `~/.ltm-wiki/config.json`. If `sync: git`, pull first.
2. Read `memory/index.md` and recent `memory/log.md` entries.
3. Search targeted memory, narrowing by frontmatter first (full ranking in
   `meta/conventions.md`):
   - Filter by type when known: `grep -rl "type: preference" <store>/memory`
   - Then search terms inside: `grep -rin "<term>" <store>/memory`
   - Or one pass: `rg -n "<term1>|<term2>" <store>/memory` (when ripgrep is available)

   Rank by status (`active` first), type/tag match, confidence, then recency.
   Open the smallest useful set.
4. Distinguish current conversation context from recalled memory.
5. Mention recalled memory only when it materially affects the response or
   transparency is useful.
6. Update memory when the conversation resolves or changes durable context, then
   append to `memory/log.md`.
