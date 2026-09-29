"""Unit tests for the shared policy validation script (SPEC-002 §5 and BEH-17 R1, D-09; SPEC-003 BEH-03).

The script ships byte-identical in skills/prd/ and skills/architecture/ (test_shared_files.py checks
that), so these tests run the prd copy. Each case writes its own policy documents, independent of the
eval fixtures, and runs the script as a subprocess: once with this interpreter's packages, and once
with a throwaway HOME, which hides user-site packages the way the eval harness does (on this machine
that switches jsonschema 4.26 for the system's 4.10, which has no `referencing` module).

Run from the repository root:
    python3 -B src/tests/prd/test_validate_policy.py
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "src/claude/DevForgeAI/skills/prd/scripts/validate_policy.py"
LINE = re.compile(r"^(?P<file>\S+): (?P<part>[^:]+): (?P<field>[^:]+): (?P<message>.+) "
                  r"\((?P<rule>schema|calendar check|SV-0[1-6])\)$")

ORG = """\
---
id: POL-001
type: policy
title: "Northwind engineering policy (vendored)"
status: approved
version: 2
created: 2026-05-04
updated: 2026-08-17
owner: "Northwind platform council"
authors: ["Northwind platform council"]
reviewed_by: ["Northwind platform council"]
approved_by: "Northwind CTO"
approved_on: 2026-08-17
upstream:
  - {id: ADR-210, relation: constrains, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- policy-specific ---
scope: organization
source: {repository: "git.northwind.example/policy", ref: "v2.1.0"}
---

# POL-001 — Northwind engineering policy (vendored)

## 1. Scope and ownership

Every Northwind product.

## 2. Settings

```yaml items
settings:
  - id: SET-01
    status: active
    key: interview.max_calls
    class: interaction_default
    value: 6
    overridable_by:
      - project
      - local
    rationale: "Short interviews"
  - id: SET-02
    status: active
    key: architecture.mandated_platforms
    class: organizational_policy
    value:
      capability: "Message queue"
      platform: "Northwind Bus"
      source: "ADR-210"
    overridable_by: []
    rationale: "One broker"
  - id: SET-03
    status: active
    key: quality.required_categories
    class: organizational_policy
    value:
      - observability
    applies_when:
      operating_context:
        - pilot
        - production
    overridable_by: []
```

## Change Log

| Version | Date | Author | Change | Settings affected |
|---|---|---|---|---|
| 2 | 2026-08-17 | Platform council | Current | all |
"""

PROJECT = """\
---
id: POL-002
type: policy
title: "Ledger project policy"
status: approved
version: 1
created: 2026-09-02
updated: 2026-09-02
owner: "Ledger team"
authors: ["Ledger team"]
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
# --- policy-specific ---
scope: project
source: null
---

# POL-002 — Ledger project policy

```yaml items
settings:
  - id: SET-01
    status: active
    key: architecture.mandated_platforms
    class: organizational_policy
    value:
      capability: "Object storage"
      platform: "Ledger S3 bucket"
      source: "ADR-003"
    overridable_by: []
```
"""


def edit(text, old, new):
    assert text.count(old) == 1, f"anchor not unique: {old!r}"
    return text.replace(old, new)


SV_SETTING = """\
  - id: {sid}
    status: {status}
    key: {key}
    class: {cls}
    value: {value}
    overridable_by: []
"""


def add_setting(text, sid, key, value, status="active"):
    cls = "interaction_default" if key == "interview.max_calls" else "organizational_policy"
    block = SV_SETTING.format(sid=sid, status=status, key=key, cls=cls, value=value)
    return edit(text, "```\n\n## Change Log", block + "```\n\n## Change Log")


def platform(capability, name):
    return "\n" + "".join(f"      {k}: \"{v}\"\n" for k, v in
                          (("capability", capability), ("platform", name), ("source", "ADR-9"))).rstrip("\n")


class Base:
    """Runs every test; subclasses choose the environment."""

    ENV = {}

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.policy = self.tmp / "docs/specs/policy"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write(self, **docs):
        self.policy.mkdir(parents=True, exist_ok=True)
        for name, text in docs.items():
            (self.policy / f"{name.replace('_', '-')}.md").write_text(text)

    def run_script(self, folder="docs/specs/policy", script=SCRIPT, env=None):
        full = dict(os.environ, **self.ENV, **(env or {}))
        p = subprocess.run([sys.executable, "-B", str(script), folder], cwd=self.tmp, env=full,
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(p.stderr, "", p.stderr)
        return p.returncode, p.stdout.splitlines()

    def errors(self, lines):
        return [LINE.match(l).groupdict() for l in lines if LINE.match(l)]

    def assert_invalid(self, lines, code, *, file, part, field, rule, message=None):
        self.assertEqual(code, 1, lines)
        errs = self.errors(lines)
        hits = [e for e in errs if e["file"].endswith(file) and e["part"] == part and e["field"] == field
                and e["rule"] == rule and (message is None or re.search(message, e["message"]))]
        self.assertTrue(hits, f"no {part}: {field} ({rule}) error in:\n" + "\n".join(lines))
        self.assertTrue(lines[-1].startswith("INVALID:"), lines)
        return errs

    # --- Valid ---------------------------------------------------------------------------------

    def test_valid_organization_policy_passes(self):
        self.write(POL_001=ORG)
        code, lines = self.run_script()
        self.assertEqual((code, lines), (0, ["OK: 1 approved policy document(s) valid."]))

    def test_valid_organization_and_project_pass(self):
        self.write(POL_001=ORG, POL_002=PROJECT)
        code, lines = self.run_script()
        self.assertEqual((code, lines), (0, ["OK: 2 approved policy document(s) valid."]))

    def test_no_folder_means_defaults(self):
        code, lines = self.run_script()
        self.assertEqual(code, 0)
        self.assertIn("framework defaults apply", lines[-1])

    def test_empty_folder_means_defaults(self):
        self.policy.mkdir(parents=True)
        code, lines = self.run_script()
        self.assertEqual(code, 0)
        self.assertTrue(lines[-1].startswith("OK: no approved policy document"), lines)

    # --- Schema: the four named negative fixtures -------------------------------------------------

    # Calendar dates: additional semantic validation. The unchanged schema's date pattern accepts these
    # values, so the only error is the calendar check's, never a schema error.

    def test_malformed_date_is_rejected(self):
        self.write(POL_001=edit(ORG, "updated: 2026-08-17", "updated: 2026-13-45"))
        code, lines = self.run_script()
        errs = self.assert_invalid(lines, code, file="POL-001.md", part="frontmatter", field="updated",
                                   rule="calendar check", message="2026-13-45")
        self.assertEqual(len(errs), 1, lines)

    def test_malformed_approved_on_is_rejected(self):
        self.write(POL_001=edit(ORG, "approved_on: 2026-08-17", "approved_on: 2026-02-30"))
        code, lines = self.run_script()
        errs = self.assert_invalid(lines, code, file="POL-001.md", part="frontmatter", field="approved_on",
                                   rule="calendar check")
        self.assertEqual(len(errs), 1, lines)

    def test_february_29_in_a_common_year_is_rejected(self):
        self.write(POL_001=edit(ORG, "created: 2026-05-04", "created: 2025-02-29"))
        code, lines = self.run_script()
        errs = self.assert_invalid(lines, code, file="POL-001.md", part="frontmatter", field="created",
                                   rule="calendar check", message="2025-02-29")
        self.assertEqual(len(errs), 1, lines)

    def test_day_zero_is_rejected(self):
        self.write(POL_001=edit(ORG, "updated: 2026-08-17", "updated: 2026-08-00"))
        code, lines = self.run_script()
        self.assert_invalid(lines, code, file="POL-001.md", part="frontmatter", field="updated", rule="calendar check")

    def test_valid_leap_days_pass(self):
        text = edit(ORG, "created: 2026-05-04", "created: 2024-02-29")
        text = edit(text, "updated: 2026-08-17", "updated: 2028-02-29")
        text = edit(text, "approved_on: 2026-08-17", "approved_on: 2028-02-29")
        self.write(POL_001=text)
        code, lines = self.run_script()
        self.assertEqual((code, lines), (0, ["OK: 1 approved policy document(s) valid."]))

    def test_null_approved_on_is_permitted(self):
        text = edit(ORG, 'approved_by: "Northwind CTO"\napproved_on: 2026-08-17', 'approved_by: ""\napproved_on: null')
        self.write(POL_001=text)
        code, lines = self.run_script()
        self.assertEqual((code, lines), (0, ["OK: 1 approved policy document(s) valid."]))

    def test_null_created_is_a_schema_error_not_a_calendar_one(self):
        self.write(POL_001=edit(ORG, "created: 2026-05-04", "created: null"))
        code, lines = self.run_script()
        errs = self.assert_invalid(lines, code, file="POL-001.md", part="frontmatter", field="created", rule="schema")
        self.assertNotIn("calendar check", {e["rule"] for e in errs}, lines)

    def test_date_not_matching_pattern_is_rejected(self):
        self.write(POL_001=edit(ORG, "created: 2026-05-04", "created: 2026-5-4"))
        code, lines = self.run_script()
        self.assert_invalid(lines, code, file="POL-001.md", part="frontmatter", field="created", rule="schema")

    def test_authors_as_string_is_rejected(self):
        self.write(POL_001=edit(ORG, 'authors: ["Northwind platform council"]', 'authors: "Northwind platform council"'))
        code, lines = self.run_script()
        errs = self.assert_invalid(lines, code, file="POL-001.md", part="frontmatter", field="authors",
                                   rule="schema", message="array")
        self.assertEqual(len(errs), 1, lines)

    def test_link_without_relation_is_rejected(self):
        self.write(POL_001=edit(ORG, "{id: ADR-210, relation: constrains, version: 1, hash: null}",
                                "{id: ADR-210, version: 1, hash: null}"))
        code, lines = self.run_script()
        errs = self.assert_invalid(lines, code, file="POL-001.md", part="frontmatter", field="upstream[0].relation",
                                   rule="schema", message="missing required field")
        self.assertEqual(len(errs), 1, lines)

    def test_link_on_a_setting_without_relation_is_rejected(self):
        self.write(POL_001=edit(ORG, '    rationale: "One broker"\n',
                                '    rationale: "One broker"\n    upstream:\n      - {id: ADR-210, version: 1, hash: null}\n'))
        code, lines = self.run_script()
        self.assert_invalid(lines, code, file="POL-001.md", part="SET-02 (architecture.mandated_platforms)",
                            field="upstream[0].relation", rule="schema")

    def test_max_calls_as_string_is_rejected(self):
        self.write(POL_001=edit(ORG, "    value: 6\n", '    value: "eight"\n'))
        code, lines = self.run_script()
        errs = self.assert_invalid(lines, code, file="POL-001.md", part="SET-01 (interview.max_calls)",
                                   field="value", rule="schema", message="integer")
        self.assertEqual(len(errs), 1, lines)

    # --- Schema: other rules the runtime checklist used to miss ------------------------------------

    def test_max_calls_out_of_range_is_rejected(self):
        self.write(POL_001=edit(ORG, "    value: 6\n", "    value: 21\n"))
        code, lines = self.run_script()
        self.assert_invalid(lines, code, file="POL-001.md", part="SET-01 (interview.max_calls)", field="value",
                            rule="schema", message="maximum")

    def test_unknown_frontmatter_key_is_rejected(self):
        self.write(POL_001=edit(ORG, "blocked_by: []\n", "blocked_by: []\nreviewers: []\n"))
        code, lines = self.run_script()
        self.assert_invalid(lines, code, file="POL-001.md", part="frontmatter", field="(whole)", rule="schema",
                            message="reviewers")

    def test_organization_without_source_is_rejected(self):
        self.write(POL_001=edit(ORG, 'source: {repository: "git.northwind.example/policy", ref: "v2.1.0"}',
                                "source: null"))
        code, lines = self.run_script()
        self.assert_invalid(lines, code, file="POL-001.md", part="frontmatter", field="source", rule="schema")

    def test_local_override_of_organizational_policy_is_rejected(self):
        self.write(POL_001=edit(ORG, "    overridable_by: []\n    rationale: \"One broker\"",
                                "    overridable_by:\n      - local\n    rationale: \"One broker\""))
        code, lines = self.run_script()
        self.assert_invalid(lines, code, file="POL-001.md", part="SET-02 (architecture.mandated_platforms)",
                            field="overridable_by[0]", rule="schema")

    def test_applies_when_on_unconditional_key_is_rejected(self):
        self.write(POL_001=edit(ORG, '    rationale: "Short interviews"\n',
                                '    rationale: "Short interviews"\n    applies_when:\n      operating_context:\n        - local\n'))
        code, lines = self.run_script()
        self.assert_invalid(lines, code, file="POL-001.md", part="SET-01 (interview.max_calls)", field="(whole)",
                            rule="schema", message="applies_when")

    def test_bad_document_id_link_is_rejected(self):
        self.write(POL_001=edit(ORG, "{id: ADR-210,", "{id: ADR-21,"))
        code, lines = self.run_script()
        self.assert_invalid(lines, code, file="POL-001.md", part="frontmatter", field="upstream[0].id", rule="schema")

    def test_yaml_syntax_error_is_rejected(self):
        self.write(POL_001=edit(ORG, "    value: 6\n", "    value: [6\n"))
        code, lines = self.run_script()
        self.assert_invalid(lines, code, file="POL-001.md", part="document", field="YAML", rule="schema")

    def test_every_error_is_reported(self):
        text = edit(ORG, "updated: 2026-08-17", "updated: 2026-13-45")
        text = edit(text, 'authors: ["Northwind platform council"]', 'authors: "Northwind platform council"')
        text = edit(text, "    value: 6\n", '    value: "eight"\n')
        self.write(POL_001=text)
        code, lines = self.run_script()
        self.assertEqual(code, 1)
        self.assertEqual({e["field"] for e in self.errors(lines)}, {"updated", "authors", "value"}, lines)
        self.assertEqual(lines[-1], "INVALID: 3 error(s) in 1 approved policy document(s).")

    # --- Semantic rules ---------------------------------------------------------------------------

    def test_sv01_duplicate_setting_id(self):
        self.write(POL_001=add_setting(ORG, "SET-02", "quality.required_categories", "[security]\n    applies_when:\n      operating_context: [production]"))
        code, lines = self.run_script()
        self.assert_invalid(lines, code, file="POL-001.md", part="SET-02", field="id", rule="SV-01")

    def test_sv02_two_approved_documents_in_one_scope(self):
        second = edit(edit(ORG, "id: POL-001", "id: POL-003"), "# POL-001", "# POL-003")
        self.write(POL_001=ORG, POL_003=second)
        code, lines = self.run_script()
        self.assert_invalid(lines, code, file="POL-003.md", part="frontmatter", field="scope", rule="SV-02",
                            message="POL-001.md")

    def test_sv02_ignores_a_draft_in_the_same_scope(self):
        draft = edit(edit(ORG, "id: POL-001", "id: POL-003"), "status: approved", "status: draft")
        self.write(POL_001=ORG, POL_003=draft)
        code, lines = self.run_script()
        self.assertEqual(code, 0, lines)

    def test_sv03_two_active_max_calls(self):
        self.write(POL_001=add_setting(ORG, "SET-04", "interview.max_calls", "10"))
        code, lines = self.run_script()
        self.assert_invalid(lines, code, file="POL-001.md", part="settings", field="key", rule="SV-03",
                            message="SET-01, SET-04")

    def test_sv03_counts_only_active_settings(self):
        self.write(POL_001=add_setting(ORG, "SET-04", "interview.max_calls", "10", status="deprecated"))
        code, lines = self.run_script()
        self.assertEqual(code, 0, lines)

    def test_sv04_two_mandates_for_one_capability_in_a_document(self):
        self.write(POL_001=add_setting(ORG, "SET-04", "architecture.mandated_platforms",
                                       platform("  message QUEUE ", "Other Bus")))
        code, lines = self.run_script()
        self.assert_invalid(lines, code, file="POL-001.md", part="settings", field="value.capability", rule="SV-04",
                            message="SET-02, SET-04")

    def test_sv04_forbidden_project_override(self):
        project = edit(edit(PROJECT, '"Object storage"', '"message queue"'), '"Ledger S3 bucket"', '"Ledger queue"')
        self.write(POL_001=ORG, POL_002=project)
        code, lines = self.run_script()
        self.assert_invalid(lines, code, file="POL-002.md", part="SET-01 (architecture.mandated_platforms)",
                            field="value.capability", rule="SV-04", message=r"POL-001\.md SET-02")

    def test_sv04_permitted_project_override(self):
        org = edit(ORG, '    overridable_by: []\n    rationale: "One broker"',
                   '    overridable_by:\n      - project\n    rationale: "One broker"')
        project = edit(PROJECT, '"Object storage"', '"Message queue"')
        self.write(POL_001=org, POL_002=project)
        code, lines = self.run_script()
        self.assertEqual(code, 0, lines)

    def test_sv05_deprecated_setting_is_reported_not_fatal(self):
        self.write(POL_001=edit(ORG, "  - id: SET-02\n    status: active", "  - id: SET-02\n    status: deprecated"))
        code, lines = self.run_script()
        self.assertEqual(code, 0, lines)
        self.assertIn("POL-001.md: SET-02 (architecture.mandated_platforms) is deprecated and takes no part (SV-05)",
                      "\n".join(lines))

    def test_sv05_deprecated_org_mandate_allows_a_project_mandate(self):
        org = edit(ORG, "  - id: SET-02\n    status: active", "  - id: SET-02\n    status: deprecated")
        project = edit(PROJECT, '"Object storage"', '"Message queue"')
        self.write(POL_001=org, POL_002=project)
        code, lines = self.run_script()
        self.assertEqual(code, 0, lines)

    def test_sv06_draft_document_is_ignored_even_when_invalid(self):
        draft = edit(edit(ORG, "status: approved", "status: draft"), "updated: 2026-08-17", "updated: 2026-13-45")
        self.write(POL_001=draft)
        code, lines = self.run_script()
        self.assertEqual(code, 0, lines)
        self.assertEqual(lines[0], "ignored docs/specs/policy/POL-001.md (status draft) (SV-06)")

    def test_sv06_in_review_document_is_ignored_next_to_an_approved_one(self):
        review = edit(PROJECT, "status: approved", "status: in-review")
        self.write(POL_001=ORG, POL_002=review)
        code, lines = self.run_script()
        self.assertEqual(code, 0, lines)
        self.assertIn("ignored docs/specs/policy/POL-002.md (status in-review) (SV-06)", lines)

    # --- Can't run --------------------------------------------------------------------------------

    def shim(self, module):
        d = self.tmp / f"shim-{module}"
        d.mkdir()
        (d / f"{module}.py").write_text(f"raise ImportError('simulated: no {module}', name='{module}')\n")
        return {"PYTHONPATH": str(d)}

    def test_missing_jsonschema_exits_2(self):
        self.write(POL_001=ORG)
        code, lines = self.run_script(env=self.shim("jsonschema"))
        self.assertEqual(code, 2, lines)
        self.assertIn("jsonschema", lines[-1])
        self.assertTrue(lines[-1].startswith("Cannot run:"), lines)

    def test_missing_pyyaml_exits_2(self):
        self.write(POL_001=ORG)
        code, lines = self.run_script(env=self.shim("yaml"))
        self.assertEqual(code, 2, lines)

    def test_missing_jsonschema_without_approved_policy_is_not_an_error(self):
        self.write(POL_001=edit(ORG, "status: approved", "status: draft"))
        code, lines = self.run_script(env=self.shim("jsonschema"))
        self.assertEqual(code, 0, lines)

    def test_missing_schema_copy_exits_2(self):
        copy = self.tmp / "skill/scripts/validate_policy.py"
        copy.parent.mkdir(parents=True)
        shutil.copy(SCRIPT, copy)
        self.write(POL_001=ORG)
        code, lines = self.run_script(script=copy)
        self.assertEqual(code, 2, lines)
        self.assertIn("schema copy unreadable", lines[-1])

    def test_folder_that_is_a_file_exits_2(self):
        (self.tmp / "notadir").write_text("x")
        code, lines = self.run_script(folder="notadir")
        self.assertEqual(code, 2, lines)

    def test_writes_nothing(self):
        self.write(POL_001=ORG)
        before = sorted(p.relative_to(self.tmp) for p in self.tmp.rglob("*"))
        self.run_script()
        self.assertEqual(before, sorted(p.relative_to(self.tmp) for p in self.tmp.rglob("*")))


class ThisInterpreter(Base, unittest.TestCase):
    ENV = {}


def _system_home_works():
    home = tempfile.mkdtemp()
    try:
        p = subprocess.run([sys.executable, "-c", "import yaml, jsonschema"], env=dict(os.environ, HOME=home),
                           capture_output=True)
        return p.returncode == 0, home
    finally:
        shutil.rmtree(home, ignore_errors=True)


_OK, _HOME = _system_home_works()


@unittest.skipUnless(_OK, "no yaml and jsonschema outside the user site-packages")
class WithoutUserSite(Base, unittest.TestCase):
    """As the eval harness runs it: HOME points elsewhere, so user-site packages are hidden."""

    ENV = {"HOME": _HOME}

    def setUp(self):
        super().setUp()
        Path(_HOME).mkdir(exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(_HOME, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
