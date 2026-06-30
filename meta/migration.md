# LTM Wiki Schema Migration

Two files carry a `schemaVersion`:

- Store config — `<store>/.ltm-wiki/config.json`
- Global pointer — `~/.ltm-wiki/config.json`

Migrations are backward compatible where possible. The `ltm-wiki-maintenance`
checklist accepts both `0.1` and `0.2`, so an old store keeps working until you
migrate it.

## 0.1 → 0.2

What changed:

- Introduced the **global pointer** `~/.ltm-wiki/config.json`
  (`defaultStore`, `backend`, `sync`) so one store is reachable from every session.
- Store config `schemaVersion` bumped to `0.2`. The memory layout is unchanged.

Migrate an existing 0.1 store:

1. Keep the store as-is — the directory layout is compatible.
2. Bump `<store>/.ltm-wiki/config.json` `schemaVersion` to `0.2`.
3. Create `~/.ltm-wiki/config.json` with `defaultStore` pointing at the store, plus
   its `backend` and a `sync` value (`git` / `obsidian` / `none`). Spec:
   `meta/global-config.md`.
4. Install entry points if missing (see the `ltm-setup` skill).
5. Run the `ltm-wiki-maintenance` checklist to confirm.

## Adding a future version

- Append a `## X → Y` section describing field changes and migration steps.
- Keep accepting the previous version in the maintenance checklist for one cycle.
- Never rewrite `raw/` — migrate metadata and structure only, preserving provenance.
