"""Structural checks for the precompact skill, SKL-012 (SPEC-015 VER-08; QR-01, QR-02, ERR-02, ERR-03, ERR-05, ERR-06).

- SKILL.md has at most 500 lines (QR-01), and every reference, asset and script it names exists;
- its frontmatter has exactly SPEC-015 §5's fields (name, description, argument-hint, and metadata with
  devforgeai-id, devforgeai-version and devforgeai-tracked), metadata values quoted, devforgeai-tracked "false", and
  validates against skill-frontmatter.schema.json, whose const refuses any other value (SPEC-013 v18);
- the description is the one SPEC-015 §5 fixes, at most 1024 characters, with no < or >;
- metadata.devforgeai-id and devforgeai-version equal provenance.yaml's id and version (QR-02), and provenance.yaml
  validates against skill.schema.json and records SKL-012 implementing SPEC-015 v2;
- the assets hold DM-01's and DM-02's headings in order and use only [[fill: ...]] placeholders, never in backticks;
- references/handoff-rules.md holds every item of SPEC-015 §4's self-check;
- SKILL.md or its references state ERR-02's, ERR-03's, ERR-05's and ERR-06's handling;
- SKILL.md, the references and the assets hold no absolute path, no /home/ and no person's name (§2, generic);
- SKILL.md runs the bundled script and never names AskUserQuestion (the skill asks nothing, §2);
- this repository's CLAUDE.md skill table has a precompact row;
- SPEC-015 validates against spec.schema.json, and every BEH, ERR, QR and IF item is covered by a VER item;
- the skill's folder holds what SPEC-015 §3 lists.

Run from the repository root:
    python3 -B src/tests/precompact/test_structure.py
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
SKILL = PLUGIN / "skills/precompact"
SCHEMAS = ROOT / "src/schemas"
SPEC = ROOT / "docs/specs/spec/SPEC-015.md"
SKL, SPEC_VERSION = "SKL-012", 2
START_HEADINGS = ["## 1. What this is", "## 2. Verified state", "## 3. Decisions", "## 4. Read first",
                  "## 5. Outstanding", "## 6. Rules, traps and learnings", "## 7. Before acting"]
TASKS_HEADINGS = ["## Done", "## Next"]


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


def spec_text():
    return SPEC.read_text()


def spec_section(n):
    """The spec's section n, from its heading at the start of a line (§4's table quotes `## 5.` headings)."""
    return re.split(rf"(?m)^## {n + 1}\. ", re.split(rf"(?m)^## {n}\. ", spec_text())[1])[0]


def spec_document(text):
    doc = {"frontmatter": yaml.load(frontmatter_text(text), Loader=_Loader)}
    for block in re.findall(r"```yaml items\n(.*?)```", text, re.S):
        for key, value in yaml.load(block, Loader=_Loader).items():
            doc.setdefault(key, []).extend(value)
    return doc


def self_check_items():
    """SPEC-015 §4's self-check, its nine numbered items, each joined onto one line."""
    block = spec_section(4).split("**The self-check**")[1]
    items, current = [], None
    for line in block.splitlines():
        m = re.match(r"^(\d+)\. (.*)$", line)
        if m:
            current = [m.group(2)]
            items.append(current)
        elif current is not None and line.startswith("   "):
            current.append(line.strip())
        elif current is not None and line.strip():
            break
    return [" ".join(parts) for parts in items]


def squash(text):
    return re.sub(r"\s+", " ", text)


def without_code(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"(`+).+?\1", "", text)


def skill_texts():
    paths = [SKILL / "SKILL.md"] + sorted((SKILL / "references").glob("*.md")) + sorted((SKILL / "assets").glob("*.md"))
    return {p.relative_to(SKILL).as_posix(): p.read_text() for p in paths}


