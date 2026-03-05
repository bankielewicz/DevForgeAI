---
id: STORY-468
title: Emotional State Tracking
type: feature
epic: EPIC-072
sprint: Sprint-16
status: QA Approved
points: 2
depends_on: ["STORY-467"]
priority: Medium
advisory: false
source_gap: null
source_story: null
assigned_to: DevForgeAI AI Agent
created: 2026-02-21
format_version: "2.9"
---

# Story: Emotional State Tracking

## Description

**As a** returning user,
**I want** the AI to remember my emotional state from my previous coaching session and adapt its opening tone accordingly,
**so that** each session feels personalized and responsive to my current needs.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-011" section="functional-requirements">
    <quote>"Emotional state tracking across sessions with tone adaptation for subsequent sessions"</quote>
    <line_reference>FR-004</line_reference>
    <quantified_impact>Increases session-to-session continuity and perceived empathy of coaching</quantified_impact>
  </origin>

  <decision rationale="self-reported-over-ai-inference">
    <selected>Self-reported emotional state only — user explicitly shares how they feel</selected>
    <rejected alternative="ai-inference">Ethical concern: AI should not infer mental/emotional state</rejected>
    <trade_off>Less data fidelity in exchange for ethical safety and user trust</trade_off>
  </decision>
</provenance>
```

## Acceptance Criteria

### AC#1: Session Log Persistence

```xml
<acceptance_criteria id="AC1" implements="COMP-001">
  <given>A coaching session completes</given>
  <when>The session state is persisted</when>
  <then>Emotional indicators are logged to devforgeai/specs/business/coaching/session-log.yaml including session date, self-reported emotional state, session outcomes, and any user overrides</then>
  <verification>
    <source_files>
      <file hint="Coaching skill session persistence">src/claude/skills/coaching-entrepreneur/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-468/test_ac1_session_log.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#2: Tone Adaptation on Session Start

```xml
<acceptance_criteria id="AC2" implements="COMP-001">
  <given>A previous coaching session exists in session-log.yaml with emotional state data</given>
  <when>A new coaching session begins</when>
  <then>The coaching skill reads the previous session state and adapts its opening tone (e.g., "Last session you seemed frustrated — let's start lighter today" or "You were on fire last time — ready to keep that momentum?")</then>
  <verification>
    <source_files>
      <file hint="Session start adaptation logic">src/claude/skills/coaching-entrepreneur/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-468/test_ac2_tone_adaptation.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#3: User Override Support

```xml
<acceptance_criteria id="AC3">
  <given>The AI adapts tone based on previous session state</given>
  <when>The user overrides the adaptation (e.g., "I'm feeling great today, let's push hard")</when>
  <then>The coaching skill respects the override immediately and logs the override in the session log for future reference</then>
  <verification>
    <source_files>
      <file hint="Override handling">src/claude/skills/coaching-entrepreneur/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-468/test_ac3_user_override.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "DataModel"
      name: "SessionLog"
      table: "devforgeai/specs/business/coaching/session-log.yaml"
      purpose: "Tracks coaching session emotional state and outcomes across sessions"
      fields:
        - name: "sessions"
          type: "Array"
          constraints: "Required"
          description: "Array of session entries"
          test_requirement: "Test: Verify sessions array structure documented"
        - name: "sessions[].date"
          type: "DateTime"
          constraints: "Required"
          description: "Session date"
          test_requirement: "Test: Verify date field in schema"
        - name: "sessions[].emotional_state"
          type: "String"
          constraints: "Required, Enum: energized|focused|neutral|tired|frustrated|anxious|overwhelmed"
          description: "Self-reported emotional state at session start"
          test_requirement: "Test: Verify enum values documented"
        - name: "sessions[].override"
          type: "String"
          constraints: "Optional"
          description: "User override of AI-suggested tone"
          test_requirement: "Test: Verify override field in schema"

  business_rules:
    - id: "BR-001"
      rule: "Emotional state is self-reported only — AI never infers emotional state"
      trigger: "Session start emotional check-in"
      validation: "AskUserQuestion used for emotional state collection"
      error_handling: "If user declines to report, default to 'neutral'"
      test_requirement: "Test: Verify AskUserQuestion pattern for emotional state"
      priority: "Critical"

    - id: "BR-002"
      rule: "User overrides are immediately respected"
      trigger: "User provides emotional state different from AI adaptation"
      validation: "Override logged and tone adjusted within same session"
      error_handling: "Log override, switch tone"
      test_requirement: "Test: Verify override handling documented in skill"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "Session log survives across Claude Code sessions"
      metric: "YAML file persists in devforgeai/specs/business/coaching/"
      test_requirement: "Test: Verify session log path documented correctly"
      priority: "High"
