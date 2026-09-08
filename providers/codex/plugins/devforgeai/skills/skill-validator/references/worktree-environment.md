# Alternative test environment with Git worktrees

This conditional path refines T01/T02 intake and freezing and T05 setup. P1–P6 and T01–T12 remain Enforced; preparation can proceed while experiment planning is incomplete. It introduces no new phase, classification question or model-controlled transition.

## Resolve the environment choice

Reuse a previous explicit selection. Otherwise ask "Which testing environment should skill-validator use?"

- **Create Git worktrees for validation (Recommended when none exists):** Prepare bounded local workspaces, then resolve native readiness.
- **Use an existing validation environment:** Record the assigned paths and establish readiness.
- **Continue with static review only:** Complete independent inspection/review and reporting; native observations remain unavailable.

"No existing environment" and silence do not select an option. Once creation is selected, carry that authorization forward without asking for it again. Resolve routine details from the assignment; ask only for consequential unresolved choices. A local Git worktree needs no GitHub hosting, remote branch or pull request.

## Freeze a workspace allocation

Fill [workspace-allocation.json](../assets/workspace-allocation.json) in the assigned evidence area. This record authorizes bounded preparation under the actual user/runtime assignment; its model-authored contents do not create authority. It is separate from [validation-plan.json](../assets/validation-plan.json).

Record:

- The selected consuming Git repository and actual common Git directory, independently of the skill source. If the assignment does not identify the repository and ownership is ambiguous, ask; do not initialize or clone one implicitly. Use the repository's native filesystem/client, including Linux paths for a WSL repository.
- Its observed current HEAD as the default base unless another existing revision is assigned; resolve the full commit ID and selection source. Keep the same project base for candidate and baseline. Git base and frozen skill manifests identify different bytes.
- A positive bounded workspace count, the assigned parent and exactly that many fresh absolute destinations, each with a workspace ID. Derive count from an explicit assignment or a clearly bounded requested preparation scope; otherwise ask for that allocation choice, not the native test budget. Detached checkout is the routine default; record any explicitly assigned branch and check ownership/occupancy. Do not invent case or attempt IDs to allocate workspaces.
- Permitted writes: only the listed new workspace paths, their explicitly assigned preparation contents, the report outbox, and narrow common-directory registration writes. Record authorization source, owner and any real protected runtime assignment reference. Measured workers must not gain write access to shared Git metadata or the original checkout.
- Protected candidate/baseline/source/grader paths and known snapshot references. Preserve exact source, baseline and governing bytes before installing or consuming them; source snapshot selection may remain pending during empty project preparation. No committed skill version substitutes for an uncommitted frozen candidate.

Inspect current repository/worktree inventory, applicable checkout hooks/filters and path aliases. Reject occupied or overlapping destinations, including protected roots and other assignments. Retain these observations. Save and freeze the complete allocation before provisioning; record its digest externally. The allocation contains no required model, authentication, repetitions, native attempt/time budget or case schedule. Those unresolved test inputs must not independently prevent creation.

If an allocation input is unresolved, preserve it with its specific cause and continue independent work. Existing/static-only choices create no worktrees and use no Git allocation. Do not change an already frozen allocation; assign additions or retries in a new bounded allocation, retaining the former one.

## Prepare the selected workspaces

Use resolved arguments through the actual shell or argument-vector API:

```text
git -C <repository-root> worktree list --porcelain
git -C <repository-root> worktree add --detach <new-workspace-path> <resolved-base-commit>
```

Recheck destination absence, repository/common-directory identity, base and authorization before each add. Do not execute evaluated skill code or unassigned checkout side effects. Create only the allocated count. Save actual command output, exit status, path, HEAD and detached/branch state in [environment-setup.json](../assets/environment-setup.json), bound to `workspace_allocation_ref`. `plan_ref` may be null: no complete native plan is needed for this record.

Continue the preparation available under that allocation: inventory the checkout and create only explicitly permitted preparation directories or stage already selected raw inputs. Once exact skill snapshots and a supported installation mechanism are selected, install only those frozen runtime bytes and retain an independent installed manifest. Do not guess an installation treatment to fill pending experiment choices. Record outstanding fixture, installation, client, authentication and boundary work alongside the delivered paths. Missing those later inputs does not undo successful worktree preparation.

Keep authored evals, hidden expectations and source-only documents outside measured worker views. Resolve duplicate target installations only within assigned disposable scope; otherwise retain the collision as a native readiness prerequisite. Preserve all dirty original source and the actual old_skill baseline. Never commit, stash or reset originals to populate worktrees.

