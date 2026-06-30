# Optional Hooks

LTM Wiki needs **no hooks** — the skills already cover capture, recall, and
maintenance. These are optional conveniences. A hook is a shell command the agent
runs automatically, so it adds a small external dependency, which cuts against the
"no external runtime" goal. Use one only if the trade-off is worth it; skip both
for zero moving parts.

> A hook cannot summarize a conversation on its own (no LLM). Durable capture stays
> with the `ltm-wiki` ambient-capture skill. Hooks only help with sync and recall
> reminders.

## Git auto-sync (only for `sync: git` stores)

Commit memory changes when a session ends. Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "S=$(jq -r .defaultStore ~/.ltm-wiki/config.json); [ -d \"$S/.git\" ] && git -C \"$S\" add -A && git -C \"$S\" commit -m 'chore: sync memory' >/dev/null 2>&1 || true"
          }
        ]
      }
    ]
  }
}
```

For `obsidian` or `none` stores this is unnecessary — Obsidian Sync / iCloud
handles replication.

## Session-start memory reminder

Surface the store location at session start so recall stays top of mind:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "test -f ~/.ltm-wiki/config.json && echo \"LTM Wiki store: $(jq -r .defaultStore ~/.ltm-wiki/config.json)\""
          }
        ]
      }
    ]
  }
}
```

Edit hooks via your agent's settings (Claude Code: `~/.claude/settings.json`).
The exact hook schema is defined by your agent — treat these as templates.
