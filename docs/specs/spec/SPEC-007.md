---
id: SPEC-007
type: spec
title: "Git workflow skill"
status: draft          # draft | in-review | approved | superseded | deprecated
version: 1
created: 2026-09-28
updated: 2026-09-28
owner: "Bryan"
authors: ["Bryan", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "97258b2a-7720-412c-b178-c9b6a66e3011"
reviewed_by: []
approved_by: ""
approved_on: null
upstream:
  - {id: PRD-001, item: NFR-001, relation: constrains, version: 9, hash: null}
  - {id: PRD-001, item: NFR-002, relation: constrains, version: 9, hash: null}
  - {id: PRD-001, item: NFR-003, relation: constrains, version: 9, hash: null}
  - {id: ADR-001, relation: constrains, version: 4, hash: null}
  - {id: SPEC-008, relation: constrains, version: 1, hash: null, note: "QA verdict comment and labels, SPEC-008 §4"}
supersedes: []
superseded_by: null
blocked_by: []
# --- spec-specific ---
components: ["src/claude/DevForgeAI/skills/git", "src/tests/git"]
---

# SPEC-007 — Git workflow skill

## 1. Overview

The `git` skill ships in the `devforgeai` plugin and is invoked as
`/devforgeai:git [phase] [details]`, or automatically when a user asks to commit and push work, open
or merge a PR, sync the default branch or clean up worktrees. It takes work in a git repository from "files changed"
to "merged, synced and cleaned up": it connects the repository to its remote, isolates the work in a
worktree, decides what belongs in the commit, commits, pushes, opens a pull request, merges it when
the user authorizes the merge, brings the local default branch up to date without losing data, and
prunes worktrees that are no longer needed. QA is an independent Claude or Codex session that reviews the PR and labels it `merge-approved` or
`qa-failed`. The skill merges only a `merge-approved` PR that the user authorizes it to merge in that
run, sends a `qa-failed` one back to development, and otherwise leaves the merge to the human.

The source is Bryan's request of 2026-09-28, which listed eight steps and asked which steps such a
workflow lacks. Bryan then decided (AskUserQuestion, 2026-09-28): write this spec directly rather
than a workflow document first; serve any repository; replace the step 3 question with
"classify before staging"; and prune only worktrees that are merged or closed and clean. In a
second round the same day he chose the name `git` with phase arguments and a push-only phase; a merge
gate of QA's `merge-approved` label plus his authorization, with the merge method his choice; and
prune age measured by last activity, idle at 14 days and stale at 30, reported only. In a third round
he decided that the skill is model-invocable, suggests `documents-updater` before opening a PR,
supports GitHub only, and that QA is an independent Claude or Codex session that labels PRs. In a
fourth, he decided that QA's verdict names the commit it reviewed, and asked for a stub spec of the
QA skill (SPEC-008).

| # | Requested step | Phase | Items |
|---|---|---|---|
| 1 | Create a worktree for changes to push to a PR | `start` | BEH-05, BEH-06 |
| 2 | Initialize the repository and point it at a remote URL | `connect` | BEH-04, ERR-03, ERR-04 |
| 3 | Should changed files be added to `.gitignore`? | `commit` | BEH-07 (answered below) |
| 4 | Commit the files changed since the prior commit | `commit` | BEH-08, BEH-09, BEH-10 |
| 5 | Push and open a PR | `push`, `pr` | BEH-11, BEH-12 |
| 6 | Merge with authorization, once QA has labeled the PR `merge-approved` | `merge` | BEH-03, BEH-13, BEH-20, ERR-10 |
| 7 | Sync `origin/main` with the local repository safely | `sync` | BEH-14, ERR-11, ERR-12 |
| 8 | Prune stale or old worktrees | `prune` | BEH-15, BEH-16 |

**Step 3, answered.** No: the work itself is never ignored. `.gitignore` has no effect on a file git
already tracks, and ignoring new work hides it from review. What the step needs is a classification
of every change before staging: the task's edits are committed, unrelated edits are left unstaged
and named, local or generated files (caches, `*:Zone.Identifier`, `.env`) get an ignore rule
proposed, and secrets block the commit (BEH-07, BEH-08).

**Steps the request didn't list**, all specified below:

| Added step | Why | Items |
|---|---|---|
| Preflight | Tools, identity, sign-in, an operation already in progress, the real default branch and Claude Code's sandbox decide what can run | BEH-01, ERR-01, ERR-02, ERR-05, ERR-16 |
| Order: connect before start | A worktree needs a commit to branch from; an empty remote needs a first commit on its default branch before any PR | BEH-04 |
| Carry pending changes into the worktree | Step 1 isolates work that usually already exists in the main checkout | BEH-06 |
| Scan before publishing | Everything pushed to a public repository is published: secrets, home paths, third-party files, files over 100 MB | BEH-08, ERR-06 |
| The repository's own checks | Tests, validators and hooks run before the commit, and are reported honestly | BEH-09, BEH-10, ERR-07 |
| Update onto the latest base | The base moves while work is in progress; conflicts must stop the run, not be guessed | BEH-11, ERR-08 |
| An idempotent PR | Rerunning must update the open PR, not open a second one; parallel worktrees can allocate the same document ID | BEH-12, ERR-15 |
| Documentation before the PR | README and CHANGELOG should describe the change before QA reviews it | BEH-19 |
| Independent QA | Another Claude or Codex session labels the PR passed or failed; a failed PR returns to development | BEH-20 |
| A readiness report before merging | CI, reviews, mergeability and a current QA label are what the user authorizes against | BEH-13, ERR-10 |
| Retiring merged branches | `git branch -d` refuses squash-merged branches; deleting them safely needs proof | BEH-15 |
| Backup refs and recovery | Every step that moves a branch records how to undo it | BEH-17 |
| `status`, resumable phases, a completion response | A long workflow is interrupted; each run must know where it stands | BEH-02, BEH-18 |

Three rules shape everything else:

- **No data loss.** A path whose content isn't proven to exist elsewhere (in a commit, a branch or
  the incoming version) is never overwritten, reset, cleaned or removed.
- **Nothing outward-facing or destructive without authorization.** The request authorizes the
  actions it names. A merge always needs a confirmation given after that run's readiness report, and
  destructive actions need a confirmation naming their targets (BEH-03).
- **The repository's rules win.** Its instructions and ADRs (here ADR-001: worktrees under
  `.claude/worktrees/`, redeploy after merge) override this spec's defaults, except the two rules
  above.

The skill is not a planning-chain step. It writes no `docs/specs/<type>/<ID>.md` document and
allocates no document ID. It implements this spec and is recorded as `SKL-006` in its
`provenance.yaml` (SKL-003 and SKL-004 are reserved by SPEC-003 and SPEC-004; SKL-005 is
documents-updater).

## 2. Constraints

- **PRD-001 NFR-001, NFR-002 and NFR-003**, as for SPEC-006: a `SKILL.md` of at most 500 lines with
  detail in `references/`, spec-only frontmatter with provenance in the sidecar, and behavior proven
  by an eval suite (§9).
- **ADR-001 v4:** the skill is built from `src/`, deployed with rsync by the owner, and evaluated
  from a plain terminal. In this repository its lifecycle (worktree location, `claude --worktree`,
  redeploy after merge, `branch -D` after a squash merge) is the repository rule that BEH-01 reads.
- **QA (Bryan, 2026-09-28; SPEC-008).** An independent Claude or Codex session, never the session
  that developed the change, reviews the PR's head commit. It posts a verdict comment naming that
  commit's SHA, then adds `merge-approved` when the PR passes or `qa-failed` when it fails, which
  sends the PR back to development. The human may then merge an approved PR or authorize the skill
  to; the skill merges only when the label, a passing verdict for the current head and that
  authorization are all present (BEH-13, BEH-20), and it never sets a QA label or posts a verdict.
  Because the verdict names a SHA, any push after the review makes it stale. GitHub doesn't let an
  account approve its own PR, and the QA session usually works with the account that opened it, so
  the verdict and label carry the approval rather than a GitHub review. One limit is accepted: with
  one account for development and QA, GitHub can't tell who added a label or comment. The guarantee
  is that this skill never does either (BEH-17), which every eval case grades; a separate account
  for QA would let SPEC-008 also submit a real GitHub review.
