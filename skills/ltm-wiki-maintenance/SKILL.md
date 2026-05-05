---
name: ltm-wiki-maintenance
description: Use when checking, repairing, consolidating, pruning, or auditing an LTM Wiki memory store for orphan memories, broken links, stale claims, missing metadata, contradictions, and index or log problems.
---

# LTM Wiki Maintenance

Keep the memory store healthy.

## Workflow

1. Run `python3 scripts/memory_doctor.py <root>`.
2. Inspect reported issues before editing.
3. Repair links, metadata, index entries, stale summaries, and backend config issues when requested.
4. Consolidate noisy episodic memory into semantic, procedural, preference, open-loop, or synthesis pages.
5. Append maintenance operations to `memory/log.md`.
