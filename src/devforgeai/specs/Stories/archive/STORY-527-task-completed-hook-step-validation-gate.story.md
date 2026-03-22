---
id: STORY-527
title: TaskCompleted Hook — Step Validation Gate
type: feature
epic: EPIC-086
sprint: Sprint-22
status: QA Approved
points: 5
depends_on: ["STORY-525", "STORY-526"]
priority: High
advisory: false
assigned_to: DevForgeAI AI Agent
created: 2026-03-02
format_version: "2.9"
---

# Story: TaskCompleted Hook — Step Validation Gate

## Description

**As a** DevForgeAI framework engineer,
**I want** a shell script hook triggered on TaskCompleted events that validates step-level phase enforcement and blocks task completion if a required subagent was not invoked,
**so that** Claude cannot mark steps "done" without actually invoking the subagents specified in the phase-steps-registry.json.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-013" section="hook-stack-design">
    <quote>"Claude tries to complete step → TaskCompleted hook checks phase-state → blocks if subagent missing"</quote>
    <line_reference>Epic EPIC-086, line 228</line_reference>
    <quantified_impact>Prevents Claude from self-reporting step completion without doing the work</quantified_impact>
  </origin>
</provenance>
```

## Acceptance Criteria

### AC#1: Hook Parses TaskCompleted JSON and Extracts Step ID

```xml
<acceptance_criteria id="AC1" implements="HOOK-001">
  <given>TaskCompleted hook at .claude/hooks/validate-step-completion.sh receives JSON on stdin</given>
  <when>Task subject matches pattern "Step NN.M: [description]" (e.g., "Step 02.2: test-automator invoked")</when>
  <then>Hook extracts step_id in dotted format (e.g., "02.2", "4.5.3"). If subject doesn't match pattern "^Step [0-9]", exits 0 (no-op for non-phase tasks).</then>
  <verification>
    <source_files>
      <file hint="Hook script">.claude/hooks/validate-step-completion.sh</file>
    </source_files>
    <test_file>tests/STORY-527/test_ac1_parse_step_id.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Hook Loads Registry and Retrieves Required Subagent

```xml
<acceptance_criteria id="AC2" implements="HOOK-002">
  <given>phase-steps-registry.json exists at .claude/hooks/ with step definitions</given>
  <when>Hook looks up step_id in registry using jq</when>
  <then>Retrieves subagent field (string for single subagent, JSON array for OR-logic e.g., ["backend-architect", "frontend-developer"], or null). Missing registry → exit 0. Unknown step → exit 0. Malformed JSON → exit 0.</then>
  <verification>
    <source_files>
      <file hint="Registry">.claude/hooks/phase-steps-registry.json</file>
      <file hint="Hook">.claude/hooks/validate-step-completion.sh</file>
    </source_files>
    <test_file>tests/STORY-527/test_ac2_load_registry.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Conditional Steps Always Pass

```xml
<acceptance_criteria id="AC3" implements="HOOK-003">
  <given>Registry step has conditional: true</given>
  <when>Hook evaluates conditional field</when>
  <then>Exits 0 immediately without checking subagent invocations. Conditional steps never block.</then>
  <verification>
    <source_files>
      <file hint="Hook">.claude/hooks/validate-step-completion.sh</file>
    </source_files>
    <test_file>tests/STORY-527/test_ac3_conditional.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: OR-Logic Support for Required Subagents

```xml
<acceptance_criteria id="AC4" implements="HOOK-004">
  <given>Step has subagent ["backend-architect", "frontend-developer"] (JSON array for OR-logic)</given>
  <when>Hook detects array type via jq and checks if ANY element exists in subagents_invoked for current phase</when>
  <then>Passes (exit 0) if ANY option in subagents_invoked. Blocks (exit 2) if NONE match.</then>
  <verification>
    <source_files>
      <file hint="Hook">.claude/hooks/validate-step-completion.sh</file>
    </source_files>
    <test_file>tests/STORY-527/test_ac4_or_logic.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Blocks with Exit Code 2 When Required Subagent Missing

```xml
<acceptance_criteria id="AC5" implements="HOOK-005">
  <given>Step requires a subagent not present in subagents_invoked for current phase</given>
  <when>Hook finds no match between required and invoked subagents</when>
  <then>Exits code 2 (blocking). Logs to stderr: step_id, required subagents, invoked subagents. Task completion blocked.</then>
  <verification>
    <source_files>
      <file hint="Hook">.claude/hooks/validate-step-completion.sh</file>
    </source_files>
    <test_file>tests/STORY-527/test_ac5_block.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Hook Configuration in settings.json

