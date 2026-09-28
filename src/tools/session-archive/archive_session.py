#!/usr/bin/env python3
"""Archive Claude Code session transcripts and index them in SQLite (SPEC-005, draft).

Hook subcommands (read the hook's JSON on stdin, always exit 0):
  archive        Stop / SessionEnd: copy the transcript into the archive and index its text.
  record-write   PostToolUse on Write|Edit: record which session wrote a docs/specs/ document.

Query subcommands:
  search TERM [--limit N] [--raw]   Full-text search over archived messages.
  path SESSION_ID                   Print the archived transcript path (for claude --resume PATH).
  writes DOC_ID                     List the sessions that wrote a document, e.g. BRN-001.
  reindex [SESSION_ID]              Rebuild the text index from the archived files.
  prune                             Delete archived sessions older than retention_days.

Configuration: CLAUDE_ARCHIVE_DIR (default ~/.local/share/claude-archive) holds config.json,
archive.db, transcripts/ and hook-errors.log. config.json:
  {"include_prefixes": ["/home/you/Projects/DevForgeAI"], "retention_days": null}
With no config.json, or an empty include_prefixes, nothing is archived.
Standard library only.
"""
import datetime as _dt
import hashlib
import json
import os
import re
import sqlite3
import sys
import traceback

SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (           -- DM-01
    session_id     TEXT PRIMARY KEY,
    cwd            TEXT NOT NULL,
    source_path    TEXT NOT NULL,
    archive_path   TEXT NOT NULL,
    first_seen     TEXT NOT NULL,
    last_archived  TEXT NOT NULL,
    last_event     TEXT,
    last_reason    TEXT,
    size           INTEGER NOT NULL,
    mtime_ns       INTEGER NOT NULL,
    sha256         TEXT NOT NULL,
    indexed_lines  INTEGER NOT NULL DEFAULT 0,
    skipped_lines  INTEGER NOT NULL DEFAULT 0,
    index_error    TEXT
);
CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts USING fts5(   -- DM-02
    text, session_id UNINDEXED, line_no UNINDEXED, role UNINDEXED, ts UNINDEXED
);
CREATE TABLE IF NOT EXISTS doc_writes (          -- DM-03
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id   TEXT NOT NULL,
    cwd          TEXT NOT NULL,
    rel_path     TEXT NOT NULL,
    tool         TEXT NOT NULL,
    doc_id       TEXT,
    doc_version  TEXT,
    tool_use_id  TEXT UNIQUE,
    written_at   TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS doc_writes_doc ON doc_writes(doc_id);
"""


def archive_dir():
    return os.path.expanduser(os.environ.get("CLAUDE_ARCHIVE_DIR", "~/.local/share/claude-archive"))


def now():
    return _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")


def load_config(root):
    try:
        with open(os.path.join(root, "config.json"), encoding="utf-8") as f:
            cfg = json.load(f)
    except FileNotFoundError:
        cfg = {}
    prefixes = [os.path.realpath(os.path.expanduser(p)) for p in cfg.get("include_prefixes") or []]
    return {"include_prefixes": prefixes, "retention_days": cfg.get("retention_days")}


def included(cwd, cfg):
    real = os.path.realpath(cwd)
    return any(real == p or real.startswith(p.rstrip(os.sep) + os.sep) for p in cfg["include_prefixes"])


def connect(root):
    os.makedirs(root, mode=0o700, exist_ok=True)   # transcripts hold file contents and tool output
    db = sqlite3.connect(os.path.join(root, "archive.db"), timeout=5)
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA busy_timeout=5000")
    db.executescript(SCHEMA)
    return db


def log_error(root, where, detail):
    try:
        os.makedirs(root, exist_ok=True)
        with open(os.path.join(root, "hook-errors.log"), "a", encoding="utf-8") as f:
            f.write(f"{now()} {where}: {detail}\n")
    except OSError:
        pass


def copy_atomic(src, dst):
    """Copy src to dst via a temp file and rename; return the sha256 of what was copied."""
    os.makedirs(os.path.dirname(dst), mode=0o700, exist_ok=True)
    tmp = f"{dst}.{os.getpid()}.tmp"
    digest = hashlib.sha256()
    try:
        with open(src, "rb") as fin, open(os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "wb") as fout:
            for chunk in iter(lambda: fin.read(1 << 20), b""):
                digest.update(chunk)
                fout.write(chunk)
        os.replace(tmp, dst)
    except BaseException:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise
    return digest.hexdigest()


def message_text(entry):
    """Best-effort text of one transcript entry. The format is internal to Claude Code."""
    if not isinstance(entry, dict) or entry.get("type") not in ("user", "assistant"):
        return None, None
    content = (entry.get("message") or {}).get("content")
    if isinstance(content, str):
        text = content
    elif isinstance(content, list):
        text = "\n".join(b.get("text", "") for b in content
                         if isinstance(b, dict) and b.get("type") == "text")
    else:
        return None, None
    return (text.strip() or None), entry.get("type")


def index_session(db, session_id, path):
    """Rebuild one session's rows in messages_fts. Returns (indexed, skipped)."""
    indexed = skipped = 0
    rows = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for line_no, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except ValueError:
                skipped += 1        # e.g. a line still being written when the Stop hook copied it
                continue
            text, role = message_text(entry)
            if text:
                rows.append((text, session_id, line_no, role, entry.get("timestamp")))
                indexed += 1
    with db:
        db.execute("DELETE FROM messages_fts WHERE session_id = ?", (session_id,))
        db.executemany("INSERT INTO messages_fts(text, session_id, line_no, role, ts) VALUES (?,?,?,?,?)", rows)
    return indexed, skipped


def project_slug(transcript_path, cwd):
    parent = os.path.basename(os.path.dirname(transcript_path))
    return parent or re.sub(r"[^A-Za-z0-9]", "-", cwd)


def cmd_archive(hook, root):
    cfg = load_config(root)
    session_id, src, cwd = hook.get("session_id"), hook.get("transcript_path"), hook.get("cwd") or ""
    if not session_id or not src:
        log_error(root, "archive", "hook input lacks session_id or transcript_path")
        return
    if not included(cwd, cfg):
        return
    if not os.path.isfile(src):
        log_error(root, "archive", f"transcript not found: {src}")
        return
    st = os.stat(src)
    dst = os.path.join(root, "transcripts", project_slug(src, cwd), f"{session_id}.jsonl")
    db = connect(root)
    try:
        row = db.execute("SELECT size, mtime_ns, first_seen FROM sessions WHERE session_id = ?",
                         (session_id,)).fetchone()
        event, reason = hook.get("hook_event_name"), hook.get("reason")
        if row and row[0] == st.st_size and row[1] == st.st_mtime_ns and os.path.isfile(dst):
            if reason:
                with db:
                    db.execute("UPDATE sessions SET last_event = ?, last_reason = ? WHERE session_id = ?",
                               (event, reason, session_id))
            return                  # unchanged since the last archive: nothing to copy
        sha = copy_atomic(src, dst)
        ts = now()
        with db:
            db.execute("""INSERT INTO sessions(session_id, cwd, source_path, archive_path, first_seen,
                              last_archived, last_event, last_reason, size, mtime_ns, sha256)
                          VALUES (?,?,?,?,?,?,?,?,?,?,?)
                          ON CONFLICT(session_id) DO UPDATE SET cwd=excluded.cwd,
                              source_path=excluded.source_path, archive_path=excluded.archive_path,
                              last_archived=excluded.last_archived, last_event=excluded.last_event,
                              last_reason=excluded.last_reason, size=excluded.size,
                              mtime_ns=excluded.mtime_ns, sha256=excluded.sha256""",
                       (session_id, cwd, src, dst, row[2] if row else ts, ts, event, reason,
                        st.st_size, st.st_mtime_ns, sha))
        try:
            indexed, skipped = index_session(db, session_id, dst)
            error = None
        except Exception as e:  # the transcript format changed: keep the copy, report the index failure
            indexed, skipped, error = 0, 0, f"{type(e).__name__}: {e}"
            log_error(root, "index", f"{session_id}: {error}")
        with db:
            db.execute("UPDATE sessions SET indexed_lines=?, skipped_lines=?, index_error=? WHERE session_id=?",
                       (indexed, skipped, error, session_id))
    finally:
        db.close()


FRONT_ID = re.compile(r"^id:\s*\"?([A-Z]+-\d+)\"?\s*$")
FRONT_VERSION = re.compile(r"^version:\s*(\d+)\s*$")


def read_front(path):
    doc_id = version = None
    try:
        with open(path, encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i > 60 or (i > 0 and line.rstrip() == "---"):
                    break
                m = FRONT_ID.match(line.rstrip()) or None
                if m:
                    doc_id = m.group(1)
                m = FRONT_VERSION.match(line.rstrip())
                if m:
                    version = m.group(1)
    except OSError:
        pass
    return doc_id, version


def cmd_record_write(hook, root):
    cfg = load_config(root)
    cwd = hook.get("cwd") or ""
    tool_input = hook.get("tool_input") or {}
    path = tool_input.get("file_path")
    if not path or not included(cwd, cfg):
        return
    real_cwd, real_path = os.path.realpath(cwd), os.path.realpath(os.path.join(cwd, path))
    specs = os.path.join(real_cwd, "docs", "specs") + os.sep
    if not (real_path.startswith(specs) and real_path.endswith(".md")):
        return
    doc_id, version = read_front(real_path)
    db = connect(root)
    try:
        with db:
            db.execute("""INSERT OR IGNORE INTO doc_writes(session_id, cwd, rel_path, tool, doc_id,
                              doc_version, tool_use_id, written_at) VALUES (?,?,?,?,?,?,?,?)""",
                       (hook.get("session_id") or "", cwd, os.path.relpath(real_path, real_cwd),
                        hook.get("tool_name") or "", doc_id, version, hook.get("tool_use_id"), now()))
    finally:
        db.close()


def cmd_search(args, root):
    raw = "--raw" in args
    limit = 20
    if "--limit" in args:
        limit = int(args[args.index("--limit") + 1])
        del args[args.index("--limit"):args.index("--limit") + 2]
    terms = [a for a in args if a != "--raw"]
    if not terms:
        print("usage: archive_session.py search TERM [--limit N] [--raw]", file=sys.stderr)
        return 2
    query = " ".join(terms) if raw else '"' + " ".join(terms).replace('"', '""') + '"'
    db = connect(root)
    rows = db.execute("""SELECT m.session_id, s.cwd, m.ts, m.role,
                                snippet(messages_fts, 0, '[', ']', '…', 12)
                         FROM messages_fts m LEFT JOIN sessions s USING(session_id)
                         WHERE messages_fts MATCH ? ORDER BY m.ts DESC LIMIT ?""", (query, limit)).fetchall()
    for sid, cwd, ts, role, snip in rows:
        print(f"{ts or '?'}  {sid}  {role}  {cwd or '?'}\n    {snip}")
    return 0 if rows else 1


def cmd_path(args, root):
    if len(args) != 1:
        print("usage: archive_session.py path SESSION_ID", file=sys.stderr)
        return 2
    row = connect(root).execute("SELECT archive_path FROM sessions WHERE session_id = ?", (args[0],)).fetchone()
    if not row:
        print(f"no archived session {args[0]}", file=sys.stderr)
        return 1
    print(row[0])
    return 0


def cmd_writes(args, root):
    if len(args) != 1:
        print("usage: archive_session.py writes DOC_ID", file=sys.stderr)
        return 2
    rows = connect(root).execute("""SELECT written_at, doc_version, tool, session_id, rel_path FROM doc_writes
                                    WHERE doc_id = ? ORDER BY written_at""", (args[0],)).fetchall()
    for written_at, version, tool, sid, rel in rows:
        print(f"{written_at}  v{version or '?'}  {tool:5}  {sid}  {rel}")
    return 0 if rows else 1


def cmd_reindex(args, root):
    db = connect(root)
    sql = "SELECT session_id, archive_path FROM sessions" + (" WHERE session_id = ?" if args else "")
    for sid, path in db.execute(sql, tuple(args[:1])).fetchall():
        try:
            indexed, skipped = index_session(db, sid, path)
            error = None
        except Exception as e:
            indexed, skipped, error = 0, 0, f"{type(e).__name__}: {e}"
        with db:
            db.execute("UPDATE sessions SET indexed_lines=?, skipped_lines=?, index_error=? WHERE session_id=?",
                       (indexed, skipped, error, sid))
        print(f"{sid}: {indexed} messages indexed, {skipped} lines skipped{', ' + error if error else ''}")
    return 0


def cmd_prune(args, root):
    days = load_config(root)["retention_days"]
    if not days:
        print("retention_days is not set in config.json; nothing pruned")
        return 0
    cutoff = (_dt.datetime.now(_dt.timezone.utc) - _dt.timedelta(days=days)).isoformat(timespec="seconds")
    db = connect(root)
    old = db.execute("SELECT session_id, archive_path FROM sessions WHERE last_archived < ?", (cutoff,)).fetchall()
    with db:
        for sid, path in old:
            db.execute("DELETE FROM messages_fts WHERE session_id = ?", (sid,))
            db.execute("DELETE FROM sessions WHERE session_id = ?", (sid,))
            try:
                os.remove(path)
            except OSError:
                pass
    print(f"pruned {len(old)} session(s) last archived before {cutoff}")
    return 0


HOOKS = {"archive": cmd_archive, "record-write": cmd_record_write}
QUERIES = {"search": cmd_search, "path": cmd_path, "writes": cmd_writes, "reindex": cmd_reindex, "prune": cmd_prune}


def main(argv):
    root = archive_dir()
    if len(argv) < 2 or argv[1] not in {**HOOKS, **QUERIES}:
        print(__doc__, file=sys.stderr)
        return 2
    name = argv[1]
    if name in HOOKS:
        # A hook must never fail or slow down the session: log problems, exit 0, print nothing.
        try:
            HOOKS[name](json.loads(sys.stdin.read() or "{}"), root)
        except Exception:
            log_error(root, name, traceback.format_exc(limit=3).replace("\n", " | "))
        return 0
    return QUERIES[name](argv[2:], root)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
