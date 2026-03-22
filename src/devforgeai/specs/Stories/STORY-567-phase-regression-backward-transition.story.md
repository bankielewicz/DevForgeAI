---
id: STORY-567
title: Add Phase Regression Backward Transition to Implementing-Stories Workflow
type: feature
epic: EPIC-087
sprint: null
status: Backlog
points: 3
depends_on: [STORY-569, STORY-566, STORY-568]
priority: Critical
advisory: false
source_gap: null
source_story: null
assigned_to: null
created: 2026-03-03
format_version: "2.9"
---

# Story: Add Phase Regression Backward Transition to Implementing-Stories Workflow

## Description

**As a** DevForgeAI orchestrator,
**I want** backward phase transition (Phase Regression) support in the implementing-stories workflow,
**so that** when test infrastructure defects are discovered in Phase 03+, the workflow can return to Phase 02 for test-automator regeneration without violating test-folder-protection or causing checksum mismatches.

**Source:** RCA-047 (REC-2) — Orchestrator Test Modification Phase Violation

**Context:** The implementing-stories workflow has a strictly forward-only phase state machine. When Phase 02 produces tests with infrastructure defects (e.g., bash arithmetic bugs), the orchestrator faces a false dilemma: fix tests directly (violation) or HALT permanently (deadlock). Adding Phase Regression allows the correct path: return to Phase 02, re-invoke test-automator, regenerate tests, update checksum snapshot, and resume forward.

## Acceptance Criteria

### AC#1: Phase Regression Section Exists in SKILL.md

```xml
<acceptance_criteria id="AC1" implements="REC-2">
  <given>The implementing-stories SKILL.md exists</given>
  <when>Reading the document</when>
  <then>A "## Phase Regression (Backward Transition)" section exists with backward transition table showing "03 (Green) → 02 (Red)" and "04 (Refactor) → 02 (Red)" rows</then>
  <verification>
    <source_files>
      <file hint="Workflow SKILL">src/claude/skills/implementing-stories/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-567/test_ac1_regression_section.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Phase Regression Protocol Defines 6-Step Process

```xml
<acceptance_criteria id="AC2" implements="REC-2">
  <given>The Phase Regression section exists in SKILL.md</given>
  <when>Reading the Phase Regression Protocol subsection</when>
  <then>6 steps documented: user approval → reset phase state → re-invoke test-automator → verify RED state → re-create checksum snapshot → resume forward</then>
  <verification>
    <source_files>
      <file hint="Workflow SKILL">src/claude/skills/implementing-stories/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-567/test_ac2_six_steps.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Only Test-Automator Authorized During Phase 02 Re-Entry

```xml
<acceptance_criteria id="AC3" implements="REC-2">
  <given>Phase Regression Protocol constraints are documented</given>
  <when>Reading the Constraints subsection</when>
  <then>Statement exists that "Only test-automator may write test files during Phase 02 re-entry"</then>
  <verification>
    <source_files>
      <file hint="Workflow SKILL">src/claude/skills/implementing-stories/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-567/test_ac3_authorized_agent.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Maximum 2 Regressions Per Story

```xml
<acceptance_criteria id="AC4" implements="REC-2">
  <given>Phase Regression constraints are documented</given>
  <when>Reading the Constraints subsection</when>
  <then>Statement exists that "Maximum 2 regressions per story" to prevent infinite loops</then>
  <verification>
    <source_files>
      <file hint="Workflow SKILL">src/claude/skills/implementing-stories/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-567/test_ac4_max_regressions.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Fallback When phase-reset CLI Not Implemented

```xml
<acceptance_criteria id="AC5" implements="REC-2">
  <given>The Phase Regression section exists</given>
  <when>Reading the Fallback subsection</when>
  <then>Manual phase-state.json editing steps documented for when phase-reset CLI (STORY-569) is not yet available</then>
  <verification>
    <source_files>
      <file hint="Workflow SKILL">src/claude/skills/implementing-stories/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-567/test_ac5_fallback.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

**Target File:** `src/claude/skills/implementing-stories/SKILL.md`
**Change Type:** Insert new section
**Insertion Point:** After the `## Phase Resumption` section (which ends with the resumption table), BEFORE `## Success Criteria`

### Exact Content to Insert

Insert the following markdown section after the Phase Resumption section:

````markdown
## Phase Regression (Backward Transition)

When a defect discovered in Phase 03+ requires returning to an earlier phase:

### Supported Backward Transitions

