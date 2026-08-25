from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "llm-wiki" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import import_source
from llm_wiki_common import WikiError


class ImportSourceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.base = Path(self.tmp.name)
        self.project = self.base / "project"; (self.project / "sources").mkdir(parents=True)
        (self.project / ".llm-wiki.json").write_text(json.dumps({"schemaVersion": 1, "projectKey": "project--0123456789ab", "identityHashes": ["a" * 64]}))
        self.external = self.base / "document.txt"; self.external.write_bytes(b"first version\n")

    def tearDown(self): self.tmp.cleanup()

    def test_import_noop_and_changed_digest_stable_origin(self):
        first = import_source.import_source(str(self.project), str(self.external))
        self.assertEqual(first["status"], "IMPORTED")
        copied = self.project / first["sourcePath"]; self.assertEqual(copied.read_bytes(), b"first version\n")
        again = import_source.import_source(str(self.project), str(self.external))
        self.assertEqual(again["status"], "NOOP"); self.assertEqual(again["sourceId"], first["sourceId"])
        self.external.write_bytes(b"second version\n")
        changed = import_source.import_source(str(self.project), str(self.external))
        self.assertEqual(changed["status"], "IMPORTED"); self.assertEqual(changed["sourceId"], first["sourceId"]); self.assertNotEqual(changed["sha256"], first["sha256"])

    def test_local_source_never_copied(self):
        local = self.project / "sources" / "original.md"; local.write_text("local")
        result = import_source.import_source(str(self.project), str(local))
        self.assertEqual(result["status"], "ALREADY_LOCAL"); self.assertEqual(result["sourcePath"], "sources/original.md")

    def test_rejects_symlink_directory_and_secret(self):
        link = self.base / "link"; link.symlink_to(self.external)
        with self.assertRaises(WikiError) as error: import_source.import_source(str(self.project), str(link))
        self.assertEqual(error.exception.status, "INVALID_SOURCE")
        with self.assertRaises(WikiError) as error: import_source.import_source(str(self.project), str(self.base))
        self.assertEqual(error.exception.status, "INVALID_SOURCE")
        secret = self.base / "key.pem"; secret.write_text("-----BEGIN PRIVATE KEY-----\nabc")
        with self.assertRaisesRegex(WikiError, "SOURCE_REJECTED_SENSITIVE"): import_source.import_source(str(self.project), str(secret))

    def test_rejects_common_credential_token_patterns(self):
        samples = {
            "openai": b"sk-proj-abcdefghijklmnopqrstuvwxyz123456",
            "aws": b"AKIAABCDEFGHIJKLMNOP",
            "github": b"ghp_abcdefghijklmnopqrstuvwxyz123456",
            "gitlab": b"glpat-abcdefghijklmnopqrstuvwxyz123456",
            "slack": b"xoxb-1234567890-abcdefghij",
            "assignment": b"password=correct-horse-battery-staple",
            "json-assignment": b'{"api_key":"not-a-provider-prefixed-secret-1234567890"}',
        }
        for name, token in samples.items():
            with self.subTest(name=name):
                source = self.base / f"{name}.txt"; source.write_bytes(token)
                with self.assertRaises(WikiError) as error:
                    import_source.import_source(str(self.project), str(source))
                self.assertEqual(error.exception.status, "SOURCE_REJECTED_SENSITIVE")

    def test_detects_credential_split_across_scan_blocks(self):
        source = self.base / "split-token.txt"
        prefix = b"x" * (1024 * 1024 - 4) + b" sk-"
        source.write_bytes(prefix + b"proj-abcdefghijklmnopqrstuvwxyz123456")
        with self.assertRaises(WikiError) as error:
            import_source.import_source(str(self.project), str(source))
        self.assertEqual(error.exception.status, "SOURCE_REJECTED_SENSITIVE")

    def test_rejects_symlinked_marker_and_import_parent(self):
        marker = self.project / ".llm-wiki.json"
        real_marker = self.base / "marker.json"
        real_marker.write_bytes(marker.read_bytes())
        marker.unlink()
        marker.symlink_to(real_marker)
        with self.assertRaises(WikiError) as error:
            import_source.import_source(str(self.project), str(self.external))
        self.assertEqual(error.exception.status, "INVALID_PROJECT_ROOT")

        marker.unlink()
        marker.write_bytes(real_marker.read_bytes())
        outside = self.base / "outside"
        outside.mkdir()
        imported = self.project / "sources/imported"
        imported.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(WikiError) as error:
            import_source.import_source(str(self.project), str(self.external))
        self.assertEqual(error.exception.status, "UNSAFE_TARGET")
        self.assertEqual(list(outside.iterdir()), [])

    def test_never_writes_absolute_origin(self):
        import_source.import_source(str(self.project), str(self.external))
        origin = str(self.external.resolve()).encode()
        for item in self.project.rglob("*"):
            if item.is_file() and item != self.project / "sources/imported":
                self.assertNotIn(origin, item.read_bytes(), str(item))


if __name__ == "__main__": unittest.main()
