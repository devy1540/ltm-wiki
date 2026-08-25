# Sanitized Basic-Flow Transcript

Fixture: `tests/fixtures/basic-project/`

This is the user/agent exchange retained from the fresh forward test. Tool output is
represented by the committed operation log, final diff, and hash manifest.

## Turn 1 — Ingest Architecture v1

User:

> Ingest `sources/architecture-v1.md` into this LLM Wiki.

Agent result:

- Created `wiki/source-notes/architecture-v1.md`.
- Updated the existing `wiki/topics/transport.md`; no duplicate topic was created.
- Recorded the public HTTP policy and bounded internal gRPC experimentation.
- Updated index and operations.

## Turn 2 — Ingest Protocol Review

User:

> Ingest `sources/protocol-review.md` and reconcile it with existing knowledge.

Agent result:

- Created the source note.
- Preserved the conflicting global gRPC recommendation instead of replacing public
  HTTP guidance.
- Marked the unresolved relationship and linked both claims.

## Turn 3 — Ingest Architecture v2

User:

> Ingest `sources/architecture-v2.md` and apply any explicit supersession.

Agent result:

- Added v2 evidence to the public HTTP claim.
- Added the controlled internal gRPC claim.
- Kept the global gRPC recommendation as superseded with bidirectional relations.

## Turn 4 — Ingest Operational Notes

User:

> Ingest `sources/operational-notes.md`.

Agent result:

- Added platform-team rollout ownership to the Transport topic.
- Preserved the explicit absence of an upload-size rule as an evidence gap, not as
  a numeric claim.

## Turn 5 — Repeat Architecture v2

User:

> Ingest `sources/architecture-v2.md` again.

Agent result:

> No-op. The source path and SHA-256 digest match, its source note exists, and all
> referenced claims remain present.

No duplicate source note or claim was created.

## Turn 6 — Supported Query

User:

> Which transports should public clients and internal high-throughput services use,
> and why?

Agent:

> Public clients should use HTTP with JSON because the approved policy preserves
> compatibility with existing clients and debugging tools. Internal high-throughput
> services may use gRPC when both endpoints are controlled by the team. The earlier
> recommendation to make gRPC the default for every integration is superseded.

Evidence used:

- `architecture-v1.md`, heading `Public transport`, lines 5–8.
- `architecture-v2.md`, heading `Approved decision`, lines 5–12.
- `protocol-review.md`, heading `Recommendation`, lines 5–9.

## Turn 7 — Unsupported Query

User:

> What is the maximum upload size?

Agent:

> The available evidence does not define a maximum upload size. Operational Notes
> explicitly says it does not define the limit, which is not evidence for a numeric
> answer.

## Turn 8 — Crystallize Approval

Agent proposal:

> I can preserve the supported transport comparison as
> `wiki/syntheses/transport-comparison.md`, derived from the approved public and
> internal topic claims. Shall I write it?

User:

> Yes, crystallize that comparison.

Agent result:

- Created one derived synthesis.
- Linked its input claim anchors and raw source evidence.
- Updated the Transport topic, index, and operations.

## Retained Evidence

- Final tree: `tests/fixtures/basic-project/golden/`
- Source and tree hashes: `tests/evidence/manifests/basic-golden.sha256`
- Final Wiki diff: `tests/evidence/basic-flow.diff`
- Semantic oracle: `tests/fixtures/basic-project/expected/claim-register.md`
