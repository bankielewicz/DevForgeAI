# session-archive (draft, SPEC-005)

User-level Claude Code hooks that keep a copy of each session transcript beyond Claude Code's 30-day
retention, index its messages for search in SQLite, and record which session wrote each
`docs/specs/` document. This is not part of the `devforgeai` plugin, and nothing here is installed.

## Files

| File | Purpose |
|---|---|
| `archive_session.py` | The hook and query script. Standard library only |
| `test_archive_session.py` | Tests: `python3 -m unittest discover -s src/tools/session-archive -p 'test_*.py'` |
| `settings-snippet.json` | Hook entries to merge into `~/.claude/settings.json` |
| `config.example.json` | Copy to `$CLAUDE_ARCHIVE_DIR/config.json` and edit |

## Install (from a plain WSL shell)

```bash
mkdir -p ~/.claude/hooks/session-archive
cp src/tools/session-archive/archive_session.py ~/.claude/hooks/session-archive/
mkdir -m 700 -p ~/.local/share/claude-archive
cp src/tools/session-archive/config.example.json ~/.local/share/claude-archive/config.json
```

Then merge the three entries from `settings-snippet.json` into the `hooks` object of
`~/.claude/settings.json`. Add them beside any hooks you already have; don't replace them.
Start a new session, send one message, and check:

```bash
python3 ~/.claude/hooks/session-archive/archive_session.py search "the words you typed"
```

## Use

```bash
A=~/.claude/hooks/session-archive/archive_session.py
python3 $A search IDEA-02                 # which sessions mention it (phrase search; --raw for FTS5 syntax)
python3 $A writes BRN-001                 # which sessions wrote BRN-001, per version
claude --resume "$(python3 $A path <session-id>)"   # reopen an archived session, even after 30 days
python3 $A reindex                        # rebuild the search index, e.g. after a Claude Code format change
python3 $A prune                          # delete sessions older than retention_days (if set)
```

Problems are logged to `~/.local/share/claude-archive/hook-errors.log`. A hook never fails a session.

## Remove

Delete the three hook entries from `~/.claude/settings.json`. The archive in
`~/.local/share/claude-archive` stays until you delete it.
