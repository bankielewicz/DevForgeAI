"""Unit tests for the brainstorm skill's BRN validator, scripts/validate_brn.py (SPEC-001 BEH-09).

Each case writes its own BRN under a temporary docs/specs/brainstorm/ and runs the script as a subprocess
three times: with this interpreter's packages, where PyYAML adds a YAML syntax check; with a throwaway
HOME, which hides user-site packages the way the eval harness does (on this machine that switches PyYAML
6.0.3 for the system's 6.0.1); and with `-S`, which hides every site-packages directory as a machine
without PyYAML would. The verdict must not depend on which one ran, and the script must never end in a
traceback.

Run from the repository root:
    python3 -B src/tests/brainstorm/test_validate_brn.py
"""
import glob
import os
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
MVP_EXAMPLE = ROOT / "src/staging/examples/brainstorm-greenfield-mvp/BRN-001.md"
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


# A new-shape BRN (it has the project-kind line), built from VALID: intake checks IV-01 to IV-07.
USERS = (
    "| Persona | Job to be done | Current workaround | Pain |\n|---|---|---|---|\n"
    "| Returning patient | Keep a check-up booked weeks ahead | A paper card on the fridge | Forgets the date |\n"
    "| Working patient | Move a visit after work | [NEEDS CLARIFICATION: current workaround of Working patient] "
    "| Cannot call during office hours |")
CUT = ("\n\n### First release cut\n\nFirst release cut: proposed, not confirmed\n\n"
       "| Idea | In first release | Why |\n|---|---|---|\n| IDEA-01 | yes | Tests ASM-01, ranked 1. |")
RANKING = ("\n\n### Assumption risk ranking\n\n| Rank | Assumption | If wrong | Confidence | Cheapest test |\n"
           "|---|---|---|---|---|\n| 1 | ASM-01 | Fatal: stops IDEA-01 (1 of 1 in the cut table). | low "
           "| Data: Check delivery and read receipts for one month. |")
SIGNAL = ("- IDEA-01: fewer missed visits; baseline one in eight visits missed (data: front-desk no-show log, "
          "August 2026)")
NEW = edit(VALID, "## 1. Context\n\n", "## 1. Context\n\nProject kind: greenfield\n\n")
NEW = edit(NEW, "sources: []", 'sources: ["data: front-desk no-show log, August 2026", '
           '"note: Dana, conversation of 2026-09-01"]')
NEW = edit(NEW, 'evidence: "Front-desk notes"',
           'evidence: "Callers ask to move visits after hours (note: Dana, conversation of 2026-09-01)"')
NEW = edit(NEW, "| Persona | Pain |\n|---|---|\n| Returning patient | Forgets the date |", USERS)
NEW = edit(NEW, "Dana confirmed IDEA-01 as promoted.", "Dana confirmed IDEA-01 as promoted." + CUT)
NEW = edit(NEW, "    state: open\n```", "    state: open\n```" + RANKING)
NEW = edit(NEW, "- Fewer no-shows per month.", SIGNAL)
# The same BRN with no idea promoted: no first-release idea, so section 8 holds "- None."
NEW_NONE = edit(NEW, 'disposition: promoted\n    reason: "Cheap to try and addresses both problems."',
                "disposition: open\n    reason: null")
NEW_NONE = edit(NEW_NONE, "| Idea | In first release | Why |\n|---|---|---|\n| IDEA-01 | yes | Tests ASM-01, "
                "ranked 1. |", "No idea is promoted or proposed for promotion.")
NEW_NONE = edit(NEW_NONE, "Fatal: stops IDEA-01 (1 of 1 in the cut table).",
                "Minor: stops no idea in the cut table (0 of 0).")
NEW_NONE = edit(NEW_NONE, SIGNAL, "- None.")
# The same BRN with the kind not decided: section 7 says which kind the run worked as.
QUESTION = "- [NEEDS CLARIFICATION: Which booking system does the clinic use?]"
WORKED_AS = "- [NEEDS CLARIFICATION: greenfield or brownfield; this run worked as %s]"
NEW_UNDECIDED = edit(NEW, "Project kind: greenfield", "Project kind: [NEEDS CLARIFICATION: greenfield or brownfield]")
NEW_UNDECIDED = edit(NEW_UNDECIDED, QUESTION, WORKED_AS % "greenfield" + "\n" + QUESTION)

# A brownfield new-shape BRN: the staged example, checks BV-01 to BV-05 (brownfield-iteration.md).
BROWN = (ROOT / "src/staging/examples/brainstorm-brownfield/BRN-002.md").read_text(encoding="utf-8")
PRODUCT = ("| Document | Version | What it already covers |\n|---|---|---|\n"
           "| BRN-001 | 1 | Reducing appointment no-shows at the dental clinic: 6 ideas (2 promoted, 2 parked, "
           "2 rejected, 0 open) |\n"
           "| PRD-001 | 3 | Online booking for returning patients (FR-001 to FR-006) |")
