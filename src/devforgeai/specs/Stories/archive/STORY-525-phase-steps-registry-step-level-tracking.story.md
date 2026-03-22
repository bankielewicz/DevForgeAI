---
id: STORY-525
title: Phase Steps Registry + Step-Level Tracking
type: feature
epic: EPIC-086
sprint: Sprint-22
status: QA Approved
points: 5
depends_on: []
priority: High
advisory: false
assigned_to: DevForgeAI AI Agent
created: 2026-03-02
format_version: "2.9"
---

# Story: Phase Steps Registry + Step-Level Tracking

## Description

**As a** DevForgeAI framework engineer,
**I want** a 72-step registry JSON file derived from Pre-Exit Checklists in all 12 phase files, along with `record_step()` and `validate_phase_steps()` methods in phase_state.py and a `phase-record-step` CLI command,
**so that** external hook-based enforcement can verify phase compliance at the step level using a single source of truth that is parseable by both Python and Bash (jq).

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-013" section="problem-statement">
    <quote>"STORY-522 phase-state.json showed subagents_invoked: [] and steps_completed: [] for ALL 12 phases despite completed status — proving self-reporting is unreliable"</quote>
    <line_reference>Epic EPIC-086, lines 23-25</line_reference>
    <quantified_impact>0% compliance rate on subagent invocation tracking across all completed phases</quantified_impact>
  </origin>
  <decision rationale="registry-as-source-of-truth">
    <selected>JSON registry derived from phase files, parseable by both Python and Bash/jq</selected>
    <rejected alternative="hardcoded-lists">Existing DEV_PHASES and PHASE_REQUIRED_SUBAGENTS dicts in phase_state.py are incomplete and not accessible to hook scripts</rejected>
    <trade_off>Registry file must be kept in sync with phase file changes</trade_off>
  </decision>
</provenance>
```

## Acceptance Criteria

### AC#1: Registry JSON Created from 12 Phase Pre-Exit Checklists

```xml
<acceptance_criteria id="AC1" implements="REG-001">
  <given>The 12 implementing-stories phase files exist at src/claude/skills/implementing-stories/phases/ and each contains a Pre-Exit Checklist section with checkable items</given>
  <when>The registry JSON file is manually authored from the Pre-Exit Checklists across all 12 phase files (phase-01 through phase-10 plus phase-04.5 and phase-05.5), using the complete registry provided in the plan file (.claude/plans/smooth-tumbling-beacon.md Section 4)</when>
  <then>A file exists at .claude/hooks/phase-steps-registry.json as a phase-keyed JSON dict. Each phase key (e.g., "01", "02", "4.5") maps to an object with name, entry_gate, exit_gate, and steps array. Each step has: id (dotted format NN.M, e.g., "01.1", "4.5.3"), check (description string), subagent (string, JSON array for OR-logic, or null), and conditional (boolean, default false). JSON is valid per python -m json.tool and jq. Total: 72 steps across 12 phases.</then>
  <verification>
    <source_files>
      <file hint="Registry file">.claude/hooks/phase-steps-registry.json</file>
      <file hint="Phase files (source data)">src/claude/skills/implementing-stories/phases/</file>
    </source_files>
    <test_file>tests/STORY-525/test_ac1_registry_generation.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: record_step() Persists Step Completion to Phase State File

```xml
<acceptance_criteria id="AC2" implements="SVC-001">
  <given>A valid story phase state file exists for STORY-525 and phase 02 is in progress</given>
  <when>PhaseState.record_step("STORY-525", "02", "02.2") is called</when>
  <then>The phase state JSON file is updated atomically via _atomic_write(), containing steps_completed array under phase 02 with the step ID "02.2". Calling record_step() again with the same step ID is idempotent (no duplicate entries). No other phase data is mutated.</then>
  <verification>
    <source_files>
      <file hint="PhaseState class extension">src/claude/scripts/devforgeai_cli/phase_state.py</file>
    </source_files>
    <test_file>tests/STORY-525/test_ac2_record_step.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: validate_phase_steps() Returns Pass/Fail Based on Required Steps

```xml
<acceptance_criteria id="AC3" implements="SVC-002">
  <given>A phase state file for STORY-525 exists with steps_completed for phase 02 and the registry contains required (non-conditional) steps for phase 02</given>
  <when>PhaseState.validate_phase_steps("STORY-525", "02") is called</when>
  <then>Returns {"status": "PASS", "missing_steps": []} when all required steps present. Returns {"status": "FAIL", "missing_steps": [...]} with actual missing step IDs (dotted format, e.g., "02.3") when steps absent. Conditional steps (conditional: true in registry) are excluded from required set. Returns FAIL with all required steps when steps_completed array is absent or empty.</then>
  <verification>
    <source_files>
      <file hint="PhaseState validation method">src/claude/scripts/devforgeai_cli/phase_state.py</file>
    </source_files>
    <test_file>tests/STORY-525/test_ac3_validate_phase_steps.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: phase-record-step CLI Command Records Step via Command Line

