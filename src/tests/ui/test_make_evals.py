"""Tests for the ui skill's eval generator, src/tests/ui/make_evals.py (SPEC-017 §9, QR-03, VER-26).

The generator builds src/claude/DevForgeAI/evals/ui/<case>/ (prompt.md, case.yaml, scaffold.sh, graders/). These
tests pin what SPEC-017 §9 fixes about the suite:
- the cases: one for each automated e2e VER item, under the names the spec gives, found by reading the spec itself
  (VER-01 to VER-22 and VER-30 to VER-38), with the tags and limits of §9 and QR-03;
- the shared fixture and prompt: BRN-001 with IDEA-01 to IDEA-06, the four boards in canvas order, the SHA-256 of
  each board computed by the generator;
- the trigger cases: `ui-trigger-01` to `ui-trigger-11`, one tool_used Skill grader each, arm both, tagged trigger,
  ver-22 and ui-trigger, with VER-22's eleven prompts;
- every seeded document validates against src/schemas/ with a format checker, except a document a case marks as
  expected to be invalid, and the DSN-in-PRD exemption (§9, "Documents that cite a DSN") ignores exactly one error:
  the docId pattern at frontmatter/upstream/N/id for an instance that matches ^DSN-\\d{3}$. Another test makes the
  suite fail the day common.schema.json accepts DSN, which is the signal to remove the exemption (§10, cycle C);
- the script on the fixtures: each stop case's boards folder fails with the ERR the case is about;
- generation is deterministic, and the tree committed under evals/ui/ is what the generator writes.

Run from the repository root, under the normal HOME (the generator imports jsonschema and referencing from the
user site):
    python3 -B src/tests/ui/test_make_evals.py
"""
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[3]
GENERATOR = ROOT / "src/tests/ui/make_evals.py"
SPEC = ROOT / "docs/specs/spec/SPEC-017.md"
COMMITTED = ROOT / "src/claude/DevForgeAI/evals/ui"
SCHEMAS = ROOT / "src/schemas"

# The e2e VER items the suite grades (VER-26 is the qualification bar, VER-23 to VER-25 are unit, VER-27 to VER-29 manual).
E2E = [f"VER-{n:02d}" for n in list(range(1, 23)) + list(range(30, 39))]

TRIGGER_PROMPTS = [
    (True, "Record the screen designs for BRN-001 from the boards we copied."),
    (True, "Add the UI design step for our release before the PRD."),
    (True, "Update the UI design: the PRD now names a settings screen."),
    (True, "Turn our Claude Design boards into a design document."),
    (True, "Run the UI design step for BRN-001."),
    (True, "Approve the design document DSN-001. I am Example Owner."),
    (False, "Write the PRD for BRN-001."),
    (False, "What UI framework should I use for a CLI?"),
    (False, "Draw a login screen for me."),
    (False, "Record the approved design for STORY-001."),
    (False, "Make the button on the report page blue."),
]
TRIGGER_MATCH = r'"skill"\s*:\s*"(?:[\w-]+:)?ui"'

# Cases whose correct run writes nothing (§9: "the stop cases"): 15 turns and 300 seconds. Every other case writes
# (60 turns, 900 seconds). The trigger cases are 15 and 300 as well.
STOP_CASES = {
    "no-boards-stops", "boards-at-wrong-number", "canvas-unreadable", "unknown-canvas-format", "board-file-absent",
    "too-many-boards", "unknown-brn", "path-refused", "unconverged-brn", "no-promoted-idea", "malformed-brn",
    "two-dsns-cite", "lists-brns", "no-brainstorm-yet", "no-brn-with-promoted-idea", "amend-nothing-to-do",
    "amend-nothing-with-prd", "amend-nothing-with-unrelated-documents", "plain-run-never-approves",
    "approval-blocked-by-changed-board", "approval-unknown-dsn", "approval-superseded-dsn", "approval-without-id",
}
# The boards folder of each stop case the script refuses, and the ERR it prints first (IF-02), with the DSN ID the
# create or amend run would give the script.
BOARDS_ERRORS = {
    "no-boards-stops": ("DSN-001", "ERR-03"),
    "boards-at-wrong-number": ("DSN-002", "ERR-03"),
    "canvas-unreadable": ("DSN-001", "ERR-04"),
    "unknown-canvas-format": ("DSN-001", "ERR-05"),
    "board-file-absent": ("DSN-001", "ERR-06"),
    "too-many-boards": ("DSN-001", "ERR-12"),
}
DSN_CITING = {"amend-changed-board", "amend-prd-requirement", "amend-adr-consequence"}

