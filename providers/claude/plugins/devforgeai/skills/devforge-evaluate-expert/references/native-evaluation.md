# Native evaluation procedure

Use this during an authorised evaluation run. It is an operator-supported procedure for an ordinary subscribed Claude Code session. It provides no launcher and installs no hooks, and nothing in it claims that the POC enforces any of it automatically - these are conditions to establish and observe.

Keep the candidate read-only throughout. You produce evidence and a builder handoff; `devforge-project-expert-creator` owns every repair. A changed candidate starts a new evaluation iteration rather than continuing this one.

## Outcomes and order

Run tier **C** (installed resources), then **B** (output quality and boundaries), then **A** (discovery and activation). Keep a separate outcome for each. Structural observations, the independent review, package identity and the three tiers never become one percentage.

- `PASS` - the required observation was obtained and satisfies the frozen assertion.
- `FAIL` - a valid completed observation contradicts it. Record the behaviour and the evidence.
- `NOT_RUN` - a planned arm or case was not attempted. Give the scheduling or dependency reason.
- `COULD_NOT_RUN` - a required observation could not be obtained: boundary failure, missing runtime or authentication, unavailable observation channel, timeout, interrupted stream, contaminated context, missing consequential input.
- `NOT_APPLICABLE` - a predeclared scope exclusion, such as a helper test against a baseline that contains no helper. An applicable case that turned out difficult cannot be excluded after the fact.

If installation or resource access fails in C, block the B and A claims that depend on that installation and continue the independent work. An ordinary output-quality `FAIL` in B with intact boundaries does not stop A - activation is a different property. Any unsafe boundary, identity mismatch or candidate mutation stops dependent execution immediately; preserve the attempt and finish the reports with the cause.

## 1. Choose and prepare the environment

Resolve the environment choice before treating its absence as a blocker. Reuse an explicit prior selection; otherwise ask:

> Which testing environment should this evaluation use?

- **Create Git worktrees for the evaluation** - recommended when none exists. Prepare bounded local workspaces, then resolve native readiness.
- **Use an existing validation environment** - record the assigned paths and establish readiness.
- **Continue with static review only** - complete the reading-based observations and the independent review, and preserve every native case with an explicit missing-observation cause.

A previous answer of "no existing environment" still needs this offer; do not stop at asking the operator to supply a ready environment.

For selected creation, freeze [workspace-allocation.json](../assets/workspace-allocation.json) **before any workspace write**: repository and common-directory identity, resolved base commit, bounded workspace count, destinations, permitted writes and the authorisation. Then prepare, and record what preparation actually achieved in [environment-setup.json](../assets/environment-setup.json), whose `plan_ref` may still be null.

Preparation may proceed while model, authentication, repetition and budget choices are pending. A measured launch may not. Workspace count is a preparation bound and is not an attempt or time budget; further workspaces need a new bounded allocation, and prior allocations, plans and observations are preserved rather than amended.

Worktrees share Git metadata. They do not isolate credentials, client state, services, policy or acceptance, and a prepared workspace is not native readiness.

## 2. Freeze the experiment before measuring

Expand the plan's checks into each required attempt and arm before execution. Candidate checks use `expectation: pass`; baseline checks use `expectation: observation`, because an observed baseline `FAIL` is comparison evidence and does not by itself fail the candidate.

Record in [validation-plan.json](../assets/validation-plan.json) and the frozen case file:

