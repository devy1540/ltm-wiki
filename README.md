# LTM Wiki

LTM Wiki is an AI-agent-agnostic long-term memory wiki. It gives agents an explicit, user-owned memory store for durable knowledge from conversations, sources, decisions, preferences, procedures, and open questions.

`ltm` means long-term memory.

## What It Does

- Remembers durable context without requiring the user to say "save this" every time.
- Recalls relevant memory before answering when prior context matters.
- Stores memory in user-owned files.
- Supports multiple storage backends.
- Ships with a Codex plugin adapter plus Claude and generic AI instruction templates.

## Storage Backends

- `markdown-files`: default portable backend.
- `obsidian`: markdown backend optimized for Obsidian wikilinks, graph view, and Dataview-friendly metadata.

## Initialize A Store

```bash
python3 scripts/init_store.py ./my-memory --backend markdown-files --store-name "My Memory"
python3 scripts/memory_doctor.py ./my-memory
python3 scripts/search_memory.py ./my-memory "project preference"
```

## Codex Plugin

The repository root contains `.codex-plugin/plugin.json` and `skills/`, so it can be installed as a Codex plugin.

## Agent Instructions

- Codex: `templates/AGENTS.ltm-wiki.md`
- Claude: `templates/CLAUDE.ltm-wiki.md`
- Generic: `templates/AI_MEMORY.md`

## Memory Lifecycle

```text
Observe -> Triage -> Store -> Link -> Recall -> Consolidate -> Prune
```

## Safety

LTM Wiki should not store secrets, credentials, private keys, tokens, or content the user says not to remember.
