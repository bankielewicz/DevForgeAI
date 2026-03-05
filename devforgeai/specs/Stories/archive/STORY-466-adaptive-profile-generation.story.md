---
id: STORY-466
title: Adaptive Profile Generation
type: feature
epic: EPIC-072
sprint: Sprint-15
status: QA Approved
points: 3
depends_on: ["STORY-465"]
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: DevForgeAI AI Agent
created: 2026-02-21
format_version: "2.9"
---

# Story: Adaptive Profile Generation

## Description

**As a** user with ADHD or executive dysfunction challenges,
**I want** the AI to automatically generate an adaptive profile that calibrates task chunk size, session length, check-in frequency, progress visualization, celebration intensity, reminder style, and overwhelm prevention based on my assessment,
**so that** business coaching tasks feel manageable and adapted to my cognitive style.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-011" section="adhd-adaptation-system">
    <quote>"Based on assessment, the system calibrates 7 dimensions: task chunk size, session length, check-in frequency, progress visualization, celebration intensity, reminder style, and overwhelm prevention"</quote>
    <line_reference>lines 246-258</line_reference>
    <quantified_impact>Every subsequent business skill reads this profile to adapt its behavior</quantified_impact>
  </origin>

  <decision rationale="yaml-persistence-over-in-memory">
    <selected>Persist profile to devforgeai/specs/business/user-profile.yaml for cross-session survival</selected>
    <rejected alternative="in-memory-only">Profile lost between sessions; users would need to re-assess every time</rejected>
    <trade_off>File I/O on every coaching session read vs. zero persistence</trade_off>
  </decision>

  <hypothesis id="H3" validation="User satisfaction + completion rates" success_criteria="40%+ milestone completion rate">
    IF we use milestone-based plans instead of calendar-based, THEN neurodivergent users complete more milestones
  </hypothesis>
</provenance>
```

## Acceptance Criteria

### AC#1: Seven-Dimension Profile Generation

```xml
<acceptance_criteria id="AC1" implements="COMP-001">
  <given>A user has completed the 6-dimension assessment questionnaire from STORY-465</given>
  <when>The profile synthesis phase executes in the assessing-entrepreneur skill</when>
  <then>An adaptive profile is generated with calibration levels for all 7 dimensions: task chunk size (5-60 min range), session length (15-60 min range), check-in frequency (every 1-5 tasks), progress visualization (per-task to weekly), celebration intensity (every-completion to milestone-only), reminder style (specific-next-action to gentle-nudge), and overwhelm prevention (next-3-tasks-only to full-roadmap)</then>
  <verification>
    <source_files>
      <file hint="Profile synthesis phase">src/claude/skills/assessing-entrepreneur/SKILL.md</file>
      <file hint="Calibration engine">src/claude/skills/assessing-entrepreneur/references/plan-calibration-engine.md</file>
    </source_files>
    <test_file>tests/STORY-466/test_ac1_profile_dimensions.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#2: Profile YAML Persistence

```xml
<acceptance_criteria id="AC2" implements="COMP-002">
  <given>The adaptive profile has been generated</given>
  <when>The profile is persisted</when>
  <then>The profile is written to devforgeai/specs/business/user-profile.yaml in valid YAML format with all 7 dimension values, a timestamp, and a schema version field</then>
  <verification>
    <source_files>
      <file hint="Profile output specification">src/claude/skills/assessing-entrepreneur/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-466/test_ac2_profile_persistence.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#3: /assess-me Command

```xml
<acceptance_criteria id="AC3" implements="COMP-003">
  <given>The DevForgeAI framework commands directory exists</given>
  <when>The /assess-me command is created</when>
  <then>assess-me.md exists at src/claude/commands/assess-me.md with valid YAML frontmatter (description, argument-hint), is under 500 lines, and invokes the assessing-entrepreneur skill via Skill() call</then>
  <verification>
    <source_files>
      <file hint="Command file">src/claude/commands/assess-me.md</file>
    </source_files>
    <test_file>tests/STORY-466/test_ac3_assess_me_command.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#4: Recalibration Support

