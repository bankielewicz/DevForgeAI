---
name: sync-branch
description: Safely sync local main with origin/main via the collision-aware sync-branch wizard (defaults to option 3 — safe sync)
argument-hint: "[--analyze] [--help]"
model: opus
allowed-tools: Read, AskUserQuestion, Bash(bash:*), Bash(git:*)
---

# /sync-branch — Safely Sync Local `main`

Launch the collision-aware **sync-branch wizard**
(`.claude/scripts/sync-branch.sh`) to reconcile a drifted local `main` with
`origin/main` without destructive git operations. The default action is
**option 3 — Safely sync main** (collision-aware; stashes only true collisions);
the other wizard actions are offered as alternatives.

The wizard classifies every dirty path against the incoming commit range as
**SAFE** (untouched by incoming commits — never stashed), **IDENTICAL**
(byte-identical to the incoming blob, proven by hash — offered for removal), or
**DIVERGENT** (colliding with different content — the only paths stashed). It
fetches first, `merge --ff-only`s, runs a post-sync stash audit, and **never**
runs `reset --hard`, `clean`, `stash pop`, or `stash drop`.

---

## Why the mutating actions hand off to your terminal

The safe-sync action runs `git merge --ff-only origin/main`. In this repo the
incoming commits almost always touch `.claude/{agents,skills,commands,rules}/`,
which the Claude Code sandbox marks read-only — a sandboxed ff-merge can
**partially fail and corrupt the working tree** (`operational-safety.md` Rule 4).
The wizard is also interactive (`[y/N]` confirmations that need a real TTY).

So the safe-sync and CLI-reinstall actions are **handed off to your own
terminal**; the read-only preview runs inline here. This is not a limitation of
the wizard — it is the sandbox boundary.

---

## Phase 01 — Argument handling

```
Parse arguments:

IF arg is "--help" or "-h":
    Display:
      "Usage: /sync-branch [--analyze] [--help]"
      ""
      "  (no args)   Present the wizard menu (default action: safely sync main)."
      "  --analyze   Print the machine-readable collision classification and stop."
      "  --help      Show this help."
      ""
      "The wizard itself: bash .claude/scripts/sync-branch.sh"
    HALT

IF arg is "--analyze":
    # Non-interactive, read-only, sandbox-safe.
    Bash: bash .claude/scripts/sync-branch.sh --analyze
    Display the SAFE / IDENTICAL / DIVERGENT lines and the final VERDICT.
    HALT
```

---

## Phase 02 — Quick state snapshot

```
# Read-only; safe under the sandbox.
Bash: git status -sb
Bash: git rev-list --left-right --count HEAD...origin/main 2>/dev/null || true

Display a one-line summary of the current branch and ahead/behind counts so the
user picks an action with context. (A stale count is fine — the wizard fetches
before doing anything.)
```

---

## Phase 03 — Present the action menu (default: safely sync main)

```
AskUserQuestion(
    questions=[{
        "question": "Which sync-branch action do you want to run?",
        "header": "Action",
        "multiSelect": false,
        "options": [
            {
                "label": "Safely sync main (Recommended)",
                "description": "Wizard option 3 — collision-aware fetch + ff-merge; stashes only truly colliding files. Runs in YOUR terminal (sandbox-unsafe ff-merge + interactive confirms)."
            },
            {
                "label": "Preview remote + collision analysis",
                "description": "Wizard option 2 — show incoming commits and classify your dirty files (SAFE/IDENTICAL/DIVERGENT). Runs inline here via --analyze; no changes made."
            },
            {
                "label": "Generate handoff log only",
                "description": "Wizard option 1 — write a self-contained Markdown handoff log (state, ahead/behind, incoming changes, recovery rules) to tmp/. Runs in YOUR terminal."
            },
            {
                "label": "Show LLM recovery prompt",
                "description": "Wizard option 5 — write a handoff log and print a paste-ready prompt for an LLM to explain/undo the sync. Runs in YOUR terminal."
            },
            {
                "label": "Reinstall the CLI (devforgeai-validate)",
                "description": "Wizard option 4 — reinstall the devforgeai-validate CLI (e.g. after a sync pulls new subcommands). Runs in YOUR terminal."
            }
        ]
    }]
)
```

---

## Phase 04 — Execute the selection

### Preview remote + collision analysis (runs inline)

```
Bash: bash .claude/scripts/sync-branch.sh --analyze
Display the SAFE / IDENTICAL / DIVERGENT lines and the VERDICT.
Display:
  "This is the collision analysis only. For the full preview (incoming commit"
  "list + file changes), run the wizard and choose option 2:"
  "  bash .claude/scripts/sync-branch.sh"
```

### Safely sync main / handoff log / recovery prompt / reinstall CLI (hand off)

```
menu_number = { "Safely sync main": 3, "Generate handoff log only": 1,
                "Show LLM recovery prompt": 5, "Reinstall the CLI": 4 }[selection]

Display:
  "This action runs in YOUR terminal (a real TTY, outside the Claude sandbox)."
  ""
  "  bash .claude/scripts/sync-branch.sh"
  ""
  "Then choose menu option ${menu_number}."
  ""
  "Shortcut: type the following in the prompt to run it in this session:"
  "  ! bash .claude/scripts/sync-branch.sh"
  ""
  IF selection is "Safely sync main":
    "For the safe sync specifically, prefer a plain terminal over the ! shortcut:"
    "the ff-merge writes .claude/ paths the sandbox marks read-only, so running"
    "it fully outside Claude Code avoids a partial-write recovery (Rule 4)."
HALT
```

---

## Error Handling

| Situation | Resolution |
|-----------|------------|
| `.claude/scripts/sync-branch.sh` not found | The command runs from a repo without the framework installed. Display: "sync-branch wizard not found — run this from a DevForgeAI-enabled repo." HALT. |
| No `origin/main` ref | `git rev-list` may print nothing; the wizard's own fetch resolves it. Proceed and let the wizard report. |
| `--analyze` exits non-zero | Display the wizard's error (e.g. "no origin/main ref available") and suggest running `git fetch origin` first. |

---

## Success Criteria

- The command never runs `git merge --ff-only` (or any mutating git operation)
  itself — mutating wizard actions are handed to the user's terminal.
- The default/recommended action is **option 3 — safely sync main**, with the
  other wizard actions offered as alternatives.
- The read-only collision preview runs inline via `--analyze`; nothing is
  stashed, reset, cleaned, or dropped by this command.
