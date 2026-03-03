---
id: STORY-306
title: Subagent Enforcement in Phase State Completion
type: feature
epic: EPIC-031
sprint: Backlog
status: QA Approved
priority: Critical
points: 3
depends_on: []
created: 2026-01-23
updated: 2026-01-23
---

# STORY-306: Subagent Enforcement in Phase State Completion

## Description

Implement programmatic enforcement to prevent phases from being marked complete without invoking required subagents. This addresses the root cause identified in RCA-027 where `complete_phase()` allows marking phases complete without validating that required subagents were invoked because `subagents_required` is never populated (always empty array).

This is a recurring systemic issue documented across 7+ incidents (RCA-019, RCA-022, RCA-024, RCA-027) occurring approximately once per week. Documentation-only enforcement has repeatedly failed; technical enforcement is required.

---

## Provenance

<provenance>
  <origin document="RCA-027" section="Root Cause Chain">
    <quote>"complete_phase() has NO validation that required subagents were invoked; subagents_required array is ALWAYS EMPTY"</quote>
    <line_reference>lines 110-124</line_reference>
    <quantified_impact>7+ incidents across 70 days (~1/week), framework integrity compromised</quantified_impact>
  </origin>
  <origin document="EPIC-031" section="Problem Statement">
    <quote>"Claude executes skill content as OPTIONAL GUIDANCE rather than MANDATORY PROTOCOL"</quote>
    <line_reference>lines 17-27</line_reference>
    <quantified_impact>Quality regression - Stories pass QA without proper validation</quantified_impact>
  </origin>
  <decision rationale="Programmatic enforcement over documentation enforcement">
    <selected>Add validation to complete_phase() checking required ⊆ invoked</selected>
    <rejected>Documentation-only enforcement (proven ineffective in 7+ RCAs)</rejected>
    <trade_off>Slightly slower phase completion (< 10ms) for guaranteed integrity</trade_off>
  </decision>
</provenance>

---

## User Story

**As a** DevForgeAI framework developer,
**I want** phase completion to be blocked when required subagents have not been invoked,
**so that** workflow integrity is maintained and phase skipping (documented in RCA-019, RCA-022, RCA-024, RCA-027) is prevented through programmatic enforcement rather than relying on documentation alone.

---

## Acceptance Criteria