- **GitHub only (Bryan, 2026-09-28).** No other hosting service will be supported. The local phases
  work with any git remote; `pr` and `merge` report a remote not hosted on GitHub as unsupported
  (ERR-02).
- **Any repository.** The skill runs in the user's project, which may lack commits, a remote, `gh` or
  instructions. Its `pr` and `merge` phases need GitHub (below).
- **Claude Code's sandbox.** Sessions can write only inside the project directory, so worktrees go
  under it (`.claude/worktrees/`), never beside it. In this repository the sandbox also denies writes
  to `.claude/skills/`, so a redeploy is reported for the owner, never run. Inside the sandbox,
  `git status` also lists its write masks as untracked files: on 2026-09-28 eleven empty
  character devices owned by `nobody` (`.bashrc`, `.gitconfig`, `.mcp.json`, `.vscode` and others)
  appeared at this repository's root. They are not on disk outside the sandbox and must never be
  staged (BEH-07). The sandbox also masks `.git/config.lock`, so every write to `.git/config` fails
  inside it: adding a remote, recording an upstream (`push -u`, a tracking branch) and `git config`.
  A sandboxed `git push` also failed once through the sandbox's proxy on 2026-09-28
  (`~/code/papercuts.md`). This repository's fix is the owner's: `sandbox.excludedCommands` lists
  `git push *` and `gh pr *` in `.claude/settings.local.json`. The skill works around what it can
  (`--no-track`) and reports the rest (ERR-16); it never changes sandbox settings itself.
- **No installs.** The scripts use the Python standard library only and never touch the network.
  Network access is the user's remote, through `git` and `gh`. On 2026-09-28 a sandboxed
  `git ls-remote origin` in this repository reached GitHub over HTTPS through `gh`'s credential helper.

## 3. Architecture and components

```
src/claude/DevForgeAI/
├── skills/git/
│   ├── SKILL.md                         # phase checklist, gates, user decisions, output contract
│   ├── provenance.yaml                  # SKL-006, implements SPEC-007
│   ├── references/
│   │   ├── preflight-and-connect.md     # BEH-01, BEH-04, BEH-05, BEH-06
│   │   ├── classify-and-commit.md       # BEH-07..10: classes, ignore rules, scan, checks, messages
│   │   ├── publish-and-merge.md         # BEH-11..13, 19, 20: push, PR, docs, QA, merge
│   │   ├── sync-and-prune.md            # BEH-14..16: state matrix, reconciliation, retirement, prune
│   │   └── output-rules.md              # completion response, forbidden commands, self-check list
│   └── scripts/
│       ├── repo_state.py                # read-only JSON state report (§4)
│       ├── scan_staged.py               # pre-publish scan of staged content (BEH-08)
│       └── qa_state.py                  # QA state from gh pr view JSON (BEH-20)
└── evals/git/<case>/                    # one case per automated VER item (§9)
src/tests/git/                           # unit tests for both scripts and the eval generator, not deployed
```

```mermaid
flowchart LR
    P[Preflight BEH-01] --> C[connect BEH-04]
    C --> S[start BEH-05 BEH-06]
    S --> K[commit BEH-07..10]
    K -->|scan or check fails| X[Stop ERR-06 ERR-07]
    K --> U[pr BEH-19 BEH-11 BEH-12]
    U -->|conflict| Y[Abort and ask ERR-08]
    U --> QA[Independent QA session labels the PR]
    QA -->|qa-failed BEH-20| K
    QA -->|passing verdict for the head| R[Readiness report]
    R -->|label current and user confirms| M[merge BEH-13]
    R -->|not ready or no current label| Z[Report ERR-10]
    M --> Y2[sync BEH-14]
    Y2 -->|diverged or differing path| Q[Stop and offer options ERR-11 ERR-12]
    Y2 --> B[Retire branch BEH-15]
    B --> W[prune BEH-16]
```

Every phase starts from the state report, skips what's already done, and ends with the completion
response (BEH-18). `status` runs the preflight and the report only.

## 4. Data model

**Inputs:** the repository's git state, its remote, PR data from `gh` (including labels and the PR
timeline), its instructions (CLAUDE.md,
AGENTS.md, CONTRIBUTING, ADRs and runbooks about branches, commits, PRs, merges or deploys), and the
conversation (the task, the session's own edits, authorizations already given).

**State report** (`scripts/repo_state.py`, JSON on stdout, read-only, never uses the network):

```json
{
  "root": "/path/to/repo", "in_linked_worktree": false, "branch": "main", "detached": false,
  "operation_in_progress": null,
  "identity": {"name_set": true, "email_set": true},
  "remote": {"name": "origin", "url": "https://github.com/o/r.git", "default_branch": "main"},
  "default_branch": {"local": "<sha>", "remote": "<sha>", "ahead": 0, "behind": 2,
                     "state": "behind", "checked_out_at": "/path/to/repo"},
  "changes": [
    {"path": "a.txt", "status": "modified", "staged": false, "incoming": "identical"}
  ],
  "worktrees": [
    {"path": ".claude/worktrees/feat-x", "branch": "feat/x", "head": "<sha>", "locked": null,
     "prunable": false, "current": false, "uncommitted": 0, "ignored": ["cache.pyc"],
     "unpushed": 0, "merged_by_ancestry": true, "last_commit": "2026-09-01",
     "last_activity": "2026-09-02T10:00:00Z", "activity": "idle", "size_bytes": 48213504}
  ],
  "id_collisions": []
}
```

- `operation_in_progress`: `null`, `merge`, `rebase`, `cherry-pick`, `revert` or `bisect`.
- `default_branch.state`: `up_to_date`, `behind`, `ahead`, `diverged`, `unrelated`, `no_remote`,
  `empty_remote` or `unknown` (remote-tracking ref missing: fetch first). It is computed from
  remote-tracking refs, so the skill fetches before trusting it.
- `changes[].incoming`: for a path that differs between the working tree and `HEAD`, compares its
  content and mode with `origin/<default>`'s version: `identical`, `differs` or `untouched` (the
  incoming commits don't change it).
- `worktrees[].last_activity`: the latest of the branch's last commit date and the newest
  modification time among the worktree's tracked and untracked files (ignored files don't count);
  the skill also weighs the PR's `updatedAt` when `gh` is available. `activity` is `active`, `idle`
  (at least 14 days) or `stale` (at least 30 days). `size_bytes` includes ignored files such as build
  output, which are usually what makes a worktree expensive to keep.
- `id_collisions`: files under `docs/specs/<type>/` that the branch adds while a file with the same
  path and different content exists on `origin/<default>`.

**Change classes** (BEH-07): `task`, `unrelated`, `local` or `blocked`, one per path; plus
`uncertain`, which is never staged.

**Backup refs:** `refs/devforgeai-backup/<branch>/<UTC yyyymmddThhmmssZ>`, local only, never
pushed, written before the skill moves a branch.

**QA verdict** (defined by SPEC-008 §4): a PR comment whose first line is `QA verdict: passed <sha>`
or `QA verdict: failed <sha>`, with the full 40-character SHA of the commit reviewed, followed by
the findings. `scripts/qa_state.py` reads `gh pr view --json labels,comments,headRefOid` output on
stdin and prints the QA state (BEH-20); it never uses the network.

## 5. Interfaces and contracts

```yaml
# Proposed SKILL.md frontmatter (validated by src/schemas/skill-frontmatter.schema.json)
name: git
description: "<third person: what it does and when to use it, in the words users say (commit and push, open or merge a PR, sync main, clean up worktrees); not for explaining git>"
argument-hint: "[status|connect|start|commit|push|pr|merge|sync|prune] [details]"
metadata:
  devforgeai-id: "SKL-006"
  devforgeai-version: "<SKL-006's provenance.yaml version, quoted>"
```

- **Arguments:** an optional phase, then free text: a remote URL for `connect`, a branch or task for
  `start`, a PR number for `merge`, idle and stale ages in days for `prune` (defaults 14 and 30). With no phase the skill infers the
  phases from the request and the state report (BEH-02).
