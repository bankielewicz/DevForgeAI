---
id: STORY-467
title: Dynamic Persona Blend Engine
type: feature
epic: EPIC-072
sprint: Sprint-16
status: QA Approved
points: 3
depends_on: ["STORY-466"]
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: DevForgeAI AI Agent
created: 2026-02-21
format_version: "2.9"
---

# Story: Dynamic Persona Blend Engine

## Description

**As a** user receiving business coaching,
**I want** the AI to dynamically shift between an empathetic coach persona and a professional consultant persona based on my emotional state and context,
**so that** I receive encouragement when struggling and structured deliverables when focused.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-011" section="design-decisions">
    <quote>"AI persona: Adaptive blend — shifts between coach and consultant dynamically"</quote>
    <line_reference>lines 97-98</line_reference>
    <quantified_impact>Core interaction model for all coaching sessions — affects every user touchpoint</quantified_impact>
  </origin>

  <decision rationale="adaptive-blend-over-fixed-persona">
    <selected>Adaptive blend — detects user needs, shifts dynamically within and across sessions</selected>
    <rejected alternative="fixed-coach">Some users need structure, not just encouragement</rejected>
    <rejected alternative="fixed-consultant">Some users need emotional support, not just deliverables</rejected>
    <trade_off>More complex prompt engineering vs. one-size-fits-all simplicity</trade_off>
  </decision>

  <hypothesis id="H4" validation="User preference surveys across sessions" success_criteria=">4/5 satisfaction rating">
    IF we use adaptive blend persona (coach/consultant), THEN user satisfaction exceeds fixed personas
  </hypothesis>
</provenance>
```

## Acceptance Criteria

### AC#1: Coaching Skill File Structure

```xml
<acceptance_criteria id="AC1" implements="COMP-001">
  <given>The DevForgeAI framework src/ tree exists</given>
  <when>The coaching-entrepreneur skill is created</when>
  <then>SKILL.md exists at src/claude/skills/coaching-entrepreneur/SKILL.md with valid YAML frontmatter (name: coaching-entrepreneur, description with "Use when" trigger), under 1000 lines, with persona blend instructions as core workflow</then>
  <verification>
    <source_files>
      <file hint="Main coaching skill">src/claude/skills/coaching-entrepreneur/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-467/test_ac1_coaching_skill_structure.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#2: Coach and Consultant Persona Definitions

```xml
<acceptance_criteria id="AC2" implements="COMP-001,COMP-002">
  <given>The coaching-entrepreneur skill is loaded</given>
  <when>The persona blend engine is evaluated</when>
  <then>The skill defines two distinct personas: Coach mode (empathetic, encouraging, celebrates wins, addresses self-doubt) and Consultant mode (structured, deliverable-focused, professional frameworks), with explicit indicators for when to use each</then>
  <verification>
    <source_files>
      <file hint="Coaching skill with persona definitions">src/claude/skills/coaching-entrepreneur/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-467/test_ac2_persona_definitions.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#3: Business-Coach Subagent

```xml
<acceptance_criteria id="AC3" implements="COMP-003">
  <given>The coaching skill needs a specialized subagent for coaching interactions</given>
  <when>The business-coach subagent is created</when>
  <then>business-coach.md exists at src/claude/agents/business-coach.md with valid YAML frontmatter, tools restricted to Read, Grep, Glob, AskUserQuestion, under 500 lines, and contains persona blend instructions in its system prompt</then>
  <verification>
    <source_files>
      <file hint="Business coach subagent">src/claude/agents/business-coach.md</file>
    </source_files>
    <test_file>tests/STORY-467/test_ac3_business_coach_subagent.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#4: User Profile Reading

