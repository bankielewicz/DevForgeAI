#!/usr/bin/env python3
"""Name where this session's precompact handoff goes, list the project's other handoffs, and prune old ones.

Usage:
    python3 handoff_paths.py --root DIR --session ID [--home DIR] [--no-prune]

DIR is the project root. Prints, one per line:
    project: <key>          the main folder's name and 8 hex characters of the SHA-256 of its path. The main folder is
                            the main checkout of the repository DIR is the top level of (so every worktree has one
                            key and a clone its own), or DIR where git isn't used for it or finds a parent repository.
    session: <name>         ID, or session-<YYYYMMDDTHHMMSSZ> when ID is empty or begins with `${`.
    folder: <path>          <home>/.devforgeai/<key>/handoff/<name>: the handoff folder.
    fallback: <path>        DIR/devforgeai/handoff/<name>: where the handoff goes when the folder can't be written.
    other: <path> | <date> | <branch> | <title>
                            each other handoff of the project, newest first, at most 10: the folders of the store's
                            handoff/ and of DIR/devforgeai/handoff/ (and one level below) that hold a START-HERE.md.
                            The date is its newest file's (UTC); branch and title come from START-HERE.md, `?` when
                            missing.
    pruned: <path>          each folder deleted, and `prune: skipped: <why>` for one that couldn't be, or --no-prune.

Pruning deletes a folder directly under the store's handoff/ that is a real directory, holds a START-HERE.md, isn't
this session's, and whose newest file is older than `handoffRetentionDays` days: the number in
<home>/.devforgeai/config.json, 30 when that file or key is absent or not a number, never when it is 0. It deletes
nothing else, and nothing under DIR. A failed deletion is reported and the run goes on.

The script creates no folder and no file. --home replaces the user's home folder (tests). Exit 0, or 2 when DIR isn't
a folder or ID isn't a single folder name. Standard library only: it runs under `python3 -S`.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time

DEFAULT_RETENTION_DAYS = 30
LISTED = 10
START = "START-HERE.md"


def git(root, *args):
    try:
        p = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    return p.stdout.strip() if p.returncode == 0 and p.stdout.strip() else None


def main_folder(root):
    """The main checkout of the repository whose top level is `root`, else `root` (git unused, or a parent repository)."""
    top = git(root, "rev-parse", "--show-toplevel")
    if not top or os.path.normcase(os.path.realpath(top)) != os.path.normcase(os.path.realpath(root)):
        return root
    common = git(root, "rev-parse", "--path-format=absolute", "--git-common-dir")
    if not common:
        return root
    common = os.path.realpath(common)
    return os.path.dirname(common) if os.path.basename(common) == ".git" else common


def project_key(folder):
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", os.path.basename(folder.rstrip("/\\"))) or "project"
    digest = hashlib.sha256(os.path.normcase(os.path.realpath(folder)).encode("utf-8")).hexdigest()[:8]
    return f"{name}-{digest}"


def newest(folder):
    """The newest modification time of a file in `folder` (any depth), or the folder's own when it has none."""
    times = []
    for base, dirs, files in os.walk(folder, onerror=lambda e: None):
        for name in files:
            try:
                times.append(os.lstat(os.path.join(base, name)).st_mtime)
            except OSError:
                pass
    try:
        return max(times) if times else os.lstat(folder).st_mtime
    except OSError:
        return 0.0


def real_dirs(folder):
    try:
        names = sorted(os.listdir(folder))
    except OSError:
        return []
    out = []
    for name in names:
        path = os.path.join(folder, name)
        if os.path.isdir(path) and not os.path.islink(path):
            out.append(path)
    return out


def has_start(folder):
    return os.path.isfile(os.path.join(folder, START))


def retention_days(home):
    try:
        with open(os.path.join(home, ".devforgeai", "config.json"), encoding="utf-8") as f:
            value = json.load(f).get("handoffRetentionDays")
    except (OSError, ValueError, AttributeError):
        return DEFAULT_RETENTION_DAYS
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
        return DEFAULT_RETENTION_DAYS
    return value


def prune(store, own, days, lines):
    if days == 0:
        return
    limit = time.time() - days * 86400
    for folder in real_dirs(store):
        if os.path.basename(folder) == own or not has_start(folder) or newest(folder) >= limit:
            continue
        try:
            shutil.rmtree(folder)
        except OSError as e:
            lines.append(f"prune: skipped: {folder}: {e.strerror or e}")
        else:
            lines.append(f"pruned: {folder}")


def one_line(text):
    return re.sub(r"\s+", " ", text.replace("|", "/")).strip() or "?"


def describe(folder):
    branch = title = "?"
    try:
        with open(os.path.join(folder, START), encoding="utf-8", errors="replace") as f:
            for n, line in enumerate(f):
                if n > 60:
                    break
                if title == "?" and line.startswith("# "):
                    title = one_line(re.sub(r"^#\s+(Start here:\s*)?", "", line))
                m = re.match(r"^[-*]\s+Branch:\s*(.+)$", line)
                if m and branch == "?":
                    tick = re.match(r"`([^`]+)`", m.group(1))
                    branch = one_line(tick.group(1) if tick else re.split(r"[,;(]", m.group(1))[0])
    except OSError:
        pass
    stamp = time.strftime("%Y-%m-%d", time.gmtime(newest(folder)))
    return f"other: {folder} | {stamp} | {branch} | {title}"


def others(store, project_handoffs, own_paths):
    found = []
    for folder in real_dirs(store):
        if has_start(folder):
            found.append(folder)
    for folder in real_dirs(project_handoffs):
        if has_start(folder):
            found.append(folder)
        for below in real_dirs(folder):
            if has_start(below):
                found.append(below)
    own = {os.path.normcase(os.path.realpath(p)) for p in own_paths}
    found = [f for f in found if os.path.normcase(os.path.realpath(f)) not in own]
    found.sort(key=newest, reverse=True)
    return [describe(f) for f in found[:LISTED]]


def main(argv):
    parser = argparse.ArgumentParser(description="Name a precompact handoff's folders, list the others, prune old ones.")
    parser.add_argument("--root", required=True, help="the project root")
    parser.add_argument("--session", required=True, help="this session's ID")
    parser.add_argument("--home", help="use this folder as the user's home folder (tests)")
    parser.add_argument("--no-prune", action="store_true", help="delete nothing")
    args = parser.parse_args(argv)
    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print(f"handoff_paths: no folder {args.root}", file=sys.stderr)
        return 2
    session = args.session.strip()
    if not session or session.startswith("${"):
        session = time.strftime("session-%Y%m%dT%H%M%SZ", time.gmtime())
    if session in (".", "..") or re.search(r"[/\\]", session):
        print(f"handoff_paths: the session must be one folder name, not {args.session!r}", file=sys.stderr)
        return 2
    home = os.path.abspath(args.home) if args.home else os.path.expanduser("~")
    key = project_key(main_folder(root))
    store = os.path.join(home, ".devforgeai", key, "handoff")
    folder = os.path.join(store, session)
    project_handoffs = os.path.join(root, "devforgeai", "handoff")
    fallback = os.path.join(project_handoffs, session)
    lines = [f"project: {key}", f"session: {session}", f"folder: {folder}", f"fallback: {fallback}"]
    pruned = []
    if args.no_prune:
        pruned.append("prune: skipped: --no-prune")
    else:
        prune(store, session, retention_days(home), pruned)
    lines += others(store, project_handoffs, [folder, fallback]) + pruned
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
