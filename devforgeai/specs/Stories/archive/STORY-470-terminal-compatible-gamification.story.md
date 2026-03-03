---
id: STORY-470
title: Terminal-Compatible Gamification
type: feature
epic: EPIC-072
sprint: Sprint-17
status: Ready for Dev
points: 3
depends_on: ["STORY-467"]
priority: Low
advisory: false
source_gap: null
source_story: null
assigned_to: DevForgeAI AI Agent
created: 2026-02-21
format_version: "2.9"
---

# Story: Terminal-Compatible Gamification

## Description

**As an** ADHD user,
**I want** to see visible progress through ASCII progress bars, streak tracking, and milestone celebrations after each completed task,
**so that** I get dopamine rewards that motivate continued action toward my business goals.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-011" section="adhd-adaptation-system">
    <quote>"ADHD UX: All three combined (chunk sizing + pacing + visual progress) — terminal-compatible"</quote>
    <line_reference>User Decision 10</line_reference>
    <quantified_impact>Gamification is the primary motivation mechanism for ADHD users — without it, session return rates drop</quantified_impact>
  </origin>

  <hypothesis id="H5" validation="User engagement metrics" success_criteria="Session return rate >60%">
    IF we use terminal-only ASCII UX for gamification, THEN engagement is sufficient
  </hypothesis>
</provenance>
```

## Acceptance Criteria

### AC#1: ASCII Progress Bar Rendering

```xml
<acceptance_criteria id="AC1" implements="COMP-001">
  <given>A user has completed some business milestones</given>
  <when>Progress is displayed</when>
  <then>An ASCII progress bar renders correctly in Claude Code Terminal showing completion percentage (e.g., "████████████░░░░░░░░ 60% Complete") using only ASCII-safe characters</then>
  <verification>
    <source_files>
      <file hint="Celebration engine reference">src/claude/skills/coaching-entrepreneur/references/celebration-engine.md</file>
    </source_files>
    <test_file>tests/STORY-470/test_ac1_ascii_progress.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#2: Streak Tracking

```xml
<acceptance_criteria id="AC2" implements="COMP-002">
  <given>A user completes coaching sessions on consecutive opportunities</given>
  <when>The streak is tracked</when>
  <then>A streak counter is maintained in devforgeai/specs/business/coaching/streak-tracker.yaml showing consecutive sessions count, and the streak is displayed in coaching session summaries and the /my-business dashboard</then>
  <verification>
    <source_files>
      <file hint="Streak tracking data model">src/claude/skills/coaching-entrepreneur/references/celebration-engine.md</file>
    </source_files>
    <test_file>tests/STORY-470/test_ac2_streak_tracking.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#3: Celebration Engine

```xml
<acceptance_criteria id="AC3" implements="COMP-001,COMP-003">
  <given>A user completes a task or milestone</given>
  <when>The celebration engine fires</when>
  <then>The celebration intensity matches the user's profile setting (high: every completion gets acknowledgment with encouraging message; medium: significant tasks; low: milestones only) and celebration messages are specific to the achievement, not generic</then>
  <verification>
    <source_files>
      <file hint="Celebration engine">src/claude/skills/coaching-entrepreneur/references/celebration-engine.md</file>
    </source_files>
    <test_file>tests/STORY-470/test_ac3_celebration_engine.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#4: Profile-Driven Adaptation

