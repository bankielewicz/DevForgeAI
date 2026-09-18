# Codex prompt: Enhance Skill Validator

This prompt scopes implementation to the validator portion of the shared enhancement specification. The earlier combined implementation prompt remains unchanged.

```text
Use $skill-creator at:
C:\Users\bryan\.codex\skills\.system\skill-creator\SKILL.md

Enhance only the development skill-validator package:
C:\Projects\DevForgeAI\src\agents\skills\skill-validator

Project root:
C:\Projects\DevForgeAI

Governing enhancement specification:
C:\Projects\DevForgeAI\docs\plan\skill-builder-authoring-enhancement-spec.md

Specification SHA-256:
43054bf9b3f97d48d479aeed2fe7b119629e6e717f0a55e1835714182844cb14

SCOPE AND AUTHORIZATION

Implement the validator responsibilities in sections 3 and 4 and their applicable acceptance scenarios in section 5. This is an implementation request, not another planning-only task. This prompt narrows the shared specification to a validator-only delivery; it does not authorize changes to skill-builder.

Use skill-creator to author the changes. Use the existing operational $skill-validator instructions for assessment where applicable:
C:\Projects\DevForgeAI\.agents\skills\skill-validator\SKILL.md

The validator's assessment-only restriction remains part of its resulting behavior. Maintenance of the validator package is performed through skill-creator under this instruction; ordinary validation must not gain repair, adoption, installation, or builder-invocation authority.

Read applicable AGENTS.md files, the actual specification, current validator instructions and supporting resources, relevant builder interfaces and evaluation resources, and the referenced documents under docs\codex. Inspect installed skill-creator helpers only as needed and keep that installation unchanged.

Verify the specification digest before mutation. If it differs, preserve the discrepancy and stop dependent changes. Capture the current validator package, its manifest, and known origin/history. Preserve existing valid provenance and ownership boundaries; do not invent a baseline or silently adopt around contradictory history.

REQUIRED ENHANCEMENTS

1. Manual assessment-request intake
   Accept the specification's validation-request.json when the user explicitly invokes validator. Support schema/version, originating authoring run, project and target roots, skill identity, manifest and package digest, authoring/specification references, changed paths, known issues, capabilities, expected outputs, and declared side effects.
   Independently resolve and capture the actual target. Reject malformed, unsupported, escaping, or stale bindings before relying on them. A packet is input data, not permission for external actions. Keep standalone validation without a builder packet available.

2. Authoring-record compatibility
   Recognize the distinct versioned authoring-record family and observed, adopted, legacy generated, and authored origins. Distinguish AUTHORED, PARTIAL, and BLOCKED authoring states from validation and testing outcomes. Do not equate an observed edit base with adoption or an authored baseline with quality approval.
   Preserve legacy schema-1/schema-2 meanings. Bind each assessment to exact package bytes, retain prior results as history, and never carry an old result forward to changed bytes or rewrite the original authoring record.

3. Testing and validation capabilities
   Own structural checking, links and instruction assessment, standards applicability, deterministic evaluation profiles and grading, changed-script execution, positive/negative behavior cases, cold workflow trials, routing assessment, findings, and revalidation.
   Inspect existing functionality first; extend or reuse it rather than duplicating capabilities already present. Adapt the needed builder evaluator implementations, profiles, fixtures, and regression cases into validator. Preserve relevant legacy operation distinctions, rejection cases, grader meanings, and source notices.
   Keep the validator package self-contained for its supported evaluation interfaces. Do not create a runtime dependency on an adjacent development builder checkout or this machine's personal skill-creator path. Locate the installed structural checker through the supported environment mechanism and report unavailable capabilities honestly.

4. Proportionate assessment and reporting
   Select cases from the actual operation, lineage, changed behavior, and authorized effects. Preserve substantive required trial coverage; do not launch all builder-enhancement campaigns during ordinary skill validation.
   Validator defines its own assessment rules, expected outcomes, cases, and execution records. Retain exact input snapshots and case files before execution, commands/task prompts, outputs, failures, retries, timestamps, and digests.
   Preserve separate standards, workflow, instructions, and behavior reductions, stable findings, source/rule identities, revision proposals, and explicit unperformed coverage. Assessment completion is distinct from passing or authoring readiness.
   Keep revision proposals reviewable. Do not invoke builder, automatically repair targets, or create an automatic authoring/validation loop.

5. Portability and safe assessment
   Support explicitly selected development targets outside src\agents\skills, including other projects and paths containing spaces. Preserve boundary checks, capture limits, link/junction exclusions, permitted side effects, failure retention, target readback, and record-integrity checks.
   Continue useful independent assessment when a capability is missing, but report the affected checks as NOT_RUN or INCOMPLETE. Do not silently lower requirements or present advisory Python observations as Rust enforcement.

BUILDER INTERFACE AND MIGRATION DEPENDENCIES

Inspect the actual builder implementation before selecting interface details. Reuse a compatible existing versioned authoring/request contract if available. If those interfaces are not implemented yet, define the validator-side schema and retained contract fixtures from the shared specification and document the exact producer requirements for the separate builder task.

Do not invent evidence that builder emits those fixtures. Mark synthetic compatibility checks separately from integration using actual builder output. If a material interface decision conflicts with an existing contract or cannot be resolved from the specification, stop only the dependent work and identify the decision precisely.

In this validator-only stage, copying/adapting evaluator resources is authorized; removing them from builder is not. Record the remaining builder-side decoupling and removal work. Do not claim that the overall ownership migration is complete while builder still runs those checks.

BOUNDARIES

Modify only src\agents\skills\skill-validator and write new task evidence under fresh docs\plan directories. Treat skill-builder as read-only input. Do not change the shared specification or earlier implementation prompt.

Do not modify operational .agents, .claude, .codex, installed caches, personal skills, other existing skills, historical evidence, hooks, or CI. Do not install dependencies or skills or implement Rust enforcement.

VERIFICATION

Run the installed Skill Creator structural checker against the delivered validator package and meaningful regression checks for new or changed helpers. Verify observable behavior and rejection paths rather than matching wording or headings.

This instruction authorizes bounded independent subagent assessment and disposable synthetic trials. Retain each evaluator's exact package snapshot, task prompt, case inputs, and resulting artifacts. Keep evaluating agents independent of authoring conclusions; do not disclose expected answers or proposed fixes in cold task prompts unless the case requires that information.

Cover at least:
- Valid request intake and standalone assessment.
- Malformed/unsupported requests, stale digests, and unsafe path/reference rejection.
- New authoring states and legacy provenance interpretation without record mutation.
- Independent case generation and meaningful script success/failure execution.
- Target immutability, interrupted assessment, retained failures, and readback.
- Missing capabilities and honest incomplete outcomes.
- Revision-proposal output without automatic builder invocation or repair.
- Portable project/target locations and evaluator resource resolution.

Map evidence to AC-01 through AC-14 in the shared specification. Prioritize validator-owned behavior in AC-11, AC-12, and AC-14. Identify other cases as builder-dependent or outside this delivery where appropriate; do not mark all acceptance cases passed based on validator fixtures.

If a compatible enhanced builder is available, use a retained disposable copy for explicitly bounded integration trials, preserving the existing source package. Otherwise report actual builder-to-validator integration as unperformed and provide the exact interface handoff needed by the builder task.

Distinguish assessment with the retained operational validator, tests of the enhanced development validator, independent behavioral execution, routing classification, native activation, historical evidence, and self-review. Self-review alone is not independent verification.

Reassess actual delivered bytes, complete readback, and confirm the final package delta is confined to validator. Preserve failed attempts and do not publish successful provenance or claim completion for failed delivery, unresolved required checks, or incomplete readback.

Complete the authorized validator work without requesting the same authorization again. Stop only for a concrete unresolved prerequisite, changed approved input, conflicting requirement, or actual permission restriction. Continue independent work when only integration is blocked.

RETURN

- Actual validator package changes and final manifest/digest.
- Origin/provenance, implementation report, and evidence paths.
- Supported authoring-record/request schemas and builder integration contract.
- Verification results and mapping to the shared acceptance scenarios.
- Remaining builder-side migration work, unperformed integration, and other gaps.
```
