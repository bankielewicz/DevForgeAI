---
id: STORY-023
title: Wire hooks into /dev command (pilot)
epic: EPIC-006
sprint: Sprint-2
status: Backlog
points: 8
priority: Critical
assigned_to: TBD
created: 2025-11-12
format_version: "2.0"
---

# Story: Wire hooks into /dev command (pilot)

## Description

**As a** DevForgeAI user running the /dev command,
**I want** automatic feedback prompts after my TDD cycle completes,
**so that** I can reflect on what I learned without having to remember to manually run /feedback.

## Acceptance Criteria

### 1. [ ] Phase N Added to /dev Command

**Given** the /dev command workflow is complete,
**When** the command reaches the end of its execution (after Phase 5: Git/Tracking),
**Then** a new "Phase 6: Invoke Feedback Hook" is added,
**And** the phase calls `devforgeai check-hooks --operation=dev --status=$STATUS`,
**And** if exit code is 0, calls `devforgeai invoke-hooks --operation=dev --story=$STORY_ID`,
**And** the phase is non-blocking (hook failures don't break /dev command).

---

### 2. [ ] Feedback Triggers on Success

**Given** I run `/dev STORY-001` and the TDD cycle completes successfully,
**When** the feedback hook check runs,
**Then** the feedback conversation starts automatically,
**And** I'm prompted with context-aware retrospective questions,
**And** the conversation references specific todos/phases from my dev session,
**And** my responses are persisted to `.devforgeai/feedback/sessions/`.

---

### 3. [ ] Feedback Skips When Configured

**Given** my hooks configuration has `enabled: false`,
**When** I run `/dev STORY-001`,
**Then** the check-hooks command returns exit code 1,
**And** invoke-hooks is NOT called,
**And** the /dev command completes without feedback prompt,
**And** a debug log shows "Hooks disabled, skipping feedback".

---

### 4. [ ] Feedback Respects failures-only Mode

**Given** my hooks configuration has `trigger_on: failures-only`,
**When** I run `/dev STORY-001` and it completes successfully (status=completed),
**Then** the check-hooks command returns exit code 1,
**And** invoke-hooks is NOT called,
**And** no feedback prompt appears.

**When** I run `/dev STORY-002` and it fails (status=failed),
**Then** the check-hooks command returns exit code 0,
**And** invoke-hooks IS called,
**And** feedback conversation starts asking about the failure.

---

### 5. [ ] Hook Failures Don't Break /dev

**Given** the feedback hook encounters an error (timeout, skill failure, etc.),
**When** the error occurs during hook invocation,
**Then** the error is logged with details,
**And** the /dev command continues to completion,
**And** the /dev command returns exit code 0 (success),
**And** the story status updates correctly,
**And** I see a warning "Feedback hook failed, continuing..."

---

### 6. [ ] Skip Tracking Works

**Given** I've skipped feedback 3 times in a row,
**When** the 4th feedback prompt appears,
**Then** the conversation includes "You've skipped 3 times - would you like to disable hooks?",
**And** if I select "Yes", the config updates to `enabled: false`,
**And** future /dev commands don't trigger feedback.

---

### 7. [ ] Performance Impact Minimal

**Given** I run `/dev STORY-001` with hooks enabled,
**When** the command completes,
**Then** the total overhead from check-hooks + invoke-hooks is <5 seconds,
**And** the check-hooks call completes in <100ms,
**And** the invoke-hooks context extraction completes in <200ms,
**And** the feedback conversation start time is <3s from command completion.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "DevCommandHookIntegration"
      file_path: ".claude/commands/dev.md"
      requirements:
        - id: "CONF-001"
          description: "Add Phase 6: Invoke Feedback Hook after existing Phase 5"
          testable: true
          test_requirement: "Test: Read dev.md, verify Phase 6 exists after Phase 5"
          priority: "Critical"
        - id: "CONF-002"
          description: "Phase 6 calls check-hooks with --operation=dev --status=$STATUS"
          testable: true
          test_requirement: "Test: Parse Phase 6 bash code, verify check-hooks call with correct arguments"
          priority: "Critical"
        - id: "CONF-003"
          description: "Phase 6 conditionally calls invoke-hooks based on exit code 0"
          testable: true
          test_requirement: "Test: Verify if [ $? -eq 0 ] condition wraps invoke-hooks call"
          priority: "Critical"
        - id: "CONF-004"
          description: "Phase 6 includes error handling (hook failures logged, not thrown)"
          testable: true
          test_requirement: "Test: Verify Phase 6 has try-catch or exit code check for invoke-hooks"
          priority: "High"

    - type: "Service"
      name: "DevCommandStatusDetermination"
      file_path: ".claude/commands/dev.md"
      requirements:
        - id: "SERV-001"
          description: "Determine $STATUS variable based on /dev command outcome"
          testable: true
          test_requirement: "Test: Verify logic sets STATUS=completed if tests pass, STATUS=failed if tests fail"
          priority: "High"
        - id: "SERV-002"
          description: "Pass $STORY_ID to invoke-hooks from command context"
          testable: true
          test_requirement: "Test: Verify invoke-hooks receives --story=$STORY_ID argument"
          priority: "High"

    - type: "Logging"
      name: "DevCommandHookLogging"
      file_path: ".claude/commands/dev.md"
      requirements:
        - id: "LOG-001"
          description: "Log hook check decision (trigger or skip)"
          testable: true
          test_requirement: "Test: Run /dev with hooks enabled, verify log 'Checking feedback hooks...'"
          priority: "Low"
        - id: "LOG-002"
          description: "Log hook invocation start"
          testable: true
          test_requirement: "Test: Verify log 'Invoking feedback hook for operation=dev'"
          priority: "Low"
        - id: "LOG-003"
          description: "Log hook failures with warning level"
          testable: true
          test_requirement: "Test: Mock hook failure, verify log 'WARNING: Feedback hook failed: [error]'"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "Feedback hooks are optional and never block /dev command completion"
      test_requirement: "Test: Mock invoke-hooks failure, verify /dev returns exit code 0"
    - id: "BR-002"
      rule: "Hook check respects configuration (enabled, trigger_on, operation-specific rules)"
      test_requirement: "Test: Set enabled=false, verify /dev skips feedback"
    - id: "BR-003"
      rule: "Status determination uses command outcome (tests pass = completed, tests fail = failed)"
      test_requirement: "Test: Mock test failure, verify STATUS=failed passed to check-hooks"

  non_functional_requirements:
    - id: "NFR-P1"
      category: "Performance"
      requirement: "Hook integration adds <5s overhead to /dev command"
      metric: "Measured time from end of Phase 5 to end of Phase 6 < 5 seconds"
      test_requirement: "Test: Run /dev 10 times with hooks enabled, measure Phase 6 duration, assert max <5s"
    - id: "NFR-R1"
      category: "Reliability"
      requirement: "/dev command success rate unchanged (hooks don't introduce failures)"
      metric: "100% /dev success rate when hooks enabled vs disabled (same test suite)"
      test_requirement: "Test: Run /dev 50 times with hooks enabled, verify all succeed if underlying TDD succeeds"
    - id: "NFR-U1"
      category: "Usability"
      requirement: "Users can easily disable hooks if desired"
      metric: "Skip tracking suggests disable after 3 skips, 1-click disable"
      test_requirement: "Test: Skip 3 times, verify 'disable hooks?' prompt appears"
```

## Edge Cases

1. **check-hooks command not found** (CLI not installed)
   - Log error "devforgeai check-hooks not found, skipping feedback"
   - Continue /dev command

2. **invoke-hooks times out** (30s timeout)
   - Log warning "Feedback hook timeout after 30s"
   - Continue /dev command

3. **User cancels feedback conversation mid-way**
   - Persist partial feedback
   - Continue /dev command

4. **Circular invocation** (feedback triggers /dev which triggers feedback)
   - Blocked by DEVFORGEAI_HOOK_ACTIVE guard
   - Logged and skipped

5. **Multiple concurrent /dev commands** (parallel execution)
   - Each has isolated hook invocation
   - No shared state corruption

## Non-Functional Requirements

**NFR-P1: Performance**
- Target: <5s overhead for hook integration
- Breakdown: check-hooks <100ms, invoke-hooks <3s, buffer 1-2s
- Acceptable impact: User notices ~5s delay but not disruptive

**NFR-R1: Reliability**
- Target: 100% /dev success rate unchanged
- Measurement: Compare /dev pass rate with hooks on/off
- Isolation: Hook failures never propagate to /dev command

**NFR-U1: Usability**
- Target: Easy disable after repeated skips
- Measurement: Skip tracking detects 3 consecutive skips, offers disable
- User control: 1-click disable via AskUserQuestion

## Definition of Done

### Implementation
- [ ] Phase 6 added to `.claude/commands/dev.md` after existing Phase 5
- [ ] STATUS variable determined from /dev outcome
- [ ] check-hooks called with correct arguments
- [ ] invoke-hooks conditionally called based on exit code
- [ ] Error handling prevents hook failures from breaking /dev
- [ ] All 7 acceptance criteria implemented

### Quality
- [ ] 10+ integration tests covering pilot scenarios
- [ ] Manual testing with real stories (5+ test cases)
- [ ] Performance verified: <5s overhead measured
- [ ] Reliability verified: 20 /dev runs, 100% success with hooks
- [ ] No regression in /dev command functionality

### Testing
- [ ] Test: /dev with hooks enabled → feedback triggers
- [ ] Test: /dev with hooks disabled → no feedback
- [ ] Test: /dev with failures-only mode + success → no feedback
- [ ] Test: /dev with failures-only mode + failure → feedback triggers
- [ ] Test: /dev with hook failure → /dev still succeeds
- [ ] Test: Skip 3 times → disable prompt appears
- [ ] Test: Measure overhead → <5s confirmed

### Documentation
- [ ] /dev command documentation updated (Phase 6 described)
- [ ] User guide: How to enable/disable hooks for /dev
- [ ] Integration pattern documented for remaining 10 commands
- [ ] Troubleshooting: Hook failures, timeout, circular invocation

## Dependencies

### Prerequisites
- STORY-021 (check-hooks CLI) completed
- STORY-022 (invoke-hooks CLI) completed
- devforgeai-feedback skill functional

### Blocked By
- STORY-021, STORY-022

### Blocks
- STORY-024 through STORY-033 (pilot validates pattern before full rollout)

## Notes

**Why /dev as Pilot?**
- High usage command (frequently run)
- Complex workflow (good test of hook integration)
- Clear success/failure status (easy to determine trigger)
- User feedback valuable (TDD reflections)

**Pilot Success Criteria:**
- 10+ users test /dev with hooks
- No /dev command breakage reported
- Feedback quality improved (context-aware questions)
- Performance acceptable (<5s overhead)
- Pattern validated for rollout to 10 remaining commands

**Integration Pattern (Proven):**
```bash
### Phase 6: Invoke Feedback Hook

# Determine status based on command outcome
if [ "$TESTS_PASSED" = "true" ]; then
  STATUS="completed"
else
  STATUS="failed"
fi

# Check if hooks should trigger
devforgeai check-hooks --operation=dev --status=$STATUS
if [ $? -eq 0 ]; then
  # Invoke feedback hook (errors logged, not thrown)
  devforgeai invoke-hooks --operation=dev --story=$STORY_ID || {
    echo "⚠️ Feedback hook failed, continuing..."
  }
fi
```

**Rollout Plan:**
1. Implement STORY-023 (pilot /dev)
2. Test with 10+ users (2 weeks)
3. Collect feedback, refine if needed
4. Rollout to 10 remaining commands (STORY-024 through STORY-033)

## Workflow History

- **2025-11-12:** Story created (STORY-023) - Batch mode from EPIC-006 Feature 6.2
