---
template_version: "0.1.0"
format_version: "0.1.0"
---

<!-- SECTION_MANIFEST
sections:
  - {name: "Description", header_level: 2, status: "Required"}
  - {name: "Provenance", header_level: 2, status: "Required"}
  - {name: "Acceptance Criteria", header_level: 2, status: "Required"}
  - {name: "Technical Specification", header_level: 2, status: "Required"}
  - name: "UI Specification"
    header_level: 2
    status: "Conditional"
    condition: "The selected story changes a user interface, including terminal interactions."
  - name: "Implementation Guide"
    header_level: 2
    status: "Conditional"
    condition: "Cross-cutting implementation guidance is needed, including feature stories estimated >=5 on the default scale."
    subsections: ["Architecture Decisions", "Cross-Cutting Concerns", "Implementation Sequence", "Task Prompt Templates", "Anti-Patterns", "Patterns and References"]
  - {name: "Technical Limitations", header_level: 2, status: "Required"}
  - name: "Non-Functional Requirements (NFRs)"
    header_level: 2
    status: "Required"
    subsections: ["Performance", "Security", "Scalability", "Reliability", "Observability"]
  - name: "Dependencies"
    header_level: 2
    status: "Required"
    subsections: ["Prerequisite Stories", "External Dependencies", "Technology Dependencies"]
  - name: "Test Strategy"
    header_level: 2
    status: "Required"
    subsections: ["Unit Tests", "Integration Tests"]
    optional_subsections: ["E2E Tests"]
  - {name: "Acceptance Criteria Verification Checklist", header_level: 2, status: "Required"}
  - {name: "Edge Cases", header_level: 2, status: "Required"}
  - name: "Definition of Done"
    header_level: 2
    status: "Required"
    subsections: ["Implementation", "Quality", "Testing", "Documentation", "TDD Workflow Summary", "Files Created/Modified"]
  - {name: "Change Log", header_level: 2, status: "Required"}
  - {name: "Notes", header_level: 2, status: "Required"}
END_SECTION_MANIFEST -->

Authoring template only: generate the document between BEGIN_STORY and END_STORY. Fill placeholders from selected facts/decisions; remove instructional comments and unused conditional sections/rows. Preserve required sections with a concrete non-applicability explanation where justified. Do not copy example content as a product requirement. Story/template version comes from the metadata above; nested technical format is independently versioned.

<!-- BEGIN_STORY -->
---
id: STORY-NNN
title: "<Selected observable outcome>"
type: feature
epic: null
sprint: Backlog
status: Backlog
points: null
depends_on: []
priority: Medium
advisory: false
source_gap: null
source_story: null
from_recommendations: false
source_recommendations: null
cycle_recorded: null
# For RCA-origin stories also populate source_rca, source_recommendation,
# rca_addresses_why and rca_evidence_files from the actual selected source.
feature_ref: ""
source_devarch: ""
branch: null
pr_base: null
worktree_path: null
pr_number: null
pr_url: null
pr_merged: false
merged_sha: null
merged_at: null
assigned_to: Unassigned
created: YYYY-MM-DD
format_version: "0.1.0"
---

# Story: <Selected outcome>

## Description

**As a** <actual actor>, **I want** <capability>, **so that** <value>.

**In scope:** <selected behavior and deliverables>.

**Out of scope:** <explicit boundaries>.

**Observable completion:** <result and the observation that will demonstrate it>.

## Provenance

| Source and current identity | Clause/decision | Story responsibility | Supported context |
| --- | --- | --- | --- |
| <project-relative source or actual user request> | <stable ID/heading> | <owned requirement or referenced shared rule> | <verified fact/decision, with quote/locator if needed> |

<!-- Optional XML provenance/rca_origin may be embedded here when supplied source structure benefits the consumer. Preserve exact facts and escape XML. -->

## Acceptance Criteria

### AC#1: <Observable result>

```xml
<acceptance_criteria id="AC1" implements="SVC-001">
  <given>Selected precondition, actor and relevant state</given>
  <when>Selected action or event</when>
  <then>Concrete permitted result, side effects and invariants</then>
</acceptance_criteria>
```

<!-- Add the actual required success, denial, boundary and recovery criteria. Omit implements only when there is a documented non-component mapping. -->

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"
  components:
    - id: COMP-001
      type: Service
      name: "<actual or planned component>"
      file_path: "<project-relative path>"
      description: "<responsibility and ownership>"
      interface: "<selected operation contract>"
      dependencies: []
      requirements:
        - id: SVC-001
          implements_ac: [AC1]
          description: "<specific required behavior>"
          testable: true
          test_requirement: "Test: <input/action and expected observation>"
          priority: High
  business_rules: []
  non_functional_requirements: []
