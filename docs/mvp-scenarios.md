# LLM Wiki MVP Scenarios

Status: Draft v0.2

The page, evidence, and update contracts used by these scenarios are defined in
[`../skills/llm-wiki/references/storage-model.md`](../skills/llm-wiki/references/storage-model.md).

## Product Boundary

The MVP serves one person working across isolated technical or research projects.
It resolves one project Wiki at a time and turns explicitly selected sources into
a maintained, source-backed Markdown Wiki.

The MVP does not automatically remember conversations, maintain a user profile,
run background jobs, or coordinate concurrent team writers.

## Scenario 0: Resolve Or Provision During Normal Work

### User intent

The user starts an ordinary project task without separately setting up or naming
a Wiki directory.

### Required behavior

1. Derive a stable identity for the current project without storing a raw Git
   remote in the Vault.
2. Reuse the configured Obsidian Vault. If none is configured, automatically use
   the only accessible registered Vault or ask once when several are available.
3. Resolve an existing project Wiki or atomically create an empty isolated
   skeleton under `LLM Wiki/projects/`.
4. Continue the user's original task in the same turn.
5. Confine all Wiki reads and writes to the resolved project root.

### Acceptance criteria

- No separate setup command is required in the single-Vault case.
- Resolving the same Git remote or its worktrees returns the same project Wiki.
- Different projects with the same folder name remain separate.
- Repeated resolution is a no-op and does not duplicate setup records.
- Multiple accessible Vaults produce a one-time selection request instead of an
  arbitrary choice.
- Creating the skeleton does not import project files or conversation content.

## Scenario 1: Ingest And Reconcile A Source

### User intent

The user asks the agent to add one document, paper, meeting record, or code finding
to the wiki.

### Required behavior

1. Read the source without modifying it.
2. If it is outside project `sources/`, create an immutable content-addressed
   snapshot after checking for credential-like content.
3. Identify its important claims, entities, concepts, and relationships.
4. Search the existing Wiki before creating new pages.
5. Create a source summary and update every materially affected page.
6. Attach traceable evidence to important claims.
7. Preserve disagreements instead of silently replacing older claims.
8. Update navigation and the operation log.
9. Show the user what changed.

### Acceptance criteria

- The raw source is unchanged.
- An imported snapshot matches the original digest, while the Vault contains no
  external absolute source path.
- Every important derived claim can be traced to the source.
- Re-ingesting the same source does not create uncontrolled duplicates.
- Relevant existing pages are updated, not merely supplemented by a new summary.
- Conflicting claims remain visible with their respective evidence.

## Scenario 2: Query And Crystallize Knowledge

### User intent

The user asks a factual, comparative, or synthesis question about the accumulated
project knowledge.

### Required behavior

1. Find the smallest relevant set of wiki pages.
2. Follow their evidence links when an important claim needs verification.
3. Distinguish sourced facts, derived conclusions, and unresolved gaps.
4. Answer with traceable citations.
5. State that evidence is insufficient when the wiki and sources do not support an
   answer.
6. Offer to crystallize a durable new comparison or synthesis; do not write it
   silently.

### Acceptance criteria

- The answer reuses accumulated wiki knowledge instead of starting from all raw
  sources.
- Citations support the claims they accompany.
- Unsupported questions produce an explicit lack-of-evidence response.
- A crystallized answer is linked to the pages and sources it builds on.

## Scenario 3: Lint And Repair The Wiki

### User intent

The user asks whether the wiki is structurally and semantically healthy.

### Required behavior

1. Check required metadata, navigation, links, duplicate topics, and source paths.
2. Flag claims that lack evidence or point to changed or missing sources.
3. Identify contradictions, superseded claims, stale syntheses, and knowledge gaps.
4. Produce a read-only report first.
5. Apply repairs only after the user approves the proposed scope.

### Acceptance criteria

- Mechanical and semantic findings are reported separately.
- Each finding identifies the affected page and supporting evidence.
- The lint pass does not modify the wiki by default.
- Repairs are visible, reviewable, and reversible.

## Explicitly Excluded Scenarios

- Remembering personal preferences from ordinary conversation.
- Saving complete conversation histories automatically.
- Sharing a global memory store across unrelated projects.
- Searching sibling project Wikis automatically.
- Running scheduled consolidation or autonomous maintenance.
- Requiring a vector database, knowledge graph, hosted service, or MCP server.
- Managing team roles, permissions, or simultaneous writers.

## MVP Completion Rule

The first implementation is complete only when all four scenarios pass against a
small public test corpus using local files, Python standard-library helpers, and
the agent's built-in tools.
