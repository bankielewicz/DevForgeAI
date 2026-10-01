"""Unit tests for the brainstorm skill's BRN validator, scripts/validate_brn.py (SPEC-001 BEH-09).

Each case writes its own BRN under a temporary docs/specs/brainstorm/ and runs the script as a subprocess
twice: with this interpreter's packages, where PyYAML adds a YAML syntax check, and with `-S`, which
hides every site-packages directory as a machine without PyYAML would. The verdict must not depend on
which one ran, and the script must never end in a traceback.

Run from the repository root:
    python3 -B src/tests/brainstorm/test_validate_brn.py
"""
import glob
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "src/claude/DevForgeAI/skills/brainstorm"
SCRIPT = SKILL / "scripts/validate_brn.py"
PROBES = ROOT / "src/codex/devforgeai/import-evidence/validator-probes"
LINE = re.compile(r"^line \d+: \S.*$")

VALID = """\
---
id: BRN-001
type: brainstorm
title: "Reducing appointment no-shows at a dental clinic"
status: draft          # draft | converged | archived
version: 1
created: 2026-09-01
updated: 2026-09-01
owner: "Dana"
authors: ["Dana", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "0b6c1d2e-3f40-4a5b-8c7d-9e0f1a2b3c4d"
reviewed_by: []
approved_by: ""
approved_on: null
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
# --- brainstorm-specific ---
participants: ["Dana"]
sources: []
---

# BRN-001 — Reducing appointment no-shows at a dental clinic

## 1. Context

One in eight booked appointments ends in a no-show.

## 2. Problems

```yaml items
problems:
  - id: PRB-01
    status: active
    statement: "Patients forget appointments booked weeks ahead."
    who: "Returning patient"
    evidence: "[NEEDS CLARIFICATION: current no-show rate]"
    severity: high            # high | medium | low
  - id: PRB-02
    status: active
    statement: "Patients can't reschedule outside office hours."
    who: "Working patient"
    evidence: "Front-desk notes"
    severity: medium
```

## 3. Target users

| Persona | Pain |
|---|---|
| Returning patient | Forgets the date |

## 4. Ideas

```yaml items
ideas:
  - id: IDEA-01
    status: active
    idea: "Text a reminder two days before, with a one-tap reschedule link."
    addresses:
      - PRB-01
      - PRB-02
    value: "high"
    effort: "low"
    risk: "low"
    score: 4
    disposition: promoted
    reason: "Cheap to try and addresses both problems."
  - id: IDEA-02
    status: active
    idea: "Take a deposit when booking."
    addresses:
      - PRB-01
    value: "medium"
    effort: "medium"
    risk: "high"
    score: -1
    disposition: open
    reason: null
  - id: IDEA-03
    status: active
    idea: "Offer online self-service rescheduling."
    addresses:
      - PRB-02
    value: "high"
    effort: "medium"
    risk: "low"
    score: 3
    disposition: open
    reason: null
```

## 5. Evaluation method

Diverge-converge, with score = 2 x value - effort - risk.

## 6. Convergence

Dana confirmed IDEA-01 as promoted.

## 7. Assumptions and open questions

```yaml items
assumptions:
  - id: ASM-01
    status: active
    statement: "We believe that patients read text messages within a day."
    validation: "Check delivery and read receipts for one month."
    state: open
```

- [NEEDS CLARIFICATION: Which booking system does the clinic use?]

## 8. Candidate success signals

- Fewer no-shows per month.

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2026-09-01 | claude-code (session 0b6c1d2e-3f40-4a5b-8c7d-9e0f1a2b3c4d) | Initial draft |
"""


def edit(text, old, new):
    """Replace the first `old`, failing loudly if it isn't there."""
    assert old in text, f"fixture has no {old!r}"
    return text.replace(old, new, 1)


def _has_yaml(flags):
    return subprocess.run([sys.executable, *flags, "-c", "import yaml"], capture_output=True).returncode == 0


