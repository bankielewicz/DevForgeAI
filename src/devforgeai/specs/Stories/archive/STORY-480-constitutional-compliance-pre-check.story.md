---
id: STORY-480
title: Add Constitutional Compliance Pre-Check to Requirements Elicitation Workflow
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

# Story: Add Constitutional Compliance Pre-Check to Requirements Elicitation Workflow

## Description

**As a** framework user running /ideate or /create-epic,
**I want** a constitutional compliance pre-check step that verifies dependency graphs respect immutability rules,
**so that** ADR creation requirements are identified as Day 0 prerequisites before story creation begins.

## Provenance

```xml
<provenance>
  <origin document="REC-EPIC081-001" section="recommendations-queue">
    <quote>"Verify dependency graphs respect immutability rules (ADR before structural changes) during /ideate or /create-epic, not after. Add Phase N.5 step that flags ADR creation as Day 0 prerequisite."</quote>
    <line_reference>recommendations-queue.json, lines 10-18</line_reference>
    <quantified_impact>Prevents post-hoc ADR creation which delays story readiness</quantified_impact>
  </origin>
</provenance>
```

## Acceptance Criteria

### AC#1: Phase N.5 Step Added to Discovering-Requirements Skill

```xml
<acceptance_criteria id="AC1">
  <given>The discovering-requirements SKILL.md contains the requirements elicitation workflow phases</given>
  <when>A new Phase N.5 (Constitutional Compliance Check) step is added between feature decomposition and requirements output</when>
  <then>The phase checks each proposed feature for structural changes that would require ADR creation per architecture-constraints.md immutability rules</then>
  <verification>
    <source_files>
      <file hint="Main skill file">.claude/skills/discovering-requirements/SKILL.md</file>
    </source_files>
    <test_file>src/tests/STORY-480/test_ac1_phase_step_exists.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#2: ADR Prerequisite Flagging

```xml
<acceptance_criteria id="AC2">
  <given>A proposed feature requires changes to context files, source-tree structure, or technology stack</given>
  <when>The constitutional compliance pre-check phase executes</when>
  <then>The feature is flagged with a warning indicating ADR creation is a Day 0 prerequisite, and the specific context file(s) affected are listed</then>
  <verification>
    <source_files>
      <file hint="Main skill file">.claude/skills/discovering-requirements/SKILL.md</file>
    </source_files>
    <test_file>src/tests/STORY-480/test_ac2_adr_flagging.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#3: Non-Blocking Warning Output

```xml
<acceptance_criteria id="AC3">
  <given>The pre-check identifies features requiring ADRs</given>
  <when>The check completes</when>
  <then>A summary is displayed listing all flagged features with their required ADR topics, without halting the workflow (warning, not blocker)</then>
  <verification>
    <source_files>
      <file hint="Main skill file">.claude/skills/discovering-requirements/SKILL.md</file>
    </source_files>
    <test_file>src/tests/STORY-480/test_ac3_warning_output.sh</test_file>
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
      name: "discovering-requirements-skill-phase"
      file_path: ".claude/skills/discovering-requirements/SKILL.md"
      required_keys:
        - key: "Phase N.5: Constitutional Compliance Check"
          type: "string"
          example: "Check proposed features against 6 context file immutability rules"
          required: true
          validation: "Phase must appear between feature decomposition and output phases"
          test_requirement: "Test: Verify Phase N.5 section exists in SKILL.md with correct position"
      requirements:
        - id: "CFG-001"
          description: "Add Phase N.5 step to discovering-requirements SKILL.md"
          testable: true
          test_requirement: "Test: Grep for 'Constitutional Compliance' or 'Phase N.5' in SKILL.md"
          priority: "Critical"
        - id: "CFG-002"
          description: "Phase checks each feature against architecture-constraints.md immutability rules"
          testable: true
          test_requirement: "Test: Verify phase references architecture-constraints.md"
          priority: "High"
        - id: "CFG-003"
          description: "Flag features requiring ADR with Day 0 prerequisite warning"
          testable: true
          test_requirement: "Test: Verify warning output format includes ADR topic and affected context file"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Any feature proposing changes to context files (tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md) must flag ADR creation as prerequisite"
      trigger: "During Phase N.5 execution"
      validation: "Check feature description for keywords: new technology, structural change, new dependency, pattern change"
      error_handling: "Display warning but do not halt workflow"
      test_requirement: "Test: Verify flagging logic triggers for context-file-changing features"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Phase N.5 must not add more than 2 seconds to workflow execution"
      metric: "< 2 seconds additional latency"
      test_requirement: "Test: Verify phase completes within time budget"
      priority: "Medium"
```

## Technical Limitations

```yaml
technical_limitations: []
```

## Non-Functional Requirements (NFRs)

