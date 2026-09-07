# Native evaluation procedure

Use this guide during an authorized validation run. Workspace preparation can start from its own bounded frozen allocation while the native plan is incomplete. Measured execution requires frozen inputs, deterministic inspection, AI review records, the complete experiment plan and observed readiness. It is an operator-supported procedure for a normal subscribed Codex terminal. It neither provides a native launcher nor installs hooks.

Follow the selected [skill authoring contract](contracts/skill-authoring-contract.md), [artifact contract](contracts/artifact-contract.md), and [execution contract](contracts/execution-contract.md). Keep the target candidate read-only. The validator produces evidence and a builder handoff; skill-builder owns subsequent repairs. A changed candidate starts a new affected evaluation iteration.

Use [validation-plan.json](../assets/validation-plan.json) to freeze the check schedule and budgets, [test-cases.json](../assets/test-cases.json) for separate case definitions and multi-turn answer schedules, [run-manifest.json](../assets/run-manifest.json) for each distinct native run, and [case-grade.json](../assets/case-grade.json) for each completed or unavailable case. Resolve these paths from this installed skill, then save filled records in the assigned evidence location. Do not fill the bundled templates in place.

## Outcomes and execution order

Run tier C (installed resources) first, tier B (quality and boundaries) second, and tier A (discovery and activation) third. Preserve a separate outcome for each. Static checks, AI review, package identity, and the three tiers never become a blended percentage.

- PASS means the required observation was obtained and satisfies the frozen case assertion.
- FAIL means a valid completed observation contradicts that assertion. Record the behavior and evidence.
- NOT_RUN means a planned arm/case has not been attempted. Give the scheduling or dependency reason; it is not a successful result.
- COULD_NOT_RUN means a required observation could not be obtained, with an actual cause: boundary failure, missing runtime/authentication, unavailable observation channel, timeout, interrupted stream, contaminated context, or a missing consequential input.
- NOT_APPLICABLE requires a predeclared scope exclusion. For example, a baseline without a candidate-only helper has no test of that helper. An applicable difficult or blocked case cannot be excluded after observing its result.

If installation or resource access fails in C, block B/A claims that depend on that installation. Continue independent static findings and the results/handoff artifacts. If B produces an ordinary output-quality FAIL with intact execution boundaries, continue planned A cases; activation is a different property. Any unsafe boundary, identity mismatch, or candidate mutation stops dependent native execution immediately. Preserve the attempt and finish reports with the cause.

Every enforced phase/task must receive an evidence-backed status even when unavailable. Enforcement intent is a workflow requirement; this document is not evidence that hooks or an external runner actively enforce it. Do not remove an enforced item to obtain PASS.

## 1. Freeze the experiment before native execution

First perform available workspace preparation under [workspace-allocation.json](../assets/workspace-allocation.json) and the setup guide. Native model/authentication/repetitions/budget choices do not gate that allocation. Preparation, installation and boundary observations may be saved before this plan is complete. The list below governs measured launch, not worktree creation.

Freeze cases in a separate file derived from test-cases.json. Bind it in the plan's input_refs using kind=cases and its exact path/digest; never place the plan's own complete-byte digest inside itself. Expand plan.checks[] into each required attempt and arm before execution. Candidate checks use expectation='pass'; baseline checks use expectation='observation', because an observed baseline FAIL is comparison evidence and does not by itself fail the candidate. A missing required baseline observation still limits the comparison. Record the following in the plan and bound case files:

