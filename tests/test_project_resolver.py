from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "llm-wiki" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import project_resolver as resolver
from llm_wiki_common import WikiError


class ProjectResolverTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.config = self.root / "config.json"
        self.vault = self.root / "vault"; (self.vault / ".obsidian").mkdir(parents=True)
        self.cwd = self.root / "app"; self.cwd.mkdir()

    def tearDown(self): self.tmp.cleanup()

    def args(self, **extra):
        values = dict(cwd=str(self.cwd), config=str(self.config), obsidian_config=None, wiki_root=None, create=False)
        values.update(extra)
        return type("Args", (), values)()

    def configure(self):
        resolver.configure(type("Args", (), {"vault": str(self.vault), "config": str(self.config)})())

    def test_config_absence_corruption_and_configure(self):
        config, found = resolver.load_config(self.config)
        self.assertFalse(found); self.assertEqual(config["projects"], {})
        self.config.write_text("not json")
        with self.assertRaises(WikiError) as error: resolver.load_config(self.config)
        self.assertEqual(error.exception.status, "CONFIG_INVALID")
        self.config.unlink(); self.configure()
        stored = json.loads(self.config.read_text())
        self.assertEqual(stored["defaultVault"], str(self.vault.resolve()))
        if os.name != "nt": self.assertEqual(self.config.stat().st_mode & 0o777, 0o600)

    def test_discover_one_multiple_and_stale(self):
        ob = self.root / "obsidian.json"
        ob.write_text(json.dumps({"vaults": {"a": {"path": str(self.vault)}, "old": {"path": str(self.root / "gone")}}}))
        vaults, configured = resolver.discover_vaults(str(ob))
        self.assertTrue(configured); self.assertEqual(vaults, [str(self.vault.resolve())])
        second = self.root / "second"; (second / ".obsidian").mkdir(parents=True)
        ob.write_text(json.dumps({"vaults": {"a": {"path": str(self.vault)}, "b": {"path": str(second)}}}))
        self.assertEqual(len(resolver.discover_vaults(str(ob))[0]), 2)

    def test_multiple_discovered_vaults_require_selection(self):
        second = self.root / "second"; (second / ".obsidian").mkdir(parents=True)
        ob = self.root / "obsidian.json"
        ob.write_text(json.dumps({"vaults": {"a": {"path": str(self.vault)}, "b": {"path": str(second)}}}))
        with self.assertRaises(WikiError) as error:
            resolver.resolve(self.args(obsidian_config=str(ob)))
        self.assertEqual(error.exception.status, "VAULT_SELECTION_REQUIRED")

    def test_auto_create_and_idempotence(self):
        self.configure()
        first = resolver.resolve(self.args(create=True))
        self.assertEqual(first["status"], "READY"); self.assertTrue(first["created"])
        root = Path(first["projectRoot"]); before = (root / "wiki/operations.md").read_bytes()
        second = resolver.resolve(self.args(create=True))
        self.assertEqual(second["status"], "READY"); self.assertEqual(before, (root / "wiki/operations.md").read_bytes())
        self.assertTrue((root / ".llm-wiki.json").is_file())

    def test_auto_provision_disabled_creates_nothing(self):
        self.configure()
        config = json.loads(self.config.read_text()); config["autoProvision"] = False
        resolver.atomic_json_write(self.config, config)
        result = resolver.resolve(self.args(create=True))
        self.assertEqual(result["status"], "AUTO_PROVISION_DISABLED")
        self.assertFalse(Path(result["projectRoot"]).exists())

    def test_staging_failure_leaves_no_target_and_setup_is_single_contract_entry(self):
        self.configure()
        preview = resolver.resolve(self.args())
        target = Path(preview["projectRoot"])
        with mock.patch.object(resolver.shutil, "copyfile", side_effect=OSError("template copy failed")):
            with self.assertRaises(OSError): resolver.resolve(self.args(create=True))
        self.assertFalse(target.exists())
        self.assertEqual(list(target.parent.glob(f".{preview['projectKey']}.staging-*")), [])
        created = resolver.resolve(self.args(create=True))
        operations = (Path(created["projectRoot"]) / "wiki/operations.md").read_text()
        self.assertRegex(operations, rf"(?m)^## \d{{4}}-\d{{2}}-\d{{2}} \| setup \| {created['projectKey']}$")
        self.assertIn("- Created: sources/imported/", operations)
        self.assertIn(f"- Project key: {created['projectKey']}", operations)
        self.assertEqual(operations.count("| setup |"), 1)
        resolver.resolve(self.args(create=True))
        self.assertEqual((Path(created["projectRoot"]) / "wiki/operations.md").read_text(), operations)

    def test_legacy_root_wins(self):
        (self.cwd / "sources").mkdir(); (self.cwd / "wiki").mkdir(); (self.cwd / "wiki/schema.md").write_text("x")
        self.configure(); found = resolver.resolve(self.args())
        self.assertTrue(found["legacy"]); self.assertEqual(found["projectRoot"], str(self.cwd.resolve()))

    def git(self, directory, *arguments):
        subprocess.run(["git", "-C", str(directory), *arguments], check=True, capture_output=True, text=True)

    def make_git(self, name, remote):
        path = self.root / name; path.mkdir(); self.git(path, "init"); self.git(path, "remote", "add", "origin", remote); return path

    def test_remote_normalization_and_distinct_basenames(self):
        try:
            one = self.make_git("one", "git@GitHub.COM:Team/Same.git")
            two = self.make_git("two", "https://github.com/team/same.git")
            three = self.make_git("same", "https://github.com/other/same.git")
        except FileNotFoundError:
            self.skipTest("git unavailable")
        self.configure()
        first = resolver.resolve(self.args(cwd=str(one), create=True))
        second = resolver.resolve(self.args(cwd=str(two), create=True))
        third = resolver.resolve(self.args(cwd=str(three), create=True))
        self.assertEqual(first["projectKey"], second["projectKey"])
        self.assertNotEqual(first["projectKey"], third["projectKey"])

    def test_remote_path_case_is_preserved_for_case_sensitive_hosts(self):
        try:
            upper = self.make_git("upper", "ssh://git@example.com/Team/Repo.git")
            lower = self.make_git("lower", "https://example.com/team/repo.git")
        except FileNotFoundError:
            self.skipTest("git unavailable")
        self.configure()
        first = resolver.resolve(self.args(cwd=str(upper), create=True))
        second = resolver.resolve(self.args(cwd=str(lower), create=True))
        self.assertNotEqual(first["projectKey"], second["projectKey"])

    def test_nondefault_remote_ports_remain_distinct(self):
        try:
            default = self.make_git("default-port", "ssh://git@example.com/Team/Repo.git")
            alternate = self.make_git("alternate-port", "ssh://git@example.com:2222/Team/Repo.git")
        except FileNotFoundError:
            self.skipTest("git unavailable")
        self.configure()
        first = resolver.resolve(self.args(cwd=str(default), create=True))
        second = resolver.resolve(self.args(cwd=str(alternate), create=True))
        self.assertNotEqual(first["projectKey"], second["projectKey"])

    def test_ipv6_remote_authority_preserves_host_port_boundary(self):
        endpoint_with_port = resolver.normalize_remote(
            "ssh://git@[2001:db8::1]:2222/Team/Repo.git"
        )
        different_host = resolver.normalize_remote(
            "ssh://git@[2001:db8::1:2222]/Team/Repo.git"
        )
        self.assertEqual(endpoint_with_port, "[2001:db8::1]:2222/Team/Repo")
        self.assertEqual(different_host, "[2001:db8::1:2222]/Team/Repo")
        self.assertNotEqual(endpoint_with_port, different_host)
        self.assertEqual(
            resolver.normalize_remote("ssh://git@[2001:db8::1]:22/Team/Repo.git"),
            resolver.normalize_remote("git@[2001:db8::1]:Team/Repo.git"),
        )

    def test_git_worktree_shares_common_directory_identity(self):
        try:
            repository = self.root / "repository"; repository.mkdir(); self.git(repository, "init")
            self.git(repository, "config", "user.email", "test@example.invalid")
            self.git(repository, "config", "user.name", "Test")
            (repository / "tracked.txt").write_text("x")
            self.git(repository, "add", "."); self.git(repository, "commit", "-m", "initial")
            worktree = self.root / "worktree"; self.git(repository, "worktree", "add", str(worktree), "-b", "other")
        except (FileNotFoundError, subprocess.CalledProcessError):
            self.skipTest("git worktree unavailable")
        self.configure()
        one = resolver.resolve(self.args(cwd=str(repository), create=True))
        two = resolver.resolve(self.args(cwd=str(worktree), create=True))
        self.assertEqual(one["projectKey"], two["projectKey"])

    def test_non_git_isolation_and_unsafe_targets(self):
        other = self.root / "app2"; other.mkdir(); self.configure()
        first = resolver.resolve(self.args(create=True))
        second = resolver.resolve(self.args(cwd=str(other), create=True))
        self.assertNotEqual(first["projectKey"], second["projectKey"])
        # An unregistered nonempty target is never adopted.
        config = json.loads(self.config.read_text())
        new = self.root / "new"; new.mkdir()
        primary, _, base = resolver.project_identity(new)
        key = f"{resolver.sanitize_name(base)}--{__import__('hashlib').sha256(primary.encode()).hexdigest()[:12]}"
        target = self.vault / config["projectsDirectory"] / key
        target.mkdir(parents=True, exist_ok=True); (target / "unrelated").write_text("x")
        with self.assertRaises(WikiError) as error:
            resolver.resolve(self.args(cwd=str(new), create=True))
        self.assertEqual(error.exception.status, "TARGET_CONFLICT")

    def test_recreated_non_git_path_does_not_reuse_previous_wiki(self):
        self.configure()
        first = resolver.resolve(self.args(create=True))
        moved = self.root / "old-app"
        self.cwd.rename(moved)
        self.cwd.mkdir()
        second = resolver.resolve(self.args(create=True))
        self.assertNotEqual(first["projectKey"], second["projectKey"])
        self.assertNotEqual(first["projectRoot"], second["projectRoot"])

    def test_marker_mismatch_and_symlink_component(self):
        self.configure(); key = resolver.resolve(self.args())["projectKey"]
        target = self.vault / "LLM Wiki/projects" / key; target.mkdir(parents=True)
        (target / ".llm-wiki.json").write_text(json.dumps({"schemaVersion": 1, "projectKey": "wrong--000000000000", "identityHashes": ["0" * 64]}))
        with self.assertRaisesRegex(WikiError, "MARKER_MISMATCH"): resolver.resolve(self.args())
        # Config path component symlinks are rejected before target access.
        linked = self.vault / "linked"; linked.symlink_to(self.root / "outside")
        config = resolver.base_config(); config["defaultVault"] = str(self.vault); config["projectsDirectory"] = "linked/projects"
        resolver.atomic_json_write(self.config, config)
        with self.assertRaises(WikiError) as error: resolver.resolve(self.args())
        self.assertEqual(error.exception.status, "UNSAFE_TARGET")

    def test_symlink_parent_never_creates_outside_directories(self):
        outside = self.root / "outside"
        (self.vault / "linked").symlink_to(outside)
        self.configure()
        config = json.loads(self.config.read_text()); config["projectsDirectory"] = "linked/escape"
        resolver.atomic_json_write(self.config, config)
        with self.assertRaises(WikiError) as error: resolver.resolve(self.args(create=True))
        self.assertEqual(error.exception.status, "UNSAFE_TARGET")
        self.assertFalse(outside.exists())

    def test_legacy_and_explicit_roots_reject_symlinked_layout(self):
        outside = self.root / "outside"
        outside.mkdir()
        (self.cwd / "sources").symlink_to(outside, target_is_directory=True)
        (self.cwd / "wiki").mkdir()
        (self.cwd / "wiki/schema.md").write_text("schema")
        self.assertIsNone(resolver.legacy_root(self.cwd))
        with self.assertRaises(WikiError) as error:
            resolver.resolve(self.args(wiki_root=str(self.cwd)))
        self.assertEqual(error.exception.status, "INVALID_WIKI_ROOT")


if __name__ == "__main__": unittest.main()
