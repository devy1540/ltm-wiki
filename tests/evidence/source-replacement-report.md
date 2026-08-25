# Sanitized Same-Path Source Replacement Record

Fixture: `tests/fixtures/source-replacement/`

User action before ingest:

> Replace `sources/policy.md` with policy v2, then ingest that same path.

Agent result:

- Detected the digest change at the existing source path.
- Rewrote the existing source note in place with the v2 digest.
- Removed current timeout evidence because v2 no longer supports it.
- Kept the 30-second claim visible as stale with the v1 digest and locator under
  Former evidence.
- Marked the dependent client-request synthesis stale.
- Added current platform-team ownership guidance from v2.
- Logged old/new digests, removed evidence, and both stale transitions.

Second user turn:

> Ingest unchanged `sources/policy.md` again.

Agent result:

> No-op. The path, digest, source note, and linked claims already match.

Retained artifacts:

- Final tree: `tests/fixtures/source-replacement/golden/`
- Final hashes: `tests/evidence/manifests/source-replacement-golden.sha256`
- Exact Wiki diff: `tests/evidence/source-replacement.diff`
