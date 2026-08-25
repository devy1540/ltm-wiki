# LLM Wiki Product Definition

Status: Draft v0.4

## Definition

LLM Wiki is a local knowledge base that an LLM builds and maintains from sources
chosen by the user. It converts those sources into linked, source-backed Markdown
pages and updates the resulting wiki as knowledge evolves.

## Problem

Knowledge work currently has four recurring losses:

1. Documents and useful conversations are scattered across tools.
2. An LLM re-reads and re-derives the same knowledge for every question.
3. Cross-source connections, contradictions, and conclusions disappear after the
   conversation ends.
4. A human-maintained wiki becomes too expensive to keep current.

LLM Wiki preserves the output of knowledge work as a durable, inspectable artifact
that compounds over time.

## Initial User

The first user is an individual working across one or more technical or research
projects who accumulates documents, papers, meeting records, code findings, or
other source material over weeks or months.

One Obsidian Vault may contain many isolated project Wikis. Knowledge from one
project is not searched or synthesized into another project unless the user later
requests an explicit, separately designed cross-project workflow.

Team-scale collaboration is a later concern.

## Primary Job

When the user accumulates material about a project, LLM Wiki turns it into a
source-backed wiki that stays current, so future questions start from accumulated
understanding instead of repeatedly re-reading raw documents.

The MVP automatically resolves or creates only the empty Wiki structure for the
current project. It accepts only sources explicitly selected by the user.
Conversation output enters the Wiki only through an explicit crystallize request
or approval.

## Core Layers

### Raw sources

- Selected and owned by the user.
- Immutable unless the user explicitly replaces or removes a source.
- The source of truth used to verify derived knowledge.
- External files selected for ingestion are copied into immutable,
  content-addressed project snapshots; their originals are never modified.

### Wiki

- Maintained by the LLM.
- Contains source summaries, entities, concepts, comparisons, syntheses, and
  answered questions.
- Connects claims to their supporting sources.
- Preserves disagreements and superseded claims instead of silently overwriting
  them.

### Schema

- Defines the page types and required metadata.
- Defines source citation and update rules.
- Defines the workflows the LLM must follow.
- Evolves with the user and the domain.

## Core Operations

### Resolve

Map the current workspace to one isolated project Wiki in the user's selected
Obsidian Vault. Reuse an existing mapping or create an empty skeleton, then
continue the original task without requiring a separate setup command.

### Ingest

Read a user-selected source, identify its important claims and relationships,
then create or update the affected wiki pages with evidence links.

### Query

Find relevant wiki pages, verify important claims against raw sources when
needed, and answer with traceable evidence.

### Crystallize

Preserve a valuable comparison, conclusion, or question result as durable wiki
knowledge instead of leaving it only in conversation history.

### Lint

Report structural problems, missing evidence, contradictions, stale claims,
broken links, duplicates, and important knowledge gaps. Lint is read-only unless
the user approves repairs.

## Non-Goals For The First Version

- Automatically remembering every conversation.
- Maintaining a general user profile or agent persona.
- Background capture or autonomous scheduled writes.
- A hosted service, remote database, or mandatory synchronization layer.
- Mandatory embeddings, vector databases, knowledge graphs, or MCP servers.
- Team permissions and concurrent multi-writer collaboration.
- Automatic cross-project search or a shared global project memory.

## Principles

1. Markdown is the source of truth for derived knowledge.
2. Raw sources remain separate and verifiable.
3. Important claims must be traceable to evidence.
4. Contradictions are represented, not hidden.
5. Derived indexes and caches must be rebuildable.
6. Writes must be visible, reviewable, and reversible.
7. A skills-only workflow with Python standard-library helpers is the baseline
   implementation.
8. Tooling is added only after a measured limitation appears.
9. Automatic provisioning is separate from knowledge capture: creating an empty
   Wiki does not authorize ingesting files or saving conversations.
10. Project resolution fails closed instead of guessing among multiple Vaults or
    conflicting project mappings.

## Success Criteria

The first useful version must demonstrate that:

- a normal project task can resolve or create its Wiki without a separate setup
  command;
- repeated work in the same Git project reuses one Wiki while unrelated projects
  remain isolated;
- multiple available Obsidian Vaults require a one-time explicit choice;
- ingesting a source updates all materially related wiki pages;
- important claims can be traced back to their source;
- conflicting or updated information is represented correctly;
- repeated ingestion does not create uncontrolled duplicates;
- query answers reuse accumulated knowledge and cite evidence;
- unsupported questions result in an explicit lack-of-evidence response;
- an explicitly selected external file is snapshotted without changing the
  original or storing its absolute path in the Vault;
- the complete workflow works with local files, Python 3.10+ standard-library
  helpers, and an agent's built-in tools.

The scenarios and observable acceptance criteria for the MVP are defined in
[`mvp-scenarios.md`](mvp-scenarios.md).

The concrete storage and claim-evidence contracts are defined in
[`../skills/llm-wiki/references/storage-model.md`](../skills/llm-wiki/references/storage-model.md).

## Open Decisions

- Final product and repository name.
- Evaluation corpus and quality metrics.
- The threshold at which an optional local search index becomes necessary.

## Source Pattern

This definition builds on Andrej Karpathy's
[LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f):
immutable raw sources, an LLM-maintained wiki, and a schema governing ingest,
query, and lint workflows.