COVERED = "| Suggestion | Covered by |\n|---|---|\n| Text reminders before a visit | PRD-001#FR-003 |"
DECIDED = ("| Idea | Decision | Where |\n|---|---|---|\n"
           "| Open a waitlist for freed slots. | parked | BRN-001#IDEA-05 |\n"
           "| Charge a deposit at booking. | rejected | BRN-001#IDEA-06 |")
UPDATE = ("| BRN-001#ASM-01 | open to validated | 8 of 10 reminder texts were opened within a day (data: "
          "reminder pilot export, October 2026) | confirmed on 2026-11-18 |")
UPDATES = "| Earlier assumption | Change | Evidence | Status |\n|---|---|---|---|\n" + UPDATE
# The same BRN in a project with no document to read (ERR-09).
BROWN_ALONE = edit(BROWN, "upstream:\n  - {id: BRN-001, relation: informed_by, version: 1, hash: null}\n"
                   "  - {id: PRD-001, relation: informed_by, version: 3, hash: null}\n", "upstream: []\n")
BROWN_ALONE = edit(BROWN_ALONE, '  - "document: docs/specs/brainstorm/BRN-001.md v1"\n'
                   '  - "document: docs/specs/prd/PRD-001.md v3"\n', "")
BROWN_ALONE = edit(BROWN_ALONE, PRODUCT, "No document was found in the project.")
BROWN_ALONE = edit(BROWN_ALONE, "    upstream:\n      - {id: BRN-001, item: IDEA-04, relation: informed_by, "
                   "version: 1, hash: null}\n", "")
for _table in (COVERED, DECIDED, UPDATES):
    BROWN_ALONE = edit(BROWN_ALONE, _table, "None.")


def _has_yaml(flags, env=None):
    return subprocess.run([sys.executable, *flags, "-c", "import yaml"], env=env,
                          capture_output=True).returncode == 0


def _system_home():
    home = tempfile.mkdtemp()
    try:
        return _has_yaml([], env=dict(os.environ, HOME=home)), home
    finally:
        shutil.rmtree(home, ignore_errors=True)


_SYSTEM_YAML, _HOME = _system_home()


