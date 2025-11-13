---
id: STORY-031
title: Wire hooks into /ideate command
epic: EPIC-006
sprint: Sprint-3
status: Backlog
points: 5
priority: High
assigned_to: TBD
created: 2025-11-13
format_version: "2.0"
---

# Story: Wire hooks into /ideate command

## Description

**As a** product owner or business analyst using DevForgeAI,
**I want** the /ideate command to automatically trigger post-ideation feedback when eligible,
**so that** I can capture insights about the requirements discovery process, complexity assessment accuracy, and epic decomposition quality while the experience is fresh.

## Acceptance Criteria

### 1. [ ] Hook Eligibility Check After Ideation

**Given** the /ideate command has completed Phase 6 (Documentation) and all epic/requirements artifacts are created,
**When** the command reaches Phase N (Hook Integration),
**Then** it calls `devforgeai check-hooks --operation=ideate --status=completed` to determine feedback eligibility,
**And** the eligibility check completes without blocking the main command flow.

---

### 2. [ ] Automatic Feedback Invocation When Eligible

**Given** the hook eligibility check returned eligible=true,
**When** Phase N proceeds to feedback invocation,
**Then** it calls `devforgeai invoke-hooks --operation=ideate` to trigger the retrospective conversation,
**And** the feedback conversation references ideation-specific context (epic documents, requirements specs, complexity scores, feasibility analysis),
**And** the command displays "✓ Post-ideation feedback initiated" to the user.

---

### 3. [ ] Graceful Degradation on Hook Failures

**Given** either the eligibility check or feedback invocation fails (CLI error, timeout, hook system unavailable),
**When** Phase N encounters the failure,
**Then** the error is logged but does NOT halt the /ideate command,
**And** the command displays "⚠ Post-ideation feedback skipped (hook system unavailable)" as a warning,
**And** the ideation results (epic documents, requirements specs) remain valid and accessible.

---

### 4. [ ] Context-Aware Feedback Configuration

**Given** the ideation operation has completed with specific artifacts (1-N epic documents, requirements specs, complexity assessments),
**When** the feedback system is invoked,
**Then** the feedback configuration includes ideation-specific context: operation_type="ideation", artifacts=[epic paths, requirements spec paths], complexity_score=[N], questions_asked=[count],
**And** the retrospective conversation template adapts to ideation concerns (requirements clarity, epic scoping, feasibility accuracy, question effectiveness).

---

### 5. [ ] Pattern Consistency with Pilot Implementation

**Given** the /dev command pilot (STORY-023) established the integration pattern,
**When** implementing Phase N in /ideate,
**Then** the implementation follows the same structural pattern: Phase N placement after primary work, check-hooks call, conditional invoke-hooks call, graceful error handling,
**And** the code structure matches pilot conventions (error messages, logging format, phase numbering),
**And** the implementation is documented with references to the pilot pattern.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "ideate command hook integration"
      file_path: ".claude/commands/ideate.md"
      requirements:
        - id: "CONF-001"
          description: "Add Phase N after Phase 6 (Documentation complete) to invoke hooks"
          testable: true
          test_requirement: "Test: Verify Phase N section exists in command file after Phase 6"
          priority: "Critical"

        - id: "CONF-002"
          description: "Add bash code block calling 'devforgeai check-hooks --operation=ideate --status=completed'"
          testable: true
          test_requirement: "Test: Verify check-hooks call with correct arguments exists in Phase N"
          priority: "Critical"

        - id: "CONF-003"
          description: "Add conditional logic: if exit code 0, call 'devforgeai invoke-hooks --operation=ideate'"
          testable: true
          test_requirement: "Test: Verify invoke-hooks called only when check-hooks returns 0"
          priority: "Critical"

        - id: "CONF-004"
          description: "Pass ideation context to hooks: epic paths, requirements specs, complexity score, question count"
          testable: true
          test_requirement: "Test: Verify context JSON includes all 4 metadata fields when invoking hooks"
          priority: "High"

        - id: "CONF-005"
          description: "Ensure Phase N is non-blocking (errors logged, command succeeds regardless)"
          testable: true
          test_requirement: "Test: Simulate hook failure, verify command still completes successfully with epic/specs created"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Hook invocation must not block ideation artifact creation success"
      test_requirement: "Test: Create epics/specs with hooks disabled/failing, verify all artifacts created"

    - id: "BR-002"
      rule: "Hook eligibility check must complete in <500ms (slower than other commands due to ideation complexity)"
      test_requirement: "Test: Measure check-hooks execution time, assert <500ms 95th percentile"

    - id: "BR-003"
      rule: "Ideation context must include all created artifacts for meaningful feedback"
      test_requirement: "Test: Run /ideate creating 3 epics, verify hook context includes all 3 epic paths"

    - id: "BR-004"
      rule: "Hook integration must follow same pattern as /dev pilot (STORY-023) for consistency"
      test_requirement: "Test: Compare Phase N structure in ideate vs dev, verify pattern match"

  non_functional_requirements:
    - id: "NFR-P1"
      category: "Performance"
      requirement: "Hook eligibility check must complete in <500ms (95th percentile)"
      metric: "Measured via command execution time, checked via logs"
      test_requirement: "Test: Run /ideate 20 times, measure check-hooks duration, assert <500ms for 19+ runs"

    - id: "NFR-R1"
      category: "Reliability"
      requirement: "Command must maintain 100% success rate regardless of hook system state"
      metric: "Ideation artifacts created successfully even if hooks fail (exit code 0 regardless)"
      test_requirement: "Test: Simulate 5 hook failure scenarios, verify command returns exit code 0 with epics/specs created in all cases"

    - id: "NFR-M1"
      category: "Maintainability"
      requirement: "Phase N implementation maintains <50 lines of code following DRY principles"
      metric: "Line count in Phase N section, no code duplication with pilot"
      test_requirement: "Test: Count lines in Phase N, assert <50. Verify hook logic matches pilot pattern (no divergence)"