class Skill(unittest.TestCase):
    def setUp(self):
        self.text = (SKILL / "SKILL.md").read_text()
        self.fm = yaml.load(frontmatter_text(self.text), Loader=_Loader)
        self.prov = yaml.load((SKILL / "provenance.yaml").read_text(), Loader=_Loader)

    def test_skill_md_has_at_most_500_lines(self):
        self.assertLessEqual(len(self.text.splitlines()), 500)

    def test_frontmatter_keys(self):
        self.assertEqual(list(self.fm), ["name", "description", "argument-hint", "metadata"])
        self.assertEqual(list(self.fm["metadata"]), ["devforgeai-id", "devforgeai-version", "devforgeai-tracked"])
        self.assertEqual(errors("skill-frontmatter.schema.json", self.fm), [])
        self.assertEqual(self.fm["name"], "precompact")
        self.assertEqual(self.fm["argument-hint"], "[note for the next session]")
        self.assertEqual(self.fm["metadata"]["devforgeai-tracked"], "false")

    def test_metadata_values_are_quoted(self):
        raw = frontmatter_text(self.text)
        self.assertRegex(raw, r'\n  devforgeai-id: "SKL-012"\n')
        self.assertRegex(raw, r'\n  devforgeai-version: "\d+"\n')
        self.assertRegex(raw, r'\n  devforgeai-tracked: "false"(\n|$)')

    def test_schema_refuses_any_other_tracked_value(self):
        for value in ("False", "no", "true", "0"):
            with self.subTest(value):
                fm = dict(self.fm, metadata=dict(self.fm["metadata"], **{"devforgeai-tracked": value}))
                self.assertTrue(errors("skill-frontmatter.schema.json", fm))
        fm = dict(self.fm, metadata=dict(self.fm["metadata"], **{"devforgeai-tracked": False}))
        self.assertTrue(errors("skill-frontmatter.schema.json", fm))

    def test_description_is_the_one_spec_015_fixes(self):
        fixed = re.search(r"^description: (.*)$", spec_section(5), re.M).group(1)
        self.assertEqual(self.fm["description"], fixed)
        self.assertLessEqual(len(self.fm["description"]), 1024)
        self.assertNotRegex(self.fm["description"], r"[<>]")

    def test_version_mirrors_provenance(self):
        self.assertEqual(self.fm["metadata"]["devforgeai-version"], str(self.prov["version"]))
        self.assertEqual(self.fm["metadata"]["devforgeai-id"], self.prov["id"])

    def test_provenance(self):
        self.assertEqual(errors("skill.schema.json", {"frontmatter": self.prov}), [])
        self.assertEqual((self.prov["id"], self.prov["skill_name"], self.prov["eval_tag"]),
                         (SKL, "precompact", "precompact"))
        self.assertIn({"id": "SPEC-015", "relation": "implements", "version": SPEC_VERSION, "hash": None},
                      self.prov["upstream"])
        # Approved by Bryan on 2026-10-05, after the 1-run suite (12 of 12 at 1.00) and the live VER-07.
        self.assertEqual((self.prov["status"], self.prov["approved_by"], self.prov["approved_on"]),
                         ("approved", "Bryan", "2026-10-05"))

    def test_every_file_skill_md_names_exists(self):
        named = set(re.findall(r"\b((?:references|assets|scripts)/[\w.-]+)", self.text))
        named |= {t for t in re.findall(r"\]\(([^)#\s]+)\)", self.text) if "://" not in t}
        self.assertTrue(named)
        for target in sorted(named):
            with self.subTest(target):
                self.assertTrue((SKILL / target).exists(), target)
        for name in ("references/handoff-rules.md", "references/memory.md", "assets/start-here.md",
                     "assets/tasks.md", "assets/resume-prompt.md"):
            self.assertIn(name, self.text)

    def test_skill_folder_holds_what_spec_015_lists(self):
        self.assertEqual(sorted(p.name for p in SKILL.iterdir()),
                         ["SKILL.md", "assets", "provenance.yaml", "references", "scripts"])
        self.assertEqual(sorted(p.name for p in (SKILL / "references").iterdir()), ["handoff-rules.md", "memory.md"])
        self.assertEqual(sorted(p.name for p in (SKILL / "assets").iterdir()),
                         ["resume-prompt.md", "start-here.md", "tasks.md"])
        self.assertEqual(sorted(p.name for p in (SKILL / "scripts").iterdir()), ["check_handoff.py"])

    def test_skill_md_runs_the_bundled_script(self):
        self.assertIn("python3 ${CLAUDE_SKILL_DIR}/scripts/check_handoff.py --root", self.text)

    def test_the_skill_asks_nothing(self):
        self.assertNotIn("AskUserQuestion", self.text)
        self.assertRegex(self.text, r"(?i)ask the user nothing")


