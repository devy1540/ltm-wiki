# LLM Wiki

> Status: automatic project-Wiki MVP. The previous LTM Wiki implementation was
> removed so this project could restart from a clear LLM Wiki product boundary.

LLM Wiki is a local knowledge base that an LLM builds and maintains from sources
chosen by the user. The LLM turns those sources into linked, source-backed
Markdown pages and keeps the resulting wiki current over time.

## The Problem

Documents and useful conversations accumulate, but their connections and
conclusions do not. A conventional retrieval system searches the raw material
again for every question. A manually maintained wiki becomes expensive to keep
consistent.

LLM Wiki addresses this by preserving the result of knowledge work as a durable,
inspectable artifact that improves as sources and questions accumulate.

## Core Model

- **Raw sources** are selected and owned by the user. The LLM reads but does not
  rewrite them.
- **Wiki pages** are derived knowledge maintained by the LLM: source summaries,
  entities, concepts, comparisons, syntheses, and answered questions.
- **Schema** defines how the LLM ingests sources, cites evidence, updates pages,
  handles contradictions, and checks wiki health.

The core operations are project resolution, `ingest`, `query`, `crystallize`,
and `lint`.

## What Using It Feels Like

Install the LTM Wiki plugin or `llm-wiki` skill once, then work normally in a
project. No separate Wiki setup command is required.

1. At the beginning of project work, the skill resolves the current project's
   Wiki before continuing the original task.
2. If the machine has one accessible Obsidian Vault, it is selected once and a
   project Wiki is created automatically under
   `LLM Wiki/projects/<project-name>--<identity-hash>/`.
3. If several Vaults are available, the agent asks which one to use once. The
   choice is stored in machine-local configuration and reused.
4. Each project gets an isolated Wiki. Git worktrees and equivalent Git remotes
   resolve to the same project Wiki; unrelated projects do not share knowledge.
5. A file is added as evidence only when the user explicitly asks to add or
   ingest it. Ordinary conversations and files used during normal work are not
   captured.

The Wiki and imported source snapshots are normal files inside the chosen Vault,
so Obsidian Sync may synchronize them if that Vault is configured for sync. The
machine-local project registry is kept outside the Vault.

Explicit prompts such as “add this design document to the project Wiki” or
“check the Wiki for the previous decision” remain available, but `$llm-wiki` is
not required for normal matching requests.

Automatic startup uses Codex's implicit skill matching, not an always-running
hook or background watcher. The skill metadata asks Codex to activate it at the
beginning of project work; explicit `$llm-wiki` remains a fallback on hosts that
do not support or select implicit skills.

## Product Boundary

LLM Wiki is not a general-purpose agent-memory system and does not automatically
save every conversation or user detail. Agent memory, search indexes, background
automation, and MCP integrations may be added later as optional layers only when
their need is demonstrated.

The initial product definition is in
[`docs/product-definition.md`](docs/product-definition.md).
The concrete MVP behavior is in
[`docs/mvp-scenarios.md`](docs/mvp-scenarios.md).

## Current Implementation

The implementation is a skills-only Codex plugin:

- [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json) packages the repository
  for plugin distribution without an MCP server.
- [`skills/llm-wiki/SKILL.md`](skills/llm-wiki/SKILL.md) routes automatic project
  resolution, setup, ingest, query, crystallize, and lint requests.
- Its bundled Python scripts discover a configured Obsidian Vault, create an
  isolated project skeleton, and safely import explicitly selected external
  source files.
- Its references define the storage model and operation-specific workflows; its
  assets contain the seed files used to initialize a Wiki.

The runtime requirement is Python 3.10 or newer using only the standard library.
The core does not require third-party Python packages, an MCP server, database,
embedding model, background process, or hosted service.

Codex also discovers the same skill directly from the repository-standard
`.agents/skills/` compatibility link during development. After installing or
updating the plugin, start a new Codex task so the skill is loaded.

## Verification

`sh tests/verify-repository.sh` validates the plugin and skill packages, automatic
project isolation, immutable source importing, source hashes, golden Wiki
contracts, source replacement behavior, and source-path boundaries. CI also runs
the Agent Skills reference validator against `skills/llm-wiki`.

These are deterministic static checks. Semantic behavior—whether evidence really
supports a claim or a synthesis is accurate—is evaluated with the workflow in
[`tests/acceptance.md`](tests/acceptance.md). Sanitized results from the current
independent forward tests are recorded in
[`tests/evidence/2026-08-24-forward-tests.md`](tests/evidence/2026-08-24-forward-tests.md).

## Origin

This project is an implementation of the
[LLM Wiki pattern proposed by Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
