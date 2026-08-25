"""Small standard-library primitives shared by the LLM Wiki command line tools."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import tempfile
from pathlib import Path, PurePosixPath


class WikiError(Exception):
    def __init__(self, status: str, detail: str = "") -> None:
        super().__init__(detail or status)
        self.status = status
        self.detail = detail


def canonical_dir(value: str | Path) -> Path:
    if "\x00" in str(value):
        raise WikiError("INVALID_PATH", "NUL byte in path")
    path = Path(value).expanduser()
    try:
        resolved = path.resolve(strict=True)
    except (OSError, RuntimeError):
        raise WikiError("INVALID_PATH", "path is not accessible")
    if not resolved.is_dir():
        raise WikiError("INVALID_PATH", "not a directory")
    return resolved


def canonical_regular_file(value: str | Path) -> Path:
    if "\x00" in str(value):
        raise WikiError("INVALID_SOURCE", "NUL byte in path")
    path = Path(value).expanduser()
    try:
        info = path.lstat()
        resolved = path.resolve(strict=True)
    except (OSError, RuntimeError):
        raise WikiError("INVALID_SOURCE", "source is not accessible")
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
        raise WikiError("INVALID_SOURCE", "source must be a regular non-symlink file")
    return resolved


def is_contained(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def safe_relative_directory(value: str) -> tuple[str, ...]:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise WikiError("INVALID_CONFIG", "invalid projectsDirectory")
    pure = PurePosixPath(value.replace("\\", "/"))
    if pure.is_absolute() or any(part in ("", ".", "..") for part in pure.parts):
        raise WikiError("INVALID_CONFIG", "unsafe projectsDirectory")
    return pure.parts


def assert_no_symlink_components(base: Path, components: tuple[str, ...]) -> Path:
    current = base
    for component in components:
        current = current / component
        try:
            # lstat detects a broken symlink too; Path.exists() deliberately does not.
            if current.is_symlink():
                raise WikiError("UNSAFE_TARGET", "symlink in target path")
        except OSError:
            # A nonexistent future component is fine. Any other lstat failure is not.
            if current.parent.exists():
                continue
            raise WikiError("UNSAFE_TARGET", "unreadable target path")
    return current


def ensure_safe_directories(base: Path, components: tuple[str, ...]) -> Path:
    """Create directory components one at a time without following a symlink."""
    current = base
    for component in components:
        if component in ("", ".", ".."):
            raise WikiError("UNSAFE_TARGET", "unsafe target component")
        current = current / component
        try:
            info = current.lstat()
        except FileNotFoundError:
            try:
                current.mkdir()
            except FileExistsError:
                # A concurrent creator raced us; validate its result below.
                pass
            except OSError as exc:
                raise WikiError("UNSAFE_TARGET", "cannot create target path") from exc
        except OSError as exc:
            raise WikiError("UNSAFE_TARGET", "cannot inspect target path") from exc
        else:
            if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
                raise WikiError("UNSAFE_TARGET", "target path is not a real directory")
        try:
            resolved = current.resolve(strict=True)
        except (OSError, RuntimeError) as exc:
            raise WikiError("UNSAFE_TARGET", "cannot canonicalize target path") from exc
        if resolved != current or not is_contained(resolved, base):
            raise WikiError("UNSAFE_TARGET", "target escapes vault")
    return current


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json_write(path: Path, value: object, mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=".tmp-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, sort_keys=True, separators=(",", ":"))
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temp_name, mode)
        os.replace(temp_name, path)
        try:
            os.chmod(path, mode)
        except OSError:
            pass
    finally:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass


def emit(payload: dict) -> None:
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
