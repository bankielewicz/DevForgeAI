"""Structural checks for the spec-lookup skill, SKL-011 (SPEC-014 VER-07; QR-01, QR-02, BEH-06, BEH-08, BEH-09).

- SKILL.md has at most 500 lines (QR-01), and every relative link in it resolves;
- its frontmatter has exactly SPEC-014 §5's fields (name, description, argument-hint and metadata with devforgeai-id
  and devforgeai-version), metadata values quoted, and validates against skill-frontmatter.schema.json;
- the description is the one SPEC-014 §5 fixes, at most 1024 characters, with no < or >;
- metadata.devforgeai-id and devforgeai-version equal provenance.yaml's id and version (QR-02), and provenance.yaml
  validates against skill.schema.json and records SKL-011 implementing SPEC-014 v3;
- SKILL.md names neither Write nor Edit as a tool to use, and says the skill writes and edits nothing (BEH-06);
- this repository's CLAUDE.md holds BEH-08's pointer, and its skill table a spec-lookup row;
- agents/spec-lookup.md's frontmatter is exactly SPEC-014 §5's (tools Bash and Read only, model haiku,
  omitClaudeMd true), and its body says to reply with the script's output lines unchanged and nothing else (BEH-09);
- SPEC-014 validates against spec.schema.json, and every BEH, ERR and QR item is covered by a VER item;
- the skill's folder holds what SPEC-014 §3 lists.

Run from the repository root:
    python3 -B src/tests/spec-lookup/test_structure.py
"""
import json
import re
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[3]
PLUGIN = ROOT / "src/claude/DevForgeAI"
SKILL = PLUGIN / "skills/spec-lookup"
AGENT = PLUGIN / "agents/spec-lookup.md"
SCHEMAS = ROOT / "src/schemas"
SPEC = ROOT / "docs/specs/spec/SPEC-014.md"
SKL, SPEC_VERSION = "SKL-011", 3


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


def spec_section_5():
    return SPEC.read_text().split("## 5.")[1].split("## 6.")[0]


def spec_document(text):
    doc = {"frontmatter": yaml.load(frontmatter_text(text), Loader=_Loader)}
    for block in re.findall(r"```yaml items\n(.*?)```", text, re.S):
        for key, value in yaml.load(block, Loader=_Loader).items():
            doc.setdefault(key, []).extend(value)
    return doc


class Skill(unittest.TestCase):
    def setUp(self):
        self.text = (SKILL / "SKILL.md").read_text()
        self.fm = yaml.load(frontmatter_text(self.text), Loader=_Loader)
        self.prov = yaml.load((SKILL / "provenance.yaml").read_text(), Loader=_Loader)

    def test_skill_md_has_at_most_500_lines(self):
        self.assertLessEqual(len(self.text.splitlines()), 500)

    def test_frontmatter_keys(self):
        self.assertEqual(list(self.fm), ["name", "description", "argument-hint", "metadata"])
        self.assertEqual(list(self.fm["metadata"]), ["devforgeai-id", "devforgeai-version"])
        self.assertEqual(errors("skill-frontmatter.schema.json", self.fm), [])
        self.assertEqual(self.fm["name"], "spec-lookup")
        self.assertEqual(self.fm["argument-hint"], "[ID or term]")

    def test_metadata_values_are_quoted(self):
        raw = frontmatter_text(self.text)
        self.assertRegex(raw, r'\n  devforgeai-id: "SKL-011"\n')
        self.assertRegex(raw, r'\n  devforgeai-version: "\d+"(\n|$)')
        self.assertIsInstance(self.fm["metadata"]["devforgeai-version"], str)

    def test_description_is_the_one_spec_014_fixes(self):
        fixed = re.search(r"^description: (.*)$", spec_section_5(), re.M).group(1)
        self.assertEqual(self.fm["description"], fixed)
        self.assertLessEqual(len(self.fm["description"]), 1024)
        self.assertNotRegex(self.fm["description"], r"[<>]")

    def test_version_mirrors_provenance(self):
        self.assertEqual(self.fm["metadata"]["devforgeai-version"], str(self.prov["version"]))
        self.assertEqual(self.fm["metadata"]["devforgeai-id"], self.prov["id"])

    def test_provenance(self):
        self.assertEqual(errors("skill.schema.json", {"frontmatter": self.prov}), [])
        self.assertEqual((self.prov["id"], self.prov["skill_name"], self.prov["eval_tag"]),
                         (SKL, "spec-lookup", "spec-lookup"))
        self.assertIn({"id": "SPEC-014", "relation": "implements", "version": SPEC_VERSION, "hash": None},
                      self.prov["upstream"])
        # Approved by Bryan on 2026-10-04, after the qualification and the live VER-08.
        self.assertEqual((self.prov["status"], self.prov["approved_by"], self.prov["approved_on"]),
                         ("approved", "Bryan", "2026-10-04"))

    def test_relative_links_resolve(self):
        for target in re.findall(r"\]\(([^)#\s]+)\)", self.text):
            if "://" not in target:
                with self.subTest(target):
                    self.assertTrue((SKILL / target).exists(), target)

    def test_skill_folder_holds_what_spec_014_lists(self):
        self.assertEqual(sorted(p.name for p in SKILL.iterdir()),
                         ["SKILL.md", "provenance.yaml", "references", "scripts"])
        self.assertEqual(sorted(p.name for p in (SKILL / "references").iterdir()), ["citing.md"])
        self.assertEqual(sorted(p.name for p in (SKILL / "scripts").iterdir()), ["find_spec.py"])

    def test_skill_md_runs_the_bundled_script(self):
        self.assertIn("python3 ${CLAUDE_SKILL_DIR}/scripts/find_spec.py", self.text)
        self.assertIn("references/citing.md", self.text)

    def test_skill_names_neither_write_nor_edit(self):
        # BEH-06: the instructions use Bash for the script, Read for cited files and AskUserQuestion only.
        self.assertNotRegex(self.text, r"\b(Write|Edit|NotebookEdit)\b")
        self.assertIn("writes and edits nothing", self.text)


