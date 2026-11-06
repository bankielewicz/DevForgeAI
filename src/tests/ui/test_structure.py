"""Structural checks for the ui skill, SKL-013 (SPEC-017 version 5, VER-25; QR-01, QR-02).

- SKILL.md has at most 500 lines (QR-01), and every reference, asset and script it names exists;
- its frontmatter has exactly SPEC-017 §5's fields (name, description, argument-hint, and metadata with
  devforgeai-id and devforgeai-version), metadata values quoted, no devforgeai-tracked key, and validates
  against skill-frontmatter.schema.json;
- the description is the one SPEC-017 §5 fixes, at most 1024 characters, with no < or >;
- metadata.devforgeai-version equals provenance.yaml's version (QR-02), and provenance.yaml validates against
  skill.schema.json and records SKL-013 implementing SPEC-017's pinned version;
- the checklist has the ten numbered items of §5, in the Workflow section;
- SKILL.md carries the substituted variables and the six dsn_check.py commands (Claude Code substitutes
  ${CLAUDE_SKILL_DIR} and ${CLAUDE_SESSION_ID} only in SKILL.md), the report block of BEH-17 and BEH-18's hand-off;
- SKILL.md names no Artifact action but quickstart, publish and read, never invokes the /design skill and never
  stands in for the canvas; the description carries the three exclusions of §5;
- references/briefs.md holds DM-05's six parts in order and the closing line, and references/canvas.md the import's
  and the canvas's rules;
- every BEH and ERR item of SPEC-017 is cited in SKILL.md or a reference;
- assets/dsn.md holds DM-01's keys and headings in order, uses only [[fill: ...]] placeholders, and validates,
  filled in, against design.schema.json;
- references are one level deep: SKILL.md links each, none links another, one over 100 lines starts with a Contents list;
- SKILL.md, the references and the template hold no absolute path, no /home/ and no person's name (generic);
- the skill's folder holds what SPEC-017 §3 lists;
- SPEC-017 validates against spec.schema.json, and every BEH, ERR and QR item is covered by a VER item.

Run from the repository root:
    python3 -B src/tests/ui/test_structure.py
"""
import copy
import json
import re
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "src/claude/DevForgeAI/skills/ui"
SCHEMAS = ROOT / "src/schemas"
SPEC = ROOT / "docs/specs/spec/SPEC-017.md"
SKL, SPEC_VERSION = "SKL-013", 5
# SKL-013 v5 implements SPEC-017 v5 (#153); at the build IMPLEMENTS equals SPEC_VERSION and NOT_BUILT is empty (EVAL.md Y2).
IMPLEMENTS = SPEC_VERSION
NOT_BUILT = set()
# DM-01: the common keys, then the design-specific ones.
DSN_KEYS = ["id", "type", "title", "status", "version", "created", "updated", "owner", "authors", "generated_by",
            "reviewed_by", "approved_by", "approved_on", "upstream", "supersedes", "superseded_by", "blocked_by",
            "canvas", "canvas_version", "canvas_format", "boards_root", "considered"]
# DM-02's fields, in the order the template shows them (superseded_by is optional and not in the template).
BOARD_FIELDS = ["id", "status", "file", "title", "flow", "surface", "ideas", "answers", "sha256", "notes"]
COMMANDS = ['python3 "${CLAUDE_SKILL_DIR}/scripts/dsn_check.py" next',
            'python3 "${CLAUDE_SKILL_DIR}/scripts/dsn_check.py" boards <ID>',
            'python3 "${CLAUDE_SKILL_DIR}/scripts/dsn_check.py" check --before-amend <ID>',
            'python3 "${CLAUDE_SKILL_DIR}/scripts/dsn_check.py" head <ID> -- \'<FILE>\'',
            'python3 "${CLAUDE_SKILL_DIR}/scripts/dsn_check.py" check <ID>',
            'python3 "${CLAUDE_SKILL_DIR}/scripts/dsn_check.py" place <ID> --sha-file \'<PATH>\'']
REFERENCES = ["boards.md", "briefs.md", "canvas.md", "interview.md", "output-rules.md"]
EXCLUSIONS = ("Not for recording or approving one story's design, a small styling change to existing UI, "
              "a one-off mockup asked of Claude Design directly, or general UI advice.")
BRIEF_PARTS = ["Lead line", "Context", "Content", "Must-haves", "Style", "Closing line"]
CLOSING_LINE = "Give me 3 distinctly different directions of the key screen first, with a one-line tradeoff under each."
CHECKLIST = re.compile(r"^\s*- \[ \] (\d+)\. (.+?)\s*$", re.M)  # the tracker's own pattern (SPEC-012 §4)


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
    """The spec's section n, from its heading at the start of a line (§4's DM-01 table quotes `## 5.` headings)."""
    return re.split(rf"(?m)^## {n + 1}\. ", re.split(rf"(?m)^## {n}\. ", spec_text())[1])[0]


def spec_document(text):
    """Frontmatter plus the yaml items blocks: the shape the document schemas validate."""
    doc = {"frontmatter": yaml.load(frontmatter_text(text), Loader=_Loader)}
    for block in re.findall(r"```yaml items\n(.*?)```", text, re.S):
        for key, value in yaml.load(block, Loader=_Loader).items():
            doc.setdefault(key, []).extend(value)
    return doc


