---
id: STORY-471
title: /my-business Aggregated Dashboard
type: feature
epic: EPIC-072
sprint: Sprint-17
status: Dev Complete
points: 3
depends_on: ["STORY-470"]
priority: Low
advisory: false
source_gap: null
source_story: null
assigned_to: DevForgeAI AI Agent
created: 2026-02-21
format_version: "2.9"
---

# Story: /my-business Aggregated Dashboard

## Description

**As a** user,
**I want** one command (`/my-business`) that shows my progress across all business skill areas including profile summary, streak count, emotional trend, completed milestones, current milestone, and next task,
**so that** I can see my overall business journey at a glance without running multiple commands.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-011" section="blue-sky-vision">
    <quote>"A developer finishes building their app in DevForgeAI and types /my-business. The AI says: 'Based on your project, here's what I see as a business opportunity. Let's explore it together.'"</quote>
    <line_reference>lines 163-164</line_reference>
    <quantified_impact>Single entry point to entire business coaching system — the "home screen" for entrepreneurship</quantified_impact>
  </origin>

  <decision rationale="thin-command-over-orchestrator-skill">
    <selected>Thin command that reads and aggregates artifacts — no heavy logic</selected>
    <rejected alternative="full-orchestrator-skill">Risk of exceeding 500-line command limit; extract to skill only if needed</rejected>
    <trade_off>Simple but potentially limited aggregation vs. rich but complex orchestration</trade_off>
  </decision>
</provenance>
```

## Acceptance Criteria

### AC#1: /my-business Command Structure

```xml
<acceptance_criteria id="AC1" implements="COMP-001">
  <given>The DevForgeAI framework commands directory exists</given>
  <when>The /my-business command is created</when>
  <then>my-business.md exists at src/claude/commands/my-business.md with valid YAML frontmatter (description, argument-hint), is under 500 lines, and reads all business artifacts from devforgeai/specs/business/</then>
  <verification>
    <source_files>
      <file hint="Dashboard command">src/claude/commands/my-business.md</file>
    </source_files>
    <test_file>tests/STORY-471/test_ac1_my_business_command.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#2: /coach-me Command Structure

```xml
<acceptance_criteria id="AC2" implements="COMP-002">
  <given>The coaching-entrepreneur skill exists</given>
  <when>The /coach-me command is created</when>
  <then>coach-me.md exists at src/claude/commands/coach-me.md with valid YAML frontmatter, is under 500 lines, and invokes the coaching-entrepreneur skill via Skill() call</then>
  <verification>
    <source_files>
      <file hint="Coach command">src/claude/commands/coach-me.md</file>
    </source_files>
    <test_file>tests/STORY-471/test_ac2_coach_me_command.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#3: Aggregated Dashboard Display

```xml
<acceptance_criteria id="AC3" implements="COMP-001">
  <given>Business artifacts exist (user-profile.yaml, session-log.yaml, streak-tracker.yaml)</given>
  <when>The user runs /my-business</when>
  <then>The command displays an ASCII dashboard showing: (1) profile summary with adaptation level, (2) streak count with fire emoji, (3) completed milestones with checkmarks, (4) current milestone in progress, (5) next recommended task with estimated time, (6) an encouraging quote based on progress</then>
  <verification>
    <source_files>
      <file hint="Dashboard rendering logic">src/claude/commands/my-business.md</file>
    </source_files>
    <test_file>tests/STORY-471/test_ac3_dashboard_display.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#4: Graceful Empty State