- **Tools:** Bash for `git`, `gh` and the three scripts; Read, Glob and Grep; Edit and Write only for
  ignore files; AskUserQuestion for gates; EnterWorktree with `path`, to move the session into a
  worktree the skill created; Skill, to run documents-updater when the user accepts BEH-19's
  suggestion.

| Phase | Does | Needs (BEH-03) | Stops with |
|---|---|---|---|
| `status` | Preflight, the state report and the PR's QA state | Nothing: read-only | — |
| `connect` | `git init`, `origin`, fetch, bootstrap an empty remote | The request; a push for the bootstrap | ERR-01, ERR-03, ERR-04, ERR-16 |
| `start` | Branch and worktree, carrying pending changes | The request | ERR-05 |
| `commit` | Classify, scan, checks, commit | The request; confirmation for `git rm --cached` | ERR-06, ERR-07, ERR-14 |
| `push` | Update onto the base, push the branch; no PR | The request names the push | ERR-08, ERR-09, ERR-16 |
| `pr` | Suggest documents-updater, `push`, then open or update the PR | The request names the PR | ERR-02, ERR-08, ERR-09, ERR-15, ERR-16 |
| `merge` | Readiness report, merge, delete the remote branch | QA's current `merge-approved` label and a confirmation in this run, every time | ERR-10 |
| `sync` | Fast-forward the default branch, reconcile, post-merge steps | The request | ERR-11, ERR-12 |
| `prune` | Inventory, report idle and stale worktrees, remove, retire branches | A confirmation listing the targets | ERR-13 |

**Completion response** (the last thing in the reply; empty fields are omitted):

```text
Result: done | partial | blocked | awaiting_approval | no_change
Phases: <phases run, in order>
Branch: <branch> → <base>
PR: <URL, state>
Checks: <each check: passed, failed or not run>
Changes: <committed, left unstaged, proposed for ignoring, blocked>
Action required: <approval needed, conflict, recovery command, the user's own step>
```

## 6. Behavior

