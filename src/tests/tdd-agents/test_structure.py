"""Structural checks for the three test-first agents (SPEC-020 VER-01; BEH-01, BEH-03, BEH-07, QR-01).

For agents/tdd-test-writer.md, agents/tdd-implementer.md and agents/tdd-verifier.md:
- each file is SPEC-020 §5's block for it, byte for byte;
- the frontmatter keys are exactly name, description, tools, model, effort, in that order; name equals the file
  name; tools equal §5's list, with no Agent; model claude-opus-5-5 and effort medium; the description is one
  double-quoted line that names the task message's line count;
- the body names no repository, owner, absolute path, test command or coverage figure (BEH-03);
- the body holds the headings, the evidence markers and the input-document checks §5 fixes;
- the verifier makes its fixed checks, runs earlier commits and mutants in a disposable worktree, and names the git commands that would change the
  worktree only in the one rule that forbids them (BEH-07);
- SPEC-020 validates against spec.schema.json, and every BEH, ERR and QR item is covered by a VER item.

Run from the repository root:
    python3 -B src/tests/tdd-agents/test_structure.py
"""
import json
import re
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[3]
AGENTS = ROOT / "src/claude/DevForgeAI/agents"
SCHEMAS = ROOT / "src/schemas"
SPEC = ROOT / "docs/specs/spec/SPEC-020.md"
SPEC_VERSION, SPEC_STATUS = 2, "in-review"   # version 1 approved 2026-11-09; version 2 awaits Bryan

WRITE_TOOLS = ["Read", "Grep", "Glob", "Edit", "Write", "Bash"]
TOOLS = {"tdd-test-writer": WRITE_TOOLS, "tdd-implementer": WRITE_TOOLS,
         "tdd-verifier": ["Read", "Grep", "Glob", "Bash"]}
LINES = {"tdd-test-writer": "three lines", "tdd-implementer": "four lines", "tdd-verifier": "six lines"}
STOP_HEADING = "## Stop and report, changing nothing more, when"
# BEH-03: nothing specific to one repository. Matched in any case.
FORBIDDEN = ["/home/", "bankielewicz", "npm run", "claude plugin", "95"]
TREE_COMMANDS = ["git checkout", "git switch", "git reset", "git restore", "git stash", "git clean"]


class _Loader(yaml.SafeLoader):
    pass


_Loader.yaml_implicit_resolvers = {k: [r for r in v if r[0] != "tag:yaml.org,2002:timestamp"]
                                   for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()}


def registry():
    reg = Registry()
    for p in SCHEMAS.glob("*.json"):
        s = json.loads(p.read_text())
        reg = reg.with_resource(s["$id"], Resource.from_contents(s)).with_resource(p.name, Resource.from_contents(s))
    return reg


def errors(schema, instance):
    v = Draft202012Validator(json.loads((SCHEMAS / schema).read_text()), registry=registry(),
                             format_checker=FormatChecker())
    return [f"{list(e.path)}: {e.message}" for e in v.iter_errors(instance)]


def frontmatter_text(text):
    return re.match(r"---\n(.*?)\n---\n", text, re.S).group(1)


def spec_blocks():
    """SPEC-020 §5's three file blocks, by agent name."""
    section = SPEC.read_text().split("## 5. Interfaces and contracts")[1].split("## 6. Behavior")[0]
    blocks = re.findall(r"### 5\.\d `(tdd-[a-z-]+)\.md`\n\n````markdown\n(.*?)````\n", section, re.S)
    return dict(blocks)


def spec_document(text):
    doc = {"frontmatter": yaml.load(frontmatter_text(text), Loader=_Loader)}
    for block in re.findall(r"```yaml items\n(.*?)```", text, re.S):
        for key, value in yaml.load(block, Loader=_Loader).items():
            doc.setdefault(key, []).extend(value)
    return doc


