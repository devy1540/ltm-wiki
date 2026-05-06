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

## Download And Setup

```bash
git clone https://github.com/devy1540/ltm-wiki.git
cd ltm-wiki
python3 scripts/setup.py ./my-memory --agent codex --backend markdown-files --store-name "My Memory"
```

For all agent instruction templates:

```bash
python3 scripts/setup.py ./my-memory --agent all --backend markdown-files --store-name "My Memory"
```

For Obsidian:

```bash
python3 scripts/setup.py /path/to/obsidian-vault --agent all --backend obsidian --store-name "My Memory"
```

The setup command initializes the memory store, installs agent instruction entry points, and runs the memory doctor.

## Agent Commands

- Codex: `$ltm-setup`
- Claude: `/ltm-setup`
- Generic AI: `ltm-setup`

Natural-language setup requests should work too, for example:

- "ltm-wiki 초기셋팅하고 싶어"
- "장기기억 저장소 만들어줘"
- "Obsidian으로 AI memory 연결해줘"

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
- Shared setup command: `templates/commands/ltm-setup.md`

## Memory Lifecycle

```text
Observe -> Triage -> Store -> Link -> Recall -> Consolidate -> Prune
```

## Safety

LTM Wiki should not store secrets, credentials, private keys, tokens, or content the user says not to remember.