1. Candidate source package and intended installation mode: project-local or exported-plugin. Select one per run; a result in one mode does not prove the other.
2. Accepted specification/contract revisions and the requirements each case observes. Preserve exact bytes and section IDs.
3. Case IDs, tier, positive/negative purpose, raw user request, fixture identities, allowed outputs and side effects, expected behavior/artifact assertions, and observation method. Keep worker-visible fixtures separate from operator/grader-only expectations.
4. Baseline kind: old_skill for the preserved previous skill, or without_skill for the same task with no target skill. Do not select an easier baseline after seeing results. Record why the chosen baseline is relevant.
5. Time/subscription budget, per-attempt deadline, number of scheduled attempts/repeats, retry policy, arm order, and the rule for each declared conclusion. Declare repeats even for a small pilot. Report counts for small samples without inventing statistical confidence.
6. Fixed development/held-out split for description changes and fresh final queries. Keep held-out expected answers away from the author and task worker. If the evaluation is a single fixed candidate with no optimization, state that scope and still preserve cases before execution.
7. Authority-selected assignment, report store or outbox, operator identity, runtime/authentication arrangement, supported process controls, and verified isolation method.
8. Environment selection and selection source; for Git worktrees, repository/common-directory identity, resolved base commit, assigned absolute paths, detached/branch state, and one attempt/arm-to-workspace/output/client-state mapping per planned run. Use runtime.environment_setup in the plan and [the setup guide](worktree-environment.md). Bind the existing workspace allocation and preparation/readiness observations, and reserve a distinct unused workspace per attempt. Save additional observations separately; do not create plan/setup digest cycles.
9. Effective runtime configuration to hold constant: provider/client version, observable model setting, project instructions, sibling skills/plugins, tool and connector availability, network policy, memory/history arrangement, and relevant local settings.

Changes to the candidate, installed copy, selected specification, fixture, baseline, expectation, or material runtime setting create a new affected iteration. Keep old attempts. Diagnostic cases added after a failure are labeled diagnostic; they do not retroactively improve the measured result.

For each quality assertion, declare the observable requirement and whether it is required by the specification or merely an improvement suggestion. Do not choose pass thresholds after seeing outputs. If an essential comparison rule is unresolved, ask the authority owner for that decision; complete independent preparation while it is pending.

## 2. Establish an actual execution boundary

The operator owns the environment assignment and runtime boundary. The validator performs the authorized preparation: reuse an assigned existing environment, or create and prepare local Git worktrees following [worktree environment setup](worktree-environment.md). Offer creation when no existing environment is available; do not stop at asking the operator to supply a ready environment. If the user selects static-only, preserve required native observations as unavailable and finish static review and reporting.

Save preparation observations using [environment-setup.json](../assets/environment-setup.json), initially bound to the workspace allocation with nullable plan_ref. Preparation and harmless readiness probes may precede the complete experiment plan; freeze that plan with their evidence before measured launch. Protected runtime admission remains separate. Worktree creation supplies the alternative workspace; continue with the remaining installation, runtime and authentication setup. A fresh directory, worktree, conversation, subagent, or CODEX_HOME value alone does not prove containment or clean context.

Before launching the measured worker, obtain observed evidence for each required boundary:

| Boundary | Required evidence | If unavailable |
| --- | --- | --- |
| Candidate and governing inputs | Exact manifests; read-only access for the worker; a separate writable report/output area. | Stop native execution that could alter them; record COULD_NOT_RUN. |
| Consuming project | Assigned path and output map, with only the permitted fixture/resource inventory visible. | Stop dependent cases; record the missing inventory or access proof. |
| Tier C source exclusion | Original framework/source docs and source-only eval inputs are inaccessible to the worker; installed runtime resources remain readable. | No tier C PASS; do not substitute a changed working directory. |
| Client history and memory | Distinct store per arm, case attempt, and retry; effective client-state mapping observed; no inherited previous attempt memory. | Preserve contaminated state; allocate a new attempt or record COULD_NOT_RUN. |
| Tools, external access, and network | Actual permitted interfaces and egress limits support the declared side-effect fence, including required subscription authentication. | Do not run an external-state-sensitive case unconfined. |
| Process ownership | Owned launch identity and a private process group/PID namespace or equally scoped termination method; unrelated processes protected. | Do not begin a run that cannot be stopped within its assignment. |
| Credentials and global state | Explicit operator-managed authentication arrangement; user's ordinary global stores remain outside worker writes. | Request the missing arrangement or record COULD_NOT_RUN; never copy credentials as a workaround. |
| Transcript and artifact observation | A method that preserves actual worker completion, tool consultation, and saved output identity for the case. | Do not assert an unobservable behavioral/activation result. |

