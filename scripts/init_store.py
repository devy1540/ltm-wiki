#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from ltm_common import (
    REQUIRED_DIRS,
    SCHEMA_VERSION,
    StoreConfig,
    dump_config,
    ensure_supported_backend,
    write_text_if_missing,
)


def frontmatter(memory_type: str, title: str, status: str = "active") -> str:
    today = date.today().isoformat()
    return (
        "---\n"
        f"type: {memory_type}\n"
        f"status: {status}\n"
        f"created: {today}\n"
        f"updated: {today}\n"
        "sources: []\n"
        "tags: []\n"
        "aliases: []\n"
        "confidence: high\n"
        "provenance: system-generated\n"
        f"last_reviewed: {today}\n"
        "---\n"
        f"# {title}\n\n"
    )


def index_content(store_name: str) -> str:
    return (
        frontmatter("index", "Memory Index")
        + f"`{store_name}` long-term memory index.\n\n"
        + "## Core Pages\n\n"
        + "- [Overview](overview.md) - Store overview and operating notes.\n"
        + "- [Log](log.md) - Append-only memory operation log.\n\n"
        + "## Memory Areas\n\n"
        + "- [Sources](sources/) - Source-backed memory.\n"
        + "- [Episodes](episodes/) - Conversation and decision records.\n"
        + "- [Preferences](preferences/) - Stable user preferences.\n"
        + "- [Procedures](procedures/) - Reusable workflows.\n"
        + "- [Open Loops](open-loops/) - Questions, hypotheses, and unresolved decisions.\n"
        + "- [Entities](entities/) - People, organizations, projects, and objects.\n"
        + "- [Concepts](concepts/) - Definitions and durable concepts.\n"
        + "- [Syntheses](syntheses/) - Cross-source conclusions and theses.\n"
        + "- [Questions](questions/) - Durable answers and explorations.\n"
    )


def log_content() -> str:
    today = date.today().isoformat()
    return (
        frontmatter("log", "Memory Log")
        + f"## [{today}] bootstrap | Memory store initialized\n\n"
        + "- Operation: bootstrap\n"
        + "- Result: created initial LTM Wiki memory store structure.\n"
    )


def overview_content(store_name: str, backend: str) -> str:
    if backend == "obsidian":
        links = "- [[index]]\n- [[log]]\n"
    else:
        links = "- [Index](index.md)\n- [Log](log.md)\n"
    return (
        frontmatter("overview", "Memory Overview")
        + f"`{store_name}` uses the `{backend}` backend.\n\n"
        + "## Start Here\n\n"
        + links
        + "\n## Policy\n\n"
        + "- Raw sources are user-owned and should not be rewritten unless explicitly requested.\n"
        + "- Memory pages are agent-maintained and must preserve provenance and confidence.\n"
        + "- Sensitive data, secrets, and credentials are not stored.\n"
    )


def schema_content(backend: str) -> str:
    return (
        "# LTM Wiki Memory Schema\n\n"
        f"Backend: `{backend}`\n\n"
        + "Required memory metadata:\n\n"
        + "- `type`\n"
        + "- `status`\n"
        + "- `created`\n"
        + "- `updated`\n"
        + "- `sources`\n"
        + "- `tags`\n"
        + "- `aliases`\n"
        + "- `confidence`\n"
        + "- `provenance`\n"
        + "- `last_reviewed`\n\n"
        + "Memory types: source, semantic, episodic, procedural, preference, open-loop, synthesis, question, entity, concept.\n"
    )


def initialize_store(root: Path, backend: str, store_name: str, force: bool = False) -> list[str]:
    ensure_supported_backend(backend)
    created: list[str] = []
    for rel in REQUIRED_DIRS:
        path = root / rel
        path.mkdir(parents=True, exist_ok=True)
        created.append(str(path))

    config = StoreConfig(SCHEMA_VERSION, backend, store_name)
    files = {
        ".ltm-wiki/config.json": dump_config(config),
        "memory/index.md": index_content(store_name),
        "memory/log.md": log_content(),
        "memory/overview.md": overview_content(store_name, backend),
        "meta/schemas/ltm-wiki.md": schema_content(backend),
    }
    for rel, content in files.items():
        if write_text_if_missing(root / rel, content, force=force):
            created.append(str(root / rel))
    return created


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize an LTM Wiki memory store.")
    parser.add_argument("root", type=Path, help="Memory store root directory.")
    parser.add_argument("--backend", choices=["markdown-files", "obsidian"], default="markdown-files")
    parser.add_argument("--store-name", default="LTM Wiki")
    parser.add_argument("--force", action="store_true", help="Overwrite generated starter files.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    created = initialize_store(args.root, args.backend, args.store_name, force=args.force)
    print(f"initialized {args.backend} memory store at {args.root}")
    print(f"created_or_verified={len(created)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