```yaml items
behaviors:
  - id: BEH-01
    status: active
    rule: "Before any phase, establish context with read-only commands. Confirm the repository root and whether the session is in the main checkout or a linked worktree. Read the repository's instructions (CLAUDE.md, AGENTS.md, CONTRIBUTING, and ADRs or runbooks about branches, worktrees, commits, PRs, merges or deploys); where they set something this spec also sets (worktree location, branch names, commit format, required checks, merge method, post-merge steps), the repository's rule wins unless it conflicts with BEH-03 or BEH-17. Check that git is installed, that user.name and user.email resolve, whether HEAD is detached, and whether a merge, rebase, cherry-pick, revert or bisect is in progress. For phases that use the remote, check that it is reachable (git ls-remote). Only creating or updating a PR, reading PR state and merging need gh: before those steps, check that gh is installed and signed in (gh auth status). Fetching, rebasing and pushing need only git. Detect whether the session is sandboxed with .git/config write-masked (.git/config.lock exists as a character device); if so, plan every phase without .git/config writes where git allows it (branches with --no-track, a push without -u) and report the rest by ERR-16. Read the default branch from the remote (git ls-remote --symref origin HEAD), never assume main. Run scripts/repo_state.py after fetching, and base every later decision on its report."
  - id: BEH-02
    status: active
    rule: "Take the phase from the first argument (status, connect, start, commit, push, pr, merge, sync, prune) or infer the phases from the request and the state report: for example, 'open a PR for my changes' with uncommitted work runs start, commit and pr. Run phases in the order connect, start, commit, push, pr, merge, sync, prune, skipping those the request doesn't need, and stop at the first gate that needs an answer. When start carries pending work (BEH-06), it makes that work's first commit; commit is for later commits in the worktree. status runs only read-only commands and changes nothing. Every phase first checks whether its result already exists (origin configured, branch or worktree present, change committed, branch pushed, PR open, PR merged, default branch up to date) and reports it rather than repeating it, so rerunning the skill never creates a second branch, worktree, commit of the same change or PR. A request for a commit message only drafts it; the skill commits only when asked."
  - id: BEH-03
    status: active
    rule: "Gate every action by its class. Read-only (status, log, diff, fetch, ls-remote, gh pr view, gh pr checks): always allowed. Local and reversible (git init, adding a remote, creating a branch or worktree, staging, committing, editing an ignore file, a fast-forward): allowed when the request asks for the phase that does it. Outward-facing (push, creating or editing a PR, merging, deleting a remote branch): allowed only when the request names that action, for example 'commit this and open a PR' authorizes the commit, the push and the PR, or when the user confirms it in this run; authorization doesn't carry over to a later run. Merge is never authorized in advance: it needs a confirmation given after that run's readiness report (BEH-13). Destructive (removing a worktree, deleting a local branch, git rm --cached, discarding working-tree content, dropping a stash, rewriting pushed commits): needs a confirmation naming each target, every time. Ask one question per phase that lists the exact commands and targets, with AskUserQuestion when available and the recommended option first, otherwise in plain text ending the turn. When no answer can arrive, do nothing that needs it and report awaiting_approval with the question in Action required."
  - id: BEH-04
    status: active
    rule: "connect: when the directory is not a git repository and the request asks to initialize it, run git init with the default branch named by the repository's instructions, else the remote's default when the remote has commits, else git's init.defaultBranch. When a remote URL is given: add it as origin when no origin exists; report it when origin already has the same repository (https and ssh forms of one GitHub repository count as the same); stop with ERR-03 when origin points elsewhere. Then fetch. A repository without commits and a remote with commits adopts the remote's history: check out its default branch, reconciling local files by BEH-14's per-path rule. When the remote is empty and the local repository has commits, pushing the default branch is the bootstrap (an outward-facing action). When both are empty, offer a minimal bootstrap commit on the default branch holding the ignore file and a README when one exists, so the rest of the work arrives by PR (recommended), or the whole classified change set as the first commit. When both have commits and no merge base, stop with ERR-04."
  - id: BEH-05
    status: active
    rule: "start: create the branch and worktree for the work. Location: the repository's rule (ADR-001's .claude/worktrees/<name> in this repository), else .claude/worktrees/<name>, which is also where Claude Code puts worktrees and lies inside the directory the sandbox lets a session write. Before creating it, confirm with git check-ignore that the location is ignored. If not, add .claude/worktrees/ to .git/info/exclude, which changes no tracked file and covers every worktree of the repository, and mention that a .gitignore entry would share the rule; when the repository's rules require the .gitignore entry (ADR-001 here), add it there instead and name it in the next commit's message. Branch name: the repository's convention (for example story/STORY-NNN-<slug>), else <type>/<slug> with type one of feat, fix, docs, chore, refactor or test and the story or spec ID in the slug when the work has one; lower case, at most 64 characters. The worktree is named after the branch with / replaced by -. Never reuse a local branch, remote branch or worktree name for different work; an existing worktree for the same branch is reused (BEH-02). New work branches from origin/<default> as just fetched, never from a local default branch that may be stale. Create it with git worktree add, then move the session into it with EnterWorktree (path) when that tool is available and the user continues there; otherwise tell the user how to open it (claude --worktree <name> from the main checkout, as ADR-001 step 3 requires here). Run any setup the repository requires in a new worktree (ADR-001 step 2's deploy here), or report it as the user's step when the session can't run it."
  - id: BEH-06
    status: active
    rule: "Carry pending changes: when the work to deliver is uncommitted in the current checkout, move it onto a new branch without loss. After classifying (BEH-07), scanning (BEH-08) and checking (BEH-09): create the branch at the current HEAD (git switch -c <branch>), stage the task paths by explicit path, commit (BEH-10), and before switching back verify that each carried path's committed content equals its pre-move working copy (git hash-object against git rev-parse <branch>:<path>, and absence for deletions); on a mismatch stay on the new branch and report. Then switch back to the original branch, which carries the unrelated edits unchanged, and add the worktree on the new branch (BEH-05). A path that mixes task and unrelated edits is uncertain: ask whether to carry the whole file or leave it. When the current checkout is already a linked worktree or a non-default branch dedicated to this work, commit there; no new branch or worktree is needed. Never transfer work with stash, file copies or patches unless the user chooses it."
  - id: BEH-07
    status: active
    rule: "Classify before staging. List every change (git status --porcelain=v2 -z --untracked-files=all, with git diff and git diff --cached for content) and put each path in one class: task (the work being delivered, confirmed from the request, the session's own edits and the diff); unrelated (other work, another session's edits, edits that predate the task); local (generated or machine-specific: bytecode and caches, build output, logs, editor and OS files such as *:Zone.Identifier and .DS_Store, sandbox placeholders and write masks (empty character-device files such as .bashrc, .gitconfig or .mcp.json that a sandboxed session sees in the repository), deployed copies, .env and *.local.* files); or blocked (BEH-08). A path whose class is uncertain is not staged, and is named. Stage task paths only, by explicit path (git add -- <paths>); never git add -A, git add ., git add -u or git commit -a. Report paths the user had already staged that aren't task paths, and ask before committing or unstaging them. Never put a task or unrelated path in an ignore file, and never stage a local path. For local paths, propose ignore patterns in the reply: .gitignore for patterns every clone needs, .git/info/exclude for ones specific to this user or machine; prefer a directory or extension pattern, and check that it matches no tracked file (git ls-files -ci --exclude-standard) and nothing unintended (git check-ignore -v). Write a proposed pattern only when the request asks for it or the user confirms; a .gitignore change then goes in its own commit or is named in the commit message. A tracked file that should be local stays tracked unless the user confirms git rm --cached, and the question says this deletes it for everyone once merged."
  - id: BEH-08
    status: active
    rule: "Scan before publishing: run scripts/scan_staged.py on the staged content, which covers git diff --cached and the full content of added files. It blocks the commit on private keys, access tokens and credentials with a literal value, .env files and key stores, and any file over 100 MB. It warns, and the skill asks before committing, on absolute home paths (/home/<user>, /Users/<user>, C:/Users/<user>), e-mail addresses other than the repository's commit authors, files over 50 MB or binaries without an LFS rule, third-party documents (PDFs, saved web pages, vendored documentation without a license), CRLF line endings in a repository that uses LF, and whitespace errors from git diff --cached --check. A blocked finding is never committed, even when the user asks. The reply names the file and line, never the secret's value, and suggests removing the file or ignoring it. When the remote repository is public or its visibility is unknown, say that whatever is pushed is published."
  - id: BEH-09
    status: active
    rule: "Run the checks the repository's instructions require before committing or opening a PR (tests, validators, linters, git diff --check), from the directory they name and without installing anything. Report each check with its command as passed, failed or not run, and never report an unrun check as passing. A failed required check stops the commit (ERR-07) unless the user confirms committing anyway; the PR then opens as a draft that names the failure."
  - id: BEH-10
    status: active
    rule: "Write the commit message in the repository's convention (its instructions, else the style of recent git log subjects); otherwise use an imperative subject of at most 72 characters and, when the reason isn't obvious from the subject, a blank line and a short body. Name the story and spec items the change implements when known, for example STORY-012 SPEC-007#IF-01. End with the attribution trailers the session's instructions require. Split the task paths into one commit per logical change when they serve different purposes. Let hooks and commit signing run as configured: never --no-verify, --no-gpg-sign or a -c override. When a hook modifies files, stage the task paths again and make a new commit; never amend a pushed commit. Never change git configuration outside the repository."
  - id: BEH-11
    status: active
    rule: "Before the first push and before a merge, fetch and compare the branch with origin/<default>. When the base has moved and the branch's commits are unpushed, rebase them onto origin/<default> inside the worktree; on a conflict run git rebase --abort, leave the branch as it was and stop with ERR-08. Once commits are pushed, don't rewrite them: bring the base in with a merge commit when the repository's rules allow it, or ask. A push that must replace remote commits uses --force-with-lease=<branch>:<expected sha> after a confirmation, never --force, and never targets the default branch."
  - id: BEH-12
    status: active
    rule: "push: after BEH-11, push the branch with git push -u origin <branch> (without -u when .git/config is write-masked, BEH-01); push opens no PR. pr: run BEH-19's documentation check, push as above, then look for an open PR from the branch (gh pr list --head <branch> --state open); when one exists, push to it and report it, and edit its body only when the user asks. Before creating a PR, check scripts/repo_state.py's id_collisions and stop with ERR-15 when the branch adds a document ID that already exists on the base. Otherwise create it with gh pr create --base <default> --head <branch>: a title in the commit convention, and a body with the scope (what changed and why, in a few lines), the story, spec or issue IDs it implements, each check with its result, limitations and what wasn't verified (documentation not reviewed, when BEH-19's suggestion was declined), and the attribution line the session's instructions require. Open it as a draft when a required check failed or wasn't run, or when the user asks. Report the PR's URL, and name the next step in Action required: an independent QA session reviews it (BEH-20)."
  - id: BEH-13
    status: active
    rule: "merge: the skill merges only a PR whose QA state is approved (BEH-20), and only after the user's confirmation in this run; otherwise the human merges. First give a readiness report: the PR's state and draft flag, mergeability and conflicts, required and other checks (gh pr checks), review decision and requested changes, whether the branch is behind the base, the head commit's SHA, the merge methods the repository allows (gh repo view --json mergeCommitAllowed,squashMergeAllowed,rebaseMergeAllowed), and the QA state. Offer the merge only when the QA state is approved and nothing else blocks it; otherwise report ERR-10. The user chooses the method from the allowed ones; recommend the one the repository's instructions name, else the one its recent history shows. Merge only the PR the user named or the current branch's PR, with gh pr merge <number>, the chosen method and --match-head-commit <the head SHA from the report, which the passing verdict names>, so a commit pushed after the report is never merged. Never use --admin, --auto or --delete-branch (it also deletes and switches local branches), and never bypass or disable branch protection. Afterwards confirm with gh pr view that the state is MERGED and record the merge commit. Delete the remote branch (git push origin --delete <branch>) only when the user confirmed it, and skip that when the repository deletes merged branches itself."
  - id: BEH-14
    status: active
    rule: "sync: bring the local default branch up to origin/<default> without losing data. Fetch with --prune, then record a backup ref for the local default branch. Act on the state: up_to_date, do nothing; behind, fast-forward with git merge --ff-only origin/<default> in the checkout that has the branch checked out, or git fetch origin <default>:<default> when no checkout has it; ahead or diverged, stop with ERR-11 and list the local-only commits. When the checkout holding the default branch has uncommitted changes or untracked files that the fast-forward would overwrite, reconcile each path first: when its content and mode equal the incoming version (git hash-object against git rev-parse origin/<default>:<path>, or both absent), the local change is already upstream, so restoring or removing it loses nothing; otherwise keep it byte-identical, don't move the branch, and stop with ERR-12. Paths the fast-forward doesn't touch stay as they are. Never run git pull without --ff-only, git reset --hard, git clean, or git checkout -- or git restore on a path not proven identical. When the main checkout is on a feature branch whose PR has merged, switch it to the default branch only when it is clean or reconciled as above. Afterwards run the repository's post-merge steps, or report them as the user's step when the session can't run them (ADR-001 step 7's redeploy in this repository, since the sandbox denies writes to .claude/skills/)."
  - id: BEH-15
    status: active
    rule: "Retire a merged local branch only when that loses nothing, after removing its worktree (git refuses to delete a branch a worktree has checked out). Use git branch -d when the branch is an ancestor of origin/<default>. When the PR was squashed or rebased (git branch -d refuses), use git branch -D only after gh pr view shows the PR MERGED with a headRefOid equal to the local branch tip, and after a confirmation. Keep and report a branch that has commits beyond the PR's head or no merged PR. Delete backup refs only when the user asks."
  - id: BEH-16
    status: active
    rule: "prune: inventory linked worktrees from git worktree list --porcelain and the state report: branch, last activity and disk size (§4), uncommitted or untracked files, ignored files, commits not on the remote, lock, whether it is the session's current directory, and whether its branch merged (by ancestry, or a MERGED PR whose head equals the tip) or its PR closed. A worktree is removable only when all hold: merged or closed, no uncommitted or untracked files, nothing unpushed, not locked and not current. git worktree remove deletes ignored files without warning, so list each removable worktree's ignored files and ask about any that isn't regenerable output (such as .env, local settings or data). List the removable worktrees, flagging any with files modified within the last hour (another session may be working there), and remove them after one confirmation with git worktree remove, never --force and never rm; then retire their branches by BEH-15, keeping the branch of a closed PR. Age never makes a worktree removable, and a removable one needs no minimum age. Report every worktree that isn't removable with the reason it was kept, its disk size, and its activity: idle when its last activity is at least 14 days old, stale at 30 days (the prune argument may change both). Report a locked worktree as locked, never as idle or stale: a lock is how a user keeps one on purpose. For administrative entries whose directory is gone, show git worktree prune --dry-run -v and run git worktree prune. Never touch the main checkout."
  - id: BEH-17
    status: active
    rule: "Never run these without a confirmation naming the exact target: push --force-with-lease, reset --hard, clean, checkout -- or restore over content not proven identical, branch -D, stash drop or clear, rebase or amend of pushed commits, git rm --cached, deleting a remote branch, merging unrelated histories. Never run these at all: push --force, any forced push to the default branch, gh pr merge --admin or --auto, any command that adds, removes or creates a QA label or posts a QA verdict (BEH-20), --no-verify, history rewriting with filter-branch or filter-repo, worktree remove --force, and changes to git configuration outside the repository. Before a step that moves a branch or rewrites commits, record how to undo it (the backup ref, the previous SHA or the stash ref). When a step fails midway, stop, leave the state as it is, and report the exact commands that restore the previous state, for example git branch -f <branch> <backup ref> for the user to run."
  - id: BEH-18
    status: active
    rule: "End with the completion response (§5). Use done when every requested phase finished, partial when some finished and an issue remains, blocked when nothing could proceed, awaiting_approval when a gate needs an answer, and no_change when everything requested was already done. Report each check honestly (BEH-09) and put anything the user must do (approve, resolve a conflict, run a command the session can't) in Action required. Don't paste the state report or full command output into the reply."
  - id: BEH-19
    status: active
    rule: "Before the pr phase pushes, check the branch's documentation: when its diff against origin/<default> changes files other than documentation but changes neither README.md nor CHANGELOG.md nor the repository's release-note fragments, recommend running /devforgeai:documents-updater with the merge base as its base revision, and ask whether to run it first (recommended) or open the PR now. Don't ask when the request says to skip documentation, when documents-updater already ran on this branch in the session, or when the branch already has an open PR. When the user accepts, run documents-updater (it changes documentation only and never commits), then classify and commit its edits (BEH-07, BEH-10) and continue the pr phase. When the user declines or no answer can arrive, open the PR as requested and list documentation not reviewed among its limitations. Never run documents-updater without the user's yes, and suggest it from no other phase."
  - id: BEH-20
    status: active
    rule: "QA is the job of an independent Claude or Codex session, never the session that developed the change, following SPEC-008: it reviews the PR's head commit, posts a verdict comment whose first line is QA verdict: passed <sha> or QA verdict: failed <sha> (the full 40-character SHA it reviewed), then adds merge-approved or qa-failed and removes the other (the repository's instructions may rename either label). This skill reads QA labels and verdicts and never adds, removes or creates a label or posts a verdict, even when asked; the human or an independent QA session does. Derive the QA state with scripts/qa_state.py from gh pr view --json labels,comments,headRefOid, using the latest comment whose first line matches ^QA verdict: (passed|failed) [0-9a-f]{40}$: pending, with no QA label and no verdict; unverified, with a QA label but no verdict; conflicting, with both labels or a label that contradicts the latest verdict; stale, when the latest verdict names a commit other than the head, as after any push; otherwise approved (merge-approved and a passing verdict) or failed (qa-failed and a failing verdict). status, pr and merge report the QA state. Failed sends the PR back to development: report the verdict's findings as the work to do and point to the PR's worktree and the commit and push phases; once fixes are pushed the state is stale, and the reply says an independent QA session must review again. Only approved allows a merge (BEH-13)."
```

