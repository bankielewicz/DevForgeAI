"""Unit tests for the context skill's scripts/context_check.py (SPEC-011 §5, BEH-17, BEH-18, ERR-08, ERR-13;
VER-27).

Each test builds a project in a temporary folder from the example set
(src/staging/examples/context-cli-service-rdbms/docs/specs/) and runs the script there as a subprocess:
once with this interpreter's packages (jsonschema 4.26 with referencing), and once with a throwaway HOME,
which hides the user-site packages the way the eval harness does (on this machine, jsonschema 4.10 with no
referencing module).

Run from the repository root:
    python3 -B src/tests/context/test_context_check.py
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "src/claude/DevForgeAI/skills/context"
SCRIPT = SKILL / "scripts/context_check.py"
EXAMPLE = ROOT / "src/staging/examples/context-cli-service-rdbms/docs/specs"
CTX = "docs/specs/context"
AMB = "docs/specs/ambiguities/AMB-001.md"
RULES = "schema|statement|approval|items|size|detail|ambiguities"
LINE = re.compile(r"^(?P<file>\S+): (?P<part>[^:]+): (?P<field>[^:]+): (?P<message>.+) \((?P<rule>" + RULES + r")\)$")
UNCHANGED = re.compile(r"^(?P<file>\S+): unchanged, invalid: (?P<error>.+) \(ERR-10\)$")


def edit(text, old, new, count=1):
    assert text.count(old) == count, f"expected {count} of {old!r}"
    return text.replace(old, new)


class Base:
    """Runs every test; subclasses choose the environment."""

    ENV = {}
    REFERENCING = True

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.project = self.tmp / "project"
        self.temp = self.tmp / "systemp"  # TMPDIR for snapshot new
        self.temp.mkdir()
        shutil.copytree(EXAMPLE / "context", self.project / CTX)
        shutil.copytree(EXAMPLE / "ambiguities", self.project / "docs/specs/ambiguities")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def path(self, rel):
        return self.project / (rel if "/" in rel else f"{CTX}/{rel}.md")

    def read(self, rel):
        return self.path(rel).read_text()

    def write(self, rel, text):
        p = self.path(rel)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)

    def change(self, rel, old, new, count=1):
        self.write(rel, edit(self.read(rel), old, new, count))

    def run_script(self, *args, script=SCRIPT, env=None):
        full = dict(os.environ, TMPDIR=str(self.temp), **self.ENV, **(env or {}))
        p = subprocess.run([sys.executable, "-B", str(script), *args], cwd=self.project, env=full,
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(p.stderr, "", p.stderr)
        return p.returncode, p.stdout.splitlines()

    def check(self, *args):
        return self.run_script("check", *args)

    def errors(self, lines):
        return [LINE.match(l).groupdict() for l in lines if LINE.match(l)]

    def assert_ok(self, code, lines):
        self.assertEqual(code, 0, "\n".join(lines))
        self.assertTrue(lines and lines[-1].startswith("OK: "), lines)
        self.assertEqual(self.errors(lines), [], lines)

    def assert_error(self, code, lines, *, file, part, field, rule, message=None):
        self.assertEqual(code, 1, "\n".join(lines))
        hits = [e for e in self.errors(lines) if e["file"] == (file if "/" in file else f"{CTX}/{file}.md")
                and re.fullmatch(part, e["part"]) and e["field"] == field and e["rule"] == rule
                and (message is None or re.search(message, e["message"]))]
        self.assertTrue(hits, f"no {file}: {part}: {field} ({rule}) error in:\n" + "\n".join(lines))
        self.assertTrue(lines[-1].startswith("INVALID: "), lines)
        self.assertRegex(lines[-1], r"^INVALID: \d+ error\(s\) in \d+ file\(s\)$")

    def snapshot(self, folder=None):
        code, lines = self.run_script("snapshot", folder or "new")
        self.assertEqual(code, 0, lines)
        m = re.fullmatch(r"snapshot: (\d+) files in (.+)", lines[-1])
        self.assertTrue(m, lines)
        return Path(m.group(2))

    # --- The environment ------------------------------------------------------------------------

    def test_runs_with_the_expected_jsonschema(self):
        full = dict(os.environ, **self.ENV)
        p = subprocess.run([sys.executable, "-c", "import importlib.util as u; print(bool(u.find_spec('referencing')))"],
                           env=full, capture_output=True, text=True)
        self.assertEqual(p.stdout.strip(), str(self.REFERENCING))

    # --- check: passing ------------------------------------------------------------------------

    def test_check_passes_on_the_example_set(self):
        code, lines = self.check()
        self.assert_ok(code, lines)
        self.assertEqual(lines[-1], "OK: 11 files checked")  # nine documents, one detail file, AMB-001

    def test_check_passes_with_no_context_folder(self):
        shutil.rmtree(self.project / CTX)
        code, lines = self.check()
        self.assert_ok(code, lines)
        self.assertEqual(lines[-1], "OK: 1 files checked")

    def test_check_passes_on_a_correct_runs_documents(self):
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        try:
            import golden
        except ImportError as exc:  # golden imports make_evals, which needs referencing
            self.skipTest(f"golden.py can't load here: {exc}")
        shutil.rmtree(self.project / CTX)
        for case in ({}, {"confirmed": False, "observed": True}, {"reminder": True}, {"policy": True},
                     {"kinds_missing": True}, {"approve": True}):
            with self.subTest(**case):
                files, _ = golden.shared_set(**case)
                for path, text in files.items():
                    self.write(path, text)
                code, lines = self.check()
                self.assert_ok(code, lines)
                shutil.rmtree(self.project / CTX)

    def test_check_writes_nothing(self):
        before = sorted(p.relative_to(self.tmp) for p in self.tmp.rglob("*"))
        self.check()
        self.assertEqual(before, sorted(p.relative_to(self.tmp) for p in self.tmp.rglob("*")))

    def test_other_paths_are_not_read(self):
        self.write("notes", "--- not yaml\n\x00 [NEEDS ADR: x]\n")
        self.write(f"{CTX}/rdbms/unlinked.md", "no parent line\n")
        code, lines = self.check()
        self.assert_ok(code, lines)

    # --- schema ---------------------------------------------------------------------------------

    def test_schema_status_not_in_the_lifecycle(self):
        self.change("front-end", "status: approved", "status: in-review")
        code, lines = self.check()
        self.assert_error(code, lines, file="front-end", part="frontmatter", field="status", rule="schema",
                          message="in-review")

    def test_schema_impossible_date(self):
        self.change("testing", "updated: 2026-09-29", "updated: 2026-13-45")
        code, lines = self.check()
        self.assert_error(code, lines, file="testing", part="frontmatter", field="updated", rule="schema",
                          message="date")

    def test_schema_item_field(self):
        self.change("tech-stack", '    name: "Alembic"\n', "")
        code, lines = self.check()
        self.assert_error(code, lines, file="tech-stack", part=r"TEC-04", field="name", rule="schema",
                          message="missing required field")

    def test_schema_document_must_match_the_file_name(self):
        self.change("middle-tier", "document: middle-tier", "document: back-end")
        self.change("middle-tier", "id: CTX-012", "id: CTX-013")
        code, lines = self.check()
        self.assert_error(code, lines, file="middle-tier", part="frontmatter", field="document", rule="schema",
                          message="middle-tier")

    def test_schema_unparsable_yaml(self):
        self.change("rdbms", "status: approved", "status: [approved")
        code, lines = self.check()
        self.assert_error(code, lines, file="rdbms", part="document", field="YAML", rule="schema")

    def test_schema_ambiguity_log(self):
        self.change(AMB, "    state: open\n", "    state: maybe\n")
        code, lines = self.check()
        self.assert_error(code, lines, file=AMB, part="ENT-02", field="state", rule="schema")

    # --- statement ------------------------------------------------------------------------------

    def test_statement_decision_needs_its_constrains_link(self):
        self.change("rdbms", "  - {id: ADR-002, relation: constrains, version: 1, hash: null}\n", "")
        code, lines = self.check()
        self.assert_error(code, lines, file="rdbms", part=r"line \d+", field="Decision", rule="statement",
                          message="ADR-002")

    def test_statement_decision_link_must_be_constrains(self):
        self.change("rdbms", "{id: ADR-002, relation: constrains,", "{id: ADR-002, relation: informed_by,")
        code, lines = self.check()
        self.assert_error(code, lines, file="rdbms", part=r"line \d+", field="Decision", rule="statement")

    def test_statement_decision_with_an_item_source(self):
        self.change("architecture", "## 2. Error handling\n\n",
                    "## 2. Error handling\n\n- **Decision** (ARCH-001#CMP-02): the service owns the shift rules.\n")
        code, lines = self.check()
        self.assert_ok(code, lines)
        self.change("architecture", "  - {id: ARCH-001, item: CMP-02, relation: constrains, version: 1, hash: null}\n", "")
        code, lines = self.check()
        self.assert_error(code, lines, file="architecture", part=r"line \d+", field="Decision", rule="statement",
                          message="ARCH-001#CMP-02")

    def test_statement_decision_without_a_source(self):
        self.change("middle-tier", "- **Convention:** one transaction per service call",
                    "- **Decision**: one transaction per service call")
        code, lines = self.check()
        self.assert_error(code, lines, file="middle-tier", part=r"line \d+", field="Decision", rule="statement")

    def test_statement_observed_needs_a_path_and_a_date(self):
        self.change("front-end", "- **Convention:** the CLI holds no state",
                    "- **Observed** (src/shiftlog/cli/): the CLI holds no state")
        code, lines = self.check()
        self.assert_error(code, lines, file="front-end", part=r"line \d+", field="Observed", rule="statement")

    def test_statement_observed_with_its_path_and_date_passes(self):
        self.change("source-tree", "- **Convention:** `build/` is written by the build",
                    "- **Observed** (.gitignore, 2026-09-29): `build/` is written by the build")
        code, lines = self.check()
        self.assert_ok(code, lines)

    def test_statement_proposed_needs_a_marker(self):
        self.change("source-tree", "- **Convention:** `build/` is written by the build",
                    "- **Proposed:** `build/` is written by the build")
        code, lines = self.check()
        self.assert_error(code, lines, file="source-tree", part=r"line \d+", field="Proposed", rule="statement")

    def test_statement_proposed_marker_on_a_continuation_line_passes(self):
        self.change("source-tree", "- **Convention:** `build/` is written by the build and never edited or committed.",
                    "- **Proposed:** `build/` is written by the build and never edited or committed.\n"
                    "  [NEEDS CLARIFICATION: confirm build/]")
        code, lines = self.check()
        self.assert_ok(code, lines)

    def test_statement_devforgeai_rule_names_no_document_id(self):
        self.change("testing", "This is not a configurable threshold.", "This is not a configurable threshold (ADR-001).")
        code, lines = self.check()
        self.assert_error(code, lines, file="testing", part=r"line \d+", field="DevForgeAI rule", rule="statement",
                          message="ADR-001")

    def test_statement_basis_cell(self):
        self.change("testing", "| tests/db/ | Convention |", "| tests/db/ | Proposed |")
        code, lines = self.check()
        self.assert_error(code, lines, file="testing", part=r"line \d+", field="Basis", rule="statement")
        self.change("testing", "| tests/db/ | Proposed |", "| tests/db/ | Observed (tests/db/) |")
        code, lines = self.check()
        self.assert_error(code, lines, file="testing", part=r"line \d+", field="Basis", rule="statement")
        self.change("testing", "| tests/db/ | Observed (tests/db/) |", "| tests/db/ | ADR-002 |")
        code, lines = self.check()
        self.assert_error(code, lines, file="testing", part=r"line \d+", field="Basis", rule="statement",
                          message="ADR-002")

    def test_statement_policy_source_cell_needs_its_link(self):
        self.change("testing", "| testing.coverage_metric | line | (default) |",
                    "| testing.coverage_metric | branch | POL-001#SET-02 |")
        code, lines = self.check()
        self.assert_error(code, lines, file="testing", part=r"line \d+", field="Source", rule="statement",
                          message="POL-001#SET-02")
        self.change("testing", "upstream:\n", "upstream:\n  - {id: POL-001, item: SET-02, relation: constrains, "
                    "version: 1, hash: null}\n")
        code, lines = self.check()
        self.assert_ok(code, lines)

    def test_statement_in_a_detail_file_uses_the_parents_links(self):
        self.change(f"{CTX}/rdbms/migrations.md", "- **Convention:** one revision per story",
                    "- **Decision** (ADR-002): one revision per story")
        code, lines = self.check()
        self.assert_ok(code, lines)
        self.change("rdbms", "  - {id: ADR-002, relation: constrains, version: 1, hash: null}\n", "")
        code, lines = self.check()
        self.assert_error(code, lines, file=f"{CTX}/rdbms/migrations.md", part=r"line \d+", field="Decision",
                          rule="statement")

    def test_statements_in_code_blocks_and_comments_are_ignored(self):
        self.change("front-end", "## 2. Framework and structure\n\n",
                    "## 2. Framework and structure\n\n```text\n- **Proposed:** an example\n```\n\n"
                    "<!-- - **Decision** (ADR-009): an author note -->\n\n")
        code, lines = self.check()
        self.assert_ok(code, lines)

    # --- approval -------------------------------------------------------------------------------

    def test_approval_with_a_marker(self):
        self.change("front-end", "- **Convention:** the CLI holds no state between runs;",
                    "- **Convention:** [NEEDS CLARIFICATION: which state?] the CLI holds no state between runs;")
        code, lines = self.check()
        self.assert_error(code, lines, file="front-end", part=r"line \d+", field="status", rule="approval",
                          message="NEEDS CLARIFICATION")

    def test_approval_with_a_proposed_statement(self):
        self.change("front-end", "- **Convention:** the CLI holds no state between runs;",
                    "- **Proposed:** [NEEDS CLARIFICATION: confirm] the CLI holds no state between runs;")
        code, lines = self.check()
        self.assert_error(code, lines, file="front-end", part=r"line \d+", field="status", rule="approval",
                          message="Proposed")

    def test_approval_with_an_active_proposed_item(self):
        self.change("source-tree", "status: draft", "status: approved")
        self.change("source-tree", 'approved_by: ""\napproved_on: null', 'approved_by: "Example Owner"\napproved_on: 2026-09-30')
        code, lines = self.check()
        self.assert_error(code, lines, file="source-tree", part=r"SRC-10.*", field="status", rule="approval")

    def test_approval_with_a_marker_in_a_detail_file(self):
        self.change(f"{CTX}/rdbms/migrations.md", "- **Convention:** one revision per story",
                    "- **Proposed:** one revision per story [NEEDS CLARIFICATION: confirm]")
        code, lines = self.check()
        self.assert_error(code, lines, file="rdbms", part=r"rdbms/migrations\.md line \d+", field="status",
                          rule="approval")

    def test_draft_documents_may_hold_markers(self):
        self.change("front-end", "status: approved", "status: draft")
        self.change("front-end", 'approved_by: "Example Owner"\napproved_on: 2026-09-29', 'approved_by: ""\napproved_on: null')
        self.change("front-end", "- **Convention:** the CLI holds no state between runs;",
                    "- **Proposed:** the CLI holds no state between runs; [NEEDS CLARIFICATION: confirm state]")
        code, lines = self.check()
        self.assert_ok(code, lines)

    # --- items ----------------------------------------------------------------------------------

    def test_items_unique_ids(self):
        self.change("tech-stack", "  - id: TEC-04\n", "  - id: TEC-02\n")
        code, lines = self.check()
        self.assert_error(code, lines, file="tech-stack", part=r"TEC-02.*", field="id", rule="items")

    def test_items_deleted_since_the_snapshot(self):
        start = self.snapshot()
        text = self.read("source-tree")
        self.write("source-tree", re.sub(r"  - id: SRC-07\n(?:    [^\n]*\n)+", "", text))
        code, lines = self.check("--snapshot", str(start))
        self.assert_error(code, lines, file="source-tree", part=r"SRC-07.*", field="id", rule="items")

    def test_items_deprecated_since_the_snapshot_pass(self):
        start = self.snapshot()
        self.change("source-tree", '    path: "tests/db/"\n    holds: tests\n    component: "ARCH-001#CMP-03"\n'
                    '    basis: convention\n    notes: ""', '    path: "tests/db/"\n    holds: tests\n'
                    '    component: "ARCH-001#CMP-03"\n    basis: convention\n    notes: "Retired by the owner"')
        self.change("source-tree", '  - id: SRC-07\n    status: active', '  - id: SRC-07\n    status: deprecated')
        code, lines = self.check("--snapshot", str(start))
        self.assert_ok(code, lines)

    # --- size -----------------------------------------------------------------------------------

    def test_size_index_at_most_100_lines(self):
        text = self.read("index")
        self.write("index", text + "\n" * (101 - text.count("\n")))
        code, lines = self.check()
        self.assert_error(code, lines, file="index", part="document", field="lines", rule="size", message="100")

    def test_size_index_of_100_lines_passes(self):
        text = self.read("index")
        self.write("index", text + "\n" * (100 - text.count("\n")))
        code, lines = self.check()
        self.assert_ok(code, lines)

    def test_size_at_most_500_lines(self):
        text = self.read("rdbms")
        self.write("rdbms", edit(text, "## Change Log", "## Contents\n\n" + "- x\n" * 500 + "\n## Change Log"))
        code, lines = self.check()
        self.assert_error(code, lines, file="rdbms", part="document", field="lines", rule="size", message="500")

    def test_size_contents_past_100_lines(self):
        text = self.read("testing")
        self.write("testing", edit(text, "## Change Log", "- **Convention:** x\n" * 20 + "\n## Change Log"))
        code, lines = self.check()
        self.assert_error(code, lines, file="testing", part="document", field="lines", rule="size",
                          message="Contents")

    # --- detail ---------------------------------------------------------------------------------

    def test_detail_without_its_parent_line(self):
        self.change(f"{CTX}/rdbms/migrations.md", "> Part of CTX-015 (rdbms.md), version 1.", "> Part of rdbms.")
        code, lines = self.check()
        self.assert_error(code, lines, file=f"{CTX}/rdbms/migrations.md", part="document", field="parent line",
                          rule="detail")

    def test_detail_with_frontmatter(self):
        self.write(f"{CTX}/rdbms/migrations.md", "---\nid: CTX-099\n---\n" + self.read(f"{CTX}/rdbms/migrations.md"))
        code, lines = self.check()
        self.assert_error(code, lines, file=f"{CTX}/rdbms/migrations.md", part="document", field="frontmatter",
                          rule="detail")

    def test_detail_with_items(self):
        self.write(f"{CTX}/rdbms/migrations.md", self.read(f"{CTX}/rdbms/migrations.md")
                   + "\n```yaml items\nroots:\n  - id: SRC-99\n```\n")
        code, lines = self.check()
        self.assert_error(code, lines, file=f"{CTX}/rdbms/migrations.md", part="document", field="items",
                          rule="detail")

    def test_detail_linking_another_detail_file(self):
        self.write(f"{CTX}/rdbms/indexes.md", "> Part of CTX-015 (rdbms.md), version 1. A change here raises that "
                   "document's version.\n\n# Relational database: indexes\n\n- **Convention:** x\n")
        self.change("rdbms", "- **Convention:** an index is added only with the query that needs it, in the same revision.",
                    "- **Convention:** an index is added only with the query that needs it, in the same revision.\n"
                    "- [Indexes](rdbms/indexes.md): read when a story adds an index.")
        code, lines = self.check()
        self.assert_ok(code, lines)
        self.change(f"{CTX}/rdbms/migrations.md", "Back to [rdbms.md](../rdbms.md).",
                    "Back to [rdbms.md](../rdbms.md); see [indexes](indexes.md).")
        code, lines = self.check()
        self.assert_error(code, lines, file=f"{CTX}/rdbms/migrations.md", part=r"line \d+", field="link",
                          rule="detail")

    def test_detail_link_to_a_missing_file(self):
        self.change("rdbms", "[Migration rules](rdbms/migrations.md)", "[Migration rules](rdbms/migration.md)")
        code, lines = self.check()
        self.assert_error(code, lines, file="rdbms", part=r"line \d+", field="link", rule="detail",
                          message="rdbms/migration.md")

    def test_detail_two_levels_deep(self):
        self.write(f"{CTX}/rdbms/deep/more.md", self.read(f"{CTX}/rdbms/migrations.md"))
        self.change("rdbms", "[Migration rules](rdbms/migrations.md)", "[Migration rules](rdbms/deep/more.md)")
        code, lines = self.check()
        self.assert_error(code, lines, file="rdbms", part=r"line \d+", field="link", rule="detail",
                          message="one level")

    # --- ambiguities ----------------------------------------------------------------------------

    def test_ambiguities_resolution_may_change(self):
        start = self.snapshot()
        self.change(AMB, '    decided_on: 2026-09-29\n    resolution: ""',
                    '    decided_on: 2026-09-29\n    resolution: "folded into CTX-003 v2: already stated"')
        code, lines = self.check("--snapshot", str(start))
        self.assert_ok(code, lines)

    def test_ambiguities_other_fields_may_not(self):
        start = self.snapshot()
        self.change(AMB, "    state: open\n", "    state: accepted\n")
        code, lines = self.check("--snapshot", str(start))
        self.assert_error(code, lines, file=AMB, part="ENT-02", field="state", rule="ambiguities")

    def test_ambiguities_no_new_entry(self):
        start = self.snapshot()
        text = self.read(AMB)
        entry = re.search(r"  - id: ENT-02\n(?:    [^\n]*\n|      [^\n]*\n)+", text).group(0)
        self.write(AMB, edit(text, entry, entry + entry.replace("ENT-02", "ENT-03")))
        code, lines = self.check("--snapshot", str(start))
        self.assert_error(code, lines, file=AMB, part="ENT-03", field="id", rule="ambiguities")

    # --- --snapshot and ERR-10 ------------------------------------------------------------------

    def test_unchanged_invalid_file_is_reported_and_not_counted(self):
        self.change("front-end", "status: approved", "status: in-review")
        start = self.snapshot()
        code, lines = self.check("--snapshot", str(start))
        self.assertEqual(code, 0, lines)
        hits = [UNCHANGED.match(l) for l in lines if UNCHANGED.match(l)]
        self.assertEqual([h["file"] for h in hits], [f"{CTX}/front-end.md"], lines)
        self.assertIn("status", hits[0]["error"])
        self.assertEqual(self.errors(lines), [], lines)
        self.assertTrue(lines[-1].startswith("OK: "), lines)

    def test_changed_invalid_file_counts(self):
        self.change("front-end", "status: approved", "status: in-review")
        start = self.snapshot()
        self.change("front-end", "commands are verbs", "commands are short verbs")
        code, lines = self.check("--snapshot", str(start))
        self.assert_error(code, lines, file="front-end", part="frontmatter", field="status", rule="schema")

    def test_approval_of_a_parent_counts_although_its_detail_file_is_unchanged(self):
        self.change("rdbms", "status: approved", "status: draft")
        self.change("rdbms", 'approved_by: "Example Owner"\napproved_on: 2026-09-29', 'approved_by: ""\napproved_on: null')
        self.change(f"{CTX}/rdbms/migrations.md", "- **Convention:** one revision per story",
                    "- **Proposed:** one revision per story [NEEDS CLARIFICATION: confirm]")
        start = self.snapshot()
        self.change("rdbms", "status: draft", "status: approved")
        self.change("rdbms", 'approved_by: ""\napproved_on: null', 'approved_by: "Example Owner"\napproved_on: 2026-10-01')
        code, lines = self.check("--snapshot", str(start))
        self.assert_error(code, lines, file="rdbms", part=r"rdbms/migrations\.md line \d+", field="status",
                          rule="approval")

    def test_check_with_a_folder_that_is_not_a_snapshot_cannot_run(self):
        (self.tmp / "empty").mkdir()
        code, lines = self.check("--snapshot", str(self.tmp / "empty"))
        self.assertEqual(code, 2, lines)
        self.assertTrue(lines[-1].startswith("Cannot run: "), lines)

    # --- snapshot and restore -------------------------------------------------------------------

    def test_snapshot_new(self):
        start = self.snapshot()
        self.assertEqual(start.name, "start")
        self.assertEqual(start.parent.parent, self.temp)
        self.assertRegex(start.parent.name, r"^devforgeai-context-\d{8}T\d{6}-[0-9a-f]{8}$")
        manifest = (start / "MANIFEST.sha256").read_text().splitlines()
        self.assertEqual(len(manifest), 11)  # ten files under docs/specs/context/ and AMB-001
        for line in manifest:
            digest, rel = line.split("  ", 1)
            self.assertEqual(hashlib.sha256((start / rel).read_bytes()).hexdigest(), digest)
            self.assertEqual((start / rel).read_bytes(), (self.project / rel).read_bytes())
        listed = [l.split("  ", 1)[1] for l in manifest]
        self.assertIn(f"{CTX}/rdbms/migrations.md", listed)
        self.assertIn(AMB, listed)

    def test_snapshot_copies_every_regular_file_under_the_context_folder(self):
        self.write("notes", "stray\n")
        start = self.snapshot()
        self.assertTrue((start / CTX / "notes.md").is_file())

    def test_snapshot_with_no_context_folder(self):
        shutil.rmtree(self.project / CTX)
        code, lines = self.run_script("snapshot", "new")
        self.assertEqual(code, 0, lines)
        self.assertRegex(lines[-1], r"^snapshot: 1 files in ")

    def test_snapshot_into_a_named_folder_creates_parents(self):
        folder = self.tmp / "run/pre-approval"
        self.assertEqual(self.snapshot(str(folder)), folder)
        self.assertTrue((folder / "MANIFEST.sha256").is_file())

    def test_snapshot_into_an_existing_folder_exits_2(self):
        folder = self.tmp / "exists"
        folder.mkdir()
        code, lines = self.run_script("snapshot", str(folder))
        self.assertEqual(code, 2, lines)
        self.assertTrue(lines[-1].startswith("Cannot run: "), lines)
        self.assertEqual(list(folder.iterdir()), [])

    def test_snapshot_writes_nothing_in_the_project(self):
        before = sorted(p.relative_to(self.project) for p in self.project.rglob("*"))
        self.snapshot()
        self.assertEqual(before, sorted(p.relative_to(self.project) for p in self.project.rglob("*")))

    def test_restore_brings_a_changed_file_back_byte_for_byte(self):
        original = self.path("tech-stack").read_bytes()
        start = self.snapshot()
        self.write("tech-stack", "broken\n")
        code, lines = self.run_script("restore", str(start), f"{CTX}/tech-stack.md")
        self.assertEqual((code, lines), (0, [f"restored {CTX}/tech-stack.md"]))
        self.assertEqual(self.path("tech-stack").read_bytes(), original)

    def test_restore_a_deleted_file(self):
        original = self.path("rdbms").read_bytes()
        start = self.snapshot()
        self.path("rdbms").unlink()
        code, lines = self.run_script("restore", str(start), f"{CTX}/rdbms.md")
        self.assertEqual(code, 0, lines)
        self.assertEqual(self.path("rdbms").read_bytes(), original)

    def test_restore_of_an_altered_snapshot_copy_is_refused(self):
        start = self.snapshot()
        self.write("tech-stack", "changed in the run\n")
        (start / CTX / "tech-stack.md").write_text("altered snapshot copy\n")
        code, lines = self.run_script("restore", str(start), f"{CTX}/tech-stack.md")
        self.assertEqual(code, 1, lines)
        self.assertRegex(lines[0], rf"^NOT RESTORED {re.escape(CTX)}/tech-stack\.md: ")
        self.assertEqual(self.read("tech-stack"), "changed in the run\n")

    def test_restore_of_a_file_not_in_the_snapshot(self):
        start = self.snapshot()
        self.write("api", "new in the run\n")
        code, lines = self.run_script("restore", str(start), f"{CTX}/api.md", f"{CTX}/index.md")
        self.assertEqual(code, 1, lines)
        self.assertRegex(lines[0], rf"^NOT RESTORED {re.escape(CTX)}/api\.md: ")
        self.assertEqual(lines[1], f"restored {CTX}/index.md")
        self.assertEqual(self.read("api"), "new in the run\n")

    def test_restore_refuses_a_path_outside_the_snapshot(self):
        start = self.snapshot()
        code, lines = self.run_script("restore", str(start), "../escape.md")
        self.assertEqual(code, 1, lines)
        self.assertTrue(lines[0].startswith("NOT RESTORED ../escape.md: "), lines)

    def test_restore_from_a_folder_that_is_not_a_snapshot_cannot_run(self):
        (self.tmp / "empty").mkdir()
        code, lines = self.run_script("restore", str(self.tmp / "empty"), f"{CTX}/index.md")
        self.assertEqual(code, 2, lines)
        self.assertTrue(lines[-1].startswith("Cannot run: "), lines)

    # --- Cannot run (ERR-13) --------------------------------------------------------------------

    def shim(self, module):
        d = self.tmp / f"shim-{module}"
        d.mkdir(exist_ok=True)
        (d / f"{module}.py").write_text(f"raise ImportError('simulated: no {module}', name='{module}')\n")
        return {"PYTHONPATH": str(d)}

    def every_subcommand(self):
        start = self.snapshot()
        return [("snapshot", "new"), ("snapshot", str(self.tmp / "fresh")), ("check",),
                ("check", "--snapshot", str(start)), ("restore", str(start), f"{CTX}/index.md")]

    def assert_cannot_run(self, args, script=SCRIPT, env=None, says=None):
        code, lines = self.run_script(*args, script=script, env=env)
        self.assertEqual(code, 2, (args, lines))
        self.assertEqual(len(lines), 1, lines)
        self.assertRegex(lines[0], r"^Cannot run: .+\.$")
        if says:
            self.assertIn(says, lines[0])

    def test_missing_pyyaml_cannot_run(self):
        for args in self.every_subcommand():
            with self.subTest(args=args):
                self.assert_cannot_run(args, env=self.shim("yaml"), says="PyYAML")

    def test_missing_jsonschema_cannot_run(self):
        for args in self.every_subcommand():
            with self.subTest(args=args):
                self.assert_cannot_run(args, env=self.shim("jsonschema"), says="jsonschema")

    def test_missing_schema_copy_cannot_run(self):
        copy = self.tmp / "skill"
        shutil.copytree(SKILL / "scripts", copy / "scripts")
        shutil.copytree(SKILL / "references/schemas", copy / "references/schemas")
        script = copy / "scripts/context_check.py"
        for name in ("context", "ambiguities", "common", "policy"):
            target = copy / f"references/schemas/{name}.schema.json"
            target.rename(target.with_suffix(".off"))
            for args in self.every_subcommand():
                with self.subTest(schema=name, args=args):
                    self.assert_cannot_run(args, script=script, says=f"{name}.schema.json")
            target.with_suffix(".off").rename(target)

    def test_usage_errors_cannot_run(self):
        for args in [(), ("snapshot",), ("restore",), ("restore", str(self.tmp)), ("check", "--snapshot"),
                     ("frobnicate",)]:
            with self.subTest(args=args):
                self.assert_cannot_run(args)


class ThisInterpreter(Base, unittest.TestCase):
    ENV = {}
    REFERENCING = True


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
    REFERENCING = False

    def setUp(self):
        super().setUp()
        Path(_HOME).mkdir(exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(_HOME, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
