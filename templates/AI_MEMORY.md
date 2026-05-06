# Portable AI Memory Instructions

This project uses LTM Wiki as user-owned long-term memory.

When the user asks to set up LTM Wiki, initialize long-term memory, connect AI memory, configure Obsidian memory, or says "ltm-wiki 초기셋팅", use the `ltm-setup` procedure: download or update the repository, run `scripts/setup.py`, then verify with `memory_doctor.py`.

Minimum agent capabilities:

- read local or connected memory files
- write markdown memory pages when allowed
- preserve raw sources
- keep provenance and confidence metadata
- avoid storing secrets

Recall relevant memory before answering when prior context may affect the result.
