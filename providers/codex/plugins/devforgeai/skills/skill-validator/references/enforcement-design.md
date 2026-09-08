# Enforced validation workflow and hook proposals

All validator phases P1-P6 and tasks T01-T12 are Enforced requirements, explicitly selected by the user on 2026-09-07. No tasks inherit an unrecorded optional default. Runtime hook deployment is outside skill-builder's authoring scope.

## Requirement mapping

| Proposal | Protected transition | Covered tasks | Required evidence |
|---|---|---|---|
| H1 Intake guard | Allocate/prepare workspaces or start measured inspection/review | T01-T02 | For preparation: actual authorization plus frozen repository/common-directory/base/count/destinations/write allocation; native model/auth/budgets may be pending. For inspection/review: selected frozen target/spec/rubric and scoped inputs/write fence |
| H2 Native launch guard | Start native task workers or measured target execution | T03-T05 | Complete frozen cases/candidate/baseline/client/model/auth/repetitions/attempt-time/observation plan; unique attempt-to-workspace/client-state bindings; relevant static records; actual installation and demonstrated boundaries/readiness; allocation/preparation evidence is insufficient alone |
| H3 Tier order guard | Start dependent tier B or A campaign | T06-T08 | Applicable prior C/B observations; failures/unavailability preserved; no dependent PASS claim when a prerequisite is unavailable |
| H4 Verdict guard | Write a suitable-for-stated-scope or passing completion record | T09 | Frozen plan and all required current evidence; coherent decision receipt and no missing required observations |
| H5 Handoff guard | Announce final delivery or transfer work to builder | T10-T12 | Saved verification report, bounded enhancement specification, output identities, incomplete-work causes, next owner and handoff |

Each proposal applies only to a registered validator evaluation assignment and its protected candidate/outbox paths. It must not infer the active workflow from arbitrary words in a chat or run globally against unrelated tasks.

## Historical generic hook proposal: event and decision design

Use synchronous PreToolUse only where the installed Codex runtime supports the relevant local tool path. Match exact tool names/aliases for shell, apply_patch or applicable MCP calls, then inspect the actual action and registered run paths. There is no native workflow-phase event.

The hook reads operator-owned run registration and evidence state keyed by run ID, candidate/spec/case/rubric digests and attempt. It allows unrelated permitted work. For a protected action, it checks the relevant current prerequisite references and returns an explicit deny with a concrete remediation message when they are missing or invalid. Evidence state must be outside the target worker's writable candidate and bound to the registered assignment.

Use the existing receipt semantics for H4, but a receipt alone is not authenticated proof: the operator must control accepted observations and reviewer/worker separation. A marker that says complete or a model's own declaration cannot prove that tests ran or that an AI review is sound.

Proposed messages name the missing task and allowable next action, for example: "Native test launch blocked: this attempt has no observed source-visibility/client-state boundary. Establish and record that boundary, or report COULD_NOT_RUN." Do not restart indefinitely.

A Stop hook may flag missing delivery records after a completed validation request, with bounded continuation and a check of stop_hook_active. It must not trap ordinary Q&A, interrupted or blocked sessions in loops. Final report saving must remain permitted on failures.

## Errors, exceptions and deployment conditions

Desired policy for protected transitions is deny when evidence/state is missing, stale or unreadable. Native runtime behavior may fail open for handler errors, disabled/untrusted hooks, unsupported return fields or unavailable MCP handlers. Document these differences and do not label the desired policy as achieved.

Before any future deployment, its owner must establish exact runtime/version, trusted hook definitions, matcher/tool coverage, effective configuration sources, synchronous execution, dependency availability, timeout/error behavior and actual observed deny behavior. Multiple matching hooks may run concurrently; one handler cannot rely on preventing another from starting. PostToolUse cannot undo a write that already happened, and background hooks cannot block their triggering action.

