"""Regression tests for collection validation (no third-party dependencies)."""
from pathlib import Path
import tempfile
import unittest

from validate_skills import validate


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / "skills/example/SKILL.md"
        self.skill.parent.mkdir(parents=True)
        self.skill.write_text("---\nname: example\ndescription: Use when testing.\n---\n\n# Example\n")
        (self.root / "README.md").write_text("[Example](skills/example/SKILL.md)\n")

    def test_valid_collection(self):
        self.assertEqual(validate(self.root), ([], 1))

    def test_name_mismatch(self):
        self.skill.write_text(self.skill.read_text().replace("name: example", "name: wrong"))
        self.assertTrue(any("directory mismatch" in e for e in validate(self.root)[0]))

    def test_broken_link(self):
        with self.skill.open("a") as f:
            f.write("\n[Missing](references/missing.md)\n")
        self.assertTrue(any("missing local link" in e for e in validate(self.root)[0]))

    def test_reference_outside_collection(self):
        with self.skill.open("a") as f:
            f.write("\n[Outside](../../../../outside.md)\n")
        self.assertTrue(any("escapes collection" in e for e in validate(self.root)[0]))

    def test_private_machine_path(self):
        with self.skill.open("a") as f:
            f.write("\n/home/alice/workspace/project\n")
        self.assertTrue(any("private path" in e for e in validate(self.root)[0]))

    def test_unclosed_fence(self):
        with self.skill.open("a") as f:
            f.write("\n```sh\necho example\n")
        self.assertTrue(any("unclosed code fence" in e for e in validate(self.root)[0]))

    def test_unindexed_skill(self):
        (self.root / "README.md").write_text("# Collection\n")
        self.assertTrue(any("not indexed" in e for e in validate(self.root)[0]))

    def test_missing_skill(self):
        self.skill.unlink()
        self.assertTrue(any("missing SKILL.md" in e for e in validate(self.root)[0]))


if __name__ == "__main__":
    unittest.main()