On failure, retain created paths, Git metadata and exact errors. Do not force reuse, prune, remove worktrees, overwrite occupied destinations, change the base or branch, or alter remote state to make preparation succeed. A retry gets a new destination and bounded allocation; no native test budget authorizes extra workspace writes implicitly.

## Bind prepared workspaces to the experiment

Once cases and repetition/attempt limits are selected, allocate each case/arm/retry to an unused prepared workspace, its own output directory and independent client-state directory. Record workspace ID, allocation reference and actual setup evidence in the complete plan. A workspace is not an attempt until this binding is made. Verify its preparation/use history and contents; a workspace used by a previous worker, preparation model session or contaminated client must not be silently reset or shared with another independent attempt. Retain it and allocate a fresh workspace when clean state cannot be demonstrated.

More attempts than unused workspaces require additional bounded allocations before creation. Additional destinations may be derived within existing explicit authority; ask only where that authority or a consequential choice is missing. Do not repeat the settled environment-choice question. Preserve previous plans and setup records when bindings change.

Before native launch, freeze the full experiment: cases/fixtures and expected assertions, exact candidate/baseline identities and installed treatment, client/model, subscription authentication arrangement, repetitions, attempt/time limits, observation methods, and demonstrated filesystem/source/process/history/tool boundaries. Bind actual installation and readiness observations. Use [native evaluation](native-evaluation.md#2-establish-an-actual-execution-boundary) for the required probes and transcript controls. A complete allocation or a created worktree is not native admission.

Subscription sign-in is an operator interaction under the selected runtime arrangement. Request it at the concrete prepared workspace when it is the remaining dependency. Do not copy credentials or normal client stores, assume Windows/WSL authentication is shared, or launch a model to work around an unknown runtime choice. Preparation can precede authentication; native execution cannot.

When these prerequisites are observed, the protected runtime owns admission and phase transitions; execute the frozen C, B and A schedule only after its applicable admission. If unavailable, retain the delivered workspaces and mark affected native observations COULD_NOT_RUN, with execution NOT_RUN for unlaunched attempts. Complete independent review and P5/P6 reporting without claiming native success or acceptance.

## Record outcomes without changing frozen inputs

The allocation and setup templates are local evidence formats, not registered runtime admission schemas or active enforcement.

- `workspace_status`: NOT_ATTEMPTED, PREPARED, PARTIAL, FAILED or SKIPPED. PREPARED means all workspaces in the record's allocation scope exist at the recorded identities and allocated preparation actions are complete; unresolved native choices may remain. Preserve mixed outcomes as PARTIAL.
- `native_readiness`: NOT_ESTABLISHED, READY, BLOCKED or NOT_REQUESTED. READY requires actual installation, authentication, boundary and observation evidence for bound attempts; no claim follows from PREPARED alone.
- `workspaces` records paths/identities, preparation actions, errors and remaining setup. `attempts` may be empty until test allocation. Every evidence reference identifies saved absolute path and exact SHA-256; record no secrets.

Avoid reference cycles: allocation precedes preparation observations; readiness observations may retain null `plan_ref` while the experiment is incomplete. Freeze a plan binding those existing records, then the run manifest binds that exact plan, allocation, workspace and setup snapshot. A later observation can reference the frozen plan, but the plan is not rewritten to point back to it. No record includes its own digest.

Report retained paths, allocation and setup identities, source/base distinctions, incomplete native choices and concrete continuation in verification results and handoff. Save successor observations rather than altering records already referenced by a plan/run. Completion never authorizes cleanup or release of worktrees.

Existing H1/H2 proposals need runtime-owner integration to distinguish allocation-backed preparation from native admission. See [enforcement design](enforcement-design.md). This guide installs no hook or native supervisor and adds no ceremonial completion marker.

Command semantics remain the selected [official Git worktree documentation](https://git-scm.com/docs/git-worktree), consulted 2026-09-07. Existing packaged execution-contract boundaries remain selected; the current user enhancement refines preparation dependencies only.

## VPR-2 no-native selection

Carry a settled environment choice forward. For a pre-run independently reviewed Routine no-native selection, record the exact T05 selection obligation with native NOT_RUN; do not fabricate a native plan or automatically provision unused workspaces. A separately authorized frozen workspace allocation can still prepare only its bounded destinations before native choices are complete. Preparation is not native readiness, C PASS, qualification or permission to launch. Full/legacy and selected native work retain every readiness and fresh-state requirement above.
