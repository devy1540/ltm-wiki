# Codex Profile

## Entry Point

- Codex plugin manifest: `.codex-plugin/plugin.json`
- Skills directory: `skills/`
- Project instruction template: `templates/AGENTS.ltm-wiki.md`

## Behavior

- Can read and write local files.
- Can run Python scripts.
- Should use targeted recall before answering when memory is likely relevant.
- May do low-risk ambient capture, then mention the changed path.
- Must ask before sensitive, personal, ambiguous, or high-volume memory writes.
