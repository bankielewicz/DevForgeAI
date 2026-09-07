# Alternative test environment with Git worktrees

Use this branch for T01/T02 environment selection and T05 preparation. Its purpose is to provide a usable alternative test workspace when the user has no existing environment. The validator creates the selected workspaces and continues preparation; the user need not provision them beforehand. This is a conditional path inside existing Enforced tasks, not a new workflow or a model-controlled gate.

## Resolve the environment choice

Reuse a previous explicit selection. Otherwise ask:

"Which testing environment should skill-validator use?"

- **Create Git worktrees for validation (Recommended when none exists):** Create separate local test workspaces for candidate and baseline attempts, then prepare the runtime.
- **Use an existing validation environment:** Use the supplied assigned paths and establish readiness.
- **Continue with static review only:** Perform deterministic inspection, AI review, results and builder handoff; required native observations remain unavailable.

"No existing environment" does not select static-only. An unanswered or preselected choice does not authorize creation. Once creation is selected, carry that authorization forward through bounded setup without asking for the same permission again. Resolve only missing consequential inputs. "GitHub worktree" means a local Git worktree of the selected repository; this option needs no GitHub-hosted environment, remote branch or pull request.

## Prepare the assignment before freezing the plan

Use `runtime.environment_setup` in [validation-plan.json](../assets/validation-plan.json). Record the actual choice and its source. For existing or static-only mode, leave inapplicable Git fields null with a reason. For worktrees:

- Resolve the actual consuming Git repository, independently of the candidate skill directory. An outer workspace may contain several repositories or none. If ownership is unclear, ask which repository supplies the test project; do not initialize or clone one implicitly.
- Inspect repository identity, common Git directory, current commit/state and existing worktrees. Use the repository's native filesystem/client: for a WSL repository, operate inside its WSL distribution using Linux paths.
- Default the test-project base to the selected repository's observed current HEAD commit unless the assignment selects another existing revision. Resolve it to a full commit ID and record the selection basis. Use the same base for both arms. A Git base identifies project contents; frozen candidate/baseline manifests independently identify the skill bytes to install.
- Allocate fresh absolute paths under an assigned test-workspace parent, outside protected candidate/grader/source directories. Allocate a unique worktree, output directory and independent client-state directory for every planned case/arm/retry. Record these against the frozen attempt IDs. Resolve path aliases and reject overlap with another assignment or existing destination.
- Include the new worktree destinations and the narrow Git administrative writes needed to register them in the setup write fence. Linked worktrees share repository metadata; measured workers must not gain write access to the common directory or the original checkout.
- Retain frozen source, baseline, specification, cases and expectations outside worker-visible test inputs. Dirty candidate files remain part of their exact frozen snapshot; do not silently substitute the committed version.

Save and freeze the completed plan before provisioning. If a required path, assignment, base or budget is unresolved, complete independent work while requesting that input. Actual setup observations belong in a separate [environment-setup.json](../assets/environment-setup.json) record; do not edit frozen plan bytes to report progress.

## Create the selected workspaces

The following is the command shape, using resolved arguments through the actual shell or an argument-vector process API. It is not a command to run with literal placeholders:

```text
git -C <repository-root> worktree list --porcelain
git -C <repository-root> worktree add --detach <new-attempt-worktree> <resolved-base-commit>
```

Create each assigned attempt at the recorded base. Detached worktrees are the default for validation; no new branch is needed. If the user explicitly assigned a branch, record it and use the corresponding supported Git form after checking branch ownership and occupancy. Inspect applicable checkout hooks/filters before preparation; do not execute evaluated skill code or unassigned setup side effects through checkout.

Before each add, recheck destination absence and the common-directory/assignment identity. On success, retain command output, exit status and actual worktree path/HEAD/branch state in the setup evidence. On partial failure, preserve the created paths and metadata as failed preparation. Do not force reuse, reset, stash, commit, prune, remove worktrees, overwrite another destination or alter remote state to make setup succeed. A retry requires a newly assigned path and a new plan iteration if the frozen allocation changes.

Continue by staging the case's permitted raw facts and installing the **exact frozen** candidate or baseline runtime package through the supported installation mechanism. Preserve uncommitted candidate changes via their frozen bytes rather than changing the original checkout. Keep authored evals, held-out answers and source-only documents outside the worker view. If a checkout already contains another target installation, resolve that collision only inside this attempt's assigned disposable scope; otherwise request a suitable project or boundary. A without-skill baseline must not discover a target through ancestor, global or plugin paths.

## Continue to native readiness and testing

Prepare the subscribed client, separate history/memory and owned process arrangement for each attempt using the supported runtime surface. Subscription sign-in remains an operator interaction when required. Do not copy credentials or ordinary client stores, or assume Windows and WSL clients share authentication. Ask for sign-in at the concrete prepared workspace when it is the remaining dependency.

Then apply the actual boundary probes, installation observations and transcript controls in [native evaluation](native-evaluation.md#2-establish-an-actual-execution-boundary). Worktree preparation is not isolation proof: Git metadata is shared, a framework checkout may expose source-only material, and client state/authentication need their own arrangement. A source-readable sandbox cannot satisfy tier C source exclusion merely because the working directory changed.

When those prerequisites are observed, continue the frozen C, B and A schedule in the prepared environments. When unavailable, retain the delivered workspaces, identify each exact missing prerequisite and mark affected native observations COULD_NOT_RUN. Continue independent review and P5/P6 reporting. Never report that a created worktree proves a native test passed.

## Record the outcome and continuation

The setup template is a local evidence format, not a registered runtime admission schema. Fill known observations; use null and a cause for missing facts. Use these values:

- `workspace_status`: NOT_ATTEMPTED, PREPARED, PARTIAL, FAILED, or SKIPPED. PREPARED requires all assigned workspaces for the record's scope to exist at their recorded identities; PARTIAL preserves mixed outcomes.
- `native_readiness`: NOT_ESTABLISHED, READY, BLOCKED, or NOT_REQUESTED. READY requires the referenced installation, boundary, auth and observation evidence for that scope; worktree creation alone leaves NOT_ESTABLISHED.
- Each attempt retains its actual paths/state, provisioning evidence, installed manifest, boundary/auth references and missing prerequisites. References contain a saved absolute path and exact SHA-256; never include secrets. Snapshot each completed record separately and bind its identity in the corresponding run manifest's `environment_setup_ref`.

Report workspace preparation and native observations separately in verification results and handoff. Include retained workspace paths, source/base identities, outstanding setup and the next action needed to resume. Do not mutate a setup record already cited by a completed run; save a successor and preserve earlier evidence. Completion does not authorize cleanup or release of worktrees.

Mechanical admission and phase transitions remain the external runtime/operator's responsibility under existing H1/H2 proposals. This guide supplies preparation work and evidence, and does not install hooks or implement a native supervisor.

Command semantics: [official Git worktree documentation](https://git-scm.com/docs/git-worktree), consulted 2026-09-07; creation, detached checkout, shared metadata and inventory. Framework boundary requirements remain the selected [execution contract](contracts/execution-contract.md).
