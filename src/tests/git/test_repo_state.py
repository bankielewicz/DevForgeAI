"""SPEC-007 VER-16: repo_state.py on temporary repositories. Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s src/tests/git -p 'test_*.py'
"""
import contextlib
import io
import json
import os
import sys
import unittest
from unittest import mock

if __package__:
    from .gitfixture import SCRIPTS, Sandbox, tree_checksum
else:
    from gitfixture import SCRIPTS, Sandbox, tree_checksum

DAY = 86400


class RepoStateTest(unittest.TestCase):
    def setUp(self):
        self.sb = Sandbox()
        self.origin = self.sb.bare()
        seed = self.sb.repo("seed", origin=self.origin)
        self.sb.write(seed, "a.txt", "one\n")
        self.sb.write(seed, "b.txt", "bee\n")
        self.sb.write(seed, "run.sh", "echo hi\n")
        self.base = self.sb.commit(seed, "Initial commit")
        self.sb.git(seed, "push", "-q", "origin", "main")
        self.seed = seed

    def tearDown(self):
        self.sb.cleanup()

    def clone(self, name="work"):
        path = self.sb.dir / name
        self.sb.git(self.sb.dir, "clone", "-q", str(self.origin), str(path))
        return path

    def advance_origin(self, files, message="Upstream change"):
        for rel, text in files.items():
            if text is None:
                (self.seed / rel).unlink()
            else:
                self.sb.write(self.seed, rel, text)
        sha = self.sb.commit(self.seed, message)
        self.sb.git(self.seed, "push", "-q", "origin", "main")
        return sha

    # --- default branch states -----------------------------------------------------------------

    def test_up_to_date_and_default_from_origin_head(self):
        w = self.clone()
        s = self.sb.state(w)
        self.assertEqual(s["remote"]["default_branch"], "main")
        self.assertEqual(s["default_branch"]["state"], "up_to_date")
        self.assertEqual(os.path.realpath(s["default_branch"]["checked_out_at"]), os.path.realpath(w))   # absolute (§4)
        self.assertFalse(s["in_linked_worktree"])
        self.assertEqual(s["branch"], "main")
        self.assertFalse(s["claude_worktrees_ignored"])
        self.assertFalse(s["sandbox"]["git_config_write_masked"])

    def test_behind(self):
        w = self.clone()
        self.advance_origin({"a.txt": "two\n"})
        self.advance_origin({"b.txt": "bees\n"})
        self.sb.git(w, "fetch", "-q", "origin")
        d = self.sb.state(w)["default_branch"]
        self.assertEqual((d["state"], d["ahead"], d["behind"]), ("behind", 0, 2))

    def test_ahead(self):
        w = self.clone()
        self.sb.write(w, "c.txt", "local\n")
        self.sb.commit(w, "Local only")
        d = self.sb.state(w)["default_branch"]
        self.assertEqual((d["state"], d["ahead"], d["behind"]), ("ahead", 1, 0))

    def test_diverged(self):
        w = self.clone()
        self.sb.write(w, "c.txt", "local\n")
        self.sb.commit(w, "Local only")
        self.advance_origin({"a.txt": "two\n"})
        self.sb.git(w, "fetch", "-q", "origin")
        d = self.sb.state(w)["default_branch"]
        self.assertEqual((d["state"], d["ahead"], d["behind"]), ("diverged", 1, 1))

    def test_unrelated(self):
        w = self.sb.repo("other", origin=self.origin)
        self.sb.write(w, "z.txt", "unrelated\n")
        self.sb.commit(w, "Unrelated root")
        self.sb.git(w, "fetch", "-q", "origin")
        d = self.sb.state(w, "--default-branch", "main")["default_branch"]
        self.assertEqual(d["state"], "unrelated")

    def test_no_remote(self):
        w = self.sb.repo("lonely")
        self.sb.write(w, "a.txt", "x\n")
        self.sb.commit(w, "Only commit")
        s = self.sb.state(w)
        self.assertIsNone(s["remote"])
        self.assertEqual(s["default_branch"]["state"], "no_remote")

    def test_empty_remote_and_unknown_before_fetch(self):
        empty = self.sb.bare("empty.git")
        w = self.sb.repo("fresh", origin=empty)
        self.sb.write(w, "a.txt", "x\n")
        self.sb.commit(w, "First")
        self.assertEqual(self.sb.state(w)["default_branch"]["state"], "unknown")
        self.sb.git(w, "fetch", "-q", "origin")
        self.assertEqual(self.sb.state(w)["default_branch"]["state"], "empty_remote")

    def test_unborn_local_with_remote_history_is_behind(self):
        w = self.sb.repo("unborn", origin=self.origin)
        self.sb.git(w, "fetch", "-q", "origin")
        s = self.sb.state(w, "--default-branch", "main")
        self.assertTrue(s["unborn"])
        self.assertEqual(s["default_branch"]["state"], "behind")
        self.assertEqual(s["default_branch"]["behind"], 1)

    # --- operations in progress and detached HEAD ----------------------------------------------

    def conflicting_branches(self):
        w = self.clone()
        self.sb.git(w, "switch", "-q", "-c", "topic")
        self.sb.write(w, "a.txt", "topic\n")
        self.sb.commit(w, "Topic edit")
        self.sb.git(w, "switch", "-q", "main")
        self.sb.write(w, "a.txt", "main\n")
        self.sb.commit(w, "Main edit")
        return w

    def test_merge_in_progress(self):
        w = self.conflicting_branches()
        self.sb.git(w, "merge", "topic", check=False)
        self.assertEqual(self.sb.state(w)["operation_in_progress"], "merge")

    def test_rebase_in_progress(self):
        w = self.conflicting_branches()
        self.sb.git(w, "rebase", "topic", check=False)
        s = self.sb.state(w)
        self.assertEqual(s["operation_in_progress"], "rebase")
        self.assertTrue(s["detached"])

    def test_cherry_pick_in_progress(self):
        w = self.conflicting_branches()
        self.sb.git(w, "cherry-pick", "topic", check=False)
        self.assertEqual(self.sb.state(w)["operation_in_progress"], "cherry-pick")

    def test_revert_in_progress(self):
        w = self.clone()
        self.sb.write(w, "a.txt", "two\n")
        first = self.sb.commit(w, "Two")
        self.sb.write(w, "a.txt", "three\n")
        self.sb.commit(w, "Three")
        self.sb.git(w, "revert", "--no-edit", first, check=False)
        self.assertEqual(self.sb.state(w)["operation_in_progress"], "revert")

    def test_bisect_in_progress(self):
        w = self.clone()
        self.sb.git(w, "bisect", "start")
        self.assertEqual(self.sb.state(w)["operation_in_progress"], "bisect")

    def test_detached_head(self):
        w = self.clone()
        self.sb.git(w, "checkout", "-q", "--detach", "HEAD")
        s = self.sb.state(w)
        self.assertTrue(s["detached"])
        self.assertIsNone(s["branch"])
        self.assertIsNone(s["operation_in_progress"])

    # --- incoming comparison -------------------------------------------------------------------

    def test_incoming_identical_differs_untouched(self):
        w = self.clone()
        self.advance_origin({"a.txt": "two\n", "b.txt": None, "new.txt": "fresh\n", "d.txt": "dee\n"})
        self.sb.git(w, "fetch", "-q", "origin")
        self.sb.write(w, "a.txt", "two\n")           # modified, equal to incoming
        (w / "b.txt").unlink()                        # deleted, deleted upstream too
        self.sb.write(w, "new.txt", "fresh\n")       # untracked, equal to incoming
        self.sb.write(w, "d.txt", "mine\n")          # untracked, differs from incoming
        self.sb.write(w, "run.sh", "echo bye\n")     # modified, upstream doesn't touch it
        self.sb.write(w, "notes.txt", "local\n")     # untracked, upstream doesn't have it
        ch = {c["path"]: c for c in self.sb.state(w)["changes"]}
        self.assertEqual(ch["a.txt"]["incoming"], "identical")
        self.assertEqual(ch["b.txt"]["status"], "deleted")
        self.assertEqual(ch["b.txt"]["incoming"], "identical")
        self.assertEqual(ch["new.txt"]["status"], "untracked")
        self.assertEqual(ch["new.txt"]["incoming"], "identical")
        self.assertEqual(ch["d.txt"]["incoming"], "differs")
        self.assertEqual(ch["run.sh"]["incoming"], "untouched")
        self.assertEqual(ch["notes.txt"]["incoming"], "untouched")

    def test_incoming_mode_change_differs(self):
        os.chmod(self.seed / "run.sh", 0o755)
        self.sb.commit(self.seed, "Make run.sh executable")
        self.sb.git(self.seed, "push", "-q", "origin", "main")
        w = self.clone()
        self.sb.git(w, "reset", "-q", "--hard", self.base)   # the local copy predates the mode change
        self.sb.write(w, "run.sh", "echo hi\n", mode=0o644)
        self.sb.write(w, "a.txt", "edited\n")
        os.chmod(w / "a.txt", 0o755)                         # mode-only difference from incoming
        ch = {c["path"]: c for c in self.sb.state(w)["changes"]}
        self.assertEqual(ch["a.txt"]["incoming"], "untouched")
        self.assertNotIn("run.sh", ch)
        self.sb.write(w, "run.sh", "echo hi\n", mode=0o755)  # now content and mode equal incoming
        ch = {c["path"]: c for c in self.sb.state(w)["changes"]}
        self.assertEqual(ch["run.sh"]["incoming"], "identical")
        self.sb.write(w, "run.sh", "echo hi\n", mode=0o644)
        self.sb.write(w, "run.sh", "echo hi!\n", mode=0o755)  # mode equal, content not
        ch = {c["path"]: c for c in self.sb.state(w)["changes"]}
        self.assertEqual(ch["run.sh"]["incoming"], "differs")

    def test_staged_flag(self):
        w = self.clone()
        self.sb.write(w, "a.txt", "staged\n")
        self.sb.git(w, "add", "a.txt")
        self.sb.write(w, "b.txt", "unstaged\n")
        ch = {c["path"]: c for c in self.sb.state(w)["changes"]}
        self.assertTrue(ch["a.txt"]["staged"])
        self.assertFalse(ch["b.txt"]["staged"])

    # --- worktrees -----------------------------------------------------------------------------

    def add_worktree(self, w, name, base="origin/main"):
        path = w / ".claude" / "worktrees" / name
        self.sb.git(w, "worktree", "add", "-q", "--no-track", "-b", f"feat/{name}", str(path), base)
        return path

    def backdate(self, path, when):
        for base, dirs, files in os.walk(path):
            for n in files:
                os.utime(os.path.join(base, n), (when, when), follow_symlinks=False)

    def test_worktree_inventory(self):
        w = self.clone()
        self.sb.write(w, ".gitignore", "*.log\n.claude/worktrees/\n")
        self.sb.commit(w, "Ignore logs and worktrees")
        self.sb.git(w, "push", "-q", "origin", "main")
        self.sb.git(w, "fetch", "-q", "origin")
        now = self.sb.clock + 60 * DAY

        merged = self.add_worktree(w, "merged")
        dirty = self.add_worktree(w, "dirty")
        self.sb.write(dirty, "scratch.txt", "untracked\n")
        self.sb.write(dirty, "build.log", "ignored output\n")
        ahead = self.add_worktree(w, "ahead")
        self.sb.write(ahead, "feature.txt", "work\n")
        self.sb.commit(ahead, "Unpushed work", date=now - 20 * DAY)
        self.backdate(ahead, now - 20 * DAY)
        old = self.add_worktree(w, "old")
        self.sb.write(old, "old.txt", "old\n")
        self.sb.commit(old, "Old work", date=now - 35 * DAY)
        self.backdate(old, now - 35 * DAY)
        locked = self.add_worktree(w, "locked")
        self.sb.git(w, "worktree", "lock", "--reason", "keep for demo", str(locked))
        gone = self.add_worktree(w, "gone")
        for base, dirs, files in os.walk(gone, topdown=False):
            for n in files:
                os.unlink(os.path.join(base, n))
            for n in dirs:
                os.rmdir(os.path.join(base, n))
        os.rmdir(gone)
        self.backdate(merged, now - 1 * DAY)
        self.backdate(dirty, now - 1 * DAY)

        iso_now = __import__("datetime").datetime.fromtimestamp(now, __import__("datetime").timezone.utc).isoformat()
        s = self.sb.state(w, "--now", iso_now)
        wt = {x["branch"]: x for x in s["worktrees"]}
        m = wt["feat/merged"]
        self.assertEqual((m["uncommitted"], m["unpushed"], m["merged_by_ancestry"], m["locked"]), (0, 0, True, None))
        self.assertEqual(m["path"], ".claude/worktrees/merged")
        self.assertGreater(m["size_bytes"], 0)
        self.assertEqual(m["activity"], "active")
        d = wt["feat/dirty"]
        self.assertEqual((d["uncommitted"], d["untracked"]), (1, 1))
        self.assertEqual(d["ignored"], ["build.log"])
        a = wt["feat/ahead"]
        self.assertEqual((a["unpushed"], a["merged_by_ancestry"], a["activity"]), (1, False, "idle"))
        self.assertTrue(a["last_activity"].endswith("Z"))
        o = wt["feat/old"]
        self.assertEqual(o["activity"], "stale")
        self.assertEqual(wt["feat/locked"]["locked"], "keep for demo")
        self.assertTrue(wt["feat/gone"]["prunable"])
        main = [x for x in s["worktrees"] if x["main"]][0]
        self.assertTrue(main["current"])
        self.assertTrue(s["claude_worktrees_ignored"])

    def test_activity_uses_file_times_over_commit_date(self):
        w = self.clone()
        self.sb.git(w, "fetch", "-q", "origin")
        now = self.sb.clock + 60 * DAY
        wt = self.add_worktree(w, "busy")
        self.sb.write(wt, "x.txt", "x\n")
        self.sb.commit(wt, "Old commit", date=now - 40 * DAY)
        self.backdate(wt, now - 40 * DAY)
        self.sb.write(wt, "x.txt", "edited recently\n")
        os.utime(wt / "x.txt", (now - 2 * DAY, now - 2 * DAY))
        iso_now = __import__("datetime").datetime.fromtimestamp(now, __import__("datetime").timezone.utc).isoformat()
        busy = [x for x in self.sb.state(w, "--now", iso_now)["worktrees"] if x["branch"] == "feat/busy"][0]
        self.assertEqual(busy["activity"], "active")
        s = self.sb.state(w, "--now", iso_now, "--idle-days", "1")
        busy = [x for x in s["worktrees"] if x["branch"] == "feat/busy"][0]
        self.assertEqual(busy["activity"], "idle")

    def test_in_linked_worktree(self):
        w = self.clone()
        wt = self.add_worktree(w, "inside")
        s = self.sb.state(wt)
        self.assertTrue(s["in_linked_worktree"])
        self.assertEqual(s["branch"], "feat/inside")
        cur = [x for x in s["worktrees"] if x["current"]]
        self.assertEqual([x["branch"] for x in cur], ["feat/inside"])

    # --- docs/specs ID collisions --------------------------------------------------------------

    def test_id_collision(self):
        w = self.clone()
        self.sb.git(w, "switch", "-q", "-c", "feat/spec")
        self.sb.write(w, "docs/specs/spec/SPEC-009.md", "branch version\n")
        self.sb.write(w, "docs/specs/spec/SPEC-010.md", "no collision\n")
        self.sb.commit(w, "Add SPEC-009 and SPEC-010")
        self.advance_origin({"docs/specs/spec/SPEC-009.md": "base version\n"})
        self.sb.git(w, "fetch", "-q", "origin")
        cols = self.sb.state(w)["id_collisions"]
        self.assertEqual([(c["path"], c["id"]) for c in cols], [("docs/specs/spec/SPEC-009.md", "SPEC-009")])

    def test_same_content_is_no_collision(self):
        w = self.clone()
        self.sb.git(w, "switch", "-q", "-c", "feat/spec")
        self.sb.write(w, "docs/specs/spec/SPEC-009.md", "same\n")
        self.sb.commit(w, "Add SPEC-009")
        self.advance_origin({"docs/specs/spec/SPEC-009.md": "same\n"})
        self.sb.git(w, "fetch", "-q", "origin")
        self.assertEqual(self.sb.state(w)["id_collisions"], [])

    # --- errors and read-only ------------------------------------------------------------------

    def test_not_a_repository(self):
        plain = self.sb.dir / "plain"
        plain.mkdir()
        r = self.sb.run_script("repo_state.py", "-C", str(plain), cwd=plain)
        self.assertEqual(r.returncode, 2)
        self.assertIn("not_a_git_repository", r.stdout)
        self.assertEqual(os.listdir(plain), [])

    def test_changes_nothing(self):
        w = self.clone()
        self.sb.write(w, ".gitignore", "*.log\n")
        self.sb.commit(w, "Ignore logs")
        self.advance_origin({"a.txt": "two\n"})
        self.sb.git(w, "fetch", "-q", "origin")
        wt = self.add_worktree(w, "side")
        self.sb.write(wt, "u.txt", "untracked\n")
        self.sb.write(w, "a.txt", "two\n")
        self.sb.write(w, "b.txt", "changed\n")
        self.sb.write(w, "x.log", "ignored\n")
        self.sb.write(w, "new.txt", "untracked\n")
        # Same content, new mtime: a refreshing command would rewrite the index here.
        os.utime(w / "run.sh", (self.sb.clock + 999, self.sb.clock + 999))
        before = tree_checksum(w)
        self.sb.state(w)
        self.sb.state(wt)
        self.assertEqual(before, tree_checksum(w))

    # --- version 2 (SPEC-007 v2, VER-16) ------------------------------------------------------

    def by_branch(self, report):
        return {x["branch"]: x for x in report["worktrees"]}

    def test_staged_version_found_nowhere_else_differs(self):
        w = self.clone()
        self.advance_origin({"a.txt": "upstream\n"})
        self.sb.git(w, "fetch", "-q", "origin")
        self.sb.write(w, "a.txt", "staged only\n")
        self.sb.git(w, "add", "a.txt")
        self.sb.write(w, "a.txt", "upstream\n")   # the working copy now equals the incoming version
        ch = {c["path"]: c for c in self.sb.state(w)["changes"]}
        self.assertEqual(ch["a.txt"]["incoming"], "differs")

    def test_staged_incoming_version_is_identical(self):
        w = self.clone()
        self.advance_origin({"a.txt": "upstream\n"})
        self.sb.git(w, "fetch", "-q", "origin")
        self.sb.write(w, "a.txt", "upstream\n")
        self.sb.git(w, "add", "a.txt")
        ch = {c["path"]: c for c in self.sb.state(w)["changes"]}
        self.assertEqual(ch["a.txt"]["incoming"], "identical")

    def test_empty_remote_fetched_in_linked_worktree(self):
        empty = self.sb.bare("empty.git")
        w = self.sb.repo("fresh", origin=empty)
        self.sb.write(w, "a.txt", "x\n")
        self.sb.commit(w, "First")
        side = self.sb.dir / "side"
        self.sb.git(w, "worktree", "add", "-q", "-b", "side", str(side))
        self.sb.git(side, "fetch", "-q", "origin")   # FETCH_HEAD is per worktree
        self.assertEqual(self.sb.state(side, "--default-branch", "main")["default_branch"]["state"], "empty_remote")

    def test_main_checkout_from_linked_worktree_and_bare(self):
        w = self.clone()
        self.sb.git(w, "fetch", "-q", "origin")
        inside = self.add_worktree(w, "inside")
        self.assertEqual(os.path.realpath(self.sb.state(inside)["main_checkout"]), os.path.realpath(w))
        bare_wt = self.sb.dir / "bare-wt"
        self.sb.git(self.origin, "worktree", "add", "-q", str(bare_wt), "main")
        self.assertIsNone(self.sb.state(bare_wt)["main_checkout"])

    def test_commits_since_created(self):
        w = self.clone()
        self.sb.git(w, "fetch", "-q", "origin")
        self.add_worktree(w, "fresh")
        used = self.add_worktree(w, "used")
        self.sb.write(used, "x.txt", "x\n")
        self.sb.commit(used, "Work")
        wt = self.by_branch(self.sb.state(w))
        self.assertEqual((wt["feat/fresh"]["commits_since_created"], wt["feat/used"]["commits_since_created"]), (0, 1))
        self.sb.git(w, "reflog", "expire", "--expire=all", "--all")
        self.assertIsNone(self.by_branch(self.sb.state(w))["feat/fresh"]["commits_since_created"])

    def test_merged_pr_head_counts_as_pushed(self):
        w = self.clone()
        self.sb.git(w, "fetch", "-q", "origin")
        wt = self.add_worktree(w, "squashed")
        self.sb.write(wt, "s.txt", "s\n")
        tip = self.sb.commit(wt, "Squash me")
        self.sb.git(wt, "push", "-q", "origin", "feat/squashed")
        self.advance_origin({"s.txt": "s\n"}, "Squash me (#7)")   # GitHub squash-merges the PR ...
        self.sb.git(self.seed, "push", "-q", "origin", "--delete", "feat/squashed")   # ... and deletes the branch
        self.sb.git(w, "fetch", "-q", "--prune", "origin")
        plain = self.by_branch(self.sb.state(w))["feat/squashed"]
        self.assertEqual((plain["unpushed"], plain["merged_by_ancestry"], plain["pr"], plain["nothing_unpushed"]),
                         (1, False, None, False))
        prs = [{"number": 3, "state": "CLOSED", "headRefName": "feat/other", "headRefOid": "c" * 40},
               {"number": 7, "state": "MERGED", "headRefName": "feat/squashed", "headRefOid": tip}]
        r = self.sb.run_script("repo_state.py", "-C", str(w), "--prs", "-", stdin=json.dumps(prs))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        x = self.by_branch(json.loads(r.stdout))["feat/squashed"]
        self.assertEqual((x["pr"], x["nothing_unpushed"]), ({"number": 7, "state": "MERGED", "head_matches": True}, True))
        prs[1]["headRefOid"] = "d" * 40   # a commit after the PR's head: not proven pushed
        r = self.sb.run_script("repo_state.py", "-C", str(w), "--prs", "-", stdin=json.dumps(prs))
        x = self.by_branch(json.loads(r.stdout))["feat/squashed"]
        self.assertEqual((x["pr"]["head_matches"], x["nothing_unpushed"]), (False, False))

    def test_non_utf8_file_name(self):
        w = self.clone()
        name = b"r\xe9sum\xe9.txt"   # Latin-1, not valid UTF-8
        with open(os.path.join(os.fsencode(w), name), "wb") as f:
            f.write(b"x\n")
        s = self.sb.state(w)
        self.assertEqual([c["path"] for c in s["changes"]], [os.fsdecode(name)])

    def test_unexpected_error_exits_2(self):
        w = self.clone()
        r = self.sb.run_script("repo_state.py", "-C", str(w), "--now", "not-a-time")
        self.assertEqual(r.returncode, 2, r.stderr)
        self.assertIn("error", json.loads(r.stdout))

    def test_sync_from_a_linked_worktree_reads_the_main_checkout(self):
        w = self.clone()
        self.sb.git(w, "fetch", "-q", "origin")
        side = self.add_worktree(w, "side")
        self.sb.write(w, "a.txt", "edited in the main checkout\n")
        first = json.loads(self.sb.run_script("repo_state.py", cwd=side).stdout)   # the session is in side
        holder = first["default_branch"]["checked_out_at"]
        self.assertEqual(os.path.realpath(holder), os.path.realpath(w))
        r = self.sb.run_script("repo_state.py", "-C", holder, cwd=side)            # sync's -C report
        s = json.loads(r.stdout)
        self.assertIn("a.txt", [c["path"] for c in s["changes"]])   # the main checkout's edit, not side's
        current = [x["branch"] for x in s["worktrees"] if x["current"]]
        self.assertEqual(current, ["feat/side"], "current is the session's checkout, not the -C one")

    def test_unhashable_file_is_not_identical(self):
        w = self.clone()
        self.advance_origin({"b.txt": None})   # upstream deletes b.txt
        self.sb.git(w, "fetch", "-q", "origin")
        p = self.sb.write(w, "b.txt", "a local edit git can't read\n")
        os.chmod(p, 0)
        try:
            ch = {c["path"]: c for c in self.sb.state(w)["changes"]}
        finally:
            os.chmod(p, 0o644)
        self.assertEqual(ch["b.txt"]["incoming"], "differs")

    def test_sandbox_masks_dont_count_as_uncommitted(self):
        w = self.clone()
        self.sb.git(w, "fetch", "-q", "origin")
        side = self.add_worktree(w, "side")
        self.sb.write(side, ".mcp.json", "")   # stands in for a mask (a character device) the sandbox shows
        sys.dont_write_bytecode = True
        sys.path.insert(0, str(SCRIPTS))
        try:
            import repo_state
        finally:
            sys.path.remove(str(SCRIPTS))
        out = io.StringIO()
        with mock.patch.object(repo_state, "is_sandbox_mask", lambda p: os.path.basename(p) == ".mcp.json"), \
                mock.patch.dict(os.environ, self.sb.env), contextlib.redirect_stdout(out):
            self.assertEqual(repo_state.main(["-C", str(w)]), 0)
        x = self.by_branch(json.loads(out.getvalue()))["feat/side"]
        self.assertEqual((x["uncommitted"], x["untracked"], x["sandbox_masks"]), (0, 0, 1))


if __name__ == "__main__":
    unittest.main()
