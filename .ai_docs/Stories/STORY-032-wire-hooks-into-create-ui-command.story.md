---
id: STORY-032
title: Wire hooks into /create-ui command
epic: EPIC-006
sprint: Sprint-3
status: Backlog
points: 5
priority: High
assigned_to: TBD
created: 2025-11-13
format_version: "2.0"
---

# Story: Wire hooks into /create-ui command

## Description

**As a** DevForgeAI user creating UI components,
**I want** the feedback system to automatically collect my insights after UI specification generation completes,
**so that** I can share valuable context about UI complexity, technology fit, and design clarity without manual effort.

## Acceptance Criteria

### 1. [ ] Hook Eligibility Check After UI Generation

**Given** the /create-ui command has completed Phase 6 (Documentation) successfully,
**When** UI specs have been generated in .devforgeai/specs/ui/,
**Then** the command calls `devforgeai check-hooks --operation=create-ui --status=completed`,
**And** the eligibility result determines whether to proceed with feedback invocation.

---

### 2. [ ] Automatic Feedback Invocation When Eligible

**Given** hook eligibility check returns eligible=true,
**When** the check-hooks command completes,
**Then** the command calls `devforgeai invoke-hooks --operation=create-ui`,
**And** the feedback conversation launches automatically,
**And** context includes UI type (web/GUI/terminal), technology choices, component complexity, and generated files.

---

### 3. [ ] Graceful Degradation on Hook Failures

**Given** hook eligibility check or invocation fails (CLI not installed, config error, hook error),
**When** the failure occurs during Phase N,
**Then** the command logs a warning message ("Feedback system unavailable, continuing..."),
**And** the /create-ui workflow completes normally without breaking,
**And** the user receives their UI specifications as expected.

---

### 4. [ ] Context-Aware Feedback Collection

**Given** feedback conversation is invoked after UI generation,
**When** the retrospective questions are presented,
**Then** questions reference UI-specific context (technology choice rationale, mockup clarity, component complexity),
**And** the operation_metadata includes ui_type, selected_technology, styling_approach, components_generated,
**And** the feedback captures insights valuable for future UI generation improvements.

---

### 5. [ ] Pilot Pattern Consistency

