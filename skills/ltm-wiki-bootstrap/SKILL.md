---
name: ltm-wiki-bootstrap
description: Use when creating, initializing, bootstrapping, repairing the initial structure of, or choosing a backend for an LTM Wiki long-term memory store, including markdown-files and Obsidian stores.
---

# LTM Wiki Bootstrap

Initialize an LTM Wiki memory store.

## Workflow

1. Choose backend:
   - Use `markdown-files` by default.
   - Use `obsidian` when the user is working in an Obsidian context or asks for Obsidian.
2. Run `python3 scripts/init_store.py <root> --backend <backend> --store-name <name>`.
3. Verify with `python3 scripts/memory_doctor.py <root>`.
4. Tell the user the memory store root, backend, and important starter files.
