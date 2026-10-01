"""Byte-identity of the policy files the prd, architecture and context skills share (SPEC-002 §5, D-09;
SPEC-003 §3 and VER-12 (f); SPEC-011 §3 and §11 step 5): references/policy.md, references/defaults.md,
scripts/validate_policy.py and the policy and common schema copies, across the three skills, and every
schema copy against src/schemas/. The context skill also holds unchanged copies of context.schema.json and
ambiguities.schema.json, which its context_check.py runs.

Run from the repository root:
    python3 -B src/tests/prd/test_shared_files.py
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / "src/claude/DevForgeAI/skills"
SHARED = ["references/policy.md", "references/defaults.md", "scripts/validate_policy.py",
          "references/schemas/policy.schema.json", "references/schemas/common.schema.json"]
SHARING = ("prd", "architecture", "context")
SCHEMA_COPIES = {"prd": ["common.schema.json", "policy.schema.json"],
                 "architecture": ["common.schema.json", "policy.schema.json"],
                 "context": ["ambiguities.schema.json", "common.schema.json", "context.schema.json",
                             "policy.schema.json"]}


class SharedPolicyFiles(unittest.TestCase):
    def test_each_shared_file_is_byte_identical_in_every_skill(self):
        for rel in SHARED:
            for skill in SHARING[1:]:
                with self.subTest(rel=rel, skill=skill):
                    prd, other = SKILLS / "prd" / rel, SKILLS / skill / rel
                    self.assertTrue(prd.is_file() and other.is_file(), rel)
                    self.assertEqual(prd.read_bytes(), other.read_bytes(), f"{rel} differs between prd and {skill}")

    def test_schema_copies_are_unchanged_copies_of_src_schemas(self):
        for skill in SHARING:
            for name in SCHEMA_COPIES[skill]:
                with self.subTest(skill=skill, schema=name):
                    self.assertEqual((SKILLS / skill / "references/schemas" / name).read_bytes(),
                                     (ROOT / "src/schemas" / name).read_bytes())

    def test_schema_folders_hold_only_their_copies(self):
        for skill in SHARING:
            with self.subTest(skill):
                names = sorted(p.name for p in (SKILLS / skill / "references/schemas").iterdir())
                self.assertEqual(names, SCHEMA_COPIES[skill])

    def test_script_is_executable_in_every_skill(self):
        for skill in SHARING:
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
