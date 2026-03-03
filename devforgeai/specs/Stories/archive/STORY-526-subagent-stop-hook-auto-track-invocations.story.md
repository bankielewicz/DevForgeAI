---
id: STORY-526
title: SubagentStop Hook — Auto-Track Invocations
type: feature
epic: EPIC-086
sprint: Sprint-22
status: QA Approved
points: 3
depends_on: ["STORY-525"]
priority: High
advisory: false
assigned_to: DevForgeAI AI Agent
created: 2026-03-02
format_version: "2.9"
---

# Story: SubagentStop Hook — Auto-Track Invocations

## Description

**As a** framework maintainer,
**I want** externally-verified subagent invocation tracking via a SubagentStop event hook,
**so that** phase-state.json `subagents_invoked` is trustworthy and not self-reported by Claude.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-013" section="hook-stack-design">
    <quote>"SubagentStop hook records it → phase-state reflects reality"</quote>
    <line_reference>Epic EPIC-086, line 227</line_reference>
    <quantified_impact>subagents_invoked from 0% populated to 100% for all completed phases</quantified_impact>
  </origin>
</provenance>
```

## Acceptance Criteria

### AC#1: Hook Script Receives and Parses SubagentStop JSON Input

```xml
<acceptance_criteria id="AC1" implements="HOOK-001">
  <given>The SubagentStop hook is registered in .claude/settings.json under the "SubagentStop" event</given>
  <when>Claude stops a subagent invocation and the SubagentStop hook is triggered</when>
  <then>The hook script at .claude/hooks/track-subagent-invocation.sh receives JSON on stdin containing agent_type field. Script parses JSON using jq. Malformed JSON does not cause crash (exits 0).</then>
  <verification>
    <source_files>
      <file hint="Hook script">.claude/hooks/track-subagent-invocation.sh</file>
    </source_files>
    <test_file>tests/STORY-526/test_ac1_json_parsing.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Filters Built-in Agents and Records DevForgeAI Subagents

```xml
<acceptance_criteria id="AC2" implements="HOOK-002">
  <given>Hook receives JSON with agent_type for Explore, Plan, Bash, general-purpose, test-automator, or code-reviewer</given>
  <when>Hook processes the agent_type value</when>
  <then>Built-in agents (Explore, Plan, Bash, general-purpose) are filtered out and NOT recorded. DevForgeAI subagents (test-automator, code-reviewer, etc.) ARE recorded via devforgeai-validate phase-record {STORY_ID} --subagent={AGENT_TYPE} --project-root={CWD}.</then>
  <verification>
    <source_files>
      <file hint="Hook script">.claude/hooks/track-subagent-invocation.sh</file>
    </source_files>
    <test_file>tests/STORY-526/test_ac2_filter_builtin.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Calls devforgeai-validate phase-record With Correct Arguments

```xml
<acceptance_criteria id="AC3" implements="HOOK-003">
  <given>A non-built-in subagent invocation is detected. Hook has access to current story ID and phase from phase-state.json</given>
  <when>Hook constructs and executes devforgeai-validate phase-record</when>
  <then>CLI receives story_id as positional arg and --subagent flag. Story ID and current phase extracted from active phase-state.json filename and current_phase field. Phase-state.json updated atomically with subagent in subagents_invoked array. If story_id or phase cannot be determined, hook exits 0 (non-blocking, logs warning).</then>
  <verification>
    <source_files>
      <file hint="Hook script">.claude/hooks/track-subagent-invocation.sh</file>
      <file hint="CLI command">src/claude/scripts/devforgeai_cli/commands/phase_commands.py</file>
    </source_files>
    <test_file>tests/STORY-526/test_ac3_phase_record.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Hook Always Exits Code 0 (Non-Blocking)

```xml
<acceptance_criteria id="AC4" implements="HOOK-004">
  <given>Hook runs in any scenario (success, error, missing files, malformed JSON)</given>
  <when>Hook completes execution</when>
  <then>Hook always exits code 0. Never blocks subagent invocation. Errors logged to stderr but do not propagate.</then>
  <verification>
    <source_files>
      <file hint="Hook script">.claude/hooks/track-subagent-invocation.sh</file>
    </source_files>
    <test_file>tests/STORY-526/test_ac4_exit_code.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Hook Configuration Added to .claude/settings.json

```xml
<acceptance_criteria id="AC5" implements="HOOK-005">
  <given>.claude/settings.json exists with existing hook configurations</given>
  <when>STORY-526 implementation is complete</when>
  <then>"SubagentStop" event key added to hooks section without modifying existing hooks. Timeout set to 10 seconds. JSON validates with jq.</then>
  <verification>
    <source_files>
      <file hint="Settings">.claude/settings.json</file>
    </source_files>
    <test_file>tests/STORY-526/test_ac5_settings.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### Source Files Guidance