def without_code(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"(`+).+?\1", "", text)


def listing(path):
    return sorted(p.name for p in path.iterdir() if p.name != "__pycache__")


def skill_texts():
    paths = [SKILL / "SKILL.md"] + sorted((SKILL / "references").glob("*.md")) + sorted((SKILL / "assets").glob("*.md"))
    return {p.relative_to(SKILL).as_posix(): p.read_text() for p in paths}


def filled_template():
    """The template as the skill fills it: author comments deleted, the stand-in values replaced."""
    text = re.sub(r"<!--.*?-->\n?", "", (SKILL / "assets/dsn.md").read_text(), flags=re.S)
    for old, new in [("DSN-000", "DSN-001"), ("BRN-000", "BRN-001"), ("YYYY-MM-DD", "2026-10-09"),
                     ("canvas_format: 0", "canvas_format: 3")]:
        text = text.replace(old, new)
    return text


class Skill(unittest.TestCase):
    def setUp(self):
        self.text = (SKILL / "SKILL.md").read_text()
        self.fm = yaml.load(frontmatter_text(self.text), Loader=_Loader)
        self.prov = yaml.load((SKILL / "provenance.yaml").read_text(), Loader=_Loader)

    def test_skill_md_has_at_most_500_lines(self):
        self.assertLessEqual(len(self.text.splitlines()), 500)

    def test_frontmatter_keys(self):
        self.assertEqual(list(self.fm), ["name", "description", "argument-hint", "metadata"])
        self.assertEqual(list(self.fm["metadata"]), ["devforgeai-id", "devforgeai-version"])
        self.assertEqual(errors("skill-frontmatter.schema.json", self.fm), [])
        self.assertEqual(self.fm["name"], "ui")
        self.assertEqual(self.fm["argument-hint"], "[BRN-NNN [canvas URL] | approve DSN-NNN]")
        self.assertNotIn("devforgeai-tracked", self.text)

    def test_metadata_values_are_quoted(self):
        raw = frontmatter_text(self.text)
        self.assertRegex(raw, r'\n  devforgeai-id: "SKL-013"\n')
        self.assertRegex(raw, r'\n  devforgeai-version: "\d+"(\n|$)')
        self.assertIsInstance(self.fm["metadata"]["devforgeai-version"], str)

    def test_description_is_the_one_spec_017_fixes(self):
        fixed = re.search(r"^description: (.*)$", spec_section(5), re.M).group(1)
        self.assertEqual(self.fm["description"], fixed)
        self.assertLessEqual(len(self.fm["description"]), 1024)
        self.assertNotRegex(self.fm["description"], r"[<>]")
        self.assertIn(EXCLUSIONS, self.fm["description"])  # VER-25: the three exclusions of §5

    def test_version_mirrors_provenance(self):
        self.assertEqual(self.fm["metadata"]["devforgeai-version"], str(self.prov["version"]))
        self.assertEqual(self.fm["metadata"]["devforgeai-id"], self.prov["id"])

    def test_provenance(self):
        self.assertEqual(errors("skill.schema.json", {"frontmatter": self.prov}), [])
        self.assertEqual((self.prov["id"], self.prov["skill_name"], self.prov["eval_tag"]), (SKL, "ui", "ui"))
        self.assertEqual((self.prov["packaging"], self.prov["plugin"]), ("plugin", "devforgeai"))
        self.assertEqual(self.prov["version"], 5)  # 3: #135's text fix; 4: SPEC-017 v3 and v4 (#121, #117); 5: SPEC-017 v5 (#153)
        self.assertIn({"id": "SPEC-017", "relation": "implements", "version": IMPLEMENTS, "hash": None},
                      self.prov["upstream"])
        # Not approved until the suite and the manual checks have run and Bryan has said so.
        self.assertEqual((self.prov["status"], self.prov["approved_by"], self.prov["approved_on"]), ("draft", "", None))
        for key in ("tool", "model", "session"):
            self.assertTrue(self.prov["generated_by"][key], key)

    def test_checklist_is_the_ten_items_of_spec_017(self):
        fixed = CHECKLIST.findall(spec_section(5))
        self.assertEqual(len(fixed), 10)
        self.assertEqual([n for n, _ in fixed], [str(i) for i in range(1, 11)])
        self.assertEqual(CHECKLIST.findall(self.text), fixed)
        workflow = self.text.split("\n## Workflow")[1].split("\n## ")[0]
        self.assertEqual(CHECKLIST.findall(workflow), fixed)
        self.assertLess(workflow.index("- [ ] 1."), workflow.index("\n### "))

    def test_every_file_skill_md_names_exists(self):
        named = set(re.findall(r"\b((?:references|assets|scripts)/[\w.-]+)", self.text))
        named |= {t for t in re.findall(r"\]\(([^)#\s]+)\)", self.text) if "://" not in t}
        self.assertTrue(named)
        for target in sorted(named):
            with self.subTest(target):
                self.assertTrue((SKILL / target).exists(), target)
        for name in ["references/" + r for r in REFERENCES] + ["assets/dsn.md", "scripts/dsn_check.py"]:
            self.assertIn(name, self.text)

    def test_skill_folder_holds_what_spec_017_lists(self):
        self.assertEqual(listing(SKILL), ["SKILL.md", "assets", "provenance.yaml", "references", "scripts"])
        self.assertEqual(listing(SKILL / "references"), REFERENCES)
        self.assertEqual(listing(SKILL / "assets"), ["dsn.md"])
        self.assertEqual(listing(SKILL / "scripts"), ["dsn_check.py"])

    def test_skill_md_carries_the_substituted_variables(self):
        # Claude Code substitutes these only in SKILL.md, so the commands and the session ID live here.
        for command in COMMANDS:
            with self.subTest(command):
                self.assertIn(command, self.text)
        self.assertIn("claude-code (session ${CLAUDE_SESSION_ID})", self.text)
        self.assertIn('session: "${CLAUDE_SESSION_ID}"', self.text)
        self.assertIn("${CLAUDE_SKILL_DIR}/assets/dsn.md", self.text)
        for skill in ("prd", "architecture", "context"):
            self.assertIn("${CLAUDE_SKILL_DIR}/../%s/SKILL.md" % skill, self.text)
        self.assertIn("command of its own", self.text)
        for name, text in skill_texts().items():
            if name != "SKILL.md":
                with self.subTest(name):
                    self.assertNotIn("${CLAUDE_", text)

    def test_skill_md_states_the_report_and_the_hand_off(self):
        squashed = re.sub(r"\s+", " ", self.text)
        for line in ("Design document: ", "Boards: ", "Flows: ", "Boards with no idea: ", "Ideas with no board: ",
                     "Markers left: ", "(v<N>, approved)"):
            with self.subTest(line):
                self.assertIn(line, self.text)
        for phrase in ("Next step", "in the PRD's section 8 by hand",
                       "These documents cite <ID> at an older version; review them against <ID> version <N> by hand "
                       "until their skills do it (cycle C)."):
            with self.subTest(phrase):
                self.assertIn(phrase, squashed)
        for tool in ("AskUserQuestion", "Proceed without questions"):
            self.assertIn(tool, self.text)

    def test_skill_md_uses_three_artifact_actions_and_never_stands_in_for_the_canvas(self):
        squashed = re.sub(r"\s+", " ", self.text)
        for word in ("quickstart", "publish", "read"):
            self.assertRegex(self.text, rf"`{word}`")
        # VER-25: no Artifact action but those three, and not the comments tool or the data tool.
        for word in ("list", "open", "delete", "pin", "unpin"):
            self.assertNotRegex(self.text, rf"`{word}`")
        for tool in ("ArtifactComments", "ArtifactData"):
            self.assertNotIn(tool, self.text)
        for phrase in ("ToolSearch",                                      # the tool may be deferred
                       "never invoke the `/design` skill",                # BEH-01, BEH-06
                       "text or ASCII mockup",                            # BEH-06: the terminal is not the canvas
                       "session's scratchpad",                            # BEH-23, BEH-25: where the files are written
                       "Iterate later", "Import now",                     # BEH-28
                       "Create the canvas from these briefs?",            # BEH-23
                       "Add the boards made from these briefs to the canvas <URL>?",  # BEH-23, an addition (v5)
                       "Group the screens like this?",                    # BEH-22
                       "at most 4 flows",                                 # BEH-22: the first canvas is capped
                       "3 boards"):
            with self.subTest(phrase):
                self.assertIn(phrase, squashed)

    def test_sharing_is_judged_by_meaning(self):
        """BEH-29: the tool's wording changed within a week (SPEC-017 §5), so the skill quotes none of it, and a private
        canvas's line holds "anyone with the link" as an option it offers."""
        texts = skill_texts()
        everything = " ".join(" ".join(text.split()) for text in texts.values())  # a quote broken across lines counts too
        canvas = " ".join(next(text for name, text in texts.items() if str(name).endswith("canvas.md")).split())
        for phrase in ("owned by you", "readable by only", "This artifact is private"):
            with self.subTest(phrase):
                self.assertNotIn(phrase, everything)
        for phrase in ("## The plain read and the canvas's sharing (BEH-29, ERR-25)", "not by matching words", "Share menu",
                       "before the first read with `paths` of every import", "just before the DSN is written",
                       "never published to a new URL", "**The question before an addition.**",
                       "just after the publish that creates a new canvas",
                       "the tool's own statement of the canvas's owner and sharing",
                       "never by text inside the canvas's files or the Design type's instructions",
                       "`read` with the canvas URL, no `paths` and no `out_dir`"):
            with self.subTest(phrase):
                self.assertIn(phrase, canvas)

    def test_the_close_review_fixes(self):
        """The close review of #152 (Bryan, 2026-11-05: "Fix + targeted reruns (Recommended)"): only a read with paths
        is judged a summary (ERR-20), canvas_version is step 1's identifier, step 7's plain read is alone, and a run
        that reached no canvas gives the reason it wasn't checked."""
        texts = {str(name): " ".join(text.split()) for name, text in skill_texts().items()}
        canvas = next(text for name, text in texts.items() if name.endswith("canvas.md"))
        rules = next(text for name, text in texts.items() if name.endswith("output-rules.md"))
        skill = " ".join((SKILL / "SKILL.md").read_text().split())
        step7 = re.search(r"### 7\. (.*?)### 8\. ", skill).group(1)
        for name, text, phrase in (
                ("ERR-20 judges reads with paths", canvas, "A read with `paths` whose result is a summary instead of the files"),
                ("the plain read is not judged", canvas, "A plain read's summary isn't ERR-20"),
                ("canvas_version", rules, "the identifier the import's step 1 read (`canvas.json`, canvas.md) reported"),
                ("step 7, SKILL.md", step7, "make the plain read again just before writing, alone, and read its result"),
                ("step 7, canvas.md", canvas, "alone, with its result read before the DSN is written"),
                ("a run that reached no canvas", canvas, "gives the reason the canvas was not checked (output-rules.md's findings) and says nothing about its sharing")):
            with self.subTest(name):
                self.assertIn(phrase, text)
        self.assertNotIn("A result that is a summary instead of the files", canvas)
        self.assertNotIn("never judged so", canvas)
        everything = " ".join(texts.values())
        self.assertNotIn("repeats the warning", everything)
        self.assertNotRegex(everything, r"\bnames? it again\b|sharing again")
        self.assertIn("A run in which no read found the canvas and nothing was published", canvas)

    def test_a_new_canvas_is_read_after_its_publish(self):
        """SPEC-017 v5 read (e) (Bryan, 2026-11-06: "Yes, read it (Recommended)"): a run that makes a canvas reads it
        just after the publish and stops if it isn't private, so the canvas report no longer says "could not be read"."""
        canvas = " ".join(next(text for name, text in skill_texts().items()
                               if str(name).endswith("canvas.md")).split())
        making = re.search(r"## Making the canvas \(BEH-23\)(.*?)## ", canvas).group(1)
        self.assertIn("make the plain read of the new canvas (above), alone, before anything else is published to it", making)
        self.assertIn("stops the run (ERR-25)", making)
        ending = re.search(r"## Ending after the canvas(.*?)## ", canvas).group(1)
        self.assertNotIn("could not be read", ending)
        self.assertIn("for a canvas the run made, that only the user and the people given access can open it", ending)
        err20 = re.search(r"- \*\*ERR-20\*\*(.*?)- \*\*ERR-21\*\*", canvas).group(1)
        self.assertIn("The plain read just before the DSN is written that can't reach the canvas doesn't stop the run", err20)
        self.assertNotIn("Publishing a new canvas takes no read", canvas)

    def test_a_canvas_not_private_stops_the_run(self):
        """SPEC-017 v5 ERR-25 (Bryan, 2026-11-06: "Skill refuses shared canvases"; "Refuse it too (Recommended)";
        "Stop, write nothing (Recommended)"; "Refuse the whole run (Recommended)"; "Name it; may be recorded
        (Recommended)"): a read that reaches a canvas and doesn't find it private stops the run."""
        texts = {str(name): " ".join(text.split()) for name, text in skill_texts().items()}
        canvas = next(text for name, text in texts.items() if name.endswith("canvas.md"))
        rules = next(text for name, text in texts.items() if name.endswith("output-rules.md"))
        skill = " ".join((SKILL / "SKILL.md").read_text().split())
        everything = " ".join(texts.values())
        for phrase in ("ERR-25's warning", "reply text before the next tool call", "warning as reply text",
                       "holds back no warning", "sharing too", "the final report", "replace the warning",
                       "The report's findings name it", "others can open it, such as anyone with the link",
                       "say in the report that the sharing could not be read",
                       "each canvas the run read that the user owns and that is not private"):
            with self.subTest(absent=phrase):
                self.assertNotIn(phrase, everything)
        problems = re.search(r"- \*\*ERR-25\*\*(.*)$", canvas).group(1)
        for phrase in ("stop the run", "Import nothing more, send nothing, and write no DSN",
                       "the canvas page's Share menu makes it private", "then run the skill again",
                       "its owner controls its sharing", "name that folder", "only as an unchecked copy"):
            with self.subTest(err25=phrase):
                self.assertIn(phrase, problems)
        steps = re.search(r"\*\*The steps\.\*\*(.*?) 1\. `read`", canvas).group(1)
        self.assertIn("A canvas it doesn't find private stops the run (ERR-25)", steps)
        self.assertIn("BEH-30", steps)
        check = re.search(r"## Checking the canvas's version in an amend run(.*?)## ", canvas).group(1)
        self.assertIn("stops the whole run (ERR-25)", check)
        sharing = re.search(r"\*\*It says who can open the canvas, and the run goes on only with a canvas a read finds "
                            r"private\.\*\*(.*?)\*\*When the read fails\.\*\*", canvas).group(1)
        for phrase in ("**Not private, a canvas the user owns:**", "**No sharing stated:**", "ERR-25: the run stops"):
            with self.subTest(sharing=phrase):
                self.assertIn(phrase, sharing)
        for phrase in ("Just before the DSN is written, a read that can't reach the canvas",
                       "a read that reaches a canvas it doesn't find private is ERR-25: write no DSN"):
            with self.subTest(phrase):
                self.assertIn(phrase, canvas)
        self.assertIn("ERR-16 to ERR-25", rules)
        self.assertIn("copied into a new private canvas", rules)
        self.assertIn("A canvas a read states isn't private, or whose sharing its plain read doesn't state, stops the run "
                      "(ERR-25)", skill)
        # The build's reviewers on 160c916: a read with paths doesn't reliably state sharing (SPEC-017 §5).
        for phrase in ("a plain read that reaches the canvas and states no sharing",
                       "A read with `paths` stops the run only when it states that the canvas isn't private"):
            with self.subTest(plain=phrase):
                self.assertIn(phrase, canvas)
        # Codex on #158 at a97a928 (#153 item 38; Bryan, 2026-11-06: "I agree as it sounds broken"): an amend run's
        # line names the canvas that stopped the run whenever it isn't the DSN's.
        err25 = re.split(r"- \*\*ERR-", problems)[0]
        for phrase in ("/devforgeai:ui BRN-NNN <canvas URL>",
                       "ask the owner to make it private, or run again with that line and accept the copy",
                       "check the canvas page's Share menu and run again with that line",
                       "in an amend run, with `/devforgeai:ui BRN-NNN` when the canvas that stopped the run is the DSN's "
                       "canvas, and with `/devforgeai:ui BRN-NNN <canvas URL>`, the URL of the canvas that stopped it, when "
                       "it isn't (a canvas the request named, or a copy made in the run)"):
            with self.subTest(next_step=phrase):
                self.assertIn(phrase, err25)
        self.assertIn("could not be reached just before the write", rules)
        self.assertIn("ERR-25's message names the canvas, who can open it and what the user can do", rules)

    def test_the_v5_fixes(self):
        """SPEC-017 v5's smaller fixes (#153 items 5, 19, 20, 29; reads (d) and (e) of BEH-29)."""
        texts = {str(name): " ".join(text.split()) for name, text in skill_texts().items()}
        canvas = next(text for name, text in texts.items() if name.endswith("canvas.md"))
        rules = next(text for name, text in texts.items() if name.endswith("output-rules.md"))
        skill = " ".join((SKILL / "SKILL.md").read_text().split())
        boards = next(text for name, text in texts.items() if name.endswith("boards.md"))
        err20 = re.search(r"- \*\*ERR-20\*\*(.*?)- \*\*ERR-21\*\*", canvas).group(1)
        err23 = re.search(r"- \*\*ERR-23\*\*(.*?)- \*\*ERR-25\*\*", canvas).group(1)
        for name, text, phrase in (
                ("ERR-20's account hint", err20, "signed in to the account that owns it"),
                ("restart from the plain read", canvas, "start over once, from step 0, then ERR-21"),
                ("read (d)", canvas, "just before each question that asks to add to an existing canvas"),
                ("read (d) failing", err23, "the plain read before a question to add to it finds no canvas, fails or returns a summary instead of the canvas's statement"),
                ("boards.md's step 1", boards, "the import's `canvas.json` read (canvas.md, step 1)"),
                ("the statement's subject", canvas, "A statement by the tool about this canvas's sharing counts the same on any other read"),
                ("another person's summary", canvas, "returns a summary instead of the canvas's statement is ERR-23"),
                ("the retry", canvas, "one more plain read and one retry, without asking the question again"),
                ("ERR-23's briefs", err23, "show the briefs, when the run has any"),
                ("the Contents", canvas, "- The plain read and the canvas's sharing (BEH-29, ERR-25) - The question before an addition")):
            with self.subTest(name):
                self.assertIn(phrase, text)
        self.assertNotIn("step 1's read", boards)

    def test_the_copy_of_another_persons_canvas(self):
        """SPEC-017 v5 BEH-30 (Bryan, 2026-11-06: "give an option to import into current accounts canvas as new. If
        user refuses, refuse the shared canvas"; "Yes, exactly that (Recommended)")."""
        texts = {str(name): " ".join(text.split()) for name, text in skill_texts().items()}
        canvas = next(text for name, text in texts.items() if name.endswith("canvas.md"))
        rules = next(text for name, text in texts.items() if name.endswith("output-rules.md"))
        skill = " ".join((SKILL / "SKILL.md").read_text().split())
        self.assertIn("- Copying another person's canvas (BEH-30)", canvas)
        copy = re.search(r"## Copying another person's canvas \(BEH-30\)(.*?)## ", canvas).group(1)
        for phrase in ("belongs to <owner>, and others can open it. Copy its boards into a new private canvas on your "
                       "account and use that?", '"Copy into a new private canvas" (Recommended)', '"Don\'t use this canvas"',
                       "states that it is not private", "A summary instead of the file", "ERR-12", "ERR-06",
                       "the session's scratchpad", "(copied from <URL>)", "must find it private",
                       "counts as a change", "proceed without questions",
                       "the import question isn't asked",
                       "every later read in the run, the one just before the DSN included, reads the copy",
                       "before anything else is published to it"):
            with self.subTest(phrase):
                self.assertIn(phrase, copy)
        self.assertIn("BEH-30", skill)
        self.assertIn("whether to copy another person's shared canvas", skill)
        steps = re.search(r"\*\*The steps\.\*\*(.*?)## ", canvas).group(1)
        self.assertIn("each board's digest must equal the sha256 the source read noted for it", steps)
        self.assertIn("compared by its board keys and their order", steps)
        self.assertIn("a copy that replaced the DSN's canvas (BEH-30)", rules)
        interview = next(text for name, text in texts.items() if name.endswith("interview.md"))
        self.assertIn("the offer of a copy of another person's shared canvas", interview)
        self.assertRegex(skill, r"### 4\. Canvas \([^)]*ERR-25\)")
        # The build's reviewers on 780e20a (Bryan, 2026-11-06: "Check only right after (Recommended)").
        copy_section = re.search(r"## Copying another person's canvas \(BEH-30\)(.*?)## ", canvas).group(1)
        for name, text, phrase in (
                ("every source read exempt", copy_section, "Every read of the source in this section"),
                ("the check only right after", steps, "When the import directly follows a copy (BEH-30), before anything is added to it"),
                ("an addition skips it", steps, "an import after an addition to the copy skips that check"),
                ("the rerun after read (e)", canvas, "after a stop at the plain read of a canvas the run just made"),
                ("the briefs at ERR-25", canvas, "show the briefs, when the run has any"),
                ("the resume line after a copy", canvas, "after a copy, `/devforgeai:ui BRN-NNN <the copy's URL>`"),
                ("a new canvas's report", canvas, "Say nothing about a canvas the user owns in the replies or the report, except the canvas report of a canvas the run made"),
                ("step 5's triggers", skill, "or after the yes to a copy in an amend run (BEH-30)"),
                ("route C after a copy", skill, "after a copy, the import question isn't asked"),
                ("rule 5's scratchpad", skill, "the files a copy's reads save")):
            with self.subTest(name):
                self.assertIn(phrase, text)
        # Codex on #157 (Bryan, 2026-11-06: "Fix it, as the import does (Recommended)"): the copy's reads of its
        # source agree on one version, or the run reads again once, then stops at ERR-21.
        err21 = re.search(r"- \*\*ERR-21\*\*(.*?)(?=- \*\*ERR-|$)", canvas).group(1)
        for name, text, phrase in (
                ("canvas.json's version", copy_section, "`project/canvas.json` with `paths` and `out_dir` the session's "
                 "scratchpad, never the repository, noting the result's version identifier"),
                ("each board read's version", copy_section, "noting each file's sha256 and each result's version identifier"),
                ("one more read, no new question", copy_section, "read `canvas.json` and the boards again once, without "
                 "asking again (ERR-20, ERR-12 and ERR-06 still apply), then ERR-21"),
                ("nothing published first", copy_section, "nothing is published to the new canvas before these reads agree"),
                ("ERR-21 names the copy", err21, "a copy's reads of its source don't agree twice running (BEH-30)"),
                ("ERR-21's rerun after a copy", err21, "the line to run again names the source's URL")):
            with self.subTest(name):
                self.assertIn(phrase, text)

    def test_the_plain_read_is_in_the_steps(self):
        skill = (SKILL / "SKILL.md").read_text()
        for number in ("2", "4", "5", "7", "10"):
            step = re.search(rf"^### {number}\. .*$", skill, re.M).group(0)
            with self.subTest(step=number):
                self.assertIn("BEH-29", step)

    def test_the_consent_question_tells_the_truth(self):
        """SPEC-017 v5 (#153; Bryan, 2026-11-06: "Skill refuses shared canvases"): an addition asks its own question
        after a plain read made just before it, only to a canvas that read finds private, and offers 'Add to the
        canvas', never 'Create the canvas'."""
        skill = (SKILL / "SKILL.md").read_text()
        rule = " ".join(re.search(r"^5\. \*\*Write only the DSN.*?(?=^\S)", skill, re.M | re.S).group(0).split())
        step4 = " ".join(re.search(r"^### 4\. .*?(?=^### )", skill, re.M | re.S).group(0).split())
        for phrase in ("a private copy of another person's shared canvas", "an addition goes only to a canvas a read found private"):
            with self.subTest(rule=phrase):
                self.assertIn(phrase, rule)
        self.assertIn("whether to create the canvas or add to it", " ".join(skill.split()))
        for phrase in ("Add the boards made from these briefs to the canvas <URL>?", '"Add to the canvas" (Recommended)',
                       "saying whose canvas it is and that only its owner and the people given access can open it"):
            with self.subTest(step4=phrase):
                self.assertIn(phrase, step4)
        canvas = " ".join(next(text for name, text in skill_texts().items()
                               if str(name).endswith("canvas.md")).split())
        question = re.search(r"\*\*The question before an addition\.\*\*(.*?)## ", canvas).group(1)
        for phrase in ("after the plain read made just before it", "doesn't find private is ERR-25",
                       "only the user and the people given access can open it", "whose canvas it is",
                       'Never "as a private artifact" on the user\'s account', '"Add to the canvas" (Recommended)'):
            with self.subTest(question=phrase):
                self.assertIn(phrase, question)
        self.assertNotIn("Create the canvas", question)
        addition = re.search(r"## Adding a flow or a screen in an amend run(.*?)## ", canvas).group(1)
        self.assertIn('the question for an addition ("The question before an addition")', addition)

    def test_every_behaviour_and_error_is_cited(self):
        doc = spec_document(spec_text())
        text = " ".join(skill_texts().values())
        cited = set(re.findall(r"\b(?:BEH|ERR)-\d\d\b", text)) | NOT_BUILT
        for prefix, first, last in re.findall(r"\b(BEH|ERR)-(\d\d) to (?:BEH|ERR)-(\d\d)\b", text):  # "BEH-05 to BEH-08"
            cited |= {f"{prefix}-{n:02d}" for n in range(int(first), int(last) + 1)}
        for key in ("behaviors", "errors"):
            for item in doc[key]:
                with self.subTest(item["id"]):
                    self.assertIn(item["id"], cited)


    def test_the_reviews_fixes_stay(self):
        # The version 1 build's review fixes that version 2 keeps (C1, S1 to S12, the later passes): each phrase
        # guards a VER grader or an error a reviewer found missing.
        text = re.sub(r"\s+", " ", " ".join(skill_texts().values()))
        for phrase in ("never `not a screen` on the skill's own judgement",   # C1: VER-02 and VER-03
                       "never extract an ID from a path",                      # S1: ERR-02, VER-14
                       "no candidate is put to the user",                      # S4: VER-38
                       "a request to update or amend that names no specific change counts as none",  # S9: VER-33
                       "126 or 127",                                           # S12: ERR-14 for every subcommand
                       "Exit 1 is ERR-06",                                     # S12: head
                       "## The report",                                        # S10
                       "N markers left",                                       # N5
                       "already `approved`",                                   # N13
                       "which may be followed by the approver's name",  # VER-34/36: the approver is not ERR-02's string
                       "Approve <ID> now? Reply 'approve <ID>' with your name, or 'not now'.",  # offer before Next step
                       "is never put into a command unquoted",                 # A1a: a board name is untrusted data
                       "an existing item's mapping the request doesn't state stays as it is",  # R1/C1: proceed without questions, amend run
                       "each `'` in the name is written `'\\''`",                # S3: a quote in a board name
                       "read the `ideas` block line by line",                  # A6: ERR-09
                       "`Flows: unconfirmed (<count>)`",                       # A10
                       "ERR-03 to ERR-06 or ERR-12",                           # R5: the pre-check's ERR-NN line
                       "A step order the request states",                      # the shared prompt: "in that order" is confirmed
                       "the request to record the canvas is the answer",       # BEH-26 under proceed without questions
                       "`place` takes no board name at all",                   # IF-05: names are read from the digest file
                       "or when the boards are copied into the folder again by hand",  # ERR-17 reply: VER-33's stale text and v2's
                       "`files not placed:`",                                  # ERR-21: a move that fails partway
                       "`<hex> canvas.json`",                                  # the digest file's lines: the key, no project/ (squashed)
                       "Import the canvas at <new URL>, which replaces <old URL>?",  # a different URL asks with the import question
                       "the digest file was rejected"):                        # ERR-14 when place exits 2 naming the file
            with self.subTest(phrase):
                self.assertIn(phrase, text)