```xml
<acceptance_criteria id="AC4">
  <given>A user has an existing adaptive profile</given>
  <when>The user invokes /assess-me --recalibrate</when>
  <then>The command supports a recalibrate argument that re-runs the assessment and overwrites the existing profile while preserving coaching session history</then>
  <verification>
    <source_files>
      <file hint="Command with argument handling">src/claude/commands/assess-me.md</file>
    </source_files>
    <test_file>tests/STORY-466/test_ac4_recalibration.py</test_file>
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
      name: "assess-me command"
      file_path: "src/claude/commands/assess-me.md"
      required_keys:
        - key: "description"
          type: "string"
          required: true
          validation: "Describes assessment purpose"
          test_requirement: "Test: Verify description field present"
        - key: "argument-hint"
          type: "string"
          required: true
          example: "[--recalibrate]"
          validation: "Contains recalibrate option"
          test_requirement: "Test: Verify argument-hint includes recalibrate"

    - type: "DataModel"
      name: "UserProfile"
      table: "devforgeai/specs/business/user-profile.yaml"
      purpose: "Stores adaptive coaching profile calibrated from assessment"
      fields:
        - name: "schema_version"
          type: "String"
          constraints: "Required"
          description: "Profile schema version for future migrations"
          test_requirement: "Test: Verify schema_version field exists"
        - name: "created"
          type: "DateTime"
          constraints: "Required"
          description: "When profile was first created"
          test_requirement: "Test: Verify created timestamp present"
        - name: "last_calibrated"
          type: "DateTime"
          constraints: "Required"
          description: "When profile was last calibrated/recalibrated"
          test_requirement: "Test: Verify last_calibrated timestamp present"
        - name: "task_chunk_size"
          type: "String"
          constraints: "Required, Enum: micro|standard|extended"
          description: "Preferred task duration: micro (5-15min), standard (30-60min), extended (60+min)"
          test_requirement: "Test: Verify valid enum value"
        - name: "session_length"
          type: "String"
          constraints: "Required, Enum: short|medium|long"
          description: "Preferred session length: short (15-25min), medium (30-45min), long (45-60min)"
          test_requirement: "Test: Verify valid enum value"
        - name: "check_in_frequency"
          type: "String"
          constraints: "Required, Enum: frequent|moderate|minimal"
          description: "How often to check in: frequent (every 1-2 tasks), moderate (every 3-5 tasks), minimal (milestone only)"
          test_requirement: "Test: Verify valid enum value"
        - name: "progress_visualization"
          type: "String"
          constraints: "Required, Enum: per_task|daily|weekly"
          description: "When to show progress: per_task, daily, weekly"
          test_requirement: "Test: Verify valid enum value"
        - name: "celebration_intensity"
          type: "String"
          constraints: "Required, Enum: high|medium|low"
          description: "How much to celebrate: high (every completion), medium (significant tasks), low (milestones only)"
          test_requirement: "Test: Verify valid enum value"
        - name: "reminder_style"
          type: "String"
          constraints: "Required, Enum: specific|balanced|gentle"
          description: "Reminder approach: specific (next action + time), balanced (what's next), gentle (nudge)"
          test_requirement: "Test: Verify valid enum value"
        - name: "overwhelm_prevention"
          type: "String"
          constraints: "Required, Enum: strict|moderate|open"
          description: "Task visibility: strict (next 3 only), moderate (current milestone), open (full roadmap)"
          test_requirement: "Test: Verify valid enum value"

  business_rules:
    - id: "BR-001"
      rule: "Assessment skill is sole writer of user-profile.yaml"
      trigger: "Any write to user-profile.yaml"
      validation: "Only assessing-entrepreneur skill writes; coaching skill reads only"
      error_handling: "Coaching skill must not modify profile"
      test_requirement: "Test: Verify coaching skill references profile as read-only"
      priority: "Critical"

    - id: "BR-002"
      rule: "Recalibration preserves coaching history"
      trigger: "/assess-me --recalibrate"
      validation: "Coaching session log not modified during recalibration"
      error_handling: "Only user-profile.yaml is overwritten"
      test_requirement: "Test: Verify recalibrate flow references profile only, not session log"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Command under 500 lines"
      metric: "Line count < 500"
      test_requirement: "Test: wc -l assess-me.md < 500"
      priority: "High"
```

