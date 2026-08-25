# Setup Workflow

Normal project setup is automatic through `project_resolver.py resolve --create`.
Use this workflow for the one-time Vault choice, an explicit Wiki root, or setup
diagnostics.

1. Run the resolver as described in
   [project-resolution.md](project-resolution.md).
2. If multiple registered Vaults are accessible, show their local folder names and
   paths and ask the user once. Never infer from undocumented recency or `open`
   fields.
3. Before configuring a Vault, state that imported source snapshots and derived
   Wiki pages live inside it and may be included in Obsidian Sync.
4. Configure only the selected existing folder with `.obsidian/`, then rerun
   `resolve --create` and continue the original task.
5. For an explicit non-Obsidian Wiki root, preserve the existing compatibility
   path. Do not move it into the Vault without a separate migration approval.
6. Verify the returned root contains `.llm-wiki.json`, empty `sources/imported/`,
   the Wiki subdirectories, seed files, and exactly one setup operation.

Automatic setup never scans the Vault, imports existing notes, or saves the current
conversation. It only creates the isolated project skeleton and registry binding.