```xml
<acceptance_criteria id="AC4">
  <given>A user-profile.yaml exists from a previous /assess-me session</given>
  <when>The coaching skill starts a session</when>
  <then>The skill reads the user profile to determine adaptation levels and adjusts persona blend, task chunking, and celebration intensity based on the profile dimensions</then>
  <verification>
    <source_files>
      <file hint="Coaching skill profile integration">src/claude/skills/coaching-entrepreneur/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-467/test_ac4_profile_reading.py</test_file>
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
      name: "coaching-entrepreneur SKILL.md"
      file_path: "src/claude/skills/coaching-entrepreneur/SKILL.md"
      required_keys:
        - key: "name"
          type: "string"
          example: "coaching-entrepreneur"
          required: true
          validation: "kebab-case, gerund form"
          test_requirement: "Test: Verify name field is 'coaching-entrepreneur'"
        - key: "description"
          type: "string"
          required: true
          validation: "Contains 'Use when' trigger"
          test_requirement: "Test: Verify description contains trigger phrase"

    - type: "Configuration"
      name: "business-coach subagent"
      file_path: "src/claude/agents/business-coach.md"
      required_keys:
        - key: "name"
          type: "string"
          example: "business-coach"
          required: true
          test_requirement: "Test: Verify subagent name"
        - key: "tools"
          type: "string"
          example: "Read, Grep, Glob, AskUserQuestion"
          required: true
          test_requirement: "Test: Verify restricted tool set"

  business_rules:
    - id: "BR-001"
      rule: "Coach mode uses empathetic language; Consultant mode uses structured language"
      trigger: "Session start and during any persona transition"
      validation: "SKILL.md contains explicit persona definition sections"
      error_handling: "Default to Coach mode if user profile unavailable"
      test_requirement: "Test: Verify both persona sections exist in SKILL.md"
      priority: "Critical"

    - id: "BR-002"
      rule: "Coaching skill reads user-profile.yaml but NEVER writes to it"
      trigger: "Any coaching session start"
      validation: "No Write() calls to user-profile.yaml in coaching skill"
      error_handling: "If profile missing, prompt user to run /assess-me first"
      test_requirement: "Test: Verify no write instructions to user-profile.yaml in coaching skill"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "SKILL.md under 1000 lines"
      metric: "Line count < 1000"
      test_requirement: "Test: wc -l SKILL.md < 1000"
      priority: "High"
    - id: "NFR-002"
      category: "Performance"
      requirement: "Subagent under 500 lines"
      metric: "Line count < 500"
      test_requirement: "Test: wc -l business-coach.md < 500"
      priority: "High"
```

## Technical Limitations

```yaml
technical_limitations: []
```

## Non-Functional Requirements

### Performance
- **Skill size:** SKILL.md < 1000 lines; deep persona docs in references/
- **Subagent size:** business-coach.md < 500 lines

### Security
- **No AI inference of mental state:** Persona shifts based on user-reported state only

## Dependencies

### Prerequisite Stories
- [ ] **STORY-466:** Adaptive Profile Generation
  - **Why:** Coaching needs the user profile to calibrate persona blend
  - **Status:** Backlog

## Test Strategy

### Unit Tests
**Coverage Target:** 95%+
1. **Happy Path:** Skill exists, has persona sections, subagent exists with correct tools
2. **Edge Cases:** Profile missing (graceful fallback), both personas defined
3. **Error Cases:** Skill over 1000 lines, subagent over 500 lines

## Acceptance Criteria Verification Checklist

### AC#1: Coaching Skill File Structure
- [x] SKILL.md exists at correct path - **Phase:** 2 *(test: test_ac1)*
- [x] Valid YAML frontmatter - **Phase:** 2 *(test: test_ac1)*
- [x] Under 1000 lines - **Phase:** 3 *(138 lines)*

### AC#2: Persona Definitions
- [x] Coach mode defined with empathetic indicators - **Phase:** 3
- [x] Consultant mode defined with structured indicators - **Phase:** 3
- [x] Transition triggers documented - **Phase:** 3

### AC#3: Business-Coach Subagent
- [x] Subagent file exists - **Phase:** 2 *(test: test_ac3)*
- [x] Tools restricted correctly - **Phase:** 3 *(Read, Grep, Glob, AskUserQuestion)*
- [x] Under 500 lines - **Phase:** 3 *(71 lines)*

### AC#4: User Profile Reading
- [x] Profile read instructions in SKILL.md - **Phase:** 3
- [x] Graceful fallback if profile missing - **Phase:** 3 *(default Coach mode)*

---

**Checklist Progress:** 11/11 items complete (100%)

---

## Definition of Done

### Implementation
- [x] coaching-entrepreneur/SKILL.md created with persona blend workflow
- [x] business-coach.md subagent created with persona instructions
- [x] Coaching skill reads user-profile.yaml (read-only)
- [x] All files in src/ tree

