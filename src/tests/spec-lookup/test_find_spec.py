"""Unit tests for the spec-lookup skill's search script, scripts/find_spec.py (SPEC-014 VER-01).

Covers BEH-07, IF-01, ERR-01, ERR-03, ERR-04 and ERR-05. Each case builds its own docs/specs/ in a temporary
folder and runs the script as a subprocess twice: with this interpreter's packages and with `-S`, which hides every
site-packages directory. The output must be the same both ways, never end in a traceback, and leave the folder as
it was.

Readings this test pins where SPEC-014 leaves a choice (listed for Bryan in the plan's end-of-workflow notes):
- paths are printed relative to the root, so they start `docs/specs/`;
- an item ID's definitions come first, in path order, then every other line naming it, in path then line order;
- a hit line inside an item block carries that item's ID and status;
- a document with no frontmatter takes its status from its `**Status:**` line up to the first full stop;
- `superseded_by` adds ", superseded by <ID>" after the status;
- the coverage line counts files at the root of docs/specs/ but lists only its folders, and says "hits" for any
  count, as the spec's "1 more hits" does;
- an excerpt longer than 100 characters is cut to 99 and ends with "…".

Run from the repository root:
    python3 -B src/tests/spec-lookup/test_find_spec.py
"""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "src/claude/DevForgeAI/skills/spec-lookup/scripts/find_spec.py"

SPEC_001 = """\
---
id: SPEC-001
type: spec
title: "Exports"
status: approved       # draft | approved
version: 2
superseded_by: null
---

# SPEC-001 — Exports

Exports follow ADR-001.

```yaml items
behaviors:
  - id: BEH-01
    status: active
    rule: "Exports are CSV only; no other format is offered."
  - id: BEH-03
    status: deprecated
    rule: "Replaced by BEH-01: exports were once Excel too."
```

Imports are SPEC-002's: see SPEC-002 BEH-01.
"""

SPEC_002 = """\
---
id: SPEC-002
type: spec
title: "Imports"
status: draft
version: 1
---

```yaml items
behaviors:
  - id: BEH-01
    status: active
    rule: "Imports read CSV files exported by SPEC-001."
```
"""

SPEC_003 = """\
---
id: SPEC-003
type: spec
title: "Old exports"
status: superseded
version: 3
superseded_by: "SPEC-001"
---

Exports were Excel files.
"""

ADR_001 = """\
---
id: ADR-001
type: adr
title: "Export format"
status: accepted
version: 1
---

## Decision

Chosen option: CSV, as SPEC-001 BEH-01 states (also SPEC-001#BEH-01).
"""

NOTES = """\
# Notes

**Status:** proposal, not approved. Nothing here is built.

A dark Mode toggle was mentioned once.
"""

FIXTURE = {
    "docs/specs/spec/SPEC-001.md": SPEC_001,
    "docs/specs/spec/SPEC-002.md": SPEC_002,
    "docs/specs/spec/SPEC-003.md": SPEC_003,
    "docs/specs/adr/ADR-001.md": ADR_001,
    "docs/specs/notes.md": NOTES,
}
COVERAGE = "searched 5 files under docs/specs/ (adr, spec)"

S1 = "docs/specs/spec/SPEC-001.md"
S2 = "docs/specs/spec/SPEC-002.md"
A1 = "docs/specs/adr/ADR-001.md"
DEF_S1_BEH01 = f'{S1}:16  SPEC-001 v2 approved  BEH-01 active  "Exports are CSV only; no other format is offered."'
DEF_S2_BEH01 = f'{S2}:11  SPEC-002 v1 draft  BEH-01 active  "Imports read CSV files exported by SPEC-001."'
ADR_LINE = f'{A1}:11  ADR-001 v1 accepted  "Chosen option: CSV, as SPEC-001 BEH-01 states (also SPEC-001#BEH-01)."'
S1_LINE_24 = f'{S1}:24  SPEC-001 v2 approved  "Imports are SPEC-002\'s: see SPEC-002 BEH-01."'


def build(root, files):
    for rel, content in files.items():
        path = Path(root) / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")


def tree(root):
    return sorted(str(p.relative_to(root)) for p in Path(root).rglob("*"))


