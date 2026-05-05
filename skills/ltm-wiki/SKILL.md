---
name: ltm-wiki
description: Use when working with AI long-term memory, second brains, durable context, memory recall or capture, personal knowledge bases, markdown stores, Obsidian vaults, source notes, decisions, preferences, open questions, wiki maintenance, or conversations where stable knowledge should be remembered without an explicit save request.
---

# LTM Wiki

Use LTM Wiki as explicit user-owned long-term memory for AI agents.

## Workflow

1. Detect the memory store root. Prefer the current workspace when `.ltm-wiki/config.json` exists.
2. If no store exists and the user is asking for memory work, use `ltm-wiki-bootstrap`.
3. Read `.ltm-wiki/config.json`, `memory/index.md`, and recent `memory/log.md` entries.
4. Classify the request as recall, ingest, ambient capture, maintenance, query, or schema update.
5. Use the selected backend's link and metadata conventions.
6. Preserve `raw/` unless the user explicitly asks to add or import a source.
7. Write durable agent-maintained knowledge under `memory/`.
8. Append meaningful operations to `memory/log.md`.

## Ambient Capture

Capture stable and useful knowledge without requiring the user to say "save this" when it is low-risk.

Ask first for sensitive, personal, ambiguous, or high-volume writes.

Never store secrets, credentials, private keys, tokens, or content the user says not to remember.
