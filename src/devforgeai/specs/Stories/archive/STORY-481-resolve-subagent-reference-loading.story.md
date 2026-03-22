---
id: STORY-481
title: Resolve Subagent Reference Loading Mechanism for EPIC-082
type: feature
epic: EPIC-083
sprint: Backlog
status: QA Approved
points: 2
depends_on: []
priority: Medium
advisory: false
source_gap: null
source_story: null
assigned_to: DevForgeAI AI Agent
created: 2026-02-22
format_version: "2.9"
---

# Story: Resolve Subagent Reference Loading Mechanism for EPIC-082

## Description

**As a** framework maintainer preparing EPIC-082 stories,
**I want** the subagent reference loading mechanism decided and documented (orchestration-driven vs opt-in vs auto-load),
**so that** EPIC-082 story creation has clear implementation guidance for domain reference generation.

## Provenance

```xml
<provenance>
  <origin document="REC-EPIC082-001" section="recommendations-queue">
    <quote>"Decide between orchestration-driven vs opt-in vs auto-load for subagent reference loading. PARTIALLY RESOLVED: 3 approaches documented in epic file with Approach A (orchestration-driven) recommended, but decision explicitly deferred to story creation."</quote>
    <line_reference>recommendations-queue.json, lines 22-30</line_reference>
    <quantified_impact>Unblocks EPIC-082 story creation with clear architectural direction</quantified_impact>
  </origin>
</provenance>
```

## Acceptance Criteria

### AC#1: Decision Documented in EPIC-082

```xml
<acceptance_criteria id="AC1">
  <given>EPIC-082 epic file contains 3 approach options with Approach A recommended</given>
  <when>The reference loading mechanism decision is finalized</when>
  <then>The EPIC-082 epic file is updated with the selected approach clearly marked as the decision (not just a recommendation), with rationale</then>
  <verification>
    <source_files>
      <file hint="Epic file">devforgeai/specs/Epics/EPIC-082-domain-reference-generation.epic.md</file>
    </source_files>
    <test_file>src/tests/STORY-481/test_ac1_decision_documented.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#2: ADR Created for Decision

```xml
<acceptance_criteria id="AC2">
  <given>The reference loading mechanism is an architectural decision affecting multiple subagents</given>
  <when>The decision is finalized</when>
  <then>An ADR is created documenting the decision, alternatives considered, and consequences</then>
  <verification>
    <source_files>
      <file hint="ADR file">devforgeai/specs/adrs/ADR-XXX-subagent-reference-loading.md</file>
    </source_files>
    <test_file>src/tests/STORY-481/test_ac2_adr_created.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#3: Implementation Guidance Section Added

```xml
<acceptance_criteria id="AC3">
  <given>The decision is documented</given>
  <when>EPIC-082 stories are created</when>
  <then>Each EPIC-082 feature has clear implementation guidance referencing the selected loading mechanism</then>
  <verification>
    <source_files>
      <file hint="Epic file">devforgeai/specs/Epics/EPIC-082-domain-reference-generation.epic.md</file>
    </source_files>
    <test_file>src/tests/STORY-481/test_ac3_guidance_added.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "epic-082-decision"
      file_path: "devforgeai/specs/Epics/EPIC-082-domain-reference-generation.epic.md"
      required_keys:
        - key: "Reference Loading Decision"
          type: "string"
          required: true
          validation: "Must specify one of: orchestration-driven, opt-in, auto-load"
          test_requirement: "Test: Verify decision section exists with selected approach"
      requirements:
        - id: "CFG-001"
          description: "Update EPIC-082 with finalized decision (not just recommendation)"
          testable: true
          test_requirement: "Test: Grep for decision marker in epic file"
          priority: "Critical"

  business_rules:
    - id: "BR-001"
      rule: "Architectural decisions affecting multiple subagents require ADR documentation"
      trigger: "When reference loading mechanism is selected"
      validation: "ADR file exists in devforgeai/specs/adrs/"
      error_handling: "HALT if ADR not created"
      test_requirement: "Test: Verify ADR file exists and references EPIC-082"
      priority: "Critical"

  non_functional_requirements: []
```

## Technical Limitations

