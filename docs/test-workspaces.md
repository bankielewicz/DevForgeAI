# Default test workspaces: fresh Git worktrees

Owner-approved default, 2026-09-10. Ordinary testing and test installation use a fresh Git worktree selected from task context, so that an end user is not asked to choose a test directory for routine validation. This document records that default and how to apply it through the existing environment-preparation path. It does not implement sandboxing, worktree selection in the Rust CLI, installer destination compatibility, or any change to a skill package.

The concurrent-session rules in the [execution contract](mvp/execution-contract.md#worktree-assignment-for-concurrent-sessions) and the evaluator's [worktree environment setup](../providers/codex/plugins/devforgeai/skills/devforge-evaluate-expert/references/worktree-environment.md) remain the governing sources for record formats and command semantics. This page adds the default choice; it adds no new record, phase, question or approval ceremony.

## The default

For routine test preparation:

1. Derive the consuming Git repository and base from the selected project or fixture and the current task. The base is that repository's observed current HEAD unless the task assigns another existing revision; resolve the full commit ID.
2. Create one fresh task-owned worktree by default. Detached checkout is the routine choice for disposable testing; create a branch only when the task itself must commit or publish from that worktree.
3. Report the resolved repository, base commit and absolute worktree path in the existing task record before dependent work begins.

One worktree is the default count. Create more only for a concrete test need that the task states, such as independent attempts that must not share state. Existing Git commands are sufficient:

```text
git -C <repository-root> worktree list --porcelain
git -C <repository-root> worktree add --detach <new-worktree-path> <resolved-base-commit>
```

Inspect the current worktree inventory first. Reject an occupied or overlapping destination, including any protected root or another session's allocation; choose a different fresh path instead of reusing, pruning or overwriting.

## Choosing the location

Prefer the project's configured worktree location when one exists. When none is configured, select an available task-owned location from project context that satisfies the required separation from the original checkout, the framework source and any protected authority, source or evidence paths.

Do not prompt for a routine directory when one can safely be derived. This workspace's authorized parent is `/home/bryan/Projects/DevForge/worktrees`; treat that as a local configuration example, not a universal path for other users or projects.

An explicit choice of an existing environment overrides the default. Static review without any test environment also remains available where the applicable skill offers it. The evaluator's three options (create worktrees, use an existing environment, static review only) are unchanged; this default supplies the carried prior selection that its reuse-a-previous-explicit-selection step already honors, so the environment question is resolved for current work and is not re-asked.

## When to ask instead

Ask only the necessary question, naming the concrete missing prerequisite, when:

- no Git repository or base can be derived from the selected project, fixture and task;
- an ownership or access conflict at the derived repository or destination cannot be resolved from context;
- no destination satisfies the required separation.

Do not silently initialize or clone a repository, substitute an unrelated project, or select a destination inside a protected path to avoid asking.

## Scope of the default

The default applies to testing and to test installation of framework packages into the test worktree. A successful test does not install into, or adopt packages for, the user's actual working project. Adoption into a real project is a separate operation using that project's context and its own authorization.

## What a worktree does and does not provide

Worktrees give separate checked-out files. They share Git metadata, configuration and credentials with the original checkout and are not a security sandbox. Verify required authority, source-visibility and evidence boundaries separately, using the applicable contract's own checks.

Creating a worktree does not:

- grant model, authentication or budget authority, or establish native readiness;
- authorize installation into any project, including the test worktree; installation must be covered by existing task authorization and applicable checks;
- authorize deleting or pruning the worktree, another worktree or the original checkout afterward.

Preserve original checkouts, existing worktrees and recorded evidence. Retain task-owned test work until the applicable cleanup decision; completion of a test never authorizes cleanup on its own.

## Relation to existing acceptance inputs

The current installer acceptance set names the original project root. Its historical bytes remain unchanged. Explicit support for a selected test destination, and any reuse of earlier evidence at that destination, belongs to the installer and contract owner's separate work. This document does not authorize silently replacing that binding, and worktree creation alone does not demonstrate destination compatibility. Historical freeze-timing changes also remain unapproved and are not decided here.

## Enforcement boundary

This is workflow guidance. No automatic scheduler, background orchestration, worktree manager or additional approval step is part of this default. Where enforcement is needed, it belongs in the compiled Rust DevForge CLI through supported hooks or commands that control the dependent action, as the [development language policy](development-language-policy.md#phases-hooks-and-skill-content) describes. Nothing here claims that such enforcement, automatic selection or a Rust selector has been implemented.