```xml
<acceptance_criteria id="AC4" implements="CLI-001">
  <given>The devforgeai-validate CLI is installed and a phase state file exists for STORY-525</given>
  <when>devforgeai-validate phase-record-step STORY-525 --phase=02 --step=02.2 is executed</when>
  <then>Command exits with code 0 and stdout contains confirmation message. Phase state file updated with step. Command is idempotent. Invalid story ID exits with code 1. Unknown step ID exits with code 1 with informative stderr message.</then>
  <verification>
    <source_files>
      <file hint="CLI command implementation">src/claude/scripts/devforgeai_cli/commands/phase_commands.py</file>
    </source_files>
    <test_file>tests/STORY-525/test_ac4_cli_command.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Registry Is Authoritative Source for validate_phase_steps()

```xml
<acceptance_criteria id="AC5" implements="SVC-003">
  <given>The registry JSON file exists at .claude/hooks/phase-steps-registry.json</given>
  <when>validate_phase_steps() is called for any phase</when>
  <then>The method loads required steps exclusively from the registry JSON (not from hardcoded lists). If registry absent, raises FileNotFoundError. If registry malformed, raises json.JSONDecodeError.</then>
  <verification>
    <source_files>
      <file hint="Registry loading logic">src/claude/scripts/devforgeai_cli/phase_state.py</file>
      <file hint="Registry file">src/claude/hooks/phase-steps-registry.json</file>
    </source_files>
    <test_file>tests/STORY-525/test_ac5_registry_authoritative.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### Source Files Guidance

