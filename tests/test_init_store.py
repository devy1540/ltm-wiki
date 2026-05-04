import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.ltm_common import has_frontmatter, iter_markdown_files, slugify

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "init_store.py"
GENERATED_FILES = [
    ".ltm-wiki/config.json",
    "memory/index.md",
    "memory/log.md",
    "memory/overview.md",
    "meta/schemas/ltm-wiki.md",
]


class LtmCommonTests(unittest.TestCase):
    def test_slugify_preserves_unicode_words(self):
        self.assertEqual(slugify("장기 기억"), "장기-기억")
        self.assertEqual(slugify("東京 Memory"), "東京-memory")
        self.assertEqual(slugify("  !!!  "), "memory")

    def test_iter_markdown_files_excludes_meta_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            memory = root / "memory" / "index.md"
            meta = root / "meta" / "schemas" / "ltm-wiki.md"
            raw = root / "raw" / "sources" / "source.md"
            for path in [memory, meta, raw]:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("# test\n", encoding="utf-8")

            self.assertEqual(list(iter_markdown_files(root)), [memory])
            self.assertEqual(list(iter_markdown_files(root, include_raw=True)), [memory, raw])

    def test_has_frontmatter_requires_delimiter_lines_and_allows_crlf(self):
        self.assertTrue(has_frontmatter("---\r\nkind: test\r\n---\r\nbody\n"))
        self.assertTrue(has_frontmatter("---\nkind: test\n---\nbody\n"))
        self.assertFalse(has_frontmatter("---\nkind: test\n--- not a delimiter\nbody\n"))
        self.assertFalse(has_frontmatter("----\nkind: test\n---\nbody\n"))


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
            custom_content = "custom generated file\n"
            for relative_path in GENERATED_FILES:
                (root / relative_path).write_text(custom_content, encoding="utf-8")
            second = subprocess.run(
                [sys.executable, str(SCRIPT), str(root), "--backend", "markdown-files"],
                text=True,
                capture_output=True,
            )
            self.assertEqual(second.returncode, 0, second.stderr)
            for relative_path in GENERATED_FILES:
                self.assertEqual((root / relative_path).read_text(encoding="utf-8"), custom_content)
            forced = subprocess.run(
                [sys.executable, str(SCRIPT), str(root), "--backend", "markdown-files", "--force"],
                text=True,
                capture_output=True,
            )
            self.assertEqual(forced.returncode, 0, forced.stderr)
            self.assertNotEqual(index.read_text(encoding="utf-8"), custom_content)


if __name__ == "__main__":
    unittest.main()
