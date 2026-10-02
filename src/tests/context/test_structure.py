"""Structural checks for the context skill, SKL-010 (SPEC-011 VER-25; QR-01, QR-02).

- SKILL.md has at most 500 lines (NFR-001, QR-01), and every relative link in it resolves;
- its frontmatter has exactly name, description, argument-hint and metadata (devforgeai-id,
  devforgeai-version), metadata values quoted, and validates against skill-frontmatter.schema.json;
- the description is the one SPEC-011 §5 fixes, at most 1024 characters, with no < or >;
- metadata.devforgeai-version equals provenance.yaml's version (QR-02), and provenance.yaml validates
  against skill.schema.json and records SKL-010 implementing SPEC-011 v3;
- SPEC-011 validates against spec.schema.json, and every BEH, ERR and QR item is covered by a VER item;
- the skill's folder holds what SPEC-011 §3 lists.

Run from the repository root:
    python3 -B src/tests/context/test_structure.py
"""
import json
import re
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "src/claude/DevForgeAI/skills/context"
SCHEMAS = ROOT / "src/schemas"
SPEC = ROOT / "docs/specs/spec/SPEC-011.md"
SKL, SPEC_VERSION = "SKL-010", 3


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
        self.assertEqual(self.fm["name"], "context")
        self.assertEqual(self.fm["argument-hint"], "[document]")

    def test_metadata_values_are_quoted(self):
        raw = frontmatter_text(self.text)
        self.assertRegex(raw, r'\n  devforgeai-id: "SKL-010"\n')
        self.assertRegex(raw, r'\n  devforgeai-version: "\d+"(\n|$)')
        self.assertIsInstance(self.fm["metadata"]["devforgeai-version"], str)

    def test_description_is_the_one_spec_011_fixes(self):
        fixed = re.search(r"^description: (.*)$", SPEC.read_text().split("## 5.")[1], re.M).group(1)
        self.assertEqual(self.fm["description"], fixed)
        self.assertLessEqual(len(self.fm["description"]), 1024)
        self.assertNotRegex(self.fm["description"], r"[<>]")

    def test_version_mirrors_provenance(self):
        self.assertEqual(self.fm["metadata"]["devforgeai-version"], str(self.prov["version"]))
        self.assertEqual(self.fm["metadata"]["devforgeai-id"], self.prov["id"])

    def test_provenance(self):
        self.assertEqual(errors("skill.schema.json", {"frontmatter": self.prov}), [])
        self.assertEqual((self.prov["id"], self.prov["skill_name"], self.prov["eval_tag"]), (SKL, "context", "context"))
        self.assertIn({"id": "SPEC-011", "relation": "implements", "version": SPEC_VERSION, "hash": None},
                      self.prov["upstream"])

    def test_relative_links_resolve(self):
        for target in re.findall(r"\]\(([^)#\s]+)\)", self.text):
            if "://" not in target:
                with self.subTest(target):
                    self.assertTrue((SKILL / target).exists(), target)

    def test_skill_folder_holds_what_spec_011_lists(self):
        self.assertEqual(sorted(p.name for p in SKILL.iterdir()),
                         ["SKILL.md", "assets", "provenance.yaml", "references", "scripts"])
        self.assertEqual(sorted(p.name for p in (SKILL / "references").iterdir()),
                         ["defaults.md", "documents.md", "inspection.md", "interview.md", "output-rules.md",
                          "policy.md", "schemas"])
        self.assertEqual(sorted(p.name for p in (SKILL / "scripts").iterdir()),
                         ["context_check.py", "validate_policy.py"])
        self.assertEqual(len(list((SKILL / "assets").iterdir())), 13)
        self.assertTrue((SKILL / "scripts/context_check.py").stat().st_mode & 0o111)

    def test_skill_md_carries_the_substituted_variables(self):
        # Claude Code substitutes these only in SKILL.md, so the commands and the session ID live here.
        self.assertIn('session: "${CLAUDE_SESSION_ID}"', self.text)
        self.assertIn("claude-code (session ${CLAUDE_SESSION_ID})", self.text)
        for command in ("validate_policy.py docs/specs/policy", "context_check.py snapshot new",
                        "context_check.py check --snapshot <start>", "context_check.py restore"):
            self.assertIn(f"python3 ${{CLAUDE_SKILL_DIR}}/scripts/{command}", self.text)
        self.assertIn("${CLAUDE_SKILL_DIR}/../epic/SKILL.md", self.text)


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