class Base:
    FLAGS = []

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.folder = self.tmp / "docs/specs/brainstorm"
        self.folder.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_file(self, path):
        p = subprocess.run([sys.executable, "-B", *self.FLAGS, str(SCRIPT), str(path)],
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(p.stderr, "", p.stderr)
        return p.returncode, p.stdout.splitlines()

    def run_text(self, text=None, raw=None, name="BRN-001.md"):
        path = self.folder / name
        if raw is not None:
            path.write_bytes(raw)
        else:
            path.write_text(text, encoding="utf-8")
        return self.run_file(path)

    def assert_valid(self, text):
        code, lines = self.run_text(text)
        self.assertEqual(code, 0, "\n".join(lines))
        self.assertTrue(lines[-1].startswith("OK: "), lines)

    def assert_invalid(self, lines, code, *patterns):
        """Exit 1, one `line N: message` per problem plus a count, and a line matching each pattern."""
        self.assertEqual(code, 1, "\n".join(lines))
        self.assertRegex(lines[-1], r"^\d+ problem\(s\) in ")
        for line in lines[:-1]:
            self.assertRegex(line, LINE)
        for pattern in patterns:
            self.assertTrue(any(re.search(pattern, l) for l in lines),
                            f"no line matches {pattern!r} in:\n" + "\n".join(lines))
        return lines[:-1]

    def assert_rejects(self, text, *patterns):
        code, lines = self.run_text(text)
        return self.assert_invalid(lines, code, *patterns)

    # --- Valid documents -----------------------------------------------------------------------

    def test_valid_brn_passes(self):
        self.assert_valid(VALID)

    def test_real_brn_001_passes(self):
        self.assert_valid((ROOT / "docs/specs/brainstorm/BRN-001.md").read_text(encoding="utf-8"))

    def test_valid_leap_day_passes(self):
        text = edit(VALID, "created: 2026-09-01", "created: 2028-02-29")
        self.assert_valid(edit(text, "updated: 2026-09-01", "updated: 2028-02-29"))

    def test_block_lists_and_link_records_pass(self):
        text = edit(VALID, "sources: []", 'sources:\n  - "Front-desk notes, 2026-09-01"  # raw input\n'
                    '  - "https://example.com/no-show-report"')
        text = edit(text, 'authors: ["Dana", "claude-code"]', 'authors:\n  - "Dana"\n  - "claude-code"')
        text = edit(text, "upstream: []",
                    'upstream:\n  - {id: BRN-002, relation: informed_by, version: 1, hash: null, note: "x"}')
        self.assert_valid(text)

    def test_a_comment_on_an_id_line_passes(self):
        self.assert_valid(edit(VALID, "  - id: IDEA-03", "  - id: IDEA-03   # from Dana"))

    def test_a_comment_on_an_addresses_entry_passes(self):
        self.assert_valid(edit(VALID, "      - PRB-02\n    value", "      - PRB-02  # main\n    value"))

    def test_inline_html_in_a_table_passes(self):
        self.assert_valid(edit(VALID, "| Forgets the date |", "| Forgets the date<br>Lives far away |"))

    def test_a_last_row_written_by_a_person_passes(self):
        self.assert_valid(VALID + "| 2 | 2026-09-02 | Dana | Fixed a typo in PRB-02 |\n")

    def test_a_placeholder_owner_passes(self):
        self.assert_valid(edit(VALID, 'owner: "Dana"', 'owner: "[NEEDS CLARIFICATION: owner]"'))

    # --- Dates (finding 3, M5): rejected with and without PyYAML, never a traceback --------------

    def test_impossible_month_is_rejected(self):
        errors = self.assert_rejects(edit(VALID, "created: 2026-09-01", "created: 2026-13-45"),
                                     r"^line 7: created 2026-13-45 is not a real calendar date")
        self.assertEqual(len(errors), 1, errors)

    def test_february_29_in_a_common_year_is_rejected(self):
        errors = self.assert_rejects(edit(VALID, "updated: 2026-09-01", "updated: 2026-02-29"),
                                     r"^line 8: updated 2026-02-29 is not a real calendar date")
        self.assertEqual(len(errors), 1, errors)

    def test_date_with_the_wrong_shape_is_rejected(self):
        self.assert_rejects(edit(VALID, "created: 2026-09-01", "created: 2026-9-1"),
                            r"created must be an unquoted YYYY-MM-DD date")

    # --- Empty template defaults (finding 5) ---------------------------------------------------

    def test_empty_owner_is_rejected(self):
        self.assert_rejects(edit(VALID, 'owner: "Dana"', 'owner: ""'),
                            r"^line 9: owner must be a quoted name")

    def test_empty_authors_is_rejected(self):
        self.assert_rejects(edit(VALID, 'authors: ["Dana", "claude-code"]', "authors: []"),
                            r"^line 10: authors must be a non-empty list of quoted names")

    def test_blank_change_log_author_is_rejected(self):
        text = edit(VALID, "| claude-code (session 0b6c1d2e-3f40-4a5b-8c7d-9e0f1a2b3c4d) |", "| |")
        self.assert_rejects(text, r"last Change Log row has no author")

    def test_unfilled_template_is_rejected(self):
        code, lines = self.run_text((SKILL / "assets/brainstorm.md").read_text(encoding="utf-8"))
        self.assert_invalid(lines, code, r"owner must be a quoted name", r"authors must be a non-empty list",
                            r"leftover template placeholder '<topic>'", r"generated_by.tool",
                            r"^line 2: leftover template placeholder BRN-000: replace it with the allocated",
                            r"^line 108: last Change Log row has no author")

    # --- Codex import probes (M7, src/codex/devforgeai/IMPORT-REPORT.md D-03) -------------------

    def test_authors_that_is_not_a_list_is_rejected(self):
        self.assert_rejects(edit(VALID, 'authors: ["Dana", "claude-code"]', "authors: 123"),
                            r"^line 10: authors must be a non-empty list of quoted names")

    def test_unknown_generated_by_key_is_rejected(self):
        text = edit(VALID, '  session: "0b6c', '  unexpected: "not allowed"\n  session: "0b6c')
        self.assert_rejects(text, r"^line 14: generated_by.unexpected is not allowed")

    def test_placeholder_in_a_change_log_cell_is_rejected(self):
        self.assert_rejects(edit(VALID, "| Initial draft |", "| <change> |"),
                            r"leftover template placeholder '<change>'")

    def test_codex_probe_files_are_rejected(self):
        expected = {"authors-not-a-list": r"authors must be a non-empty list",
                    "unknown-provenance-key": r"generated_by.unexpected is not allowed",
                    "placeholder-in-change-log": r"placeholder '<change>'"}
        files = sorted(glob.glob(str(PROBES / "*/claude/docs/specs/brainstorm/BRN-001.md")))
        if not files:
            self.skipTest("no Codex probe files in this checkout")
        for f in files:
            probe = Path(f).parts[-6]
            with self.subTest(probe=probe):
                code, lines = self.run_file(f)
                self.assert_invalid(lines, code, expected[probe])

    # --- Item-block parsing (finding 8) --------------------------------------------------------

    def test_a_comment_on_an_id_line_keeps_items_apart(self):
        # Before the fix, IDEA-03's fields replaced IDEA-02's and the bad disposition went unseen.
        text = edit(VALID, "  - id: IDEA-03", "  - id: IDEA-03  # from Dana")
        text = edit(text, "score: -1\n    disposition: open", "score: -1\n    disposition: maybe")
        self.assert_rejects(text, r"IDEA-02: disposition must be one of")

    def test_unindented_list_items_are_reported_plainly(self):
        block = VALID[VALID.index("problems:\n"):VALID.index("```", VALID.index("problems:\n"))]
        flat = "\n".join(l[2:] if l.startswith("  ") else l for l in block.split("\n"))
        lines = self.assert_rejects(edit(VALID, block, flat),
                                    r"list items must be indented under 'problems:'")
        self.assertFalse(any("second top-level key" in l or "no problems" in l for l in lines), lines)

    def test_empty_block_is_reported_after_an_earlier_error(self):
        text = edit(VALID, 'title: "Reducing', "title: Reducing")
        text = edit(text, 'clinic"\nstatus', "clinic\nstatus")
        text = edit(text, "- Fewer no-shows per month.\n",
                    "- Fewer no-shows per month.\n\n```yaml items\n```\n")
        self.assert_rejects(text, r"title must be a non-empty quoted string", r"empty yaml items block")

    def test_text_after_a_closing_quote_is_rejected(self):
        self.assert_rejects(edit(VALID, 'who: "Returning patient"', 'who: "Returning" patient "x"'),
                            r"PRB-01: who must be a quoted string")

    def test_second_collection_in_one_block_is_rejected(self):
        text = edit(VALID, "    severity: medium\n```", "    severity: medium\nideas:\n```")
        self.assert_rejects(text, r"second top-level key 'ideas'.*own")

    def test_non_utf8_file_is_reported(self):
        raw = VALID.encode("utf-8").replace(b"One in eight", b"One in \xff eight", 1)
        code, lines = self.run_text(raw=raw)
        self.assert_invalid(lines, code, r"^line 0: file is not UTF-8")

    # --- Other frontmatter values (finding 8) --------------------------------------------------

    def test_supersedes_must_be_empty(self):
        self.assert_rejects(edit(VALID, "supersedes: []", "supersedes: [BRN-002]"),
                            r"supersedes must be \[\]")

    def test_superseded_by_must_be_null(self):
        self.assert_rejects(edit(VALID, "superseded_by: null", "superseded_by: BRN-002"),
                            r"superseded_by must be null")

    def test_blocked_by_must_be_empty(self):
        self.assert_rejects(edit(VALID, "blocked_by: []", "blocked_by: whatever"), r"blocked_by must be \[\]")

    def test_unquoted_participant_is_rejected(self):
        self.assert_rejects(edit(VALID, 'participants: ["Dana"]', "participants: [Dana]"),
                            r"participants must be \[\] or a list of quoted strings")

    def test_sources_that_is_not_a_list_is_rejected(self):
        self.assert_rejects(edit(VALID, "sources: []", 'sources: "notes"'),
                            r"sources must be \[\] or a list of quoted strings")

    def test_upstream_without_link_records_is_rejected(self):
        self.assert_rejects(edit(VALID, "upstream: []", "upstream: [BRN-002]"),
                            r"upstream must be \[\] or a list of link records")


@unittest.skipUnless(_has_yaml([]), "PyYAML is not installed for this interpreter")
class WithPyYAML(Base, unittest.TestCase):
    """PyYAML importable: the script adds its YAML syntax check."""

    FLAGS = []


@unittest.skipIf(_has_yaml(["-S"]), "PyYAML is importable even with -S")
class WithoutPyYAML(Base, unittest.TestCase):
    """`python3 -S` hides site-packages, so the script runs on the standard library alone."""

    FLAGS = ["-S"]


if __name__ == "__main__":
    unittest.main()
