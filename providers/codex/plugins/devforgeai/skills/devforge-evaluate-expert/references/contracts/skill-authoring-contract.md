# Packaged skill authoring contract

Derived for these Codex authoring utilities from DevForgeAI docs/mvp/skill-authoring-contract.md, draft revision 3, 2026-09-07. Exact source and destination hashes are in ../derivation.json. This operational summary retains applicable requirements; the assignment's selected source bytes govern any conflict. It does not declare draft framework capabilities implemented.

## Ownership and package

DevForgeAI owns methodology and provider skills. Codex framework skill sources are providers/codex/plugins/devforgeai/skills/<name>. Claude sources are separate. .agents/skills is the generated Codex project installation; a source directory alone is not discovered. Per-skill agents/openai.yaml is optional discovery metadata, not a standalone subagent. Shared templates and sibling policy have distinct owners.

A skill contains SKILL.md with YAML name and description. scripts, references, assets and metadata exist only when useful. Keep entry instructions focused and reference detailed resources at the phase that needs them. Resolve resources from the actual loaded installed skill directory; resolve the consuming project's artifact directory independently. Do not depend on developer home paths or source docs being present.

Authored cases and reproducible fixtures live under evals in source. Exclude evals from ordinary installations/exports. Reusable evaluator templates and procedures live under assets/references and ship at runtime. Keep run output/history/caches out of the package. Installed content preserves source bytes, but executable mode preservation is not assured: call helpers through their documented interpreter.

Package-local derivations record source path, selected preserved revision/location and exact SHA-256, destination path/hash, transformation and refresh condition. Pin sources before updating; source changes do not silently replace an assignment's governing version. Refresh only within the named skill/provider and preserve prior evidence. Runtime maintenance metadata uses references/derivation.json, not an excluded provenance sidecar.

Helpers declare runtime/dependencies, arguments, --help, noninteractive behavior, bounded output and exit meanings. Missing prerequisites are unavailable observations. A hash/placeholder check does not prove schema meaning, provenance fidelity or behavioral quality. Optional dependencies must be explicit; do not silently install them.

## Authoring and evidence

Recover actual task authorization, source/specification, ownership and template revisions. Preserve the previous candidate before enhancement. Resolve consequential ambiguity with the owner; do not reinterpret an accepted rule. This builder delegates validation to the separate validator by user decision; do not run validation while authoring.

Define realistic requirement-derived cases and reproducible raw fixtures before measured execution. Preserve train/validation split and hide held-out expectations from authors/task workers. Version expectations before measurement. Diagnostics may inform a later iteration; they cannot change the grading rule of a failed measured run.

Keep candidate and baseline source manifests separate from actual installed manifests. Record source and installed identities, case/spec/rubric/fixture/contract identities, provider/client/model, installation mode, actual assignment, output paths and evidence. Changes to any relevant input invalidate affected observations. Retain old bytes and failures. External acceptance is separate from an author's or validator's scoped recommendation.

## Isolation and native runtime

Each candidate arm, baseline arm and retry has a unique identity, writable output area and separate history/memory state. A new chat or worktree is insufficient proof. Observe effective client state, visible instructions/skills/plugins/tools/settings and actual tool success/denial. Shared availability does not imply equal effective assistance.

Use assigned disposable consuming projects. Keep global history, memory, configuration and credentials outside the writable run area. Subscription authentication needs an explicit operator arrangement; never copy secrets into evidence. Record launched process identities and terminate only verified owned processes. Probe the filesystem, source visibility and process boundaries harmlessly before model execution. Missing required isolation means COULD_NOT_RUN, with no unconfined fallback.

Manual isolated subscribed terminal evaluation is a supported method. No model API or API-backed CI is required. A tool's name does not prove native discovery or permitted authentication. Inspect its actual documented invocation, revision, source selection and observation method before adopting it.

## Three independent native tiers

Perform C, then B, then A, and report each separately.

