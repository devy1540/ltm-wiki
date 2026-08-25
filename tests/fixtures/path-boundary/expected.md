# Expected Boundary Result

- Query and lint must not read `outside.md` as evidence.
- `source_path: ../outside.md` is invalid because it contains parent traversal and
  does not begin with `sources/`.
- The topic evidence link canonically resolves outside `sources/` and is invalid.
- A symlink created inside `sources/` that resolves to `outside.md` must also be
  rejected.
- The valid `sources/valid.md` file remains readable.
