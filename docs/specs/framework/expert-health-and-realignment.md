---
id: DFF-09
status: planning-baseline
implementation_readiness: not-ready
updated: 2026-09-17
---

# Expert health and realignment

## Purpose and ownership

Project expertise can become stale when requirements, architecture, tools or artifact contracts change. This planning baseline defines observable review dimensions and boundaries. It does not implement monitoring, a competence score or automatic repair.

[Skills and project expertise](skills-and-project-expertise.md) owns expert responsibilities and lineage. [Project context and policy](project-context-and-policy.md) owns current project evidence and policy selection. [Quality and delivery](quality-and-delivery.md) owns assessment results and delivery claims. This capability owns the proposed comparison between an expert's relied-upon evidence and current selected inputs. [Subagents and context](subagents-and-context.md) owns any delegated review, while the [foundation](foundation.md) and [index](index.md) establish the wider boundaries.

## Existing contracts to reuse

The [builder adaptive specification, section 7](../../plan/skill-builder-adaptive-enhancement-spec.md) compares selected parent digests, requirements and project evidence. Changed bytes establish changed input, not a semantic defect. It proposes impact without automatic authoring or carrying old validation to new bytes.

The [validator adaptive specification, sections 4–6](../../plan/skill-validator-adaptive-enhancement-spec.md) checks grounding, lineage and handoffs; separates standards, workflow, instructions and behavior; and preserves failures and incomplete coverage. Known-good and defective fixtures expose false positives and missed defects. These are reusable contracts, not an expert-health implementation.

The [builder](../../../src/agents/skills/skill-builder/SKILL.md) authors selected changes; the [validator](../../../src/agents/skills/skill-validator/SKILL.md) assesses exact bytes and proposes revisions. Neither automatically installs or invokes the other. Existing authorization may cover revision; a finding does not grant new effects.

## Inputs and proposed outputs

A review takes the expert/package identity, responsibilities, retained and current evidence, project quality policy, prior observations and triggering change/failure. Execution evidence binds tools, host and candidate. Missing baselines, inaccessible sources and discovery omissions remain visible.

The proposed output is an impact record linking changed or unresolved inputs to affected assertions, responsibilities, tests, resources and handoffs. It identifies evidence that still applies, observations requiring rerun, demonstrated defects and the smallest supported next action. A separate revision proposal describes any required source change. These outputs need a versioned schema decision; fields must not be silently inserted into existing closed adaptive schemas.

Expertise needs a domain-evidence baseline; a variant also needs parent requirement dispositions. Neither claims to capture all possible knowledge.

## Separate health dimensions

Declare measurement scope and report raw counts, identities and limitations. Do not produce a composite competence score.

| Dimension | Meaningful observation and denominator |
| --- | --- |
| Grounding currency | Rechecked, still-supported required assertions divided by all required assertions declared for this review. Also report changed, unsupported, unknown and not-rechecked counts. |
| Requirement/lineage coverage | Requirements with current supported dispositions and verification mappings divided by all applicable selected requirements; missing mappings remain in the denominator. |
| Behavioral evidence | Passing required cases divided by all declared required cases, with failed, errored, blocked and unexecuted counts separately visible. |
| Routing and boundaries | Correct decisions over the declared positive and near-miss cases; show each class and its mistakes so numerous easy cases cannot hide failures. |
| Handoff compatibility | Passing required producer-consumer checks divided by all declared required handoffs, bound to actual artifacts and versions. |

`NOT_RUN` means a check was not executed. `unknown` means applicability, a fact or its supporting evidence is unresolved; it is not a passing result. A justified nonapplicable item has a recorded scope reason. No denominator may be reduced merely because an item is difficult to verify. A zero denominator does not produce 100%: a deliberately empty applicable set is reported as nonapplicable with its scope basis; an unknown or missing set remains unknown/incomplete. If the relevant obligation set cannot be established, report that limitation rather than inventing a whole-expert coverage percentage.

A source digest change triggers investigation, not a failed semantic verdict. An unchanged digest does not prove competence. Elapsed time since review, confidence prose, output length and files read are not substitutes for evidence. Each managed project supplies its selected thresholds and mandatory scenarios; DevForgeAI's own Rust/95% rules remain local framework implementation obligations.

## Bounded review and realignment

A review starts from an explicit selection, a relevant source change or a demonstrated failure under an authorized workflow. Automatic watchers and scheduled reassessment are future proposals. Declare affected scope, intended observations, execution limits and permitted effects before work.

First compare identities and trace affected dependencies. Then perform only necessary source checks and held-out behavior/handoff cases, preserving independent expected outcomes. Retain unaffected observations only when their inputs and prerequisites still match. Return one evidence-backed decision: retain the current guidance, propose a selected revision, or identify the exact unresolved prerequisite.

After authorized authoring, reassess changed behavior and affected integration against the new candidate. Keep older attempts and findings. Further cycles require a new concrete failure, change or unresolved concern; they are not a fixed ritual. Budget exhaustion remains incomplete evidence. Operational rewriting, installation, upstream overwrite and binding changes require their corresponding authorization.

## Feedback during work and after delivery

Lessons can be recorded when observed during discovery, specification, development or QA, as well as in a later retrospective. DFF-02 owns the general follow-up handoff; this capability receives only relevant stale/conflicting expertise or variant evidence. A process-friction observation records the concrete event, evidence, affected work, proposed owner and whether it is an immediate blocker or unselected improvement. A product idea remains a post-MVP/epic/sprint proposal until selected; it does not silently amend the current objective.

Separate a proposed core improvement, project specialization, policy revision and expert correction by the responsibility that actually needs to change. Reuse existing guidance when it remains sufficient. Authorized authoring and independent reassessment follow their own contracts; feedback does not automatically mutate operational skills, constitutional documents or bindings. MIG-03 still requires a versioned expert-health record, so these logical fields must not be inserted into closed adaptive records.

The prohibition on a composite expert competence score remains in force. A separately proposed [story-readiness rubric](work-items-and-dependencies.md#readiness-parallel-work-and-sprint-grouping) has a different purpose, but it cannot waive known blockers or claim an uncalibrated probability of AI completion.

## Observable scenarios

**Fictional OrderDesk:** cancellation is permitted before dispatch and denied afterward; racing cancellation and dispatch must not produce contradictory states. These are walkthrough inputs, not actual project requirements. An expert's stale return-window guidance prompts bounded review. Business analysis confirms the cancellation boundary; architecture owns the race contract; development and QA consume the same revision. QA checks after-dispatch and concurrent-operation counterexamples. Detection, a scoped proposal and a later passing retest demonstrate realignment for this change, not general expertise certification or automatic adoption.

If the referenced document changed only punctuation, review can retain the guidance with a supported explanation. If dispatch has two contradictory definitions, affected conclusions remain unresolved. If a required host is unavailable, that native case stays `NOT_RUN`; passing text review does not replace it. If a producer still emits the old contract, the consumer check fails despite both packages having individually passing observations.

## Decisions before implementation

Resolve baseline ownership, stable assertion/dependency identities, review triggers, denominator declaration, independent semantic labels, and execution limits. Define versioning that preserves historical facts and quality results.

The bounded next expansion is one synthetic OrderDesk expert, one changed rule, one unchanged control and one incompatible handoff. Specify exact observations and the proposed record before building a health service. Keep automated monitoring and broader calibration work in [roadmap and decisions](roadmap-and-decisions.md).
