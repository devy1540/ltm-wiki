# LTM Wiki Instructions For Claude

Use this repository's LTM Wiki memory store as explicit long-term memory when you can read and write local files.

When the user invokes `/ltm-setup` or asks naturally to set up LTM Wiki, initialize long-term memory, connect AI memory, configure an Obsidian memory store, or says "ltm-wiki 초기셋팅", follow `commands/ltm-setup.md` when available.

Follow the same lifecycle:

Observe -> Triage -> Store -> Link -> Recall -> Consolidate -> Prune

Before using memory, read `.ltm-wiki/config.json`, then inspect `memory/index.md` and relevant pages. Do not assume Codex-specific skills or tools exist.