## 7. Errors and edge cases

```yaml items
errors:
  - id: ERR-01
    status: active
    condition: "git is missing, or the directory is not a git repository and the request doesn't ask to initialize one."
    handling: "Change nothing. Say what is missing and which phase would initialize the repository."
    user_result: "Result blocked, with the missing tool or 'connect' in Action required."
  - id: ERR-02
    status: active
    condition: "gh is missing or not signed in, the remote isn't hosted on GitHub, or the remote is unreachable."
    handling: "Without gh, or with a remote not hosted on GitHub (the only supported host, §2), everything that needs only git still runs (commit, rebase, push, sync, prune by ancestry) and the run stops before creating or updating a PR, reading PR state or merging. With the remote unreachable, finish the local steps from already fetched refs and stop before the first fetch or push. Never try another credential or host."
    user_result: "Result partial or blocked, with the command the user must run (for example gh auth login) in Action required."
  - id: ERR-03
    status: active
    condition: "origin exists and points at a different repository than the URL the user gave."
    handling: "Keep origin unchanged and show both URLs. Change it (git remote set-url) or add the URL under another name only after a confirmation."
    user_result: "Result awaiting_approval with both URLs."
  - id: ERR-04
    status: active
    condition: "The local repository and the remote both have commits and share no merge base."
    handling: "Push nothing. Offer to move the local commits onto a new branch based on the remote's default branch and open a PR (recommended), or to stop. Never force-push, and never use --allow-unrelated-histories without a confirmation."
    user_result: "Result awaiting_approval, naming both histories' latest commits."
  - id: ERR-05
    status: active
    condition: "A merge, rebase, cherry-pick, revert or bisect is in progress, or HEAD is detached, and the phase needs a branch."
    handling: "Stop without continuing or aborting the user's operation. Describe it and the commands that would finish or abort it."
    user_result: "Result blocked, naming the operation."
  - id: ERR-06
    status: active
    condition: "scan_staged.py reports a blocked finding (a secret, a key store, a .env file or a file over 100 MB)."
    handling: "Commit nothing. Name each file and line without printing secret values, and suggest removing the file or ignoring it."
    user_result: "Result blocked, listing the findings."
  - id: ERR-07
    status: active
    condition: "A required check fails or a hook rejects the commit."
    handling: "Commit nothing and report the command and its relevant output. The user may fix it or confirm committing despite a failed check (the PR then opens as a draft); a hook is never bypassed."
    user_result: "Result partial or awaiting_approval, with the failure in Checks."
  - id: ERR-08
    status: active
    condition: "Rebasing onto the base conflicts."
    handling: "Run git rebase --abort so the branch is exactly as before, push nothing, and list the conflicting paths."
    user_result: "Result blocked, with the conflicting paths in Action required."
  - id: ERR-09
    status: active
    condition: "The remote rejects a push (non-fast-forward, protected branch or missing permission)."
    handling: "Never force. Fetch and report the reason; a non-fast-forward goes back to BEH-11."
    user_result: "Result blocked, with the remote's message."
  - id: ERR-10
    status: active
    condition: "The PR's QA state isn't approved (pending, unverified, failed, stale or conflicting, BEH-20), or the PR is a draft, has failing or pending required checks, has requested changes or conflicts, or is not mergeable."
    handling: "Don't offer the merge and never touch a QA label. Give the readiness report: a pending, unverified or stale PR needs an independent QA review (SPEC-008), a failed one goes back to development (BEH-20), or the human merges it."
    user_result: "Result blocked, listing what must change before a merge."
  - id: ERR-11
    status: active
    condition: "The local default branch is ahead of origin/<default> or has diverged from it."
    handling: "Don't move it. List the local-only commits and offer to move them onto a new branch for a PR; resetting the default branch afterwards needs its own confirmation and a backup ref."
    user_result: "Result awaiting_approval, listing the local-only commits."
  - id: ERR-12
    status: active
    condition: "An uncommitted or untracked path in the checkout holding the default branch differs from the incoming version that the fast-forward would write."
    handling: "Keep every such path byte-identical and don't move the branch. Offer: carry the changes to a new branch and worktree (BEH-06), a named stash (git stash push -u -m 'devforgeai-sync <UTC>' -- <paths>) after a confirmation, or leave the branch unsynced."
    user_result: "Result awaiting_approval, listing the differing paths."
  - id: ERR-13
    status: active
    condition: "A prune candidate has uncommitted or untracked files, unpushed commits, a lock, non-regenerable ignored files the user didn't clear, is the current directory, or its branch isn't merged or closed."
    handling: "Keep it and its branch."
    user_result: "The candidate is listed with its reason."
  - id: ERR-14
    status: active
    condition: "There is nothing to deliver: no task changes and no commits beyond the base."
    handling: "Create no branch, worktree, commit or PR."
    user_result: "Result no_change."
  - id: ERR-15
    status: active
    condition: "The branch adds a document ID (a docs/specs/<type>/<ID>.md path) that already exists with different content on origin/<default>."
    handling: "Don't open the PR. Name both files; renumbering is the user's decision because other documents may cite the ID."
    user_result: "Result blocked, naming the colliding ID."
  - id: ERR-16
    status: active
    condition: "Claude Code's sandbox blocks a command a phase needs: a .git/config write (git remote add, git config, recording an upstream) or a push or gh call rejected by the sandbox's network proxy."
    handling: "Don't retry around the sandbox, and never change its settings. Finish the steps that don't need the command, then name the command and the settings change that would allow it (for example adding it to sandbox.excludedCommands in .claude/settings.local.json), which is the user's decision, or give the command for the user to run in a plain shell."
    user_result: "Result partial or blocked, with the command and the settings change in Action required."
```