class Agent(unittest.TestCase):
    def setUp(self):
        self.text = AGENT.read_text()
        self.raw = frontmatter_text(self.text)
        self.fm = yaml.load(self.raw, Loader=_Loader)
        self.body = self.text.split("\n---\n", 1)[1]

    def test_frontmatter_is_the_one_spec_014_fixes(self):
        # §5's block is read line by line, splitting at the first ": ", since v3's description holds "parts: 'Script:'",
        # which isn't valid as a plain YAML value; the agent file quotes it, and the values must be equal.
        block = re.search(r"```yaml\n(  name: spec-lookup\n.*?)```", spec_section_5(), re.S).group(1)
        fixed = dict(line[2:].split(": ", 1) for line in block.splitlines() if line.strip())
        fixed["omitClaudeMd"] = {"true": True, "false": False}[fixed["omitClaudeMd"]]
        self.assertEqual(self.fm, fixed)
        self.assertEqual(list(self.fm), ["name", "description", "tools", "model", "omitClaudeMd"])

    def test_tools_are_bash_and_read_only(self):
        self.assertEqual([t.strip() for t in self.fm["tools"].split(",")], ["Bash", "Read"])
        self.assertNotIn("disallowedTools", self.fm)
        self.assertEqual((self.fm["model"], self.fm["omitClaudeMd"]), ("haiku", True))

    def test_body_returns_the_output_lines_unchanged_and_nothing_else(self):
        self.assertIn("exactly as printed", self.body)
        self.assertIn("nothing else", self.body)
        self.assertIn("one fenced block per query", self.body)
        self.assertIn("find_spec.py", self.body)


class Claude(unittest.TestCase):
    def setUp(self):
        self.text = (ROOT / "CLAUDE.md").read_text()

    def test_pointer_is_in_the_rules_for_changes(self):
        rules = self.text.split("## Rules a change must not break")[1].split("\n## ")[0]
        self.assertIn("/devforgeai:spec-lookup", rules)
        self.assertRegex(rules, r"never build what no spec, ADR or recorded decision covers")

    def test_skill_table_row(self):
        self.assertRegex(self.text, r"\n\| `spec-lookup` \| SKL-011[^|]*\| SPEC-014 v3")


class Spec(unittest.TestCase):
    def test_spec_validates_and_every_item_is_covered(self):
        doc = spec_document(SPEC.read_text())
        self.assertEqual(errors("spec.schema.json", doc), [])
        self.assertEqual((doc["frontmatter"]["version"], doc["frontmatter"]["status"]), (SPEC_VERSION, "approved"))
        covered = {c for v in doc["verifications"] for c in v.get("covers", [])}
        for key in ("behaviors", "errors", "quality_responses"):
            for item in doc[key]:
                with self.subTest(item["id"]):
                    self.assertIn(item["id"], covered)


if __name__ == "__main__":
    unittest.main()
