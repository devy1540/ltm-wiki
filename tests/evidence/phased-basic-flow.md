# Phased Basic-Flow Evidence

This is the primary auditable basic-flow record. One fresh agent executed one phase
at a time in the same isolated root and stopped after every phase. The parent
captured a complete Wiki manifest and reconstructable recursive diff before
allowing the next phase.

## Phase 00 — Baseline

The run started from `tests/fixtures/basic-project/baseline/wiki` with all four
fixture sources present and unchanged.

## Phase 01 — Architecture v1

- Created one source note.
- Updated the existing Transport topic rather than creating a duplicate.
- Added current public HTTP and bounded internal gRPC-experiment claims.

## Phase 02 — Protocol Review

- Added the unapproved global gRPC recommendation.
- Changed the public HTTP and global gRPC claims to `disputed`.
- Added mutual contradiction links.

## Phase 03 — Architecture v2

- Returned public HTTP to `current` with v2 evidence.
- Added current controlled-internal-gRPC policy.
- Changed the global gRPC recommendation to `superseded`.
- Preserved historical contradiction and both supersession directions.

Before the phase snapshot, the executor corrected an initial omission that had
removed historical `Contradicts` links. The retained delta contains the corrected
state required by the acceptance oracle.

## Phase 04 — Operational Notes

- Added source-only assertions and a Rollout Ownership topic.
- Linked the existing Transport topic to that materially related topic without
  duplicating claims.
- Recorded that upload size and retention remain unspecified; no value was
  invented.

Before the phase snapshot, the executor corrected an initial omission of the link
from Transport to Rollout Ownership. The retained delta contains the corrected
state.

## Phase 05 — Repeated Architecture v2

The unchanged source was a no-op. Only `wiki/operations.md` changed to record the
meaningful no-op; source notes, topics, index, and syntheses were unchanged.

## Phase 06 — Read-Only Queries

Supported query answer:

> Public clients use HTTP with JSON for compatibility with existing clients and
> debugging tools. Controlled internal high-throughput services may use gRPC. The
> earlier global gRPC-default recommendation is superseded.

Unsupported query answer:

> The maximum upload size is not defined by the Wiki or valid sources. Operational
> Notes explicitly leaves the limit unspecified, which is not evidence for a
> numeric answer.

The complete phase-05 and phase-06 manifests are byte-identical. No synthesis
existed before approval.

## Phase 07 — Explicit Crystallize Approval

After explicit approval, the agent created exactly one synthesis with a current
derived claim, links to the approved input topic claims, underlying source evidence,
and limitations. It updated the Transport topic, index, and operations without
modifying sources.

## Retained Artifacts

- Full-tree manifests: `tests/evidence/phases/manifests/`
- Reconstructable deltas: `tests/evidence/phases/deltas/`
- Source hashes: `tests/evidence/phases/sources.sha256`
- Deterministic replay: `tests/verify-phased-evidence.sh`
