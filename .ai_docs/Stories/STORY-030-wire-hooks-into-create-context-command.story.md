---
id: STORY-030
title: Wire hooks into /create-context command
epic: EPIC-006
sprint: Sprint-3
status: Backlog
points: 3
priority: High
assigned_to: TBD
created: 2025-11-13
format_version: "2.0"
---

# Story: Wire hooks into /create-context command

## Description

**As a** DevForgeAI user,
**I want** the /create-context command to automatically trigger feedback conversations after successful context file creation,
**so that** I can provide insights about the context setup process while the experience is fresh and contribute to continuous framework improvement.

## Acceptance Criteria

### 1. [ ] Hook Eligibility Check After Context Creation

**Given** the /create-context command has successfully created all 6 context files (.devforgeai/context/*.md),
**When** Phase N executes immediately after Phase 4 (context file creation completes),
**Then** the command invokes `devforgeai check-hooks --operation=create-context --status=completed`,
**And** the command captures the exit code and proceeds based on eligibility (0 = eligible, 1 = skip).

---

### 2. [ ] Automatic Hook Invocation When Eligible

**Given** the check-hooks command returns exit code 0 (user is eligible for feedback),
**When** the /create-context command receives the eligible response,
**Then** the command invokes `devforgeai invoke-hooks --operation=create-context --status=completed`,
**And** the command waits for the feedback conversation to complete before displaying final completion message,
**And** the command captures feedback conversation metadata (if provided).

---

### 3. [ ] Graceful Degradation on Hook Failures

**Given** either check-hooks or invoke-hooks encounters an error (CLI not installed, config invalid, conversation fails),
**When** the hook execution fails at any point,
**Then** the command logs a warning message ("Optional feedback system unavailable, continuing..."),
**And** the command completes successfully with all context files created,
**And** the command does NOT halt or error due to hook failures,
**And** users can still use /create-context normally.

---

### 4. [ ] Hook Skip When Not Eligible

**Given** the check-hooks command returns exit code 1 (user not eligible due to skip patterns, rate limits, or configuration),
**When** the /create-context command receives the ineligible response,
**Then** the command skips hook invocation entirely,
**And** the command displays the standard completion message without mentioning feedback,
**And** the command execution time remains unaffected by hook check overhead (<100ms).

---

### 5. [ ] Integration with Existing Command Flow

**Given** the /create-context command completes Phase 4 (context files created),
**When** Phase N (hook integration) executes,
**Then** the command maintains backward compatibility (existing usage patterns unchanged),
**And** the command's primary success criteria remain context file creation (hooks are secondary),
**And** the command output clearly separates context creation success from optional feedback,
**And** the command follows the same hook pattern as /dev pilot (STORY-023).

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "create-context command hook integration"
      file_path: ".claude/commands/create-context.md"
      requirements:
        - id: "CONF-001"
          description: "Add Phase N after Phase 4 (context file creation) to invoke hooks"
          testable: true
          test_requirement: "Test: Verify Phase N section exists in command file after Phase 4"
          priority: "Critical"

        - id: "CONF-002"
          description: "Add bash code block calling 'devforgeai check-hooks --operation=create-context --status=completed'"
          testable: true
          test_requirement: "Test: Verify check-hooks call with correct arguments exists in Phase N"
          priority: "Critical"

        - id: "CONF-003"
          description: "Add conditional logic: if exit code 0, call 'devforgeai invoke-hooks --operation=create-context'"
          testable: true
          test_requirement: "Test: Verify invoke-hooks called only when check-hooks returns 0"
          priority: "Critical"

        - id: "CONF-004"
          description: "Ensure Phase N is non-blocking (errors logged, command succeeds regardless)"
          testable: true
          test_requirement: "Test: Simulate hook failure, verify command still completes successfully with context files created"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Hook invocation must not block context file creation success"
      test_requirement: "Test: Create context files with hooks disabled/failing, verify all 6 files created"

    - id: "BR-002"
      rule: "Hook eligibility check must complete in <100ms to avoid user-perceived delay"
      test_requirement: "Test: Measure check-hooks execution time, assert <100ms"

    - id: "BR-003"
      rule: "Hook integration must follow same pattern as /dev pilot (STORY-023) for consistency"
      test_requirement: "Test: Compare Phase N structure in create-context vs dev, verify pattern match"

  non_functional_requirements:
    - id: "NFR-P1"
      category: "Performance"
      requirement: "Hook eligibility check must add <100ms overhead when skipped"
      metric: "Measured via command execution time comparison (with/without hooks configured)"
      test_requirement: "Test: Run /create-context 10 times with skip_all:true, measure average overhead <100ms"

    - id: "NFR-R1"
      category: "Reliability"
      requirement: "Command must maintain 100% success rate regardless of hook system state"
      metric: "Context files created successfully even if hooks fail (exit code 0 regardless)"
      test_requirement: "Test: Simulate 5 hook failure scenarios (CLI missing, config invalid, conversation interrupted, timeout, permission error), verify command returns exit code 0 with 6 context files created in all cases"

    - id: "NFR-U1"
      category: "Usability"
      requirement: "Hook failures must display concise, non-alarming messages"
      metric: "Error messages <50 words, no scary language, include 'optional' keyword"
      test_requirement: "Test: Trigger hook failures, verify error message format matches 'Optional feedback system unavailable, continuing...'"
```

## UI Specification

Not applicable - This is a command-line interface modification with no graphical UI components.

## Edge Cases

- **CLI not installed:** If devforgeai CLI is missing, check-hooks will fail. Command should catch error, log warning "devforgeai CLI not found, skipping feedback", and complete successfully. Users can install CLI later.

- **Config file corrupted:** If .devforgeai/config/hooks.yaml is invalid, check-hooks may error. Command should catch parsing errors, log warning "Hook configuration invalid, skipping feedback", and complete successfully. Users can fix config with `devforgeai check-hooks --validate`.

- **User interrupts feedback (Ctrl+C):** If user cancels feedback conversation mid-flow, invoke-hooks should handle gracefully (save partial responses if any). /create-context should detect interruption, log "Feedback interrupted by user", and complete successfully without re-triggering hooks on next run.

- **Multiple rapid invocations:** If user runs /create-context multiple times quickly (e.g., testing, different projects), rate limiting in hooks.yaml should prevent feedback fatigue. Command should respect rate limits from check-hooks (1 = skip), no special handling needed.

## Non-Functional Requirements

- **NFR-P1 (Performance):** Hook check execution must add <100ms overhead to /create-context command when skipped (not eligible). Full feedback conversation may add 30-90 seconds when invoked, which is acceptable for post-creation feedback.

- **NFR-R1 (Reliability):** Hook integration must maintain 100% /create-context command success rate regardless of hook system state. If hooks fail, context files are still created successfully and command returns exit code 0.

- **NFR-U1 (Usability):** Hook invocation must be transparent to users who have opted out (skip_all: true). Users should not see feedback prompts or delays if they've configured skip patterns. Error messages for hook failures must be concise (<50 words) and non-alarming ("Optional feedback unavailable").

## Dependencies

### Prerequisites
- **STORY-021:** devforgeai check-hooks CLI command must be implemented and tested
- **STORY-022:** devforgeai invoke-hooks CLI command must be implemented and tested
- **STORY-023:** /dev pilot integration completed and pattern validated

### Dependent Stories
- **STORY-031:** /ideate command integration (follows same pattern)
- **STORY-032:** /create-ui command integration (follows same pattern)
- **STORY-033:** /audit-deferrals command integration (follows same pattern)

## Definition of Done

### Implementation
- [ ] Phase N added to .claude/commands/create-context.md after Phase 4
- [ ] Bash code block with check-hooks call implemented
- [ ] Conditional invoke-hooks call implemented (exit code 0 check)
- [ ] Error handling with graceful degradation implemented
- [ ] Warning messages for hook failures added (<50 words, non-alarming)
- [ ] Pattern matches /dev pilot (STORY-023) for consistency

### Quality
- [ ] Unit tests: Hook check logic verified (5+ test cases)
- [ ] Integration tests: Full command flow with hooks enabled/disabled (8+ scenarios)
- [ ] Edge case tests: All 4 edge cases covered
- [ ] Performance test: Hook check overhead <100ms (10 runs measured)
- [ ] Reliability test: Command succeeds with hooks failing (5 failure scenarios)
- [ ] Backward compatibility: Existing /create-context usage unchanged
- [ ] Code review: Pattern consistency verified against STORY-023

### Testing
- [ ] Test Case 1: Context files created, check-hooks returns 0 → invoke-hooks called
- [ ] Test Case 2: Context files created, check-hooks returns 1 → invoke-hooks skipped
- [ ] Test Case 3: CLI missing → warning logged, command succeeds, 6 files created
- [ ] Test Case 4: Config invalid → warning logged, command succeeds
- [ ] Test Case 5: Hook interrupted (Ctrl+C) → partial save, command succeeds
- [ ] Test Case 6: Rate limit exceeded → hooks skipped silently
- [ ] Test Case 7: Measure overhead with skip_all:true → <100ms
- [ ] Test Case 8: Compare Phase N with /dev → pattern match confirmed

### Documentation
- [ ] Command integration documented in `.claude/commands/create-context.md`
- [ ] Pattern documented in `.devforgeai/protocols/hook-integration-pattern.md`
- [ ] User guide updated with /create-context feedback capability
- [ ] Troubleshooting section added for hook failures

## Acceptance Sign-Off

- [ ] Product Owner: Story meets acceptance criteria
- [ ] Tech Lead: Implementation follows pilot pattern (STORY-023)
- [ ] QA Lead: All tests pass, no regressions
- [ ] User Testing: 3+ users validate hook experience

---

**Related Documents:**
- Epic: `.ai_docs/Epics/EPIC-006-feedback-integration-completion.epic.md`
- Sprint: `.ai_docs/Sprints/Sprint-3.md`
- Pilot Story: `.ai_docs/Stories/STORY-023-wire-hooks-into-dev-command-pilot.story.md`
- Hook Infrastructure: `STORY-021`, `STORY-022`