The `<source_files>` element provides hints to the ac-compliance-verifier about where implementation code is located.

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "PhaseState (extended)"
      file_path: "src/claude/scripts/devforgeai_cli/phase_state.py"
      interface: "PhaseState"
      lifecycle: "Singleton"
      dependencies:
        - "json"
        - "pathlib.Path"
        - "_atomic_write() (existing)"
      requirements:
        - id: "SVC-001"
          description: "record_step(story_id, phase, step_id) appends step to steps_completed list idempotently using _atomic_write()"
          testable: true
          test_requirement: "Test: Call record_step twice with same args; assert steps_completed contains step exactly once"
          priority: "Critical"
        - id: "SVC-002"
          description: "validate_phase_steps(story_id, phase) returns dict with status and missing_steps keys based on registry"
          testable: true
          test_requirement: "Test: With 2 of 4 required steps present, assert return is {status: FAIL, missing_steps: [2 missing IDs]}"
          priority: "Critical"
        - id: "SVC-003"
          description: "validate_phase_steps loads required steps from registry JSON, not hardcoded lists"
          testable: true
          test_requirement: "Test: Mock registry with custom steps; verify validate uses registry not DEV_PHASES"
          priority: "High"

    - type: "Configuration"
      name: "phase-steps-registry.json"
      file_path: ".claude/hooks/phase-steps-registry.json"
      description: "Phase-keyed JSON dict. Manually authored from Pre-Exit Checklists (not auto-generated). Full 72-step registry is provided in plan file (.claude/plans/smooth-tumbling-beacon.md Section 4)."
      required_keys:
        - key: "<phase_id>"
          type: "object"
          required: true
          description: "Phase keys: '01' through '10' plus '4.5' and '5.5' (12 total)"
          test_requirement: "Test: Registry has exactly 12 phase keys"
        - key: "<phase_id>.name"
          type: "string"
          required: true
          test_requirement: "Test: All phases have non-empty name"
        - key: "<phase_id>.entry_gate"
          type: "string"
          required: true
          test_requirement: "Test: All phases have entry_gate CLI command"
        - key: "<phase_id>.exit_gate"
          type: "string"
          required: true
          test_requirement: "Test: All phases have exit_gate CLI command"
        - key: "<phase_id>.steps[].id"
          type: "string"
          required: true
          validation: "Dotted format: NN.M (e.g., '01.1', '4.5.3')"
          test_requirement: "Test: All step IDs match regex ^[\\d]+\\.?[\\d]*\\.\\d+$"
        - key: "<phase_id>.steps[].check"
          type: "string"
          required: true
          test_requirement: "Test: No empty check descriptions"
        - key: "<phase_id>.steps[].subagent"
          type: "string|array|null"
          required: true
          description: "String for single subagent, JSON array for OR-logic (e.g., ['backend-architect', 'frontend-developer']), null if no subagent required"
          test_requirement: "Test: Value is null, a string, or an array of strings"
        - key: "<phase_id>.steps[].conditional"
          type: "bool"
          required: false
          description: "Defaults to false. True for steps that may be N/A (e.g., deferral steps when no deferrals exist)"
          test_requirement: "Test: Conditional steps correctly marked"

    - type: "API"
      name: "phase-record-step"
      endpoint: "CLI: devforgeai-validate phase-record-step"
      method: "CLI"
      authentication:
        required: false
      request:
        content_type: "CLI positional arg + named flags"
        schema:
          story_id:
            type: "string"
            required: true
            position: "positional arg 1"
            validation: "^STORY-\\d+$"
          phase:
            type: "string"
            required: true
            flag: "--phase"
            validation: "Valid phase ID (01-10, 4.5, 5.5)"
          step_id:
            type: "string"
            required: true
            flag: "--step"
            validation: "Dotted format: NN.M (e.g., '02.2', '4.5.3')"
      response:
        success:
          status_code: 0
          schema:
            message: "Recorded step {step_id} for {story_id} phase {phase}"
        errors:
          - status_code: 1
            condition: "Invalid story ID format"
            schema:
              error: "Invalid story ID: {value}"
          - status_code: 1
            condition: "Unknown step ID not in registry"
            schema:
              error: "Unknown step ID: {value}"
      requirements:
        - id: "CLI-001"
          description: "Accept positional args story_id, phase, step_id; validate all three before file write"
          testable: true
          test_requirement: "Test: Valid args exit 0 and update state; invalid args exit 1 with error message"
          priority: "Critical"

  business_rules:
    - id: "BR-001"
      rule: "Registry is the single source of truth for phase step requirements — hardcoded lists in phase_state.py (DEV_PHASES, PHASE_REQUIRED_SUBAGENTS) are superseded"
      trigger: "When validate_phase_steps() is called"
      validation: "Method loads from registry JSON file, not from in-memory dicts"
      error_handling: "FileNotFoundError if registry absent"
      test_requirement: "Test: validate_phase_steps uses registry JSON, not DEV_PHASES dict"
      priority: "Critical"
    - id: "BR-002"
      rule: "record_step() is idempotent — recording the same step twice has no effect"
      trigger: "When record_step() called with duplicate step_id"
      validation: "steps_completed list contains no duplicates"
      error_handling: "Silent success (no error, no duplicate)"
      test_requirement: "Test: Call record_step twice with same args; list has step exactly once"
      priority: "High"
    - id: "BR-003"
      rule: "Conditional steps (conditional: true in registry) do not cause validation failure when missing"
      trigger: "When validate_phase_steps() checks completed steps against registry"
      validation: "Only steps with conditional: false are considered required"
      error_handling: "Conditional steps excluded from missing_steps list"
      test_requirement: "Test: Phase with 3 required + 2 conditional steps; missing conditional steps still returns PASS"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Correctness"
      requirement: "Registry contains exactly 72 steps across 12 phases matching Pre-Exit Checklists"
      metric: "Step count matches phase file checklists"
      test_requirement: "Test: Registry has 12 phase keys with total 72 step entries"
      priority: "High"
    - id: "NFR-002"
      category: "Performance"
      requirement: "record_step() completes in less than 50ms per call"
      metric: "< 50ms excluding disk I/O variance"
      test_requirement: "Test: Benchmark record_step with timer; assert < 50ms"
      priority: "Medium"
    - id: "NFR-003"
      category: "Reliability"
      requirement: "Atomic writes prevent partial state corruption"
      metric: "Zero partial writes on crash (temp file + rename pattern)"
      test_requirement: "Test: Verify record_step uses _atomic_write; no direct file.write calls"
      priority: "Critical"
    - id: "NFR-004"
      category: "Correctness"
      requirement: "Registry JSON validates with both python -m json.tool and jq"
      metric: "Zero parse errors from either tool"
      test_requirement: "Test: Validate registry with json.loads() and jq ."
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Registry generator"
    limitation: "Step count may differ from exactly 72 if phase files are modified after epic creation"
    decision: "workaround:Registry stores actual parsed count in metadata field; validation uses actual count not hardcoded 72"
    discovered_phase: "Architecture"
    impact: "Low — registry is regenerated from source files"
  - id: TL-002
    component: "Phase IDs"
    limitation: "Fractional phase IDs (04.5, 05.5) require dotted notation in step_id format"
    decision: "workaround:Step IDs use PHASE-04.5-STEP-MM format; regex validation updated to accept dots"
    discovered_phase: "Architecture"
    impact: "Low — format documented and validated"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- `record_step()`: < 50ms per call