A complete boundary must cover alternate write/launch routes, already-running shell sessions and unsupported/hosted tools as relevant. Ordinary local hooks are guardrails; they do not create external acceptance authority. If the necessary coverage or protected state cannot be established, mark that proposal Partial or Unsupported and keep the dependent acceptance decision under the external operator's control.

No override is implied. An allowed exception needs actual authority, recorded scope, expiry/attempt identity and its effect on the validation claim. Changed target/plan/runtime/assignment invalidates affected registration and receipts.

## Historical proposal status and selected mechanical implementation

- Workflow obligations and evidence-result rules are authored in this skill.
- inspect_skill.py and assess_evidence.py implement deterministic inspection/record processing; they are not native launch enforcers.
- H1-H5 remain required controls. Their older generic hook configuration is historical design only; no hook files/configuration are installed, activated, run or validated by this authoring package. The selected protected utility component supplies the bounded mechanical mapping below.
- Feasibility: Partial with ordinary Codex hooks; complete workflow/semantic enforcement is not established.
- Reference: [official Codex hooks](https://learn.chatgpt.com/docs/hooks). Recheck actual target runtime documentation before proposing concrete configuration.

## Workspace allocation integration requirement

The protected runtime owns mechanical admission and phase transitions. Its integration owner must distinguish bounded workspace preparation admitted from an actual authorized allocation from measured launch requiring the complete experiment and readiness evidence. Preserve those separate references and consumed workspace/client-state assignments, cover additional bounded allocations and reject stale identities or state reuse. Missing model/authentication/test budget must not independently deny otherwise authorized preparation. Missing preparation authority still blocks creation; missing native requirements still blocks native launch.

The selected component distinguishes native schedule admission from ordinary authorized preparation; actual Git workspace creation remains operator-owned under its frozen bounded allocation. Allocation/setup templates are local records; neither evaluator helper supplies that preparation admission or validates every new allocation binding. Do not invoke the experiment evidence reducer as a preparation gate or fill invented native budgets to satisfy it. Record unsupported runtime admission separately and retain reports/prepared workspaces. No shared policy, hooks, supervisor, model completion marker or phase-advance command is installed here.

## H1-H5 mapping for an admitted utility assignment

| Control | Selected protected mechanics | Remaining observation or owner |
| --- | --- | --- |
| H1 / T01-T02 | Session/delivery/assignment identity and output preimage admission; immutable selected input snapshots | Operator authorizes bounded Git preparation and records actual workspace actions; semantic completeness is not a hash predicate |
| H2 / T03-T05 | Required external P2 deterministic-inspection and P3 independent-review gates; native-prerequisites gate before P4 schedule binding | Complete native allocation, authentication and effective isolation/hooks must be separately observed before any worker launch |
| H3 / T06-T08 | Protected C/B/A dependency map, one-use reservations and original campaign clock | Reservation alone is not execution; real process custody and independent exact-tier review are additional prerequisites |
| H4 / T09 | P5 evidence coverage/freshness and ordered phase admission; immutable accepted artifacts | Reducer and producer identities do not authenticate semantic judgments or grant external acceptance |
| H5 / T10-T12 | P6 saved artifact checks, exclusive runtime receipt publication and readback | Prepared continuation is distinct from native transport, rendered delivery and receiving invocation |

The selected schema family is devforge.utility-session/delivery/checkpoint/receipt v1, described in [managed validation](managed-validation.md). The worker supplies substantive artifacts and allocated evidence; protected runtime owns the transition. Do not install the historical generic PreToolUse/Stop proposals beside managed callbacks automatically. Effective provider callbacks require the selected trusted configuration, exactly observed event behavior and external acceptance of their limits. An error, disabled/duplicate hook or failed transport cannot establish managed completion.

Feasibility is Partial: the selected mechanical component is implemented and separately reviewed, while native event coverage, interactive answer transport, semantic grading, actual delivery and acceptance remain separate. Hook status for this authoring package: Design only; not installed, activated, executed, or validated.
