# Sanitized Lint Report And Repair Record

Fixture: `tests/fixtures/basic-project/lint-seed/`

The read-only lint pass produced the following report.

## Mechanical Findings

### LWM-MS-001 — Missing source

- Severity: high
- Target: `wiki/source-notes/missing-source.md`
- Rule: a source note must reference a real source inside `sources/`.
- Evidence: `source_path: sources/missing-source.md`; no such file exists.
- Proposed repair: restore the source or approve removal/correction of the note.

### LWM-ML-002 — Broken index link

- Severity: high
- Target: `wiki/index.md`
- Rule: index links must resolve to managed pages.
- Evidence: `topics/does-not-exist.md` is absent.
- Proposed repair: remove the link or create an approved topic.

### LWM-MC-003 — Duplicate claim ID

- Severity: high
- Target: `wiki/topics/transport.md`
- Rule: claim IDs are unique across the Wiki.
- Evidence: `claim-transport-public-http` appears twice.
- Proposed repair: merge the duplicate or assign a distinct ID after review.

## Semantic Findings

### LWM-SS-004 — Stale state did not propagate

- Severity: high
- Target: `claim-transport-global-grpc-recommendation`
- Rule: a derived claim depending on superseded input is stale until reviewed.
- Evidence: the synthesis is `current` but derives from superseded
  `claim-transport-all-new-grpc`.
- Proposed repair: mark the synthesis stale and review its conclusion.

## Read-Only Proof

`tests/evidence/manifests/lint-pre.sha256` and
`tests/evidence/manifests/lint-post-readonly.sha256` are byte-identical. No Wiki or
source file changed during lint.

## Scoped Repair Exchange

User:

> Approve only `LWM-ML-002`. Remove the broken index link and do not repair any
> other finding.

Agent result:

- Removed only `topics/does-not-exist.md` from `wiki/index.md`.
- Added one repair entry to `wiki/operations.md`.
- Left the missing source, duplicate claim ID, and stale-state defect unchanged.

Retained artifacts:

- Repaired tree: `tests/fixtures/basic-project/lint-repaired/`
- Repaired hashes: `tests/evidence/manifests/lint-repaired.sha256`
- Exact repair diff: `tests/evidence/lint-repair.diff`
