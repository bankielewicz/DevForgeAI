#!/usr/bin/env python3
"""Prototype of src/tests/brainstorm/test_structure.py, run against a scratch tree."""
import re
import sys
import unittest
from pathlib import Path

SKILL = Path(sys.argv.pop(1)) if len(sys.argv) > 1 else None
FW = SKILL / "references/frameworks"
SKILL_MD = (SKILL / "SKILL.md").read_text().splitlines()

NAMES = ["shortlist-ranking", "risk-first-mvp", "improve-existing", "problem-reframing", "diverge-converge"]
HEADINGS = ["## When to use / When not to use", "## Steps", "## Questions to ask", "## Mapping to the BRN",
            "## Evaluation method text", "## Example"]
CHECKLIST = [
    "- [ ] 1. Intake: topic, existing BRNs, clarifying questions",
    "- [ ] 2. Select a framework",
    "- [ ] 3. Diverge: problems, ideas, assumptions",
    "- [ ] 4. Evaluate with the framework",
    "- [ ] 5. Propose dispositions and ask the user to confirm",
    "- [ ] 6. Write the BRN",
    "- [ ] 7. Validate the BRN",
    "- [ ] 8. Report and hand off",
]
RULES = [
    "The user names a framework that the index lists",
    "The request supplies three or more candidate ideas, or names a backlog or list to use, and asks to rank, "
    "prioritise, choose among or cut them",
    "The request asks what to build first, for an MVP or a prototype, or what could make the idea fail",
    "Project kind is brownfield and the topic is improving, extending or fixing the existing product",
    "After intake, no problem can be stated with an affected person and what hurts them "
    "(the topic is a symptom, a goal or a solution)",
    "Otherwise",
]
TARGETS = ["that one", "`shortlist-ranking`", "`risk-first-mvp`", "`improve-existing`", "`problem-reframing`",
           "`diverge-converge`"]
CLAUSES = ["you named it", "you gave candidate ideas to rank or choose among",
           "you asked what to build first or what could make it fail",
           "the product exists and the topic is improving it",
           "no problem with an affected person and a hurt could be stated yet", "no more specific rule matched"]
NOLIST = "you named shortlist-ranking but gave no list, so I'm using diverge-converge instead"
TOKENS = {"shortlist-ranking": "Shortlist ranking:", "risk-first-mvp": "Risk-first MVP:",
          "improve-existing": "Improve existing:", "problem-reframing": "Problem reframing:",
          "diverge-converge": "Diverge-converge:"}


def outside_fences(text):
    out, fenced = [], False
    for line in text.splitlines():
        if line.startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            out.append(line)
    return out


def section(text, heading):
    lines = outside_fences(text)
    start = lines.index(heading)
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return lines[start + 1:end]


def table_rows(lines):
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines if l.startswith("|")]
    return [r for r in rows[2:]]  # drop header and separator