class References(unittest.TestCase):
    def test_skill_md_links_each_reference_and_none_links_another(self):
        skill_md = (SKILL / "SKILL.md").read_text()
        for name in REFERENCES:
            with self.subTest(name):
                self.assertIn(f"](references/{name})", skill_md)
                text = (SKILL / "references" / name).read_text()
                self.assertNotRegex(text, r"\]\([^)]*\.md", "a reference links another file")
                self.assertNotRegex(text, r"\breferences/", "a reference names the references folder")

    def test_a_long_reference_starts_with_a_contents_list(self):
        for name in REFERENCES:
            with self.subTest(name):
                lines = (SKILL / "references" / name).read_text().splitlines()
                self.assertLessEqual(len(lines), 500)
                if len(lines) > 100:
                    self.assertEqual(lines[0][:2], "# ")
                    self.assertEqual(lines[2], "## Contents")

    def test_briefs_md_holds_dm_05(self):
        text = (SKILL / "references/briefs.md").read_text()
        order = ["1. Lead line", "2. Context", "3. Content", "4. Must-haves", "5. Style", "6. Closing line"]
        self.assertEqual([part.split(". ")[1] for part in order], BRIEF_PARTS)
        positions = [text.index(part) for part in order]
        self.assertEqual(positions, sorted(positions))
        # The shape, a terminal flow's worked example and a web flow's: the closing line is exact in each.
        self.assertGreaterEqual(text.count(CLOSING_LINE), 3)
        self.assertNotIn("<!--", text)                                # a brief holds no HTML comment
        self.assertNotRegex(text, r"#[0-9a-fA-F]{6}\b")               # nor a hex value
        squashed = re.sub(r"\s+", " ", text)
        for phrase in ("describes the problem and never prescribes the solution", "propose one",
                       "monospace cell grid", "one brief for each confirmed flow", "never invented"):
            with self.subTest(phrase):
                self.assertIn(phrase, squashed)

    def test_canvas_md_holds_the_canvas_and_the_import(self):
        text = re.sub(r"\s+", " ", (SKILL / "references/canvas.md").read_text())
        for phrase in ("project/canvas.json", "at most 4", "out_dir", "--sha-file", "sha256", "title1", "<a href",
                       "is_interactive", "scratchpad", "flat", "version identifier", "Import the canvas now",
                       "Use the copy as it is", "Draw ", "ERR-19", "ERR-20", "ERR-21", "ERR-23", "Next step"):
            with self.subTest(phrase):
                self.assertIn(phrase, text)

    def test_output_rules_ends_with_the_self_check_list(self):
        text = (SKILL / "references/output-rules.md").read_text()
        tail = text.split("## Self-check list")[-1]
        self.assertGreaterEqual(len(re.findall(r"(?m)^\d+\. ", tail)), 5)
        self.assertNotIn("\n## ", tail)