**Given** hook integration uses the /dev pilot pattern (STORY-023),
**When** implementing Phase N in /create-ui,
**Then** the implementation matches pilot structure (eligibility check → conditional invocation → graceful degradation),
**And** error handling follows same approach (log warnings, don't break workflow),
**And** the hook phase is clearly documented in command workflow.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "create-ui command hook integration"
      file_path: ".claude/commands/create-ui.md"
      requirements:
        - id: "CONF-001"
          description: "Add Phase N after Phase 6 (Documentation complete) to invoke hooks"
          testable: true
          test_requirement: "Test: Verify Phase N section exists in command file after Phase 6"
          priority: "Critical"

        - id: "CONF-002"
          description: "Add bash code block calling 'devforgeai check-hooks --operation=create-ui --status=completed'"
          testable: true
          test_requirement: "Test: Verify check-hooks call with correct arguments exists in Phase N"
          priority: "Critical"

        - id: "CONF-003"
          description: "Add conditional logic: if exit code 0, call 'devforgeai invoke-hooks --operation=create-ui'"
          testable: true
          test_requirement: "Test: Verify invoke-hooks called only when check-hooks returns 0"
          priority: "Critical"

        - id: "CONF-004"
          description: "Pass UI context to hooks: ui_type (web/GUI/terminal), technology, styling, component list"
          testable: true
          test_requirement: "Test: Verify context JSON includes all 4 metadata fields when invoking hooks"
          priority: "High"

        - id: "CONF-005"
          description: "Ensure Phase N is non-blocking (errors logged, command succeeds regardless)"
          testable: true
          test_requirement: "Test: Simulate hook failure, verify command still completes successfully with UI specs created"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Hook invocation must not block UI specification creation success"
      test_requirement: "Test: Generate UI specs with hooks disabled/failing, verify all specs created"

    - id: "BR-002"
      rule: "Hook eligibility check must complete in <500ms (UI generation already interactive, small overhead acceptable)"
      test_requirement: "Test: Measure check-hooks execution time, assert <500ms"

    - id: "BR-003"
      rule: "UI context must include technology choices for meaningful feedback about tech fit"
      test_requirement: "Test: Generate React component, verify hook context includes 'technology: React'"

    - id: "BR-004"
      rule: "Hook integration must follow same pattern as /dev pilot (STORY-023) for consistency"
      test_requirement: "Test: Compare Phase N structure in create-ui vs dev, verify pattern match"

  non_functional_requirements:
    - id: "NFR-P1"
      category: "Performance"
      requirement: "Hook eligibility check must complete in <500ms"
      metric: "Measured via command execution time logs"
      test_requirement: "Test: Run /create-ui 20 times, measure check-hooks duration, assert <500ms for 19+ runs"

    - id: "NFR-P2"
      category: "Performance"
      requirement: "Total Phase N overhead adds <2 seconds to command execution time"
      metric: "Measured via before/after comparison with hooks enabled but skip_all:true"
      test_requirement: "Test: Compare /create-ui execution time with hooks disabled vs skip_all:true, assert difference <2s"

    - id: "NFR-R1"
      category: "Reliability"
      requirement: "Command must maintain 100% success rate regardless of hook system state"
      metric: "UI specs created successfully even if hooks fail (exit code 0 regardless)"
      test_requirement: "Test: Simulate 5 hook failure scenarios, verify command returns exit code 0 with UI specs created in all cases"

    - id: "NFR-U1"
      category: "Usability"
      requirement: "Feedback invocation messaging must be clear and non-intrusive"
      metric: "Message format: 'Launching feedback conversation... You can skip questions if needed'"
      test_requirement: "Test: Capture command output when hooks invoked, verify message matches format"
```

## UI Specification

Not applicable - This is a command-line interface modification with no graphical UI components.

## Edge Cases

- **Hook CLI not installed:** Command logs warning "DevForgeAI CLI not found, skipping feedback. Install with: pip install --break-system-packages -e .claude/scripts/", continues with UI generation completion

- **Config file missing/invalid:** check-hooks returns error, command treats as ineligible, logs "Feedback config invalid", completes normally

- **Feedback conversation crashes:** invoke-hooks returns non-zero exit, command logs error, user still gets UI specs (feedback failure doesn't lose work)

- **User cancels feedback mid-conversation:** Hook system handles gracefully (partial responses saved), command already completed UI generation

- **Multiple UI components generated:** operation_metadata includes count and list of all components, feedback questions acknowledge batch generation context

## Non-Functional Requirements

- **NFR-P1 (Performance):** Hook eligibility check completes in <500ms (fast Python validation, no heavy processing)

- **NFR-P2 (Performance):** Total overhead from Phase N (check + invoke if eligible) adds <2 seconds to /create-ui execution time (minimal user-perceivable delay)

- **NFR-R1 (Reliability):** Hook failures have 0% impact on /create-ui success rate (all failures caught, logged, workflow continues)

- **NFR-U1 (Usability):** Feedback invocation messaging is clear ("Launching feedback conversation... You can skip questions if needed") and non-intrusive

## Dependencies

### Prerequisites
- **STORY-021:** devforgeai check-hooks CLI command must be implemented and tested
- **STORY-022:** devforgeai invoke-hooks CLI command must be implemented and tested
- **STORY-023:** /dev pilot integration completed and pattern validated

### Dependent Stories
- **STORY-033:** /audit-deferrals command integration (last command in Feature 6.2)

## Definition of Done

### Implementation
- [ ] Phase N added to .claude/commands/create-ui.md after Phase 6 (Documentation)
- [ ] Bash code block with check-hooks call implemented
- [ ] Conditional invoke-hooks call implemented (exit code 0 check)
- [ ] UI context passed to hooks (ui_type, technology, styling, component list)
- [ ] Error handling with graceful degradation implemented
- [ ] User-friendly messaging for feedback invocation
- [ ] Warning messages for hook failures (<50 words, non-alarming)
- [ ] Pattern matches /dev pilot (STORY-023) for consistency

### Quality
- [ ] Unit tests: Hook check logic verified (5+ test cases)
- [ ] Integration tests: Full command flow with hooks enabled/disabled (10+ scenarios including context passing)
- [ ] Edge case tests: All 5 edge cases covered
- [ ] Performance test: Hook check <500ms (20 runs measured)
- [ ] Performance test: Total overhead <2s (10 runs measured)
- [ ] Reliability test: Command succeeds with hooks failing (5 failure scenarios)
- [ ] Context passing test: Verify all 4 metadata fields included
- [ ] Code review: Pattern consistency verified against STORY-023

### Testing
- [ ] Test Case 1: UI generation complete (React web), check-hooks returns 0 → invoke-hooks called with context
- [ ] Test Case 2: UI generation complete, check-hooks returns 1 → invoke-hooks skipped
- [ ] Test Case 3: CLI missing → warning logged, command succeeds, specs created
- [ ] Test Case 4: Config invalid → warning logged, command succeeds
- [ ] Test Case 5: Hook crashes → error logged, command succeeds
- [ ] Test Case 6: User cancels feedback → partial save, command already complete
- [ ] Test Case 7: Multiple components (3) → context includes all 3
- [ ] Test Case 8: Measure overhead with skip_all:true → <2s total
- [ ] Test Case 9: Technology context → verify "technology: React" in hook metadata
- [ ] Test Case 10: Compare Phase N with /dev → pattern match confirmed

### Documentation
- [ ] Command integration documented in `.claude/commands/create-ui.md`
- [ ] Pattern documented in `.devforgeai/protocols/hook-integration-pattern.md`
- [ ] UI context passing format documented
- [ ] User guide updated with /create-ui feedback capability
- [ ] Troubleshooting section added for hook failures

## Acceptance Sign-Off

- [ ] Product Owner: Story meets acceptance criteria
- [ ] Tech Lead: Implementation follows pilot pattern (STORY-023)
- [ ] QA Lead: All tests pass, no regressions
- [ ] User Testing: 3+ users validate hook experience with UI generation workflows

---

**Related Documents:**
- Epic: `.ai_docs/Epics/EPIC-006-feedback-integration-completion.epic.md`
- Sprint: `.ai_docs/Sprints/Sprint-3.md`
- Pilot Story: `.ai_docs/Stories/STORY-023-wire-hooks-into-dev-command-pilot.story.md`
- Hook Infrastructure: `STORY-021`, `STORY-022`