```

## UI Specification

Not applicable - This is a command-line interface modification with no graphical UI components.

## Edge Cases

- **Case 1: Hook system disabled in configuration:** check-hooks returns eligible=false immediately, Phase N skips invocation gracefully, no warning displayed (intentional configuration)

- **Case 2: Multiple epics created in single ideation session:** Feedback context includes all epic document paths as an array, retrospective conversation can reference any/all epics for quality assessment

- **Case 3: Ideation aborted mid-process (user cancellation, error):** Phase N never reached (only runs after Phase 6 completion), hook not invoked for incomplete ideation sessions

- **Case 4: Feedback system already invoked manually:** Hook system tracks invocation history, check-hooks returns eligible=false for duplicate invocations, prevents double-feedback on same operation

- **Case 5: User running batch ideation (multiple projects/epics sequentially):** Each /ideate invocation treated independently, hook eligibility checked per operation, feedback invoked once per ideation session if eligible

## Non-Functional Requirements

- **NFR-P1 (Performance):** Hook eligibility check completes in <500ms (95th percentile), feedback invocation is asynchronous and does NOT block command completion

- **NFR-R1 (Reliability):** Hook integration failures have ZERO impact on ideation success rate (100% graceful degradation), all hook errors logged to .devforgeai/feedback/logs/hook-errors.log with timestamps

- **NFR-M1 (Maintainability):** Phase N implementation maintains <50 lines of code following DRY principles, hook integration logic is extracted to reusable helper function (can be shared with other commands during Feature 6.2 rollout)

## Dependencies

### Prerequisites
- **STORY-021:** devforgeai check-hooks CLI command must be implemented and tested
- **STORY-022:** devforgeai invoke-hooks CLI command must be implemented and tested
- **STORY-023:** /dev pilot integration completed and pattern validated

### Dependent Stories
- **STORY-032:** /create-ui command integration (follows same pattern)
- **STORY-033:** /audit-deferrals command integration (follows same pattern)

## Definition of Done

### Implementation
- [ ] Phase N added to .claude/commands/ideate.md after Phase 6 (Documentation)
- [ ] Bash code block with check-hooks call implemented
- [ ] Conditional invoke-hooks call implemented (exit code 0 check)
- [ ] Ideation context passed to hooks (epic paths, requirements specs, complexity score, question count)
- [ ] Error handling with graceful degradation implemented
- [ ] Warning messages for hook failures added (<50 words, non-alarming)
- [ ] Pattern matches /dev pilot (STORY-023) for consistency
- [ ] Code extracted to reusable helper function (DRY principle)

### Quality
- [ ] Unit tests: Hook check logic verified (5+ test cases)
- [ ] Integration tests: Full command flow with hooks enabled/disabled (10+ scenarios including context passing)
- [ ] Edge case tests: All 5 edge cases covered
- [ ] Performance test: Hook check <500ms 95th percentile (20 runs measured)
- [ ] Reliability test: Command succeeds with hooks failing (5 failure scenarios)
- [ ] Context passing test: Verify all 4 metadata fields included
- [ ] Code review: Pattern consistency verified against STORY-023
- [ ] Maintainability review: <50 lines, no duplication

### Testing
- [ ] Test Case 1: Ideation complete (1 epic), check-hooks returns 0 → invoke-hooks called with context
- [ ] Test Case 2: Ideation complete, check-hooks returns 1 → invoke-hooks skipped
- [ ] Test Case 3: CLI missing → warning logged, command succeeds, epics created
- [ ] Test Case 4: Config invalid → warning logged, command succeeds
- [ ] Test Case 5: Hook interrupted (Ctrl+C) → partial save, command succeeds
- [ ] Test Case 6: Multiple epics (3) → context includes all 3 paths
- [ ] Test Case 7: Ideation aborted → hooks not invoked
- [ ] Test Case 8: Duplicate invocation → check-hooks prevents double-feedback
- [ ] Test Case 9: Measure overhead with skip_all:true → <500ms
- [ ] Test Case 10: Compare Phase N with /dev → pattern match confirmed

### Documentation
- [ ] Command integration documented in `.claude/commands/ideate.md`
- [ ] Pattern documented in `.devforgeai/protocols/hook-integration-pattern.md`
- [ ] Context passing format documented
- [ ] User guide updated with /ideate feedback capability
- [ ] Troubleshooting section added for hook failures

## Acceptance Sign-Off

- [ ] Product Owner: Story meets acceptance criteria
- [ ] Tech Lead: Implementation follows pilot pattern (STORY-023)
- [ ] QA Lead: All tests pass, no regressions
- [ ] User Testing: 3+ users validate hook experience with ideation workflows

---

**Related Documents:**
- Epic: `.ai_docs/Epics/EPIC-006-feedback-integration-completion.epic.md`
- Sprint: `.ai_docs/Sprints/Sprint-3.md`
- Pilot Story: `.ai_docs/Stories/STORY-023-wire-hooks-into-dev-command-pilot.story.md`
- Hook Infrastructure: `STORY-021`, `STORY-022`
