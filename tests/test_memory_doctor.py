import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
INIT = REPO / "scripts" / "init_store.py"
DOCTOR = REPO / "scripts" / "memory_doctor.py"


class MemoryDoctorTests(unittest.TestCase):
    def test_doctor_passes_generated_store(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "store"
            subprocess.run([sys.executable, str(INIT), str(root)], check=True, text=True, capture_output=True)
            result = subprocess.run([sys.executable, str(DOCTOR), str(root)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("OK", result.stdout)

    def test_doctor_reports_missing_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "store"
            subprocess.run([sys.executable, str(INIT), str(root)], check=True, text=True, capture_output=True)
            (root / ".ltm-wiki" / "config.json").unlink()
            result = subprocess.run([sys.executable, str(DOCTOR), str(root)], text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing required file: .ltm-wiki/config.json", result.stdout)

    def test_doctor_reports_missing_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "store"
            subprocess.run([sys.executable, str(INIT), str(root)], check=True, text=True, capture_output=True)
            page = root / "memory" / "concepts" / "plain.md"
            page.write_text("# Plain\n\nNo frontmatter.\n", encoding="utf-8")
            result = subprocess.run([sys.executable, str(DOCTOR), str(root)], text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing frontmatter: memory/concepts/plain.md", result.stdout)


if __name__ == "__main__":
    unittest.main()
