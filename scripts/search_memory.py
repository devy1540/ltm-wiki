#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

from ltm_common import iter_markdown_files


@dataclass(frozen=True)
class Match:
    score: int
    path: Path
    line: int
    excerpt: str


def tokenize(query: str) -> list[str]:
    return [token for token in re.findall(r"[A-Za-z0-9가-힣_-]+", query.lower()) if token]


def search(root: Path, query: str, limit: int = 10) -> list[Match]:
    terms = tokenize(query)
    if not terms:
        return []
    matches: list[Match] = []
    for path in iter_markdown_files(root):
        rel = path.relative_to(root)
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            lower = line.lower()
            score = sum(lower.count(term) for term in terms)
            if score:
                matches.append(Match(score, rel, line_no, line.strip()))
    matches.sort(key=lambda item: (-item.score, str(item.path), item.line))
    return matches[:limit]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search an LTM Wiki memory store.")
    parser.add_argument("root", type=Path)
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=10)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    matches = search(args.root, args.query, args.limit)
    if not matches:
        print("no matches")
        return 0
    for match in matches:
        print(f"{match.path}:{match.line}: score={match.score}: {match.excerpt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
