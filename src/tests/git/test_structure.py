"""SPEC-007 VER-30: the git skill's structure. Run from the repository root, under your normal HOME
(jsonschema's `referencing` module is in the user site-packages):

    python3 -B src/tests/git/test_structure.py

- SKILL.md's frontmatter and provenance.yaml validate, and their IDs and versions agree with each
  other and with SPEC-007's version;
- every relative link and every ${CLAUDE_SKILL_DIR} path resolves; SKILL.md has at most 500 lines;
- every ERR code the skill names is one of SPEC-007's, and each of SPEC-007's appears in a reference;
- the never-run list (BEH-17) is complete in SKILL.md and repeated in no reference;
- SPEC-007 validates against spec.schema.json with every BEH, ERR and QR item covered, and every e2e
  VER item has an eval case tagged git and ver-NN that carries the safety grader (QR-03).
"""
import json
import re
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "src/claude/DevForgeAI/skills/git"
EVALS = ROOT / "src/claude/DevForgeAI/evals/git"
SPEC = ROOT / "docs/specs/spec/SPEC-007.md"
SCHEMAS = ROOT / "src/schemas"
REFERENCES = sorted((SKILL / "references").glob("*.md"))

# BEH-17's never-run list: each item, and a pattern that finds it in SKILL.md's list.
NEVER_RUN = {
    "push --force or -f": r"--force`? or `-f",
    "+<refspec> push": r"\+<refspec>",
    "forced push to the default branch": r"forced push to the default branch",
    "gh pr merge --admin": r"--admin",
    "gh pr merge --auto": r"--auto",
    "gh pr merge --delete-branch": r"--delete-branch",
    "QA label or verdict": r"QA label[\s\S]*QA verdict",
    "--no-verify": r"--no-verify",
    "--no-gpg-sign": r"--no-gpg-sign",
    "-c override of hooks or signing": r"`-c` override of hooks or signing",
    "filter-branch, filter-repo": r"filter-branch[\s\S]*filter-repo",
    "worktree remove --force": r"worktree remove --force",
    "rm on a worktree": r"`rm` on a worktree",
    "git configuration outside the repository": r"--global",
    "sandbox or permission settings": r"sandbox or permission settings",
    "bulk staging": r"git add -A`?, `git add \.`?, `git add -u`? or `git commit -a",
    "git pull without --ff-only": r"git pull` without `--ff-only",
}


class _Loader(yaml.SafeLoader):
    pass


_Loader.yaml_implicit_resolvers = {k: [r for r in v if r[0] != "tag:yaml.org,2002:timestamp"]
                                   for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()}


def errors(schema, instance):
    reg = Registry()
    for p in SCHEMAS.glob("*.json"):
        s = json.loads(p.read_text())
        reg = reg.with_resource(s["$id"], Resource.from_contents(s)).with_resource(p.name, Resource.from_contents(s))
    v = Draft202012Validator(json.loads((SCHEMAS / schema).read_text()), registry=reg, format_checker=FormatChecker())
    return [f"{list(e.path)}: {e.message}" for e in v.iter_errors(instance)]


def frontmatter(text):
    return yaml.load(re.match(r"---\n(.*?)\n---\n", text, re.S).group(1), Loader=_Loader)


def spec_document():
    text = SPEC.read_text()
    doc = {"frontmatter": frontmatter(text)}
    for block in re.findall(r"```yaml items\n(.*?)```", text, re.S):
        for key, value in yaml.load(block, Loader=_Loader).items():
            doc.setdefault(key, []).extend(value)
    return doc


def never_run_section(text):
    """SKILL.md's paragraph that starts with **Never run these at all:**."""
    m = re.search(r"\*\*Never run these at all:\*\*(.*?)(?:\n\n|\Z)", text, re.S)
    return " ".join(m.group(1).split()) if m else ""   # one line, so wrapped phrases still match


