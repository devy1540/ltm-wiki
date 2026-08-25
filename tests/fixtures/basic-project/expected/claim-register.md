# Expected Claim Register

This is the semantic oracle for the basic MVP fixture. Generated prose may differ,
but these claims and evidence relationships must remain observable.

All four sourced claim blocks are owned by `wiki/topics/transport.md`. Source notes
summarize only their own source and link their assertions to these topic claims.

## `transport-public-http`

- Kind: sourced
- Final state: current
- Statement: Public client integrations use HTTP with JSON payloads.
- Evidence:
  - `sources/architecture-v1.md`, heading `Public transport`
  - `sources/architecture-v2.md`, heading `Approved decision`

## `transport-all-new-grpc`

- Kind: sourced
- Final state: superseded
- Statement: gRPC should be the default for every new public and internal
  integration.
- Evidence:
  - `sources/protocol-review.md`, heading `Recommendation`
- Relations:
  - Contradicts `transport-public-http`
  - Superseded by the approved decision in `architecture-v2.md`
  - The approved public and internal claims link back with `Supersedes`

## `transport-internal-grpc`

- Kind: sourced
- Final state: current
- Statement: Controlled internal high-throughput services may use gRPC.
- Evidence:
  - `sources/architecture-v2.md`, heading `Approved decision`

## `transport-rollout-owner`

- Kind: sourced
- Final state: current
- Statement: The platform team owns the transport migration checklist.
- Evidence:
  - `sources/operational-notes.md`, heading `Rollout ownership`
