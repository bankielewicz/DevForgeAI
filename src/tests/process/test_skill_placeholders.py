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
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return yaml.safe_load(m.group(1)), text[m.end():]


class Placeholders(unittest.TestCase):
    def test_the_skills_are_found(self):
        self.assertGreaterEqual(len(list(SKILLS.glob("*/SKILL.md"))), 10)

    def test_no_live_placeholder_in_a_skill_body(self):
        for path in sorted(SKILLS.glob("*/SKILL.md")):
            meta, body = split(path.read_text())
            names = meta.get("arguments") or []
            names = names.split() if isinstance(names, str) else names
            pattern = LIVE if not names else re.compile(LIVE.pattern + "|" + "|".join(rf"(?<!\\)\${n}\b" for n in names))
            for number, line in enumerate(body.splitlines(), 1):
                with self.subTest(skill=path.parent.name, line=number):
                    self.assertIsNone(pattern.search(line), line)

    def test_no_argument_word_in_a_reference(self):
        for path in sorted(SKILLS.glob("*/references/**/*.md")):
            for number, line in enumerate(path.read_text().splitlines(), 1):
                with self.subTest(file=str(path.relative_to(SKILLS)), line=number):
                    self.assertIsNone(WORD.search(line), line)


if __name__ == "__main__":
    unittest.main()