- C, installed resources: use the actual installation in a consuming project with source docs demonstrably unavailable. Exercise package-local templates/references/helpers and output paths. A changed working directory does not establish source inaccessibility.
- B, quality and boundaries: explicit skill-path input is permitted. Give candidate and old_skill/without_skill baseline the same raw facts with isolated contexts/output. Grade required named behavior, artifacts, constraints and provenance. Baseline FAIL may be useful comparison evidence; unrun baseline is NOT_RUN.
- A, native discovery/activation: actual installed identity in a fresh target terminal. Separate explicit invocation, direct ordinary request, indirect request and near-miss negative. Implicit queries cannot give the skill path or force its name. Record selection request, actual loading/consultation and successful terminal completion independently.

Negative activation PASS requires a completed successful terminal with no target consultation. Timeout, premature EOF, truncated output or missing completion is COULD_NOT_RUN. Detect exact identity/consultation, not unrelated substrings. Test any detector's termination and identity handling with synthetic traces before relying on model observations; synthetic traces themselves are not native evidence.

## Grading and closure

Grade behavior, artifact delivery and overall result independently against accepted requirements. Resolve referenced revisions against retained bytes; provenance binding does not prove semantics. Record producer identity, active assignment, actual feedback and adoption separately. A historical author is not proof of a current exclusive writer.

Use PASS and FAIL only for supported observed conditions. NOT_RUN means unattempted; COULD_NOT_RUN means required observation unavailable with cause; NOT_APPLICABLE means predefined scoped exclusion with reason. Required phases cannot be silently excluded. A small pilot reports its counts and limits, not unsupported statistical claims.

Retain native outputs in their own formats. The report binds them with exact references rather than rewriting history. Promote only the provider, installation mode and use cases supported by evidence. A refreshed installation or integration candidate requires affected rechecks.

## Revision-3 controlled refresh

This assignment explicitly selects the revision-3 sources preserved in derivation.json. Historical evaluations retain their original revision-2 authoring contract and exact inputs. No previous result becomes revision-3 conformance evidence.

Managed operation keeps useful phase work in the skill and mechanical transitions, evidence predicates, waiting, correction bounds and receipt publication in the protected runtime. The selected shared source describes the brainstorm adapter. A separately reviewed utility component supplies mechanical builder/validator phases; consult the package-local managed reference for its bounded interface. Complete native integration remains separate and unobserved. Native admission is NOT_VALIDATED and native activation/rendered delivery NOT_OBSERVED.

Keep conditional managed guidance package-local. Final identities and receipts come from runtime observations; no model-issued completion check or helper fallback. Delivery-aware installation/export belongs to integration and must bind the explicit runtime executable, six-field requirement and single effective synchronous callback per event from the execution contract. Package/source compatibility does not certify native behavior. Frozen case expectations, task deadlines, old failures and separate C/B/A results remain intact; runtime-aware measurement requires newly allocated independent evidence.

## Accepted VPR-2 validation policy for manual mode

This section transcribes the owner-accepted VPR-2 policy (canonical source: `../skill-authoring/proposals/validation-policy-v1-20260908/policy-revision.md`) and requirement diff (canonical source: `../skill-authoring/proposals/validation-policy-v1-20260908/requirement-diff.md`) at DevForgeAI commit `8ede26450ae737a5e928c5f70a945aa995969b30`. Historical proposal labels and results stay unchanged. Policy acceptance authorizes this contract meaning; it does not establish runtime support, native qualification, funding or installation. The [manual v2 record reference](../manual-records.md) and assets define the current record shapes and producer bindings; the creator carries the selection facts into its handoff. Historical canonical locators here are provenance, not runtime resource dependencies. The validator design (canonical source: `../skill-authoring/skill-validator-design.md#vpr-2-accepted-policy-amendment--2026-09-08`) freezes requirement-derived discriminators.

For this manual mode, select `VPR-2` and its exact accepted policy source from the task, and freeze the manual pre-review context before T04. This does not require a managed v2 delivery contract. A v1 record, another provider, brainstorm or a generic request does not inherit conditional exclusions. Preserve every v1 predicate, including C/B/A ordering. A generic “validate” request is neutral: determine its actual claim, accepted baseline and scope, then select coverage. Resolve only consequential missing facts.

