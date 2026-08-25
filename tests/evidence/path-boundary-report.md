# Sanitized Source Path Boundary Record

Fixture: `tests/fixtures/path-boundary/`

A fresh security-oriented agent discovered the repository skill and ran read-only
lint plus a query against the seeded invalid claim.

## Canonical Path Results

```text
valid sources/valid.md: inside canonical sources -> allowed
wiki evidence ../../outside.md: outside canonical sources -> rejected
sources/escape.md symlink target: outside canonical sources -> rejected
source_path ../outside.md: invalid frontmatter path -> rejected before read
```

## Query

User:

> Can `claim-boundary-invalid` be substantiated from its evidence?

Agent:

> No. Its only evidence target resolves outside the canonical `sources/` boundary,
> so it cannot be read or used as evidence. The valid source is not linked to this
> claim and does not independently substantiate it.

## Read-Only Proof

The independent run recorded identical pre/post state aggregates:

```text
abe7b452550c66149d7144948d2e23b36f9d99c02587760434700735a5fcb5c0
```

The aggregate used allowed-file hashes and metadata for the forbidden outside file
and symlink; forbidden file contents were not read. Deterministic canonical-path
checks are retained in `tests/verify-path-boundary.sh`.
