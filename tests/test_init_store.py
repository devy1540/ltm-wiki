import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "init_store.py"


class InitStoreTests(unittest.TestCase):
    def test_initializes_markdown_store(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "memory-store"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(root), "--backend", "markdown-files", "--store-name", "Test Memory"],
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            config = json.loads((root / ".ltm-wiki" / "config.json").read_text(encoding="utf-8"))
            self.assertEqual(config["backend"], "markdown-files")
            self.assertEqual(config["storeName"], "Test Memory")
            self.assertTrue((root / "memory" / "index.md").exists())
            self.assertTrue((root / "memory" / "log.md").exists())
            self.assertTrue((root / "meta" / "schemas" / "ltm-wiki.md").exists())

    def test_initializes_obsidian_store_with_wikilinks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "obsidian-store"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(root), "--backend", "obsidian", "--store-name", "Obsidian Memory"],
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            overview = (root / "memory" / "overview.md").read_text(encoding="utf-8")
            self.assertIn("[[index]]", overview)

    def test_does_not_overwrite_existing_files_without_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "memory-store"
            first = subprocess.run(
                [sys.executable, str(SCRIPT), str(root), "--backend", "markdown-files"],
                text=True,
                capture_output=True,
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            index = root / "memory" / "index.md"
            index.write_text("custom index\n", encoding="utf-8")
            second = subprocess.run(
                [sys.executable, str(SCRIPT), str(root), "--backend", "markdown-files"],
                text=True,
                capture_output=True,
            )
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(index.read_text(encoding="utf-8"), "custom index\n")


if __name__ == "__main__":
    unittest.main()
