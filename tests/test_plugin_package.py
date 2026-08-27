from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PluginPackageTests(unittest.TestCase):
    def test_manifest_points_to_canonical_skill_package(self):
        manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        self.assertEqual(manifest["name"], "ltm-wiki")
        self.assertEqual(manifest["version"], "0.0.1")
        self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertNotIn("mcpServers", manifest)
        self.assertNotIn("apps", manifest)
        self.assertNotIn("hooks", manifest)
        self.assertLessEqual(len(manifest["interface"]["defaultPrompt"]), 3)
        for prompt in manifest["interface"]["defaultPrompt"]:
            self.assertLessEqual(len(prompt), 128)

    def test_repository_skill_link_resolves_to_canonical_package(self):
        canonical = ROOT / "skills/llm-wiki"
        compatibility = ROOT / ".agents/skills/llm-wiki"
        self.assertTrue(canonical.is_dir())
        self.assertTrue(compatibility.is_symlink())
        self.assertEqual(compatibility.resolve(strict=True), canonical.resolve(strict=True))

    def test_skill_metadata_enables_implicit_matching(self):
        skill = (ROOT / "skills/llm-wiki/SKILL.md").read_text()
        metadata = (ROOT / "skills/llm-wiki/agents/openai.yaml").read_text()
        self.assertRegex(skill, r"(?m)^name: llm-wiki$")
        self.assertIn("automatically resolve or provision", skill)
        self.assertRegex(metadata, r"(?m)^\s*allow_implicit_invocation: true$")
        self.assertIsNotNone(re.search(r"\$llm-wiki", metadata))


if __name__ == "__main__":
    unittest.main()