### Claims, selection and lineage

Select `Routine` for a bounded update to an identified owner-accepted baseline within its accepted capability/environment scope, with understood immediate and cumulative dependencies. Select `Full` for first or explicit qualification, a new supported capability/environment, consequential control/authority/enforcement/receiving semantics, a release/support contract requiring Full, or remaining unbounded impact. Adoption, installation, tagging and distribution inside an already accepted scope do not alone select Full. Record the requested claim in its actual words and its qualification requirement.

Routine PASS means the selected update meets complete current required evidence under that coverage. It may support scoped owner acceptance and installation when destination, exact bytes, effective controls and applicable post-install identity/resource/compatibility checks are bound and complete. Carried conditional owner authority can cover this; no per-check approval ceremony is required. A mismatch blocks affected use under the existing recovery arrangement. A Routine result never grants owner authority or qualifies new bytes. Full PASS means complete applicable assertion coverage for the exact candidate/environment, including actual native obligations and receiving transfer; release and human acceptance remain distinct.

Keep `current_routinely_accepted` separate from `qualified_anchor`. The latter is the last fully qualified candidate/environment with its evidence, or explicitly `ABSENT`/`UNKNOWN`. Routine never advances it. If no qualified anchor exists, bind the explicitly accepted unqualified baseline; preserve the missing qualification. Every update binds its immediate diff from the current accepted candidate and cumulative diff from the qualified anchor or that unqualified baseline, including effective configuration, installation and provider/client behavior. Review the union of affected requirements and transitive dependencies across both diffs. The acceptance chain cannot reset the anchor, erase a failure, or manufacture qualification. There is no fixed number of Routine edits after which Full becomes mandatory; unresolved consequential cumulative interaction is the trigger.

### Enforced tasks and reviewed conditional coverage

W1, P1–P6 and T01–T12 remain `Enforced`. Each task records its obligation disposition separately from observations. Native observations excluded by accepted Routine selection remain `NOT_RUN`; only a genuine scope exclusion may be `NOT_APPLICABLE`. Neither is native PASS. Accurate reporting may complete P5/P6 with failed or unavailable evidence.

| Tasks | Required obligation |
| --- | --- |
| T01–T02 | Bind external authority, policy, actual claim, accepted base/scope, candidate/environment, lineage, both diffs, dependency closure and frozen evidence selection. Full accounts for every applicable original assertion. |
| T03 | Preserve all applicable S001–S013 checks and affected deterministic regressions; source checks do not establish installed behavior. |
| T04 | Obtain one actual fresh independent AI review of selection, affected/dependent clauses and all R01–R10 invariants. Full reviews all applicable anchors. Retain separate criterion judgments and observed independence limits; no reviewer per criterion is required. |
| T05 | Complete the selected preparation/readiness obligation. A reviewed no-native selection records no-native disposition, without fabricating a native plan, boundary evidence or launch. The separately authorized workspace preparation branch remains available before native choices are complete. |
| T06–T08 | Record C/B/A observations or exact reviewed conditional/dependency dispositions. Every selected native behavior needs matching installed C and actual readiness. |
| T09 | Adjudicate candidate outcomes, required comparisons, coverage, freshness, compatibility and cumulative lineage. Full target receiving evidence must already exist. |
| T10–T12 | Save honest results, bounded repairs/enhancements and a prepared handoff. Report completion, suitability, owner acceptance, qualification and receiving invocation separately. |

T04 must be selected by the external owner, independent of the author/measured workers, and bind the frozen plan and actual reviewed bytes. A self-declared reviewer or a hash alone does not establish independence or adequate judgment. Missing applicable invariant context remains unavailable. Review selection once at this boundary; do not add per-row approval or recursive review chains.

