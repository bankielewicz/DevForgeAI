"""Structure tests for the brainstorm skill's text (SPEC-001; framework-catalog VER-18).

They check what no eval can: that SKILL.md opens with the task list and keeps its eight checklist lines, that
its headings stand in the agreed order, that every reference file shows its guide at the top, and that the
framework index and the framework files agree with each other.

Run from the repository root:
    python3 -B src/tests/brainstorm/test_structure.py
"""
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PLUGIN = ROOT / "src/claude/DevForgeAI"
SKILL = PLUGIN / "skills/brainstorm"
SKILL_MD = SKILL / "SKILL.md"
REFERENCES = SKILL / "references"
FRAMEWORKS = REFERENCES / "frameworks"
INDEX = FRAMEWORKS / "INDEX.md"
MANIFEST = PLUGIN / "progress/manifests/brainstorm.json"
VALIDATOR = SKILL / "scripts/validate_brn.py"

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
CHECKLIST_LINE = re.compile(r"^\s*- \[ \] (\d+)\. (.+?)\s*$")  # progress/evaluate.py's pattern
H2 = [
    "## Workflow",
    "## Decisions that belong to the user",
    "## Inputs",
    "## Working through the steps",
    "## Output contract",
    "## Examples",
    "## References",
]
STEPS = [
    "### 1. Intake",
    "### 2. Select a framework",
    "### 3. Diverge",
    "### 4. Evaluate",
    "### 5. Propose dispositions and confirm",
    "### 6. Write the BRN",
    "### 7. Validate the BRN",
    "### 8. Report and hand off",
]
SECTIONS = [
    "## When to use / When not to use",
    "## Steps",
    "## Questions to ask",
    "## Mapping to the BRN",
    "## Evaluation method text",
    "## Example",
]
FRAMEWORK_HEADER = "| framework | file | use when | avoid when |"
RULES_HEADER = "| # | When | Framework | Tell the user |"
FENCE = re.compile(r"^\s*(`{3,})(.*)$")

BRN = """\
---
id: BRN-001
type: brainstorm
title: "Example"
status: draft
version: 1
created: 2026-11-18
updated: 2026-11-18
owner: "Dana"
authors: ["Dana", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-fable-5-2"
  session: "0f0f0f0f-0000-4000-8000-000000000001"
reviewed_by: []
approved_by: ""
approved_on: null
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
# --- brainstorm-specific ---
participants: []
sources: []
---

# BRN-001 — Example

## 1. Context

Example.

## 2. Problems

%(problems)s

## 3. Target users

Example.

## 4. Ideas

%(ideas)s

## 5. Evaluation method

Example.

## 6. Convergence

Example.

## 7. Assumptions and open questions

%(assumptions)s

- None.

## 8. Candidate success signals

- None.

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2026-11-18 | claude-code (session 0f0f0f0f-0000-4000-8000-000000000001) | Initial draft |
"""
DEFAULT_PROBLEMS = """\
problems:
  - id: PRB-01
    status: active
    statement: "Example."
    who: "Example"
    evidence: "[NEEDS CLARIFICATION: example]"
    severity: medium"""


def read_lines(path):
    return path.read_text(encoding="utf-8").split("\n")


def fences(lines):
    """[(info string, [content lines])] for each fenced block, and the set of line indexes inside any fence."""
    blocks, inside, marker, info, body = [], set(), None, "", []
    for i, line in enumerate(lines):
        m = FENCE.match(line)
        if marker is None:
            if m:
                marker, info, body = m.group(1), m.group(2).strip(), []
                inside.add(i)
        else:
            inside.add(i)
            if m and len(m.group(1)) >= len(marker) and not m.group(2).strip():
                blocks.append((info, body))
                marker = None
            else:
                body.append(line)
    return blocks, inside


def headings(lines, prefix):
    """The lines outside fences that start with the prefix, with their indexes."""
    _, inside = fences(lines)
    return [(i, line.rstrip()) for i, line in enumerate(lines) if i not in inside and line.startswith(prefix)]


def table(lines, header):
    """The body rows of the table whose header line is given, each a list of its cells."""
    start = lines.index(header)
    rows = []
    for line in lines[start + 2:]:
        if not line.startswith("|"):
            break
        rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return rows


def section(lines, heading):
    """The lines under a ## heading, up to the next ## heading outside a fence."""
    marks = headings(lines, "## ")
    for n, (i, text) in enumerate(marks):
        if text == heading:
            end = marks[n + 1][0] if n + 1 < len(marks) else len(lines)
            return lines[i + 1:end]
    raise AssertionError("no heading %r" % heading)


def framework_files():
    return sorted(p for p in FRAMEWORKS.glob("*.md") if p.name != "INDEX.md")