M = None            # the generator module
CHECKED = None      # check_fixtures()'s problems, computed once
GENERATED = None    # a tree written by write_cases(), shared by the tests that read it


def load_generator():
    spec = importlib.util.spec_from_file_location("ui_make_evals", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    sys.modules["ui_make_evals"] = module
    spec.loader.exec_module(module)
    return module


def setUpModule():
    global M, GENERATED
    M = load_generator()
    GENERATED = Path(tempfile.mkdtemp(prefix="ui-evals-"))
    M.write_cases(GENERATED)


def tearDownModule():
    shutil.rmtree(GENERATED, ignore_errors=True)


def tree(root):
    """Every file under root: relative path -> bytes."""
    root = Path(root)
    return {str(p.relative_to(root)): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file()}


def front_matter(path):
    text = Path(path).read_text()
    m = re.match(r"---\n(.*?)\n---\n(.*)\Z", text, re.S)
    assert m, f"{path}: no front matter"
    return yaml.safe_load(m.group(1)), m.group(2)


def js(items):
    """JavaScript RegExp results for (pattern, flags, text) triples; a pattern that does not compile gives a string."""
    program = ("const items = JSON.parse(require('fs').readFileSync(0, 'utf8'));"
               "console.log(JSON.stringify(items.map(([p, f, t]) => {"
               "try { return new RegExp(p, f).test(t); } catch (e) { return 'ERR ' + e.message; } })));")
    out = subprocess.run(["node", "-e", program], input=json.dumps(items), capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def spec_verifications():
    text = SPEC.read_text()
    block = re.search(r"```yaml items\nverifications:\n(.*?)\n```", text, re.S).group(1)
    return {v["id"]: v for v in yaml.safe_load("verifications:\n" + block)["verifications"]}


def spec_case_names(obligation):
    """The eval case names an obligation ends with: 'Eval case(s) a, b and c' up to the colon or '(graders …)'."""
    found = re.findall(r"Eval cases? ([a-z0-9][a-z0-9, -]*?)(?: \(graders [\w-]+\))?:", obligation)
    assert len(found) == 1, obligation[-200:]
    return [n for n in re.split(r",\s*|\s+and\s+", found[0]) if n]


def case_by_name():
    return {c.name: c for c in M.CASES}


def run_scaffold(name):
    ws = Path(tempfile.mkdtemp(prefix="ui-ws-"))
    subprocess.run(["bash", str(GENERATED / name / "scaffold.sh")], cwd=ws, check=True, capture_output=True)
    return ws


def run_script(ws, *args):
    p = subprocess.run([sys.executable, "-B", str(M.SCRIPT), *args[:-1], "--root", str(ws), args[-1]],
                       capture_output=True, text=True, env={"PYTHONDONTWRITEBYTECODE": "1", "PATH": "/usr/bin:/bin"})
    return p.returncode, p.stdout


class SpecTests(unittest.TestCase):
    """The suite has the cases the spec names, and nothing else."""

    def test_every_e2e_ver_item_has_its_cases(self):
        specs = spec_verifications()
        cases = case_by_name()
        wanted = set()
        for ver in E2E:
            self.assertIn(ver, specs)
            self.assertEqual("e2e", specs[ver]["level"])
            obligation = specs[ver]["obligation"]
            if ver == "VER-22":
                self.assertIn("ui-trigger-01 to ui-trigger-11", obligation)
                names = [f"ui-trigger-{i:02d}" for i in range(1, 12)]
            else:
                names = spec_case_names(obligation)
            for name in names:
                self.assertIn(name, cases, f"{ver}: no case {name}")
                self.assertIn(ver[4:], cases[name].vers, f"{name} does not grade {ver}")
                wanted.add(name)
        self.assertEqual(wanted, set(cases), "cases the spec does not name, or names the suite lacks")
        self.assertEqual(53, len(M.CASES))

    def test_only_the_e2e_items_are_graded(self):
        graded = {v for c in M.CASES for v in c.vers}
        self.assertEqual({v[4:] for v in E2E}, graded)

    def test_the_shared_prompt_is_the_specs(self):
        text = SPEC.read_text()
        m = re.search(r'\*\*The shared prompt,\*\* unless a case gives its own: "(.*?)" It confirms', text, re.S)
        spec_prompt = " ".join(m.group(1).split())
        self.assertEqual(spec_prompt, " ".join(M.SHARED_PROMPT.split()))
        cases = case_by_name()
        for name in ("writes-dsn", "coverage-and-report", "neighbours-unchanged"):
            self.assertEqual(spec_prompt, " ".join(cases[name].prompt.split()), name)

    def test_unconfirmed_prompt_is_the_specs(self):
        self.assertEqual("Record the UI design for BRN-001. Proceed without questions.",
                         case_by_name()["unconfirmed-stays-null"].prompt.strip())

    def test_the_trigger_prompts_are_the_specs(self):
        obligation = spec_verifications()["VER-22"]["obligation"]
        for _, prompt in TRIGGER_PROMPTS:
            self.assertIn(f"'{prompt}'", obligation)
        cases = case_by_name()
        for i, (_, prompt) in enumerate(TRIGGER_PROMPTS, start=1):
            self.assertEqual(prompt, cases[f"ui-trigger-{i:02d}"].prompt.strip())


class GeneratedTreeTests(unittest.TestCase):
    def test_generation_is_deterministic(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            M.write_cases(Path(a))
            M.write_cases(Path(b))
            self.assertEqual(tree(a), tree(b))
        self.assertEqual(tree(GENERATED), tree(GENERATED))

    def test_the_committed_tree_is_what_the_generator_writes(self):
        self.assertTrue(COMMITTED.is_dir(), "run src/tests/ui/make_evals.py")
        generated, committed = tree(GENERATED), tree(COMMITTED)
        self.assertEqual(sorted(generated), sorted(committed))
        for path in generated:
            self.assertEqual(generated[path], committed[path], path)

    def test_the_layout_of_each_case(self):
        for c in M.CASES:
            d = GENERATED / c.name
            self.assertEqual(
                f'schema_version: "1.1"\nname: {c.name}\ncontext:\n  scaffold_script: scaffold.sh\n',
                (d / "case.yaml").read_text(), c.name)
            self.assertTrue((d / "prompt.md").is_file() and (d / "scaffold.sh").is_file(), c.name)
            self.assertTrue(list((d / "graders").glob("*.md")), f"{c.name} has no grader")
            self.assertTrue((d / "scaffold.sh").stat().st_mode & 0o100, f"{c.name}: scaffold.sh is not executable")

    def test_tags_and_limits(self):
        for c in M.CASES:
            fm, body = front_matter(GENERATED / c.name / "prompt.md")
            self.assertEqual(c.prompt.strip(), body.strip(), c.name)
            if c.name.startswith("ui-trigger-"):
                self.assertEqual(["trigger", "ver-22", "ui-trigger"], fm["tags"], c.name)
                self.assertNotIn("ui", fm["tags"])
                self.assertEqual((15, 300), (fm["max_turns"], fm["timeout_seconds"]), c.name)
                continue
            self.assertEqual(["ui"] + [f"ver-{v}" for v in c.vers], fm["tags"], c.name)
            expected = (15, 300) if c.name in STOP_CASES else (60, 900)
            self.assertEqual(expected, (fm["max_turns"], fm["timeout_seconds"]), c.name)
            self.assertEqual(["Skill", "Read", "Glob", "Grep", "Write", "Edit", "Bash"], fm["allowed_tools"], c.name)
        names = {c.name for c in M.CASES}
        self.assertTrue(STOP_CASES <= names)

    def test_grader_names_and_files(self):
        for c in M.CASES:
            names = [g.name for g in c.graders]
            self.assertEqual(len(names), len(set(names)), c.name)
            files = sorted(p.stem for p in (GENERATED / c.name / "graders").glob("*.md"))
            self.assertEqual(sorted(names), files, c.name)
            for n in names:
                self.assertTrue(re.match(r"ver(%s)-" % "|".join(c.vers), n), f"{c.name}: {n}")

    def test_graders_are_well_formed(self):
        for c in M.CASES:
            for g in c.graders:
                fm, body = front_matter(GENERATED / c.name / "graders" / f"{g.name}.md")
                where = f"{c.name}/{g.name}"
                self.assertIn(fm["type"], ("regex", "file_exists", "tool_used"), where)
                if fm["type"] == "regex":
                    self.assertIn(fm["match"], ("contains", "not_contains"), where)
                    self.assertTrue(fm["target"] == "last_message"
                                    or (fm["target"]["source"] == "file" and fm["target"]["path"].startswith("docs/")),
                                    where)
                    pattern = body[:-1] if body.endswith("\n") else body
                    self.assertTrue(pattern and "\n" not in pattern, where)
                    self.assertEqual(g.pattern, pattern, where)
                elif fm["type"] == "file_exists":
                    self.assertTrue(fm["path"].startswith("docs/") and isinstance(fm["exists"], bool), where)

    def test_whole_content_graders_have_no_m_flag(self):
        # SPEC-017 §9 (VER-20): written ^…$ without the m flag, as the context suite does.
        found = 0
        for c in M.CASES:
            for g in c.graders:
                if g.type == "regex" and g.pattern.startswith("^") and g.pattern.endswith("$") and g.name.endswith("-unchanged"):
                    found += 1
                    self.assertNotIn("m", g.flags, f"{c.name}/{g.name}")
                    self.assertEqual("contains", g.match, f"{c.name}/{g.name}")
        self.assertGreater(found, 10)

    def test_every_regex_compiles_in_javascript(self):
        regexes = [(c.name, g) for c in M.CASES for g in c.graders if g.type == "regex"]
        results = js([[g.pattern, g.flags, ""] for _, g in regexes])
        bad = [(n, g.name, r) for (n, g), r in zip(regexes, results) if isinstance(r, str)]
        self.assertEqual([], bad)

    def test_graders_read_replies_and_files_only(self):
        for c in M.CASES:
            for g in c.graders:
                if g.type == "tool_used":
                    self.assertTrue(c.name.startswith("ui-trigger-"), f"{c.name}/{g.name}: tool_used outside a trigger case")
                if g.type == "regex":
                    # VER-02: never whether the prd skill exists
                    self.assertNotIn("SKILL.md", g.pattern, f"{c.name}/{g.name}")

    def test_trigger_cases(self):
        for i, (fires, prompt) in enumerate(TRIGGER_PROMPTS, start=1):
            c = case_by_name()[f"ui-trigger-{i:02d}"]
            self.assertEqual(["22"], c.vers)
            self.assertEqual(1, len(c.graders))
            fm, body = front_matter(GENERATED / c.name / "graders" / f"{c.graders[0].name}.md")
            self.assertEqual("tool_used", fm["type"])
            self.assertEqual("Skill", fm["tool"])
            self.assertEqual(TRIGGER_MATCH, fm["input_match"])
            self.assertEqual("both", fm["arm"])
            if fires:
                self.assertEqual(1, fm["min"])
                self.assertNotIn("max", fm)
            else:
                self.assertEqual(0, fm["min"])
                self.assertEqual(0, fm["max"])
            # the pattern accepts the plugin's namespaced name and the bare name, and no other skill
            yes = ['{"skill": "devforgeai:ui"}', '{"skill":"ui"}', '{"skill": "ui", "args": "BRN-001"}']
            no = ['{"skill": "devforgeai:prd"}', '{"skill": "ui-mockups"}', '{"skill": "devforgeai:context"}']
            self.assertEqual([True] * 3 + [False] * 3, js([[fm["input_match"], "", t] for t in yes + no]))

    def test_trigger_fixtures_have_no_boards_folder(self):
        for i in range(1, 12):
            c = case_by_name()[f"ui-trigger-{i:02d}"]
            self.assertIn("docs/specs/brainstorm/BRN-001.md", c.files)
            self.assertFalse([p for p in c.files if "/boards/" in p or p.startswith("docs/specs/design/")], c.name)

    def test_the_pre_check_grader_accepts_both_ways_of_quoting_the_script(self):
        # VER-10: SKILL.md quotes the script path, the spec shows it unquoted, and the substituted path is absolute.
        g = next(g for g in case_by_name()["amend-changed-board"].graders if g.name == "ver10-pre-check-order")
        replies = {
            "quoted": 'python3 "/home/u/.claude/plugins/devforgeai/skills/ui/scripts/dsn_check.py" boards DSN-001\n'
                      'python3 "/home/u/.claude/plugins/devforgeai/skills/ui/scripts/dsn_check.py" check --before-amend DSN-001\n',
            "unquoted": "python3 ${CLAUDE_SKILL_DIR}/scripts/dsn_check.py boards DSN-001\n"
                        "python3 ${CLAUDE_SKILL_DIR}/scripts/dsn_check.py check --before-amend DSN-001\n",
            "bare": "dsn_check.py boards DSN-001: boards: ok; then dsn_check.py check --before-amend DSN-001: OK\n",
            "single quoted": "python3 '/home/u/skills/ui/scripts/dsn_check.py' boards DSN-001\n"
                             "python3 '/home/u/skills/ui/scripts/dsn_check.py' check --before-amend DSN-001\n",
        }
        bad = {
            "wrong order": 'python3 "/x/dsn_check.py" check --before-amend DSN-001 then python3 "/x/dsn_check.py" boards DSN-001\n',
            "no pre-check": 'python3 "/x/dsn_check.py" boards DSN-001\npython3 "/x/dsn_check.py" check DSN-001\n',
            "no boards": 'python3 "/x/dsn_check.py" check --before-amend DSN-001\n',
        }
        got = js([[g.pattern, g.flags, r] for r in list(replies.values()) + list(bad.values())])
        self.assertEqual([True] * len(replies) + [False] * len(bad), got)


class ReplyGraderTests(unittest.TestCase):
    """Reply graders that a round of review found too loose or too narrow."""

    def grader(self, case, name):
        return next(g for g in case_by_name()[case].graders if g.name == name)

    def results(self, case, name, replies):
        g = self.grader(case, name)
        return js([[g.pattern, g.flags, r] for r in replies])

    def test_the_marker_remains_is_a_sentence_not_the_markers_left_line(self):
        block = ("Design document: DSN-001 (v1, draft; new)\nMarkers left: DSN-001: 1\nOK docs/specs/design/DSN-001.md\n")
        yes = [block + "\nDSN-001 stays draft: the marker for IDEA-06 remains, so I did not offer approval.\n",
               block + "\nI cannot approve while a [NEEDS CLARIFICATION marker is open.\n",
               block + "\nApproval waits until the marker for IDEA-06 is resolved.\n"]
        no = [block, block.replace("Markers left:", "**Markers left:**"), block.replace("Markers left:", "- Markers left:"),
              "Written as a draft.\nIDEA-06 has no board yet.\n"]
        got = self.results("approve-blocked-by-marker", "ver19-reply-says-the-marker-remains", yes + no)
        self.assertEqual([True] * len(yes) + [False] * len(no), got)

    def test_in_review_is_accepted_with_a_hyphen_or_a_space(self):
        yes = ["Only a draft or in-review DSN is approved.", "Only a draft or in review DSN is approved.",
               "A DSN is approved only when it is a draft or In Review."]
        no = ["Only a draft DSN is approved.", "DSN-001 is superseded."]
        got = self.results("approval-superseded-dsn", "ver37-says-only-draft-or-in-review", yes + no)
        self.assertEqual([True] * len(yes) + [False] * len(no), got)

    def test_asking_for_an_id_is_a_question_or_a_request(self):
        yes = ["Which BRN ID should I use?", "Please give me the BRN ID."]
        no = ["The skill takes a BRN ID or approve DSN-NNN, never a path; paths such as docs/specs/brainstorm/BRN-001.md are not accepted."]
        self.assertEqual([True] * 2 + [False], self.results("path-refused", "ver14-asks-for-the-brn-id", yes + no))
        yes = ["Which DSN should I approve? DSN-001 (v1, draft).", "Give me the DSN ID."]
        no = ["Only DSN-NNN can be approved. DSN-001 (v1, draft)."]
        self.assertEqual([True] * 2 + [False], self.results("approval-without-id", "ver37-asks-for-the-dsn-id", yes + no))

    def test_the_malformed_block_is_named_as_a_block(self):
        yes = ["The ideas block of docs/specs/brainstorm/BRN-001.md is malformed YAML."]
        no = ["The ideas of docs/specs/brainstorm/BRN-001.md are malformed YAML (an unterminated quote)."]
        self.assertEqual([True, False], self.results("malformed-brn", "ver17-names-the-ideas-block", yes + no))

    def test_prd_001_is_named_as_citing_dsn_001_on_one_line(self):
        for case, name, n in (("amend-changed-board", "ver10-names-prd-citing-version-1", 1),
                              ("amend-prd-requirement", "ver31-names-prd-001-citing-version-2", 2),
                              ("amend-adr-consequence", "ver32-names-prd-001-citing-version-3", 3)):
            yes = [f"PRD-001 cites DSN-001 at version {n}.", f"DSN-001 is cited by PRD-001 at version {n}."]
            no = [f"PRD-001 cites it at version {n}.", f"DSN-001 is at version {n}.\nPRD-001 is a PRD.",
                  f"PRD-001 cites DSN-001 at version {n + 1}."]
            self.assertEqual([True] * 2 + [False] * 3, self.results(case, name, yes + no), name)


class ObservedReplyTests(unittest.TestCase):
    """Wording of correct replies that suite run 1 (2ace6b9) showed the graders to refuse."""

    results = ReplyGraderTests.results
    grader = ReplyGraderTests.grader

    def test_a_later_run_may_be_an_interactive_run(self):
        yes = ["Left for a later run: FR-037.", "They wait for an interactive run, and PRD-001 is not yet added to `considered`.",
               "Six candidates wait for a later session.", "They are left for the next run."]
        no = ["Next step: run /devforgeai:prd BRN-001.", "Run `/devforgeai:ui BRN-001` again without questions.", "The check is done."]
        got = self.results("amend-candidates-left", "ver38-says-for-a-later-run", yes + no)
        self.assertEqual([True] * len(yes) + [False] * len(no), got)

    def test_six_candidates_may_be_called_requirements(self):
        yes = ["Six candidates from PRD-001 version 2 were left for a later run.",
               "PRD-001 v2 has 6 requirements that name a screen and that no board answers yet:", "6 candidates remain."]
        no = ["Report's mapping is unchanged: version 1 -> 2.", "FR-026 (edit) and FR-025 (summary) are not mapped.",
              "Boards: docs/specs/design/DSN-001/boards/ · 4 · version 1791580000-c3d4"]
        got = self.results("amend-candidates-left", "ver38-says-six-candidates-were-left", yes + no)
        self.assertEqual([True] * len(yes) + [False] * len(no), got)

    def test_one_candidate_left_may_be_named_by_its_id(self):
        yes = ["**Left for a later run:** FR-037, the print screen.", "One candidate (PRD-001 FR-037) was left for a later run.",
               "FR-037 was left for later."]
        no = ["FR-037 is a print screen.", "Declined FR-025 to FR-036 as asked."]
        got = self.results("amend-candidates-capped", "ver38-says-one-candidate-was-left", yes + no)
        self.assertEqual([True] * len(yes) + [False] * len(no), got)

    def test_a_brainstorm_id_is_the_brn_id(self):
        yes = ["Which brainstorm ID should I use? If it's BRN-001, run `/devforgeai:ui BRN-001`.", "Which BRN ID should I use?"]
        no = ["The skill takes a BRN ID, never a path.", "| BRN-001 | Shiftlog: record shifts | converged | 5 | none |"]
        got = self.results("path-refused", "ver14-asks-for-the-brn-id", yes + no)
        self.assertEqual([True] * len(yes) + [False] * len(no), got)


class DigestTests(unittest.TestCase):
    def test_digests_are_the_sha256_of_the_boards(self):
        import hashlib
        self.assertEqual(["Home.dc.html", "List.dc.html", "Add.dc.html", "Report.dc.html"], list(M.BOARDS))
        for name, text in M.BOARDS.items():
            self.assertEqual(hashlib.sha256(text.encode()).hexdigest(), M.DIGESTS[name], name)
            self.assertEqual(64, len(M.DIGESTS[name]))
        self.assertNotEqual(M.digest(M.REPORT_CHANGED), M.DIGESTS["Report.dc.html"])

    def grader_text(self, case):
        return "\n".join(g.pattern for g in case_by_name()[case].graders if g.pattern)

    def test_writes_dsn_names_each_digest(self):
        text = self.grader_text("writes-dsn")
        for name, digest in M.DIGESTS.items():
            self.assertIn(digest, text, name)

    def test_amend_changed_board_names_the_new_report_digest(self):
        text = self.grader_text("amend-changed-board")
        self.assertIn(M.digest(M.REPORT_CHANGED), text)
        for name in ("Home.dc.html", "List.dc.html", "Add.dc.html"):
            self.assertIn(M.DIGESTS[name], text, name)

    def test_the_scaffold_writes_the_boards_in_canvas_order(self):
        ws = run_scaffold("writes-dsn")
        try:
            boards = ws / "docs/specs/design/DSN-001/boards"
            canvas = json.loads((boards / "canvas.json").read_text(), object_pairs_hook=lambda pairs: pairs)
            members = dict(canvas)
            self.assertEqual(3, members["v"])
            self.assertEqual([], members["attachments"])
            self.assertEqual(["Home.dc.html", "List.dc.html", "Add.dc.html", "Report.dc.html"],
                             [k for k, _ in members["boards"]])
            code, out = run_script(ws, "boards", "DSN-001")
            self.assertEqual(0, code, out)
            lines = [l.split() for l in out.splitlines() if l.startswith("board ")]
            self.assertEqual([[str(i + 1), n, str(len(t.encode())), str(t.count("\n")), M.DIGESTS[n]]
                              for i, (n, t) in enumerate(M.BOARDS.items())], [l[1:] for l in lines])
        finally:
            shutil.rmtree(ws, ignore_errors=True)


class SharedFixtureTests(unittest.TestCase):
    def test_brn_001(self):
        m = re.match(r"---\n(.*?)\n---\n", M.BRN, re.S)
        fm = yaml.safe_load(m.group(1))
        self.assertEqual(("BRN-001", "converged", 1, "Example Owner", "Shiftlog: record shifts"),
                         (fm["id"], fm["status"], fm["version"], fm["owner"], fm["title"]))
        ideas = yaml.safe_load(re.search(r"```yaml items\n(ideas:.*?)```", M.BRN, re.S).group(1))["ideas"]
        self.assertEqual({
            "IDEA-01": ("Add a shift from the terminal", "promoted"), "IDEA-02": ("List shifts in a table", "promoted"),
            "IDEA-03": ("A weekly report page", "promoted"), "IDEA-04": ("Export shifts as CSV", "promoted"),
            "IDEA-05": ("Sync to a server", "parked"), "IDEA-06": ("A dark theme for the report page", "promoted"),
        }, {i["id"]: (i["idea"], i["disposition"]) for i in ideas})

    def test_the_shared_fixture_has_no_other_documents(self):
        files = case_by_name()["writes-dsn"].files
        design = sorted(p for p in files if p.startswith("docs/specs/") and "/boards/" not in p)
        self.assertEqual(["docs/specs/brainstorm/BRN-001.md"], design)
        self.assertEqual(5, len([p for p in files if "/boards/" in p]))   # canvas.json and four boards

    def test_the_stop_cases_boards_fail_where_the_case_is_about(self):
        for name, (dsn, err) in BOARDS_ERRORS.items():
            ws = run_scaffold(name)
            try:
                code, out = run_script(ws, "boards", dsn)
                self.assertEqual(1, code, f"{name}: {out}")
                self.assertTrue(out.startswith(err + ":"), f"{name}: {out}")
            finally:
                shutil.rmtree(ws, ignore_errors=True)

    def test_board_file_absent_names_both_boards(self):
        ws = run_scaffold("board-file-absent")
        try:
            code, out = run_script(ws, "boards", "DSN-001")
            self.assertEqual(1, code)
            self.assertIn("Gone.dc.html", out)
            self.assertIn("../outside.dc.html", out)
        finally:
            shutil.rmtree(ws, ignore_errors=True)

    def test_too_many_boards_holds_100(self):
        ws = run_scaffold("too-many-boards")
        try:
            canvas = json.loads((ws / "docs/specs/design/DSN-001/boards/canvas.json").read_text())
            self.assertEqual(100, len(canvas["boards"]))
        finally:
            shutil.rmtree(ws, ignore_errors=True)


class SchemaTests(unittest.TestCase):
    def test_every_seeded_document_validates_apart_from_the_exemption(self):
        checked = 0
        for c in M.CASES:
            for path, text in c.files.items():
                if path in c.unparseable or M.schema_kind(path) is None:
                    continue
                errors, exempt = M.schema_errors(path, text)
                if path in c.invalid:
                    self.assertTrue(errors, f"{c.name}: {path} is marked invalid but validates")
                else:
                    self.assertEqual([], errors, f"{c.name}: {path}")
                checked += 1
        self.assertGreater(checked, 60)

    def test_the_malformed_brn_is_the_only_document_that_cannot_be_read(self):
        c = case_by_name()["malformed-brn"]
        self.assertEqual({"docs/specs/brainstorm/BRN-001.md"}, set(c.unparseable))
        with self.assertRaises(Exception):
            M.parse(c.files["docs/specs/brainstorm/BRN-001.md"])

    def test_the_exempt_error_is_present_for_each_document_that_cites_a_dsn(self):
        citing = {}
        for c in M.CASES:
            for path, text in c.files.items():
                m = re.match(r"---\n(.*?)\n---\n", text, re.S)
                if not m or not path.endswith(".md") or path.startswith("docs/specs/design/"):
                    continue
                fm = yaml.safe_load(m.group(1)) if path not in c.unparseable else {}
                links = [l for l in (fm.get("upstream") or []) if str(l.get("id", "")).startswith("DSN-")]
                if links:
                    errors, exempt = M.schema_errors(path, text)
                    self.assertEqual([], errors, f"{c.name}: {path}")
                    self.assertEqual(len(links), len(exempt), f"{c.name}: {path} has {len(links)} DSN link(s)")
                    for e in exempt:
                        self.assertRegex(e["path"], r"^frontmatter/upstream/\d+/id$")
                        self.assertRegex(e["instance"], r"^DSN-\d{3}$")
                    citing.setdefault(c.name, []).append(path)
        self.assertTrue(DSN_CITING <= set(citing), sorted(citing))
        for name in DSN_CITING:
            self.assertIn("docs/specs/prd/PRD-001.md", citing[name])

    def test_the_exemption_ignores_that_error_and_no_other(self):
        text = case_by_name()["amend-changed-board"].files["docs/specs/prd/PRD-001.md"]
        errors, exempt = M.schema_errors("docs/specs/prd/PRD-001.md", text)
        self.assertEqual(([], 1), (errors, len(exempt)))
        # another error in the same document stays an error
        bad = text.replace("status: approved", "status: finished", 1)
        errors, exempt = M.schema_errors("docs/specs/prd/PRD-001.md", bad)
        self.assertEqual(1, len(exempt))
        self.assertEqual(["frontmatter/status"], [e["path"] for e in errors])
        # a DSN ID that does not match ^DSN-\d{3}$ is no exemption
        odd = text.replace("DSN-001", "DSN-1", 1)
        errors, exempt = M.schema_errors("docs/specs/prd/PRD-001.md", odd)
        self.assertEqual([], exempt)
        self.assertTrue(any(re.match(r"frontmatter/upstream/\d+/id$", e["path"]) for e in errors), errors)

    def test_the_suite_fails_when_the_schema_accepts_dsn(self):
        # The day cycle C adds DSN to the document ID pattern, the exempt error is gone and the presence test above
        # fails: the signal to remove the exemption (§10).
        text = case_by_name()["amend-changed-board"].files["docs/specs/prd/PRD-001.md"]
        with tempfile.TemporaryDirectory() as scratch:
            shutil.copytree(SCHEMAS, scratch, dirs_exist_ok=True)
            common = Path(scratch) / "common.schema.json"
            schema = json.loads(common.read_text())
            pattern = schema["$defs"]["docId"]["pattern"]
            self.assertNotIn("DSN", pattern)
            schema["$defs"]["docId"]["pattern"] = pattern.replace("AMB)", "AMB|DSN)")
            common.write_text(json.dumps(schema))
            errors, exempt = M.schema_errors("docs/specs/prd/PRD-001.md", text, schemas=Path(scratch))
            self.assertEqual(([], []), (errors, exempt))

    def test_the_fixtures_pass_the_scaffold_and_script_checks(self):
        global CHECKED
        if CHECKED is None:
            CHECKED = M.check_fixtures()
        self.assertEqual([], CHECKED)


if __name__ == "__main__":
    unittest.main()