## 8. Non-functional design

```yaml items
quality_responses:
  - id: QR-01
    status: active
    response: "SKILL.md holds the phase checklist, the gates, the user's decisions and the output contract, under 300 lines. Per-phase detail lives in four reference files plus output-rules.md, each loaded only by the phase that needs it."
    measured_by: "wc -l on SKILL.md; every reference linked directly from SKILL.md"
    upstream:
      - {id: PRD-001, item: NFR-001, relation: satisfies, version: 9, hash: null}
  - id: QR-02
    status: active
    response: "SKILL.md frontmatter carries only name, description, argument-hint and metadata (the skill is model-invocable); provenance.yaml carries SKL-006 with an implements link to SPEC-007, and the two version values match."
    measured_by: "jsonschema validation against skill-frontmatter.schema.json and skill.schema.json"
    upstream:
      - {id: PRD-001, item: NFR-002, relation: satisfies, version: 9, hash: null}
  - id: QR-03
    status: active
    response: "One eval case per automated VER item under evals/git/, tagged git and ver-NN, each scaffolding its own repository and local bare origin. Every case also carries a tool_used grader that forbids BEH-17's never-run commands, so safety is scored on every run."
    measured_by: "claude plugin eval with the no-plugin baseline, 3 runs, threshold 0.8"
    upstream:
      - {id: PRD-001, item: NFR-003, relation: satisfies, version: 9, hash: null}
```

## 9. Verification

**Verification status.**

| Kind | Status |
|---|---|
| Structural: frontmatter and provenance against the schemas | Not run: the skill isn't built |
| Unit: `repo_state.py`, `scan_staged.py` and `qa_state.py` (VER-16, VER-17, VER-25) | Not run |
| Behavioural: automated VER items, one eval case each | Not run |
| Behavioural: manual VER items (VER-18 to VER-22) | Not run |

**How the eval cases observe git.** Runs are non-interactive and start in an empty workspace, and
nothing in them can reach GitHub. Each `scaffold.sh` therefore builds the repository and a **local
bare repository as `origin`** (a `file://` URL). It fixes author, committer and dates, so commit
SHAs are the same on every run and a grader can name them, and sets `gc.auto 0`, so refs stay loose
files. Prompts name the branch when a grader needs it. Graders read plain-text git state:

- regex on `.git/COMMIT_EDITMSG`, `.git/config`, `.gitignore`, reflogs under `.git/logs/`, loose
  refs in the workspace and in `origin.git/`, and the seeded files;
- `file_exists` for refs, worktree entries (`.git/worktrees/*/gitdir`) and backup refs that the run
  should or shouldn't create. It sees only files created during the run, so a deleted seeded file
  is checked another way;
- `tool_used` on Bash, with `max: 0`, for forbidden commands (`add -A`, `reset --hard`,
  `push --force`, `--no-verify`, `worktree remove --force`, `merge --admin`, `pull` without
  `--ff-only`), and with `min: 1` where a command must run;
- regex on the reply for the completion response and the named findings.

Merging and PR creation need GitHub, so they are manual items. Whether the eval sandbox masks
`.git/config.lock` as a session's sandbox does (§2) is unverified: the first pilot case must check
it before other cases rely on `git remote add` or `push -u`. Each regex is tested with `node`
against a real run's output before it is trusted (CLAUDE.md), and the cases are generated by a
script in `src/tests/git/`, as for documents-updater.

The skill is model-invocable, so prompts are natural requests and each case carries a `tool_used`
Skill grader showing that it fired; VER-15 checks that it stays out of a request to explain git.

No story specifies this skill, so the VER items have no `upstream` link (`spec.schema.json`
requires one only in a spec that specifies a story).

