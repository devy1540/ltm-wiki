#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from init_store import initialize_store
from ltm_common import write_text_if_missing
from memory_doctor import doctor

REPO_ROOT = Path(__file__).resolve().parents[1]

AGENT_TEMPLATES = {
    "codex": [
        ("templates/AGENTS.ltm-wiki.md", "AGENTS.ltm-wiki.md"),
    ],
    "claude": [
        ("templates/CLAUDE.ltm-wiki.md", "CLAUDE.ltm-wiki.md"),
        ("adapters/claude/commands/ltm-setup.md", ".claude/commands/ltm-setup.md"),
    ],
    "generic": [
        ("templates/AI_MEMORY.md", "AI_MEMORY.md"),
    ],
}


@dataclass(frozen=True)
class SetupResult:
    root: Path
    backend: str
    store_name: str
    agents: tuple[str, ...]
    initialized_count: int
    installed_files: tuple[str, ...]
    doctor_issues: tuple[str, ...]


def expand_agents(agent_args: list[str] | None) -> tuple[str, ...]:
    requested = agent_args or ["codex"]
    if "all" in requested:
        return ("codex", "claude", "generic")
    deduped: list[str] = []
    for agent in requested:
        if agent not in deduped:
            deduped.append(agent)
    return tuple(deduped)


def install_agent_templates(root: Path, agents: tuple[str, ...], force: bool = False) -> list[str]:
    installed: list[str] = []
    for agent in agents:
        for source_rel, target_rel in AGENT_TEMPLATES[agent]:
            source = REPO_ROOT / source_rel
            target = root / target_rel
            content = source.read_text(encoding="utf-8")
            if write_text_if_missing(target, content, force=force):
                installed.append(target_rel)
    return installed


def setup(root: Path, backend: str, store_name: str, agents: tuple[str, ...], force: bool = False) -> SetupResult:
    initialized = initialize_store(root, backend, store_name, force=force)
    installed = install_agent_templates(root, agents, force=force)
    issues = doctor(root)
    return SetupResult(
        root=root,
        backend=backend,
        store_name=store_name,
        agents=agents,
        initialized_count=len(initialized),
        installed_files=tuple(installed),
        doctor_issues=tuple(issues),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Set up an LTM Wiki memory store and agent entry points.")
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd(), help="Memory store root. Defaults to cwd.")
    parser.add_argument("--backend", choices=["markdown-files", "obsidian"], default="markdown-files")
    parser.add_argument("--store-name", default="LTM Wiki")
    parser.add_argument(
        "--agent",
        choices=["codex", "claude", "generic", "all"],
        action="append",
        help="Agent instructions to install. Repeatable. Defaults to codex.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite generated store and agent template files.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    agents = expand_agents(args.agent)
    result = setup(args.root, args.backend, args.store_name, agents, force=args.force)
    print(f"root={result.root}")
    print(f"backend={result.backend}")
    print(f"store_name={result.store_name}")
    print(f"agents={','.join(result.agents)}")
    print(f"initialized_or_verified={result.initialized_count}")
    print(f"installed_files={len(result.installed_files)}")
    for rel in result.installed_files:
        print(f"installed: {rel}")
    if result.doctor_issues:
        print("doctor=failed")
        for issue in result.doctor_issues:
            print(issue)
        return 1
    print("doctor=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