```

<!-- Replace the component example with real applicable kinds, fields and complete schemas/interfaces. Empty arrays require an actual non-applicability reason. -->

| AC / source clause | Component/rule/NFR or document obligation | Planned verification |
| --- | --- | --- |
| AC1 / <source clause> | <resolving ID and responsibility> | <specific test or document observation> |

## UI Specification

<!-- Conditional: remove this whole section when no UI behavior is selected and state the reason in Notes. -->

### Components

<Component purposes, data, states and validation.>

### Layout Mockup

<Terminal-readable hierarchy/wireframe and actual responsive constraints.>

### Component Interfaces

<Inputs, outputs, events and data/API relationships.>

### User Interactions

<Action, state change, success, denial/failure, retry and cancellation.>

### Accessibility

<Applicable keyboard/focus/naming/announcement/visual requirements and verification.>

## Implementation Guide

<!-- Conditional under SECTION_MANIFEST; remove the whole section if not applicable. -->

### Architecture Decisions

<Selected boundaries/alternatives/rationale, citing canonical decisions.>

### Cross-Cutting Concerns

<Data/error flow, concurrency, security and shared invariants.>

### Implementation Sequence

<Dependency-ordered behavioral slices; no mandatory agent or phase per slice.>

### Task Prompt Templates

<Useful optional handoff with exact scope/inputs/outputs, or explain why none is needed.>

### Anti-Patterns

<Relevant rejected approaches and concrete reasons.>

### Patterns and References

<Inspected existing examples and their applicability.>

## Technical Limitations

```yaml
technical_limitations: []
```

<Known limitations with impact and current decision, or the observed basis for none identified. No silent deferrals.>

## Non-Functional Requirements (NFRs)

### Performance

<Source-defined workload/metric/method, or grounded non-applicability.>

### Security

<Threats, permission/data boundaries and observable denial/protection requirements.>

### Scalability

<Actual load/data/concurrency constraints, or grounded non-applicability.>

### Reliability

<Failure, timeout, recovery and consistency obligations, or grounded non-applicability.>

### Observability

<Required events/metrics/errors and prohibited sensitive content, or grounded non-applicability.>

## Dependencies

### Prerequisite Stories

| Producer | Required artifact/decision/evidence | Consumer need | Satisfaction observation |
| --- | --- | --- | --- |
| <resolving story ID or explicit unresolved prerequisite> | <concrete interface> | <why necessary> | <what proves it available> |

### External Dependencies

<Selected external interface, ownership and availability/permission requirements, or none.>

### Technology Dependencies

<Approved runtime/library/tool constraints with governing references, or none.>

## Test Strategy

### Unit Tests

<Concrete cases and oracles per AC/rule, denied/invalid cases, or documentation review observations for prose-only work.>

### Integration Tests

<Real producer-consumer boundaries, failure recovery and required platform evidence, or concrete non-applicability.>

### E2E Tests

<Conditional end-to-end/native/UI observations; remove this subsection when inapplicable.>

<State actual project quality thresholds, source denominator/exclusions, tools and measurement method where required. Planned verification is not execution.>

## Acceptance Criteria Verification Checklist

- [ ] AC1: <specific planned observation and expected result; add every selected AC and cross-cutting obligation>

## Edge Cases

| Condition | Expected behavior and unchanged state | AC/test mapping |
| --- | --- | --- |
| <applicable boundary, invalid input, denial or recovery> | <concrete result> | <resolving AC or test obligation> |

## Definition of Done

### Implementation

- [ ] <Required observable behavior and interfaces delivered under selected scope.>

### Quality

- [ ] <Applicable formatting/static analysis/regression and independently measured project thresholds.>

### Testing

- [ ] <All mandatory selected scenarios and platforms have current candidate-bound results; gaps remain explicit.>

### Documentation

- [ ] <Required usage/interface/decision documentation matches actual delivered behavior.>

### TDD Workflow Summary

<Planned project-required red, green, refactor and QA obligations, or accurate prose-only non-applicability. No fabricated executions.>

### Files Created/Modified

<Planned product/test/document paths and responsibilities. None are claimed delivered by story authoring.>

## Change Log

| Date | Actor | Change | Evidence |
| --- | --- | --- | --- |
| <actual date> | <actual author role> | Created planning story | <selected request and source identity> |

## Notes

**Open decisions:** <question, owner, affected requirement and readiness impact; state none only when supported>.

**Assumptions/estimates:** <disclosed defaults and rationale>.

**UI applicability:** <selected interface or concrete reason none is needed>.

**Author review:** <actual content observations and limitations; no product test/QA acceptance claim>.

**Next action:** <manual consumer, literal story/source paths and selected scope; no automatic invocation>.
<!-- END_STORY -->
