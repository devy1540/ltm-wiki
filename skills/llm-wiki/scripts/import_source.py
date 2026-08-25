#!/usr/bin/env python3
"""Create immutable, credential-safe snapshots of explicitly named source files."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import tempfile
from pathlib import Path

from llm_wiki_common import (WikiError, assert_no_symlink_components, canonical_dir,
                             canonical_regular_file, emit, ensure_safe_directories,
                             is_contained, sha256_file)

SENSITIVE = re.compile(
    rb"-----BEGIN(?: [A-Z0-9]+)? PRIVATE KEY-----"
    rb"|AKIA[0-9A-Z]{16}"
    rb"|\bsk-[A-Za-z0-9_-]{16,}\b"
    rb"|\bgh[pousr]_[A-Za-z0-9]{20,}\b"
    rb"|\bglpat-[A-Za-z0-9_-]{20,}\b"
    rb"|\bxox[baprs]-[A-Za-z0-9-]{10,}\b"
    rb"|\bAIza[0-9A-Za-z_-]{35}\b"
    rb"|(?i:[\"']?(?:api[_-]?key|password|secret)[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9_./+=-]{8,})"
)


def contains_sensitive_content(path: Path) -> bool:
    """Scan without loading an arbitrarily large source into memory."""
    overlap = b""
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            candidate = overlap + block
            if SENSITIVE.search(candidate):
                return True
            overlap = candidate[-256:]
    return False


def valid_root(value: str) -> Path:
    root = canonical_dir(value)
    marker = root / ".llm-wiki.json"
    try:
        marker_info = marker.lstat()
        if stat.S_ISLNK(marker_info.st_mode) or not stat.S_ISREG(marker_info.st_mode):
            raise ValueError
        data = json.loads(marker.read_text(encoding="utf-8"))
        if (not isinstance(data, dict) or set(data) != {"schemaVersion", "projectKey", "identityHashes"}
                or data.get("schemaVersion") != 1
                or not isinstance(data.get("projectKey"), str)
                or not re.fullmatch(r"[a-z0-9][a-z0-9-]*--[0-9a-f]{12}", data["projectKey"])
                or not isinstance(data.get("identityHashes"), list)
                or not data["identityHashes"]
                or any(not isinstance(item, str) or not re.fullmatch(r"[0-9a-f]{64}", item)
                       for item in data["identityHashes"])):
            raise ValueError
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        raise WikiError("INVALID_PROJECT_ROOT")
    sources = root / "sources"
    if not sources.is_dir() or sources.is_symlink():
        raise WikiError("INVALID_PROJECT_ROOT")
    return root


def safe_basename(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip(".-")
    return cleaned[:180] or "source"


def import_source(project_root: str, source: str) -> dict:
    root = valid_root(project_root)
    source_path = canonical_regular_file(source)
    sources = (root / "sources").resolve()
    digest = sha256_file(source_path)
    origin_hash = hashlib.sha256(str(source_path).encode("utf-8", "surrogateescape")).hexdigest()
    source_id = hashlib.sha256(("origin:" + origin_hash).encode()).hexdigest()[:24]
    if is_contained(source_path, sources):
        return {"status": "ALREADY_LOCAL", "sourceId": source_id,
                "sourcePath": source_path.relative_to(root).as_posix(), "sha256": digest,
                "originPathHash": origin_hash}
    # Read only after all boundary checks; the source is data, never instructions.
    if contains_sensitive_content(source_path):
        raise WikiError("SOURCE_REJECTED_SENSITIVE")
    relative = Path("sources") / "imported" / source_id / digest / safe_basename(source_path.name)
    destination = root / relative
    if destination.exists():
        if destination.is_symlink() or not destination.is_file() or sha256_file(destination) != digest:
            raise WikiError("TARGET_CONFLICT")
        return {"status": "NOOP", "sourceId": source_id, "sourcePath": relative.as_posix(), "sha256": digest, "originPathHash": origin_hash}
    lock = root / ".llm-wiki-import.lock"
    try:
        os.mkdir(lock)
    except FileExistsError:
        raise WikiError("LOCKED")
    except OSError:
        raise WikiError("LOCKED")
    try:
        if destination.exists():
            if destination.is_file() and not destination.is_symlink() and sha256_file(destination) == digest:
                return {"status": "NOOP", "sourceId": source_id, "sourcePath": relative.as_posix(), "sha256": digest, "originPathHash": origin_hash}
            raise WikiError("TARGET_CONFLICT")
        destination_parts = tuple(destination.relative_to(root).parts)
        assert_no_symlink_components(root, destination_parts)
        safe_parent = ensure_safe_directories(root, destination_parts[:-1])
        if safe_parent != destination.parent:
            raise WikiError("UNSAFE_TARGET")
        fd, temporary = tempfile.mkstemp(prefix=".snapshot-", dir=str(root))
        try:
            with source_path.open("rb") as input_handle, os.fdopen(fd, "wb") as output_handle:
                while True:
                    block = input_handle.read(1024 * 1024)
                    if not block:
                        break
                    output_handle.write(block)
                output_handle.flush(); os.fsync(output_handle.fileno())
            temp_path = Path(temporary)
            if sha256_file(temp_path) != digest:
                raise WikiError("DIGEST_MISMATCH")
            assert_no_symlink_components(root, destination_parts)
            if destination.parent.resolve(strict=True) != safe_parent:
                raise WikiError("UNSAFE_TARGET")
            os.replace(temp_path, destination)
        finally:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass
    finally:
        try:
            lock.rmdir()
        except OSError:
            pass
    return {"status": "IMPORTED", "sourceId": source_id, "sourcePath": relative.as_posix(), "sha256": digest, "originPathHash": origin_hash}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True); parser.add_argument("--source", required=True); parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        emit(import_source(args.project_root, args.source)); return 0
    except WikiError as exc:
        emit({"status": exc.status, **({"detail": exc.detail} if exc.detail else {})}); return 2


if __name__ == "__main__":
    raise SystemExit(main())
