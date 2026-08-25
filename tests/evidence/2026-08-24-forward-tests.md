# Independent Forward-Test Evidence — 2026-08-24

This record summarizes fresh-agent runs against isolated temporary copies of the
public fixtures. Temporary paths are omitted because they are not durable. The
committed golden trees preserve the generated artifacts used for deterministic
follow-up validation.

## Skill Discovery

Result: PASS.

A fresh agent discovered `llm-wiki` through the repository compatibility path at
`.agents/skills/llm-wiki/SKILL.md`. The final package keeps one canonical copy at
`skills/llm-wiki/`, resolves all eight references and three seed assets, and
passes both the Agent Skills and Codex plugin validators.

## Setup

Result: PASS.

A fresh agent initialized an empty temporary root with the supplied project title.
The final automatic resolver preserves that contract while adding a project
marker and empty `sources/imported/` directory. It creates the three Wiki
subdirectories and three seed files atomically. `operations.md` contains exactly
one setup entry, and repeated resolution is a no-op. No MCP, database, embedding,
or background process is used.

## Automatic Project Resolution And External Import

Result: PASS.

The subprocess-level tests used isolated fake Obsidian registries, Vaults,
machine configuration, and project directories. They verified:

- one accessible Vault is selected and configured without a separate setup step;
- multiple accessible Vaults return `VAULT_SELECTION_REQUIRED` and create no
  Wiki;
- repeated resolution reuses one Wiki while unrelated projects remain isolated;
- Git remotes, worktrees, case-sensitive paths, non-default ports, and IPv6
  authorities keep stable, non-colliding project identities;
- deleting and recreating a non-Git project at the same path does not reuse its
  predecessor's Wiki;
- symlinked target components and symlinked legacy layouts fail closed;
- an explicitly selected external source is copied byte-for-byte to an immutable,
  content-addressed snapshot, while its absolute origin path is absent from the
  Vault;
- repeated imports are no-ops, changed content creates a new digest snapshot, and
  common provider tokens, assignment-style secrets, and JSON credentials are
  rejected.

An independent reviewer first reproduced four isolation and credential-scanning
defects plus an IPv6 authority collision. Regression tests were added for every
case. The reviewer reran the reproductions after the fixes and reported no
remaining findings. `tests/verify-repository.sh` finished with 29 Python tests and
all retained golden-fixture checks passing.

## Ingest, Query, And Crystallize

Fixture: `tests/fixtures/basic-project/`

Result: PASS.

- Four sources were ingested in order.
- Re-ingesting unchanged Architecture v2 was a no-op.
- Source SHA-256 values remained equal to `expected/raw.sha256`.
- Four reconciled sourced claims were owned by `wiki/topics/transport.md`.
- Source notes remained limited to their own source and linked to topic claims.
- The unapproved gRPC-default recommendation remained visible as superseded with
  conflict and supersession relations.
- The supported transport question was answered from the Wiki and source locators.
- The upload-size question returned explicit insufficient evidence.
- An explicitly approved transport comparison was written as a synthesis with a
  derived-claim evidence chain.

Generated artifacts are retained under `tests/fixtures/basic-project/golden/` and
checked by `tests/verify-generated-wiki.sh`.

## Read-Only Lint And Scoped Repair

Fixture: `tests/fixtures/basic-project/lint-seed/`

Result: PASS.

Lint reported exactly the seeded missing source, broken index link, duplicate claim
ID, and stale-propagation defect. Mechanical and semantic findings were separated.
Whole-tree hashes were identical before and after lint. After explicit approval of
only the broken index link, only `wiki/index.md` and `wiki/operations.md` changed;
the three unapproved findings remained.

## Same-Path Source Replacement

Fixture: `tests/fixtures/source-replacement/`

Result: PASS.

- `sources/policy.md` was explicitly replaced from v1 to v2 at the same path.
- The source note was rewritten in place with the v2 digest.
- Removed 30-second timeout evidence no longer remained current.
- The old digest and locator were retained as Former evidence.
- The sourced timeout claim and dependent synthesis became stale.
- The operation recorded old/new digests and both transitions.
- Re-ingesting unchanged v2 was a no-op.

Generated artifacts are retained under
`tests/fixtures/source-replacement/golden/` and checked by
`tests/verify-source-replacement.sh`.

## Source Path Boundary

Fixture: `tests/fixtures/path-boundary/`

Result: PASS.

A fresh security-oriented agent rejected:

- `source_path: ../outside.md` before content access;
- a topic evidence link whose canonical target escaped `sources/`;
- a symlink under `sources/` whose canonical target escaped the directory.

The valid regular file inside `sources/` remained eligible. The invalid claim was
not treated as substantiated, and pre/post state fingerprints were identical. The
deterministic canonical-path checks are retained in
`tests/verify-path-boundary.sh`.

## Evidence Boundary

The independent runs provide behavioral evidence for the public fixtures, not a
proof for arbitrary domains or models. CI does not call an LLM. Human or independent
semantic review remains required for claim importance, evidence entailment,
conflict interpretation, and synthesis quality.

Detailed sanitized records:

- [`phased-basic-flow.md`](phased-basic-flow.md)
- [`basic-flow-transcript.md`](basic-flow-transcript.md)
- [`lint-report.md`](lint-report.md)
- [`source-replacement-report.md`](source-replacement-report.md)
- [`path-boundary-report.md`](path-boundary-report.md)
