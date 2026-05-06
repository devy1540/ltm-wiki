# LTM Wiki Agent Instructions

Use LTM Wiki as explicit user-owned long-term memory.

## Setup

When the user invokes `$ltm-setup` or asks naturally to set up LTM Wiki, initialize long-term memory, connect AI memory, configure an Obsidian memory store, or says "ltm-wiki 초기셋팅", follow the `ltm-setup` workflow.

## Before Acting

Check memory when the current request relates to an existing project, preference, open loop, source-backed topic, or repeated workflow.

Read:

- `.ltm-wiki/config.json`
- `memory/index.md`
- recent entries in `memory/log.md`

Search targeted memory with `scripts/search_memory.py` when available.

## Remember

Capture durable knowledge from conversation when it is stable and useful:

- preferences
- project decisions
- definitions
- source-backed findings
- unresolved questions
- reusable procedures
- synthesis across sources

Do not store secrets, credentials, private keys, or content the user says not to remember.

## Write Policy

For low-risk durable notes, update memory and briefly mention the changed path. Ask first for sensitive, ambiguous, personal, or high-volume memory writes.