```

## Technical Limitations

```yaml
technical_limitations: []
```

## Dependencies

### Prerequisite Stories
- [ ] **STORY-467:** Dynamic Persona Blend Engine
  - **Why:** Emotional tracking extends the coaching skill created in STORY-467
  - **Status:** Backlog

## Test Strategy

### Unit Tests
**Coverage Target:** 95%+
1. **Happy Path:** Session log schema documented, tone adaptation logic present
2. **Edge Cases:** No previous session (first-time user), user declines emotional check-in
3. **Error Cases:** Malformed session log

## Acceptance Criteria Verification Checklist

### AC#1: Session Log Persistence
- [x] Session log schema documented in SKILL.md - **Phase:** 3
- [x] Emotional state enum values defined - **Phase:** 3
- [x] Session outcomes tracking defined - **Phase:** 3

### AC#2: Tone Adaptation
- [x] Previous session read logic documented - **Phase:** 3
- [x] Tone adaptation examples provided - **Phase:** 3

### AC#3: User Override
- [x] Override handling documented - **Phase:** 3
- [x] Override logging specified - **Phase:** 3

---

**Checklist Progress:** 7/7 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Session log schema added to coaching-entrepreneur skill
- [x] Tone adaptation on session start documented
- [x] User override handling documented
- [x] Session log YAML path specified (devforgeai/specs/business/coaching/session-log.yaml)

### Quality
- [x] All 3 acceptance criteria have passing tests
- [x] Self-reported only constraint verified (no AI inference)

### Testing
- [x] Unit tests for session log (test_ac1)
- [x] Unit tests for tone adaptation (test_ac2)
- [x] Unit tests for user override (test_ac3)

### Documentation
- [x] Session log YAML schema documented

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-03-05

- [x] Session log schema added to coaching-entrepreneur skill - Completed: Added Session Log section with schema table, emotional state enum (7 values), YAML path
- [x] Tone adaptation on session start documented - Completed: Added Tone Adaptation section with Read logic and 5 tone examples
- [x] User override handling documented - Completed: Added Override Handling section with 3-step process and logging specification
- [x] Session log YAML path specified (devforgeai/specs/business/coaching/session-log.yaml) - Completed: Path documented in Session Log section
- [x] All 3 acceptance criteria have passing tests - Completed: 12/12 tests passing across 3 test files
- [x] Self-reported only constraint verified (no AI inference) - Completed: BR-001 business rule documented
- [x] Unit tests for session log (test_ac1) - Completed: 6 tests in test_ac1_session_log.py
- [x] Unit tests for tone adaptation (test_ac2) - Completed: 3 tests in test_ac2_tone_adaptation.py
- [x] Unit tests for user override (test_ac3) - Completed: 3 tests in test_ac3_user_override.py
- [x] Session log YAML schema documented - Completed: Full schema table with field types and constraints

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Phase 02 (Red) | ✅ Complete | 12 failing tests created |
| Phase 03 (Green) | ✅ Complete | All 12 tests passing |
| Phase 04 (Refactor) | ✅ Complete | Code review approved, light QA passed |
| Phase 04.5 (AC Verify) | ✅ Complete | 3/3 ACs verified PASS |
| Phase 05 (Integration) | ✅ Complete | 24/24 integration checks passed |
| Phase 05.5 (AC Verify) | ✅ Complete | 3/3 ACs verified PASS |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/coaching-entrepreneur/SKILL.md | Modified | +60 lines (Emotional State Tracking sections) |
| tests/STORY-468/test_ac1_session_log.py | Created | 61 lines |
| tests/STORY-468/test_ac2_tone_adaptation.py | Created | 57 lines |
| tests/STORY-468/test_ac3_user_override.py | Created | 50 lines |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-21 | .claude/story-requirements-analyst | Created | Story created from EPIC-072 Feature 4 | STORY-468.story.md |
| 2026-03-04 | DevForgeAI AI Agent | Documentation | Updated 5 sections in framework docs via /document | docs/api/API.md, docs/architecture/ARCHITECTURE.md, docs/guides/DEVELOPER-GUIDE.md, docs/guides/TROUBLESHOOTING.md, docs/guides/ROADMAP.md |
| 2026-03-05 | .claude/qa-result-interpreter | QA Deep | PASSED: Coverage 100%, 5 violations (0 CRITICAL, 0 blocking) | devforgeai/qa/reports/STORY-468-qa-report.md |

## Notes

**Source Requirements:** FR-004
**Design Decisions:**
- Emotional state is self-reported via AskUserQuestion — never AI-inferred
- Enum values provide bounded options rather than freeform text for consistency
- Default to "neutral" if user skips emotional check-in

---

Story Template Version: 2.9
Last Updated: 2026-02-21
