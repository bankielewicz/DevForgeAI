"""Temporary git repositories for the git skill's script tests (SPEC-007 VER-16, VER-17).

Every repository lives under a fresh temporary directory, uses no global or system git
configuration, and gets fixed author, committer and dates, so tests don't depend on the machine.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "claude" / "DevForgeAI" / "skills" / "git" / "scripts"


class Sandbox:
    """A temporary directory with an isolated git environment."""

    def __init__(self):
        self.dir = Path(tempfile.mkdtemp(prefix="git-skill-test-"))
        cfg = self.dir / "gitconfig"
        cfg.write_text("[init]\n\tdefaultBranch = main\n[gc]\n\tauto = 0\n[commit]\n\tgpgsign = false\n"
                       "[advice]\n\tdetachedHead = false\n")
        self.env = dict(os.environ, GIT_CONFIG_GLOBAL=str(cfg), GIT_CONFIG_NOSYSTEM="1",
                        GIT_AUTHOR_NAME="Dana Reyes", GIT_AUTHOR_EMAIL="dana@example.com",
                        GIT_COMMITTER_NAME="Dana Reyes", GIT_COMMITTER_EMAIL="dana@example.com",
                        GIT_TERMINAL_PROMPT="0", GIT_EDITOR="true", PYTHONDONTWRITEBYTECODE="1")
        self.clock = 1788000000  # 2026-08-29T10:40:00Z

    def cleanup(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def git(self, cwd, *args, check=True, date=None):
        env = self.env
        if date is not None:
            env = dict(env, GIT_AUTHOR_DATE=f"@{date} +0000", GIT_COMMITTER_DATE=f"@{date} +0000")
        r = subprocess.run(["git", *args], cwd=cwd, env=env, capture_output=True, text=True)
        if check and r.returncode != 0:
            raise AssertionError(f"git {' '.join(args)} failed in {cwd}: {r.stderr}")
        return r

    def bare(self, name="origin.git"):
        path = self.dir / name
        self.git(self.dir, "init", "-q", "--bare", "-b", "main", str(path))
        return path

    def repo(self, name="work", origin=None):
        path = self.dir / name
        self.git(self.dir, "init", "-q", "-b", "main", str(path))
        if origin is not None:
            self.git(path, "remote", "add", "origin", str(origin))
        return path

    def write(self, repo, rel, text, mode=None):
        p = Path(repo) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text) if isinstance(text, str) else p.write_bytes(text)
        if mode is not None:
            os.chmod(p, mode)
        return p

    def commit(self, repo, message, paths=None, date=None):
        self.clock += 60
        self.git(repo, "add", "-A", *(["--", *paths] if paths else []))
        self.git(repo, "commit", "-q", "--allow-empty", "-m", message, date=date or self.clock)
        return self.git(repo, "rev-parse", "HEAD").stdout.strip()

    def run_script(self, name, *args, cwd=None, stdin=None):
        r = subprocess.run([sys.executable, str(SCRIPTS / name), *args], cwd=cwd, env=self.env,
                           input=stdin, capture_output=True, text=True)
        return r

    def state(self, repo, *args):
        r = self.run_script("repo_state.py", "-C", str(repo), *args)
        if r.returncode != 0:
            raise AssertionError(f"repo_state.py exited {r.returncode}: {r.stdout}{r.stderr}")
        return json.loads(r.stdout)


def tree_checksum(*roots):
    """Checksum of every path, content, mode and mtime under the given directories."""
    h = hashlib.sha256()
    for root in roots:
        for base, dirs, files in sorted(os.walk(root)):
            dirs.sort()
            for n in sorted(files):
                p = os.path.join(base, n)
                st = os.lstat(p)
                h.update(f"{p}\0{st.st_mode}\0{st.st_mtime_ns}\0{st.st_size}\0".encode())
                if os.path.isfile(p) and not os.path.islink(p):
                    with open(p, "rb") as f:
                        h.update(f.read())
    return h.hexdigest()
