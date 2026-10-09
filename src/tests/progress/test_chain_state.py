"""Tests for SPEC-012 version 17's chain listing (src/claude/DevForgeAI/progress/chain_state.py), VER-50.

ChainRules checks IF-03, BEH-26, ERR-13 and ERR-14 on fixture trees built in a temporary folder, with the exact JSON
asserted and validated against DM-05. ChainRulesUnderS runs every test with the script under `python3 -S` (QR-05).
Each spawn uses -B, so no __pycache__ lands in the plugin folder, which deploys.

Run from the repository root:
    PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider src/tests/progress
"""
import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import script_fixtures as fx  # noqa: E402

SPEC = "docs/specs/"


def doc(**keys):
    """Frontmatter lines for a key order of the test's choosing, then a body whose lines must never be read."""
    return "---\n" + "".join("%s: %s\n" % kv for kv in keys.items()) + "---\n# Body\nid: BODY-NEVER\nstatus: body\n"


def entry(id, type, status, version, updated, path, upstream=()):
    return {"id": id, "type": type, "status": status, "version": version, "updated": updated, "path": path,
            "upstream": list(upstream)}


FLOW_SPEC = """---
id: SPEC-012
type: spec
status: approved       # draft | in-review | approved | superseded | deprecated
version: 18
created: 2026-10-02
updated: 2026-10-08
generated_by:
  tool: "claude-code"
  id: NESTED-ID
upstream:
  - {id: ADR-002, relation: constrains, version: 2, hash: null, note: "the workflow chain's order"}
  - {id: PRD-001, item: FR-003, relation: informed_by, version: 12, hash: null}
  - {id: PRD-001, item: FR-004, relation: informed_by, version: 12, hash: null}
  # a comment between the entries
  - {id: SPEC-001, item: VER-02, relation: informed_by, version: 17, hash: null}
supersedes: []
---
# SPEC-012
"""

BLOCK_SPEC = """---
id: SPEC-013
type: spec
status: in-review
version: 25
updated: 2026-10-08
upstream:
  - id: SPEC-012
    relation: constrains
    version: 18

  - id: ADR-006
    relation: constrains
# a comment at column 0 inside the list
  - id: ADR-002
blocked_by: []
---
"""

COLUMN_ZERO_ITEMS = """---
id: ADR-003
type: adr
status: accepted
version: 2
updated: 2026-09-30
upstream:
- id: SPEC-012
- {id: ADR-001, relation: x}
authors: ["a"]
---
"""


class Base(unittest.TestCase):
    INTERPRETER = (sys.executable, "-B")

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "project"
        self.root.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def chain(self, *args, root=None):
        args = list(args) if args else ["--root", root or self.root]
        return fx.run_script(fx.CHAIN_STATE, args, self.INTERPRETER)

    def listing(self, root=None):
        proc = self.chain(root=root)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stderr, "")
        return json.loads(proc.stdout)

    def tree(self):
        """The fixture tree of VER-50: every shape of document the spec names, listed or left out."""
        write = lambda rel, text, mode="w": fx.write(self.root, SPEC + rel, text, mode)  # noqa: E731
        write("brainstorm/BRN-001.md", doc(id="BRN-001", type="brainstorm", status="converged", version="2",
                                           updated="2026-10-01", upstream="[]"))
        write("prd/PRD-001.md", "---\nid: PRD-001\ntype: prd\ntitle: \"A title: with a colon\"\nstatus: approved\n"
                                "version: 12\nupdated: 2026-10-07\nupstream:\n  - id: BRN-001\n    relation: informed_by\n"
                                "  - id: BRN-001\n    relation: informed_by\n---\n")
        write("spec/SPEC-012.md", FLOW_SPEC)
        write("spec/SPEC-013.md", BLOCK_SPEC)
        write("adr/ADR-003.md", COLUMN_ZERO_ITEMS)
        write("adr/ADR-001.md", doc(id="ADR-001", type="adr", status="accepted", version="1", updated="2026-09-26",
                                    upstream="[]"))
        write("adr/ADR-002.md", "---\nid: ADR-002\ntype: adr\nstatus: in-review       # draft | in-review | accepted\n"
                                "version: 3\nupdated: 2026-10-01 # the date\n---\n")
        write("arch/ARCH-001.md", "---\nid: \"ARCH-001\"\ntype: 'arch'\nstatus: 'draft'\nversion: \"3\"\n"
                                  "updated: \"2026-10-02\"\n---\n")
        write("spec/SPEC-020.md", doc(id="SPEC-020", type="spec", status="draft", version="1.2", updated="2026-10-08"))
        write("epic/sub/deeper/EPIC-001.md", doc(id="EPIC-001", type="epic", status="approved", version="4",
                                                 updated="2026-10-02"))
        write("misc/NOTYPE-001.md", "---\nid: NOTYPE-001\n---\n")
        write("misc/CRLF-001.md", b"---\r\nid: CRLF-001\r\ntype: policy\r\nstatus: approved\r\nversion: 2\r\n---\r\nid: no\r\n",
              "wb")
        write("misc/notes.txt", "---\nid: TXT-001\n---\n")
        # Left out, each counted in skipped.
        write("devforgeai-dashboard.md", "# A design proposal with no frontmatter and no ID\n")
        write("spec/never-closes.md", "---\nid: OPEN-001\ntype: spec\nstatus: draft\n")
        write("spec/no-id.md", doc(type="spec", status="draft"))
        write("spec/empty-id.md", "---\nid:\ntype: spec\n---\n")
        write("spec/blank-first.md", "\n---\nid: BLANK-001\n---\n")
        write("spec/empty.md", "")
        write("spec/binary.md", b"---\nid: BIN-001\ntitle: \xff\xfe\n---\n", "wb")
        outside = fx.write(Path(self._tmp.name), "outside/OUT-001.md", doc(id="OUT-001", type="spec", status="draft"))
        os.symlink(outside, self.root / SPEC / "spec/linked.md")
        os.symlink(outside.parent, self.root / SPEC / "linked-folder")


