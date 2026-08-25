# Expected Source Replacement Result

Replace `baseline/sources/policy.md` with `versions/policy-v2.md` at the same path,
then ingest `sources/policy.md`.

PASS requires:

- `wiki/source-notes/policy.md` is rewritten in place with digest
  `sha256:9b721fb2d9dfe360bdc38283e54ac3677962c040f6f9b4bbae63e1052cc0cf61`.
- The source note no longer asserts a 30-second timeout and does not gain a second
  page.
- `claim-client-timeout-30-seconds` remains visible but becomes `stale` because the
  replacement no longer supports it.
- The old digest and `Timeout` locator remain under `Former evidence`.
- `claim-client-request-behavior` becomes `stale` because its input became stale.
- Current ownership guidance may be added as a new sourced topic claim with v2
  evidence.
- `operations.md` records old/new digests, removed timeout evidence, and both stale
  claim transitions.
- Re-ingesting unchanged v2 is a no-op.