class Base:
    FLAGS = []
    ENV = {}

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.folder = self.tmp / "docs/specs/brainstorm"
        self.folder.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_file(self, path):
        p = subprocess.run([sys.executable, "-B", *self.FLAGS, str(SCRIPT), str(path)],
                           env=dict(os.environ, **self.ENV), capture_output=True, text=True, timeout=60)
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
                            r"^line 191: last Change Log row has no author",
                            r"^line 41: the Project kind line must be exactly .* \(IV-01\)$")

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

    # --- New-shape BRNs: intake checks IV-01 to IV-07 (intake-and-evidence.md) -------------------

    def test_new_shape_brn_passes(self):
        self.assert_valid(NEW)

    def test_undecided_project_kind_passes(self):
        self.assert_valid(NEW_UNDECIDED)

    def test_undecided_project_kind_without_its_bullet_is_rejected(self):
        errors = self.assert_rejects(edit(NEW_UNDECIDED, WORKED_AS % "greenfield" + "\n", ""),
                                     r"^line 116: while the project kind is not decided, section 7 must hold "
                                     r"exactly one bullet .* \(IV-07\)$")
        self.assertEqual(len(errors), 1, errors)

    def test_undecided_project_kind_with_two_bullets_is_rejected(self):
        text = edit(NEW_UNDECIDED, QUESTION, WORKED_AS % "brownfield" + "\n" + QUESTION)
        self.assert_rejects(text, r"^line 116: while the project kind is not decided, .* \(IV-07\)$")

    def test_decided_project_kind_with_the_bullet_is_rejected(self):
        text = edit(NEW, QUESTION, WORKED_AS % "greenfield" + "\n" + QUESTION)
        errors = self.assert_rejects(text, r"^line 133: the project kind is decided: remove the bullet .* "
                                     r"\(IV-07\)$")
        self.assertEqual(len(errors), 1, errors)

    def test_project_kind_inside_a_fenced_block_is_not_the_gate(self):
        self.assert_valid(edit(VALID, "Dana confirmed IDEA-01 as promoted.",
                               "Dana confirmed IDEA-01 as promoted.\n\n```text\nProject kind: greenfield\n```"))

    def test_wrong_project_kind_value_is_rejected(self):
        self.assert_rejects(edit(NEW, "Project kind: greenfield", "project  kind: Brownfield"),
                            r"^line 31: the Project kind line must be exactly .* \(IV-01\)$")

    def test_project_kind_after_the_prose_is_rejected(self):
        text = edit(NEW, "Project kind: greenfield\n\nOne in eight booked appointments ends in a no-show.",
                    "One in eight booked appointments ends in a no-show.\n\nProject kind: greenfield")
        self.assert_rejects(text, r"^line 33: the Project kind line must be the first line under .* \(IV-01\)$")

    def test_project_kind_without_a_blank_line_after_is_rejected(self):
        self.assert_rejects(edit(NEW, "Project kind: greenfield\n\n", "Project kind: greenfield\n"),
                            r"^line 31: the Project kind line must be the first line under .* \(IV-01\)$")

    def test_second_project_kind_line_is_rejected(self):
        text = edit(NEW, "Dana confirmed IDEA-01 as promoted.",
                    "Dana confirmed IDEA-01 as promoted.\n\nProject kind: brownfield")
        errors = self.assert_rejects(text, r"^line 108: only one Project kind line is allowed \(IV-01\)$")
        self.assertEqual(len(errors), 1, errors)

    def test_sources_entry_without_a_known_kind_is_rejected(self):
        text = edit(NEW, '"data: front-desk no-show log, August 2026"', '"Front-desk no-show log"')
        self.assert_rejects(text, r'^line 24: sources entry "Front-desk no-show log" must be .* \(IV-02\)$')

    def test_sources_entry_with_a_vertical_bar_is_rejected(self):
        text = edit(NEW, '"data: front-desk no-show log, August 2026"', '"data: log | August"')
        self.assert_rejects(text, r"^line 24: sources entry .* \(IV-02\)$")

    def test_duplicate_sources_entry_is_rejected(self):
        text = edit(NEW, '"data: front-desk no-show log, August 2026"',
                    '"note: Dana, conversation of 2026-09-01"')
        self.assert_rejects(text, r"^line 24: duplicate sources entry .* \(IV-02\)$")

    def test_evidence_without_a_source_is_rejected(self):
        text = edit(NEW, " (note: Dana, conversation of 2026-09-01)", "")
        errors = self.assert_rejects(text, r"^line 49: PRB-02: evidence must be one .* \(IV-03\)$")
        self.assertEqual(len(errors), 1, errors)

    def test_evidence_citing_an_unlisted_source_is_rejected(self):
        text = edit(NEW, "(note: Dana, conversation of 2026-09-01)", "(data: call log, 2026)")
        self.assert_rejects(text, r"^line 49: PRB-02: evidence must be one .* \(IV-03\)$")

    def test_marker_with_text_around_it_is_not_cited_evidence(self):
        text = edit(NEW, '"[NEEDS CLARIFICATION: current no-show rate]"',
                    '"High, we think [NEEDS CLARIFICATION: current no-show rate]"')
        self.assert_rejects(text, r"^line 43: PRB-01: evidence must be one .* \(IV-03\)$")

    def test_deprecated_problem_needs_no_cited_evidence(self):
        text = edit(NEW, " (note: Dana, conversation of 2026-09-01)", "")
        text = edit(text, '  - id: PRB-02\n    status: active', '  - id: PRB-02\n    status: deprecated')
        self.assert_valid(edit(text, "\n| Working patient | Move a visit after work | [NEEDS CLARIFICATION: current "
                               "workaround of Working patient] | Cannot call during office hours |", ""))

    def test_section_3_as_prose_is_rejected(self):
        self.assert_rejects(edit(NEW, USERS, "Returning patients and working patients."),
                            r"^line 55: section 3 must start with the table header .* \(IV-04\)$")

    def test_persona_that_is_not_a_who_value_is_rejected(self):
        self.assert_rejects(edit(NEW, "| Working patient | Move", "| Working patients | Move"),
                            r"^line 55: section 3's Persona cells must be .*: expected Returning patient; "
                            r"Working patient, got Returning patient; Working patients \(IV-04\)$")

    def test_missing_persona_row_is_rejected(self):
        text = edit(NEW, "\n| Working patient | Move a visit after work | [NEEDS CLARIFICATION: current workaround "
                    "of Working patient] | Cannot call during office hours |", "")
        self.assert_rejects(text, r"^line 55: section 3's Persona cells must be .* \(IV-04\)$")

    def test_target_users_row_with_an_empty_cell_is_rejected(self):
        self.assert_rejects(edit(NEW, "| A paper card on the fridge |", "| |"),
                            r"^line 57: section 3 holds only the Target users table: .* \(IV-04\)$")

    def test_new_shape_brn_with_no_first_release_idea_passes(self):
        self.assert_valid(NEW_NONE)

    def test_free_text_success_signal_is_rejected(self):
        self.assert_rejects(edit(NEW, SIGNAL, "- Fewer no-shows per month."),
                            r"^line 137: section 8 holds one bullet per first-release idea, .* \(IV-05\)$")

    def test_success_signal_for_an_idea_outside_the_first_release_is_rejected(self):
        text = edit(NEW, "| IDEA-01 | yes | Tests ASM-01, ranked 1. |", "| IDEA-01 | no | Left out by the user. |")
        self.assert_rejects(text, r"^line 135: section 8 must hold one bullet for each idea whose First release "
                            r"cut row says yes \(none\) and no other; .* \(IV-06\)$")

    def test_none_with_a_first_release_idea_is_rejected(self):
        self.assert_rejects(edit(NEW, SIGNAL, "- None."),
                            r"^line 135: section 8 must hold one bullet .* says yes \(IDEA-01\) and no other; .* "
                            r"\(IV-06\)$")

    def test_baseline_without_a_source_is_rejected(self):
        text = edit(NEW, SIGNAL, "- IDEA-01: fewer missed visits; baseline one in eight")
        self.assert_rejects(text, r"^line 137: IDEA-01: baseline must be one .* \(IV-05\)$")

    def test_success_signal_for_an_unknown_idea_is_rejected(self):
        text = edit(NEW, SIGNAL, SIGNAL + "\n- IDEA-09: more bookings; baseline [NEEDS CLARIFICATION: bookings "
                    "a week]")
        self.assert_rejects(text, r"^line 138: section 8: IDEA-09 is not an active idea \(IV-05\)$")

    def test_success_signals_out_of_order_are_rejected(self):
        text = edit(NEW, "| IDEA-01 | yes | Tests ASM-01, ranked 1. |",
                    "| IDEA-01 | yes | Tests ASM-01, ranked 1. |\n| IDEA-03 | yes | Included by the user. |")
        text = edit(text, SIGNAL, "- IDEA-03: more visits moved online; baseline [NEEDS CLARIFICATION: visits "
                    "moved by phone a week]\n" + SIGNAL)
        self.assert_rejects(text, r"^line 139: section 8's bullets must be in ID order, each idea once \(IV-05\)$")

    def test_earlier_shape_brn_is_not_held_to_the_new_checks(self):
        # VALID has no project-kind line: prose in section 3, a free bullet in section 8, uncited evidence.
        code, lines = self.run_text(VALID)
        self.assertEqual((code, len(lines)), (0, 1), lines)

    # --- Brownfield BRNs: checks BV-01 to BV-05 (brownfield-iteration.md) ------------------------

    def brown_valid(self, text):
        code, lines = self.run_text(text, name="BRN-002.md")
        self.assertEqual(code, 0, "\n".join(lines))

    def brown_rejects(self, text, *patterns):
        code, lines = self.run_text(text, name="BRN-002.md")
        return self.assert_invalid(lines, code, *patterns)

    def test_brownfield_example_passes(self):
        self.brown_valid(BROWN)

    def test_brownfield_with_no_document_passes(self):
        self.brown_valid(BROWN_ALONE)

    def test_brownfield_without_assumption_updates_is_rejected(self):
        text = edit(BROWN, "### Assumption updates\n\n" + UPDATES + "\n\n", "")
        errors = self.brown_rejects(text, r"^line 165: a brownfield BRN needs '### Assumption updates' in "
                                    r"section 6 \(BV-01\)$")
        self.assertEqual(len(errors), 1, errors)

    def test_brownfield_without_existing_product_is_rejected(self):
        text = edit(BROWN_ALONE, "### Existing product\n\nNo document was found in the project.\n\n", "")
        self.brown_rejects(text, r"^line 32: a brownfield BRN needs '### Existing product' in section 1 "
                           r"\(BV-01\)$")

    def test_greenfield_with_a_brownfield_heading_is_rejected(self):
        text = edit(BROWN_ALONE, "Project kind: brownfield", "Project kind: greenfield")
        lines = self.brown_rejects(text, r"^line 40: '### Existing product' belongs to a brownfield BRN only: "
                                   r".* \(BV-01\)$")
        self.assertEqual(len(lines), 4, lines)

    def undecided(self, text, worked):
        text = edit(text, "Project kind: brownfield", "Project kind: [NEEDS CLARIFICATION: greenfield or brownfield]")
        return edit(text, "\n- [NEEDS CLARIFICATION: ", "\n" + WORKED_AS % worked + "\n- [NEEDS CLARIFICATION: ")

    def test_undecided_kind_worked_as_brownfield_passes(self):
        self.brown_valid(self.undecided(BROWN, "brownfield"))

    def test_undecided_kind_worked_as_brownfield_needs_every_heading(self):
        text = edit(self.undecided(BROWN_ALONE, "brownfield"), "### Already covered\n\nNone.\n\n", "")
        self.brown_rejects(text, r"^line 156: this run worked as brownfield: '### Already covered' is needed in "
                           r"section 6 \(BV-01\)$")

    def test_undecided_kind_worked_as_greenfield_has_no_brownfield_heading(self):
        lines = self.brown_rejects(self.undecided(BROWN_ALONE, "greenfield"),
                                   r"^line 40: this run worked as greenfield: remove '### Existing product' "
                                   r"\(BV-01\)$")
        self.assertEqual(len(lines), 4, lines)

    def test_brownfield_subsections_out_of_order_are_rejected(self):
        text = edit(BROWN_ALONE, "### Already covered\n\nNone.\n\n### Previously decided\n\nNone.\n\n",
                    "### Previously decided\n\nNone.\n\n### Already covered\n\nNone.\n\n")
        self.brown_rejects(text, r"^line \d+: section 6's subsections must come in this order: .* \(BV-01\)$")

    def test_empty_existing_product_is_rejected(self):
        text = edit(BROWN_ALONE, "No document was found in the project.\n\n", "")
        self.brown_rejects(text, r"^line 40: '### Existing product' must hold its table or the line .* "
                           r"\(BV-02\)$")

    def test_skipped_line_after_the_table_passes(self):
        self.brown_valid(edit(BROWN, PRODUCT, PRODUCT + "\n\nSkipped: docs/specs/prd/PRD-002.md (no frontmatter)"))

    def test_other_text_after_the_table_is_rejected(self):
        text = edit(BROWN, PRODUCT, PRODUCT + "\n\nPRD-002 was unreadable.")
        self.brown_rejects(text, r"^line 51: under '### Existing product', .* \(BV-02\)$")

    def test_existing_product_row_that_is_not_a_document_is_rejected(self):
        text = edit(BROWN, "| PRD-001 | 3 | Online booking", "| ADR-001 | 3 | Online booking")
        self.brown_rejects(text, r"^line 49: Existing product: Document must be a BRN, PRD, EPIC or ARCH ID "
                           r".* \(BV-02\)$")

    def test_document_without_its_upstream_record_is_rejected(self):
        text = edit(BROWN, "  - {id: PRD-001, relation: informed_by, version: 3, hash: null}\n", "")
        self.brown_rejects(text, r"^line 48: PRD-001: the frontmatter's upstream needs the record \{id: PRD-001, "
                           r"relation: informed_by, version: 3, hash: null\} \(BV-02\)$")

    def test_upstream_record_with_another_version_is_rejected(self):
        text = edit(BROWN, "  - {id: PRD-001, relation: informed_by, version: 3, hash: null}",
                    "  - {id: PRD-001, relation: informed_by, version: 2, hash: null}")
        self.brown_rejects(text, r"^line 49: PRD-001: the frontmatter's upstream needs the record .* \(BV-02\)$")

    def test_document_without_its_sources_entry_is_rejected(self):
        text = edit(BROWN, '  - "document: docs/specs/prd/PRD-001.md v3"\n', "")
        self.brown_rejects(text, r'^line 48: PRD-001: sources needs the entry "document: docs/specs/prd/'
                           r'PRD-001\.md v3" \(BV-02\)$')

    def test_document_sources_entries_may_follow_other_entries(self):
        # An extension appends its new entries: the validator checks that each is there, not where.
        entry = '  - "document: docs/specs/prd/PRD-001.md v3"\n'
        note = '  - "note: Dana, conversation of 2026-11-18"\n'
        self.brown_valid(edit(edit(BROWN, entry, ""), note, note + entry))

    def test_covered_by_without_an_item_is_rejected(self):
        text = edit(BROWN, "| PRD-001#FR-003 |", "| PRD-001 |")
        self.brown_rejects(text, r"^line 183: Already covered: Covered by must be .* \(BV-03\)$")

    def test_covered_by_an_unlisted_document_is_rejected(self):
        text = edit(BROWN, "| PRD-001#FR-003 |", "| PRD-009#FR-003 |")
        self.brown_rejects(text, r"^line 183: Already covered: PRD-009#FR-003 cites a document that Existing "
                           r"product does not list \(BV-03\)$")

    def test_already_covered_as_prose_is_rejected(self):
        text = edit(BROWN, COVERED, "Text reminders are covered by PRD-001.")
        self.brown_rejects(text, r"^line 181: '### Already covered' must be the table .* \(BV-03\)$")

    def test_unknown_decision_is_rejected(self):
        text = edit(BROWN, "| parked | BRN-001#IDEA-05 |", "| deferred | BRN-001#IDEA-05 |")
        self.brown_rejects(text, r"^line 189: Previously decided: Decision must be rejected or parked, .* "
                           r"\(BV-04\)$")

    def test_previously_decided_idea_listed_twice_is_rejected(self):
        text = edit(BROWN, "| rejected | BRN-001#IDEA-06 |", "| rejected | BRN-001#IDEA-05 |")
        self.brown_rejects(text, r"^line 190: Previously decided: BRN-001#IDEA-05 is listed twice \(BV-04\)$")

    def test_idea_taken_up_and_still_listed_is_rejected(self):
        text = edit(BROWN, "| parked | BRN-001#IDEA-05 |", "| parked | BRN-001#IDEA-04 |")
        self.brown_rejects(text, r"^line 121: IDEA-03 is linked to BRN-001#IDEA-04, which Previously decided also "
                           r"lists: .* \(BV-04\)$")

    def test_assumption_update_without_a_source_is_rejected(self):
        text = edit(BROWN, " (data: reminder pilot export, October 2026) | confirmed", " | confirmed")
        self.brown_rejects(text, r"^line 196: Assumption updates: Evidence must be a fact that ends with one "
                           r"sources entry in parentheses \(BV-05\)$")

    def test_assumption_update_with_a_marker_as_evidence_is_rejected(self):
        text = edit(BROWN, "8 of 10 reminder texts were opened within a day (data: reminder pilot export, "
                    "October 2026)", "[NEEDS CLARIFICATION: pilot result]")
        self.brown_rejects(text, r"^line 196: Assumption updates: Evidence must be .* \(BV-05\)$")

    def test_unknown_change_is_rejected(self):
        self.brown_rejects(edit(BROWN, "| open to validated |", "| validated |"),
                           r"^line 196: Assumption updates: Change must be .* \(BV-05\)$")

    def test_status_without_a_date_or_with_a_name_is_rejected(self):
        # The second sample is the form of the drafts before 2026-11-20: a cell that names someone is not valid.
        for status in ("confirmed", "confirmed by Dana on 2026-11-18"):
            with self.subTest(status=status):
                self.brown_rejects(edit(BROWN, "| confirmed on 2026-11-18 |\n\n## 7", f"| {status} |\n\n## 7"),
                                   r"^line 196: Assumption updates: Status must be .* \(BV-05\)$")

    def test_status_with_an_impossible_date_is_rejected(self):
        self.brown_rejects(edit(BROWN, "| confirmed on 2026-11-18 |\n\n## 7",
                                "| confirmed on 2026-11-31 |\n\n## 7"),
                           r"^line 196: Assumption updates: Status must be .* \(BV-05\)$")

    def test_proposed_assumption_update_passes(self):
        self.brown_valid(edit(BROWN, "| confirmed on 2026-11-18 |\n\n## 7",
                              "| proposed, not confirmed |\n\n## 7"))

    def test_update_of_an_unlisted_brn_is_rejected(self):
        self.brown_rejects(edit(BROWN, "| BRN-001#ASM-01 | open", "| BRN-007#ASM-01 | open"),
                           r"^line 196: Assumption updates: Earlier assumption must be .* \(BV-05\)$")

    def test_confirmed_update_of_this_brns_assumption_needs_the_new_state(self):
        own = edit(BROWN, UPDATE, UPDATE + "\n" + UPDATE.replace("BRN-001#ASM-01", "BRN-002#ASM-01"))
        self.brown_rejects(own, r"^line 197: Assumption updates: ASM-01 of this BRN must have state validated "
                           r"while its row says 'confirmed' \(BV-05\)$")
        code, lines = self.run_text(edit(own, "    state: open", "    state: validated"), name="BRN-002.md")
        self.assertFalse(any("(BV-05)" in line for line in lines), lines)

    def test_proposed_update_of_this_brns_assumption_keeps_it_open(self):
        own = edit(BROWN, UPDATE, UPDATE + "\n" + UPDATE.replace("BRN-001#ASM-01", "BRN-002#ASM-01").replace(
            "confirmed on 2026-11-18", "proposed, not confirmed"))
        self.brown_valid(own)
        self.brown_rejects(edit(own, "    state: open", "    state: validated"),
                           r"^line 197: Assumption updates: ASM-01 of this BRN must have state open while its row "
                           r"says 'proposed, not confirmed' \(BV-05\)$")


    # --- The path to a first release: MV-01 to MV-12, new-shape BRNs only ------------------------

    def mvp(self, *edits):
        text = MVP_EXAMPLE.read_text(encoding="utf-8")
        for old, new in edits:
            text = edit(text, old, new)
        return text

    def mvp_unconfirmed(self):
        """The example as a run with nobody to confirm writes it: ideas open, draft, the cut proposed."""
        text = re.sub(r'disposition: (?:promoted|parked|rejected)\n    reason: "[^\n]*"',
                      "disposition: open\n    reason: null", self.mvp())
        text = edit(text, "status: converged", "status: draft")
        return edit(text, "First release cut: confirmed on 2026-11-18",
                    "First release cut: proposed, not confirmed")

    def test_mvp_example_passes(self):
        self.assert_valid(self.mvp())

    def test_mvp_unconfirmed_cut_passes(self):
        self.assert_valid(self.mvp_unconfirmed())

    def test_mvp_rows_set_by_the_user_pass(self):
        self.assert_valid(self.mvp(
            ("| IDEA-03 | no | Tests ASM-02, ranked 2, which IDEA-01 already tests. |",
             "| IDEA-03 | yes | Included by the user. |"),
            ("\n\n## Change Log", "\n- IDEA-03: shorter waits at the stop; baseline "
             "[NEEDS CLARIFICATION: how long commuters wait today]\n\n## Change Log")))

    def mvp_idea_01_left_out(self):
        """The unconfirmed example after the typed change 'IDEA-01 out': reasons refreshed, one row flagged."""
        text = self.mvp_unconfirmed()
        for old, new in (
                ("| IDEA-01 | yes | Tests ASM-01, ranked 1. |", "| IDEA-01 | no | Left out by the user. |"),
                ("| IDEA-02 | yes | Tests ASM-03, ranked 3. |", "| IDEA-02 | yes | Tests ASM-01, ranked 1. |"),
                ("| IDEA-03 | no | Tests ASM-02, ranked 2, which IDEA-01 already tests. |",
                 "| IDEA-03 | no | Needs review: no rule supports this value. |")):
            text = edit(text, old, new)
        return re.sub(r"- IDEA-01: [^\n]*\n", "", text)

    def test_mvp_a_flagged_row_passes_in_a_proposed_cut(self):
        self.assert_valid(self.mvp_idea_01_left_out())

    def test_mvp_a_stale_reason_is_rejected_after_a_user_change(self):
        text = edit(self.mvp_idea_01_left_out(), "| IDEA-03 | no | Needs review: no rule supports this value. |",
                    "| IDEA-03 | no | Tests ASM-02, ranked 2, which IDEA-01 already tests. |")
        self.assert_rejects(text, r"the Why cell of IDEA-03 .* \(MV-10\)$")

    def test_mvp_a_user_sentence_is_never_checked_against_the_rules(self):
        self.assert_valid(edit(self.mvp_idea_01_left_out(),
                               "| IDEA-03 | no | Needs review: no rule supports this value. |",
                               "| IDEA-03 | no | Left out by the user. |"))

    def test_mv12_a_confirmed_cut_holds_no_flagged_row(self):
        text = self.mvp(("| IDEA-05 | no | Tests no assumption ranked 1 to 3. |",
                         "| IDEA-05 | no | Needs review: no rule supports this value. |"))
        self.assert_rejects(text, r"a confirmed cut holds no row that says .*; flagged: IDEA-05 \(MV-12\)$")

    def test_mvp_no_open_assumption_takes_the_highest_score(self):
        text = self.mvp().replace("    state: open\n", "    state: validated\n")
        text = re.sub(r"\| Rank \|[^\n]*\n\|---[^\n]*\n(?:\| \d \| ASM[^\n]*\n)+", "None.\n", text)
        for old, new in (
                ("| IDEA-01 | yes | Tests ASM-01, ranked 1. |",
                 "| IDEA-01 | yes | Highest score; no assumption ranked 1 to 3 picks an idea. |"),
                ("| IDEA-02 | yes | Tests ASM-03, ranked 3. |",
                 "| IDEA-02 | no | Tests no assumption ranked 1 to 3. |"),
                ("| IDEA-03 | no | Tests ASM-02, ranked 2, which IDEA-01 already tests. |",
                 "| IDEA-03 | no | Tests no assumption ranked 1 to 3. |")):
            text = edit(text, old, new)
        text = re.sub(r"- IDEA-02: [^\n]*\n", "", text)
        self.assert_valid(text)

    def test_mvp_no_cut_row_passes(self):
        text = re.sub(r"\| Idea \|[^\n]*\n\|---[^\n]*\n(?:\| IDEA[^\n]*\n)+",
                      "No idea is promoted or proposed for promotion.\n", self.mvp_unconfirmed())
        text = re.sub(r"(?:Serious|Fatal): stops [^|]*\|", "Minor: stops no idea in the cut table (0 of 0). |", text)
        text = text.replace("| medium |", "| low |").replace("| high |", "| low |")
        text = re.sub(r"- IDEA-01: [^\n]*\n- IDEA-02: [^\n]*\n", "- None.\n", text)
        self.assert_valid(text)

    def test_mvp_checks_skip_an_earlier_shape_brn(self):
        self.assert_valid(self.mvp(("Project kind: greenfield\n\n", ""),
                                   ("| IDEA-01 | yes | Tests ASM-01, ranked 1. |", "| IDEA-01 | maybe | |")))

    def test_mv01_ranking_heading_is_required(self):
        self.assert_rejects(self.mvp(("### Assumption risk ranking\n\n", "")), r"\(MV-01\)$")

    def test_mv02_ranking_header_row_is_fixed(self):
        self.assert_rejects(self.mvp(("| Rank | Assumption | If wrong | Confidence | Cheapest test |",
                                      "| Rank | Assumption | If wrong |")), r"\(MV-02\)$")

    def test_mv03_ranking_rows_are_the_open_assumptions(self):
        self.assert_rejects(self.mvp(("    state: open\n```", "    state: validated\n```")),
                            r"ASM-01, ASM-02, ASM-03\) \(MV-03\)$")

    def test_mv04_if_wrong_counts_the_cut_rows(self):
        self.assert_rejects(self.mvp(("(1 of 4 in the cut table)", "(1 of 3 in the cut table)")),
                            r"ASM-03: 'If wrong' .* \(MV-04\)$")

    def test_mv05_confidence_needs_a_source_of_its_kind(self):
        self.assert_rejects(self.mvp(('  - "note: Maya Okafor, conversation of 2026-11-18"\n', "")),
                            r"ASM-03: Confidence medium needs .* \(MV-05\)$")

    def test_mv06_ranking_order_is_checked(self):
        first, second = (re.search(rf"^\| {n} \| ASM-0{n} [^\n]*$", self.mvp(), re.M).group(0) for n in (1, 2))
        text = self.mvp((first + "\n" + second, "| 1 |" + second[5:] + "\n| 2 |" + first[5:]))
        self.assert_rejects(text, r"the order is ASM-01, ASM-02, ASM-03, ASM-04 \(MV-06\)$")

    def test_mv07_cheapest_test_comes_from_the_validation(self):
        self.assert_rejects(self.mvp(("| Data: Count the paid jobs per week in the van job log. |",
                                      "| Interview: Count the paid jobs per week in the van job log. |")),
                            r"must be 'Data: Count the paid jobs per week in the van job log\.' \(MV-07\)$")

    def test_mv08_cut_status_line_is_fixed(self):
        # The second sample is the form of the drafts before 2026-11-20: a line that names someone is not valid.
        for new in ("First release cut: confirmed", "First release cut: confirmed by Maya Okafor on 2026-11-18",
                    "First release cut: confirmed on 18 November 2026"):
            with self.subTest(new=new):
                self.assert_rejects(self.mvp(("First release cut: confirmed on 2026-11-18", new)), r"\(MV-08\)$")

    def test_mv09_every_promoted_idea_has_a_cut_row(self):
        self.assert_rejects(self.mvp(("| IDEA-05 | no | Tests no assumption ranked 1 to 3. |\n", "")),
                            r"the promoted idea IDEA-05 has no row \(MV-09\)$")

    def test_mv09_a_parked_idea_has_no_cut_row(self):
        self.assert_rejects(self.mvp(("| IDEA-05 | no | Tests no assumption ranked 1 to 3. |\n",
                                      "| IDEA-05 | no | Tests no assumption ranked 1 to 3. |\n"
                                      "| IDEA-07 | no | Tests no assumption ranked 1 to 3. |\n")),
                            r"'IDEA-07' is not an active idea .* \(MV-09\)$")

    def test_mv10_why_is_a_fixed_sentence(self):
        self.assert_rejects(self.mvp(("| IDEA-05 | no | Tests no assumption ranked 1 to 3. |",
                                      "| IDEA-05 | no | Too big for a first release. |")),
                            r"the Why cell of IDEA-05 .* \(MV-10\)$")

    def test_mv10_why_must_match_the_ranking(self):
        self.assert_rejects(self.mvp(("| IDEA-01 | yes | Tests ASM-01, ranked 1. |",
                                      "| IDEA-01 | yes | Tests ASM-03, ranked 3. |")),
                            r"the Why cell of IDEA-01 .* \(MV-10\)$")

    def test_mv11_each_of_the_top_three_is_tested(self):
        self.assert_rejects(self.mvp(("| IDEA-02 | yes | Tests ASM-03, ranked 3. |",
                                      "| IDEA-02 | no | Tests ASM-01, ranked 1, which IDEA-01 already tests. |")),
                            r"no 'yes' row tests ASM-03, ranked 3; one of IDEA-02 .* \(MV-11\)$")

    def test_mv12_a_confirmed_cut_needs_promoted_ideas(self):
        text = edit(self.mvp_unconfirmed(), "First release cut: proposed, not confirmed",
                    "First release cut: confirmed on 2026-11-18")
        self.assert_rejects(text, r"not promoted: IDEA-01, IDEA-02, IDEA-03, IDEA-05 \(MV-12\)$")

    def test_mv12_a_confirmed_cut_has_a_real_date_from_created_to_updated(self):
        for new in ("confirmed on 2026-11-17", "confirmed on 2026-11-19", "confirmed on 2026-02-30"):
            with self.subTest(new=new):
                self.assert_rejects(self.mvp(("First release cut: confirmed on 2026-11-18",
                                              "First release cut: " + new)),
                                    r"the date of a confirmed cut is a real date .* \(MV-12\)$")


@unittest.skipUnless(_has_yaml([]), "PyYAML is not installed for this interpreter")
class WithPyYAML(Base, unittest.TestCase):
    """PyYAML importable: the script adds its YAML syntax check."""

    FLAGS = []


@unittest.skipUnless(_SYSTEM_YAML, "no PyYAML outside the user site-packages")
class WithoutUserSite(Base, unittest.TestCase):
    """As the eval harness runs it: HOME points elsewhere, so only system-wide PyYAML loads."""

    ENV = {"HOME": _HOME}

    def setUp(self):
        super().setUp()
        Path(_HOME).mkdir(exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(_HOME, ignore_errors=True)


@unittest.skipIf(_has_yaml(["-S"]), "PyYAML is importable even with -S")
class WithoutPyYAML(Base, unittest.TestCase):
    """`python3 -S` hides site-packages, so the script runs on the standard library alone."""

    FLAGS = ["-S"]


if __name__ == "__main__":
    unittest.main()
