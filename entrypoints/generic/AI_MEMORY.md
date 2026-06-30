# AI Long-Term Memory (LTM Wiki)

This project uses LTM Wiki as user-owned long-term memory. No external runtime is
required — read and write markdown directly.

## Find The Store

1. Local `.ltm-wiki/config.json` in this project or a parent directory.
2. Else `defaultStore` in `~/.ltm-wiki/config.json` (the global pointer).
3. If neither exists, run LTM Wiki setup (`ltm-setup`).

## Use It

- **Recall** before answering when prior context may matter: read
  `memory/index.md`, then grep `memory/` for the topic; open the smallest useful
  set of pages.
- **Remember** durable knowledge (preferences, decisions, definitions,
  source-backed findings, open questions, procedures, syntheses) with full
  frontmatter under `memory/`, and append to `memory/log.md`.
- **Preserve** `raw/` sources; keep provenance and confidence metadata.
- If `sync` is `git`, pull before relying on memory and commit after durable writes.

Never store secrets, credentials, private keys, tokens, or content the user says
not to remember.