class Structure(unittest.TestCase):
    def setUp(self):
        self.skill_md = (SKILL / "SKILL.md").read_text()
        self.spec = spec_document()

    def test_versions_agree(self):
        fm = frontmatter(self.skill_md)
        self.assertEqual(errors("skill-frontmatter.schema.json", fm), [])
        self.assertEqual(fm["name"], "git")
        prov = yaml.load((SKILL / "provenance.yaml").read_text(), Loader=_Loader)
        self.assertEqual(errors("skill.schema.json", {"frontmatter": prov}), [])
        self.assertEqual((prov["id"], prov["skill_name"]), ("SKL-006", "git"))
        self.assertEqual(fm["metadata"], {"devforgeai-id": prov["id"], "devforgeai-version": str(prov["version"])})
        implements = [u for u in prov["upstream"] if u["id"] == "SPEC-007" and u["relation"] == "implements"]
        self.assertEqual([u["version"] for u in implements], [self.spec["frontmatter"]["version"]])

    def test_length_and_links(self):
        self.assertLessEqual(len(self.skill_md.splitlines()), 500)
        for path in [SKILL / "SKILL.md", *REFERENCES]:
            text = path.read_text()
            for link in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", text):
                if not re.match(r"[a-z]+:", link):
                    self.assertTrue((path.parent / link).is_file(), f"{path.name}: {link}")
            for rel in re.findall(r"\$\{CLAUDE_SKILL_DIR\}/([\w./-]+)", text):
                self.assertTrue((SKILL / rel).exists(), f"{path.name}: {rel}")

    def test_err_codes_are_defined(self):
        defined = {e["id"] for e in self.spec["errors"]}
        used = set()
        for path in [SKILL / "SKILL.md", *REFERENCES]:
            used |= set(re.findall(r"\bERR-\d{2}\b", path.read_text()))
        self.assertEqual(used - defined, set(), "codes the skill names but SPEC-007 doesn't define")
        in_refs = set()
        for path in REFERENCES:
            in_refs |= set(re.findall(r"\bERR-\d{2}\b", path.read_text()))
        self.assertEqual(defined - in_refs, set(), "SPEC-007 codes no reference handles")

    def test_never_run_list_only_in_skill_md(self):
        section = never_run_section(self.skill_md)
        self.assertTrue(section, "SKILL.md has no **Never run these at all:** list")
        missing = [item for item, pattern in NEVER_RUN.items() if not re.search(pattern, section)]
        self.assertEqual(missing, [], "items of BEH-17's never-run list missing from SKILL.md")
        for path in REFERENCES:
            text = path.read_text()
            self.assertNotRegex(text, r"(?i)never run (?:these )?at all", f"{path.name} repeats the list")
            self.assertNotRegex(text, r"filter-(?:branch|repo)", f"{path.name} repeats list-only items")

    def test_spec_validates_and_every_item_is_verified(self):
        self.assertEqual(errors("spec.schema.json", self.spec), [])
        ids = {i["id"] for k in ("behaviors", "errors", "quality_responses") for i in self.spec[k]}
        covered = {c for v in self.spec["verifications"] for c in v["covers"]}
        self.assertEqual(ids - covered, set())

    def test_every_e2e_item_has_a_case_with_the_safety_grader(self):
        tagged = {}
        for prompt in EVALS.glob("*/prompt.md"):
            tags = frontmatter(prompt.read_text())["tags"]
            self.assertIn("git", tags, prompt.parent.name)
            for t in tags:
                if t.startswith("ver-"):
                    tagged.setdefault("VER-" + t[4:], []).append(prompt.parent)
        for v in self.spec["verifications"]:
            if v["level"] != "e2e":
                continue
            with self.subTest(v["id"]):
                cases = tagged.get(v["id"], [])
                self.assertEqual(len(cases), 1, f"{v['id']} needs exactly one eval case")
                self.assertTrue((cases[0] / "graders" / "safety.md").is_file(), cases[0].name)
                self.assertIn(f"Eval case {cases[0].name}.", v["obligation"])


if __name__ == "__main__":
    unittest.main()