- `validate_phase_steps()`: < 100ms per call
- CLI command: < 500ms end-to-end

**Throughput:**
- N/A (single-user CLI tool)

---

### Security

**Authentication:** None required (local CLI tool)

**Data Protection:**
- Phase state files written with 0o600 permissions (owner read/write only)
- Registry file written with 0o644 permissions
- Step IDs validated against regex before file write
- Story IDs validated against `^STORY-\d+$` before file write

---

### Scalability

**Registry Schema:**
- Supports up to 500 step entries without schema changes
- `completed_steps` converted to set for O(n) lookup
- Registry file size under 100 KB for 500 steps

---

### Reliability

**Error Handling:**
- `record_step()` uses `_atomic_write()` for crash safety
- `validate_phase_steps()` is read-only with no side effects
- Registry generation is deterministic on unchanged inputs
- Missing registry file raises clear `FileNotFoundError`

---

### Observability

**Logging:**
- `record_step()` logs at DEBUG level: step recorded
- `validate_phase_steps()` logs at INFO level: pass/fail result
- Registry generation logs at INFO: step count per phase
- CLI command outputs human-readable confirmation to stdout

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-522:** Pre-Exit Checklists in all 12 phase files
  - **Why:** Source data for the 72-step registry
  - **Status:** Complete

- [x] **STORY-524:** Phase state tracking infrastructure
  - **Why:** Provides PhaseState, record_subagent(), _atomic_write() methods to extend
  - **Status:** Complete

### External Dependencies

- [x] **jq:** JSON processor for Bash hook scripts
  - **Owner:** System dependency
  - **Status:** Available

### Technology Dependencies

- No new packages required. Uses existing Python stdlib (json, pathlib, argparse) and jq.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**
1. **Happy Path:** Registry JSON valid, contains 12 phases and 72 steps. record_step() and validate_phase_steps() work correctly.
2. **Edge Cases:**
   - Fractional phase IDs (4.5, 5.5) in registry and step IDs
   - OR-logic subagent arrays in registry
   - Conditional steps excluded from validation
   - Idempotent record_step calls
   - Missing phase state file during validate
3. **Error Cases:**
   - Invalid story ID format
   - Unknown step ID not in registry
   - Missing registry file (FileNotFoundError)
   - Malformed registry JSON (json.JSONDecodeError)

---

### Integration Tests

**Coverage Target:** 85%+ for application layer

**Test Scenarios:**
1. **End-to-End CLI Flow:** phase-record-step → state file update → validate_phase_steps
2. **Registry + Validation Integration:** Generate registry → record steps → validate passes

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

### AC#1: Registry JSON Created from 12 Phase Pre-Exit Checklists

- [ ] Registry JSON file exists at .claude/hooks/phase-steps-registry.json - **Phase:** 3 - **Evidence:** test_ac1_registry_generation.py
- [ ] Contains 12 phase keys with 72 total step entries - **Phase:** 3 - **Evidence:** test_ac1_registry_generation.py
- [ ] Each step has required fields (id in NN.M format, check, subagent as string/array/null) - **Phase:** 3 - **Evidence:** test_ac1_registry_generation.py
- [ ] JSON valid per python json.loads() and jq - **Phase:** 3 - **Evidence:** test_ac1_registry_generation.py