```yaml
technical_limitations: []
```

## Dependencies

### Prerequisite Stories
- None

## Test Strategy

### Unit Tests
**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Decision documented in EPIC-082, ADR created
2. **Edge Cases:** Partially resolved status updated to fully resolved

## Acceptance Criteria Verification Checklist

### AC#1: Decision Documented
- [x] EPIC-082 updated with selected approach - **Phase:** 3 - **Evidence:** EPIC-082 line 182 DECISION marker
- [x] Rationale included - **Phase:** 3 - **Evidence:** EPIC-082 Rationale paragraph after DECISION

### AC#2: ADR Created
- [x] ADR file exists in adrs/ directory - **Phase:** 3 - **Evidence:** ADR-022-subagent-reference-loading.md
- [x] ADR references all 3 alternatives - **Phase:** 3 - **Evidence:** ADR-022 Alternatives section

### AC#3: Implementation Guidance
- [x] Features reference selected mechanism - **Phase:** 3 - **Evidence:** EPIC-082 Implementation Guidance section

---

**Checklist Progress:** 5/5 items complete (100%)

---

## Definition of Done

### Implementation
- [x] EPIC-082 epic file updated with finalized decision
- [x] ADR created for reference loading mechanism
- [x] Implementation guidance added to EPIC-082 features

### Quality
- [x] All 3 acceptance criteria have passing tests

### Testing
- [x] Unit tests for decision documentation
- [x] Unit tests for ADR existence

### Documentation
- [x] ADR documents decision with alternatives and consequences

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-23

- [x] EPIC-082 epic file updated with finalized decision - Completed: Added ## Reference Loading Decision section with DECISION marker selecting Approach A (orchestration-driven)
- [x] ADR created for reference loading mechanism - Completed: Created ADR-022-subagent-reference-loading.md with all 3 alternatives, decision, rationale, consequences
- [x] Implementation guidance added to EPIC-082 features - Completed: Added ## Implementation Guidance section with per-feature requirements and ADR-022 reference
- [x] All 3 acceptance criteria have passing tests - Completed: 17/17 tests pass across 3 AC test suites
- [x] Unit tests for decision documentation - Completed: test_ac1_decision_documented.sh (5 assertions)
- [x] Unit tests for ADR existence - Completed: test_ac2_adr_created.sh (7 assertions)
- [x] ADR documents decision with alternatives and consequences - Completed: ADR-022 includes orchestration-driven, opt-in, auto-load alternatives with positive/negative/neutral consequences

### TDD Workflow Summary

| Phase | Status | Key Actions |
|-------|--------|------------|
| Red | ✅ | 17 tests written, all failing initially |
| Green | ✅ | ADR-022 created, EPIC-082 updated with decision + guidance |
| Refactor | ✅ | EPIC-082 condensed (~22 lines removed), DRY with ADR-022 |

### Files Created/Modified

| File | Action |
|------|--------|
| devforgeai/specs/adrs/ADR-022-subagent-reference-loading.md | Created |
| devforgeai/specs/Epics/EPIC-082-domain-reference-generation.epic.md | Modified |
| src/tests/STORY-481/test_ac1_decision_documented.sh | Created |
| src/tests/STORY-481/test_ac2_adr_created.sh | Created |
| src/tests/STORY-481/test_ac3_guidance_added.sh | Created |
| src/tests/STORY-481/run_all_tests.sh | Created |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-22 | .claude/story-requirements-analyst | Created | Story created from REC-EPIC082-001 triage | STORY-481.story.md |
| 2026-02-23 | DevForgeAI AI Agent | Dev Complete | Implemented: ADR-022, EPIC-082 decision, implementation guidance, tests | ADR-022, EPIC-082, test files |
| 2026-02-23 | .claude/qa-result-interpreter | QA Deep | PASSED: 17/17 tests, 0 violations, 3/3 validators passed | - |

## Notes

**Source:** REC-EPIC082-001 from framework-analyst (EPIC-082 epic-creation ai-analysis)
**Audit Status:** Resolved — Approach A (orchestration-driven) formally decided via ADR-022.

---

Story Template Version: 2.9
Last Updated: 2026-02-22
