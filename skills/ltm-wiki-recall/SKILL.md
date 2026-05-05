---
name: ltm-wiki-recall
description: Use when the user asks to remember, recall, use previous context, continue a thread, apply preferences, revisit decisions, or answer a question where long-term memory may affect the response.
---

# LTM Wiki Recall

Recall targeted long-term memory before answering.

## Workflow

1. Read `.ltm-wiki/config.json`.
2. Read `memory/index.md` and recent `memory/log.md`.
3. Search targeted memory with `python3 scripts/search_memory.py <root> "<query>"`.
4. Open the smallest useful set of memory pages.
5. Distinguish current conversation context from recalled memory.
6. Mention recalled memory only when it materially affects the response or transparency is useful.
7. Update memory when the conversation resolves or changes durable context.
