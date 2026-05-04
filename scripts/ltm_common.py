from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

SCHEMA_VERSION = "0.1"
SUPPORTED_BACKENDS = {"markdown-files", "obsidian"}

MEMORY_DIRS = [
    "memory/sources",
    "memory/episodes",
    "memory/preferences",
    "memory/procedures",
    "memory/open-loops",
    "memory/entities",
    "memory/concepts",
    "memory/syntheses",
    "memory/questions",
]

REQUIRED_DIRS = [
    ".ltm-wiki",
    "raw/sources",
    "raw/assets",
    "memory",
    "meta/prompts",
    "meta/schemas",
    *MEMORY_DIRS,
]

REQUIRED_FILES = [
    ".ltm-wiki/config.json",
    "memory/index.md",
    "memory/log.md",
    "memory/overview.md",
    "meta/schemas/ltm-wiki.md",
]


@dataclass(frozen=True)
class StoreConfig:
    schema_version: str
    backend: str
    store_name: str


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "memory"


def ensure_supported_backend(backend: str) -> None:
    if backend not in SUPPORTED_BACKENDS:
        allowed = ", ".join(sorted(SUPPORTED_BACKENDS))
        raise ValueError(f"unsupported backend '{backend}', expected one of: {allowed}")


def config_path(root: Path) -> Path:
    return root / ".ltm-wiki" / "config.json"


def write_text_if_missing(path: Path, content: str, force: bool = False) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def load_config(root: Path) -> StoreConfig:
    data = json.loads(config_path(root).read_text(encoding="utf-8"))
    return StoreConfig(
        schema_version=str(data["schemaVersion"]),
        backend=str(data["backend"]),
        store_name=str(data["storeName"]),
    )


def dump_config(config: StoreConfig) -> str:
    return json.dumps(
        {
            "schemaVersion": config.schema_version,
            "backend": config.backend,
            "storeName": config.store_name,
        },
        indent=2,
        ensure_ascii=False,
    ) + "\n"


def iter_markdown_files(root: Path, include_raw: bool = False) -> Iterable[Path]:
    roots = [root / "memory", root / "meta"]
    if include_raw:
        roots.append(root / "raw")
    for base in roots:
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.md")):
            if path.is_file():
                yield path


def has_frontmatter(text: str) -> bool:
    return text.startswith("---\n") and "\n---\n" in text[4:]