# Left out: the design proposal, never-closes, no-id, empty-id, blank-first, empty, binary, the link to a document
# and the link to a folder.
SKIPPED = 9

DOCUMENTS = [
    entry("NOTYPE-001", None, None, None, None, SPEC + "misc/NOTYPE-001.md"),
    entry("ADR-001", "adr", "accepted", 1, "2026-09-26", SPEC + "adr/ADR-001.md"),
    entry("ADR-002", "adr", "in-review", 3, "2026-10-01", SPEC + "adr/ADR-002.md"),
    entry("ADR-003", "adr", "accepted", 2, "2026-09-30", SPEC + "adr/ADR-003.md", ["SPEC-012", "ADR-001"]),
    entry("ARCH-001", "arch", "draft", 3, "2026-10-02", SPEC + "arch/ARCH-001.md"),
    entry("BRN-001", "brainstorm", "converged", 2, "2026-10-01", SPEC + "brainstorm/BRN-001.md"),
    entry("EPIC-001", "epic", "approved", 4, "2026-10-02", SPEC + "epic/sub/deeper/EPIC-001.md"),
    entry("CRLF-001", "policy", "approved", 2, None, SPEC + "misc/CRLF-001.md"),
    entry("PRD-001", "prd", "approved", 12, "2026-10-07", SPEC + "prd/PRD-001.md", ["BRN-001"]),
    entry("SPEC-012", "spec", "approved", 18, "2026-10-08", SPEC + "spec/SPEC-012.md",
          ["ADR-002", "PRD-001", "SPEC-001"]),
    entry("SPEC-013", "spec", "in-review", 25, "2026-10-08", SPEC + "spec/SPEC-013.md",
          ["SPEC-012", "ADR-006", "ADR-002"]),
    entry("SPEC-020", "spec", "draft", "1.2", "2026-10-08", SPEC + "spec/SPEC-020.md"),
]


