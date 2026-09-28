#!/usr/bin/env python3
"""Tests for archive_session.py (SPEC-005). Each test drives the script the way Claude Code does:
a subprocess with the hook's JSON on stdin. Run: python3 -m unittest test_archive_session -v"""
import concurrent.futures
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "archive_session.py")


def entry(kind, text, ts="2026-09-27T10:00:00Z"):
    return json.dumps({"type": kind, "timestamp": ts,
                       "message": {"role": kind, "content": [{"type": "text", "text": text}]}})


class ArchiveTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = self.tmp.name
        self.root = os.path.join(base, "archive")
        self.project = os.path.join(base, "Projects", "DevForgeAI")
        self.other = os.path.join(base, "Projects", "Other")
        os.makedirs(os.path.join(self.project, "docs", "specs", "brainstorm"))
        os.makedirs(self.other)
        self.tdir = os.path.join(base, "claude", "projects", "-Projects-DevForgeAI")
        os.makedirs(self.tdir)
        os.makedirs(self.root)
        with open(os.path.join(self.root, "config.json"), "w") as f:
            json.dump({"include_prefixes": [self.project], "retention_days": None}, f)
        self.env = {**os.environ, "CLAUDE_ARCHIVE_DIR": self.root}

    def tearDown(self):
        self.tmp.cleanup()

    def transcript(self, sid, lines):
        path = os.path.join(self.tdir, f"{sid}.jsonl")
        with open(path, "w") as f:
            f.write("\n".join(lines) + "\n")
        return path

    def run_script(self, *args, stdin=""):
        return subprocess.run([sys.executable, SCRIPT, *args], input=stdin, env=self.env,
                              capture_output=True, text=True, timeout=30)

    def hook(self, sub, payload):
        r = self.run_script(sub, stdin=json.dumps(payload) if not isinstance(payload, str) else payload)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout, "", "hooks must print nothing")
        return r

    def db(self):
        return sqlite3.connect(os.path.join(self.root, "archive.db"))

    def end(self, sid, path, cwd=None, event="SessionEnd", **extra):
        return {"session_id": sid, "transcript_path": path, "cwd": cwd or self.project,
                "hook_event_name": event, **extra}

    # VER-01: archive copies the transcript, records it, and makes it searchable; path finds it.
    def test_archive_copies_indexes_and_resolves_path(self):
        src = self.transcript("s1", [entry("user", "Park IDEA-02 instead, we have no budget"),
                                     entry("assistant", "Recorded IDEA-02 as parked.")])
        self.hook("archive", self.end("s1", src, reason="prompt_input_exit"))
        dst = os.path.join(self.root, "transcripts", "-Projects-DevForgeAI", "s1.jsonl")
        with open(src, "rb") as a, open(dst, "rb") as b:
            self.assertEqual(a.read(), b.read())
        row = self.db().execute("SELECT cwd, archive_path, last_reason, indexed_lines, index_error "
                                "FROM sessions WHERE session_id='s1'").fetchone()
        self.assertEqual(row, (self.project, dst, "prompt_input_exit", 2, None))
        r = self.run_script("search", "IDEA-02")
        self.assertEqual(r.returncode, 0)
        self.assertIn("s1", r.stdout)
        self.assertIn("[IDEA-02]", r.stdout)    # snippet() brackets the matched phrase
        self.assertEqual(self.run_script("path", "s1").stdout.strip(), dst)
        self.assertEqual(os.stat(dst).st_mode & 0o777, 0o600)
        self.assertEqual([n for n in os.listdir(os.path.dirname(dst)) if n.endswith(".tmp")], [])

    # VER-02: an unchanged transcript is not copied again; a grown one is re-copied and re-indexed.
    def test_unchanged_is_skipped_and_growth_is_recopied(self):
        src = self.transcript("s2", [entry("user", "first message")])
        self.hook("archive", self.end("s2", src, event="Stop"))
        first = self.db().execute("SELECT last_archived, sha256 FROM sessions").fetchone()
        dst = os.path.join(self.root, "transcripts", "-Projects-DevForgeAI", "s2.jsonl")
        mtime = os.stat(dst).st_mtime_ns
        time.sleep(1.1)
        self.hook("archive", self.end("s2", src, event="Stop"))
        self.assertEqual(os.stat(dst).st_mtime_ns, mtime, "unchanged transcript was copied again")
        self.assertEqual(self.db().execute("SELECT last_archived FROM sessions").fetchone()[0], first[0])
        with open(src, "a") as f:
            f.write(entry("assistant", "second message about magnets") + "\n")
        self.hook("archive", self.end("s2", src, event="Stop"))
        row = self.db().execute("SELECT sha256, indexed_lines FROM sessions").fetchone()
        self.assertNotEqual(row[0], first[1])
        self.assertEqual(row[1], 2)
        self.assertIn("s2", self.run_script("search", "magnets").stdout)

    # VER-03: a malformed line is skipped; the copy, the row and the other lines survive.
    def test_malformed_line_does_not_lose_the_session(self):
        src = self.transcript("s3", [entry("user", "alpha request"), '{"type": "assistant", "mess',
                                     entry("assistant", "omega answer")])
        self.hook("archive", self.end("s3", src))
        row = self.db().execute("SELECT indexed_lines, skipped_lines, index_error FROM sessions").fetchone()
        self.assertEqual(row, (2, 1, None))
        self.assertIn("s3", self.run_script("search", "omega").stdout)

    # VER-04: sessions outside include_prefixes, and every session when no config exists, are ignored.
    def test_scope_is_opt_in(self):
        src = self.transcript("s4", [entry("user", "private stuff")])
        self.hook("archive", self.end("s4", src, cwd=self.other))
        os.remove(os.path.join(self.root, "config.json"))
        self.hook("archive", self.end("s4", src))
        self.assertFalse(os.path.exists(os.path.join(self.root, "transcripts")))
        count = self.db().execute("SELECT count(*) FROM sessions").fetchone()[0] if \
            os.path.exists(os.path.join(self.root, "archive.db")) else 0
        self.assertEqual(count, 0)

    # VER-05: a Write to docs/specs/ records session, document ID and version; other paths don't.
    def test_record_write_maps_documents_to_sessions(self):
        doc = os.path.join(self.project, "docs", "specs", "brainstorm", "BRN-001.md")
        with open(doc, "w") as f:
            f.write('---\nid: BRN-001\ntype: brainstorm\ntitle: "x"\nstatus: draft\nversion: 2\n---\n# BRN-001\n')
        base = {"session_id": "s5", "cwd": self.project, "hook_event_name": "PostToolUse"}
        self.hook("record-write", {**base, "tool_name": "Write", "tool_use_id": "t1",
                                   "tool_input": {"file_path": doc}})
        self.hook("record-write", {**base, "tool_name": "Write", "tool_use_id": "t1",
                                   "tool_input": {"file_path": doc}})           # same call again: ignored
        self.hook("record-write", {**base, "tool_name": "Edit", "tool_use_id": "t2",
                                   "tool_input": {"file_path": os.path.join(self.project, "README.md")}})
        rows = self.db().execute("SELECT session_id, rel_path, tool, doc_id, doc_version FROM doc_writes").fetchall()
        self.assertEqual(rows, [("s5", os.path.join("docs", "specs", "brainstorm", "BRN-001.md"), "Write",
                                 "BRN-001", "2")])
        r = self.run_script("writes", "BRN-001")
        self.assertEqual(r.returncode, 0)
        self.assertIn("v2", r.stdout)
        self.assertIn("s5", r.stdout)

    # VER-06: bad input never fails the session: exit 0, nothing printed, the problem logged.
    def test_hooks_fail_open(self):
        self.hook("archive", "not json at all")
        self.hook("archive", self.end("s6", os.path.join(self.tdir, "missing.jsonl")))
        self.hook("record-write", "[1, 2, 3]")
        with open(os.path.join(self.root, "hook-errors.log")) as f:
            log = f.read()
        self.assertIn("archive:", log)
        self.assertIn("transcript not found", log)
        self.assertIn("record-write:", log)

    # VER-07: ten sessions archiving at once all land (WAL + busy timeout).
    def test_concurrent_archives(self):
        paths = {f"c{i}": self.transcript(f"c{i}", [entry("user", f"concurrent message {i}")]) for i in range(10)}
        with concurrent.futures.ThreadPoolExecutor(10) as pool:
            results = list(pool.map(lambda kv: self.run_script(
                "archive", stdin=json.dumps(self.end(kv[0], kv[1], event="Stop"))), paths.items()))
        self.assertTrue(all(r.returncode == 0 for r in results))
        self.assertEqual(self.db().execute("SELECT count(*) FROM sessions").fetchone()[0], 10)
        self.assertFalse(os.path.exists(os.path.join(self.root, "hook-errors.log")))

    # VER-08: reindex rebuilds the text index from the archived files; prune honours retention_days.
    def test_reindex_and_prune(self):
        src = self.transcript("s8", [entry("user", "zebra crossing")])
        self.hook("archive", self.end("s8", src))
        with self.db() as db:
            db.execute("DELETE FROM messages_fts")
        self.assertEqual(self.run_script("search", "zebra").returncode, 1)
        self.assertEqual(self.run_script("reindex").returncode, 0)
        self.assertIn("s8", self.run_script("search", "zebra").stdout)
        self.assertIn("nothing pruned", self.run_script("prune").stdout)
        with open(os.path.join(self.root, "config.json"), "w") as f:
            json.dump({"include_prefixes": [self.project], "retention_days": 30}, f)
        with self.db() as db:
            db.execute("UPDATE sessions SET last_archived = '2000-01-01T00:00:00+00:00'")
        self.assertIn("pruned 1", self.run_script("prune").stdout)
        self.assertEqual(self.run_script("path", "s8").returncode, 1)
        self.assertFalse(os.path.exists(os.path.join(self.root, "transcripts", "-Projects-DevForgeAI", "s8.jsonl")))


if __name__ == "__main__":
    unittest.main()