class Agents(unittest.TestCase):
    def each(self):
        for name in TOOLS:
            text = (AGENTS / f"{name}.md").read_text()
            raw = frontmatter_text(text)
            yield name, text, raw, yaml.load(raw, Loader=_Loader), text.split("\n---\n", 1)[1]

    def test_the_three_files_exist(self):
        for name in TOOLS:
            with self.subTest(name):
                self.assertTrue((AGENTS / f"{name}.md").is_file())

    def test_each_file_is_the_spec_s_block_byte_for_byte(self):
        blocks = spec_blocks()
        self.assertEqual(sorted(blocks), sorted(TOOLS))
        for name, text, *_ in self.each():
            with self.subTest(name):
                self.assertEqual(text, blocks[name])

    def test_frontmatter(self):
        for name, _, raw, fm, _ in self.each():
            with self.subTest(name):
                self.assertEqual(list(fm), ["name", "description", "tools", "model", "effort"])
                self.assertEqual(fm["name"], name)
                self.assertEqual([t.strip() for t in fm["tools"].split(",")], TOOLS[name])
                self.assertNotIn("Agent", fm["tools"])
                self.assertEqual((fm["model"], fm["effort"]), ("claude-opus-5-5", "medium"))

    def test_description_is_one_double_quoted_line_naming_the_task_message(self):
        for name, _, raw, fm, _ in self.each():
            with self.subTest(name):
                self.assertRegex(raw, r'(?m)^description: "[^"\n]*"$')
                self.assertIn(LINES[name], fm["description"])

    def test_body_names_nothing_of_one_repository(self):
        for name, *_, body in self.each():
            for s in FORBIDDEN:
                with self.subTest(name=name, string=s):
                    self.assertNotIn(s.lower(), body.lower())

    def test_body_headings(self):
        for name, *_, body in self.each():
            with self.subTest(name):
                for heading in ("## Steps", "## Rules", "## Reply format"):
                    self.assertIn(f"\n{heading}\n", body)
                if name == "tdd-verifier":
                    self.assertNotIn(STOP_HEADING, body)
                else:
                    self.assertIn(f"\n{STOP_HEADING}\n", body)

    def test_body_evidence_and_input_document_checks(self):
        for name, *_, body in self.each():
            with self.subTest(name):
                self.assertIn("[evidence: command N]", body)
                self.assertIn("NOT REPRODUCED" if name == "tdd-verifier" else "[UNVERIFIED]", body)
                for s in ("Refactor: none", "Refactor: allowed", "input document incomplete:", "missing input:"):
                    self.assertIn(s, body)
                self.assertIn("disposable worktrees", body)
                # ERR-07, in all three.
                self.assertIn("Never create what it's missing, and never claim its result.", body)

    def test_commit_names_in_the_replies(self):
        bodies = {name: body for name, *_, body in self.each()}
        self.assertIn("\nGREEN: <the green commit from step 8, or none when you stopped before making it>\n",
                      bodies["tdd-implementer"])
        # The refactor's undo deletes created files by name (ADR-005 D7 names git clean).
        self.assertEqual(bodies["tdd-implementer"].count("git clean"), 1)
        self.assertIn("never with `git clean`", bodies["tdd-implementer"])
        self.assertNotIn("git clean", bodies["tdd-test-writer"])
        self.assertIn("`Green commit:`", bodies["tdd-verifier"])
        self.assertIn("criterion <number>", bodies["tdd-verifier"])
        self.assertIn("VERDICT: PASS | FAIL | INCOMPLETE", bodies["tdd-verifier"])

    def test_verifier_s_fixed_checks(self):
        body = next(body for name, *_, body in self.each() if name == "tdd-verifier")
        checks = body.split("\nCHECKS:\n")[1].split("\nMUTANTS:\n")[0].splitlines()
        self.assertEqual([line.split(":")[0].split(",")[0] for line in checks],
                         ["- start", "- commits", "- red", "- command <number>", "- paths", "- criterion <number>",
                          "- end"])
        self.assertIn("don't run it\n   again: its line cites that command", body)
        self.assertIn("`INCOMPLETE` when the `start` line is `NOT REPRODUCED`", body)

    def test_verifier_never_changes_the_worktree(self):
        body = next(body for name, *_, body in self.each() if name == "tdd-verifier")
        self.assertIn("\n## Disposable worktrees\n", body)
        self.assertIn("git -C <worktree> worktree add --detach <folder> <commit>", body)
        self.assertIn("git -C <worktree> worktree remove --force <folder>", body)
        # The one rule that forbids them is the first bullet under "## Rules"; they appear nowhere else.
        rule = body.split("\n## Rules\n")[1].split("\n- ")[1]
        self.assertTrue(rule.startswith("Never change the worktree"))
        for command in TREE_COMMANDS:
            with self.subTest(command):
                self.assertIn(f"`{command}`", rule)
                self.assertEqual(body.count(command), 1)
        self.assertNotIn("git -C <worktree> checkout", body)
        self.assertIn("Remove only a folder you added in this run.", body)
        self.assertIn("never in the\n   worktree", body)


class Spec(unittest.TestCase):
    def test_spec_validates_and_every_item_is_covered(self):
        doc = spec_document(SPEC.read_text())
        self.assertEqual(errors("spec.schema.json", doc), [])
        self.assertEqual((doc["frontmatter"]["version"], doc["frontmatter"]["status"]), (SPEC_VERSION, SPEC_STATUS))
        covered = {c for v in doc["verifications"] for c in v.get("covers", [])}
        for key in ("behaviors", "errors", "quality_responses"):
            for item in doc[key]:
                with self.subTest(item["id"]):
                    self.assertIn(item["id"], covered)


if __name__ == "__main__":
    unittest.main()