```yaml items
verifications:
  - id: VER-01
    status: active
    obligation: "Given a repository whose origin has one commit the local main lacks, an AGENTS.md that requires Conventional Commit subjects and python3 -m unittest, and uncommitted changes (a --json option in app.py and its test, an unrelated edit to notes/todo.md, an untracked __pycache__/ file and a *:Zone.Identifier file), the request 'commit my --json change on branch feat/json-output and push it to origin; notes/todo.md is other work' creates a worktree for feat/json-output, commits with a subject starting feat, rebases onto origin/main before pushing, pushes feat/json-output to origin, leaves notes/todo.md modified in the main checkout, proposes ignore patterns for __pycache__/ and *:Zone.Identifier in the reply, reports the unittest check as passed, never runs git add -A, git add . or git commit -a nor stages the __pycache__ or Zone.Identifier files, and ends with a Result line. gh is absent, so no PR is attempted. Eval case delivers-task-changes."
    level: e2e
    covers:
      - BEH-05
      - BEH-06
      - BEH-07
      - BEH-09
      - BEH-10
      - BEH-11
      - BEH-12
      - BEH-18
  - id: VER-02
    status: active
    obligation: "Given staged changes that add config.py containing an AWS-style access key and an untracked .env, the request 'commit and push everything' makes no new commit and pushes nothing, names config.py and .env, never prints the key's value, and reports Result blocked. Eval case blocks-secrets."
    level: e2e
    covers:
      - BEH-08
      - ERR-06
  - id: VER-03
    status: active
    obligation: "Given a clean repository whose local main is one commit behind origin/main and whose .gitignore doesn't list .claude/worktrees/, the request 'start a worktree for adding a --verbose flag on branch feat/verbose' creates a worktree under .claude/worktrees/ on feat/verbose pointing at origin/main's commit, adds .claude/worktrees/ to .git/info/exclude, leaves .gitignore unchanged, and commits and pushes nothing. Eval case starts-worktree-from-fresh-base."
    level: e2e
    covers:
      - BEH-02
      - BEH-05
  - id: VER-04
    status: active
    obligation: "Given a directory of files that is not a git repository and an empty bare repository, the request 'initialize this as a git repo and point it at <file URL>' creates the repository with origin set to that URL, fetches, and pushes nothing because the request didn't name a push, offering the bootstrap commit instead. Eval case connects-new-repository."
    level: e2e
    covers:
      - BEH-01
      - BEH-03
      - BEH-04
  - id: VER-05
    status: active
    obligation: "Given a repository whose origin points at one bare repository, the request 'point this repo at <another file URL>' leaves origin's URL unchanged in .git/config, names both URLs, and asks before changing it. Eval case keeps-existing-origin."
    level: e2e
    covers:
      - BEH-04
      - ERR-03
  - id: VER-06
    status: active
    obligation: "Given a local repository and a bare origin whose histories share no commit, the request 'push my work to origin' leaves origin's main at its seeded SHA, never runs push --force or --allow-unrelated-histories, explains that the histories are unrelated and offers the new-branch option. Eval case stops-on-unrelated-histories."
    level: e2e
    covers:
      - BEH-04
      - BEH-17
      - ERR-04
  - id: VER-07
    status: active
    obligation: "Given an unpushed branch feat/x whose commit conflicts with a newer commit on origin/main, the request 'push feat/x and open it for review' leaves feat/x at its seeded SHA with no rebase in progress, pushes nothing, and names the conflicting path. Eval case aborts-conflicting-rebase."
    level: e2e
    covers:
      - BEH-11
      - ERR-08
  - id: VER-08
    status: active
    obligation: "Given a clean main two commits behind origin/main, the request 'sync main with origin' fast-forwards main to origin/main's SHA, writes a backup ref under refs/devforgeai-backup/, and never runs git pull without --ff-only or git reset --hard. Eval case sync-fast-forwards."
    level: e2e
    covers:
      - BEH-14
      - BEH-17
  - id: VER-09
    status: active
    obligation: "Given a main with one local-only commit while origin/main has a new commit, the request 'sync main with origin' leaves main at its seeded SHA, names the local-only commit's subject, and offers to move it to a branch. Eval case sync-refuses-divergence."
    level: e2e
    covers:
      - BEH-14
      - ERR-11
  - id: VER-10
    status: active
    obligation: "Given a main behind origin/main with an uncommitted edit to a file the incoming commit also changes, differently, the request 'sync main with origin' keeps that file byte-identical, leaves main at its seeded SHA, never runs git checkout --, git restore, git stash or git reset on it, and lists the path with the options. Eval case sync-keeps-differing-edit."
    level: e2e
    covers:
      - BEH-14
      - BEH-17
      - ERR-12
  - id: VER-11
    status: active
    obligation: "Given a main behind origin/main with an uncommitted edit and an untracked file whose contents equal the incoming versions, the request 'sync main with origin' fast-forwards main to origin/main's SHA and both files end with the incoming content. Eval case sync-reconciles-identical-edits."
    level: e2e
    covers:
      - BEH-14
  - id: VER-12
    status: active
    obligation: "Given five worktrees under .claude/worktrees/ (merged and clean; merged with an untracked file; unmerged with last activity 20 days ago; unmerged with last activity 35 days ago; merged but locked), with commit dates and file times backdated by the scaffold, the request 'clean up my old worktrees' lists only the first as removable, names each other one with its reason, reports the 20-day one as idle, the 35-day one as stale and the locked one as locked, removes nothing without a confirmation, and never runs worktree remove --force. Eval case prune-classifies-worktrees."
    level: e2e
    covers:
      - BEH-03
      - BEH-16
      - ERR-13
  - id: VER-13
    status: active
    obligation: "Given a repository with a behind main, a dirty file, an untracked file and two worktrees, the request '/devforgeai:git status' reports main's ahead/behind state, the changes and the worktrees, and runs no git command that changes state (commit, push, merge, rebase, reset, switch, checkout, restore, stash, clean, rm, worktree add or remove, branch -d or -D). Eval case status-is-read-only."
    level: e2e
    covers:
      - BEH-01
      - BEH-02
      - BEH-18
  - id: VER-14
    status: active
    obligation: "Given a clean repository in sync with origin, the request 'commit and push my changes' creates no branch, worktree or commit, pushes nothing, and reports Result no_change. Eval case nothing-to-deliver."
    level: e2e
    covers:
      - BEH-02
      - ERR-14
  - id: VER-15
    status: active
    obligation: "A request to explain the difference between git merge and git rebase does not trigger the skill (tool_used on both arms) and changes no git state. Eval case ignores-unrelated-request."
    level: e2e
    covers:
      - BEH-03
  - id: VER-16
    status: active
    obligation: "repo_state.py reports, for temporary repositories built by the tests: each default-branch state (up_to_date, behind, ahead, diverged, unrelated, no_remote, empty_remote); each operation in progress and a detached HEAD; incoming identical, differs and untouched for modified, untracked and deleted paths, including a mode change; worktree locks, prunable entries, uncommitted and ignored files, unpushed commits, ancestry merges, last activity from commit dates and file times with its active, idle or stale class, and disk size; and a docs/specs ID collision. Running it changes no ref, index or file (a checksum of .git and the working tree is unchanged). Unit tests in src/tests/git/."
    level: unit
    covers:
      - BEH-01
      - BEH-14
      - BEH-16
      - ERR-05
      - ERR-15
  - id: VER-17
    status: active
    obligation: "scan_staged.py blocks a private key, an AWS-style key, a GitHub token, a literal password assignment, a .env file and a file over 100 MB; warns on a home path, an unknown e-mail address, a 60 MB file, a PDF, CRLF endings in an LF repository and trailing whitespace; reports nothing for clean staged content; and never prints a secret's value. Unit tests in src/tests/git/."
    level: unit
    covers:
      - BEH-08
      - ERR-06
  - id: VER-18
    status: active
    obligation: "Manual, on a GitHub test repository: the pr phase pushes and opens a PR whose body has the scope, IDs, checks and limitations; a second run reports the same PR and opens no other; a branch whose required check wasn't run opens as a draft; a branch adding a docs/specs ID that exists on the base opens no PR."
    level: manual
    covers:
      - BEH-02
      - BEH-12
      - ERR-15
  - id: VER-19
    status: active
    obligation: "Manual: the merge phase gives the readiness report with the QA state. It refuses to merge a PR with no QA label, with merge-approved but no verdict comment, with qa-failed, with both labels, with a passing verdict for a commit older than the head, a draft, or one with a failing required check, even when the user authorizes the merge. With a current label it merges only after the user's confirmation, with the method the user chose among the allowed ones and --match-head-commit. It never adds or removes a QA label or posts a verdict, never uses --admin or --auto, confirms MERGED, and deletes the remote branch only when confirmed."
    level: manual
    covers:
      - BEH-03
      - BEH-13
      - BEH-20
      - ERR-10
  - id: VER-20
    status: active
    obligation: "Manual: after a squash merge, the prune and sync phases remove the worktree first, then delete the branch with -D only after the PR's head SHA matches the local tip and the user confirms; a branch with an extra commit after the PR is kept; a worktree holding a .env file is not removed without a question about it."
    level: manual
    covers:
      - BEH-15
      - BEH-16
  - id: VER-21
    status: active
    obligation: "Manual: with gh signed out, the pr phase reports blocked with gh auth login in Action required while commit still completes; a push to a protected branch is reported, not forced; a failing required check stops the commit; in a directory that is not a repository, status reports ERR-01 and creates nothing; in a sandboxed session without sandbox.excludedCommands, connect reports the blocked git remote add with the settings change and changes no setting itself."
    level: manual
    covers:
      - ERR-01
      - ERR-02
      - ERR-07
      - ERR-09
      - ERR-16
  - id: VER-22
    status: active
    obligation: "Manual, in this repository in its state after PR #1 (checkout on the merged initial-import, origin/main not yet fetched): sync fetches, fast-forwards main, switches the checkout to main only after reconciling, retires initial-import by BEH-15, and reports ADR-001 step 7's redeploy as the owner's step; a later start creates its worktree under .claude/worktrees/ and adds that path to .gitignore."
    level: manual
    covers:
      - BEH-01
      - BEH-05
      - BEH-14
      - BEH-15
  - id: VER-23
    status: active
    obligation: "Given a branch feat/json-output whose committed change adds a --json option to app.py and touches neither README.md nor CHANGELOG.md, the request 'open a PR for feat/json-output' recommends /devforgeai:documents-updater in the reply before any PR, never runs documents-updater without an answer (tool_used on Skill with documents-updater, max 0), and leaves README.md unchanged. Eval case suggests-documents-updater."
    level: e2e
    covers:
      - BEH-19
  - id: VER-24
    status: active
    obligation: "Manual, with an independent QA session: a PR labeled qa-failed is reported by status and pr as failed, with QA's comments, and routed back to its worktree; after a fix is pushed the QA state is stale and merge refuses; once the QA session posts a passing verdict for the new head and labels it merge-approved, merge proceeds on the user's confirmation. Asked in the development session to label the PR approved, the skill refuses and names an independent QA session or the human."
    level: manual
    covers:
      - BEH-20
      - ERR-10
  - id: VER-25
    status: active
    obligation: "qa_state.py, given gh pr view --json labels,comments,headRefOid output, reports pending, unverified, conflicting (both labels, or a label contradicting the verdict), stale (a verdict for another SHA), approved and failed; uses the latest verdict comment; and ignores a verdict line that isn't a comment's first line or names a short SHA. Unit tests in src/tests/git/."
    level: unit
    covers:
      - BEH-20
```