### Performance
- Phase N.5 execution: < 2 seconds additional latency

### Reliability
- Non-blocking: Warning failures must not halt /ideate or /create-epic workflows

## Dependencies

### Prerequisite Stories
- None

### Technology Dependencies
- None (Markdown documentation changes only)

## Test Strategy

### Unit Tests
**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Feature proposing new technology triggers ADR warning
2. **Edge Cases:**
   - Feature with no structural changes produces no warnings
   - Multiple features each requiring different ADRs
3. **Error Cases:**
   - Malformed feature description still processes without crash

## Acceptance Criteria Verification Checklist

### AC#1: Phase N.5 Step Added
- [x] Phase N.5 section exists in SKILL.md - **Phase:** 2 - **Evidence:** src/claude/skills/discovering-requirements/SKILL.md line 281
- [x] Phase positioned correctly in workflow - **Phase:** 2 - **Evidence:** Between Phase 2 (line 263) and Phase 3 (line 368)

### AC#2: ADR Prerequisite Flagging
- [x] Features requiring context file changes are flagged - **Phase:** 3 - **Evidence:** 5/5 tests pass
- [x] Warning includes affected context file names - **Phase:** 3 - **Evidence:** All 6 context files listed in table

### AC#3: Non-Blocking Warning Output
- [x] Summary displays flagged features with ADR topics - **Phase:** 3 - **Evidence:** 5/5 tests pass
- [x] Workflow continues after warnings - **Phase:** 3 - **Evidence:** "non-blocking" + "Proceed to Phase 3"

---

**Checklist Progress:** 6/6 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Phase N.5 added to discovering-requirements SKILL.md
- [x] Constitutional compliance check logic documented
- [x] ADR prerequisite flagging format defined
- [x] Non-blocking warning output format specified

### Quality
- [x] All 3 acceptance criteria have passing tests
- [x] Edge cases covered (no-change features, multiple ADR needs)

### Testing
- [x] Unit tests for Phase N.5 detection
- [x] Unit tests for ADR flagging logic
- [x] Unit tests for warning output format

### Documentation
- [x] SKILL.md updated with Phase N.5
- [x] Phase N.5 purpose documented inline

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-23

- [x] Phase N.5 added to discovering-requirements SKILL.md - Completed: Added Phase 2.5 Constitutional Compliance Pre-Check between Phase 2 and Phase 3
- [x] Constitutional compliance check logic documented - Completed: Pseudocode checking features against 6 context file immutability rules
- [x] ADR prerequisite flagging format defined - Completed: WARNING format with affected files and required ADR topics
- [x] Non-blocking warning output format specified - Completed: Summary report with "Proceed to Phase 3" continuation
- [x] All 3 acceptance criteria have passing tests - Completed: 14/14 tests pass across 3 test files
- [x] Edge cases covered (no-change features, multiple ADR needs) - Completed: Example shows both multi-ADR and no-prerequisite paths
- [x] Unit tests for Phase N.5 detection - Completed: test_ac1_phase_step_exists.sh (4 tests)
- [x] Unit tests for ADR flagging logic - Completed: test_ac2_adr_flagging.sh (5 tests)
- [x] Unit tests for warning output format - Completed: test_ac3_warning_output.sh (5 tests)
- [x] SKILL.md updated with Phase N.5 - Completed: src/claude/skills/discovering-requirements/SKILL.md
- [x] Phase N.5 purpose documented inline - Completed: Purpose statement and procedure documented in SKILL.md

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Red | ✅ Complete | 14 tests written, all FAIL |
| Green | ✅ Complete | Phase 2.5 added, 14/14 tests PASS |
| Refactor | ✅ Complete | No refactoring needed (clean documentation) |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/discovering-requirements/SKILL.md | Modified | +85 lines (Phase 2.5 section) |
| src/tests/STORY-480/test_ac1_phase_step_exists.sh | Created | 67 lines |
| src/tests/STORY-480/test_ac2_adr_flagging.sh | Created | 63 lines |
| src/tests/STORY-480/test_ac3_warning_output.sh | Created | 63 lines |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-22 | .claude/story-requirements-analyst | Created | Story created from REC-EPIC081-001 triage | STORY-480.story.md |
| 2026-02-23 | .claude/qa-result-interpreter | QA Deep | PASSED: 14/14 tests, 0 violations | STORY-480-qa-report.md |

## Notes

**Source:** REC-EPIC081-001 from framework-analyst (EPIC-081 epic-creation ai-analysis)

**Design Decisions:**
- Non-blocking warning approach chosen over hard blocker to avoid disrupting ideation flow
- Check targets all 6 context files for comprehensive coverage

**Related ADRs:**
- None yet (this story enables ADR-awareness in the workflow)

---

Story Template Version: 2.9
Last Updated: 2026-02-22