1. The candidate source package and the intended installation mode - project-local `.claude/skills/` or an exported plugin. Pick one per run; a result in one mode does not prove the other.
2. The accepted specification and contract revisions, and the requirements each case observes.
3. Case IDs, tier, positive or negative purpose, the raw user request, fixture identities, allowed outputs and side effects, expected behaviour, and the observation method. Keep worker-visible fixtures separate from grader-only expectations.
4. The baseline kind - `old_skill` for a preserved previous revision, `without_skill` for a new capability - and why it is the relevant comparison. Do not select an easier baseline after seeing results.
5. Time and subscription budget, per-attempt deadline, scheduled attempts, retry policy, arm order, and the rule for each declared conclusion. Declare repeats even for a small pilot, and report counts without inventing statistical confidence.
6. A fixed train/validation split for any description work, with held-out expectations kept away from the author and the task worker.
7. The assignment, report destination, operator identity, authentication arrangement, supported process controls and the isolation method.
8. The environment selection, and for worktrees the repository identity, base commit, assigned absolute paths, and one attempt-to-workspace-to-client-state mapping per planned run.
9. The effective runtime configuration to hold constant: client version, observable model setting, project instructions, sibling skills and plugins, tool availability, network policy, and memory or history arrangement.

A change to the candidate, the installed copy, the specification, a fixture, the baseline, an expectation or a material runtime setting creates a new affected iteration. Keep the old attempts. Cases added after a failure are labelled diagnostic and do not retroactively improve a measured result.

## 3. Establish an actual boundary

Obtain observed evidence for each of these before launching a measured worker.

| Boundary | Required evidence | If unavailable |
| --- | --- | --- |
| Candidate and governing inputs | Exact manifests; read-only for the worker; a separate writable output area | Stop any run that could alter them; record `COULD_NOT_RUN` |
| Consuming project | Assigned path and output map, with only the permitted inventory visible | Stop dependent cases; record the missing access proof |
| Tier C source exclusion | The original framework and source-only files are genuinely unreachable; installed resources remain readable | No tier C `PASS`; a changed working directory does not substitute |
| Client history and memory | A distinct store per arm, attempt and retry, with the effective mapping observed | Preserve the contaminated state; allocate a new attempt or record `COULD_NOT_RUN` |
| Tools, external access, network | The actual permitted interfaces and egress support the declared side-effect fence | Do not run an external-state-sensitive case unconfined |
| Process ownership | An owned launch identity and a scoped termination method | Do not begin a run you cannot stop within its assignment |
| Credentials and global state | An explicit operator-managed authentication arrangement; ordinary global stores stay outside worker writes | Request the arrangement or record `COULD_NOT_RUN`; never copy credentials as a workaround |
| Transcript and artifact observation | A method that preserves worker completion, tool consultation and saved output identity | Do not assert an unobservable behavioural or activation result |

Use harmless operator-created probes first, through the same launch boundary and settings as the measured worker: read a permitted fixture; try to read an operator sentinel outside the allowed view; try to write an operator-owned protected sentinel; write a disposable file in the permitted output area; inspect and terminate only a disposable process created for the probe. Preserve the expected and observed results, and limit the claim to the conditions actually tested. Never use real credentials, production data, user files or another session's process as a probe, and never relax a denied boundary to make a test pass.

Do not delete, reset or rewrite ordinary user history, memory, configuration, authentication or global skill installations. The operator may complete subscription sign-in under the recorded arrangement; record the method and the outcome, never a secret. No model API key is required by this process.

**A caution about apparent isolation.** A fresh directory, a new worktree, a new conversation or a subagent proves none of these boundaries on its own. Claude subagents run in separate context windows, which separates a prompt - not a filesystem, a process table, a credential store or a memory store. Verify the effective client-state mapping and the visible instructions, skills, plugins, tools and settings before relying on clean-context evidence.

If no acceptable boundary plus subscribed runtime is available after the offer and the selected setup, record `COULD_NOT_RUN` for the affected observations, preserve the dependent cases as unattempted with that cause, and finish the reading-based results and the builder recommendations. Do not fall back to an unconfined run or an API-backed harness while describing it as subscribed native testing.

## 4. Prepare each attempt

For each case, arm and retry, separately:

1. Use the assigned unique attempt ID, consuming-project directory, writable output directory, isolated client history and memory store, and owned runtime process. Candidate, baseline and retries never reuse a writable workspace or history.
2. Stage the same underlying raw facts into the candidate and baseline projects. Differences are limited to the declared skill treatment and any recorded unavoidable runtime difference.
3. Install the exact frozen package through the selected supported mechanism, using its actual documented command surface. Do not invent a command, flag or slash command. Authored `evals/` stay out of runtime installations.
4. Verify the installation path, relative file inventory and digests, provider, mode and entrypoint identity. A partial installation is retained as failed evidence; a retry uses a new destination.
5. Inventory every visible discovery location and check for duplicate copies of the target. Claude loads skills from the managed settings directory, `~/.claude/skills/`, the project's `.claude/skills/` and every parent up to the repository root, nested `<subdir>/.claude/skills/`, enabled plugins and any `--add-dir` directory, with a defined precedence. A `without_skill` arm must lack the target in **every** one of them; an `old_skill` arm must expose only the selected preserved copy.
6. Record the actual client version from the client's own version surface, and the model configuration if the session exposes it. A version observation identifies the client and proves no behaviour.
7. Launch a fresh subscribed session inside the verified boundary. Do not resume or fork an earlier task or reuse its writable memory.
8. Confirm transcript capture and output collection work without revealing held-out expectations to the worker. Save the manifest before the measured request.

Use [run-manifest.json](../assets/run-manifest.json) for each distinct run and [case-grade.json](../assets/case-grade.json) for each completed or unavailable case. Fill copies in the assigned evidence location; never fill the bundled templates in place.

## 5. Tier C - installed resources and consuming-project outputs

Choose cases that exercise the package's real runtime dependencies: a required reference, an output template and a helper, where each exists. A skill without scripts needs no invented script test; state applicability before execution.

1. Confirm the source-exclusion probes still hold for this attempt and that source-only files cannot be consulted. Installed package-relative copies of required contracts are legitimate runtime resources.
2. Give the frozen realistic request. Naming the target explicitly is allowed in C.
3. Observe successful consultation of the required installed entrypoint and resources, and any allowed helper execution. Record the resolved absolute path, the matching installed identity, the interpreter and arguments if observable, the completion result and the delivered artifacts.
4. Inspect the outputs in the consuming project's declared artifact map, and confirm their actual saved bytes. A promised path or a closing message is not proof that a file was written.
5. Grade resource loading, required artifact delivery, task behaviour where the case specifies it, and the overall case separately.
6. Stop dependent B and A execution if C shows a broken installation, a wrong identity, a missing required resource or an unavailable source-exclusion observation. A merely missing presentation detail does not prove installation failure.

A source-level link check, a hash match or a successful helper run is not sufficient for C. This tier observes the installed package operating in its consuming environment, and it does not prove discovery.

## 6. Tier B - output quality and boundaries

Naming the skill path is allowed. Both arms get the same raw task in separate clean attempts. A `without_skill` baseline receives no substitute text copied from the candidate.

1. Run the frozen task for each declared arm in the scheduled order.
2. Cover representative intended behaviour plus the declared consequential cases: missing required information, conflicting or changed accepted input, an unavailable dependency, a nearby out-of-scope request, and an attempted instruction override in task data where relevant. Derive them from actual requirements; do not add unrelated hazards.
3. For interactive skills, freeze an operator answer schedule or policy. Answer only the worker's real questions, from the same facts in both arms, and record every unscripted answer as a deviation.
4. Preserve final messages, actual tool outcomes and required artifacts. Record observed successful, denied and failed auxiliary tool use per arm - shared availability does not imply equal effective assistance.
5. Grade with deterministic checks where they apply and a separate semantic reviewer for interpretation. Give the grader the frozen requirement, the raw input and the actual output; never a desired winner.
6. Record named behaviour, artifact delivery and the overall case independently. A correct idea can still fail an artifact requirement. A missing required observation is `COULD_NOT_RUN`; an observed wrong result is `FAIL`.
7. Compare arms only after independent grades. Blind arm identity where possible, counterbalance presentation order, and disclose length bias, order sensitivity and identity leakage. A longer output is not a better one.

Keep a planned but unexecuted baseline at `NOT_RUN`. `NOT_APPLICABLE` is only for a scope-excluded assertion, never for a missing arm, and an incomplete baseline supports no improvement claim.

