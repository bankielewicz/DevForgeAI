---
id: STORY-530
title: Phase File TaskCreate Integration
type: feature
epic: EPIC-086
sprint: Sprint-22
status: Ready for Dev
points: 3
depends_on: ["STORY-525"]
priority: High
advisory: false
assigned_to: DevForgeAI AI Agent
created: 2026-03-02
format_version: "2.9"
---

# Story: Phase File TaskCreate Integration

## Description

**As a** developer using /dev,
**I want** progressive task disclosure (one phase at a time) in all 12 phase files,
**so that** context bloat doesn't cause late-phase skipping and I only see 4-8 tasks for the current phase instead of ~72 for all phases.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-013" section="progressive-disclosure">
    <quote>"Progressive task disclosure (4-8 active tasks vs 72) directly combats context bloat"</quote>
    <line_reference>Epic EPIC-086, line 261</line_reference>
    <quantified_impact>90% reduction in active task list (72 → 4-8 items per phase)</quantified_impact>
  </origin>
</provenance>
```

## Acceptance Criteria

### AC#1: Progressive Task Disclosure Section Added to All 12 Phase Files

```xml
<acceptance_criteria id="AC1" implements="PTD-001">
  <given>All 12 phase files exist at src/claude/skills/implementing-stories/phases/</given>
  <when>Each file is updated with a "## Progressive Task Disclosure" section</when>
  <then>All 12 files contain the section with: (1) Purpose statement, (2) Registry read instruction (.claude/hooks/phase-steps-registry.json), (3) Phase filtering logic, (4) TaskCreate instructions for current phase steps only.</then>
  <verification>
    <source_files>
      <file hint="Phase files">src/claude/skills/implementing-stories/phases/phase-01-preflight.md</file>
      <file hint="Phase files">src/claude/skills/implementing-stories/phases/phase-02-test-first.md</file>
    </source_files>
    <test_file>tests/STORY-530/test_ac1_section_presence.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: TaskCreate Tasks Created Only for Current Phase Steps

```xml
<acceptance_criteria id="AC2" implements="PTD-002">
  <given>Registry contains 72 steps across 12 phases</given>
  <when>Phase 03 file executes Progressive Task Disclosure</when>
  <then>TaskCreate calls generated ONLY for phase 03 steps (~6 tasks). Zero tasks for other phases. Step ID in subject uses dotted format: "Step 03.1: {description}".</then>
  <verification>
    <source_files>
      <file hint="Phase file">src/claude/skills/implementing-stories/phases/phase-03-implementation.md</file>
    </source_files>
    <test_file>tests/STORY-530/test_ac2_phase_filtering.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: TaskUpdate Instruction for Step Completion

```xml
<acceptance_criteria id="AC3" implements="PTD-003">
  <given>Progressive Task Disclosure section is present</given>
  <when>Developer completes a step</when>
  <then>Clear instruction provided to use TaskUpdate to mark task complete. Example format included with variable placeholders.</then>
  <verification>
    <source_files>
      <file hint="Phase files">src/claude/skills/implementing-stories/phases/phase-01-preflight.md</file>
    </source_files>
    <test_file>tests/STORY-530/test_ac3_taskupdate.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Error Handling for Missing Registry

```xml
<acceptance_criteria id="AC4" implements="PTD-004">
  <given>phase-steps-registry.json is missing or malformed</given>
  <when>Progressive Task Disclosure section attempts to read registry</when>
  <then>Missing registry: HALT with message referencing STORY-525. Malformed JSON: HALT with error. Invalid step entries: skip with warning, continue with valid steps.</then>
  <verification>
    <source_files>
      <file hint="Phase files">src/claude/skills/implementing-stories/phases/phase-01-preflight.md</file>
    </source_files>
    <test_file>tests/STORY-530/test_ac4_error_handling.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### Source Files Guidance

12 phase files at src/claude/skills/implementing-stories/phases/.

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "ProgressiveTaskDisclosure"
      file_path: "src/claude/skills/implementing-stories/phases/"
      required_keys:
        - key: "Progressive Task Disclosure section"
          type: "markdown"
          required: true
          test_requirement: "Test: All 12 phase files contain ## Progressive Task Disclosure section"

  business_rules:
    - id: "BR-001"
      rule: "Tasks created ONLY for current phase — never for other phases"
      trigger: "When Progressive Task Disclosure section executes"
      validation: "TaskCreate calls match current phase number from filename"
      error_handling: "Steps from other phases silently skipped"
      test_requirement: "Test: Phase 03 creates only 'Step 03.*' tasks"
      priority: "Critical"
    - id: "BR-002"
      rule: "Conditional steps marked with (conditional) suffix"
      trigger: "When creating TaskCreate for conditional step"
      validation: "conditional: true → suffix added to subject"
      error_handling: "Missing conditional field defaults to false"
      test_requirement: "Test: Conditional steps have (conditional) in subject"
      priority: "Medium"
    - id: "BR-003"
      rule: "Phase 04.5 and 05.5 handled correctly"
      trigger: "When extracting phase number from filename"
      validation: "Decimal phase IDs parse correctly"
      error_handling: "Regex supports NN.N format"
      test_requirement: "Test: phase-04.5 file creates 'Step 4.5.*' tasks"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Registry read and filtering < 500ms"
      metric: "< 500ms for 200+ step registry"
      test_requirement: "Test: Registry parsing < 500ms"
      priority: "Medium"
    - id: "NFR-002"
      category: "Scalability"
      requirement: "Section adds < 15% to phase file size"
      metric: "100-150 lines per section"
      test_requirement: "Test: Section size within bounds"
      priority: "Low"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "TaskCreate tool"
    limitation: "TaskCreate may not be available in all environments"
    decision: "workaround:Graceful degradation — display step list as markdown if TaskCreate unavailable"
    discovered_phase: "Architecture"
    impact: "Low — fallback provides same information"
```