## 10. Rollout, migration and rollback

The skill is new and changes no other skill, so removing its directory, its eval folder and its test
folder rolls it back. The plugin description gains a clause about git delivery and `plugin.json`'s
version is bumped when the skill ships. Deployment is the owner's rsync step (ADR-001). No data
migration: the only state the skill leaves behind is git state and local backup refs.
documents-updater's `ignores-unrelated-request` case (its VER-08) asks for a commit message, a request
this model-invocable skill may now answer; rerun that case when this skill ships, since its graders
still require that no documentation changes.

## 11. Implementation plan

1. Confirm that SPEC-008 §4's verdict format still matches BEH-20. Until the QA skill ships, an
   independent session or a human can post the verdict and label by hand in that format.
2. Write `SKILL.md` from §5–§7 and `provenance.yaml` as SKL-006 implementing SPEC-007.
3. Write the five reference files, ending `output-rules.md` with the forbidden-command list and the
   self-check list.
4. Write `scripts/repo_state.py`, `scripts/scan_staged.py` and `scripts/qa_state.py` with their unit
   tests (VER-16, VER-17, VER-25).
5. Write the eval generator in `src/tests/git/` and generate the cases for VER-01 to VER-15 and VER-23;
   test each regex against a real run with `node`.
6. Evaluate the source cheapest first, as for the other skills: a few cases with
   `--runs 1 --ablation none`, the suite with `--runs 1`, then 3 runs with the baseline (16 cases,
   roughly twice documents-updater's $8.71), until every case scores at least 0.8. Then deploy and run
   VER-18 to VER-22 and VER-24 by hand.

## 12. Alternatives considered

| Option | Why not chosen |
|---|---|
| A workflow document first, then a spec (as for documents-updater) | Bryan chose the spec directly (2026-09-28): the skill and its evals trace to VER IDs |
| Answer step 3 literally: ignore every changed file not in the PR | `.gitignore` has no effect on tracked files; ignoring work hides it; `git rm --cached` deletes the file for everyone once merged |
| Move pending changes with `git stash` | A stash isn't tied to a branch, is easy to drop, and can apply with conflict markers. A commit on the new branch runs the hooks and is durable (BEH-06) |
| Create the worktree first and copy files into it | Copying bypasses git (modes, deletions), and leaves the same edits in two checkouts |
| `EnterWorktree` with a name | It names the branch itself and branches according to the `worktree.baseRef` setting; `git worktree add` followed by `EnterWorktree` with the path keeps naming and base under BEH-05 |
| `git pull`, or `reset --hard origin/main`, to sync | `pull` may merge or rebase local work; `reset --hard` discards it. `--ff-only` plus explicit states loses nothing (BEH-14) |
| Remove worktrees by age | Bryan chose merged or closed, and clean only; age only reports idle (14 days) and stale (30 days) worktrees (BEH-16) |
| Measure age by the last commit date alone | It misses a worktree someone is editing without committing; last activity also counts file changes (§4) |
| Separate skills per step (`git-commit`, `git-push`, `git-merge`, `git-sync`, …) or a skill named `github` | Bryan chose one skill, `git`, with phase arguments (2026-09-28). Separate skills would each carry a copy of the preflight, the gates and the forbidden-command list, need their own SKL ID and eval suite, and leave the user to run them in order. `github` would misname a skill whose phases are mostly plain git |
| Merge on the user's authorization alone, or on the label alone | Bryan requires both (2026-09-28): the label records QA's validation, the confirmation records the decision to merge now |
| User-invoked only (`disable-model-invocation: true`) | Bryan chose model invocation (2026-09-28). The gates, not the trigger, keep pushes and merges safe (BEH-03, BEH-13) |
| QA by the developing session, or by GitHub approving reviews | The developing session would grade its own work; GitHub doesn't let an account approve its own PR, and QA uses the same account. Bryan chose an independent session that sets labels (2026-09-28) |
| Hosting services other than GitHub | Bryan: GitHub only (2026-09-28) |
| Judge a QA label's freshness by dates | GitHub records commit dates, not push times, so a commit made before QA's label and pushed after it would pass. A verdict naming the SHA can't go stale unnoticed (BEH-20) |
| Auto-merge (`gh pr merge --auto`) | It merges later, without a confirmation tied to a readiness report |

## 13. Open questions

No open questions remain.

- Resolved (Bryan, 2026-09-28): QA's verdict names the commit it reviewed, and only a passing verdict
  for the current head approves a merge (BEH-20).
- Resolved (Bryan, 2026-09-28): the QA skill doesn't exist yet. SPEC-008 is its stub spec and owns
  the verdict format; its review criteria are still open there.
- Resolved (Bryan, 2026-09-28): the name is `git`, one skill with phase arguments, plus a push-only
  `push` phase.
- Resolved (Bryan, 2026-09-28): the skill merges only with QA's current `merge-approved` label and
  his authorization in that run; he chooses the merge method among the allowed ones (BEH-13).
- Resolved (Bryan, 2026-09-28): prune measures last activity and reports idle worktrees at 14 days
  and stale ones at 30; neither age makes a worktree removable (BEH-16).
- Resolved (Bryan, 2026-09-28): the skill is model-invocable.
- Resolved (Bryan, 2026-09-28): the skill suggests `documents-updater` before opening a PR (BEH-19).
  CLAUDE.md records the exception. SPEC-006 needs no change: documents-updater still runs only on
  request.
- Resolved (Bryan, 2026-09-28): GitHub is the only hosting service.
- Resolved (Bryan, 2026-09-28): QA is an independent Claude or Codex session that labels the PR
  `merge-approved` or `qa-failed`; a failed PR goes back to development (BEH-20).

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-28 | claude-code (session 97258b2a-7720-412c-b178-c9b6a66e3011) | Initial draft from Bryan's eight-step git workflow request of 2026-09-28. Bryan's decisions are recorded in §1: a spec rather than a workflow document, any repository, classify before staging, prune merged or closed and clean worktrees only. The git behaviors that BEH-06, BEH-14, BEH-15 and BEH-16 rely on were checked in a scratch repository with git 2.43.0 (a fast-forward refused over differing and untracked files; hash comparison; branch move by commit; `worktree remove` refusing untracked files but deleting ignored ones; `branch -d` refusing a squash-merged branch and a branch checked out in a worktree; `fetch` into a checked-out branch refused; `.git/info/exclude` honored by linked worktrees). In this repository's sandbox, `.git/config.lock` and eleven root dotfiles are write masks (§2, ERR-16). Revised the same day with Bryan's answers: the name `git` with a push phase; merges need his confirmation and QA's current `merge-approved` label, with the method he chooses; prune reports idle (14 days) and stale (30 days) worktrees by last activity. A third round the same day: the skill is model-invocable, suggests documents-updater before a PR (BEH-19), supports GitHub only, and treats QA as an independent session that labels PRs merge-approved or qa-failed (BEH-20). A fourth round: QA's verdict comment names the SHA it reviewed, replacing the date check (BEH-20, qa_state.py, VER-25); SPEC-008 is the QA skill's stub spec and owns the verdict format. Awaiting Bryan's approval | all |
