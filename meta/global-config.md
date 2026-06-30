# LTM Wiki Global Pointer

The global pointer is what makes one memory store reachable from **any** session,
project, or environment. It is a single agent-agnostic file that records where the
store lives and how it syncs.

## Location

```
~/.ltm-wiki/config.json
```

One file per machine. It does not hold memory — only the location of the store
(the single source of truth) plus the sync method.

## Schema

```json
{
  "schemaVersion": "0.2",
  "defaultStore": "/absolute/path/to/store",
  "backend": "markdown-files",
  "sync": "git"
}
```

- `defaultStore`: absolute path to the memory store root (the SSOT).
- `backend`: `markdown-files` | `obsidian`.
- `sync`: `git` | `obsidian` | `none` — how the store replicates across machines.

## Store Resolution Order

When an entry point or skill needs the active store, resolve in this order and
stop at the first hit:

1. **Local store** — `.ltm-wiki/config.json` in the current working directory or
   a parent. Use this when a project keeps its own dedicated memory.
2. **Global store** — `defaultStore` from `~/.ltm-wiki/config.json`. This is the
   default for ordinary sessions, so the same memory is reachable everywhere.

If neither exists, the store has not been set up — run `ltm-setup`.

## Idempotent Updates

`ltm-setup` writes or rewrites this file. Writing it again with the same values is
a no-op; pointing it at a new path simply changes `defaultStore`. Never duplicate
the file or append to it — it is a single JSON object.

## Sync Notes

- `git`: the store directory is a git repository with a remote. Pull before a
  session that may rely on memory; commit and push after durable writes.
- `obsidian`: the store is an Obsidian vault; replication is handled by Obsidian
  Sync / iCloud / the user's chosen mechanism. No git actions are required.
- `none`: single machine, no replication yet. Can be upgraded to `git` later.