class Structure(unittest.TestCase):
    def index_text(self):
        return (FW / "INDEX.md").read_text()

    def test_index_rows_have_files(self):
        rows = table_rows(section(self.index_text(), "## Frameworks"))
        self.assertEqual([r[0] for r in rows], NAMES)
        for name, r in zip(NAMES, rows):
            self.assertEqual(r[1], f"[{name}.md]({name}.md)")
            self.assertTrue((FW / f"{name}.md").is_file(), name)

    def test_every_file_is_in_the_index(self):
        files = sorted(p.stem for p in FW.glob("*.md") if p.name != "INDEX.md")
        self.assertEqual(files, sorted(NAMES))

    def test_six_headings_in_order(self):
        for name in NAMES:
            text = (FW / f"{name}.md").read_text()
            heads = [l for l in outside_fences(text) if l.startswith("## ")]
            self.assertEqual(heads, HEADINGS, name)

    def test_selection_rules(self):
        rows = table_rows(section(self.index_text(), "## Selection rules"))
        self.assertEqual([r[0] for r in rows], ["1", "2", "3", "4", "5", "6"])
        self.assertEqual([r[1] for r in rows], RULES)
        self.assertEqual([r[2] for r in rows], TARGETS)

    def test_telling_the_user(self):
        text = self.index_text()
        rows = table_rows(section(text, "## Telling the user"))
        self.assertEqual([r[0] for r in rows], ["1", "2", "3", "4", "5", "6"])
        self.assertEqual([r[1] for r in rows], CLAUSES)
        self.assertIn("I'm using `name`, because clause.", text)
        self.assertIn(NOLIST, text)

    def test_checklist_pinned(self):
        i = SKILL_MD.index("Work through this checklist:")
        a = next(k for k in range(i, len(SKILL_MD)) if SKILL_MD[k] == "```")
        b = next(k for k in range(a + 1, len(SKILL_MD)) if SKILL_MD[k] == "```")
        self.assertEqual(SKILL_MD[a + 1:b], CHECKLIST)

    def test_checklist_first(self):
        fence = SKILL_MD.index("```")
        self.assertLessEqual(fence + 1, 25)
        self.assertLess(fence, SKILL_MD.index("## Inputs"))
        heads = [l for l in outside_fences("\n".join(SKILL_MD)) if l.startswith("## ")]
        self.assertEqual(heads, ["## Workflow", "## Inputs", "## Decisions that belong to the user",
                                 "## Output contract", "## Examples", "## References"])
        steps = [l for l in SKILL_MD if re.match(r"### [1-8]\. ", l)]
        self.assertEqual([l[:5] for l in steps], ["### " + str(n) + "." for n in range(1, 9)][:8] and
                         [l[:5] for l in steps])
        a, b = SKILL_MD.index("## Workflow"), SKILL_MD.index("## Inputs")
        self.assertTrue(all(a < SKILL_MD.index(l) < b for l in steps))

    def test_references_open_with_their_guide(self):
        for p in sorted((SKILL / "references").glob("*.md")) + sorted(FW.glob("*.md")):
            head = p.read_text().splitlines()[:15]
            if p.parent == FW and p.name != "INDEX.md":
                self.assertIn("## When to use / When not to use", head, p.name)
            elif p.name == "INDEX.md":
                self.assertIn("## Selection rules", head, p.name)
            else:
                self.assertIn("## Contents", head, p.name)

    def test_skill_md_length(self):
        self.assertLessEqual(len(SKILL_MD), 400)

    def test_skill_md_texts(self):
        text = "\n".join(SKILL_MD)
        s2 = text.split("### 2. Select a framework")[1].split("### 3. Diverge")[0]
        self.assertIn("selection rules", s2)
        self.assertIn("the first\nrule that matches the request decides", s2)
        self.assertIn("does not list", s2.replace("\n", " "))
        self.assertNotIn("best fit the topic", s2)
        s3 = text.split("### 3. Diverge")[1].split("### 4. Evaluate")[0]
        self.assertIn("or\n  the framework's *Steps* say otherwise", s3)

    def test_method_text_names_its_framework_only(self):
        for name in NAMES:
            sec = "\n".join(section((FW / f"{name}.md").read_text(), "## Evaluation method text"))
            quote = [l for l in sec.splitlines() if l.startswith("> ")]
            self.assertTrue(quote, name)
            self.assertTrue(quote[0].startswith("> " + TOKENS[name]), name)
            for other, tok in TOKENS.items():
                if other != name:
                    self.assertNotIn(tok, "\n".join(quote), (name, other))

    def test_mapping_names_the_four_fields(self):
        for name in NAMES:
            sec = "\n".join(section((FW / f"{name}.md").read_text(), "## Mapping to the BRN"))
            for field in ("`value`", "`effort`", "`risk`", "`score`"):
                self.assertIn(field, sec, (name, field))

    def test_no_citation_of_proposals(self):
        for p in FW.glob("*.md"):
            text = p.read_text()
            for bad in ("<!--", "docs/specs/brainstorming", "README.md", "TODO", "PLACEHOLDER"):
                self.assertNotIn(bad, text, (p.name, bad))

    def test_default_points_to_shortlist(self):
        sec = "\n".join(section((FW / "diverge-converge.md").read_text(), "## When to use / When not to use"))
        self.assertIn("use\n`shortlist-ranking`", sec)


if __name__ == "__main__":
    unittest.main(verbosity=1)