## Technical Limitations

```yaml
technical_limitations: []
```

## Non-Functional Requirements

### Performance
- **Command size:** assess-me.md < 500 lines (lean orchestration)

### Reliability
- **Profile survival:** YAML file persists across Claude Code sessions
- **Recalibration safety:** Overwrites profile only, preserves all other business artifacts

## Dependencies

### Prerequisite Stories
- [ ] **STORY-465:** Guided Self-Assessment Skill
  - **Why:** Profile generation requires the assessment questionnaire and subagent
  - **Status:** Backlog

### Technology Dependencies
- None (Markdown + YAML only)

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Profile YAML schema contains all 7 dimensions with valid enum values
2. **Edge Cases:**
   - Profile missing a dimension
   - Invalid enum value in dimension
3. **Error Cases:**
   - assess-me.md missing frontmatter
   - Command exceeds 500 lines

## Acceptance Criteria Verification Checklist

### AC#1: Seven-Dimension Profile Generation
- [x] Profile synthesis phase documented in SKILL.md - **Phase:** 3 - **Evidence:** tests/STORY-466/test_ac1_profile_dimensions.py
- [x] All 7 dimensions specified with ranges - **Phase:** 3 - **Evidence:** tests/STORY-466/test_ac1_profile_dimensions.py
- [x] Calibration engine reference file created - **Phase:** 3 - **Evidence:** tests/STORY-466/test_ac1_profile_dimensions.py

### AC#2: Profile YAML Persistence
- [x] user-profile.yaml schema documented - **Phase:** 3 - **Evidence:** tests/STORY-466/test_ac2_profile_persistence.py
- [x] Schema version field included - **Phase:** 3 - **Evidence:** tests/STORY-466/test_ac2_profile_persistence.py
- [x] Timestamps included - **Phase:** 3 - **Evidence:** tests/STORY-466/test_ac2_profile_persistence.py

### AC#3: /assess-me Command
- [x] Command file exists at correct path - **Phase:** 2 - **Evidence:** tests/STORY-466/test_ac3_assess_me_command.py
- [x] Valid YAML frontmatter - **Phase:** 2 - **Evidence:** tests/STORY-466/test_ac3_assess_me_command.py
- [x] Invokes assessing-entrepreneur skill - **Phase:** 3 - **Evidence:** tests/STORY-466/test_ac3_assess_me_command.py
- [x] Under 500 lines - **Phase:** 3 - **Evidence:** tests/STORY-466/test_ac3_assess_me_command.py

### AC#4: Recalibration Support
- [x] --recalibrate argument documented - **Phase:** 3 - **Evidence:** tests/STORY-466/test_ac4_recalibration.py
- [x] Overwrites profile, preserves history - **Phase:** 3 - **Evidence:** tests/STORY-466/test_ac4_recalibration.py

---

**Checklist Progress:** 12/12 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Profile synthesis phase added to assessing-entrepreneur SKILL.md
- [x] user-profile.yaml schema documented with all 7 dimensions
- [x] assess-me.md command created with skill invocation and recalibrate support
- [x] plan-calibration-engine.md reference file contains calibration logic

### Quality
- [x] All 4 acceptance criteria have passing tests
- [x] Profile schema validates all 7 dimensions
- [x] Command < 500 lines

### Testing
- [x] Unit tests for profile dimensions (test_ac1_profile_dimensions.py)
- [x] Unit tests for YAML persistence (test_ac2_profile_persistence.py)
- [x] Unit tests for command structure (test_ac3_assess_me_command.py)
- [x] Unit tests for recalibration (test_ac4_recalibration.py)

### Documentation
- [x] Profile YAML schema documented in calibration engine reference
- [x] Command argument-hint documents --recalibrate option

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-22

