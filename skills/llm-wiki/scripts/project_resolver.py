#!/usr/bin/env python3
"""Discover an Obsidian vault and resolve a safely provisioned LLM Wiki root."""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from llm_wiki_common import (WikiError, assert_no_symlink_components, atomic_json_write,
                             canonical_dir, emit, ensure_safe_directories,
                             safe_relative_directory)

SCHEMA_VERSION = 1
DEFAULT_PROJECTS_DIRECTORY = "LLM Wiki/projects"
SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = SCRIPT_DIR.parent / "assets" / "wiki-template"


def default_config_path() -> Path:
    if os.name == "nt":
        root = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    else:
        root = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return root / "llm-wiki" / "config.json"


def base_config() -> dict[str, Any]:
    return {"schemaVersion": SCHEMA_VERSION, "defaultVault": None,
            "projectsDirectory": DEFAULT_PROJECTS_DIRECTORY, "autoProvision": True,
            "projects": {}}


def _hashes(value: Any) -> list[str]:
    if (not isinstance(value, list) or not value
            or any(not isinstance(x, str) or not re.fullmatch(r"[0-9a-f]{64}", x)
                   for x in value)):
        raise WikiError("CONFIG_INVALID", "invalid identity hash aliases")
    return sorted(set(value))


def validate_config(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) - {"schemaVersion", "defaultVault", "projectsDirectory", "autoProvision", "projects"}:
        raise WikiError("CONFIG_INVALID", "invalid config shape")
    required = {"schemaVersion", "defaultVault", "projectsDirectory", "autoProvision", "projects"}
    if set(value) != required or value["schemaVersion"] != SCHEMA_VERSION or not isinstance(value["autoProvision"], bool):
        raise WikiError("CONFIG_INVALID", "invalid config fields")
    default = value["defaultVault"]
    if default is not None and not isinstance(default, str):
        raise WikiError("CONFIG_INVALID", "invalid defaultVault")
    safe_relative_directory(value["projectsDirectory"])
    if not isinstance(value["projects"], dict):
        raise WikiError("CONFIG_INVALID", "invalid projects")
    projects: dict[str, Any] = {}
    for key, entry in value["projects"].items():
        if not isinstance(key, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*--[0-9a-f]{12}", key):
            raise WikiError("CONFIG_INVALID", "invalid project key")
        if not isinstance(entry, dict) or set(entry) != {"identityHashes"}:
            raise WikiError("CONFIG_INVALID", "invalid project entry")
        projects[key] = {"identityHashes": _hashes(entry["identityHashes"])}
    return {"schemaVersion": SCHEMA_VERSION, "defaultVault": default,
            "projectsDirectory": value["projectsDirectory"], "autoProvision": value["autoProvision"],
            "projects": projects}


def load_config(path: Path) -> tuple[dict[str, Any], bool]:
    if not path.exists():
        return base_config(), False
    try:
        with path.open(encoding="utf-8") as handle:
            return validate_config(json.load(handle)), True
    except (OSError, json.JSONDecodeError, TypeError, WikiError) as exc:
        if isinstance(exc, WikiError):
            raise
        raise WikiError("CONFIG_INVALID", "cannot read config")


def obsidian_config_candidates(explicit: str | None) -> list[Path]:
    if explicit:
        return [Path(explicit).expanduser()]
    home = Path.home()
    if sys.platform == "darwin":
        return [home / "Library/Application Support/obsidian/obsidian.json"]
    if os.name == "nt":
        return [Path(os.environ.get("APPDATA", home / "AppData/Roaming")) / "obsidian/obsidian.json"]
    xdg = Path(os.environ.get("XDG_CONFIG_HOME", home / ".config"))
    return [xdg / "obsidian/obsidian.json", home / ".config/obsidian/obsidian.json",
            home / ".var/app/md.obsidian.Obsidian/config/obsidian/obsidian.json"]


def discover_vaults(explicit: str | None = None) -> tuple[list[str], bool]:
    found: set[str] = set()
    configured = False
    for candidate in obsidian_config_candidates(explicit):
        try:
            with candidate.open(encoding="utf-8") as handle:
                data = json.load(handle)
            configured = True
        except (OSError, json.JSONDecodeError, TypeError):
            continue
        vaults = data.get("vaults") if isinstance(data, dict) else None
        if not isinstance(vaults, dict):
            continue
        for entry in vaults.values():
            raw = entry.get("path") if isinstance(entry, dict) else None
            if not isinstance(raw, str) or "\x00" in raw:
                continue
            try:
                vault = Path(raw).expanduser().resolve(strict=True)
                if vault.is_dir() and (vault / ".obsidian").is_dir():
                    found.add(str(vault))
            except (OSError, RuntimeError):
                continue
    return sorted(found), configured


def normalize_remote(raw: str) -> str | None:
    raw = raw.strip()
    if not raw:
        return None
    # user@host:path (SCP form), excluding normal URLs
    match = re.fullmatch(r"(?:[^@/:]+@)?(\[[^\]]+\]|[^/:]+):/?(.+)", raw)
    if match and "://" not in raw:
        host, path = match.group(1), match.group(2)
    else:
        from urllib.parse import urlsplit
        try:
            parts = urlsplit(raw)
            port = parts.port
        except ValueError:
            return None
        if parts.scheme not in {"ssh", "git", "http", "https"} or not parts.hostname:
            return None
        hostname, path = parts.hostname.lower(), parts.path
        host = f"[{hostname}]" if ":" in hostname else hostname
        default_ports = {"ssh": 22, "git": 9418, "http": 80, "https": 443}
        if port is not None and port != default_ports[parts.scheme]:
            host = f"{host}:{port}"
    path = path.strip("/")
    if path.endswith(".git"):
        path = path[:-4]
    if not host or not path or any(x in path for x in ("?", "#")):
        return None
    if host.lower() == "github.com":
        path = path.lower()
    return f"{host.lower()}/{path}"


def git_output(cwd: Path, *args: str) -> str | None:
    try:
        run = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True,
                             timeout=3, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    return run.stdout.strip() if run.returncode == 0 and run.stdout.strip() else None


def project_identity(cwd: Path) -> tuple[str, list[str], Path]:
    canonical = cwd.resolve()
    top = git_output(canonical, "rev-parse", "--show-toplevel")
    root = Path(top).resolve() if top else canonical
    remotes: list[str] = []
    branch = git_output(root, "symbolic-ref", "--quiet", "--short", "HEAD")
    if branch:
        remote = git_output(root, "config", f"branch.{branch}.remote")
        if remote:
            url = git_output(root, "remote", "get-url", remote)
            if url:
                remotes.append(url)
    push_default = git_output(root, "config", "remote.pushDefault")
    if push_default:
        url = git_output(root, "remote", "get-url", push_default)
        if url:
            remotes.append(url)
    for name in ("origin",):
        url = git_output(root, "remote", "get-url", name)
        if url:
            remotes.append(url)
    names = git_output(root, "remote")
    if names and len(names.splitlines()) == 1:
        url = git_output(root, "remote", "get-url", names)
        if url:
            remotes.append(url)
    normalized = next((normalize_remote(item) for item in remotes if normalize_remote(item)), None)
    common = git_output(root, "rev-parse", "--git-common-dir")
    common_identity = ""
    if common:
        common_path = (root / common).resolve() if not Path(common).is_absolute() else Path(common).resolve()
        try:
            common_stat = common_path.stat()
            common_identity = f"git-common-inode:{common_stat.st_dev}:{common_stat.st_ino}"
        except OSError as exc:
            raise WikiError("PROJECT_IDENTITY_UNAVAILABLE", "cannot inspect Git common directory") from exc
    try:
        stat_value = root.stat()
        inode_identity = f"inode:{stat_value.st_dev}:{stat_value.st_ino}"
    except OSError as exc:
        raise WikiError("PROJECT_IDENTITY_UNAVAILABLE", "cannot inspect project directory") from exc
    primary = normalized or common_identity or inode_identity
    aliases = [hashlib.sha256(primary.encode()).hexdigest()]
    if common_identity:
        aliases.append(hashlib.sha256(common_identity.encode()).hexdigest())
    elif not normalized:
        aliases.append(hashlib.sha256(inode_identity.encode()).hexdigest())
    return primary, sorted(set(aliases)), root


def sanitize_name(path: Path) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", path.name.lower()).strip("-")
    return value or "project"


def marker(root: Path) -> dict[str, Any] | None:
    path = root / ".llm-wiki.json"
    try:
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        if (isinstance(data, dict) and set(data) == {"schemaVersion", "projectKey", "identityHashes"}
                and data["schemaVersion"] == SCHEMA_VERSION
                and isinstance(data["projectKey"], str)
                and re.fullmatch(r"[a-z0-9][a-z0-9-]*--[0-9a-f]{12}", data["projectKey"])):
            _hashes(data["identityHashes"])
            return data
    except (OSError, json.JSONDecodeError, TypeError, WikiError):
        return None
    return None


def valid_wiki_layout(root: Path) -> bool:
    sources = root / "sources"
    wiki = root / "wiki"
    schema = wiki / "schema.md"
    return (sources.is_dir() and not sources.is_symlink()
            and wiki.is_dir() and not wiki.is_symlink()
            and schema.is_file() and not schema.is_symlink())


def legacy_root(cwd: Path) -> Path | None:
    current = cwd.resolve()
    for candidate in (current, *current.parents):
        if valid_wiki_layout(candidate):
            return candidate
    return None


def result(status: str, **kwargs: Any) -> dict[str, Any]:
    return {"status": status, **kwargs}


def provision(target: Path, vault: Path, config_path: Path, config: dict[str, Any], key: str, aliases: list[str]) -> None:
    relative_parts = tuple(target.relative_to(vault).parts)
    parent = ensure_safe_directories(vault, relative_parts[:-1])
    if target.parent != parent:
        raise WikiError("UNSAFE_TARGET", "target parent changed")
    lock = parent / f".{key}.llm-wiki.lock"
    try:
        os.mkdir(lock)
    except FileExistsError:
        raise WikiError("LOCKED", "provision lock exists")
    except OSError:
        raise WikiError("UNSAFE_TARGET", "cannot create provision lock")
    staging: Path | None = None
    try:
        if target.exists():
            if target.is_symlink() or not target.is_dir() or any(target.iterdir()):
                raise WikiError("TARGET_CONFLICT", "unregistered target is not empty")
        elif target.is_symlink():
            raise WikiError("TARGET_CONFLICT", "target is a symlink")
        staging = Path(tempfile.mkdtemp(prefix=f".{key}.staging-", dir=str(parent)))
        for relative in ("sources/imported", "wiki/source-notes", "wiki/topics", "wiki/syntheses"):
            (staging / relative).mkdir(parents=True, exist_ok=True)
        for source in TEMPLATE_DIR.rglob("*"):
            if source.is_file():
                destination = staging / "wiki" / source.relative_to(TEMPLATE_DIR)
                destination.parent.mkdir(parents=True, exist_ok=True)
                if not destination.exists():
                    shutil.copyfile(source, destination)
        operations = staging / "wiki/operations.md"
        with operations.open("a", encoding="utf-8") as handle:
            handle.write(
                f"\n## {datetime.date.today().isoformat()} | setup | {key}\n\n"
                "- Created: .llm-wiki.json\n"
                "- Created: sources/\n"
                "- Created: sources/imported/\n"
                "- Created: wiki/\n"
                "- Created: wiki/source-notes/\n"
                "- Created: wiki/topics/\n"
                "- Created: wiki/syntheses/\n"
                f"- Project key: {key}\n"
                "- Result: initialized LLM Wiki project\n"
            )
            handle.flush(); os.fsync(handle.fileno())
        atomic_json_write(staging / ".llm-wiki.json", {"schemaVersion": SCHEMA_VERSION,
                          "projectKey": key, "identityHashes": aliases})
        # An empty pre-existing target is safe to replace. Remove it explicitly so
        # os.replace has the same cross-platform meaning as the absent-target case.
        if target.exists():
            if target.is_symlink() or not target.is_dir() or any(target.iterdir()):
                raise WikiError("TARGET_CONFLICT", "target changed during provisioning")
            target.rmdir()
        elif target.is_symlink():
            raise WikiError("TARGET_CONFLICT", "target changed during provisioning")
        os.replace(staging, target)
        staging = None
        updated = dict(config)
        projects = dict(config["projects"])
        projects[key] = {"identityHashes": aliases}
        updated["projects"] = projects
        atomic_json_write(config_path, updated)
    finally:
        if staging is not None:
            try:
                shutil.rmtree(staging)
            except OSError:
                pass
        try:
            lock.rmdir()
        except OSError:
            pass


def resolve(args: argparse.Namespace) -> dict[str, Any]:
    config_path = Path(args.config).expanduser() if args.config else default_config_path()
    config, _ = load_config(config_path)
    cwd = canonical_dir(args.cwd or os.getcwd())
    if args.wiki_root:
        root = canonical_dir(args.wiki_root)
        root_marker = marker(root)
        if valid_wiki_layout(root):
            return result("READY", projectRoot=str(root),
                          projectKey=root_marker["projectKey"] if root_marker else None,
                          legacy=not bool(root_marker))
        raise WikiError("INVALID_WIKI_ROOT", "missing valid marker or wiki layout")
    primary, aliases, project_base = project_identity(cwd)
    matching = [key for key, item in config["projects"].items()
                if set(aliases).intersection(item["identityHashes"])]
    if len(matching) > 1:
        raise WikiError("AMBIGUOUS_PROJECT_MAPPING", "multiple project aliases match")
    legacy = legacy_root(cwd)
    if matching:
        key = matching[0]
    else:
        key = f"{sanitize_name(project_base)}--{hashlib.sha256(primary.encode()).hexdigest()[:12]}"
        if key in config["projects"]:
            raise WikiError("HASH_COLLISION", "project key is already allocated")
    if legacy and not matching:
        return result("READY", projectRoot=str(legacy), projectKey=key, legacy=True)
    vault_raw = config["defaultVault"]
    if vault_raw:
        try:
            vault = canonical_dir(vault_raw)
            if not (vault / ".obsidian").is_dir():
                raise WikiError("NO_ACCESSIBLE_VAULT", "configured vault is invalid")
        except WikiError:
            raise WikiError("NO_ACCESSIBLE_VAULT", "configured vault is invalid")
    else:
        vaults, configured = discover_vaults(args.obsidian_config)
        if not vaults:
            raise WikiError("NO_ACCESSIBLE_VAULT" if configured else "OBSIDIAN_NOT_CONFIGURED")
        if len(vaults) > 1:
            raise WikiError("VAULT_SELECTION_REQUIRED")
        vault = Path(vaults[0])
        config = dict(config); config["defaultVault"] = str(vault)
        atomic_json_write(config_path, config)
    target = assert_no_symlink_components(vault, safe_relative_directory(config["projectsDirectory"]) + (key,))
    existing_marker = marker(target) if target.exists() else None
    if existing_marker:
        if existing_marker["projectKey"] != key or not set(aliases).intersection(existing_marker["identityHashes"]):
            raise WikiError("MARKER_MISMATCH")
        return result("READY", projectRoot=str(target), projectKey=key)
    target_is_empty = target.exists() and target.is_dir() and not target.is_symlink() and not any(target.iterdir())
    if target.is_symlink() or (target.exists() and not target_is_empty):
        raise WikiError("TARGET_CONFLICT", "unregistered target exists")
    if args.create and not config["autoProvision"]:
        return result("AUTO_PROVISION_DISABLED", projectRoot=str(target), projectKey=key)
    if not args.create:
        return result("NOT_PROVISIONED", projectRoot=str(target), projectKey=key)
    provision(target, vault, config_path, config, key, aliases)
    return result("READY", projectRoot=str(target), projectKey=key, created=True)


def configure(args: argparse.Namespace) -> dict[str, Any]:
    vault = canonical_dir(args.vault)
    if not (vault / ".obsidian").is_dir():
        raise WikiError("INVALID_VAULT", "vault lacks .obsidian")
    path = Path(args.config).expanduser() if args.config else default_config_path()
    config, _ = load_config(path)
    config["defaultVault"] = str(vault)
    atomic_json_write(path, config)
    return result("CONFIGURED", defaultVault=str(vault), configPath=str(path))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    discover = commands.add_parser("discover-vaults"); discover.add_argument("--obsidian-config"); discover.add_argument("--json", action="store_true")
    configure_parser = commands.add_parser("configure"); configure_parser.add_argument("--vault", required=True); configure_parser.add_argument("--config"); configure_parser.add_argument("--json", action="store_true")
    resolve_parser = commands.add_parser("resolve")
    for flag in ("cwd", "config", "obsidian_config", "wiki_root"):
        resolve_parser.add_argument("--" + flag.replace("_", "-"))
    resolve_parser.add_argument("--create", action="store_true"); resolve_parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "discover-vaults":
            vaults, configured = discover_vaults(args.obsidian_config)
            emit(result("READY" if vaults else ("NO_ACCESSIBLE_VAULT" if configured else "OBSIDIAN_NOT_CONFIGURED"), vaults=vaults))
        elif args.command == "configure":
            emit(configure(args))
        else:
            emit(resolve(args))
        return 0
    except WikiError as exc:
        emit(result(exc.status, detail=exc.detail) if exc.detail else result(exc.status))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
