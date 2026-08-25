# Expected Lint Findings

The lint report must identify at least these seeded problems without modifying any
file:

## Mechanical

- `wiki/source-notes/missing-source.md` references a missing source path.
- `wiki/index.md` contains a broken link to `topics/does-not-exist.md`.
- `claim-transport-public-http` is duplicated in
  `wiki/topics/transport.md`.

## Semantic

- `claim-transport-global-grpc-recommendation` is marked `current` even though it derives from
  superseded `claim-transport-all-new-grpc`; it must be reported as stale.

Every finding needs a stable ID, affected path or claim, rule, evidence, and a
proposed repair. The report must keep mechanical and semantic sections separate.