- [x] Profile synthesis phase added to assessing-entrepreneur SKILL.md - Completed: Added Profile Synthesis Output section with 7-dimension table, ranges, and YAML schema
- [x] user-profile.yaml schema documented with all 7 dimensions - Completed: Schema includes schema_version, created, last_calibrated, and all 7 dimension fields with enum values
- [x] assess-me.md command created with skill invocation and recalibrate support - Completed: Created 51-line command with YAML frontmatter, Skill() invocation, and --recalibrate flow
- [x] plan-calibration-engine.md reference file contains calibration logic - Completed: Added Seven-Dimension Adaptive Calibration section with enum mappings
- [x] All 4 acceptance criteria have passing tests - Completed: 46 tests across 4 test files all passing
- [x] Profile schema validates all 7 dimensions - Completed: task_chunk_size, session_length, check_in_frequency, progress_visualization, celebration_intensity, reminder_style, overwhelm_prevention
- [x] Command < 500 lines - Completed: assess-me.md is 51 lines
- [x] Unit tests for profile dimensions (test_ac1_profile_dimensions.py) - Completed: 15 tests verifying SKILL.md and calibration engine
- [x] Unit tests for YAML persistence (test_ac2_profile_persistence.py) - Completed: 14 tests verifying schema fields and enum values
- [x] Unit tests for command structure (test_ac3_assess_me_command.py) - Completed: 9 tests verifying frontmatter, line count, skill invocation
- [x] Unit tests for recalibration (test_ac4_recalibration.py) - Completed: 8 tests verifying --recalibrate arg, overwrite, history preservation
- [x] Profile YAML schema documented in calibration engine reference - Completed: Seven-Dimension Adaptive Calibration section in plan-calibration-engine.md
- [x] Command argument-hint documents --recalibrate option - Completed: argument-hint field contains "[--recalibrate]"

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Phase 02 (Red) | ✅ Complete | 42 failing tests, 4 passing |
| Phase 03 (Green) | ✅ Complete | 46 passing tests |
| Phase 04 (Refactor) | ✅ Complete | No refactoring needed |
| Phase 04.5 (AC Verify) | ✅ Complete | 4/4 ACs PASS |
| Phase 05 (Integration) | ✅ Complete | All integration points validated |
| Phase 05.5 (AC Verify) | ✅ Complete | 4/4 ACs PASS |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/assessing-entrepreneur/SKILL.md | Modified | ~231 |
| src/claude/skills/assessing-entrepreneur/references/plan-calibration-engine.md | Modified | ~153 |
| src/claude/commands/assess-me.md | Created | 51 |
| tests/STORY-466/__init__.py | Created | 0 |
| tests/STORY-466/test_ac1_profile_dimensions.py | Created | 190 |
| tests/STORY-466/test_ac2_profile_persistence.py | Created | 176 |
| tests/STORY-466/test_ac3_assess_me_command.py | Created | 160 |
| tests/STORY-466/test_ac4_recalibration.py | Created | 162 |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-21 | .claude/story-requirements-analyst | Created | Story created from EPIC-072 Feature 2 | STORY-466.story.md |
| 2026-02-23 | .claude/qa-result-interpreter | QA Deep | PASSED: 46 tests, 0 violations, 100% traceability | STORY-466-qa-report.md |
| 2026-03-04 | DevForgeAI AI Agent | Documentation | Updated 6 module docs via /document --type=all (merge) | docs/assessing-entrepreneur-README.md, docs/api/assessing-entrepreneur-API.md, docs/architecture/assessing-entrepreneur-ARCHITECTURE.md, docs/guides/assessing-entrepreneur-DEVELOPER-GUIDE.md, docs/guides/assessing-entrepreneur-TROUBLESHOOTING.md, docs/guides/assessing-entrepreneur-ROADMAP.md |

## Notes

**Design Decisions:**
- YAML persistence chosen over JSON for consistency with DevForgeAI framework standards
- Enum values for dimensions (micro/standard/extended etc.) provide bounded options rather than numeric scales
- Assessment skill is sole writer — prevents data coordination bugs between skills

**Source Requirements:**
- FR-002 from business-skills-framework-requirements.md

---

Story Template Version: 2.9
Last Updated: 2026-02-21
