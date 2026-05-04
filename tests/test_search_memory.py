import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
INIT = REPO / "scripts" / "init_store.py"
SEARCH = REPO / "scripts" / "search_memory.py"


class SearchMemoryTests(unittest.TestCase):
    def test_search_finds_memory_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "store"
            subprocess.run([sys.executable, str(INIT), str(root)], check=True, text=True, capture_output=True)
            page = root / "memory" / "concepts" / "retrieval.md"
            page.write_text(
                "---\ntype: concept\nstatus: active\nconfidence: high\nprovenance: user-stated\n---\n# Retrieval\n\nHybrid retrieval combines lexical and semantic search.\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(SEARCH), str(root), "hybrid retrieval"],
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("memory/concepts/retrieval.md", result.stdout)

    def test_search_returns_no_results_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "store"
            subprocess.run([sys.executable, str(INIT), str(root)], check=True, text=True, capture_output=True)
            result = subprocess.run(
                [sys.executable, str(SEARCH), str(root), "nonexistent phrase"],
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("no matches", result.stdout)


if __name__ == "__main__":
    unittest.main()