class ChainRules(Base):
    """VER-50: the listing of documents under docs/specs/, BEH-26 and ERR-13."""

    def test_ver50_the_listing_is_exactly_what_the_frontmatters_say(self):
        self.tree()
        listing = self.listing()
        self.assertEqual(listing["format"], "devforgeai-chain/1")
        self.assertEqual(listing["documents"], DOCUMENTS)
        self.assertEqual(listing["skipped"], SKIPPED)
        self.assertEqual(sorted(listing), ["documents", "format", "skipped"])
        validator = Draft202012Validator(json.loads((fx.SCHEMAS / "chain.schema.json").read_text(encoding="utf-8")))
        self.assertEqual([e.message for e in validator.iter_errors(listing)], [])

    def test_ver50_the_output_is_sorted_json_with_two_space_indentation_and_a_final_newline(self):
        self.tree()
        proc = self.chain()
        self.assertEqual(proc.stdout, json.dumps(json.loads(proc.stdout), sort_keys=True, indent=2,
                                                 ensure_ascii=False) + "\n")

    def test_ver50_a_trailing_comment_a_quote_and_a_version_like_1_2(self):
        self.tree()
        by_id = {d["id"]: d for d in self.listing()["documents"]}
        self.assertEqual(by_id["ADR-002"]["status"], "in-review")  # 'in-review       # draft | in-review | accepted'
        self.assertEqual(by_id["ADR-002"]["updated"], "2026-10-01")
        self.assertEqual(by_id["ARCH-001"]["version"], 3)  # "3" is all digits once the quote is gone
        self.assertEqual((by_id["ARCH-001"]["type"], by_id["ARCH-001"]["status"]), ("arch", "draft"))
        self.assertEqual(by_id["SPEC-020"]["version"], "1.2")  # text as written, not an integer or a float

    def test_ver50_upstream_ids_in_file_order_each_once_in_either_style(self):
        self.tree()
        by_id = {d["id"]: d for d in self.listing()["documents"]}
        self.assertEqual(by_id["SPEC-012"]["upstream"], ["ADR-002", "PRD-001", "SPEC-001"])  # flow style, a repeat
        self.assertEqual(by_id["SPEC-013"]["upstream"], ["SPEC-012", "ADR-006", "ADR-002"])  # block style, a comment
        self.assertEqual(by_id["ADR-003"]["upstream"], ["SPEC-012", "ADR-001"])  # items at column 0
        self.assertEqual(by_id["BRN-001"]["upstream"], [])  # upstream: []
        self.assertEqual(by_id["ADR-002"]["upstream"], [])  # no upstream key
        self.assertEqual(by_id["PRD-001"]["upstream"], ["BRN-001"])  # the same ID twice, once

    def test_ver50_only_the_frontmatter_is_read(self):
        self.tree()
        documents = self.listing()["documents"]
        self.assertNotIn("BODY-NEVER", [d["id"] for d in documents])
        self.assertTrue(all(d["status"] != "body" for d in documents))
        # A body that isn't UTF-8 after the closing line is never read, so the document still lists (QR-06).
        fx.write(self.root, SPEC + "spec/late-bytes.md", b"---\nid: LATE-001\ntype: spec\n---\n\xff\xfe\n", "wb")
        self.assertIn("LATE-001", [d["id"] for d in self.listing()["documents"]])

    def test_ver50_a_document_in_a_subfolder_is_listed_with_its_relative_path(self):
        self.tree()
        epic = next(d for d in self.listing()["documents"] if d["id"] == "EPIC-001")
        self.assertEqual(epic["path"], "docs/specs/epic/sub/deeper/EPIC-001.md")

    def test_ver50_files_left_out_are_counted_and_a_links_target_is_never_read(self):
        self.tree()
        listing = self.listing()
        ids = [d["id"] for d in listing["documents"]]
        for gone in ("OPEN-001", "BIN-001", "BLANK-001", "OUT-001", "TXT-001"):
            self.assertNotIn(gone, ids)
        self.assertEqual(listing["skipped"], SKIPPED)
        # Make the link's target unreadable: a script that opened it would fail or list it; neither happens.
        target = Path(self._tmp.name) / "outside/OUT-001.md"
        os.chmod(target, 0)
        try:
            again = self.listing()
        finally:
            os.chmod(target, 0o644)
        self.assertEqual(again, listing)

    def test_ver50_the_order_never_depends_on_the_order_the_files_were_made_in(self):
        self.tree()
        first = self.chain().stdout
        other = Path(self._tmp.name) / "other"
        other.mkdir()
        paths = sorted(p for p in (self.root / SPEC).rglob("*.md") if not p.is_symlink())
        # Rebuild the same tree in the reverse creation order, the links last.
        for path in reversed(paths):
            fx.write(other, path.relative_to(self.root).as_posix(), path.read_bytes(), "wb")
        outside = Path(self._tmp.name) / "outside"
        os.symlink(outside / "OUT-001.md", other / SPEC / "spec/linked.md")
        os.symlink(outside, other / SPEC / "linked-folder")
        self.assertEqual(self.chain(root=other).stdout, first)

    def test_ver50_no_docs_specs_is_an_empty_listing(self):
        for build in (lambda: None, lambda: (self.root / "docs").mkdir()):
            build()
            proc = self.chain()
            self.assertEqual((proc.returncode, proc.stderr), (0, ""))
            self.assertEqual(json.loads(proc.stdout), {"format": "devforgeai-chain/1", "documents": [], "skipped": 0})

    def test_ver50_errors_exit_2_with_nothing_on_stdout_and_one_line_on_stderr(self):
        a_file = self.root / "a-file"
        a_file.write_text("x\n")
        for args in ([], ["--root"], ["--root", self.root / "missing"], ["--root", a_file],
                     ["--root", self.root, "--bogus"], ["--bogus"], ["--root", self.root, "extra"]):
            with self.subTest(args=[str(a) for a in args]):
                proc = fx.run_script(fx.CHAIN_STATE, args, self.INTERPRETER)
                self.assertEqual(proc.returncode, 2, proc.stderr)
                self.assertEqual(proc.stdout, "")
                self.assertEqual(len(proc.stderr.splitlines()), 1, proc.stderr)
                self.assertTrue(proc.stderr.startswith("chain_state: "), proc.stderr)

    # The review of the build (tmp/plans/dashboard/review-build-028.md, S2): a version of 5,000 digits is all digits, but
    # no integer this script can hold under Python's default limit of 4,300 digits for int(); BEH-26 and DM-05 give
    # "the text" for a value that isn't an integer, so it is listed as the text as written, never a traceback.
    def test_ver50_a_version_too_long_for_an_integer_is_kept_as_text(self):
        fx.write(self.root, SPEC + "big.md", "---\nid: BIG-1\ntype: spec\nversion: %s\n---\n" % ("9" * 5000))
        fx.write(self.root, SPEC + "ok.md", "---\nid: OK-1\ntype: spec\nversion: 7\n---\n")
        env = dict(os.environ, PYTHONINTMAXSTRDIGITS="4300")  # the default, so the test doesn't depend on the host's
        proc = fx.run_script(fx.CHAIN_STATE, ["--root", self.root], self.INTERPRETER, env=env)
        self.assertEqual((proc.returncode, proc.stderr), (0, ""))
        listing = json.loads(proc.stdout)
        self.assertEqual({d["id"]: d["version"] for d in listing["documents"]}, {"BIG-1": "9" * 5000, "OK-1": 7})
        self.assertEqual(listing["skipped"], 0)

    # S3: a list line's ID is read from `{id: <ID>` or `- id: <ID>` at the line's start (BEH-26), never out of a quoted
    # note. The reviewer's probe up.md; an entry whose id is not first (`{relation: x, ..., id: SPEC-002}`) has neither
    # form, so it is not read (builder's reading, kept: BEH-26 names only those two forms).
    UP_MD = ('---\nid: UP-1\ntype: spec\nupstream:\n  - id: ADR-001\n    relation: constrains\n'
             '    note: "see also - id: ADR-999"\n  - {relation: x, note: "{id: EVIL-1}", id: SPEC-002}\n'
             'status: approved\n---\nbody\n')

    def test_ver50_upstream_ids_are_not_read_out_of_quoted_notes(self):
        fx.write(self.root, SPEC + "up.md", self.UP_MD)
        (up,) = self.listing()["documents"]
        self.assertEqual(up["upstream"], ["ADR-001"])

    def test_ver50_upstream_lines_that_have_neither_form_are_not_read(self):
        text = ("---\nid: UP-2\ntype: spec\nupstream:\n"
                "  - {id: A-1, relation: x, note: \"- id: NOTE-1 and {id: NOTE-2}\"}\n"
                "# - id: COMMENT-1\n"
                "  - relation: informed_by\n    id: NOFIRST-1\n"
                "  -{id: A-2}\n"
                "- id: \"A-3\"\n"
                "  - {relation: x, id: NOFIRST-2}\n"
                "    note: \"x {id: INNER-1}\"\n"
                "---\n")
        fx.write(self.root, SPEC + "up2.md", text)
        (up,) = self.listing()["documents"]
        self.assertEqual(up["upstream"], ["A-1", "A-2", "A-3"])

    def test_ver50_the_listing_of_this_repositorys_specs(self):
        listing = self.listing(root=fx.ROOT)
        validator = Draft202012Validator(json.loads((fx.SCHEMAS / "chain.schema.json").read_text(encoding="utf-8")))
        self.assertEqual([e.message for e in validator.iter_errors(listing)], [])
        spec = (fx.ROOT / "docs/specs/spec/SPEC-012.md").read_text(encoding="utf-8")
        front = spec.split("\n---\n", 1)[0]
        version = int(re.search(r"^version: (\d+)", front, re.M).group(1))
        upstream = []
        for ident in re.findall(r"^\s*- \{id: ([A-Za-z0-9-]+)", front, re.M):
            if ident not in upstream:
                upstream.append(ident)
        mine = next(d for d in listing["documents"] if d["id"] == "SPEC-012")
        self.assertEqual((mine["version"], mine["upstream"], mine["type"]), (version, upstream, "spec"))
        self.assertEqual(mine["path"], "docs/specs/spec/SPEC-012.md")
        self.assertTrue(upstream, "SPEC-012's frontmatter names upstream IDs")
        # Sorted by type (null first), then id, then path, in the byte order of the text.
        keys = [(d["type"] is not None, (d["type"] or "").encode(), d["id"].encode(), d["path"].encode())
                for d in listing["documents"]]
        self.assertEqual(keys, sorted(keys))
        self.assertGreater(listing["skipped"], 0)  # docs/specs/devforgeai-dashboard.md and the other proposals


class ChainRulesUnderS(ChainRules):
    """Every ChainRules test with the script under python3 -S (QR-05)."""
    INTERPRETER = (sys.executable, "-S", "-B")


if __name__ == "__main__":
    unittest.main()