Use harmless operator-created probes before model execution: read a permitted fixture; attempt to read an operator-owned sentinel outside the allowed source view; attempt to write an operator-owned protected sentinel through the worker's actual boundary; write a disposable file only in the permitted output area; and inspect/terminate only a disposable process created for this probe. Preserve the exact expected and observed results. Do not use real credentials, production data, user files, or another session's process as probes. Never intentionally relax a denied boundary to make a test pass.

The probe must use the same launch boundary and relevant settings as the measured worker. Testing an unrelated shell, or observing a read-only source flag in configuration, does not establish the worker's actual access. Limit the claim to the tested filesystem/process/network conditions; separate untested surfaces.

Do not delete, reset, or rewrite normal user history, memory, configuration, authentication, or global skill installation. Do not copy account credentials or session stores into fixtures, exports, reports, or evidence bundles. The operator may complete subscription sign-in under the recorded runtime arrangement; record success/failure and method, never secrets. No model API key or API-backed CI is required.

Known tooling limits are recorded in [framework context](framework-context.md). In the source inspected on 2026-09-07, the external delivery supervisor rejects native execution with synthetic=False; it cannot supply a real native observation. The older isolate implementation mounts the host root read-only and records network isolation as false. That alone leaves source material visible and does not establish tier C source exclusion or the required external-access boundary. Do not assume a command named "isolate", a successful sandbox startup, or a simulated receipt supplies stronger protection. Reinspect an actually changed revision and retain the resulting evidence before making a different claim.

After offering the alternative and carrying out the selected setup to the extent available, if no observed acceptable boundary plus subscribed native runtime is available, record COULD_NOT_RUN for the affected observation and preserve dependent cases as unattempted with that cause. Finish the deterministic/AI results and builder recommendations. Do not fall back to unconfined execution, a synthetic supervisor, or an API-backed harness while claiming subscribed native testing.

## 3. Prepare each independent attempt

For each scheduled case/arm/retry, perform these actions separately:

1. Use the operator-assigned unique attempt ID, consuming-project directory, writable output directory, isolated client history/memory store, and owned runtime process. For the worktree branch, bind an unused prepared workspace from a frozen allocation; allocate bounded additions before creating further worktrees. Candidate, baseline and retries never reuse a writable workspace or history. Bind validation_plan_ref, workspace_allocation_ref, workspace_id, client_state_directory and environment_setup_ref in the run manifest, retaining corresponding access probes. Native launch waits for the complete frozen plan and demonstrated readiness.
2. Stage the same underlying raw task facts into candidate and baseline projects. Differences must be limited to the declared skill treatment and recorded unavoidable runtime differences. Keep candidate, baseline, grader, and operator writable areas separate.
3. Install the exact frozen runtime package through the selected supported installation/export mechanism. Use its actual documented/help-listed command surface. Do not invent a DevForge command, slash command, harness flag, or plugin flag. Keep authored eval cases outside normal runtime exports.
4. Verify installation path, relative file inventory and digests, provider, mode, actual entrypoint identity, and allowed supporting resources. A partial export is retained as failed evidence; a retry uses a new destination rather than overwriting it.
5. Inventory visible project/ancestor/user/admin instructions, skills, plugins, tools, settings, and effective client state through the actual runtime/operator observation surfaces. Check for duplicate copies of the target. Without_skill must lack the target in every visible discovery location; an old_skill arm must expose only the selected preserved old copy.
6. Record the actual client version from the installed client's observed version surface and model configuration from the actual session if exposed. A version observation identifies the client; it proves no skill behavior.
7. Launch a fresh subscribed native terminal inside the verified attempt boundary. Do not resume or fork an earlier task or reuse its writable memory. The operator can use the actual skill selector for inventory in a separate preparation session; an implicit measured prompt must not be seeded with a target-specific instruction from that inventory.
8. Confirm that transcript capture and permitted output collection are working without revealing held-out expectations to the worker. Save the prepared manifest before the measured request.

The manifest uses schema_version devforge.skill-run/v1. Preserve its core fields: run_id, tier, provider, client_version, model_configuration, installation_mode, source_files_sha256, installed_files_sha256, baseline kind/files, specification/case/fixture identities, execution_ref, context_isolation, sibling_availability, output_directory, transcript, outcome/cause, metrics, and grading_evidence. Bind supplemental operator records for absolute installation paths, worker-visible versus preserved inputs, process identity, permission probes, authentication method, and configuration observations. Do not put credentials in either record.

