# LLM Wiki Agentic Memory Design

## Goal

Build this repository as a GitHub-publishable, AI-agent-agnostic long-term memory system that turns Andrej Karpathy's LLM Wiki pattern into an Obsidian-backed agentic second brain. The larger goal is portable long-term memory for AI agents: durable knowledge should compound across sessions, projects, sources, conversations, and agent runtimes. The project should help agents remember and reuse important context from curated raw sources and from normal conversation, without requiring the user to explicitly type a skill name, command name, or phrases like "save this to the wiki" for common memory moments.

## Source Idea

Karpathy's LLM Wiki pattern has three layers:

- Raw sources: immutable files curated by the user.
- Wiki: generated and maintained markdown pages that summarize, connect, and update knowledge over time.
- Schema: instructions that tell the LLM how to ingest, query, lint, and maintain the wiki.

This project will instantiate that pattern for AI agents and Obsidian, while broadening "wiki" into a practical long-term memory substrate. The wiki is not only a publishing surface; it is the agent's externalized memory.

## Product Definition

`llm-wiki` is an agentic second brain for AI agents.

The project has two equally important jobs:

- Remember: detect, structure, link, and store durable knowledge from sources and conversations.
- Recall: consult the stored memory before answering, planning, or making decisions when prior context is likely relevant.

The user experience should feel like working with an assistant that gradually learns the user's projects, preferences, vocabulary, open questions, and accumulated research. Obsidian is the inspectable memory interface: the user can browse, edit, audit, and visualize what the AI remembers.

This is not hidden model memory. The memory is explicit markdown in the user's vault and should be portable across Codex, Claude, and other capable AI agents.

## Architecture Principle

The project separates memory semantics from agent-specific integration.

- Core memory system: vault layout, markdown schemas, memory lifecycle, safety policy, scripts, templates, and verification.
- Agent adapters: instructions and packaging for specific runtimes such as Codex, Claude, and future agents.
- Agent profiles: small capability descriptions that tune behavior for a model/runtime without changing the core memory format.

The core memory should remain stable even when agent tooling changes. Adapters may differ in how they invoke skills, commands, instructions, hooks, or context files, but they should read and write the same Obsidian vault format.

## Repository Shape

The repository root is the project root. It should also remain installable as a Codex plugin by keeping `.codex-plugin/plugin.json` at the root. Other agent integrations live as adapters and templates rather than forcing the whole project to be Codex-specific.

Planned structure:

```text
.codex-plugin/plugin.json
adapters/
  claude/
    CLAUDE.llm-wiki.md
  generic/
    AI_MEMORY.md
agent-profiles/
  codex.md
  claude.md
  generic.md
skills/
  llm-wiki/SKILL.md
  llm-wiki-bootstrap/SKILL.md
  llm-wiki-recall/SKILL.md
  llm-wiki-maintenance/SKILL.md
scripts/
  init_vault.py
  wiki_doctor.py
  search_wiki.py
templates/
  AGENTS.llm-wiki.md
  CLAUDE.llm-wiki.md
  AI_MEMORY.md
  obsidian-vault/
README.md
```

## Codex Plugin Manifest

The Codex manifest will declare:

- `name`: `llm-wiki`
- `skills`: `./skills/`
- category: `Productivity`
- capabilities: `Read`, `Write`, `Interactive`
- keywords around `obsidian`, `wiki`, `pkm`, `markdown`, `knowledge-base`, `research`, `notes`, `memory`, `second-brain`, and `long-term-memory`
- starter prompts for ingesting a source, bootstrapping a vault, and health-checking a wiki

The manifest should not require network services or authentication. All core behavior is local filesystem work over markdown files.

The Codex plugin is the first-class local integration for this repository, but not the conceptual boundary of the project.

## Agent Adapters

Adapters translate the same memory system into each agent's native instruction style.

### Codex Adapter

The Codex adapter uses:

- `.codex-plugin/plugin.json` for plugin discovery
- `skills/` for natural invocation inside Codex
- `AGENTS.llm-wiki.md` as a reusable project instruction template

### Claude Adapter

The Claude adapter should provide:

- a `CLAUDE.llm-wiki.md` template that can be copied or merged into a Claude-facing instruction file
- workflow guidance that avoids assuming Codex-specific tools
- the same memory lifecycle, vault layout, and safety rules as the Codex adapter

### Generic Adapter

The generic adapter should provide:

- `AI_MEMORY.md`, a portable instruction file for agents that can read/write local files
- a compact description of the memory lifecycle
- minimum capabilities required for an agent to use the vault responsibly

## Agent Profiles

Different AI agents and models have different strengths, context windows, filesystem access, tool calling behavior, and instruction-following quirks. The project should model those differences with agent profiles rather than forking the memory format.

Each profile should state:

- supported file access and write behavior
- preferred instruction entrypoint
- context budget and recall budget guidance
- whether the agent can run scripts directly
- how proactive ambient capture should be
- when confirmation is required before writing memory
- known limitations or failure modes

Profiles tune behavior. They must not redefine what memory means.

## Natural Invocation Strategy

Codex skill invocation is driven mainly by skill metadata and instruction wording, while other agents may rely on instruction files, commands, or project memory files. The project therefore needs both broad Codex skill descriptions and portable natural-language instructions for other agents.

`llm-wiki` should trigger for natural requests such as:

- ingesting, organizing, or maintaining markdown knowledge bases
- working with Obsidian vaults
- processing notes, papers, articles, clips, meeting notes, transcripts, or source folders into a wiki
- asking questions against an existing personal wiki or research wiki
- asking the AI to remember, recall, learn, keep track of, or use prior context
- updating `index.md`, `log.md`, cross-links, entity pages, concept pages, synthesis pages, or source summaries
- checking wiki health, contradictions, stale claims, missing links, and orphan pages
- discussing a topic over multiple turns where stable decisions, definitions, research findings, preferences, or open questions emerge

The primary workflow must route to the right behavior without requiring users to type command names.

The intended feel is ambient rather than command-driven. The user should be able to talk normally, and the AI should notice when the conversation has produced durable knowledge worth adding to the wiki.

Agent integrations are not background daemons by default, so the project cannot watch every conversation outside an active agent session unless a future runtime explicitly supports that. Within an active conversation, however, the agent should behave like a quiet memory maintainer: detect durable knowledge, decide whether it belongs in the vault, and either update the wiki directly or make a brief confirmation request when the edit could be surprising.

## Ambient Capture Policy

The project will include ambient capture in the primary `llm-wiki` workflow. In Codex this is expressed as a skill; in other agents it is expressed through their adapter instructions.

Capture candidates:

- user preferences, conventions, or durable project decisions
- stable definitions, concepts, entities, and relationships
- research findings or source-backed claims
- conclusions from analysis that are likely to be useful later
- unresolved questions, TODOs, hypotheses, contradictions, and follow-up source ideas
- summaries of long conversations that would otherwise be lost in chat history

Do not capture:

- throwaway brainstorming fragments that the user has not settled on
- sensitive personal data unless the user explicitly asks to keep it
- secrets, credentials, private keys, tokens, or auth material
- transient task mechanics such as "run tests now" or "fix this typo"
- content the user explicitly says not to remember or not to save

Default write behavior:

- For low-risk durable notes, the agent may update the wiki without asking first, then briefly mention what changed.
- For ambiguous, sensitive, personal, or high-volume updates, the agent must ask before writing.
- For conflicting claims, the agent must preserve the conflict explicitly instead of overwriting the older claim.
- For early brainstorming, the agent should wait until decisions stabilize, then capture the decision and alternatives.
- For repeated conversational work on the same topic, the agent should update existing pages rather than creating duplicate pages.

This creates a "soft automatic" model: the active agent acts naturally and proactively, but still respects user agency and avoids surprising writes.

## Memory Model

The project will treat the Obsidian vault as a typed memory system.

Memory types:

- Source memory: facts and claims extracted from immutable raw sources.
- Semantic memory: durable concepts, entities, definitions, relationships, and summaries.
- Episodic memory: compact records of meaningful conversations, decisions, and turning points.
- Procedural memory: workflows, conventions, recurring processes, and how the user prefers work to be done.
- Preference memory: stable user preferences, style choices, defaults, and dislikes.
- Open-loop memory: unresolved questions, hypotheses, contradictions, TODOs, and follow-up source ideas.
- Synthesis memory: higher-level conclusions, theses, comparisons, and patterns that emerge across sources or conversations.

Each memory page should make provenance explicit. A page should distinguish between:

- user-stated information
- source-backed claims
- agent inference
- unresolved or low-confidence interpretation

When confidence is low, the agent should either mark the memory as tentative or ask before storing it.

## Recall Policy

Long-term memory is only useful if the agent recalls it.