Source files for this story are hook scripts (.claude/hooks/) and settings configuration.

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "SubagentStopHook"
      file_path: ".claude/hooks/track-subagent-invocation.sh"
      requirements:
        - id: "HOOK-001"
          description: "Parse SubagentStop event JSON from stdin using jq"
          testable: true
          test_requirement: "Test: Hook receives valid JSON; jq parsing succeeds"
          priority: "Critical"
        - id: "HOOK-002"
          description: "Filter built-in agents (Explore, Plan, Bash) from recording"
          testable: true
          test_requirement: "Test: Explore/Plan/Bash agent_type not recorded; DevForgeAI agents recorded"
          priority: "High"
        - id: "HOOK-003"
          description: "Call devforgeai-validate phase-record with story_id, phase, agent_type"
          testable: true
          test_requirement: "Test: Valid subagent triggers phase-record; phase-state.json updated"
          priority: "Critical"
        - id: "HOOK-004"
          description: "Exit code 0 under all conditions (non-blocking)"
          testable: true
          test_requirement: "Test: Hook exits 0 on success, missing files, jq errors"
          priority: "Critical"
        - id: "HOOK-005"
          description: "Register in .claude/settings.json SubagentStop event"
          testable: true
          test_requirement: "Test: settings.json contains SubagentStop hook entry"
          priority: "High"

    - type: "Configuration"
      name: "settings.json (SubagentStop)"
      file_path: ".claude/settings.json"
      required_keys:
        - key: "hooks.SubagentStop"
          type: "array"
          required: true
          test_requirement: "Test: SubagentStop key exists with hook entry array"

  business_rules:
    - id: "BR-001"
      rule: "Built-in agents (Explore, Plan, Bash) are never recorded in subagents_invoked"
      trigger: "When SubagentStop event fires for any agent"
      validation: "Check agent_type against filter list"
      error_handling: "Silently skip, exit 0"
      test_requirement: "Test: Built-in agents filtered; subagents_invoked empty after built-in stops"
      priority: "High"
    - id: "BR-002"
      rule: "Hook is always non-blocking (exit 0) — recording is observational only"
      trigger: "On any error or exception in hook"
      validation: "All code paths exit 0"
      error_handling: "Log to stderr, exit 0"
      test_requirement: "Test: All error paths exit 0"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Hook execution completes in < 500ms"
      metric: "< 500ms end-to-end including JSON parsing and CLI call"
      test_requirement: "Test: Time hook execution; assert < 500ms"
      priority: "Medium"
    - id: "NFR-002"
      category: "Security"
      requirement: "Subagent_type validated against safe regex before CLI call"
      metric: "Regex ^[a-zA-Z0-9_-]+$ applied to all inputs"
      test_requirement: "Test: Invalid agent_type with injection chars rejected"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Hook execution: < 500ms end-to-end

---

### Security

**Input Validation:**
- Subagent_type validated against `^[a-zA-Z0-9_-]+$` before passing to CLI
- Variables quoted in shell to prevent injection

---

### Scalability

- Supports unlimited sequential SubagentStop events
- Each story has isolated phase-state.json (no contention)

---

### Reliability

- Exit code 0 always (non-blocking)
- Graceful degradation on missing files or CLI errors
- Uses existing _atomic_write() via phase-record CLI

---

### Observability

**Logging:**
- DEBUG: Parsed agent_type
- INFO: Subagent recorded
- WARN: Built-in agent filtered, phase-state not found

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-525:** Phase Steps Registry + Step-Level Tracking
  - **Why:** Provides phase-record CLI command and phase-state infrastructure
  - **Status:** Backlog

### External Dependencies

- [x] **jq:** JSON processor
  - **Owner:** System dependency
  - **Status:** Available

### Technology Dependencies

- No new packages required

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Non-built-in subagent recorded via phase-record CLI
2. **Edge Cases:**
   - Built-in agent filtering (Explore, Plan, Bash)
   - Missing phase-state.json
   - Malformed JSON input
   - CLI not available (command not found)
3. **Error Cases:**
   - Invalid agent_type with special characters
   - Empty stdin

---

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **E2E Hook Flow:** SubagentStop event → hook → phase-record → state file update
2. **Settings Integration:** Hook registered correctly in settings.json

---

## Acceptance Criteria Verification Checklist

### AC#1: JSON Parsing

- [x] Hook parses valid JSON from stdin - **Phase:** 2 - **Evidence:** test_ac1_json_parsing.sh
- [x] Malformed JSON handled gracefully - **Phase:** 3 - **Evidence:** test_ac1_json_parsing.sh

### AC#2: Built-in Filtering

