# Claude Profile

## Entry Point

- Instruction template: `templates/CLAUDE.ltm-wiki.md`

## Behavior

- File access depends on the Claude runtime.
- Should avoid Codex-specific tool assumptions.
- Should use targeted recall when local file access is available.
- Should ask before proactive memory writes unless the user has clearly opted into automatic capture.
