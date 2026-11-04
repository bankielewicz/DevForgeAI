"""Structural checks for SPEC-019, the dev-guard's requirements (EVAL.md W2): the document validates against
spec.schema.json, its frontmatter version and status are the pinned ones, every BEH, ERR and QR item is covered by a
VER item, every JSON block parses, and the initial guard.json example fits DM-02 with patterns that compile. Self-contained: it imports nothing from the other test folders, since pytest
runs this tree in importlib mode. Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider src/tests/process
"""
import json
import re
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[3]
SCHEMAS = ROOT / "src/schemas"
SPEC = ROOT / "docs/specs/spec/SPEC-019.md"
# SPEC-019 v1 approved by Bryan on 2026-11-02 ("Approve as drafted (Recommended)"); v2 the same day, the close
# review's fixes ("Version 2 in this PR (Recommended)").
# v3 (2026-11-04): deprecated, the dev-guard cancelled unbuilt ("Cancel the dev-guard --> we are going in a different direction").
PIN = (3, "deprecated")


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


def spec_document(text):
    doc = {"frontmatter": yaml.load(re.match(r"---\n(.*?)\n---\n", text, re.S).group(1), Loader=_Loader)}
    for block in re.findall(r"```yaml items\n(.*?)```", text, re.S):
        for key, value in yaml.load(block, Loader=_Loader).items():
            doc.setdefault(key, []).extend(value)
    return doc


class Spec019(unittest.TestCase):
    def test_validates_pinned_and_every_item_is_verified(self):
        text = SPEC.read_text()
        doc = spec_document(text)
        self.assertEqual(errors("spec.schema.json", doc), [])
        self.assertEqual((doc["frontmatter"]["version"], doc["frontmatter"]["status"]), PIN)
        ids = {i["id"] for k in ("behaviors", "errors", "quality_responses") for i in doc[k]}
        covered = {c for v in doc["verifications"] for c in v["covers"]}
        self.assertEqual(ids - covered, set(), "an item no VER item covers")
        self.assertEqual(covered - ids, set(), "a VER item covers an unknown item")
        blocks = [json.loads(b) for b in re.findall(r"```json\n(.*?)```", text, re.S)]
        schemas = {b["x-item-id"]: b for b in blocks if "x-item-id" in b}
        self.assertEqual(set(schemas), {"DM-01", "DM-02", "DM-03"})
        examples = [b for b in blocks if "x-item-id" not in b]
        self.assertEqual(len(examples), 1, "one example block: the initial guard.json")
        guard = examples[0]
        dm02 = Draft202012Validator(schemas["DM-02"], format_checker=FormatChecker())
        self.assertEqual([e.message for e in dm02.iter_errors(guard)], [], "the initial guard.json fits DM-02")
        for entry in guard["allow"]:
            expanded = entry["pattern"]
            for name in ("P", "F", "V", "Q"):
                expanded = re.sub(rf"(?<![A-Za-z]){name}(?![A-Za-z])", "x", expanded)
            re.compile(expanded)
            for flag in entry["flags"]:
                re.compile(flag)


if __name__ == "__main__":
    unittest.main()
