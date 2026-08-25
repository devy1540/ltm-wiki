# Wiki Operations

## 2026-01-01 | setup | Client Policy fixture

- Created: sources/, wiki/source-notes/, wiki/topics/, wiki/syntheses/
- Result: initialized the source-replacement baseline

## 2026-08-24 | ingest | sources/policy.md

- Updated: wiki/source-notes/policy.md, wiki/topics/client-policy.md, wiki/syntheses/client-request-behavior.md
- Source replacement: sha256:1e5a4a8b80c727eec7905a96f8a122914d14fffb4f3b3dd1e11845eb700b5d9e -> sha256:9b721fb2d9dfe360bdc38283e54ac3677962c040f6f9b4bbae63e1052cc0cf61
- Removed evidence: `claim-client-timeout-30-seconds` no longer has heading "Timeout", lines 3-5 support.
- **Former evidence:**
  - **Source:** [Client Policy](../sources/policy.md)
  - **Digest:** sha256:1e5a4a8b80c727eec7905a96f8a122914d14fffb4f3b3dd1e11845eb700b5d9e
  - **Locator:** heading "Timeout", lines 3-5
- Claim transitions: `claim-client-timeout-30-seconds` current -> stale; `claim-client-request-behavior` current -> stale.
- Result: rewrote the existing source note with the replacement's ownership guidance and retained removed timeout evidence as historical context.

## 2026-08-24 | ingest | sources/policy.md

- Created: none
- Updated: none
- Result: no-op; the source path and SHA-256 digest already matched the existing source note, and its linked topic claims still exist.
