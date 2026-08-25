# MVP Acceptance Procedure

The basic fixture validates product behavior, not exact model wording.

## Automatic Project Resolution

Use temporary directories for all paths in this procedure; do not touch a real
Obsidian Vault or the machine's normal LLM Wiki configuration.

1. Create one fake Vault containing `.obsidian/`, one temporary machine config
   path, and two Git repositories with distinct remotes but the same directory
   basename.
2. Run `project_resolver.py resolve --create --json` from the first repository
   without preconfiguring a Vault, using an Obsidian registry fixture that lists
   only the fake Vault.
3. Resolve the first repository again, then resolve one of its Git worktrees.
4. Resolve the second repository.
5. Repeat with an Obsidian registry fixture containing two accessible fake Vaults.

PASS requires:

- the single-Vault run returns `READY` and `created: true` without a separate
  setup step;
- repeated resolution and the worktree return the original project root without
  adding another setup operation;
- the distinct remote gets a different project root even though its basename is
  the same;
- the two-Vault run returns `VAULT_SELECTION_REQUIRED` and creates nothing;
- no raw Git remote or unrelated project path is written inside either Vault;
- the created skeleton contains the marker, source directories, Wiki directories,
  three seed files, and exactly one setup operation.

The deterministic version of this procedure is covered by
`tests/test_project_resolver.py` and the subprocess-level
`tests/test_cli_flow.py`.

## External Source Snapshot

Use a temporary file outside the resolved project root and run
`import_source.py` with that file explicitly selected.

PASS requires:

- the first import returns `IMPORTED` and creates
  `sources/imported/<source-id>/<sha256>/<basename>`;
- the snapshot bytes and digest match the unchanged external original;
- a repeated import returns `NOOP`;
- changing the same external file creates a new digest directory under the same
  source ID and does not overwrite the old snapshot;
- symlinks, directories, invalid project roots, and common credential-like
  patterns fail closed;
- the Vault contains no external absolute source path.

The deterministic version of this procedure is covered by
`tests/test_import_source.py` and `tests/test_cli_flow.py`.

## Prepare

1. Copy `tests/fixtures/basic-project/baseline/wiki` and
   `tests/fixtures/basic-project/sources` into an isolated temporary directory.
2. Record SHA-256 for every source file.
3. Use the repository's `llm-wiki` skill for every operation after resolving the
   isolated temporary project root.

## Ingest And Reconcile

1. Ingest `architecture-v1.md`.
2. Ingest `protocol-review.md` and verify the conflict remains visible.
3. Ingest `architecture-v2.md` and verify the approved supersession.
4. Ingest `operational-notes.md`.
5. Ingest `architecture-v2.md` again and verify it is a no-op.

Compare the result with `expected/claim-register.md` and
`expected/required-relations.md`. Exact prose is not compared.

PASS requires:

- source hashes remain unchanged;
- all four claims and required evidence relationships are observable;
- all sourced claim blocks live in the Transport topic, while source notes remain
  limited to their own source;
- the existing Transport topic is updated instead of duplicated;
- claim IDs and source notes remain unique after repeated ingest;
- the index and operations log describe completed writes.

## Query And Crystallize

Ask:

> Which transports should public clients and internal high-throughput services use,
> and why?

PASS requires the answer to distinguish the approved public and internal policies,
mention the superseded recommendation, and cite supporting source locators.

Then ask:

> What is the maximum upload size?

PASS requires an explicit lack-of-evidence response. The operational note saying it
does not define the limit is not evidence for a numeric answer.

If the agent proposes crystallizing the transport comparison, approve it. PASS
requires one synthesis linked to the input claims and sources. No synthesis may be
written before approval.

## Lint And Repair

Create an isolated damaged copy of the generated wiki and introduce:

- one missing source path;
- one duplicate claim ID;
- one broken Markdown link;
- one derived claim based on a superseded claim but still marked `current`.

Run lint. PASS requires separate mechanical and semantic findings with stable IDs,
affected paths, evidence, and proposed repairs. The lint run must not change files.

Approve one finding ID only. PASS requires only the approved scope to change and a
single repair entry in `wiki/operations.md`.

## Evidence To Retain

- agent operation transcript;
- source hashes before and after;
- wiki tree before and after each phase;
- final diff;
- claim-to-evidence review against the oracle;
- lint report and approved repair diff.

The current repository retains these under `tests/evidence/`. The primary staged
basic-flow evidence is replayed by `tests/verify-phased-evidence.sh`; lint evidence
is checked by `tests/verify-lint-fixture.sh`.

Deterministic checks prove file integrity, uniqueness, link targets, and write
boundaries. A human or independent reviewer must still verify that evidence
actually supports each claim and that the synthesis is accurate.

## Source Replacement

Use `tests/fixtures/source-replacement/` in a fresh temporary directory:

1. Copy `baseline/` as the working root.
2. Confirm `sources/policy.md` matches `versions/policy-v1.md`.
3. Replace that same path with `versions/policy-v2.md` as an explicit user source
   update.
4. Ingest `sources/policy.md` and compare with `expected.md`.
5. Re-ingest unchanged v2 and verify a no-op.

PASS requires removed evidence to stop supporting a current claim, the old digest
and locator to remain as former evidence, and stale state to propagate to the
dependent synthesis.

## Source Path Boundary

Use `tests/fixtures/path-boundary/` in a fresh temporary directory. Query or lint
the seeded wiki.

PASS requires the agent to reject `source_path: ../outside.md` and the topic link
that canonically resolves outside `sources/` without reading `outside.md`.

For the symlink case, create a temporary symlink under `sources/` pointing to
`outside.md`. PASS requires the canonical target check to reject it. The valid
`sources/valid.md` file must remain readable.