<acceptance_criteria>
  <ac id="AC1" title="PHASE_REQUIRED_SUBAGENTS constant defines subagent requirements">
    <given>The phase_state.py module is loaded</given>
    <when>I inspect the PHASE_REQUIRED_SUBAGENTS constant</when>
    <then>It contains subagent requirements for phases 01-10, 4.5, and 5.5 matching the Required Subagents Per Phase table in SKILL.md (lines 167-181)</then>
    <verification>
      <step>Read phase_state.py and locate PHASE_REQUIRED_SUBAGENTS constant</step>
      <step>Verify keys include all 12 valid phases: 01, 02, 03, 04, 4.5, 05, 5.5, 06, 07, 08, 09, 10</step>
      <step>Verify Phase 09 entry contains 'framework-analyst'</step>
    </verification>
    <source_files>
      <file path="src/claude/scripts/devforgeai_cli/phase_state.py" hint="PHASE_REQUIRED_SUBAGENTS constant definition"/>
    </source_files>
  </ac>

  <ac id="AC2" title="subagents_required populated on phase state creation">
    <given>A new phase state is being created via `_create_initial_state()`</given>
    <when>The state dictionary is initialized</when>
    <then>Each phase entry in `phases` has `subagents_required` populated from PHASE_REQUIRED_SUBAGENTS constant instead of empty array</then>
    <verification>
      <step>Create new phase state for test story</step>
      <step>Read resulting state file</step>
      <step>Verify phases.02.subagents_required contains 'test-automator'</step>
      <step>Verify phases.09.subagents_required contains 'framework-analyst'</step>
    </verification>
    <source_files>
      <file path="src/claude/scripts/devforgeai_cli/phase_state.py" hint="_create_initial_state method"/>
    </source_files>
  </ac>

  <ac id="AC3" title="complete_phase() blocks when required subagents not invoked">
    <given>A phase has `subagents_required = ["test-automator"]`</given>
    <when>I call `complete_phase(story_id, phase="02", checkpoint_passed=True)` with `subagents_invoked = []`</when>
    <then>A `SubagentEnforcementError` is raised with message identifying missing subagent(s)</then>
    <verification>
      <step>Create phase state with populated subagents_required</step>
      <step>Attempt complete_phase without invoking required subagents</step>
      <step>Verify SubagentEnforcementError raised</step>
      <step>Verify error message contains 'test-automator'</step>
    </verification>
    <source_files>
      <file path="src/claude/scripts/devforgeai_cli/phase_state.py" hint="complete_phase method validation logic"/>
    </source_files>
  </ac>

  <ac id="AC4" title="complete_phase() succeeds when all required subagents invoked">
    <given>Phase 02 requires `["test-automator"]` and `subagents_invoked = ["test-automator"]`</given>
    <when>I call `complete_phase(story_id, phase="02", checkpoint_passed=True)`</when>
    <then>The phase status is set to "completed" and current_phase advances to "03"</then>
    <verification>
      <step>Create phase state and record test-automator via record_subagent</step>
      <step>Call complete_phase with checkpoint_passed=True</step>
      <step>Verify phase status is "completed"</step>
      <step>Verify current_phase advanced to "03"</step>
    </verification>
    <source_files>
      <file path="src/claude/scripts/devforgeai_cli/phase_state.py" hint="complete_phase method success path"/>
    </source_files>
  </ac>

  <ac id="AC5" title="Escape hatch allows completion without subagent validation">
    <given>A phase has required subagents not yet invoked</given>
    <when>I call `complete_phase(story_id, phase, checkpoint_passed=False)`</when>
    <then>The phase completes WITHOUT validating subagent invocation (escape hatch for edge cases)</then>
    <verification>
      <step>Create phase state with required subagents</step>
      <step>Call complete_phase with checkpoint_passed=False (no subagents invoked)</step>
      <step>Verify phase completes without error</step>
      <step>Verify checkpoint_passed is False in state file</step>
    </verification>
    <source_files>
      <file path="src/claude/scripts/devforgeai_cli/phase_state.py" hint="complete_phase escape hatch logic"/>
    </source_files>
  </ac>

  <ac id="AC6" title="OR logic handled for Phase 03 subagents">
    <given>Phase 03 requires "backend-architect OR frontend-developer"</given>
    <when>Either `["backend-architect"]` OR `["frontend-developer"]` is in `subagents_invoked`</when>
    <then>The subagent requirement is satisfied (either one fulfills the requirement)</then>
    <verification>
      <step>Create phase state where Phase 03 subagents_required uses tuple for OR logic</step>
      <step>Record only backend-architect (not frontend-developer)</step>
      <step>Verify Phase 03 completes successfully</step>
      <step>Repeat with only frontend-developer - verify success</step>
    </verification>
    <source_files>
      <file path="src/claude/scripts/devforgeai_cli/phase_state.py" hint="OR logic validation in complete_phase"/>
    </source_files>
  </ac>

  <ac id="AC7" title="SKILL.md Phase 09 documentation corrected">
    <given>SKILL.md Required Subagents Per Phase table (line 179)</given>
    <when>I read the Phase 09 entry</when>
    <then>It shows `framework-analyst` as required with BLOCKING enforcement (not "none - hook invocation")</then>
    <verification>
      <step>Read SKILL.md line 179</step>
      <step>Verify Phase 09 row contains 'framework-analyst'</step>
      <step>Verify enforcement column shows 'BLOCKING'</step>
    </verification>
    <source_files>
      <file path="src/claude/skills/devforgeai-development/SKILL.md" hint="Required Subagents Per Phase table, line 179"/>
    </source_files>
  </ac>

  <ac id="AC8" title="Backward compatibility for legacy state files">
    <given>A state file exists from before this enhancement (with empty subagents_required arrays)</given>
    <when>The state file is loaded via _read_state() or _ensure_phases_exist()</when>
    <then>The subagents_required arrays are populated from PHASE_REQUIRED_SUBAGENTS constant</then>
    <verification>
      <step>Create a mock legacy state file with empty subagents_required</step>
      <step>Load it via PhaseState.read()</step>
      <step>Verify subagents_required is now populated</step>
    </verification>
    <source_files>
      <file path="src/claude/scripts/devforgeai_cli/phase_state.py" hint="_ensure_phases_exist or _read_state migration logic"/>
    </source_files>
  </ac>
