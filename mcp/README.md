# LTM Wiki MCP Server (optional)

An **opt-in** MCP server that exposes the LTM Wiki memory store over stdio, so a
client that can't read the store files directly still gets structured read/write
access. LTM Wiki works fully without it — this is a choice, not a requirement.

## Scope

- **Local stdio only.** The server runs on the machine that holds the store and is
  launched by a local MCP client (Claude Desktop/Code). Remote (web/mobile) use
  would need hosting + auth and is out of scope for now.
- **Same SSOT as the files.** It resolves the store the way the skills do — a local
  `.ltm-wiki/config.json`, else `~/.ltm-wiki/config.json` → `defaultStore` — and
  reads/writes the same markdown. The file path and the MCP path never diverge.

## Build

```bash
cd mcp
npm install
npm run build
```

## Register (this is the opt-in step)

Add it to your client's MCP config — e.g. Claude Code `~/.claude.json` or a
project `.mcp.json`:

```json
{
  "mcpServers": {
    "ltm-wiki": {
      "command": "node",
      "args": ["/absolute/path/to/ltm-wiki/mcp/dist/index.js"]
    }
  }
}
```

The plugin manifests do **not** register this server, so installing the LTM Wiki
plugin never turns it on. You enable it here, deliberately.

## Tools

| Tool | Purpose |
|---|---|
| `ltm_status` | active store path, backend, sync, page count |
| `ltm_recall` | keyword search (optional type filter, ranked) |
| `ltm_get` | read one page by slug or store-relative path |
| `ltm_list` | list active pages (optional type filter) |
| `ltm_capture` | create a memory page (frontmatter, slug, log entry); rejects secrets |
| `ltm_log` | append an entry to `memory/log.md` |

## Safety

`ltm_capture` runs the same secret scan as the skills and never writes under
`raw/`. Because it operates on the same store, nothing about the file-based
workflow changes — MCP is just a second door to the same room.
