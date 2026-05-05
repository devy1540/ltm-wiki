#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from ltm_common import (
    REQUIRED_DIRS,
    REQUIRED_FILES,
    SUPPORTED_BACKENDS,
    has_frontmatter,
    iter_markdown_files,
    load_config,
)

MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+\.md)\)")


def check_required_paths(root: Path) -> list[str]:
    issues: list[str] = []
    for rel in REQUIRED_DIRS:
        if not (root / rel).is_dir():
            issues.append(f"missing required directory: {rel}")
    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            issues.append(f"missing required file: {rel}")
    return issues


def check_config(root: Path) -> list[str]:
    try:
        config = load_config(root)
    except Exception as exc:
        return [f"invalid config: {exc}"]
    if config.schema_version != "0.1":
        return [f"unsupported schemaVersion: {config.schema_version}"]
    if config.backend not in SUPPORTED_BACKENDS:
        return [f"unsupported backend: {config.backend}"]
    return []


def check_frontmatter(root: Path) -> list[str]:
    issues: list[str] = []
    for path in iter_markdown_files(root):
        rel = path.relative_to(root)
        if rel.as_posix() == "memory/log.md":
            continue
        if not has_frontmatter(path.read_text(encoding="utf-8")):
            issues.append(f"missing frontmatter: {rel.as_posix()}")
    return issues


def check_markdown_links(root: Path) -> list[str]:
    issues: list[str] = []
    for path in iter_markdown_files(root):
        text = path.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                continue
            if not resolved.exists():
                rel = path.relative_to(root).as_posix()
                issues.append(f"broken markdown link: {rel} -> {target}")
    return issues


def doctor(root: Path) -> list[str]:
    issues: list[str] = []
    issues.extend(check_required_paths(root))
    if (root / ".ltm-wiki" / "config.json").exists():
        issues.extend(check_config(root))
    issues.extend(check_frontmatter(root))
    issues.extend(check_markdown_links(root))
    return issues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check an LTM Wiki memory store.")
    parser.add_argument("root", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    issues = doctor(args.root)
    if not issues:
        print("OK: memory store health checks passed")
        return 0
    for issue in issues:
        print(issue)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
