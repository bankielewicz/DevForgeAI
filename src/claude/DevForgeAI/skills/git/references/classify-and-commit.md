# Classify, scan, check and commit

## Contents

- Classify before staging
- Ignore rules for local paths
- The pre-publish scan
- The repository's checks
- Commit messages and hooks

## Classify before staging

List every change: `git status --porcelain=v2 -z --untracked-files=all` (or the report's
`changes`), with `git diff` and `git diff --cached` for content. Put each path in exactly one class:

| Class | What | Handling |
|---|---|---|
| `task` | The work being delivered, confirmed from the request, the session's own edits and the diff | Staged by explicit path |
| `unrelated` | Other work: another session's edits, edits that predate the task, paths the user calls other work | Left unstaged and named |
| `local` | Generated or machine-specific: bytecode and caches (`__pycache__/`, `*.pyc`, `.pytest_cache/`, `node_modules/`), build output, logs, editor and OS files (`*:Zone.Identifier`, `.DS_Store`, `.idea/`, `.vscode/`), sandbox write masks (`sandbox_mask: true`), deployed copies, `.env` and `*.local.*` files | Never staged; an ignore pattern is proposed |
| `blocked` | A scan finding that blocks (below) | Never committed |
| `uncertain` | Anything the evidence doesn't settle, including a file mixing task and unrelated edits | Not staged; named, with a question |

- Stage task paths only: `git add -- <path> <path> …`. Never `git add -A`, `git add .`,
  `git add -u`, `git add <directory>` holding non-task files, or `git commit -a`.
- **Already staged by the user** but not task: report those paths and ask before committing or
  unstaging them.
- Never put a task or unrelated path in an ignore file.
- A tracked file that should be local stays tracked unless the user confirms `git rm --cached
  <path>`; the question says this deletes the file for everyone once merged.
- ERR-14: no task paths and no commits beyond the base means nothing to deliver. Create nothing and
  report `no_change`.

## Ignore rules for local paths

Propose patterns in the reply; don't write them unless the request asks for it or the user
confirms.
- `.gitignore` for patterns every clone needs (build output, caches, `*:Zone.Identifier`);
  `.git/info/exclude` for ones specific to this user or machine.
- Prefer a directory or extension pattern (`__pycache__/`, `*.log`) over single files.
- Before proposing, check that it matches no tracked file (`git ls-files -ci --exclude-standard`
  after adding it to a scratch copy, or `git ls-files -- <pattern>`) and nothing unintended
  (`git check-ignore -v --no-index <path>`).
- A written `.gitignore` change goes in its own commit or is named in the commit message.
- Propose no pattern for a sandbox write mask (`sandbox_mask: true`): it exists only inside the
  sandbox. Name the masks once as local and leave them alone.

## The pre-publish scan

With the task paths staged, run:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/scan_staged.py"
```

It scans the added lines of `git diff --cached` (a new file's full content) and every staged file's
size and type, and prints `{"blocked": [...], "warnings": [...]}`; exit 1 means blocked.

**Blocked (ERR-06):** private keys, access tokens and credentials with a literal value, `.env` files
and key stores, files over 100 MB. Commit nothing, even when the user asks. Name each file and line,
never the value, and suggest removing the file from the commit, moving the value to an environment
variable or ignored file, and rotating a real credential. Leave the index as the user had it:
unstage only what this run staged (`git restore --staged -- <path>` keeps the working copy). An
untracked `.env` or key store that the request would include ("commit everything") is named as
blocked too, though the scan never sees an unstaged file. Report `blocked`.

**Warnings**, which need the user's yes before committing: absolute home paths, e-mail addresses
other than the repository's commit authors, files over 50 MB or binaries outside the LFS rules,
third-party documents (PDFs, saved web pages, vendored documentation without a license), CRLF line
endings in an LF repository, whitespace errors. With no answer possible, commit nothing that carries
a warning and report `awaiting_approval`.

When the remote is public or its visibility is unknown, say that whatever is pushed is published.

## The repository's checks

- Run the checks the repository's instructions require before committing (and again before a PR
  when a rebase brought in new commits): tests, validators, linters, `git diff --cached --check`.
  Use the commands and directory they name; install nothing.
- Keep checks from writing into the repository where the tool allows it
  (`PYTHONDONTWRITEBYTECODE=1`, pytest's `-p no:cacheprovider`).
- Report each check with its command: `passed`, `failed` or `not run`. Never report an unrun check
  as passing.
- **ERR-07.** A failed required check, or a hook that rejects the commit: commit nothing and report
  the command and its relevant output. The user may fix it or confirm committing despite a failed
  check; the PR then opens as a draft naming the failure. A hook is never bypassed. Report `partial`
  or `awaiting_approval`, with the failure in Checks.

## Commit messages and hooks

- **Convention:** the repository's instructions, else the style of recent `git log --format=%s -n 20`
  subjects, else an imperative subject of at most 72 characters and, when the reason isn't obvious,
  a blank line and a short body. With Conventional Commits, the type matches the change (`feat` for a
  new option or behavior, `fix`, `docs`, `test`, `refactor`, `chore`).
- Name the story and spec items the change implements when known (`STORY-012 SPEC-007#IF-01`).
- End with the attribution trailers the session's instructions require.
- One commit per logical change: split task paths that serve different purposes.
- Pass the message with `-m` or a here-document (`git commit -F - <<'EOF'`), never an editor.
- Let hooks and signing run as configured: never `--no-verify`, `--no-gpg-sign` or a `-c` override.
  When a hook modifies files, stage the task paths again and make a new commit; never amend a
  pushed commit.
- Never change git configuration outside the repository.
- A request for a commit message only drafts it: show the message and commit nothing.