Selected C failure, missing evidence or stale identity blocks dependent B/A. Under v2 Routine only, a pre-run T04-reviewed `NOT_SELECTED` B disposition permits selected A after matching C. It is never B PASS; an observed selected B failure cannot be relabeled as unselected. An intact B quality FAIL can remain an observed comparison while later independently permissible collection proceeds; candidate suitability still fails for a required candidate violation. Full retains required C/B/A ordering. Later observations cannot repair an earlier admission retroactively.

### Impact and compatibility union

Take every matching CI rule across immediate and cumulative changes, plus all affected regressions and negative branches. Cost targets do not choose applicability.

| Rule | Trigger | Required evidence or disposition |
| --- | --- | --- |
| CI-01 | Spelling/layout/commentary without semantic, metadata, resolution or output-contract change | Applicable D checks and focused independent S review; no native work unless semantic impact is found. |
| CI-02 | Trigger/invocation/selection exposure | Matching C and affected explicit/direct/indirect/near-miss A including adjacent negatives; B when promised behavior changes. |
| CI-03 | Resources/dependencies/helpers/templates/package/output destinations | D resolution/identity/regressions, affected actual installed C and downstream B; A if discovery changes; CI-06 if transfer meaning changes. |
| CI-04 | Bounded workflow/prompt/clarification/quality/failure behavior | C and affected normal/edge/negative B/prior failures; matched candidate/baseline arms for behavior change or a comparative claim; A for selection impact. |
| CI-05 | Consequential authority/permission/trust/enforcement/gate/evidence authenticity | Full before adoption of the changed contract, D denial/identity tests, S meaning review and representative actual native controls. |
| CI-06 | Receiving prerequisites/output meaning/receipt authority/transfer/completion | Full before adoption, producer/consumer contract checks and actual eligible target-to-receiver transfer/failures. Unchanged prose spelling follows CI-01. |
| CI-07 | Client/provider/installation/configuration | Apply CP-01–CP-04 to used capabilities. Names/version strings establish neither compatibility nor incompatibility. |
| CI-08 | Requirement/case/oracle/grading meaning | Explicit specification decision before use; new revision and affected assertion reevaluation; preserve originals and historical outcomes. |
| CI-09 | Unbounded impact/unresolved cumulative interaction | Full or insufficient evidence; no Routine adoption for the affected unbounded claim. |

| Rule | Bound compatibility obligation |
| --- | --- |
| CP-01 | Pin old/new client/provider/installer and effective configuration, applicable official change information/local source evidence, used capabilities, changed/unknown dependencies and affected assertions. Identical relevant bytes are not a behavioral change. |
| CP-02 | Observe affected schema/install/resource/parser/control mechanics and negative inputs using deterministic checks. Documentation and a version probe are insufficient native evidence. |
| CP-03 | Changed executable/provider/installer: observe exact-installed load and a completed bounded task, plus each affected control/selection denial, failure or activation probe. Add paired B for possible provider/model output-quality change; retain source visibility, capture completeness and effective differences. |
| CP-04 | Routine is eligible only for evidenced equivalence within accepted used-capability scope with unchanged trust/control/transfer meaning. New unsupported scope, consequential meaning or remaining unbounded impact selects Full. Unknown changed components stay unresolved. |

Unchanged components may reuse exact fresh evidence with a stated scope. Do not run every compatibility permutation. A post-install check may share an actual load/task observation only when its conditions, identities, timing and required outputs match.

### Assertion evidence, receiving and results

`D` is deterministic mechanical evidence, `S` independent semantic judgment, and `N` actual native observation. D tests of native evidence admission do not supply N. Full completeness means every original applicable case/assertion/variant has its required evidence kinds and independent per-arm/assertion judgment. Preserve all original catalogs, S001–S013, R01–R10 and historical outcomes. No optimized Full call total exists until its complete reviewed observation map exists.

One raw observation can serve compatible assertions only with matching candidate/environment/input, prompt and forcing conditions, arm, visibility, time/freshness and prerequisite order. Disclose shared sample counts and correlation. Opposite arms, incompatible variants and forced-versus-implicit prompts remain distinct. One independent bounded paired/batch grade may assess complete actual raw outputs, retaining each arm/assertion judgment, neutral labels where possible and order/arm leakage. Baseline quality FAIL may complete an intact comparison; absent/mismatched baseline evidence cannot. The pair summary never overwrites candidate judgment. A child-output grade and parent interpretation remain distinct assertions, without a recursive grader campaign.