</acceptance_criteria>

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "PHASE_REQUIRED_SUBAGENTS"
      file_path: "src/claude/scripts/devforgeai_cli/phase_state.py"
      requirements:
        - id: "COMP-001"
          description: "Define PHASE_REQUIRED_SUBAGENTS constant mapping phases to required subagents"
          testable: true
          test_requirement: "Test: Constant contains entries for all 12 valid phases"
          priority: "Critical"
        - id: "COMP-002"
          description: "Phase 03 uses tuple for OR logic: ('backend-architect', 'frontend-developer')"
          testable: true
          test_requirement: "Test: Phase 03 entry is tuple, not list"
          priority: "High"
        - id: "COMP-003"
          description: "Phase 09 includes 'framework-analyst' to match phase-09-feedback.md"
          testable: true
          test_requirement: "Test: PHASE_REQUIRED_SUBAGENTS['09'] == ['framework-analyst']"
          priority: "Critical"

    - type: "Service"
      name: "PhaseState._create_initial_state enhancement"
      file_path: "src/claude/scripts/devforgeai_cli/phase_state.py"
      requirements:
        - id: "COMP-004"
          description: "Populate subagents_required from PHASE_REQUIRED_SUBAGENTS constant"
          testable: true
          test_requirement: "Test: New state has non-empty subagents_required for phases with requirements"
          priority: "Critical"

    - type: "Service"
      name: "PhaseState.complete_phase enhancement"
      file_path: "src/claude/scripts/devforgeai_cli/phase_state.py"
      requirements:
        - id: "COMP-005"
          description: "Add subagent enforcement validation before phase completion"
          testable: true
          test_requirement: "Test: Raises SubagentEnforcementError when required subagents missing and checkpoint_passed=True"
          priority: "Critical"
        - id: "COMP-006"
          description: "Skip validation when checkpoint_passed=False (escape hatch)"
          testable: true
          test_requirement: "Test: Phase completes when checkpoint_passed=False even without subagents"
          priority: "High"
        - id: "COMP-007"
          description: "Support OR logic for Phase 03 subagent groups"
          testable: true
          test_requirement: "Test: Phase 03 completes with either backend-architect OR frontend-developer"
          priority: "High"

    - type: "DataModel"
      name: "SubagentEnforcementError"
      file_path: "src/claude/scripts/devforgeai_cli/phase_state.py"
      requirements:
        - id: "COMP-008"
          description: "New exception class for subagent enforcement failures"
          testable: true
          test_requirement: "Test: Exception contains story_id, phase, and missing_subagents attributes"
          priority: "High"

    - type: "Service"
      name: "PhaseState._ensure_phases_exist enhancement"
      file_path: "src/claude/scripts/devforgeai_cli/phase_state.py"
      requirements:
        - id: "COMP-009"
          description: "Migrate legacy state files by populating empty subagents_required"
          testable: true
          test_requirement: "Test: Legacy state file gets subagents_required populated on read"
          priority: "High"

    - type: "Documentation"
      name: "SKILL.md Phase 09 fix"
      file_path: "src/claude/skills/devforgeai-development/SKILL.md"
      requirements:
        - id: "COMP-010"
          description: "Update Required Subagents table line 179 for Phase 09"
          testable: true
          test_requirement: "Test: Grep confirms 'framework-analyst' in Phase 09 row"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Phases with required subagents cannot complete (checkpoint_passed=True) until all required subagents are invoked"
      test_requirement: "Test: complete_phase raises error for phase with missing subagents"
    - id: "BR-002"
      rule: "OR logic subagent groups are satisfied if ANY one subagent in the group is invoked"
      test_requirement: "Test: Phase 03 completes with backend-architect alone"
    - id: "BR-003"
      rule: "Phases with empty subagents_required can always complete (07, 08)"
      test_requirement: "Test: Phase 07 completes without validation errors"
    - id: "BR-004"
      rule: "Escape hatch (checkpoint_passed=False) bypasses subagent validation"
      test_requirement: "Test: Phase with missing subagents completes when checkpoint_passed=False"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Phase completion validation including subagent check"
      metric: "< 10ms per validation"
      test_requirement: "Test: Benchmark complete_phase with subagent validation"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Zero false positives - valid completions never blocked"
      metric: "0% false positive rate"
      test_requirement: "Test: 100 valid completions all succeed"
    - id: "NFR-003"
      category: "Reliability"
      requirement: "Zero false negatives - missing subagents always caught"
      metric: "100% detection rate for missing required subagents"
      test_requirement: "Test: All 12 phases with missing subagents raise error"