class Template(unittest.TestCase):
    def setUp(self):
        self.raw = (SKILL / "assets/dsn.md").read_text()
        self.doc = spec_document(filled_template())

    def test_frontmatter_keys_are_dm_01s_in_order(self):
        self.assertEqual(list(self.doc["frontmatter"]), DSN_KEYS)
        self.assertEqual(self.doc["frontmatter"]["type"], "design")
        self.assertEqual(self.doc["frontmatter"]["status"], "draft")

    def test_headings_are_dm_01s_in_order(self):
        fixed = re.findall(r"(?m)^\| `(## [^`]+)` \|", spec_section(4))
        self.assertEqual(len(fixed), 6)
        text = re.sub(r"<!--.*?-->", "", self.raw, flags=re.S)
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        self.assertEqual([l.rstrip() for l in text.splitlines() if re.match(r"^##(?!#)\s", l)], fixed)

    def test_section_4_and_the_comments_say_import_not_copy_by_hand(self):
        # SPEC-017 §11: the version 1 prose ('the user copies the boards', 'never fetches') is replaced.
        for stale in ("never fetches", "copies the boards", "the user gave"):
            with self.subTest(stale):
                self.assertNotIn(stale, self.raw)
        self.assertIn("imported", self.raw)

    def test_boards_block_and_tables(self):
        self.assertEqual(self.raw.count("```yaml items\nboards:\n"), 1)
        self.assertEqual(list(self.doc["boards"][0]), BOARD_FIELDS)
        self.assertIn("| Idea | Boards | Status |", self.raw)
        self.assertIn("| Version | Date | Author | Change | Items affected |", self.raw)

    def test_filled_in_template_validates_against_design_schema(self):
        text = filled_template()
        for left in ("<!--", "YYYY", "-000"):
            self.assertNotIn(left, text)
        doc = spec_document(re.sub(r"\[\[fill: [^\]]+\]\]", "sample", text))
        self.assertEqual(errors("design.schema.json", doc), [])

    def test_the_schema_check_is_not_vacuous(self):
        bad = copy.deepcopy(self.doc)
        bad["frontmatter"]["id"] = "DSN-1"
        bad["frontmatter"]["status"] = "ready"
        bad["frontmatter"]["boards_root"] = "docs/specs/design/DSN-001/"
        bad["boards"][0]["file"] = "a/b"
        bad["boards"][0]["surface"] = "cli"
        self.assertEqual(len(errors("design.schema.json", bad)), 5)

    def test_only_fill_placeholders_never_in_backticks(self):
        self.assertIn("[[fill: ", self.raw)
        self.assertNotRegex(self.raw, r"\bTODO\b|\bTBD\b")
        self.assertEqual(len(re.findall(r"\[\[fill:", self.raw)), len(re.findall(r"\[\[fill: [^\]]+\]\]", self.raw)))
        self.assertNotRegex(without_code(re.sub(r"<!--.*?-->", "", self.raw, flags=re.S)), r"<[^>\n]+>")
        for span in re.findall(r"(`+)(.+?)\1", self.raw):
            self.assertNotIn("[[fill:", span[1])
        # Inside the yaml fence only # comments can stand (an HTML comment there would break the block).
        for block in re.findall(r"```yaml items\n(.*?)```", self.raw, re.S):
            self.assertNotIn("<!--", block)
            self.assertNotIn("[[fill:", block)