Validator self-evaluation keeps every explicitly native outer/inner source assertion, including SV-009, SV-012 and SV-024–SV-028 and representative actual nested review/return/failure/receiving integration. A generic validation subtask does not automatically invoke a 17-case inner Full suite. Real compatible bundles may support adjudication assertions; synthetic bundles support only explicitly synthetic/mechanical/error handling assertions, never clean native negatives, installed resources, isolation, callback origin, nested execution or receiving.

Full T09 consumes eligible output actually produced by the measured target, observed receiver loading, and the required completed receiver action or expected negative disposition under the receiving contract. Record evidence before adjudication. The evaluator's own prepared T12 handoff does not invoke or recursively qualify another evaluator. Receipt creation, publication/readback and actual receiver invocation remain separate facts.

Required candidate/protocol FAIL yields `FAIL`; otherwise any required missing/unavailable evidence prevents PASS and yields `INSUFFICIENT_EVIDENCE`. With all required evidence complete and current, select `ROUTINE_PASS` or `FULL_PASS` according to the selected mode. A complete honest report can carry any of those dispositions. Helpers advise; they do not authenticate observations, grant acceptance or publish protected receipts.

Authentication lifecycle reuse is conceptually separate from independent native evidence state. Supported cached authentication need not mean one login per generation, but credential copying, writable history reuse or unproved global-state isolation is not authorized. Authentication/readiness for the actual selected native environment must be observed; this policy supplies no credential or execution allocation.


### Manual applicability amendment (F01–F08)

The September 8 implementation handoff accepts the Routine/Full distinction for user-initiated workflows. The policy selection itself does not require managed admission or automated funding. Required independent review, isolation, native evidence and authority remain. Automatic receiver invocation, background resumption, campaign scheduling and automatic repair are deferred. G8-FUNDING-COMPLETION-01 remains a failure of the deferred automated funded-launch path. No historical record, case, assertion or ledger is changed.

For manual evaluation, a pre-review context binds the exact plan, accepted policy and separately assigned reviewer without claiming protected admission. The advisory reducer checks this context; it cannot enforce actions or prove semantic quality. The manual operator establishes required boundaries and preserves actual observations. The plan call_graph records the selected manual workers/reviewers and dependencies; exhaustive automatically scheduled return/continuation charging belongs to deferred automation. Do not invent model-budget measurements.

Full receiving evidence must come from actual user-mediated delivery of the target's real eligible outputs and the receiver's observed loading and action. The evaluator's own T12 handoff is prepared only and does not initiate recursive qualification. Missing enforcement prevents its specific consequential adoption claim, even when reporting finishes.


## Owner-approved local unqualified baseline

A distinct owner-selected local adoption claim is permitted for the exact manual-mode creator/evaluator packages after a predefined bounded acceptance set passes. Require deterministic package/resource checks, independent semantic review, representative actual creation/reuse/enhancement and missing-evidence behavior, both actual user-mediated handoffs, current source/runtime identities and owner acceptance. The supported installer records `LOCAL_ACCEPTANCE_SET_PASS` with `qualification_status: UNQUALIFIED`. This permission applies even when the candidate has changes that would require Full evidence for a qualification claim; it does not make those changes qualified.

All original creator phases and evaluator phases/tasks retain their Enforced classification and author/evaluator separation. The local installation gate measures its named acceptance set, not universal phase interception. Preserve all historical failures and leave the remaining qualification catalog NOT_RUN. Full qualification, its original assertions, controls, comparison arms and selection rules remain separate. An unqualified local baseline neither creates a qualified anchor nor automatically becomes a Routine acceptance chain. Conditional owner installation authority can be used after its actual conditions pass; no automatic orchestration or native launch is implied.
