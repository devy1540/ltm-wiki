import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "setup.py"


class SetupTests(unittest.TestCase):
    def run_setup(self, root: Path, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(root), *extra],
            text=True,
            capture_output=True,
        )

    def test_setup_initializes_store_and_codex_instructions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "memory"
            result = self.run_setup(
                root,
                "--backend",
                "markdown-files",
                "--store-name",
                "Setup Memory",
                "--agent",
                "codex",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            config = json.loads((root / ".ltm-wiki" / "config.json").read_text(encoding="utf-8"))
            self.assertEqual(config["backend"], "markdown-files")
            self.assertEqual(config["storeName"], "Setup Memory")
            self.assertIn("doctor=ok", result.stdout)
            codex = root / "AGENTS.ltm-wiki.md"
            self.assertTrue(codex.exists())
            self.assertIn("LTM Wiki Agent Instructions", codex.read_text(encoding="utf-8"))

    def test_setup_installs_claude_command_and_instructions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "memory"
            result = self.run_setup(root, "--agent", "claude")

            self.assertEqual(result.returncode, 0, result.stderr)
            command = root / ".claude" / "commands" / "ltm-setup.md"
            self.assertTrue(command.exists())
            command_text = command.read_text(encoding="utf-8")
            self.assertIn("/ltm-setup", command_text)
            self.assertIn("scripts/setup.py", command_text)
            claude = root / "CLAUDE.ltm-wiki.md"
            self.assertTrue(claude.exists())
            self.assertIn("ltm-wiki 초기셋팅", claude.read_text(encoding="utf-8"))

    def test_setup_does_not_overwrite_agent_files_without_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "memory"
            first = self.run_setup(root, "--agent", "generic")
            self.assertEqual(first.returncode, 0, first.stderr)

            generic = root / "AI_MEMORY.md"
            generic.write_text("# Custom Memory Instructions\n", encoding="utf-8")
            second = self.run_setup(root, "--agent", "generic")
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(generic.read_text(encoding="utf-8"), "# Custom Memory Instructions\n")

            forced = self.run_setup(root, "--agent", "generic", "--force")
            self.assertEqual(forced.returncode, 0, forced.stderr)
            self.assertIn("Portable AI Memory Instructions", generic.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