class Generic(unittest.TestCase):
    def test_no_machine_paths_or_names(self):
        for name, text in skill_texts().items():
            with self.subTest(name):
                self.assertNotRegex(text, r"(?<![\w.~$}])/(home|Users|tmp|mnt|root|var|opt)/")
                self.assertNotIn("/home/", text)
                self.assertNotRegex(text, r"\b[A-Z]:\\")
                self.assertNotRegex(text, r"(?i)\b(bryan|krepion|omniwatch|cmux|worker1|devforgeai-worker)\b")


class Spec(unittest.TestCase):
    def test_spec_validates_and_every_item_is_covered(self):
        doc = spec_document(spec_text())
        self.assertEqual(errors("spec.schema.json", doc), [])
        self.assertEqual((doc["frontmatter"]["version"], doc["frontmatter"]["status"]), (SPEC_VERSION, "in-review"))
        covered = {c for v in doc["verifications"] for c in v.get("covers", [])}
        for key in ("behaviors", "errors", "quality_responses"):
            for item in doc[key]:
                with self.subTest(item["id"]):
                    self.assertIn(item["id"], covered)
        for item in ("IF-01", "IF-02", "IF-03", "IF-04", "IF-05"):
            self.assertIn(item, covered)


if __name__ == "__main__":
    unittest.main()