| From Phase | To Phase | Trigger | Authorized By |
|------------|----------|---------|---------------|
| 03 (Green) | 02 (Red) | Test infrastructure defect (not business logic) | test-folder-protection "Return to Phase 02" option |
| 04 (Refactor) | 02 (Red) | Test file needs structural changes | test-folder-protection "Return to Phase 02" option |

### Phase Regression Protocol

1. **User selects "Return to Phase 02"** from test-folder-protection AskUserQuestion
2. **Reset phase state:**
   ```bash
   devforgeai-validate phase-reset ${STORY_ID} --to=02
   ```
3. **Re-invoke test-automator** with context about the defect:
   ```
   Agent(
     subagent_type="test-automator",
     description="Regenerate tests for ${STORY_ID} — fix infrastructure defect",
     prompt="Regenerate test files. Previous tests had defect: {defect_description}. Fix: {fix_description}. Preserve all test assertions and business logic."
   )
   ```
4. **Verify RED state** (tests must still fail for expected business logic reasons)
5. **Re-create red-phase checksum snapshot** (overwrite per BR-005)
6. **Resume forward** from Phase 03

### Constraints

- Phase regression requires explicit user approval (via test-folder-protection AskUserQuestion)
- Only test-automator may write test files during Phase 02 re-entry
- Red-phase snapshot MUST be regenerated after test-automator produces new files
- Phase regression is logged in story Implementation Notes under `### Phase Regressions`
- Maximum 2 regressions per story (prevent infinite loops)

### Fallback When `phase-reset` CLI Not Yet Implemented

If STORY-569 (`phase-reset` CLI command) is not yet implemented, the orchestrator performs the reset manually:

1. Read `devforgeai/workflows/${STORY_ID}-phase-state.json`
2. Edit `current_phase` value from current (e.g., `"03"`) to target (e.g., `"02"`)
3. Add entry to `regressions` array (create array if absent):
   ```json
   {"from": "03", "to": "02", "timestamp": "2026-03-03T00:00:00Z", "reason": "test infrastructure defect"}
   ```
4. Save file
5. Continue with Phase Regression Protocol step 3 (re-invoke test-automator)
````

### Current State Context

The Phase Resumption section currently ends with this table (for reference to find insertion point):

```markdown
## Phase Resumption

When workflow stops incomplete:

1. Check phase state: `devforgeai-validate phase-status STORY-XXX`
2. Load phase file for current phase
3. Execute remaining phases from current to 10
4. Run Workflow Completion Validation

| Scenario | Action |
|----------|--------|
| Phase state exists | Resume from current phase |
| No prior execution evidence | Fresh start |
| Git conflicts | Fresh start after resolving |
```

### Structured Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "implementing-stories-skill"
      file_path: "src/claude/skills/implementing-stories/SKILL.md"
      required_keys:
        - key: "Phase Regression section"
          type: "object"
          example: "Backward transition table, protocol, constraints, fallback"
          required: true
          validation: "All subsections present"
          test_requirement: "Test: Verify Phase Regression section structure"

  business_rules:
    - id: "BR-001"
      rule: "Phase regression requires explicit user approval via test-folder-protection AskUserQuestion"
      trigger: "When backward transition is requested"
      validation: "Protocol step 1 references user approval"
      error_handling: "Cannot regress without user consent"
      test_requirement: "Test: Verify user approval is step 1"
      priority: "Critical"
    - id: "BR-002"
      rule: "Red-phase checksum snapshot must be regenerated after Phase 02 re-entry"
      trigger: "After test-automator produces new files"
      validation: "Protocol step 5 references snapshot regeneration"
      error_handling: "Missing snapshot causes QA TAMPERING detection"
      test_requirement: "Test: Verify snapshot regeneration in protocol"
      priority: "Critical"
    - id: "BR-003"
      rule: "Maximum 2 regressions per story to prevent infinite loops"
      trigger: "When regression is requested"
      validation: "Constraints section documents limit"
      error_handling: "Third regression attempt blocked"
      test_requirement: "Test: Verify max 2 regression limit documented"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "Backward transitions must preserve workflow state integrity"
      metric: "Phase-state.json reflects correct phase after regression"
      test_requirement: "Test: Verify state consistency after regression"
      priority: "Critical"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "phase-reset CLI"
    limitation: "Programmatic phase reset requires STORY-569 (phase-reset CLI command)"
    decision: "workaround:Manual phase-state.json editing documented as fallback"
    discovered_phase: "Architecture"
    impact: "Fallback is functional but less auditable than CLI approach"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:** N/A — documentation change

