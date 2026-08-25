from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESOLVER = ROOT / "skills/llm-wiki/scripts/project_resolver.py"
IMPORTER = ROOT / "skills/llm-wiki/scripts/import_source.py"


class CliFlowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.vault = self.base / "vault"
        (self.vault / ".obsidian").mkdir(parents=True)
        self.project_one = self.base / "project-one"
        self.project_two = self.base / "project-two"
        self.project_one.mkdir()
        self.project_two.mkdir()
        self.config = self.base / "machine-config.json"
        self.obsidian = self.base / "obsidian.json"
        self.obsidian.write_text(
            json.dumps({"vaults": {"only": {"path": str(self.vault)}}}),
            encoding="utf-8",
        )

    def tearDown(self):
        self.tmp.cleanup()

    def run_json(self, script: Path, *arguments: str, expected_code: int = 0):
        result = subprocess.run(
            [sys.executable, str(script), *arguments, "--json"],
            capture_output=True,
            check=False,
            text=True,
        )
        self.assertEqual(result.returncode, expected_code, result.stderr)
        self.assertEqual(result.stderr, "")
        return json.loads(result.stdout)

    def resolve(self, project: Path):
        return self.run_json(
            RESOLVER,
            "resolve",
            "--cwd",
            str(project),
            "--config",
            str(self.config),
            "--obsidian-config",
            str(self.obsidian),
            "--create",
        )

    def test_install_once_style_flow_is_isolated_and_idempotent(self):
        first = self.resolve(self.project_one)
        self.assertEqual(first["status"], "READY")
        self.assertTrue(first["created"])
        first_root = Path(first["projectRoot"])

        repeated = self.resolve(self.project_one)
        self.assertEqual(repeated["projectRoot"], str(first_root))
        self.assertNotIn("created", repeated)
        self.assertEqual(
            (first_root / "wiki/operations.md").read_text().count("| setup |"),
            1,
        )

        second = self.resolve(self.project_two)
        self.assertNotEqual(second["projectRoot"], str(first_root))

        external = self.base / "decision.md"
        external.write_text("# Decision\n\nUse the public transport.\n")
        imported = self.run_json(
            IMPORTER,
            "--project-root",
            str(first_root),
            "--source",
            str(external),
        )
        self.assertEqual(imported["status"], "IMPORTED")
        snapshot = first_root / imported["sourcePath"]
        self.assertEqual(snapshot.read_bytes(), external.read_bytes())
        self.assertEqual(
            self.run_json(
                IMPORTER,
                "--project-root",
                str(first_root),
                "--source",
                str(external),
            )["status"],
            "NOOP",
        )
        external_path = str(external.resolve()).encode()
        for path in self.vault.rglob("*"):
            if path.is_file():
                self.assertNotIn(external_path, path.read_bytes(), str(path))

    def test_multiple_vaults_fail_closed_without_creating_a_wiki(self):
        second_vault = self.base / "second-vault"
        (second_vault / ".obsidian").mkdir(parents=True)
        self.obsidian.write_text(
            json.dumps(
                {
                    "vaults": {
                        "one": {"path": str(self.vault)},
                        "two": {"path": str(second_vault)},
                    }
                }
            ),
            encoding="utf-8",
        )
        result = self.run_json(
            RESOLVER,
            "resolve",
            "--cwd",
            str(self.project_one),
            "--config",
            str(self.config),
            "--obsidian-config",
            str(self.obsidian),
            "--create",
            expected_code=2,
        )
        self.assertEqual(result["status"], "VAULT_SELECTION_REQUIRED")
        self.assertFalse((self.vault / "LLM Wiki").exists())
        self.assertFalse((second_vault / "LLM Wiki").exists())


if __name__ == "__main__":
    unittest.main()
