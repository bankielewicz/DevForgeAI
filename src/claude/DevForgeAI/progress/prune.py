"""Remove old working files of DevForgeAI's progress tracker: SPEC-013 IF-04, run by the adapter (BEH-19).

    prune --root DIR --days N [--keep-session ID] [--keep-run ID]

Under DIR/devforgeai/progress/ it removes each folder runs/<name> whose name is a run ID (SPEC-012 §4) and each
sessions/<name> whose name is a session ID (a UUID), when the newest entry in it, the folder included, was last
modified more than N days ago, other than the kept session's and run's folders. A session ID of another shape is
left alone. It never follows a symbolic link: it skips one, and leaves any folder that holds one; a folder whose
real path isn't inside the progress folder is refused. It deletes nothing else.

Prints "pruned <r> runs, <s> sessions"; exit 0, also when there is no devforgeai/progress/; exit 2 with one line on
stderr when DIR isn't a folder, N isn't a whole number of at least 1, or a deletion fails.

The adapter starts it as a process because the mods API can't delete files ($.fs has no delete). Standard library
only; runs under python3 -S (QR-04).
"""
import argparse
import os
import re
import stat
import sys
import time

DAY = 86400
RUN = re.compile(r"[0-9]{8}T[0-9]{6}Z-[a-z][a-z0-9-]*-[0-9a-f]{8}")
SESSION = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")


class Fail(Exception):
    """A reason the command can't run or finish: exit 2 with one line on stderr."""


def is_link(path):
    return stat.S_ISLNK(os.lstat(path).st_mode)


def newest(folder):
    """The newest modification time in a folder, the folder included; None when it holds a symbolic link."""
    latest = os.lstat(folder).st_mtime
    for parent, dirs, files in os.walk(folder):
        for name in dirs + files:
            info = os.lstat(os.path.join(parent, name))
            if stat.S_ISLNK(info.st_mode):
                return None
            latest = max(latest, info.st_mtime)
    return latest


def remove(folder):
    """Delete a folder's contents bottom-up, then the folder; os.walk doesn't descend through links."""
    for parent, dirs, files in os.walk(folder, topdown=False):
        for name in files:
            os.unlink(os.path.join(parent, name))
        for name in dirs:
            os.rmdir(os.path.join(parent, name))
    os.rmdir(folder)


def candidates(progress, kind, pattern, keep):
    """The folders of one kind that may be pruned: plain folders, named by the pattern, not kept, inside progress."""
    parent = os.path.join(progress, kind)
    if not os.path.isdir(parent) or is_link(parent):
        return []
    inside = os.path.realpath(progress) + os.sep
    found = []
    for name in sorted(os.listdir(parent)):
        path = os.path.join(parent, name)
        if name == keep or not pattern.fullmatch(name) or is_link(path) or not os.path.isdir(path):
            continue
        if not os.path.realpath(path).startswith(inside):
            continue
        found.append(path)
    return found


def days_of(text):
    if not re.fullmatch(r"[0-9]+", text) or int(text) < 1:
        raise Fail("--days must be a whole number of at least 1, not %r" % text)
    return int(text)


def prune(root, days, keep_session, keep_run, now):
    if not os.path.isdir(root):
        raise Fail("%s: not a folder" % root)
    base = os.path.join(root, "devforgeai")
    progress = os.path.join(base, "progress")
    if not os.path.isdir(progress) or is_link(base) or is_link(progress):
        return 0, 0
    cutoff = now - days * DAY
    counts = []
    for kind, pattern, keep in (("runs", RUN, keep_run), ("sessions", SESSION, keep_session)):
        removed = 0
        for path in candidates(progress, kind, pattern, keep):
            latest = newest(path)
            if latest is None or latest >= cutoff:
                continue
            try:
                remove(path)
            except OSError as err:
                raise Fail("%s: %s" % (path, err))
            removed += 1
        counts.append(removed)
    return counts[0], counts[1]


def main(argv=None):
    p = argparse.ArgumentParser(prog="prune.py", description="remove old run and session folders (SPEC-013 IF-04)")
    sub = p.add_subparsers(dest="command", required=True)
    c = sub.add_parser("prune", help="remove run and session folders older than --days")
    c.add_argument("--root", required=True, help="the project root")
    c.add_argument("--days", required=True, help="the retention period, a whole number of days of at least 1")
    c.add_argument("--keep-session", default=None, help="a session ID whose folder stays")
    c.add_argument("--keep-run", default=None, help="a run ID whose folder stays")
    args = p.parse_args(argv)
    try:
        runs, sessions = prune(args.root, days_of(args.days), args.keep_session, args.keep_run, time.time())
    except Fail as why:
        print("prune: %s" % why, file=sys.stderr)
        return 2
    print("pruned %d runs, %d sessions" % (runs, sessions))
    return 0


if __name__ == "__main__":
    sys.exit(main())