class SkillLayout(unittest.TestCase):
    def setUp(self):
        self.lines = read_lines(SKILL_MD)

    def test_checklist_lines_are_the_pinned_eight(self):
        found = [line.strip() for line in self.lines if CHECKLIST_LINE.match(line)]
        self.assertEqual(found, CHECKLIST)

    def test_checklist_hash_matches_the_progress_manifest(self):
        digest = "sha256:" + hashlib.sha256("\n".join(CHECKLIST).encode("utf-8")).hexdigest()
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(digest, manifest["checklistHash"])

    def test_workflow_section_holds_only_the_checklist(self):
        body = [line for line in section(self.lines, "## Workflow") if line.strip()]
        self.assertEqual(body, ["Work through this checklist:", "```"] + CHECKLIST + ["```"])

    def test_checklist_fence_opens_early_and_before_decisions(self):
        first = next(i for i, line in enumerate(self.lines) if CHECKLIST_LINE.match(line))
        fence = first - 1
        self.assertEqual(self.lines[fence], "```")
        close = self.lines.index("---", 1)  # the frontmatter's closing line
        self.assertLessEqual(fence - close, 17,
                             "the checklist's fence must open at most 17 lines after the frontmatter")
        self.assertLess(fence, self.lines.index("## Decisions that belong to the user"))

    def test_h2_headings_in_order(self):
        self.assertEqual([text for _, text in headings(self.lines, "## ")], H2)
        self.assertEqual([text for _, text in headings(self.lines, "# ")], ["# Brainstorm"])

    def test_step_headings_sit_in_working_through_the_steps(self):
        marks = headings(self.lines, "### ")
        self.assertEqual([text for _, text in marks], STEPS)
        start = self.lines.index("## Working through the steps")
        end = self.lines.index("## Output contract")
        for i, text in marks:
            self.assertTrue(start < i < end, text)

    def test_no_reference_to_the_old_heading(self):
        self.assertNotIn("(Workflow", "\n".join(self.lines))

    def test_at_most_400_lines(self):
        self.assertLessEqual(len(SKILL_MD.read_text(encoding="utf-8").splitlines()), 400)

    def test_frameworks_are_reached_through_the_index(self):
        text = "\n".join(self.lines)
        self.assertIn("references/frameworks/INDEX.md", text)
        for path in framework_files():
            if path.stem != "diverge-converge":
                self.assertNotIn(path.name, text)


class ReferenceGuides(unittest.TestCase):
    def test_every_reference_shows_its_guide_within_15_lines(self):
        paths = sorted(REFERENCES.glob("*.md")) + sorted(FRAMEWORKS.glob("*.md"))
        self.assertGreaterEqual(len(paths), 4)
        for path in paths:
            top = read_lines(path)[:15]
            self.assertTrue(any(line == "## Contents" or line.startswith("## When to use") for line in top),
                            "%s: no '## Contents' or '## When to use' line in its first 15 lines" % path.name)


class FrameworkIndex(unittest.TestCase):
    def setUp(self):
        self.lines = read_lines(INDEX)
        self.rows = table(self.lines, FRAMEWORK_HEADER)
        self.names = [row[0] for row in self.rows]

    def test_rows_and_files_match(self):
        self.assertEqual(len(self.names), len(set(self.names)))
        self.assertEqual(sorted(self.names), [p.stem for p in framework_files()])
        for row in self.rows:
            self.assertEqual(len(row), 4, row)
            self.assertEqual(row[1], "[%s.md](%s.md)" % (row[0], row[0]))
            self.assertTrue(row[2] and row[3], row)

    def test_selection_rules(self):
        rules = table(self.lines, RULES_HEADER)
        self.assertEqual([row[0] for row in rules], [str(n) for n in range(1, len(rules) + 1)])
        self.assertEqual(rules[0][2], "the one named")
        self.assertEqual(rules[0][3], "Framework: `<name>`, because you named it.")
        chosen = []
        for row in rules[1:]:
            self.assertEqual(len(row), 4, row)
            name = row[2].strip("`")
            self.assertEqual(row[2], "`%s`" % name)
            self.assertIn(name, self.names)
            self.assertTrue(row[3].startswith("Framework: `%s`, because " % name), row)
            self.assertTrue(row[3].endswith("."), row)
            chosen.append(name)
        self.assertEqual(chosen[-1], "diverge-converge")
        self.assertEqual(chosen, [name for name in self.names if name in chosen])

    def test_index_lists_the_six_required_headings(self):
        body = section(self.lines, "## Required sections")
        listed = [line.split("`")[1] for line in body if re.match(r"^\d\. `## ", line)]
        self.assertEqual(listed, SECTIONS)


class FrameworkFiles(unittest.TestCase):
    def test_six_headings_in_order(self):
        for path in framework_files():
            lines = read_lines(path)
            self.assertTrue(lines[0].startswith("# "), path.name)
            self.assertEqual([text for _, text in headings(lines, "## ")], SECTIONS, path.name)

    def test_method_texts_open_with_distinct_words(self):
        tokens = {}
        for path in framework_files():
            quoted = [line for line in section(read_lines(path), "## Evaluation method text")
                      if line.startswith("> ")]
            self.assertTrue(quoted and ":" in quoted[0], "%s: no quoted method text with a colon" % path.name)
            tokens[path.name] = quoted[0][2:].split(":")[0] + ":"
        values = list(tokens.values())
        for a in values:
            self.assertEqual(sum(1 for b in values if b.startswith(a)), 1, tokens)

    def test_examples_pass_the_validator(self):
        for path in framework_files():
            blocks, _ = fences(section(read_lines(path), "## Example"))
            found = {}
            for info, body in blocks:
                if info == "yaml" and body:
                    found[body[0].rstrip(":")] = "\n".join(body)
            self.assertIn("ideas", found, path.name)
            parts = {
                "problems": found.get("problems", DEFAULT_PROBLEMS),
                "ideas": found["ideas"],
                "assumptions": found.get("assumptions", ""),
            }
            text = BRN % {key: "```yaml items\n%s\n```" % value if value else "" for key, value in parts.items()}
            with tempfile.TemporaryDirectory() as tmp:
                brn = Path(tmp) / "docs/specs/brainstorm/BRN-001.md"
                brn.parent.mkdir(parents=True)
                brn.write_text(text, encoding="utf-8")
                for flags in (["-B"], ["-B", "-S"]):
                    proc = subprocess.run([sys.executable] + flags + [str(VALIDATOR), str(brn)],
                                          capture_output=True, text=True)
                    self.assertEqual(proc.returncode, 0, "%s %s: %s" % (path.name, flags, proc.stdout))
                    self.assertTrue(proc.stdout.startswith("OK: "), proc.stdout)


if __name__ == "__main__":
    unittest.main()