## 7. Tier A - discovery and activation

Use the actual installed package in fresh sessions with the same preflight. Define separate cases for explicit invocation, direct domain requests, indirect requests and realistic near-miss negatives.

Explicit invocation uses the real surface: `/<skill-name>` for a project-local skill and `/<plugin-name>:<skill-name>` for a plugin skill. Confirm which is installed rather than asserting one. Ordinary implicit prompts contain no skill name, no path, no forced invocation and no evaluation hint, and no earlier preparation message may teach the worker which skill to select.

Record these four as separate observations:

| Observation | Sufficient evidence | Insufficient evidence |
| --- | --- | --- |
| Discovery | The actual installation appears in the session's skill inventory with an identifiable path, provider and mode | It exists only in provider source; a similarly named skill appears |
| Selection | The session selects the exact target identity for that case | The name occurs in unrelated prose, a glob, a search result or another tool's arguments |
| Load | The selected target's real instructions are returned and loaded, tied to the installed identity | A requested read that has not completed; a selection event alone |
| Completed execution | The case reaches a successful terminal result and the assertions can be graded | Timeout, tool error, premature EOF, truncated stream, a stopped worker |

For a positive case, grade the selection or loading assertion and the task result independently: a skill that was selected but never successfully loaded has not passed a load assertion. For a negative case, `PASS` requires a completed successful run with no consultation of the exact target - another skill being selected during an incomplete run does not establish it, and a timeout, error, truncated transcript or missing consultation visibility is `COULD_NOT_RUN`.

Record suggested continuation, sibling discovery and actual sibling invocation independently. An absent sibling need not fail a non-activation assertion, but it is a capability gap when the case requires that continuation.

If a detector parses transcripts, inspect its source and establish its interpretation against deterministic synthetic transcripts first - exact-identity matches, unrelated substrings, requested-but-failed reads, negative completions, timeouts, errors, truncated streams and premature EOF. Synthetic transcripts test the detector; they are never native results.

A path-based subagent exercise belongs to B, not implicit A. A version probe, a source-level check or a plugin export cannot establish A either. Keep explicit and implicit results separate.

## 8. Finish an attempt

1. Stop only owned processes, by verified identity and the assigned scoped mechanism. Preserve their completion facts. Never terminate by a broad process name.
2. Preserve artifacts and transcripts before releasing the attempt. Redact secrets, and record any redaction that limits interpretation.
3. Re-confirm the installed, candidate and protected-input manifests. A mismatch invalidates the dependent identity claims: preserve the attempt and stop dependent execution. You do not repair the candidate.
4. Save the run manifest and case grades as separate evidence files. Record observed token and time metrics only where the runtime exposes them; otherwise leave them null.
5. Bind the outputs, manifests, transcripts, grader records, deviations and unresolved causes into the validation results. Record a report path only after its bytes exist at that location.
6. Route demonstrated candidate defects to `devforge-project-expert-creator` with the identity, the requirement, the evidence, a bounded change and the cases to rerun. Route unavailable runtime, authority or observation prerequisites to the operator or integration owner - never invent a candidate defect to compensate for an environment gap.
7. Leave acceptance and adoption with their owner. A scoped `PASS` is evidence for a decision, not a decision.

Stop after the results and the handoff. Do not edit the target, rewrite failed evidence, install a repair, or rerun in search of a passing sample.

## Reference basis

The three tiers, the client-state and process boundaries, the manifest shape and the manual native method come from the packaged framework contracts in `contracts/`. They are requirements to observe, not a claim that an enforcing launcher exists.

Claude's own documentation on skills and subagents (retrieved 2026-09-10; see [sources](sources.md)) supplies the discovery locations, their precedence, the invocation surfaces and the separate-context-window property used above. Documentation describes the client; it never replaces consultation evidence for the version you actually ran. Recheck the affected behaviour after any client, packaging, discovery-configuration or contract change.
