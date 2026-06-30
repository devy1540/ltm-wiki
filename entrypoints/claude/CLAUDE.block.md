<!-- ltm-wiki:begin -->
## LTM Wiki Long-Term Memory

You have a persistent, user-owned memory store. Resolve it by reading
`~/.ltm-wiki/config.json` and using its `defaultStore` path — or a local
`.ltm-wiki/config.json` if the current project has one.

- **Recall** relevant memory before answering when prior context may matter (use
  the `ltm-wiki-recall` skill, or grep the store's `memory/` directory).
- **Capture** durable, low-risk knowledge (preferences, decisions, procedures,
  findings, open questions) without being asked; ask first for sensitive,
  personal, ambiguous, or high-volume writes.
- If the store's `sync` is `git`, pull before relying on memory and commit after
  durable writes.
- Never store secrets, credentials, private keys, tokens, or content the user
  says not to remember.
<!-- ltm-wiki:end -->