```

---

## Edge Cases

1. **Existing state files (backward compatibility):** When loading state files created before this enhancement (with empty `subagents_required` arrays), the system must populate `subagents_required` from PHASE_REQUIRED_SUBAGENTS during `_read_state()` to enable enforcement without requiring state file regeneration.

2. **OR logic subagent groups (Phase 03):** Phase 03 accepts `backend-architect` OR `frontend-developer` (not both required). Implementation must use tuple/list grouping in PHASE_REQUIRED_SUBAGENTS to indicate "any one of these satisfies requirement."

3. **Phases with no required subagents (07, 08):** Phases 07 and 08 have no required subagents (file operations, git operations). The enforcement logic must allow phases with empty `subagents_required` to complete without validation errors.

4. **Partial invocation:** If Phase 04 requires `["refactoring-specialist", "code-reviewer"]` but only `["refactoring-specialist"]` was invoked, the error message must list all missing subagents (not just the first one found).

5. **Invalid subagent names in record_subagent():** If `record_subagent()` is called with a subagent name that doesn't exist in `.claude/agents/`, consider whether to validate or allow (current behavior allows any string).

---

## Data Validation Rules

1. **Subagent names:** Each subagent in PHASE_REQUIRED_SUBAGENTS should correspond to a file in `.claude/agents/{subagent-name}.md`.

2. **Phase IDs:** PHASE_REQUIRED_SUBAGENTS keys must be valid phase IDs matching `VALID_PHASES` constant (01-10, 4.5, 5.5).

3. **OR group format:** Subagent groups using OR logic use tuple format: `('backend-architect', 'frontend-developer')`. List format indicates "all required."

---

## Non-Functional Requirements

### Performance
- Phase completion validation including subagent check: < 10ms (measured from `complete_phase()` call to return or exception)
- PHASE_REQUIRED_SUBAGENTS lookup: O(1) dictionary access
- Module import time increase: < 5ms (constant is defined at module level)

### Reliability
- Zero false positives: Valid completions with all required subagents invoked must never be blocked
- Zero false negatives: Completions with missing required subagents must always be blocked (when checkpoint_passed=True)
- Error messages must specify exactly which subagent(s) are missing, not generic "validation failed"

### Maintainability
- PHASE_REQUIRED_SUBAGENTS constant defined in single location (top of phase_state.py near VALID_PHASES)
- Adding/removing subagent requirements requires only constant modification (no logic changes)
- Unit tests cover all 12 phases (including 4.5 and 5.5) for both positive and negative cases

### Backward Compatibility
- Existing state files (without populated `subagents_required`) must work after upgrade
- Migration logic in `_read_state()` or `_ensure_phases_exist()` handles legacy files
- No manual intervention required for existing workflows

### Auditability
- When enforcement blocks completion, log at WARNING level: "Phase {N} completion blocked: Missing required subagents: {list}"
- When escape hatch used (checkpoint_passed=False), log at INFO level: "Phase {N} completed via escape hatch (checkpoint_passed=False)"

---

## Definition of Done

### Implementation
- [x] PHASE_REQUIRED_SUBAGENTS constant added to phase_state.py
- [x] SubagentEnforcementError exception class created
- [x] `_create_initial_state()` populates subagents_required from constant
- [x] `complete_phase()` validates required subagents before completion
- [x] OR logic implemented for Phase 03 subagent groups
- [x] Escape hatch (checkpoint_passed=False) bypasses validation
- [x] `_ensure_phases_exist()` migrates legacy state files

### Documentation
- [x] SKILL.md Phase 09 entry updated (framework-analyst, BLOCKING)
- [ ] RCA-027 marked RESOLVED with reference to this story

### Testing
- [x] Unit tests for PHASE_REQUIRED_SUBAGENTS constant validation
- [x] Unit tests for subagents_required population on state creation
- [x] Unit tests for complete_phase blocking on missing subagents
- [x] Unit tests for complete_phase success with all subagents
- [x] Unit tests for escape hatch (checkpoint_passed=False)
- [x] Unit tests for OR logic (Phase 03)
- [x] Unit tests for backward compatibility (legacy state files)
- [x] Integration test: Full /dev workflow with enforcement active

### Quality
- [x] All tests passing (25/25 for STORY-306)
- [x] No Critical/High anti-pattern violations
- [x] Performance benchmark confirms < 10ms validation time

---

## AC Verification Checklist

### AC1: PHASE_REQUIRED_SUBAGENTS constant
- [x] Constant exists in phase_state.py
- [x] Contains entries for all 12 phases (01-10, 4.5, 5.5)
- [x] Phase 09 entry is ['framework-analyst']
- [x] Phase 03 entry uses tuple for OR logic

### AC2: subagents_required populated
- [x] New state files have non-empty subagents_required
- [x] phases.02.subagents_required == ['test-automator']
- [x] phases.09.subagents_required == ['framework-analyst']

### AC3: Blocking when missing subagents
- [x] SubagentEnforcementError raised for Phase 02 without test-automator
- [x] Error message identifies missing subagent

### AC4: Success when subagents invoked
- [x] Phase completes when required subagents recorded
- [x] current_phase advances correctly

### AC5: Escape hatch works
- [x] checkpoint_passed=False allows completion without subagents
- [x] checkpoint_passed stored as False in state file

### AC6: OR logic for Phase 03
- [x] Completes with backend-architect only
- [x] Completes with frontend-developer only
- [x] Blocks with neither

### AC7: SKILL.md documentation fix
- [x] Line 179 shows framework-analyst
- [x] Enforcement column shows BLOCKING

### AC8: Backward compatibility
- [x] Legacy state files load successfully
- [x] subagents_required populated on read

---

## Implementation Notes

- [x] **VERIFIED**: All changes exist in src/ tree per source-tree.md constitution:
  - `src/claude/scripts/devforgeai_cli/phase_state.py` - PHASE_REQUIRED_SUBAGENTS, SubagentEnforcementError, enforcement logic
  - `src/claude/skills/devforgeai-development/SKILL.md` - Phase 09 documentation updated
  - `.claude/scripts/devforgeai_cli/tests/test_subagent_enforcement.py` - 25 unit tests passing

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-23 | claude/story-requirements-analyst | Story Creation | Initial story created from RCA-027 research | STORY-306-subagent-enforcement-phase-completion.story.md |
| 2026-01-25 | claude/dev | Verification | Verified implementation in src/ tree, fixed SKILL.md Phase 09 doc, added 25 unit tests | phase_state.py, SKILL.md, test_subagent_enforcement.py |
| 2026-01-26 | claude/qa-result-interpreter | QA Deep | PASSED: 25/25 tests, 8/8 ACs verified, 0 violations, security score 92/100 | STORY-306-qa-report.md |