# LLM Wiki Codex Plugin Design

## Goal

Build this repository as a GitHub-publishable Codex plugin that turns Andrej Karpathy's LLM Wiki pattern into a reusable Obsidian-first workflow. The plugin should help Codex naturally maintain a persistent markdown wiki from curated raw sources, without requiring the user to explicitly type a skill or command name for common wiki tasks.

## Source Idea

Karpathy's LLM Wiki pattern has three layers:

- Raw sources: immutable files curated by the user.
- Wiki: generated and maintained markdown pages that summarize, connect, and update knowledge over time.
- Schema: instructions that tell the LLM how to ingest, query, lint, and maintain the wiki.

This plugin will instantiate that pattern for Codex and Obsidian.

## Repository Shape

The repository root is the plugin root. This keeps GitHub distribution simple: cloning or installing the repository gives Codex the plugin manifest and all bundled skills directly.

Planned structure:

```text
.codex-plugin/plugin.json
skills/
  llm-wiki/SKILL.md
  llm-wiki-bootstrap/SKILL.md
  llm-wiki-maintenance/SKILL.md
scripts/
  init_vault.py
  wiki_doctor.py
  search_wiki.py
templates/
  AGENTS.llm-wiki.md
  obsidian-vault/
README.md
```

## Plugin Manifest

The manifest will declare:

- `name`: `llm-wiki`
- `skills`: `./skills/`
- category: `Productivity`
- capabilities: `Read`, `Write`, `Interactive`
- keywords around `obsidian`, `wiki`, `pkm`, `markdown`, `knowledge-base`, `research`, and `notes`
- starter prompts for ingesting a source, bootstrapping a vault, and health-checking a wiki

The manifest should not require network services or authentication. All core behavior is local filesystem work over markdown files.

## Natural Invocation Strategy

Codex skill invocation is driven mainly by skill metadata and instruction wording. The plugin therefore needs a broad, high-signal primary skill description.

`llm-wiki` should trigger for natural requests such as:

- ingesting, organizing, or maintaining markdown knowledge bases
- working with Obsidian vaults
- processing notes, papers, articles, clips, meeting notes, transcripts, or source folders into a wiki
- asking questions against an existing personal wiki or research wiki
- updating `index.md`, `log.md`, cross-links, entity pages, concept pages, synthesis pages, or source summaries
- checking wiki health, contradictions, stale claims, missing links, and orphan pages

The primary skill must route to the right workflow without requiring users to type command names.

## Skills

### `llm-wiki`

Primary always-on wiki maintainer workflow. It should:

- detect or ask for the vault root only when it cannot infer one
- read `AGENTS.md`, `AGENTS.llm-wiki.md`, `wiki/index.md`, and recent `wiki/log.md` entries when present
- classify the user request as bootstrap, ingest, query, maintenance, or schema update
- preserve raw sources as immutable input
- write generated knowledge only into the wiki layer
- maintain Obsidian wikilinks and Dataview-friendly frontmatter
- append parseable log entries for meaningful operations

### `llm-wiki-bootstrap`

Use when creating or initializing a new LLM Wiki/Obsidian vault. It should:

- create the default folder layout
- create starter `index.md`, `log.md`, and overview pages
- install a Codex-oriented schema/instructions file
- optionally create Obsidian configuration templates that are safe to copy into a vault

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
  entities/
  concepts/
  syntheses/
  questions/
meta/
  prompts/
  schemas/
```

Rules:

- `raw/` is user-owned and immutable to Codex except when explicitly asked to add imported files.
- `wiki/` is LLM-owned and can be created or updated by Codex.
- `meta/` stores conventions, schemas, and optional prompts.
- Use Obsidian `[[wikilinks]]` for internal references.
- Use relative markdown links only when linking to raw source files or assets.
- Prefer YAML frontmatter on wiki pages with fields such as `type`, `status`, `created`, `updated`, `sources`, `tags`, and `aliases`.
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
2. Codex runs the bootstrap workflow.
3. The plugin creates folders, starter wiki files, and schema instructions.
4. Codex summarizes what was created and how to open it in Obsidian.

Ingest:

1. User points Codex at a raw source file or folder.
2. Codex reads the source without modifying it.
3. Codex extracts key claims, entities, concepts, and contradictions.
4. Codex creates or updates source summary, entity, concept, and synthesis pages.
5. Codex updates `wiki/index.md`.
6. Codex appends a `wiki/log.md` entry.

Query:

1. Codex reads `wiki/index.md` first.
2. Codex searches or opens relevant wiki pages.
3. Codex answers with citations to wiki/source pages.
4. If the answer is durable, Codex offers or creates a page under `wiki/questions/` or `wiki/syntheses/`.

Maintenance:

1. Codex reads index, log, and wiki page graph.
2. Codex reports health findings.
3. When asked, Codex repairs links, index entries, metadata, and stale summaries.
4. Codex logs the maintenance pass.

## Error Handling

- If no vault is detected, ask for or infer a target directory before writing.
- If required files are missing, offer bootstrap or partial repair.
- If a raw source cannot be parsed, create a log entry only if meaningful work was completed.
- If the wiki has conflicting claims, preserve both claims and mark the conflict instead of silently choosing one.
- If a file has user-authored content in a wiki page, update conservatively and avoid deleting information unless the user asks.

## Testing And Verification

Minimum verification before completion:

- validate plugin manifest JSON
- confirm every skill has valid YAML frontmatter
- run `scripts/init_vault.py` against a temporary directory
- run `scripts/wiki_doctor.py` against the generated sample vault
- run `scripts/search_wiki.py` against the generated sample vault
- manually inspect generated markdown for Obsidian wikilinks and parseable log headings

## Out Of Scope For First Version

- embedding/vector search
- MCP server
- Obsidian desktop plugin written in TypeScript
- automatic browser clipping
- automatic PDF OCR or audio transcription
- network sync
- hosted service or authentication

These can be added later without changing the core plugin shape.

