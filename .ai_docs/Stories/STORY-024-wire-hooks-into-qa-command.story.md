---
id: STORY-024
title: Wire hooks into /qa command
epic: EPIC-006
sprint: Sprint-2
status: Backlog
points: 5
priority: Critical
assigned_to: TBD
created: 2025-11-12
format_version: "2.0"
---

# Story: Wire hooks into /qa command

## Description

**As a** DevForgeAI user running the /qa command,
**I want** automatic feedback prompts when QA validation fails (but not when it passes),
**so that** I can reflect on what caused failures and improve quality practices without being interrupted during successful validations.

## Acceptance Criteria

### 1. [ ] Phase N Added to /qa Command

**Given** the /qa command workflow is complete (after Phase 3: Next Steps),
**When** the command reaches the end of execution,
**Then** a new "Phase 4: Invoke Feedback Hook" is added,
**And** the phase calls `devforgeai check-hooks --operation=qa --status=$STATUS`,
**And** if exit code is 0, calls `devforgeai invoke-hooks --operation=qa --story=$STORY_ID`,
**And** the phase is non-blocking (hook failures don't break /qa).

---

### 2. [ ] Feedback Triggers on QA Failures

**Given** my hooks config has `trigger_on: failures-only` (default),
**When** I run `/qa STORY-001 deep` and validation fails (coverage <80%, violations detected),
**Then** check-hooks returns exit code 0,
**And** invoke-hooks is called automatically,
**And** feedback conversation starts with context-aware questions about the failure,
**And** questions reference specific violations (e.g., "Coverage was 75% - what prevented higher coverage?").

---

### 3. [ ] Feedback Skips on QA Success

**Given** my hooks config has `trigger_on: failures-only`,
**When** I run `/qa STORY-001 deep` and validation passes (all quality gates passed),
**Then** check-hooks returns exit code 1 (don't trigger),
**And** invoke-hooks is NOT called,
**And** /qa completes normally with success message,
**And** no feedback prompt appears.

---

### 4. [ ] Status Determination from QA Result

**Given** QA validation completes,
**When** the result is "PASSED" (all quality gates met),
**Then** STATUS="completed" is passed to check-hooks.

**When** the result is "FAILED" (violations detected),
**Then** STATUS="failed" is passed to check-hooks.

**When** the result is "PARTIAL" (some warnings but no blocking issues),
**Then** STATUS="partial" is passed to check-hooks.

---

### 5. [ ] Hook Failures Don't Break /qa

**Given** the feedback hook encounters an error (timeout, skill failure),
**When** the error occurs during hook invocation,
**Then** the error is logged with details,
**And** the /qa command continues to completion,
**And** /qa returns the original QA result (not hook failure),
**And** I see a warning "Feedback hook failed, QA result unchanged".

---

### 6. [ ] Light Mode Integration

**Given** I run `/qa STORY-001 light` (quick validation),
**When** light validation fails,
**Then** hook check runs with --operation=qa --status=failed,
**And** feedback is triggered if config allows,
**And** light mode result is not affected by hook.

---

### 7. [ ] Deep Mode Integration

**Given** I run `/qa STORY-001 deep` (comprehensive validation),
**When** deep validation fails with specific violations (coverage, anti-patterns, spec compliance),
**Then** hook invocation passes violation context to feedback,
**And** feedback questions reference specific violations,
**And** deep mode report generation is not affected by hook.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "QACommandHookIntegration"
      file_path: ".claude/commands/qa.md"
      requirements:
        - id: "CONF-001"
          description: "Add Phase 4: Invoke Feedback Hook after Phase 3: Next Steps"
          testable: true
          test_requirement: "Test: Read qa.md, verify Phase 4 exists after Phase 3"
          priority: "Critical"
        - id: "CONF-002"
          description: "Determine STATUS from QA result (PASSED=completed, FAILED=failed, PARTIAL=partial)"
          testable: true
          test_requirement: "Test: Mock QA failure, verify STATUS=failed passed to check-hooks"
          priority: "High"
        - id: "CONF-003"
          description: "Phase 4 calls check-hooks with --operation=qa --status=$STATUS"
          testable: true
          test_requirement: "Test: Parse Phase 4 bash code, verify check-hooks call with correct arguments"
          priority: "Critical"
        - id: "CONF-004"
          description: "Phase 4 conditionally calls invoke-hooks based on exit code 0"
          testable: true
          test_requirement: "Test: Verify if [ $? -eq 0 ] condition wraps invoke-hooks call"
          priority: "Critical"
        - id: "CONF-005"
          description: "Phase 4 includes error handling (hook failures logged, not thrown)"
          testable: true
          test_requirement: "Test: Verify Phase 4 has try-catch for invoke-hooks"
          priority: "High"

    - type: "Service"
      name: "QAResultStatusMapping"
      file_path: ".claude/commands/qa.md"
      requirements:
        - id: "SERV-001"
          description: "Map QA result to status: PASSED→completed, FAILED→failed, PARTIAL→partial"
          testable: true
          test_requirement: "Test: Mock each QA result, verify correct STATUS set"
          priority: "High"
        - id: "SERV-002"
          description: "Extract violation context from QA report for feedback"
          testable: true
          test_requirement: "Test: Mock QA report with violations, verify context extracted"
          priority: "Medium"

    - type: "Logging"
      name: "QACommandHookLogging"
      file_path: ".claude/commands/qa.md"
      requirements:
        - id: "LOG-001"
          description: "Log hook check decision (trigger or skip)"
          testable: true
          test_requirement: "Test: Run /qa with failures-only + pass, verify log 'QA passed, skipping feedback (failures-only mode)'"
          priority: "Low"
        - id: "LOG-002"
          description: "Log hook invocation start with QA result"
          testable: true
          test_requirement: "Test: Verify log 'Invoking feedback hook: qa failed (coverage 75%, violations: 3)'"
          priority: "Medium"
        - id: "LOG-003"
          description: "Log hook failures with warning level"
          testable: true
          test_requirement: "Test: Mock hook failure, verify log 'WARNING: Feedback hook failed, QA result unchanged'"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "Default config (failures-only) triggers feedback on QA failures only, not successes"
      test_requirement: "Test: QA pass with failures-only → no feedback, QA fail → feedback"
    - id: "BR-002"
      rule: "QA result (pass/fail) is determined BEFORE hook check (hook never changes result)"
      test_requirement: "Test: Mock hook failure during QA pass, verify /qa still returns pass"
    - id: "BR-003"
      rule: "Light and deep modes both support hook integration (same pattern)"
      test_requirement: "Test: /qa light fail → hook triggers, /qa deep fail → hook triggers"

  non_functional_requirements:
    - id: "NFR-P1"
      category: "Performance"
      requirement: "Hook integration adds <5s overhead to /qa command"
      metric: "Measured time from Phase 3 end to Phase 4 end < 5 seconds"
      test_requirement: "Test: Run /qa 10 times with hooks enabled, measure Phase 4 duration, assert max <5s"
    - id: "NFR-R1"
      category: "Reliability"
      requirement: "/qa result accuracy unchanged (hooks don't affect validation outcome)"
      metric: "100% identical results with hooks on vs off (same codebase, 20 runs)"
      test_requirement: "Test: Run /qa 20 times with hooks enabled, compare results to baseline (hooks disabled)"
    - id: "NFR-U1"
      category: "Usability"
      requirement: "Feedback questions reference specific QA violations"
      metric: "Context includes coverage %, violation types, failed criteria"
      test_requirement: "Test: QA fail with coverage 75%, verify feedback mentions '75%' in questions"
```

## Edge Cases

1. **QA report generation fails** (before hook runs)
   - Hook check skipped, log warning
   - /qa returns failure for QA report issue

2. **Story status already "QA Approved"** (re-running QA)
   - Hook runs normally (status determined by new result)
   - Previous QA history preserved

3. **Multiple QA validation attempts** (retry after fix)
   - Each attempt triggers hook independently
   - Feedback references attempt number if available

4. **User exits /qa during validation** (Ctrl+C)
   - Hook does not run (validation incomplete)
   - No partial feedback collected

5. **QA deep mode with partial pass** (warnings but no failures)
   - STATUS="partial" passed to check-hooks
   - Config determines if partial triggers feedback

## Non-Functional Requirements

**NFR-P1: Performance**
- Target: <5s overhead for hook integration
- Measurement: Time from Phase 3 end to Phase 4 end
- Acceptable: User notices brief delay but QA result displayed first

**NFR-R1: Reliability**
- Target: 100% /qa result accuracy unchanged by hooks
- Measurement: Compare /qa results with hooks on/off
- Isolation: Hook failures never change QA pass/fail outcome

**NFR-U1: Usability**
- Target: Feedback questions specific to QA failures
- Example: "Coverage was 75% (target 85%) - what prevented higher coverage?"
- Context-aware: Reference specific violations from QA report

## Definition of Done

### Implementation
- [ ] Phase 4 added to `.claude/commands/qa.md` after Phase 3
- [ ] STATUS determination logic implemented (PASSED/FAILED/PARTIAL mapping)
- [ ] check-hooks called with correct arguments
- [ ] invoke-hooks conditionally called based on exit code
- [ ] Error handling prevents hook failures from breaking /qa
- [ ] Violation context extracted for feedback
- [ ] All 7 acceptance criteria implemented

### Quality
- [ ] 12+ integration tests covering /qa hook scenarios
- [ ] Manual testing with real stories (light and deep modes)
- [ ] Performance verified: <5s overhead measured
- [ ] Reliability verified: 20 /qa runs, 100% result accuracy
- [ ] No regression in /qa functionality

### Testing
- [ ] Test: /qa deep fail with failures-only → feedback triggers
- [ ] Test: /qa deep pass with failures-only → no feedback
- [ ] Test: /qa light fail → feedback triggers
- [ ] Test: /qa with hook failure → /qa result unchanged
- [ ] Test: Violation context passed to feedback
- [ ] Test: Measure overhead → <5s confirmed
- [ ] Test: Compare results hooks on/off → 100% match

### Documentation
- [ ] /qa command documentation updated (Phase 4 described)
- [ ] User guide: Hook behavior for /qa (failures-only default)
- [ ] Integration pattern documented
- [ ] Troubleshooting: Hook failures, timeout, context extraction

## Dependencies

### Prerequisites
- STORY-021 (check-hooks CLI) completed
- STORY-022 (invoke-hooks CLI) completed
- STORY-023 (/dev pilot) completed and validated

### Blocked By
- STORY-023 (pilot validates integration pattern)

### Blocks
- None (can proceed in parallel with other command integrations)

## Notes

**Why failures-only Default Makes Sense for /qa:**
- Users run /qa frequently (validation cycles)
- Success is common (after fixing issues)
- Feedback most valuable when unexpected failures occur
- Reduces interruption frequency while capturing critical insights

**Context Extraction for QA Failures:**
```python
qa_context = {
    "operation": "qa",
    "story_id": "STORY-001",
    "mode": "deep",
    "result": "FAILED",
    "coverage": {
        "actual": 75,
        "target": 85,
        "gap": 10
    },
    "violations": [
        {"type": "coverage", "severity": "HIGH", "message": "Business logic coverage 75% < 85%"},
        {"type": "anti-pattern", "severity": "MEDIUM", "message": "God Object detected in UserService.cs"},
        {"type": "spec-compliance", "severity": "LOW", "message": "AC-3 not fully validated"}
    ],
    "duration": 45  # seconds
}
```

**Integration Pattern (Proven from Pilot):**
```bash
### Phase 4: Invoke Feedback Hook

# Determine status from QA result
if [ "$QA_RESULT" = "PASSED" ]; then
  STATUS="completed"
elif [ "$QA_RESULT" = "FAILED" ]; then
  STATUS="failed"
else
  STATUS="partial"
fi

# Check if hooks should trigger
devforgeai check-hooks --operation=qa --status=$STATUS
if [ $? -eq 0 ]; then
  # Extract violation context for feedback
  VIOLATIONS=$(cat .devforgeai/qa/reports/${STORY_ID}-qa-report.md | grep "VIOLATION")

  # Invoke feedback hook (errors logged, not thrown)
  devforgeai invoke-hooks --operation=qa --story=$STORY_ID --context="$VIOLATIONS" || {
    echo "⚠️ Feedback hook failed, QA result unchanged"
  }
fi
```

## Workflow History

- **2025-11-12:** Story created (STORY-024) - Batch mode from EPIC-006 Feature 6.2