### AC#2: record_step() Persists Step Completion

- [ ] Atomic write via _atomic_write() - **Phase:** 3 - **Evidence:** test_ac2_record_step.py
- [ ] steps_completed updated correctly - **Phase:** 3 - **Evidence:** test_ac2_record_step.py
- [ ] Idempotent behavior verified - **Phase:** 3 - **Evidence:** test_ac2_record_step.py

### AC#3: validate_phase_steps() Returns Pass/Fail

- [ ] PASS when all required steps present - **Phase:** 3 - **Evidence:** test_ac3_validate_phase_steps.py
- [ ] FAIL with missing step IDs when steps absent - **Phase:** 3 - **Evidence:** test_ac3_validate_phase_steps.py
- [ ] Conditional steps excluded from required set - **Phase:** 3 - **Evidence:** test_ac3_validate_phase_steps.py

### AC#4: phase-record-step CLI Command

- [ ] Exits 0 on valid input - **Phase:** 3 - **Evidence:** test_ac4_cli_command.py
- [ ] Updates phase state file - **Phase:** 3 - **Evidence:** test_ac4_cli_command.py
- [ ] Exits 1 on invalid input with error message - **Phase:** 3 - **Evidence:** test_ac4_cli_command.py

### AC#5: Registry Is Authoritative Source

- [ ] Loads from registry JSON not hardcoded lists - **Phase:** 3 - **Evidence:** test_ac5_registry_authoritative.py
- [ ] FileNotFoundError when registry absent - **Phase:** 3 - **Evidence:** test_ac5_registry_authoritative.py

---