Before answering or acting, `llm-wiki` should guide the active agent to check memory when the current conversation appears related to:

- an existing project, person, organization, topic, or research thread in the vault
- a prior user preference or convention
- an open question or unresolved decision
- a source-backed topic that has already been ingested
- a repeated workflow where procedural memory may apply

Recall flow:

1. Read `wiki/index.md` and recent `wiki/log.md` entries.
2. Search likely memory pages with `scripts/search_wiki.py` when available.
3. Open the smallest useful set of pages.
4. Use recalled context in the answer or plan.
5. Mention recalled context only when it materially affects the response or when transparency is useful.

The agent should not over-recall. For simple unrelated tasks, it should stay lightweight.

## Memory Lifecycle

The project should support a memory lifecycle, not just one-off note writing.

1. Observe: notice durable information in sources or conversation.
2. Triage: decide whether it is worth remembering, should be ignored, or needs confirmation.
3. Store: write a concise memory entry with type, provenance, links, and confidence.
4. Link: connect it to relevant concepts, entities, projects, sources, and open loops.
5. Recall: use it in later relevant conversations.
6. Consolidate: periodically merge episodic notes into semantic, procedural, or synthesis pages.
7. Prune: flag stale, superseded, duplicate, or low-value memory during maintenance.

This lifecycle keeps the vault from becoming a dumping ground of chat summaries.

## Codex Skills

These skills are the Codex adapter's implementation of the agent-agnostic memory system.

### `llm-wiki`

Primary second-brain workflow. It should:

- detect or ask for the vault root only when it cannot infer one
- read `AGENTS.md`, `AGENTS.llm-wiki.md`, `wiki/index.md`, and recent `wiki/log.md` entries when present
- classify the user request or conversation state as bootstrap, ingest, recall, query, maintenance, schema update, or ambient capture
- monitor the active conversation for durable knowledge that should compound into the wiki
- recall existing memory when it is likely relevant to the user's current task
- preserve raw sources as immutable input
- write generated knowledge only into the wiki layer
- maintain Obsidian wikilinks and Dataview-friendly frontmatter
- append parseable log entries for meaningful operations
- keep ambient capture updates concise and avoid interrupting the main task unless confirmation is needed

### `llm-wiki-bootstrap`

Use when creating or initializing a new LLM Wiki/Obsidian vault. It should:

- create the default folder layout
- create starter `index.md`, `log.md`, and overview pages
- install an agent-facing schema/instructions file plus any adapter-specific instructions
- optionally create Obsidian configuration templates that are safe to copy into a vault

### `llm-wiki-recall`

Use when the user asks the AI to remember, recall, use prior context, continue a thread, or make a decision that may depend on long-term memory. It should:

- find relevant memory pages before answering
- distinguish current conversation context from recalled vault context
- cite or name the memory pages that materially influenced the answer
- avoid loading the entire vault when targeted recall is enough
- update open-loop or episodic memory if the conversation resolves or changes prior context

### `llm-wiki-maintenance`

Use for health checks and linting. It should:

- find orphan wiki pages
- identify missing backlinks and cross-reference opportunities
- flag stale or contradictory claims
- detect pages missing frontmatter or required sections
- suggest useful follow-up sources or questions
- produce actionable repair edits when the user asks for fixes

## Obsidian Vault Conventions

Default vault layout:

```text
raw/
  sources/
  assets/
wiki/
  index.md
  log.md
  overview.md
  sources/
  memory/
    episodes/
    preferences/
    procedures/
    open-loops/
  entities/
  concepts/
  syntheses/
  questions/
meta/
  prompts/
  schemas/
```

Rules:

- `raw/` is user-owned and immutable to agents except when explicitly asked to add imported files.
- `wiki/` is AI-owned and can be created or updated by agents following the memory policy.
- `meta/` stores conventions, schemas, and optional prompts.
- Use Obsidian `[[wikilinks]]` for internal references.
- Use relative markdown links only when linking to raw source files or assets.
- Prefer YAML frontmatter on wiki pages with fields such as `type`, `status`, `created`, `updated`, `sources`, `tags`, and `aliases`.
- Memory pages should also include `confidence`, `provenance`, and `last_reviewed` when relevant.
- `wiki/index.md` is content-oriented and should be updated after ingest or major edits.
- `wiki/log.md` is chronological and append-only with parseable headings like `## [2026-05-04] ingest | Title`.

## Scripts

### `scripts/init_vault.py`