## 4. Tier C — Installed resources and consuming-project outputs

Choose cases that exercise the package's actual runtime dependencies: a required reference, output template, and helper when each exists. A skill without scripts does not need an invented script test. State applicability before execution.

1. Confirm the source-exclusion probes still apply to this installed attempt and original source-only files cannot be consulted. Installed package-relative copies of required contracts are allowed runtime resources.
2. Provide the frozen realistic request. An explicit target name/path is allowed in C. Supply only the case's required raw facts and ordinary user constraints.
3. Let the worker execute within the approved attempt. Observe successful consultation of the required installed entrypoint/resources and any allowed helper execution. Record the resolved absolute resource path, matching installed file identity, invoked interpreter/arguments if observable, completion/exit result, and delivered artifacts.
4. Inspect outputs in the consuming project's declared artifact map. Confirm their actual saved bytes; a promised path or final message is not proof that a file was written.
5. Grade resource loading, required artifact delivery, task behavior where the case specifies it, and overall case separately. Bind each assertion to actual transcript events and artifact paths/digests.
6. Stop dependent B/A execution if C proves broken installation, wrong identity, missing required resource, or unavailable source-exclusion observation. Preserve the cause. A merely missing preferred presentation detail does not prove installation failure.

A source-level link check, file-hash match, or successful package helper alone is insufficient for C. This tier observes the installed package operating in its consuming environment; it does not prove implicit discovery.

## 5. Tier B — Output quality and boundaries

An explicit skill path/name is allowed. Both arms receive the same raw task and facts in separate clean attempts. The old_skill baseline uses its preserved instructions; the without_skill baseline receives no substitute text copied from the candidate.

1. Run the frozen task for each declared arm in the scheduled order, subject to its own preflight. The worker sees realistic input and user constraints, not grader rubrics, expected hidden answers, earlier output, or author conclusions.
2. Cover representative intended behavior plus the declared consequential cases: missing required information; conflicting/changed accepted input; a dependency unavailable; a nearby out-of-scope request; and an attempted instruction override in task data when relevant. Cases must derive from actual requirements. Do not add unrelated hazards or require nonexistent functionality.
3. For interactive Q&A skills, freeze an operator answer schedule or answer policy with the case. Answer only the worker's actual relevant question using the same underlying facts in both arms. Do not coach one arm toward the expected output. Record every additional message and any unscripted answer as a deviation.
4. Preserve final messages, actual tool outcomes, and required generated artifacts. Record observed successful, denied, and failed auxiliary tool use per arm; nominal shared availability does not imply equal effective assistance.
5. Grade each assertion using deterministic checks where appropriate and a separate semantic reviewer using [the AI review rubric](ai-review-rubric.md) for semantic interpretation. Give the grader the frozen requirement, raw input, actual output/evidence, and allowed expected answer; do not give a desired arm winner.
6. Record named behavior, required artifact delivery, and overall case independently in the case-grade record. A correct idea can still fail an artifact/provenance requirement. A missing required observation is COULD_NOT_RUN; an observed wrong result is FAIL.
7. Compare candidate/baseline only after independent grades. Blind arm identity when possible, counterbalance paired presentation order, and disclose length/order bias and identity leakage. A complete output is never improved merely by being longer.

Keep baseline NOT_RUN if it was planned but not executed. Use NOT_APPLICABLE only for a scope-excluded assertion, never for a missing baseline arm. An incomplete baseline cannot support an improvement claim. Report observations for the candidate without claiming causation beyond the observed, comparable environment.

## 6. Tier A — Discovery and activation

Use actual installed Codex packages in fresh target terminals with the same preflight requirements. Define separate cases for explicit invocation, ordinary direct domain requests, indirect requests, and realistic negative/near-miss requests. Use the actual supported skill selector or mention mechanism for explicit cases only; ordinary implicit prompts contain no skill name, path, forced invocation, or special evaluation hint.

Record these as separate observations:

| Observation | Sufficient evidence | Insufficient evidence |
| --- | --- | --- |
| Discovery | The actual target installation is available in the native skill inventory/catalog, with identifiable path/provider/mode. | It exists only in provider source; a similarly named skill appears. |
| Selection | The native worker selects/requests the exact target identity for the case. | The skill name occurs in unrelated prose, a file glob, search result, or another tool argument. |
| Read/load | The selected target's real instructions are returned/loaded successfully, tied to the installed identity. | A requested read has not completed; a selection event alone. |
| Completed execution | The case reaches a successful terminal result and required task/artifact assertions can be graded. | Timeout, tool error, premature EOF, truncated stream, or a stopped worker. |

1. Preserve discovery evidence without injecting a target name/path into implicit task input. Do not include prior preparation messages that teach the implicit worker which skill should be selected.
2. Send the exact frozen request for that case. Let the worker complete within the planned budget and allowed side effects.
3. Capture actual target consultation/loading and terminal completion through available native traces or operator observations. If the client hides the needed event, record COULD_NOT_RUN for that observation rather than inferring it from a plausible answer.
4. For positive cases, grade the predeclared selection/loading assertion and task result independently. A selected skill that was never successfully loaded has not passed a load assertion.
5. For negative cases, PASS requires a successful completed terminal result with no consultation of the exact target. Selection of another skill during an incomplete run does not establish this. A timeout, error, incomplete transcript, or missing consultation visibility is COULD_NOT_RUN.
6. Record suggested continuation, sibling discovery, and actual sibling invocation independently. An absent sibling need not fail a target non-activation assertion, but it is a capability gap if the case requires that continuation.
7. If a detector parses transcripts, inspect its source/revision and establish its interpretation with deterministic synthetic transcripts before trusting model-run classifications. Include exact-identity matches, unrelated substrings, requested-but-failed reads, negative completions, timeouts, errors, truncated streams, and premature EOF. Synthetic transcripts test the detector; they are not native skill results.

A direct path-based subagent exercise belongs to B, not implicit A. A successful --version check, source validator, plugin export, or keyword occurrence also cannot establish A. Keep explicit and implicit results separate.

## 7. Finish an attempt and hand off evidence

1. Stop only owned processes using verified identity and the assigned scoped mechanism. Preserve their exit/completion facts. Never terminate by a broad process name.
2. Preserve artifacts and transcripts before releasing the attempt. Redact secrets from reports; do not distribute raw authentication or global session stores. Record any redaction that limits interpretation.
3. Confirm installed/candidate/protected-input manifests after the attempt. A mismatch invalidates dependent identity claims; preserve the attempt as evidence and stop dependent execution. The validator does not repair the candidate.
4. Save the run manifest and case grades as separate evidence files. Each grade uses schema_version devforge.skill-case-grade/v1, case_id, arm, overall, run_manifest with its path/sha256, and separately graded dimensions. Record observed token/time metrics only when the runtime exposes them; otherwise leave them unknown/null.
5. Bind exact outputs, manifests, transcripts, grader records, deviations, source references, and unresolved causes into the validation results artifact using the selected artifact envelope and assigned storage arrangement. A report path is saved only after its actual bytes/location have been observed, or after the operator saves and reads back a declared terminal handoff.
6. Route demonstrated candidate defects to skill-builder with candidate identity, requirement, evidence, bounded recommended change, retained behavior, and the cases that must be rerun after repair. Route unavailable runtime/authority/observation prerequisites to the named operator or integration owner; do not invent a candidate defect to compensate for environment unavailability.
7. Keep acceptance/adoption with its actual owner. A validator's scoped PASS is evidence for a decision, not a release decision or authority to change the source.

Stop after results and handoff. Do not edit the target, rewrite failed evidence, activate proposed hooks, publish/install a repair, or rerun indefinitely to search for a passing sample.

## Reference basis

The three tiers, client-state and process boundaries, manifest schema, manual native method, and output ownership come from the selected package-local framework contracts above. They are requirements to observe, not a claim that the POC already implements an enforcing launcher.

[OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills), retrieved 2026-09-07, documents explicit and implicit selection and local discovery locations. Use the installed client's actual observable behavior for the evaluated version; documentation cannot replace consultation evidence. Recheck affected provider behavior after a client, packaging, discovery configuration, or governing-contract change.

