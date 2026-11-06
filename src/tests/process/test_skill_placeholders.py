"""No skill text holds a live argument placeholder (#135).

Claude Code substitutes $ARGUMENTS, $ARGUMENTS[N], $N and a declared $name in SKILL.md
(docs/research/Claude/skills/skills.md, "Available string substitutions"). A skill that describes its input with the
word $ARGUMENTS therefore reads the user's input in its place, and empty backticks when there is none; and a live
placeholder stops Claude Code appending the `ARGUMENTS:` line the skills rely on. A probe on 2026-11-04 (2.1.317, typed
and through the Skill tool) saw all of this. The skills say "the arguments" instead.

A reference file is read with the Read tool, not substituted, so only $ARGUMENTS is checked there, for one term.

Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider src/tests/process
"""
import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / "src/claude/DevForgeAI/skills"
# An unescaped placeholder: a single backslash directly before the token escapes it (skills.md).
LIVE = re.compile(r"(?<!\\)\$(ARGUMENTS\b|\d)")
WORD = re.compile(r"\$ARGUMENTS\b")


def split(text):
    """The frontmatter mapping and the body; (None, text) when there's no frontmatter, or it's empty (#155)."""
    m = re.match(r"---\n(.*?)\n?---\n", text, re.S)
    if not m:
        return None, text
    return yaml.safe_load(m.group(1)), text[m.end():]


class Placeholders(unittest.TestCase):
    def test_the_skills_are_found(self):
        self.assertGreaterEqual(len(list(SKILLS.glob("*/SKILL.md"))), 10)

    def test_no_live_placeholder_in_a_skill_body(self):
        for path in sorted(SKILLS.glob("*/SKILL.md")):
            meta, body = split(path.read_text())
            with self.subTest(skill=path.parent.name, frontmatter=True):
                self.assertIsInstance(meta, dict, f"{path} doesn't open with a frontmatter mapping")
            if not isinstance(meta, dict):
                continue
            names = meta.get("arguments") or []
            names = names.split() if isinstance(names, str) else names
            pattern = LIVE if not names else re.compile(LIVE.pattern + "|" + "|".join(rf"(?<!\\)\${n}\b" for n in names))
            for number, line in enumerate(body.splitlines(), 1):
                with self.subTest(skill=path.parent.name, line=number):
                    self.assertIsNone(pattern.search(line), line)

    def test_a_skill_with_no_frontmatter_is_reported_not_a_crash(self):
        """A SKILL.md that doesn't open with frontmatter fails with a message, not an AttributeError (#155)."""
        self.assertEqual(split("# A skill\n\nNo frontmatter.\n"), (None, "# A skill\n\nNo frontmatter.\n"))
        self.assertEqual(split("---\n\n---\nBody\n"), (None, "Body\n"))

    def test_the_skill_template_has_no_live_placeholder(self):
        """The next skill starts by copying this file (.claude/rules/skills.md)."""
        self.assertIsNone(LIVE.search((ROOT / "src/templates/skill/SKILL.md").read_text()))

    def test_no_argument_word_in_a_reference(self):
        for path in sorted(SKILLS.glob("*/references/**/*.md")):
            for number, line in enumerate(path.read_text().splitlines(), 1):
                with self.subTest(file=str(path.relative_to(SKILLS)), line=number):
                    self.assertIsNone(WORD.search(line), line)


if __name__ == "__main__":
    unittest.main()