class Assets(unittest.TestCase):
    def headings(self, name):
        text = (SKILL / "assets" / name).read_text()
        return [l.rstrip() for l in text.splitlines() if re.match(r"^##(?!#)\s", l)]

    def test_start_here_headings(self):
        self.assertEqual(self.headings("start-here.md"), START_HEADINGS)
        text = (SKILL / "assets/start-here.md").read_text()
        self.assertIn("### Decided", text)
        self.assertIn("### Open", text)

    def test_tasks_headings(self):
        self.assertEqual(self.headings("tasks.md"), TASKS_HEADINGS)

    def test_resume_prompt_has_no_required_headings_and_fits(self):
        text = (SKILL / "assets/resume-prompt.md").read_text()
        self.assertLessEqual(len(text.splitlines()), 20)
        self.assertIn("START-HERE", text)

    def test_only_fill_placeholders_never_in_backticks(self):
        for name in ("start-here.md", "tasks.md", "resume-prompt.md"):
            with self.subTest(name):
                text = (SKILL / "assets" / name).read_text()
                self.assertIn("[[fill: ", text)
                self.assertNotRegex(text, r"\bTODO\b|\bTBD\b")
                self.assertNotRegex(without_code(text), r"<[^>\n]+>")
                for span in re.findall(r"(`+)(.+?)\1", text):
                    self.assertNotIn("[[fill:", span[1])


class Rules(unittest.TestCase):
    def test_handoff_rules_hold_every_self_check_item(self):
        rules = squash((SKILL / "references/handoff-rules.md").read_text())
        items = self_check_items()
        self.assertEqual(len(items), 9)
        for item in items:
            with self.subTest(item[:40]):
                self.assertIn(squash(item), rules)

    def test_error_handling_is_stated(self):
        text = squash(" ".join(skill_texts().values()))
        for item, phrase in [("ERR-02", "give the files' content in the reply"),
                             ("ERR-03", "read the files back against the whole self-check"),
                             ("ERR-05", "as not continued here"),
                             ("ERR-06", "START-HERE.md is written first")]:
            with self.subTest(item):
                self.assertIn(phrase, text)

    def test_generic_no_machine_paths_or_names(self):
        for name, text in skill_texts().items():
            with self.subTest(name):
                self.assertNotRegex(text, r"(?<![\w.~$}])/(home|Users|tmp|mnt|root|var|opt)/")
                self.assertNotRegex(text, r"\b[A-Z]:\\")
                self.assertNotRegex(text, r"(?i)\b(bryan|cmux|worker1|devforgeai-worker)\b")


class Claude(unittest.TestCase):
    def test_skill_table_row(self):
        self.assertRegex((ROOT / "CLAUDE.md").read_text(), r"\n\| `precompact` \| SKL-012[^|]*\| SPEC-015 v\d")


class Spec(unittest.TestCase):
    def test_spec_validates_and_every_item_is_covered(self):
        doc = spec_document(spec_text())
        self.assertEqual(errors("spec.schema.json", doc), [])
        # Version 2 (the description without <branch>, found by this test) approved by Bryan on 2026-10-05.
        self.assertEqual((doc["frontmatter"]["version"], doc["frontmatter"]["status"]), (SPEC_VERSION, "approved"))
        covered = {c for v in doc["verifications"] for c in v.get("covers", [])}
        for key in ("behaviors", "errors", "quality_responses"):
            for item in doc[key]:
                with self.subTest(item["id"]):
                    self.assertIn(item["id"], covered)
        self.assertIn("IF-01", covered)


if __name__ == "__main__":
    unittest.main()