```xml
<acceptance_criteria id="AC4">
  <given>A user profile exists with celebration_intensity and progress_visualization settings</given>
  <when>Gamification elements are rendered</when>
  <then>The gamification system respects the profile: high-adaptation users see progress after every task and frequent celebrations; low-adaptation users see weekly summaries and milestone-only celebrations</then>
  <verification>
    <source_files>
      <file hint="Coaching skill with profile integration">src/claude/skills/coaching-entrepreneur/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-470/test_ac4_profile_adaptation.py</test_file>
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
      name: "celebration-engine.md"
      file_path: "src/claude/skills/coaching-entrepreneur/references/celebration-engine.md"
      required_keys:
        - key: "ascii-progress-patterns"
          type: "section"
          required: true
          test_requirement: "Test: Verify ASCII progress bar pattern section exists"
        - key: "streak-tracking"
          type: "section"
          required: true
          test_requirement: "Test: Verify streak tracking section exists"
        - key: "celebration-tiers"
          type: "section"
          required: true
          test_requirement: "Test: Verify high/medium/low celebration tiers documented"

    - type: "DataModel"
      name: "StreakTracker"
      table: "devforgeai/specs/business/coaching/streak-tracker.yaml"
      purpose: "Tracks consecutive coaching session streaks for gamification"
      fields:
        - name: "current_streak"
          type: "Int"
          constraints: "Required, >= 0"
          description: "Number of consecutive sessions"
          test_requirement: "Test: Verify current_streak field in schema"
        - name: "longest_streak"
          type: "Int"
          constraints: "Required, >= 0"
          description: "All-time longest streak"
          test_requirement: "Test: Verify longest_streak field in schema"
        - name: "last_session_date"
          type: "DateTime"
          constraints: "Required"
          description: "Date of most recent session"
          test_requirement: "Test: Verify last_session_date field in schema"

  business_rules:
    - id: "BR-001"
      rule: "All visual elements must use ASCII-safe characters only"
      trigger: "Any progress or celebration rendering"
      validation: "No Unicode outside ASCII range; use block characters (█░) and standard symbols"
      error_handling: "Fallback to simple text if rendering fails"
      test_requirement: "Test: Verify ASCII patterns in celebration-engine.md use safe characters"
      priority: "High"

    - id: "BR-002"
      rule: "Celebration intensity matches user profile"
      trigger: "Task or milestone completion"
      validation: "Profile celebration_intensity dimension read before celebration"
      error_handling: "Default to medium if profile unavailable"
      test_requirement: "Test: Verify celebration tiers mapped to profile dimensions"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Compatibility"
      requirement: "All renders work in Claude Code Terminal"
      metric: "Zero GUI dependencies; ASCII-only"
      test_requirement: "Test: Verify no GUI-specific markup in celebration patterns"
      priority: "Critical"
```

## Technical Limitations

```yaml
technical_limitations: []
```

## Dependencies

### Prerequisite Stories
- [ ] **STORY-467:** Dynamic Persona Blend Engine
  - **Why:** Gamification extends the coaching skill; needs the skill to exist first
  - **Status:** Backlog

## Test Strategy

### Unit Tests
**Coverage Target:** 95%+
1. **Happy Path:** Celebration engine reference exists with required sections
2. **Edge Cases:** Zero milestones completed, streak of 1
3. **Error Cases:** Missing profile (fallback to medium)

## Acceptance Criteria Verification Checklist

### AC#1: ASCII Progress Bar
- [ ] Progress bar pattern documented - **Phase:** 3
- [ ] Uses ASCII-safe characters - **Phase:** 3

### AC#2: Streak Tracking
- [ ] Streak tracker YAML schema documented - **Phase:** 3
- [ ] Streak display in session summary - **Phase:** 3

### AC#3: Celebration Engine
- [ ] Three celebration tiers defined (high/medium/low) - **Phase:** 3
- [ ] Achievement-specific messages (not generic) - **Phase:** 3

### AC#4: Profile-Driven Adaptation
- [ ] Profile dimensions mapped to gamification behavior - **Phase:** 3
- [ ] Fallback for missing profile - **Phase:** 3

---

**Checklist Progress:** 0/8 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] celebration-engine.md created with ASCII patterns, streak tracking, and celebration tiers
- [ ] Streak tracker YAML schema documented
- [ ] Profile-driven adaptation logic documented in coaching skill
- [ ] All files in src/ tree

### Quality
- [ ] All 4 acceptance criteria have passing tests
- [ ] ASCII-only rendering verified
- [ ] Profile fallback tested

### Testing
- [ ] Unit tests for ASCII progress (test_ac1)
- [ ] Unit tests for streak tracking (test_ac2)
- [ ] Unit tests for celebration engine (test_ac3)
- [ ] Unit tests for profile adaptation (test_ac4)

### Documentation
- [ ] Celebration patterns are specific and encouraging (not patronizing)

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|

---

## Change Log

**Current Status:** Ready for Dev

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-21 | .claude/story-requirements-analyst | Created | Story created from EPIC-072 Feature 6 | STORY-470.story.md |

## Notes

**Source Requirements:** FR-006
**Design Decisions:**
- Unicode block characters (█░) are ASCII-safe enough for most terminals
- Streak resets after configurable gap (documented in celebration-engine.md)
- Celebrations are context-specific ("You just validated your first customer segment!") not generic ("Good job!")

---

Story Template Version: 2.9
Last Updated: 2026-02-21
