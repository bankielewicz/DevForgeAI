"""Byte-identity of the policy files the prd and architecture skills share (SPEC-002 §5, D-09; SPEC-003 §3
and VER-12 (f)): references/policy.md, references/defaults.md, scripts/validate_policy.py and the
references/schemas/ copies, across both skills, and the schema copies against src/schemas/.

Run from the repository root:
    python3 -B src/tests/prd/test_shared_files.py
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / "src/claude/DevForgeAI/skills"
SHARED = ["references/policy.md", "references/defaults.md", "scripts/validate_policy.py",
          "references/schemas/policy.schema.json", "references/schemas/common.schema.json"]


class SharedPolicyFiles(unittest.TestCase):
    def test_each_shared_file_is_byte_identical_in_both_skills(self):
        for rel in SHARED:
            with self.subTest(rel):
                prd, arch = SKILLS / "prd" / rel, SKILLS / "architecture" / rel
                self.assertTrue(prd.is_file() and arch.is_file(), rel)
                self.assertEqual(prd.read_bytes(), arch.read_bytes(), f"{rel} differs between the skills")

    def test_schema_copies_are_unchanged_copies_of_src_schemas(self):
        for skill in ("prd", "architecture"):
            for name in ("policy.schema.json", "common.schema.json"):
                with self.subTest(skill=skill, schema=name):
                    self.assertEqual((SKILLS / skill / "references/schemas" / name).read_bytes(),
                                     (ROOT / "src/schemas" / name).read_bytes())

    def test_schema_folders_hold_only_the_two_copies(self):
        for skill in ("prd", "architecture"):
            with self.subTest(skill):
                names = sorted(p.name for p in (SKILLS / skill / "references/schemas").iterdir())
                self.assertEqual(names, ["common.schema.json", "policy.schema.json"])

    def test_script_is_executable_in_both_skills(self):
        for skill in ("prd", "architecture"):
            with self.subTest(skill):
                self.assertTrue((SKILLS / skill / "scripts/validate_policy.py").stat().st_mode & 0o111)

    def test_shared_text_is_skill_neutral(self):
        # A skill-specific word in a shared file would force the copies apart.
        for rel in SHARED[:3]:
            text = (SKILLS / "prd" / rel).read_text()
            for word in ("PRD-", "ARCH-", "SKILL.md step", "BEH-", "ERR-0"):
                with self.subTest(rel=rel, word=word):
                    self.assertNotIn(word, text)


if __name__ == "__main__":
    unittest.main()