**Checklist Progress:** 0/15 items complete (0%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
When filling in the Implementation Notes section during /dev workflow:
1. DoD items MUST be placed DIRECTLY under "## Implementation Notes" header
2. NO ### subsection headers (like "### Definition of Done Status") before DoD items
3. The extract_section() validator stops at the first ### header it encounters
4. If DoD items are under a ### subsection, the validator cannot find them → commit blocked
5. The ### Additional Notes subsection is OK because it comes AFTER DoD items
See: .claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-03-02

- [x] phase-steps-registry.json created at .claude/hooks/phase-steps-registry.json (manually authored from plan Section 4) - Completed: 72-step registry with 12 phases derived from Pre-Exit Checklists in all phase files
- [x] record_step() method added to PhaseState class in src/claude/scripts/devforgeai_cli/phase_state.py - Completed: Idempotent step recording with _atomic_write(), input validation, FileNotFoundError for missing state
- [x] validate_phase_steps() method added to PhaseState class - Completed: Loads from registry JSON, filters conditional steps, returns PASS/FAIL dict with missing_steps
- [x] phase-record-step CLI command added to src/claude/scripts/devforgeai_cli/commands/phase_commands.py - Completed: Validates step_id against registry, exits 0 on success, 1 on error with informative messages
- [x] Registry contains entries for all 12 phases - Completed: Phases 01-10 plus 4.5 and 5.5, 72 total steps
- [x] All 5 acceptance criteria have passing tests - Completed: 47 unit tests + 12 integration tests = 59 total, all passing
- [x] Edge cases covered (conditional steps, fractional phases, idempotency, missing files) - Completed: All covered in test suite
- [x] Input validation enforced (story ID regex, step ID regex, phase ID validation) - Completed: Uses existing _validate_story_id, _validate_phase_id, plus registry-based step validation
- [x] NFRs met (performance, reliability, determinism) - Completed: Atomic writes, idempotent operations, registry as single source of truth
- [x] Code coverage > 95% for phase_state.py new methods - Completed: 59 tests covering all paths
- [x] Unit tests for registry JSON validation (schema, step count, phase keys) - Completed: 15 tests in test_ac1_registry_generation.py
- [x] Unit tests for record_step() - Completed: 11 tests in test_ac2_record_step.py
- [x] Unit tests for validate_phase_steps() - Completed: 10 tests in test_ac3_validate_phase_steps.py
- [x] Unit tests for CLI command - Completed: 6 tests in test_ac4_cli_command.py
- [x] Integration tests for end-to-end flow - Completed: 12 tests in test_integration.py
- [x] Registry JSON schema documented in story file - Completed: Technical specification section documents full schema
- [x] CLI command usage documented - Completed: API section in technical spec documents CLI interface
- [x] Step ID format documented - Completed: Dotted format NN.M documented in story notes

## Definition of Done

### Implementation
- [x] phase-steps-registry.json created at .claude/hooks/phase-steps-registry.json (manually authored from plan Section 4)
- [x] record_step() method added to PhaseState class in src/claude/scripts/devforgeai_cli/phase_state.py
- [x] validate_phase_steps() method added to PhaseState class
- [x] phase-record-step CLI command added to src/claude/scripts/devforgeai_cli/commands/phase_commands.py
- [x] Registry contains entries for all 12 phases

### Quality
- [x] All 5 acceptance criteria have passing tests
- [x] Edge cases covered (conditional steps, fractional phases, idempotency, missing files)
- [x] Input validation enforced (story ID regex, step ID regex, phase ID validation)
- [x] NFRs met (performance, reliability, determinism)
- [x] Code coverage > 95% for phase_state.py new methods

### Testing
- [x] Unit tests for registry JSON validation (schema, step count, phase keys)
- [x] Unit tests for record_step()
- [x] Unit tests for validate_phase_steps()
- [x] Unit tests for CLI command
- [x] Integration tests for end-to-end flow

### Documentation
- [x] Registry JSON schema documented in story file
- [x] CLI command usage documented
- [x] Step ID format documented

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Red | ✅ Complete | 47 failing tests across 5 test files |
| Green | ✅ Complete | All 47 tests passing - registry + 3 methods + CLI |
| Refactor | ✅ Complete | Import cleanup, registry validation hardened |
| Integration | ✅ Complete | 12 integration tests added, 59/59 passing |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/hooks/phase-steps-registry.json | Created | 159 |
| .claude/hooks/phase-steps-registry.json | Created | 159 |
| src/claude/scripts/devforgeai_cli/phase_state.py | Modified | +120 |
| src/claude/scripts/devforgeai_cli/commands/phase_commands.py | Modified | +60 |
| tests/STORY-525/conftest.py | Created | 74 |
| tests/STORY-525/test_ac1_registry_generation.py | Created | 166 |
| tests/STORY-525/test_ac2_record_step.py | Created | 126 |
| tests/STORY-525/test_ac3_validate_phase_steps.py | Created | 171 |
| tests/STORY-525/test_ac4_cli_command.py | Created | 108 |
| tests/STORY-525/test_ac5_registry_authoritative.py | Created | 115 |
| tests/STORY-525/test_integration.py | Created | ~150 |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-03-02 12:00 | .claude/story-requirements-analyst | Created | Story created from EPIC-086 Feature 1 | STORY-525.story.md |
| 2026-03-02 | .claude/qa-result-interpreter | QA Deep | PASS WITH WARNINGS: Coverage >95%, 4 violations (0 blocking) | - |

## Notes

**Design Decisions:**
- Registry JSON format chosen over YAML for direct jq compatibility in Bash hooks
- Step ID format NN.M (dotted notation, e.g., "01.1", "4.5.3") matches phase numbering and is simpler than verbose PHASE-NN-STEP-MM
- Registry is manually authored (not auto-generated) from plan Section 4 — the complete 72-step registry is provided inline in the plan file
- OR-logic for subagents uses JSON array (e.g., ["backend-architect", "frontend-developer"]) — parsed natively by jq, cleaner than pipe separators
- validate_phase_steps returns dict (not raises exception) to support hook exit-code patterns
- Field name is steps_completed (matching existing phase-state.json schema), not completed_steps

**Open Questions:**
- None

**Related ADRs:**
- None (uses existing technology stack)

**References:**
- EPIC-086: Claude Hooks for Step-Level Phase Enforcement
- BRAINSTORM-013: Hook-based enforcement discovery
- STORY-522: Pre-Exit Checklists (dependency — complete)
- STORY-524: Phase state tracking infrastructure (dependency — complete)

---

Story Template Version: 2.9
Last Updated: 2026-03-02
