# Enforced validation workflow and hook proposals

All validator phases P1-P6 and tasks T01-T12 are Enforced requirements, explicitly selected by the user on 2026-09-07. No tasks inherit an unrecorded optional default. Runtime hook deployment is outside skill-builder's authoring scope.

## Requirement mapping

| Proposal | Protected transition | Covered tasks | Required evidence |
|---|---|---|---|
| H1 Intake guard | Start measured inspection/review or native evaluation | T01-T02 | Selected target/spec/cases/rubric identities; owner/write fence; baseline; budget and runtime arrangement |
| H2 Native launch guard | Start target scripts or native task workers | T03-T05 | Relevant structural result; independent AI review or documented inability; observed filesystem/process/client-state boundaries; explicit permitted native runtime |
| H3 Tier order guard | Start dependent tier B or A campaign | T06-T08 | Applicable prior C/B observations; failures/unavailability preserved; no dependent PASS claim when a prerequisite is unavailable |
| H4 Verdict guard | Write a suitable-for-stated-scope or passing completion record | T09 | Frozen plan and all required current evidence; coherent decision receipt and no missing required observations |
| H5 Handoff guard | Announce final delivery or transfer work to builder | T10-T12 | Saved verification report, bounded enhancement specification, output identities, incomplete-work causes, next owner and handoff |

Each proposal applies only to a registered validator evaluation assignment and its protected candidate/outbox paths. It must not infer the active workflow from arbitrary words in a chat or run globally against unrelated tasks.

## Proposed event and decision design

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

## Current implementation status

- Workflow obligations and evidence-result rules are authored in this skill.
- inspect_skill.py and assess_evidence.py implement deterministic inspection/record processing; they are not native launch enforcers.
- H1-H5 are design proposals only. No hook files/configuration are installed, activated, run or validated by this authoring package.
- Feasibility: Partial with ordinary Codex hooks; complete workflow/semantic enforcement is not established.
- Reference: [official Codex hooks](https://learn.chatgpt.com/docs/hooks). Recheck actual target runtime documentation before proposing concrete configuration.