```xml
<acceptance_criteria id="AC4">
  <given>No business artifacts exist (user has never run /assess-me)</given>
  <when>The user runs /my-business</when>
  <then>The command displays a welcome message guiding the user to start with /assess-me, rather than showing an error or empty dashboard</then>
  <verification>
    <source_files>
      <file hint="Empty state handling">src/claude/commands/my-business.md</file>
    </source_files>
    <test_file>tests/STORY-471/test_ac4_empty_state.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "my-business command"
      file_path: "src/claude/commands/my-business.md"
      required_keys:
        - key: "description"
          type: "string"
          required: true
          validation: "Describes business dashboard purpose"
          test_requirement: "Test: Verify description field present"
        - key: "argument-hint"
          type: "string"
          required: true
          example: "[--summary | --detail]"
          test_requirement: "Test: Verify argument-hint present"

    - type: "Configuration"
      name: "coach-me command"
      file_path: "src/claude/commands/coach-me.md"
      required_keys:
        - key: "description"
          type: "string"
          required: true
          validation: "Describes coaching session purpose"
          test_requirement: "Test: Verify description field present"
        - key: "argument-hint"
          type: "string"
          required: true
          test_requirement: "Test: Verify argument-hint present"

  business_rules:
    - id: "BR-001"
      rule: "/my-business reads all business artifacts but NEVER writes to them"
      trigger: "Command execution"
      validation: "No Write() or Edit() calls in command"
      error_handling: "Read-only aggregation"
      test_requirement: "Test: Verify no write instructions in my-business.md"
      priority: "High"

    - id: "BR-002"
      rule: "Empty state shows onboarding guidance, not errors"
      trigger: "No business artifacts found"
      validation: "Welcome message displayed with /assess-me CTA"
      error_handling: "Graceful empty state"
      test_requirement: "Test: Verify empty state guidance documented"
      priority: "High"

    - id: "BR-003"
      rule: "/coach-me is a thin invoker delegating to coaching-entrepreneur skill"
      trigger: "Command invocation"
      validation: "Contains Skill(command='coaching-entrepreneur') call"
      error_handling: "Skill handles all coaching logic"
      test_requirement: "Test: Verify Skill() invocation present in coach-me.md"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Both commands under 500 lines"
      metric: "Line count < 500 per command"
      test_requirement: "Test: wc -l for each command < 500"
      priority: "High"

    - id: "NFR-002"
      category: "Compatibility"
      requirement: "Dashboard renders in ASCII only"
      metric: "Zero GUI dependencies"
      test_requirement: "Test: Verify ASCII-only rendering patterns"
      priority: "High"
```

## Technical Limitations

```yaml
technical_limitations: []
```

## Non-Functional Requirements

### Performance
- **Command size:** Both commands < 500 lines
- **Dashboard load:** Reads YAML files only; no heavy processing

### Compatibility
- **Terminal only:** ASCII rendering for all dashboard elements

## Dependencies

### Prerequisite Stories
- [ ] **STORY-470:** Terminal-Compatible Gamification
  - **Why:** Dashboard displays gamification elements (streak, progress bars)
  - **Status:** Backlog

## Test Strategy

### Unit Tests
**Coverage Target:** 95%+
1. **Happy Path:** Commands exist, have valid frontmatter, under 500 lines
2. **Edge Cases:** No artifacts exist (empty state), partial artifacts
3. **Error Cases:** Commands exceed 500 lines, missing skill invocation

## Acceptance Criteria Verification Checklist

### AC#1: /my-business Command
- [x] Command file exists at correct path - **Phase:** 2
- [x] Valid YAML frontmatter - **Phase:** 2
- [x] Under 500 lines - **Phase:** 3
- [x] Reads business artifacts - **Phase:** 3

### AC#2: /coach-me Command
- [x] Command file exists at correct path - **Phase:** 2
- [x] Valid YAML frontmatter - **Phase:** 2
- [x] Invokes coaching-entrepreneur skill - **Phase:** 3
- [x] Under 500 lines - **Phase:** 3

### AC#3: Dashboard Display
- [x] ASCII dashboard pattern documented - **Phase:** 3
- [x] Shows 6 required elements - **Phase:** 3

### AC#4: Empty State
- [x] Welcome message documented - **Phase:** 3
- [x] /assess-me CTA present - **Phase:** 3

---

**Checklist Progress:** 12/12 items complete (100%)

---

## Definition of Done

### Implementation
- [x] my-business.md command created as read-only dashboard
- [x] coach-me.md command created as thin skill invoker
- [x] ASCII dashboard pattern documented with 6 display elements
- [x] Empty state handling with onboarding guidance
- [x] All files in src/ tree

### Quality
- [x] All 4 acceptance criteria have passing tests
- [x] Both commands < 500 lines
- [x] /my-business is read-only (no writes)
- [x] /coach-me delegates to skill correctly

### Testing
- [x] Unit tests for my-business command (test_ac1)
- [x] Unit tests for coach-me command (test_ac2)
- [x] Unit tests for dashboard display (test_ac3)
- [x] Unit tests for empty state (test_ac4)