class FindSpec(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = self._tmp.name
        build(self.root, FIXTURE)

    def tearDown(self):
        self._tmp.cleanup()

    def run_script(self, *query, root=None, cwd=None):
        """Run the script normally and under -S; both runs must agree. Returns (code, stdout lines, stderr)."""
        args = list(query) if root is None and cwd is not None else ["--root", root or self.root, *query]
        watched = cwd or root or self.root
        before = tree(watched) if Path(watched).is_dir() else None
        results = []
        for flags in (["-B"], ["-S", "-B"]):
            proc = subprocess.run([sys.executable, *flags, str(SCRIPT), *args], cwd=cwd, capture_output=True,
                                  text=True, encoding="utf-8")
            self.assertNotIn("Traceback", proc.stderr, f"{flags}: {proc.stderr}")
            results.append((proc.returncode, proc.stdout.splitlines(), proc.stderr))
        self.assertEqual(results[0][:2], results[1][:2], "the output differs under python3 -S")
        if before is not None:
            self.assertEqual(tree(watched), before, "the script changed the folder")
        return results[0]

    def assert_hits(self, query_args, expected, code=0, **kw):
        got_code, lines, _ = self.run_script(*query_args, **kw)
        self.assertEqual(lines, expected)
        self.assertEqual(got_code, code)

    # A qualified item ID, in both forms: its definition first, then the lines naming it with its document.
    def test_qualified_item_id_space_form(self):
        self.assert_hits(["SPEC-001 BEH-01"], [DEF_S1_BEH01, ADR_LINE, f"2 hits; {COVERAGE}"])

    def test_qualified_item_id_hash_form(self):
        self.assert_hits(["SPEC-001#BEH-01"], [DEF_S1_BEH01, ADR_LINE, f"2 hits; {COVERAGE}"])

    def test_qualified_item_id_given_as_two_arguments(self):
        self.assert_hits(["SPEC-001", "BEH-01"], [DEF_S1_BEH01, ADR_LINE, f"2 hits; {COVERAGE}"])

    def test_qualified_item_id_of_the_other_document(self):
        self.assert_hits(["SPEC-002 BEH-01"], [DEF_S2_BEH01, S1_LINE_24, f"2 hits; {COVERAGE}"])

    # A document ID: every line naming it, in path then line order, its own id line included.
    def test_document_id(self):
        self.assert_hits(["SPEC-002"], [S1_LINE_24, f'{S2}:2  SPEC-002 v1 draft  "id: SPEC-002"',
                                        f"2 hits; {COVERAGE}"])

    # A bare item ID defined in two documents: both definitions, then every other line naming it.
    def test_bare_item_id_defined_in_two_documents(self):
        self.assert_hits(["BEH-01"], [
            DEF_S1_BEH01,
            DEF_S2_BEH01,
            ADR_LINE,
            f'{S1}:21  SPEC-001 v2 approved  BEH-03 deprecated  "rule: "Replaced by BEH-01: exports were once Excel too.""',
            S1_LINE_24,
            f"5 hits; {COVERAGE}",
        ])

    # A term: every line holding all its words, case-insensitively, in any order, as literal text.
    def test_multi_word_term(self):
        expected = [f'{S1}:18  SPEC-001 v2 approved  BEH-01 active  "rule: "Exports are CSV only; no other format '
                    f'is offered.""', f"1 hits; {COVERAGE}"]
        self.assert_hits(["csv EXPORTS"], expected)
        self.assert_hits(["exports", "csv"], expected)

    def test_term_is_literal_text(self):
        self.assert_hits(["ONLY;"], [f'{S1}:18  SPEC-001 v2 approved  BEH-01 active  "rule: "Exports are CSV only; '
                                     f'no other format is offered.""', f"1 hits; {COVERAGE}"])
        self.assert_hits(["C.V"], [f'no match: "C.V" is in none of 5 files under docs/specs/ (adr, spec)'], code=1)

    # Labels: a deprecated item, and a superseded document.
    def test_deprecated_item_is_labelled(self):
        self.assert_hits(["BEH-03"], [
            f'{S1}:19  SPEC-001 v2 approved  BEH-03 deprecated  "Replaced by BEH-01: exports were once Excel too."',
            f"1 hits; {COVERAGE}"])

    def test_superseded_document_is_labelled(self):
        self.assert_hits(["SPEC-003"], [
            f'docs/specs/spec/SPEC-003.md:2  SPEC-003 v3 superseded, superseded by SPEC-001  "id: SPEC-003"',
            f"1 hits; {COVERAGE}"])

    # ERR-03: no frontmatter, so the path stands for the ID, v?, and the **Status:** line's value.
    def test_document_without_frontmatter(self):
        self.assert_hits(["dark mode"], [
            'docs/specs/notes.md:5  docs/specs/notes.md v? proposal, not approved  '
            '"A dark Mode toggle was mentioned once."',
            f"1 hits; {COVERAGE}"])

    def test_document_without_frontmatter_or_status_line(self):
        build(self.root, {"docs/specs/plain.md": "# Plain\n\nA dark mode note.\n"})
        self.assert_hits(["dark mode"], [
            'docs/specs/notes.md:5  docs/specs/notes.md v? proposal, not approved  '
            '"A dark Mode toggle was mentioned once."',
            'docs/specs/plain.md:3  docs/specs/plain.md v? unknown  "A dark mode note."',
            "2 hits; searched 6 files under docs/specs/ (adr, spec)"])

    # Exit codes, and the no-match line naming what was searched.
    def test_no_match(self):
        self.assert_hits(["dark theme"], ['no match: "dark theme" is in none of 5 files under docs/specs/ (adr, spec)'],
                         code=1)

    def test_root_that_is_not_a_folder_exits_2(self):
        code, lines, err = self.run_script("SPEC-001", root=str(Path(self.root) / "missing"))
        self.assertEqual((code, lines), (2, []))
        self.assertIn("missing", err)

    # ERR-01: no docs/specs/ folder.
    def test_no_specs_folder(self):
        with tempfile.TemporaryDirectory() as empty:
            self.assert_hits(["dark mode"], [f"no docs/specs/ folder under {empty}: nothing is specified yet"],
                             code=1, root=empty)

    def test_default_root_is_the_working_folder(self):
        self.assert_hits(["SPEC-002"], [S1_LINE_24, f'{S2}:2  SPEC-002 v1 draft  "id: SPEC-002"',
                                        f"2 hits; {COVERAGE}"], cwd=self.root)
        with tempfile.TemporaryDirectory() as empty:
            self.assert_hits(["x"], ["no docs/specs/ folder under .: nothing is specified yet"], code=1, cwd=empty)

    # ERR-04: at most 50 hits.
    def test_51_hits_print_50(self):
        body = "".join(f"widget {n}\n" for n in range(1, 52))
        build(self.root, {"docs/specs/spec/SPEC-009.md": "---\nid: SPEC-009\nstatus: draft\nversion: 1\n---\n" + body})
        code, lines, _ = self.run_script("widget")
        self.assertEqual(code, 0)
        self.assertEqual(len(lines), 52)
        self.assertEqual(lines[0], 'docs/specs/spec/SPEC-009.md:6  SPEC-009 v1 draft  "widget 1"')
        self.assertEqual(lines[49], 'docs/specs/spec/SPEC-009.md:55  SPEC-009 v1 draft  "widget 50"')
        self.assertEqual(lines[50:], ["1 more hits: narrow the query",
                                      "51 hits; searched 6 files under docs/specs/ (adr, spec)"])

    def test_long_excerpt_is_cut_to_100_characters(self):
        long = "gadget " + "x" * 120
        build(self.root, {"docs/specs/spec/SPEC-009.md": f"---\nid: SPEC-009\nstatus: draft\nversion: 1\n---\n{long}\n"})
        code, lines, _ = self.run_script("gadget")
        self.assertEqual(lines[0], f'docs/specs/spec/SPEC-009.md:6  SPEC-009 v1 draft  "{long[:99]}…"')

    # ERR-05: an undecodable file is skipped and named; the search goes on.
    def test_undecodable_file_is_skipped_and_named(self):
        build(self.root, {"docs/specs/spec/BAD.md": b"\xff\xfe not utf-8 SPEC-002\n"})
        self.assert_hits(["SPEC-002"], [
            S1_LINE_24, f'{S2}:2  SPEC-002 v1 draft  "id: SPEC-002"',
            f"2 hits; {COVERAGE}; skipped 1 unreadable: docs/specs/spec/BAD.md"])

    def test_undecodable_file_named_on_no_match(self):
        build(self.root, {"docs/specs/spec/BAD.md": b"\xff\xfe\n"})
        self.assert_hits(["dark theme"], [
            'no match: "dark theme" is in none of 5 files under docs/specs/ (adr, spec); '
            "skipped 1 unreadable: docs/specs/spec/BAD.md"], code=1)

    # Standard library only.
    def test_imports_only_the_standard_library(self):
        source = SCRIPT.read_text(encoding="utf-8")
        imported = {line.split()[1].split(".")[0] for line in source.splitlines()
                    if line.startswith(("import ", "from "))}
        self.assertLessEqual(imported, set(sys.stdlib_module_names))

    def test_script_is_executable(self):
        self.assertTrue(os.access(SCRIPT, os.X_OK))


if __name__ == "__main__":
    unittest.main()
