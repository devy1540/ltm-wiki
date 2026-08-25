# Project Resolution And Automatic Provisioning

Use this workflow at the start of every `llm-wiki` task. Automatic provisioning
creates an empty project Wiki skeleton; it does not authorize ambient capture.

## Resolve

From the installed skill directory, run:

```bash
python3 scripts/project_resolver.py resolve \
  --cwd "<current-workspace-root>" \
  --create \
  --json
```

Interpret the JSON `status`:

- `READY`: use only the returned `projectRoot` and continue the original task in
  the same turn. `created: true` means the skeleton was just provisioned. When a
  Vault was auto-selected on first use, mention once that Wiki files and imported
  snapshots may follow that Vault's Obsidian Sync settings; do not pause the task.
- `VAULT_SELECTION_REQUIRED`: run `discover-vaults`, show the accessible Vault
  names and paths, ask the user once, then run `configure --vault` and repeat
  `resolve --create` in the same task.
- `OBSIDIAN_NOT_CONFIGURED` or `NO_ACCESSIBLE_VAULT`: ask for an existing Obsidian
  Vault folder once, configure it, then resume. Do not create an arbitrary Vault.
- `AUTO_PROVISION_DISABLED`: report the configured boundary and ask before changing
  it. The skill does not silently override config.
- `NOT_PROVISIONED`: occurs only when resolution was requested without `--create`.
- `AMBIGUOUS_PROJECT_MAPPING`, `MARKER_MISMATCH`, `HASH_COLLISION`, `TARGET_CONFLICT`,
  `UNSAFE_TARGET`, `LOCKED`, `CONFIG_INVALID`, `PROJECT_IDENTITY_UNAVAILABLE`, or
  `INVALID_*`: fail closed and report the exact status. Do not choose another
  directory or modify data.

To list candidates:

```bash
python3 scripts/project_resolver.py discover-vaults --json
```

To store the user's one-time choice:

```bash
python3 scripts/project_resolver.py configure \
  --vault "<selected-vault-path>" \
  --json
```

## Resulting Layout

```text
<Obsidian Vault>/
  LLM Wiki/
    projects/
      <project-name>--<identity-hash>/
        .llm-wiki.json
        sources/
          imported/
        wiki/
```

One Vault contains many isolated project Wikis. Never search sibling project
directories. A project query is confined to the single returned `projectRoot`.

## Identity

The resolver derives identity from the Git remote when possible, then the
filesystem identity of the Git common directory or non-Git project directory.
Equivalent SSH/HTTPS remotes and Git worktrees reuse one project Wiki. Remote
hosts are case-normalized; paths retain case except on explicitly known
case-insensitive hosts such as GitHub, and non-default ports remain part of the
identity. Different remotes with the same basename remain separate. Path strings
alone are never identity aliases, so deleting and recreating a project at the same
path cannot silently adopt the previous Wiki. Only identity hashes are stored;
raw Git remotes are not written into the Vault.

## Global Config

The resolver keeps one machine-local JSON config:

- Windows: `%APPDATA%/llm-wiki/config.json`
- Other platforms: `${XDG_CONFIG_HOME:-$HOME/.config}/llm-wiki/config.json`

It stores the canonical default Vault path, the relative projects directory,
`autoProvision`, and hashed project aliases. It is written atomically and uses
mode `0600` on POSIX. It is not synced through Obsidian.

Obsidian's own registered-Vault metadata is used only as best-effort discovery.
One accessible registered Vault may be selected automatically. Multiple Vaults
always require one explicit choice; undocumented `open` or timestamp fields are
never used as authority.

## Compatibility

An explicitly supplied Wiki root wins. An existing ancestor root containing
`sources/` and `wiki/schema.md` remains usable as a legacy project Wiki and is not
automatically moved or deleted.