---

## Non-Functional Requirements (NFRs)

### Performance

- Registry read and filtering: < 500ms

---

### Security

- JSON injection prevention: standard parser only
- No eval() or exec() with registry values

---

### Scalability

- Supports 500+ step registries
- O(n) filtering by phase

---

### Reliability

- HALT on missing registry (clear error message)
- Skip invalid entries, continue with valid ones

---

### Observability

- Step creation logged per phase
- Invalid entries reported with warnings

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-525:** Phase Steps Registry + Step-Level Tracking
  - **Why:** Provides registry JSON at .claude/hooks/phase-steps-registry.json
  - **Status:** Backlog

### External Dependencies

- None

### Technology Dependencies

- No new packages required

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Registry loaded, tasks created for current phase
2. **Edge Cases:**
   - Decimal phases (04.5, 05.5)
   - Conditional steps marked
   - Empty step list for phase
3. **Error Cases:**
   - Missing registry → HALT
   - Malformed JSON → HALT
   - Invalid step entries → skip

---

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **E2E Flow:** Phase file → read registry → create tasks → mark complete

---

## Acceptance Criteria Verification Checklist

### AC#1: Section Presence
- [ ] All 12 phase files contain section - **Phase:** 3 - **Evidence:** test_ac1

### AC#2: Phase Filtering
- [ ] Only current phase tasks created - **Phase:** 3 - **Evidence:** test_ac2

### AC#3: TaskUpdate Instruction
- [ ] Completion instruction included - **Phase:** 3 - **Evidence:** test_ac3

### AC#4: Error Handling
- [ ] Missing registry HALT - **Phase:** 3 - **Evidence:** test_ac4
- [ ] Malformed JSON HALT - **Phase:** 3 - **Evidence:** test_ac4

---

**Checklist Progress:** 0/5 items complete (0%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT -->

## Implementation Notes

*To be filled during /dev workflow*

## Definition of Done

### Implementation
- [ ] Progressive Task Disclosure section added to all 12 phase files
- [ ] Registry read instruction pointing to .claude/hooks/phase-steps-registry.json
- [ ] Phase filtering logic (current phase only)
- [ ] TaskCreate format with step_id in subject
- [ ] TaskUpdate completion instruction
- [ ] Conditional step marking
- [ ] Decimal phase support (04.5, 05.5)

### Quality
- [ ] All 4 acceptance criteria have passing tests
- [ ] Edge cases covered (decimal phases, conditional steps, empty lists)
- [ ] NFRs met (< 500ms, < 15% file size increase)
- [ ] Code coverage > 95%

### Testing
- [ ] Unit tests for section presence in all 12 files
- [ ] Unit tests for phase filtering
- [ ] Unit tests for error handling
- [ ] Integration test for end-to-end flow

### Documentation
- [ ] Progressive Task Disclosure pattern documented
- [ ] Registry reference path documented

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-03-02 12:00 | .claude/story-requirements-analyst | Created | Story created from EPIC-086 Feature 6 | STORY-530.story.md |

## Notes

**Design Decisions:**
- Section added after Entry Gate, before Mandatory Steps in each phase file (so tasks are created BEFORE work begins)
- Registry path hardcoded (.claude/hooks/phase-steps-registry.json) for consistency
- Graceful degradation: display step list as text if TaskCreate unavailable
- Section kept small (100-150 lines) to minimize phase file bloat

**References:**
- EPIC-086: Claude Hooks for Step-Level Phase Enforcement
- STORY-525: Phase Steps Registry (dependency)

---

Story Template Version: 2.9
Last Updated: 2026-03-02