### Quality
- [x] All 4 acceptance criteria have passing tests
- [x] Coaching skill never writes to user-profile.yaml
- [x] Both persona modes clearly defined

### Testing
- [x] Unit tests for skill structure (test_ac1)
- [x] Unit tests for persona definitions (test_ac2)
- [x] Unit tests for subagent structure (test_ac3)
- [x] Unit tests for profile reading (test_ac4)

### Documentation
- [x] Persona blend logic documented in SKILL.md
- [x] Subagent system prompt describes coaching role

---

## Implementation Notes

- [x] coaching-entrepreneur/SKILL.md created with persona blend workflow - Completed: Added YAML frontmatter, persona blend engine with Coach/Consultant modes, transition indicators, profile reading
- [x] business-coach.md subagent created with persona instructions - Completed: Added persona blend instructions, restricted tools to Read/Grep/Glob/AskUserQuestion
- [x] Coaching skill reads user-profile.yaml (read-only) - Completed: Step 1 reads profile at session start, adapts blend, graceful fallback to Coach mode
- [x] All files in src/ tree - Completed: src/claude/skills/coaching-entrepreneur/SKILL.md and src/claude/agents/business-coach.md
- [x] All 4 acceptance criteria have passing tests - Completed: 69 tests (42 unit + 27 integration) all passing
- [x] Coaching skill never writes to user-profile.yaml - Completed: Explicitly states read-only, no Write() calls
- [x] Both persona modes clearly defined - Completed: Coach (empathetic, encouraging) and Consultant (structured, deliverable-focused)
- [x] Unit tests for skill structure (test_ac1) - Completed: 8 tests
- [x] Unit tests for persona definitions (test_ac2) - Completed: 12 tests
- [x] Unit tests for subagent structure (test_ac3) - Completed: 14 tests
- [x] Unit tests for profile reading (test_ac4) - Completed: 8 tests
- [x] Persona blend logic documented in SKILL.md - Completed: Persona Blend Engine section with Coach/Consultant/Transition Indicators
- [x] Subagent system prompt describes coaching role - Completed: Persona Blend Instructions section in business-coach.md

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-03-04

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| 01 Pre-Flight | ✅ Complete | Git validated, 6 context files loaded, tech-stack detected |
| 02 Red | ✅ Complete | 42 tests generated, 26 fail + 3 error (RED confirmed) |
| 03 Green | ✅ Complete | SKILL.md + business-coach.md updated, 42/42 pass |
| 04 Refactor | ✅ Complete | No refactoring needed, code review approved |
| 4.5 AC Verify | ✅ Complete | 4/4 ACs PASS |
| 05 Integration | ✅ Complete | 27 integration tests added, 69/69 pass |
| 5.5 AC Verify | ✅ Complete | 4/4 ACs PASS post-integration |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/coaching-entrepreneur/SKILL.md | Modified | 137 |
| src/claude/agents/business-coach.md | Modified | 70 |
| tests/STORY-467/test_ac1_coaching_skill_structure.py | Created | ~80 |
| tests/STORY-467/test_ac2_persona_definitions.py | Created | ~100 |
| tests/STORY-467/test_ac3_business_coach_subagent.py | Created | ~120 |
| tests/STORY-467/test_ac4_profile_reading.py | Created | ~70 |
| tests/STORY-467/test_integration_cross_file_consistency.py | Created | ~200 |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-21 | .claude/story-requirements-analyst | Created | Story created from EPIC-072 Feature 3 | STORY-467.story.md |
| 2026-03-04 | DevForgeAI AI Agent | Documentation | Updated 3 sections in framework docs via /document --type=all | docs/api/API.md, docs/architecture/ARCHITECTURE.md, docs/guides/DEVELOPER-GUIDE.md |
| 2026-03-04 | .claude/qa-result-interpreter | QA Deep | PASSED: 69/69 tests, 0 blocking violations, 3/3 validators passed | devforgeai/qa/reports/STORY-467-qa-report.md |

## Notes

**Source Requirements:** FR-003
**Design Decisions:**
- Persona blend is prompt-engineering based (XML tags for context, role assignment per Anthropic guidelines)
- Default to Coach mode when profile unavailable — encouragement is safer than cold structure for new users

---

Story Template Version: 2.9
Last Updated: 2026-02-21
