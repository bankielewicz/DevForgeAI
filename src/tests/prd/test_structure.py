"""Structural checks for SKL-002 v3 and SKL-003 v5 (docs/runbooks/spec-002-v2-verification-plan.md §2).

- SKILL.md frontmatter against skill-frontmatter.schema.json, and the description the spec's §5 fixes;
- provenance.yaml against skill.schema.json, implementing the spec version this build targets;
- metadata.devforgeai-version equals provenance.yaml's version (QR-02);
- SKILL.md is at most 500 lines (NFR-001, QR-01), and every relative link in it resolves;
- SPEC-002 v4 (in review; SKL-002 v3 still implements v3) and SPEC-003 v4 validate against
  spec.schema.json, and every BEH, ERR and QR item is covered by a VER item.

Byte-identity of the shared policy files is in test_shared_files.py. Run from the repository root:
    python3 -B src/tests/prd/test_structure.py
"""
import json
import re
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / "src/claude/DevForgeAI/skills"
SCHEMAS = ROOT / "src/schemas"
SPECS = ROOT / "docs/specs/spec"
TARGETS = {"prd": ("SKL-002", 3, "SPEC-002", 3), "architecture": ("SKL-003", 5, "SPEC-003", 4)}
SPEC_STATE = {"SPEC-002": (4, "in-review"), "SPEC-003": (4, "approved")}  # SPEC-002 v4: issues #36-#38, #40


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


def frontmatter(text):
    return yaml.load(re.match(r"---\n(.*?)\n---\n", text, re.S).group(1), Loader=_Loader)


def spec_document(text):
    doc = {"frontmatter": frontmatter(text)}
    for block in re.findall(r"```yaml items\n(.*?)```", text, re.S):
        for key, value in yaml.load(block, Loader=_Loader).items():
            doc.setdefault(key, []).extend(value)
    return doc


class Skills(unittest.TestCase):
    def test_frontmatter_and_provenance(self):
        for name, (skl, version, spec, spec_version) in TARGETS.items():
            with self.subTest(name):
                skill_md = (SKILLS / name / "SKILL.md").read_text()
                fm = frontmatter(skill_md)
                self.assertEqual(errors("skill-frontmatter.schema.json", fm), [])
                self.assertEqual(fm["name"], name)
                self.assertEqual(fm["metadata"], {"devforgeai-id": skl, "devforgeai-version": str(version)})
                spec_text = (SPECS / f"{spec}.md").read_text()
                fixed = re.search(r"^description: (.*)$", spec_text.split("## 5.")[1], re.M).group(1)
                self.assertEqual(fm["description"], fixed, "the description is fixed by the spec's §5")
                prov = yaml.load((SKILLS / name / "provenance.yaml").read_text(), Loader=_Loader)
                self.assertEqual(errors("skill.schema.json", {"frontmatter": prov}), [])
                self.assertEqual((prov["id"], prov["version"], prov["skill_name"]), (skl, version, name))
                self.assertIn({"id": spec, "relation": "implements", "version": spec_version, "hash": None},
                              prov["upstream"])
                # Approved by Bryan on 2026-09-30, after the policy cases were requalified.
                self.assertEqual((prov["status"], prov["approved_by"], prov["approved_on"]),
                                 ("approved", "Bryan", "2026-09-30"))

    def test_skill_md_length_and_links(self):
        for name in TARGETS:
            with self.subTest(name):
                text = (SKILLS / name / "SKILL.md").read_text()
                self.assertLessEqual(len(text.splitlines()), 500)
                for link in re.findall(r"\]\(([^)#]+)\)", text):
                    self.assertTrue((SKILLS / name / link).is_file(), link)
                for rel in re.findall(r"\$\{CLAUDE_SKILL_DIR\}/([\w./-]+)", text):
                    if not rel.startswith(".."):
                        self.assertTrue((SKILLS / name / rel).exists(), rel)


class Specs(unittest.TestCase):
    def test_specs_validate_and_every_item_is_verified(self):
        for spec, (version, status) in SPEC_STATE.items():
            with self.subTest(spec):
                doc = spec_document((SPECS / f"{spec}.md").read_text())
                self.assertEqual(errors("spec.schema.json", doc), [])
                self.assertEqual((doc["frontmatter"]["version"], doc["frontmatter"]["status"]), (version, status))
                ids = {i["id"] for k in ("behaviors", "errors", "quality_responses") for i in doc[k]}
                covered = {c for v in doc["verifications"] for c in v["covers"]}
                self.assertEqual(ids - covered, set())


if __name__ == "__main__":
    unittest.main()