### Security

**Authentication:** None
**Authorization:** None

### Scalability

N/A — workflow rule documentation

### Reliability

**Error Handling:**
- Fallback process documented for missing CLI
- Maximum regression limit prevents infinite loops

### Observability

**Logging:**
- Phase regressions logged in story Implementation Notes under `### Phase Regressions`
- Regression entries in phase-state.json `regressions` array

---

## Dependencies

### Prerequisite Stories

- None (can be implemented independently)

### Advisory Dependencies

- **STORY-569** (phase-reset CLI command) — Phase Regression Protocol step 2 references `devforgeai-validate phase-reset`. AC#5 documents a manual fallback for when STORY-569 is not yet available. Implementing STORY-569 first is recommended but not required. (Source: TL-001, Audit F-002)
- **STORY-566** (test-folder-protection phase return option) — Phase Regression is triggered via the "Return to Phase 02" option added by STORY-566. Can be implemented independently since the SKILL.md section is self-contained.

### External Dependencies

- None

### Technology Dependencies

- None

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Phase Regression section exists with all subsections
2. **Edge Cases:**
   - Backward transition table has correct rows
   - 6-step protocol complete
   - Fallback documented
3. **Error Cases:**
   - Missing subsections detected

### Integration Tests

**Coverage Target:** 85%

**Test Scenarios:**
1. **Protocol Consistency:** Steps reference correct tools and subagents

---

## Acceptance Criteria Verification Checklist

### AC#1: Regression Section

- [ ] Section header present - **Phase:** 3 - **Evidence:** test_ac1
- [ ] Backward transition table present - **Phase:** 3 - **Evidence:** test_ac1

### AC#2: 6-Step Protocol

- [ ] All 6 steps documented - **Phase:** 3 - **Evidence:** test_ac2
- [ ] Steps in correct order - **Phase:** 3 - **Evidence:** test_ac2

### AC#3: Authorized Agent

- [ ] test-automator authorization documented - **Phase:** 3 - **Evidence:** test_ac3

### AC#4: Max Regressions

- [ ] "Maximum 2 regressions" text present - **Phase:** 3 - **Evidence:** test_ac4

### AC#5: Fallback

- [ ] Manual editing steps documented - **Phase:** 3 - **Evidence:** test_ac5

---

**Checklist Progress:** 0/7 items complete (0%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
See: .claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Implementation Notes

*To be filled during development*

## Definition of Done

### Implementation
- [ ] SKILL.md contains Phase Regression section
- [ ] Backward transition table with Phase 03→02 and Phase 04→02 rows
- [ ] 6-step Phase Regression Protocol documented
- [ ] Only test-automator authorized for Phase 02 re-entry
- [ ] Maximum 2 regressions per story constraint documented
- [ ] Fallback for manual phase-state.json editing documented

### Quality
- [ ] All 5 acceptance criteria have passing tests
- [ ] No broken references to other documents
- [ ] Protocol steps reference correct tools

### Testing
- [ ] Unit tests for regression section (test_ac1)
- [ ] Unit tests for protocol steps (test_ac2)
- [ ] Unit tests for authorization (test_ac3)
- [ ] Unit tests for max limit (test_ac4)
- [ ] Unit tests for fallback (test_ac5)

### Documentation
- [ ] SKILL.md updated with Phase Regression section
- [ ] Story Implementation Notes completed

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
| 2026-03-03 | .claude/story-requirements-analyst | Created | Story created from RCA-047 REC-2 | STORY-567.story.md |

## Notes

**Source:** RCA-047 — Orchestrator Test Modification Phase Violation
**Source Recommendation:** REC-2 — Add backward phase transition (Phase Regression) to implementing-stories workflow

**Design Decisions:**
- Supports Phase 03→02 and Phase 04→02 transitions only (no arbitrary backward jumps)
- Maximum 2 regressions prevents infinite loops
- Fallback ensures functionality before CLI is built
- test-integrity-snapshot.md BR-005 already supports Phase 02 re-entry (snapshot overwrite)

**References:**
- RCA-047: devforgeai/RCA/RCA-047-orchestrator-test-modification-phase-violation.md
- SKILL.md: src/claude/skills/implementing-stories/SKILL.md
- test-integrity-snapshot.md BR-005: supports re-running Phase 02

---

Story Template Version: 2.9
Last Updated: 2026-03-03