- [x] Explore/Plan/Bash filtered - **Phase:** 3 - **Evidence:** test_ac2_filter_builtin.sh
- [x] DevForgeAI agents recorded - **Phase:** 3 - **Evidence:** test_ac2_filter_builtin.sh

### AC#3: CLI Integration

- [x] phase-record called with correct args - **Phase:** 3 - **Evidence:** test_ac3_phase_record.sh

### AC#4: Exit Code

- [x] Exit 0 on all paths - **Phase:** 3 - **Evidence:** test_ac4_exit_code.sh

### AC#5: Configuration

- [x] settings.json updated correctly - **Phase:** 3 - **Evidence:** test_ac5_settings.sh

---

**Checklist Progress:** 7/7 items complete (100%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
1. DoD items MUST be placed DIRECTLY under "## Implementation Notes" header
2. NO ### subsection headers before DoD items
See: .claude/skills/implementing-stories/references/dod-update-workflow.md
-->

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-03-02

- [x] track-subagent-invocation.sh created at .claude/hooks/ - Completed: Created bash hook script at src/claude/hooks/track-subagent-invocation.sh with JSON parsing, built-in agent filtering, and phase-record CLI integration
- [x] Built-in agent filter list implemented (Explore, Plan, Bash, general-purpose) - Completed: Hardcoded filter list with loop-based matching, exits 0 for built-in agents
- [x] devforgeai-validate phase-record integration working - Completed: Extracts story_id from phase-state.json filename, current_phase from JSON content, calls CLI with correct args
- [x] settings.json updated with SubagentStop hook entry - Completed: Added SubagentStop key to hooks section with timeout 10, preserving existing hooks
- [x] Hook is executable (chmod +x) - Completed: chmod +x applied to hook script
- [x] All 5 acceptance criteria have passing tests - Completed: 34 unit tests across 5 test files, all passing
- [x] Edge cases covered (missing files, malformed JSON, CLI unavailable) - Completed: 8 error scenarios tested in AC4 test file
- [x] Input validation enforced (agent_type regex) - Completed: Regex ^[a-zA-Z0-9_-]+$ applied before CLI call, injection attempts rejected
- [x] Code coverage > 95% for hook script - Completed: All code paths exercised by unit and integration tests
- [x] Unit tests for JSON parsing - Completed: tests/STORY-526/test_ac1_json_parsing.sh (7 tests)
- [x] Unit tests for built-in agent filtering - Completed: tests/STORY-526/test_ac2_filter_builtin.sh (7 tests)
- [x] Unit tests for exit code behavior - Completed: tests/STORY-526/test_ac4_exit_code.sh (8 tests)
- [x] Integration test for end-to-end flow - Completed: tests/STORY-526/test_integration_e2e.sh (23 tests)
- [x] Hook script documented with usage comments - Completed: Header comments explain input/output/side effects
- [x] settings.json hook configuration documented - Completed: Configuration follows existing hook patterns with timeout

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Phase 02 (Red) | Complete | 34 failing tests written across 5 AC test files |
| Phase 03 (Green) | Complete | Hook script created, settings.json updated, all tests pass |
| Phase 04 (Refactor) | Complete | Code review applied: improved jq fallback, added comments |
| Phase 05 (Integration) | Complete | 23 integration tests: E2E flow, settings, security |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/hooks/track-subagent-invocation.sh | Created | 116 |
| src/claude/settings.json | Modified | +11 (SubagentStop hook entry) |
| tests/STORY-526/test_ac1_json_parsing.sh | Created | 72 |
| tests/STORY-526/test_ac2_filter_builtin.sh | Created | 113 |
| tests/STORY-526/test_ac3_phase_record.sh | Created | 98 |
| tests/STORY-526/test_ac4_exit_code.sh | Created | 77 |
| tests/STORY-526/test_ac5_settings.sh | Created | 58 |
| tests/STORY-526/test_integration_e2e.sh | Created | 280 |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-03-02 12:00 | .claude/story-requirements-analyst | Created | Story created from EPIC-086 Feature 2 | STORY-526.story.md |
| 2026-03-02 | .claude/qa-result-interpreter | QA Deep | PASSED: Coverage >95%, 0 blocking violations | - |

## Notes

**Design Decisions:**
- Hook is non-blocking (exit 0 always) because recording is observational, not enforcement
- Built-in agent filter list is hardcoded in script (Explore, Plan, Bash, general-purpose)
- Uses existing phase-record CLI (not phase-record-step) for subagent tracking

**References:**
- EPIC-086: Claude Hooks for Step-Level Phase Enforcement
- STORY-525: Phase Steps Registry (dependency)

---

Story Template Version: 2.9
Last Updated: 2026-03-02
