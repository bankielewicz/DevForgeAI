"""Remove old working files of DevForgeAI's progress tracker: SPEC-013 IF-04, run by the adapter (BEH-19).

    prune --root DIR --days N [--keep-session ID] [--keep-run ID]

Under DIR/devforgeai/progress/ it removes each folder runs/<name> whose name is a run ID (SPEC-012 §4) and each
sessions/<name> whose name is a session ID (a UUID), when the newest entry in it, the folder included, was last
modified more than N days ago, other than the kept session's and run's folders. A session ID of another shape is
left alone. It never follows a symbolic link: every folder is opened by a descriptor without following one and
everything beneath it is reached through that descriptor, so a folder swapped for a link meanwhile is never entered;
it skips a link, and leaves any folder that holds one. It deletes nothing else. A folder that changes or vanishes
while it works, as another session's prune or an active run makes it, is skipped. A platform without descriptor
support (Windows) is refused rather than walked by path.

Prints "pruned <r> runs, <s> sessions"; exit 0, also when there is no devforgeai/progress/; exit 2 with one line on
stderr when DIR isn't a folder, N isn't a whole number of at least 1, the platform lacks descriptor support, or a
deletion fails (after both kinds were tried, naming the first failure).

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


# Each folder is opened by a descriptor, without following a link, and everything beneath it is reached through that
# descriptor: a path string resolved again later could meet a folder swapped for a link meanwhile, and prune runs
# outside Claude Code's sandbox (SPEC-013 §9, the plugin-validator's review of version 3).
FOLDER = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)


def supported():
    """Whether this platform can open, walk and delete through descriptors without following links."""
    needed = (os.open, os.stat, os.unlink, os.rmdir)
    return (hasattr(os, "fwalk") and hasattr(os, "O_NOFOLLOW") and hasattr(os, "O_DIRECTORY")
            and all(f in os.supports_dir_fd for f in needed) and os.scandir in os.supports_fd)


def open_folder(name, dir_fd):
    """A plain folder's descriptor; OSError when the name is missing, a link or not a folder."""
    return os.open(name, FOLDER, dir_fd=dir_fd)


def is_link(name, dir_fd):
    return stat.S_ISLNK(os.stat(name, dir_fd=dir_fd, follow_symlinks=False).st_mode)


def newest(name, dir_fd):
    """The newest modification time in a folder, the folder included; None when it holds a symbolic link."""
    latest = os.stat(name, dir_fd=dir_fd, follow_symlinks=False).st_mtime
    fd = open_folder(name, dir_fd)
    try:
        for _, dirs, files, here in os.fwalk(".", dir_fd=fd, follow_symlinks=False):
            for entry in dirs + files:
                info = os.stat(entry, dir_fd=here, follow_symlinks=False)
                if stat.S_ISLNK(info.st_mode):
                    return None
                latest = max(latest, info.st_mtime)
    finally:
        os.close(fd)
    return latest


def remove(name, dir_fd):
    """Delete a folder's contents bottom-up through descriptors, then the folder. A link that appeared since the check
    is removed as a link, never followed."""
    fd = open_folder(name, dir_fd)
    try:
        for _, dirs, files, here in os.fwalk(".", dir_fd=fd, topdown=False, follow_symlinks=False):
            for entry in files:
                os.unlink(entry, dir_fd=here)
            for entry in dirs:
                if is_link(entry, here):
                    os.unlink(entry, dir_fd=here)
                else:
                    os.rmdir(entry, dir_fd=here)
    finally:
        os.close(fd)
    os.rmdir(name, dir_fd=dir_fd)


def prune_kind(kind_fd, kind, pattern, keep, cutoff):
    """Remove one kind's old folders; (removed, the first failure or None). A folder that changes or vanishes meanwhile,
    as another prune or an active run makes it, is skipped."""
    removed, failure = 0, None
    names = sorted(entry.name for entry in os.scandir(kind_fd))
    for name in names:
        if name == keep or not pattern.fullmatch(name):
            continue
        try:
            if is_link(name, kind_fd):
                continue
            latest = newest(name, kind_fd)
            if latest is None or latest >= cutoff:
                continue
            remove(name, kind_fd)
            removed += 1
        except FileNotFoundError:
            continue
        except NotADirectoryError:
            continue
        except OSError as err:
            failure = failure or "%s/%s: %s" % (kind, name, err.strerror or err)
    return removed, failure


def days_of(text):
    if not re.fullmatch(r"[0-9]+", text) or int(text) < 1:
        raise Fail("--days must be a whole number of at least 1, not %r" % text)
    return int(text)


def prune(root, days, keep_session, keep_run, now):
    """(runs removed, sessions removed, the first failure or None)."""
    if not os.path.isdir(root):
        raise Fail("%s: not a folder" % root)
    if not supported():
        raise Fail("this platform can't remove folders without following links; nothing pruned")
    fds = []
    try:
        fds.append(os.open(root, os.O_RDONLY | os.O_DIRECTORY))
        try:
            fds.append(open_folder("devforgeai", fds[-1]))
            fds.append(open_folder("progress", fds[-1]))
        except OSError:
            # Missing, a link or not a folder: nothing of the tracker's to prune.
            return 0, 0, None
        progress_fd, cutoff = fds[-1], now - days * DAY
        counts, failure = [], None
        for kind, pattern, keep in (("runs", RUN, keep_run), ("sessions", SESSION, keep_session)):
            try:
                kind_fd = open_folder(kind, progress_fd)
            except OSError:
                counts.append(0)
                continue
            try:
                removed, failed = prune_kind(kind_fd, kind, pattern, keep, cutoff)
            finally:
                os.close(kind_fd)
            counts.append(removed)
            failure = failure or failed
        return counts[0], counts[1], failure
    finally:
        for fd in reversed(fds):
            os.close(fd)


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
        runs, sessions, failure = prune(args.root, days_of(args.days), args.keep_session, args.keep_run, time.time())
    except Fail as why:
        print("prune: %s" % why, file=sys.stderr)
        return 2
    except OSError as err:
        print("prune: %s" % err, file=sys.stderr)
        return 2
    if failure is not None:
        print("prune: pruned %d runs, %d sessions; %s" % (runs, sessions, failure), file=sys.stderr)
        return 2
    print("pruned %d runs, %d sessions" % (runs, sessions))
    return 0


if __name__ == "__main__":
    sys.exit(main())
