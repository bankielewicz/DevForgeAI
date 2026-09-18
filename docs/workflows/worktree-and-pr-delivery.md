# Worktree and PR delivery

This procedure implements the repository change-and-delivery guidance in
[AGENTS.md](../../AGENTS.md#repository-changes-and-delivery). Read it when a task
will change repository source, skills or documentation, or publish Git changes.
Discussion and read-only inspection do not require it. If a task becomes a change
request, load it before editing or selecting an authoring destination.

This is repository-level coordination around the selected workflow. It does not
expand a skill's responsibility, implement a protected Rust gate, or grant
framework acceptance. Ordinary host permissions and approval requirements apply.

## Authorization and scope

A repository change request authorizes the necessary task branch/worktree,
selected edits, commits, push to the verified origin, and a draft PR against the
selected base. Reuse that authorization rather than asking for it at every step.
Explicit limits such as "local only", "do not push", a selected checkout or a
different base take precedence. Never reinterpret a read-only request as
permission to edit or publish.

Merge, installation, deployment, operational configuration changes and invoking
another workflow require their own applicable authorization. A draft PR may
publish incomplete work honestly; its existence does not imply tests passed.
If a user-selected destination conflicts with worktree isolation, resolve that
specific conflict before dependent changes instead of silently changing the path.

## Preflight and task worktree

1. Inspect the selected root, applicable instructions, branch/HEAD, staged and
   unstaged changes, untracked task inputs, origin URL and registered worktrees.
   Use bounded status summaries for large trees. Confirm the remote belongs to
   the selected project before sending content.
2. Fetch origin and record the intended base commit. Default to `origin/main`;
   an explicitly selected base or continuation branch takes precedence. A failed
   fetch cannot be described as a current remote observation. Preserve local work
   and report any authentication/network/permission blocker.
3. Determine whether the task depends on uncommitted or local-only inputs that
   are absent from the base. Identify the exact dependency before authoring; do
   not silently omit it, transfer unrelated edits or copy the entire checkout.
   Carry selected inputs only within the task's authorization, preserving their
   source bytes and provenance. Ask about a material ownership/base conflict.
4. Create a unique branch, for example `docs/<task>`, `feat/<task>` or
   `fix/<task>`, and an actual Git worktree using `git worktree add`. Place new
   task checkouts under `<primary-checkout>/worktrees/git/<task-name>/`.
   Identify the primary checkout through Git's worktree/common-directory
   information, not the current directory's name. Check branch/path collisions
   and path components before creation; never overwrite or create a nested
   worktree inside an existing task checkout.
5. Reuse an existing task worktree only after verifying its resolved path,
   branch, source identity, ownership, changes and task continuity. Do not check
   out a branch already in use elsewhere or bypass Git's protection with force.
   A directory named `worktrees` is not evidence of Git registration, and a
   linked worktree normally has a `.git` file rather than a `.git` directory.
6. In the task worktree, confirm the actual root, branch/HEAD, base and applicable
   AGENTS.md instructions before edits. Keep the primary checkout and other task
   checkouts unchanged. A dirty primary checkout need not block independent work
   from a verified base, but its relevant unpublished changes must be accounted
   for. Do not stash, reset, clean or switch someone else's checkout.

Use native Windows PowerShell for this repository. The existing `/worktrees/`
ignore rule in the primary checkout keeps nested checkout contents out of its
index; the task worktree still tracks its own repository files normally. Do not
force-add the parent worktrees directory, and do not recurse into other checkouts
or archived evidence during discovery or source capture.

## Execute the selected workflow

Use the task worktree as the root for edits, commands and task-local evidence.
Repository-relative paths resolve there. Identify separately selected external
inputs explicitly; do not rewrite their location or assume files ignored in the
primary checkout exist in the new checkout.

For skill-builder, select and report
`<task-worktree>/src/agents/skills/<skill-name>/` before preparing the authoring
contract/design. Honor an explicit alternative development destination. Resolve
any literal primary-checkout destination conflict before staging, because the
authoring records bind actual roots and paths. Keep input, target and evidence
roots disjoint and follow the selected package's evidence contract.

Finish the selected skill's outputs before performing repository delivery.
For skill-builder, that means source delivery/readback, authoring records and the
[manual validator handoff](../../.agents/skills/skill-builder/references/validation-handoff.md).
Do not run skill checkers, graders, native trials or skill-validator merely to
open its PR. Report validation/testing as NOT_PERFORMED unless separately selected
applicable evidence binds the exact candidate. Other workflows retain their own
required checks; documentation-only work uses factual/link/consistency review.

Do not edit operational skill copies unless that task explicitly selects them.
Do not copy or modify an operational project binding to make another worktree
appear activated. The existing [absolute-root binding limitation](../specs/framework/installation-and-integrations.md#setup-bootstrap-and-worktree-compatibility)
still applies; Git isolation alone does not qualify binding-required execution.
Missing prerequisites block the dependent workflow, not unrelated authorized work.

## Commit and open or update the PR

1. Review the complete task diff against the recorded base and inspect new files.
   Confirm scope, ownership, intended deletions, absence of credentials and
   generated artifacts, and preservation of unrelated bytes. Unexpected changes
   or concurrent edits need reconciliation; do not overwrite them to obtain a
   clean status.
2. Perform checks appropriate to the selected change and workflow. Record actual
   results, gaps and candidate identities. Use `git diff --check` for whitespace
   issues, but never present it as semantic validation or product QA. Do not
   invent test/coverage results for documentation-only changes.
3. Stage explicit task-owned paths, inspect the staged diff, and commit with a
   concise subject. Avoid repository-wide `git add .` or `git add -A` when other
   work or retained artifacts could be included. Do not force-add ignored raw
   evidence. If no source change is needed, report that outcome rather than
   manufacturing an empty commit or PR.
4. Push the explicit task branch to the verified origin and set its upstream to
   that remote task branch. A branch created from origin/main may initially track
   main; do not rely on an ambiguous default push. Never push task changes directly
   to main or force-push. If the remote branch advanced, inspect and reconcile its
   ownership and changes before retrying; no history replacement.
5. Create one draft PR against the selected base, or update the existing PR for
   this task branch. Lead with the problem and resulting behavior. Include scope,
   checks actually performed, known findings, missing validation and usable
   evidence/handoff references. For multiline GitHub CLI content, write exact
   text to a task-local file and pass `--body-file`.
6. Verify the remote branch/commit and PR base/head after publication. Return the
   PR URL, worktree path, branch, commit, verification status and next owner. A
   successful local commit is not proof of a push or PR. On publication failure,
   preserve the commit and report the concrete blocker without claiming delivery.

Keep the PR draft while mandatory validation or review is missing or failing.
Later readiness changes require applicable current evidence and the selected
delivery/review scope. Skill authoring does not automatically select independent
validation. Merge remains a separately authorized action even after checks pass.

## Evidence, concurrent work and cleanup

Keep task-required source, specifications and reviewable handoff information
available to their consumers. Raw execution workspaces, local archives and
generated artifacts remain local according to existing ignore rules and evidence
contracts. A required local-only artifact needs an explicit accessible handoff;
a dead absolute path in a PR is not sufficient. Do not publish secrets or add a
new broad evidence exclusion that hides a required tracked deliverable.

Worktree isolation prevents shared source-directory edits, but does not isolate
services, databases, ports, credentials or shared caches. Check ownership of such
resources before concurrent execution. Separate branches passing separately do
not establish combined-candidate integration success.

Do not automatically delete worktrees, branches, ignored evidence or archives
after publication or merge. First inspect uncommitted/untracked work, active
processes, other owners and evidence references to the checkout. Cleanup is a
separately selected task. Preserve path-bound evidence until an authorized
retention/relocation plan makes its handoff usable; never rewrite sealed history
or claim a copied/moved candidate inherited earlier validation automatically.

Resume by inspecting actual local and remote state, including whether a commit,
push or PR already succeeded. Reuse the existing task/PR when verified. Preserve
failed attempts and uncertain effects; do not replay mutations blindly or invent
a rollback. Fetch newer base changes before final delivery review; if integration
is needed, preserve commits, resolve conflicts within scope and repeat affected
checks. Do not automatically rebase another contributor's published work.