```xml
<acceptance_criteria id="AC6" implements="HOOK-006">
  <given>.claude/settings.json exists with existing hooks</given>
  <when>STORY-527 implementation complete</when>
  <then>"TaskCompleted" event added to hooks with command referencing validate-step-completion.sh, timeout 15. Existing hooks unchanged. JSON valid.</then>
  <verification>
    <source_files>
      <file hint="Settings">.claude/settings.json</file>
    </source_files>
    <test_file>tests/STORY-527/test_ac6_settings.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### Source Files Guidance

Hook scripts at .claude/hooks/, registry at .claude/hooks/phase-steps-registry.json, state at devforgeai/workflows/.

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "TaskCompletedHook"
      file_path: ".claude/hooks/validate-step-completion.sh"
      requirements:
        - id: "HOOK-001"
          description: "Parse TaskCompleted JSON and extract step_id from task subject"
          testable: true
          test_requirement: "Test: Subject 'Step 03.4: context-validator invoked' extracts '03.4'"
          priority: "Critical"
        - id: "HOOK-002"
          description: "Load registry and retrieve required_subagent for step"
          testable: true
          test_requirement: "Test: Registry lookup returns correct required_subagent"
          priority: "Critical"
        - id: "HOOK-003"
          description: "Conditional steps (conditional: true) pass immediately"
          testable: true
          test_requirement: "Test: Conditional step exits 0 regardless of subagent state"
          priority: "High"
        - id: "HOOK-004"
          description: "OR-logic: pass if ANY element in JSON array subagent option invoked"
          testable: true
          test_requirement: "Test: ['a','b'] passes when only 'b' invoked; fails when neither"
          priority: "Critical"
        - id: "HOOK-005"
          description: "Exit 2 (block) when required subagent missing from subagents_invoked"
          testable: true
          test_requirement: "Test: Missing required subagent exits 2; present exits 0"
          priority: "Critical"
        - id: "HOOK-006"
          description: "Register in settings.json TaskCompleted event"
          testable: true
          test_requirement: "Test: settings.json contains TaskCompleted hook entry"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Exit 0 on all error conditions (missing registry, malformed JSON, unknown step) — only exit 2 on proven violations"
      trigger: "When hook encounters error processing step"
      validation: "Error paths exit 0; only missing-subagent exits 2"
      error_handling: "Log warning to stderr, exit 0"
      test_requirement: "Test: Missing registry exits 0; malformed JSON exits 0; unknown step exits 0"
      priority: "Critical"
    - id: "BR-002"
      rule: "QA workflow state files (*-qa-*) are never checked"
      trigger: "When scanning for phase-state files"
      validation: "Pattern excludes *-qa-* files"
      error_handling: "Skip silently"
      test_requirement: "Test: QA phase-state files ignored during hook execution"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Hook completes in < 500ms"
      metric: "< 500ms end-to-end"
      test_requirement: "Test: Time hook execution; assert < 500ms"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Performance

- Hook execution: < 500ms end-to-end
- Registry load: < 100ms for 72-step registry

---

### Security

- No command injection: uses jq for JSON parsing, variables quoted
- No path traversal: file paths hardcoded

---

### Scalability

- Tested with 200+ step registry
- Linear O(n) step lookup via jq

---

### Reliability

- Graceful degradation: exit 0 on all errors except proven violations
- Read-only (no state mutations in hook)
- Exit code semantics: 0=pass, 2=block

---

### Observability

- All decisions logged to stderr with timestamp
- Log format: [ISO8601] [TASK-HOOK] {decision} - {reason}

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-525:** Phase Steps Registry + Step-Level Tracking
  - **Why:** Provides registry JSON and step-level infrastructure
  - **Status:** Backlog

- [ ] **STORY-526:** SubagentStop Hook — Auto-Track Invocations
  - **Why:** Populates subagents_invoked that this hook validates against
  - **Status:** Backlog

### External Dependencies

- [x] **jq:** JSON processor — Available

### Technology Dependencies

- No new packages required

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Step with required subagent invoked → exit 0
2. **Edge Cases:**
   - Conditional step → exit 0
   - OR-logic with partial match → exit 0
   - Missing registry → exit 0
   - Unknown step → exit 0
3. **Error Cases:**
   - Required subagent not invoked → exit 2
   - OR-logic with no matches → exit 2

---

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **E2E Validation Flow:** SubagentStop records → TaskCompleted validates → pass/block
2. **Settings Integration:** Hook registered correctly

---

## Acceptance Criteria Verification Checklist

### AC#1: Parse Step ID
- [x] Extracts step_id from task subject - **Phase:** 2 - **Evidence:** test_ac1_parse_step_id.sh (5 tests written, RED)
- [x] Non-step tasks exit 0 - **Phase:** 2 - **Evidence:** test_ac1_parse_step_id.sh (non-step no-op test)

### AC#2: Registry Lookup
- [x] Retrieves required_subagent - **Phase:** 2 - **Evidence:** test_ac2_load_registry.sh (5 tests written, RED)

### AC#3: Conditional Steps
- [x] Conditional steps pass immediately - **Phase:** 2 - **Evidence:** test_ac3_conditional.sh (3 tests written, RED)

### AC#4: OR-Logic
- [x] OR-logic JSON array evaluated correctly - **Phase:** 2 - **Evidence:** test_ac4_or_logic.sh (5 tests written, RED)

### AC#5: Blocking
- [x] Exit 2 when subagent missing - **Phase:** 2 - **Evidence:** test_ac5_block.sh (6 tests written, RED)

### AC#6: Configuration
- [x] settings.json updated - **Phase:** 2 - **Evidence:** test_ac6_settings.sh (5 tests written, RED)

---

**Checklist Progress:** 7/7 items complete (100%) - Tests written, awaiting GREEN

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT -->

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-03-03

- [x] validate-step-completion.sh created at .claude/hooks/ - Completed: 165-line bash hook with jq JSON parsing, step ID extraction, registry lookup, conditional bypass, OR-logic, and exit code 2 blocking
- [x] Step ID extraction from task subject working - Completed: Regex extracts dotted format (02.2, 4.5.3) from "Step NN.M:" pattern
- [x] Registry lookup with jq implemented - Completed: Loads phase-steps-registry.json, looks up step by id in .steps[] array
- [x] Conditional step pass-through implemented - Completed: Steps with conditional:true exit 0 immediately
- [x] OR-logic for subagent JSON arrays implemented (jq type detection) - Completed: jq type check differentiates string vs array, ANY match passes
- [x] Exit code 2 blocking on missing subagent - Completed: Logs step_id, required, and invoked to stderr
- [x] settings.json updated with TaskCompleted hook - Completed: Added with timeout 15, existing hooks preserved
- [x] All 6 acceptance criteria have passing tests - Completed: 29 unit + 9 integration = 38 tests passing
- [x] Edge cases covered (missing registry, unknown step, conditional, OR-logic) - Completed: All error paths exit 0 per BR-001
- [x] NFRs met (< 500ms execution) - Completed: ~73ms measured execution time
- [x] Code coverage > 95% - Completed: All code paths tested
- [x] Unit tests for step ID parsing - Completed: test_ac1_parse_step_id.sh (5 tests)
- [x] Unit tests for registry lookup - Completed: test_ac2_load_registry.sh (5 tests)
- [x] Unit tests for OR-logic - Completed: test_ac4_or_logic.sh (5 tests)
- [x] Unit tests for blocking behavior - Completed: test_ac5_block.sh (6 tests)
- [x] Integration test for end-to-end flow - Completed: test_integration_e2e.sh (9 tests)
- [x] Hook script documented - Completed: Header comments with input/output/exit code semantics
- [x] OR-logic format documented - Completed: JSON array format documented in story notes
- [x] Exit code semantics documented - Completed: 0=pass/no-op, 2=block

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Phase 02 (Red) | ✅ Complete | 29 failing tests across 6 AC test files |
| Phase 03 (Green) | ✅ Complete | validate-step-completion.sh + settings.json update, all 29 tests pass |
| Phase 04 (Refactor) | ✅ Complete | Extracted find_project_root() function, code review approved |
| Phase 05 (Integration) | ✅ Complete | 9 integration tests added, all 38 tests pass |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| .claude/hooks/validate-step-completion.sh | Created | 165 |
| .claude/settings.json | Modified | +12 (TaskCompleted hook) |
| tests/STORY-527/test_ac1_parse_step_id.sh | Created | 105 |
| tests/STORY-527/test_ac2_load_registry.sh | Created | 94 |
| tests/STORY-527/test_ac3_conditional.sh | Created | 90 |
| tests/STORY-527/test_ac4_or_logic.sh | Created | 115 |
| tests/STORY-527/test_ac5_block.sh | Created | 113 |
| tests/STORY-527/test_ac6_settings.sh | Created | 76 |
| tests/STORY-527/test_integration_e2e.sh | Created | 280 |
| tests/STORY-527/run_all_tests.sh | Created | 34 |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-03-02 12:00 | .claude/story-requirements-analyst | Created | Story created from EPIC-086 Feature 3 | STORY-527.story.md |
| 2026-03-03 | .claude/qa-result-interpreter | QA Deep | PASSED: Coverage >95%, 0 blocking violations, 38/38 tests pass | - |

## Notes

**Design Decisions:**
- Exit 0 on errors, exit 2 only on proven violations (conservative approach)
- OR-logic uses JSON array format (parsed with `jq -e 'type == "array"'`) — cleaner than pipe separators
- QA workflow files excluded to prevent cross-workflow interference

**References:**
- EPIC-086: Claude Hooks for Step-Level Phase Enforcement
- STORY-525: Phase Steps Registry (dependency)
- STORY-526: SubagentStop Hook (dependency — populates subagents_invoked)

---

Story Template Version: 2.9
Last Updated: 2026-03-02
