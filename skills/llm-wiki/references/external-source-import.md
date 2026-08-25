# External Source Snapshot Import

Use when the user explicitly identifies a file as LLM Wiki source evidence and the
file is outside the resolved project's `sources/` directory.

Run from the installed skill directory:

```bash
python3 scripts/import_source.py \
  --project-root "<resolved-project-root>" \
  --source "<explicitly-selected-file>" \
  --json
```

Interpret `status`:

- `IMPORTED`: ingest the returned project-relative `sourcePath`.
- `NOOP`: the identical immutable snapshot already exists; reuse it.
- `ALREADY_LOCAL`: the selected regular file is already inside project `sources/`;
  ingest the returned relative path without copying.
- `SOURCE_REJECTED_SENSITIVE`: stop. Do not copy credential/private-key material
  into a Vault that may sync.
- `INVALID_SOURCE`, `INVALID_PROJECT_ROOT`, `TARGET_CONFLICT`, `LOCKED`, or
  `DIGEST_MISMATCH`: fail closed and report the status.

The importer accepts only an explicitly selected regular non-symlink file. It
copies bytes into:

```text
sources/imported/<source-id>/<sha256>/<safe-basename>
```

It verifies the copy digest and activates it with an atomic rename. Snapshots are
content-addressed and never overwritten or deleted. A changed file at the same
external path keeps its logical `sourceId` and creates a new digest directory.

Do not write the external absolute path into the Vault, source note, Wiki, or
operations log. Use only the returned `sourceId`, project-relative `sourcePath`,
and SHA-256 digest. The machine-local command output may contain only the hashed
origin identity.

Import permission is not ambient: merely opening, reading, editing, or mentioning a
project file does not select it as Wiki evidence. The user's request must identify
the file as a durable source or ask for it to be added to the Wiki.