### Documentation
- [x] Dashboard layout documented with ASCII example
- [x] Empty state message documented

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-03-04

- [x] my-business.md command created as read-only dashboard - Completed: Created src/claude/commands/my-business.md (113 lines) with Read()-only artifact aggregation
- [x] coach-me.md command created as thin skill invoker - Completed: Created src/claude/commands/coach-me.md (29 lines) with Skill(command="coaching-entrepreneur") delegation
- [x] ASCII dashboard pattern documented with 6 display elements - Completed: Dashboard renders profile/adaptation, streak, completed milestones, current milestone, next task, encouraging quote
- [x] Empty state handling with onboarding guidance - Completed: Welcome message guides user to /assess-me when no business artifacts exist
- [x] All files in src/ tree - Completed: Both files at src/claude/commands/
- [x] All 4 acceptance criteria have passing tests - Completed: 26/26 tests pass across 4 test files
- [x] Both commands < 500 lines - Completed: my-business.md=113 lines, coach-me.md=29 lines
- [x] /my-business is read-only (no writes) - Completed: Verified no Write() or Edit() calls present
- [x] /coach-me delegates to skill correctly - Completed: Skill(command="coaching-entrepreneur", args="$ARGUMENTS")
- [x] Unit tests for my-business command (test_ac1) - Completed: 8 tests covering existence, frontmatter, line count, read-only, artifact paths
- [x] Unit tests for coach-me command (test_ac2) - Completed: 5 tests covering existence, frontmatter, line count, skill invocation
- [x] Unit tests for dashboard display (test_ac3) - Completed: 7 tests covering 6 dashboard elements + ASCII rendering
- [x] Unit tests for empty state (test_ac4) - Completed: 4 tests covering empty state, /assess-me CTA, welcome message, no-error
- [x] Dashboard layout documented with ASCII example - Completed: ASCII dashboard template in my-business.md with box-drawing characters
- [x] Empty state message documented - Completed: Welcome message and /assess-me guidance in my-business.md Step 2

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| 01 Pre-Flight | Complete | Git validated, 6 context files loaded, tech-stack detected |
| 02 Red | Complete | 26 tests written, all FAIL (4 FAILED + 22 ERROR) |
| 03 Green | Complete | 2 command files created, 26/26 tests PASS |
| 04 Refactor | Complete | No changes needed, code reviewer approved |
| 4.5 AC Verify | Complete | 4/4 ACs PASS with HIGH confidence |
| 05 Integration | Complete | 26 + 148 related tests PASS, no regressions |
| 5.5 AC Verify | Complete | 4/4 ACs PASS with HIGH confidence |
| 06 Deferral | Complete | No deferrals |
| 07 DoD Update | Complete | All 15 DoD items marked [x] |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/commands/my-business.md | Created | 113 |
| src/claude/commands/coach-me.md | Created | 29 |
| tests/STORY-471/test_ac1_my_business_command.py | Created | 131 |
| tests/STORY-471/test_ac2_coach_me_command.py | Created | 112 |
| tests/STORY-471/test_ac3_dashboard_display.py | Created | 103 |
| tests/STORY-471/test_ac4_empty_state.py | Created | 65 |

---

## Change Log

**Current Status:** Dev Complete

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-21 | .claude/story-requirements-analyst | Created | Story created from EPIC-072 Feature 7 | STORY-471.story.md |

## Notes

**Source Requirements:** FR-007
**Design Decisions:**
- /my-business is read-only aggregator — if complexity grows, extract to a `summarizing-business` skill
- /coach-me follows lean orchestration: validate args → invoke skill → done
- Dashboard shows encouraging quote based on progress level — context-specific, not generic
- Empty state is an onboarding moment, not an error state

**ASCII Dashboard Example:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Business Journey Dashboard
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Profile: ADHD-adapted (micro-tasks)
  ████████████░░░░░░░░  60% Complete

  ✅ Problem validated
  ✅ Customer segments defined
  ✅ Value proposition drafted
  🔄 Revenue model (IN PROGRESS)
  ⬜ Go-to-market strategy

  🔥 Streak: 5 sessions
  ⏱️  Next task: ~10 min

  💡 "You've made more progress than most
     people who think about starting a
     business. That's real momentum."
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

Story Template Version: 2.9
Last Updated: 2026-02-21