Creates the default vault layout and starter markdown files. It must be idempotent and avoid overwriting user content unless an explicit force flag is passed.

### `scripts/search_wiki.py`

Provides local lexical search over markdown pages. It should be simple and dependency-light, using Python standard library only for the first version.

### `scripts/wiki_doctor.py`

Checks wiki health. It should report missing required files, broken wikilinks, orphan pages, missing frontmatter, and stale index entries. It should emit human-readable text and exit non-zero only for structural problems that should fail verification.

## Data Flow

Bootstrap:

1. User asks to create or initialize an LLM Wiki/Obsidian vault.
2. The active agent runs the bootstrap workflow.
3. The project creates folders, starter wiki files, and schema instructions.
4. The active agent summarizes what was created and how to open it in Obsidian.

Ingest:

1. User points the active agent at a raw source file or folder.
2. The active agent reads the source without modifying it.
3. The active agent extracts key claims, entities, concepts, and contradictions.
4. The active agent creates or updates source summary, entity, concept, and synthesis pages.
5. The active agent updates `wiki/index.md`.
6. The active agent appends a `wiki/log.md` entry.

Query:

1. The active agent reads `wiki/index.md` first.
2. The active agent searches or opens relevant wiki pages.
3. The active agent answers with citations to wiki/source pages.
4. If the answer is durable, the active agent offers or creates a page under `wiki/questions/` or `wiki/syntheses/`.

Recall:

1. User asks something where prior memory may matter, or the active conversation resembles an existing memory thread.
2. The active agent reads the index, recent log entries, and targeted memory pages.
3. The active agent uses recalled preferences, procedures, prior decisions, source-backed claims, or open loops to shape the response.
4. The active agent updates memory only if the conversation adds or changes durable context.

Maintenance:

1. The active agent reads index, log, and wiki page graph.
2. The active agent reports health findings.
3. When asked, the active agent repairs links, index entries, metadata, and stale summaries.
4. The active agent logs the maintenance pass.

Ambient capture:

1. User discusses a topic naturally without asking for a wiki operation.
2. The active agent detects durable knowledge using the ambient capture policy.
3. The active agent checks `wiki/index.md` and likely target pages.
4. The active agent updates an existing page or creates a focused page only when the knowledge is stable enough.
5. The active agent updates `wiki/index.md` when a page is created or materially changed.
6. The active agent appends a compact `wiki/log.md` entry for the capture.
7. The active agent returns to the main conversation with a short note such as "I also captured the finalized convention in `wiki/concepts/...`."

Consolidation:

1. The active agent reviews recent episodic memory and log entries.
2. The active agent identifies durable patterns, decisions, or preferences.
3. The active agent merges them into semantic, procedural, preference, open-loop, or synthesis pages.
4. The active agent marks the source episode as consolidated instead of deleting it.
5. The active agent logs the consolidation pass.

## Error Handling

- If no vault is detected, ask for or infer a target directory before writing.
- If required files are missing, offer bootstrap or partial repair.
- If a raw source cannot be parsed, create a log entry only if meaningful work was completed.
- If the wiki has conflicting claims, preserve both claims and mark the conflict instead of silently choosing one.
- If a file has user-authored content in a wiki page, update conservatively and avoid deleting information unless the user asks.
- If ambient capture would interrupt a time-sensitive coding task, defer the capture until the task has a natural pause.
- If the user rejects an ambient capture suggestion, do not ask again for the same content.
- If recalled memory conflicts with current user instructions, current instructions win and the conflict should be noted or updated.
- If memory provenance is unclear, treat it as low-confidence context instead of fact.
- If memory starts to accumulate noisy chat summaries, maintenance should consolidate or mark them for pruning.

## Testing And Verification

Minimum verification before completion:

- validate plugin manifest JSON
- confirm every skill has valid YAML frontmatter
- run `scripts/init_vault.py` against a temporary directory
- run `scripts/wiki_doctor.py` against the generated sample vault
- run `scripts/search_wiki.py` against the generated sample vault
- manually inspect generated markdown for Obsidian wikilinks and parseable log headings
- verify that sample memory pages include provenance and confidence metadata
- verify that recall instructions prefer targeted memory lookup over loading the whole vault

## Out Of Scope For First Version

- embedding/vector search
- MCP server
- Obsidian desktop plugin written in TypeScript
- automatic browser clipping
- automatic PDF OCR or audio transcription
- network sync
- hosted service or authentication

These can be added later without changing the core memory shape.
