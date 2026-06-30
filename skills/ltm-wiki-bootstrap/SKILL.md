---
name: ltm-wiki-bootstrap
description: Use when creating, initializing, bootstrapping, repairing the initial structure of, or choosing a backend for an LTM Wiki long-term memory store, including markdown-files and Obsidian stores.
---

# LTM Wiki Bootstrap

Initialize an LTM Wiki memory store by creating files directly — no script.

## Workflow

1. Choose backend:
   - `markdown-files` by default.
   - `obsidian` when the user works in an Obsidian context or asks for it.
2. Create the directory skeleton (full spec: `meta/store-structure.md`):
   ```bash
   mkdir -p "<store>/.ltm-wiki" \
            "<store>/memory"/{sources,episodes,preferences,procedures,open-loops,entities,concepts,syntheses,questions} \
            "<store>/raw"/{sources,assets} \
            "<store>/meta"/{prompts,schemas}
   ```
3. Write the seed files exactly as specified in `meta/store-structure.md`:
   - `.ltm-wiki/config.json` (set `backend`, `storeName`, `schemaVersion: "0.2"`)
   - `memory/index.md`, `memory/log.md`, `memory/overview.md`
   - `meta/schemas/ltm-wiki.md`

   Use today's date for `created` / `updated` / `last_reviewed`. For the
   `obsidian` backend use wikilinks (`[[index]]`) in `overview.md`.
4. Verify with the `ltm-wiki-maintenance` checklist.
5. Tell the user the store root, backend, and key starter files.

To also make this store reachable from every session (global pointer + agent
entry points), use `ltm-setup` instead of bootstrapping alone.
