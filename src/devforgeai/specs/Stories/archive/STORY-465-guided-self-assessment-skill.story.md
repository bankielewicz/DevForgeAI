---
id: STORY-465
title: Guided Self-Assessment Skill
type: feature
epic: EPIC-072
sprint: Sprint-15
status: QA Approved
points: 3
depends_on: []
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: DevForgeAI AI Agent
created: 2026-02-21
format_version: "2.9"
---

# Story: Guided Self-Assessment Skill

## Description

**As a** solo developer or aspiring entrepreneur,
**I want** to complete a guided self-assessment questionnaire covering my work style, challenges, motivations, energy management, and previous business attempts,
**so that** the AI can adapt its coaching approach to my cognitive style and needs.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-011" section="problem-statement">
    <quote>"Developers and aspiring entrepreneurs build projects but never turn them into businesses due to intertwined barriers: lack of business knowledge (MBA gap), lack of confidence (psychological gap), and executive dysfunction (ADHD/neurodivergent gap)."</quote>
    <line_reference>lines 12-13</line_reference>
    <quantified_impact>Foundation for all 9 business skills — without user assessment, no adaptive coaching is possible</quantified_impact>
  </origin>

  <decision rationale="combination-assessment-over-pure-self-report">
    <selected>Combination: self-report + guided questions — NEVER diagnoses</selected>
    <rejected alternative="pure-self-report">Too superficial; misses patterns users don't recognize</rejected>
    <rejected alternative="ai-inference">Ethical concern; AI should never diagnose mental health conditions</rejected>
    <trade_off>Longer initial session (~10-15 min) in exchange for significantly better adaptation quality</trade_off>
  </decision>

  <stakeholder role="Solo Developer" goal="turn-project-into-business">
    <quote>"Has a project, wants to turn it into a business, struggles with overwhelm and imposter syndrome"</quote>
    <source>BRAINSTORM-011, stakeholder map</source>
  </stakeholder>

  <stakeholder role="Aspiring Entrepreneur" goal="structure-business-idea">
    <quote>"Has a business idea, no technical product yet, doesn't know where to start"</quote>
    <source>BRAINSTORM-011, stakeholder map</source>
  </stakeholder>

  <hypothesis id="H1" validation="Track completion % with/without adaptation" success_criteria="50%+ session completion rate">
    IF we break business tasks into 5-15 min micro-chunks, THEN ADHD users will complete more sessions
  </hypothesis>
</provenance>
```

## Acceptance Criteria

### AC#1: Assessment Skill File Structure

```xml
<acceptance_criteria id="AC1" implements="COMP-001">
  <given>The DevForgeAI framework src/ tree exists</given>
  <when>The assessing-entrepreneur skill is created</when>
  <then>SKILL.md exists at src/claude/skills/assessing-entrepreneur/SKILL.md with valid YAML frontmatter containing name, description (with "Use when..." trigger), and the file is under 1000 lines</then>
  <verification>
    <source_files>
      <file hint="Main skill file">src/claude/skills/assessing-entrepreneur/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-465/test_ac1_skill_structure.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#2: Six-Dimension Questionnaire

```xml
<acceptance_criteria id="AC2" implements="COMP-001,COMP-002">
  <given>The assessing-entrepreneur skill is loaded</given>
  <when>A user invokes the assessment workflow</when>
  <then>The skill guides the user through 6 assessment dimensions: (1) Work Style Preferences, (2) Task Completion Patterns, (3) Motivation Drivers, (4) Energy Management, (5) Previous Attempts, (6) Self-Reported Challenges, using AskUserQuestion for each dimension</then>
  <verification>
    <source_files>
      <file hint="Main skill with questionnaire phases">src/claude/skills/assessing-entrepreneur/SKILL.md</file>
      <file hint="Work style questionnaire reference">src/claude/skills/assessing-entrepreneur/references/work-style-questionnaire.md</file>
    </source_files>
    <test_file>tests/STORY-465/test_ac2_questionnaire_dimensions.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#3: Entrepreneur-Assessor Subagent

```xml
<acceptance_criteria id="AC3" implements="COMP-003">
  <given>The assessment questionnaire responses are collected</given>
  <when>The entrepreneur-assessor subagent is invoked via Task()</when>
  <then>The subagent normalizes responses into structured profile data, is defined at src/claude/agents/entrepreneur-assessor.md with valid YAML frontmatter, is under 500 lines, and has tools restricted to Read, Glob, Grep, AskUserQuestion</then>
  <verification>
    <source_files>
      <file hint="Subagent definition">src/claude/agents/entrepreneur-assessor.md</file>
    </source_files>
    <test_file>tests/STORY-465/test_ac3_assessor_subagent.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#4: Reference Files for Progressive Disclosure

```xml
<acceptance_criteria id="AC4" implements="COMP-001">
  <given>The assessing-entrepreneur skill requires deep documentation</given>
  <when>Reference files are created</when>
  <then>The references/ directory contains at minimum: adhd-adaptation-framework.md, confidence-assessment-workflow.md, work-style-questionnaire.md, and plan-calibration-engine.md, each with valid content and under 1500 lines</then>
  <verification>
    <source_files>
      <file hint="ADHD framework">src/claude/skills/assessing-entrepreneur/references/adhd-adaptation-framework.md</file>
      <file hint="Confidence workflow">src/claude/skills/assessing-entrepreneur/references/confidence-assessment-workflow.md</file>
      <file hint="Questionnaire">src/claude/skills/assessing-entrepreneur/references/work-style-questionnaire.md</file>
      <file hint="Calibration">src/claude/skills/assessing-entrepreneur/references/plan-calibration-engine.md</file>
    </source_files>
    <test_file>tests/STORY-465/test_ac4_reference_files.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#5: Safety Disclaimers

```xml
<acceptance_criteria id="AC5">
  <given>The assessment covers self-reported challenges including ADHD, anxiety, and confidence</given>
  <when>The skill content is reviewed</when>
  <then>The skill explicitly states it NEVER diagnoses mental health conditions, includes a disclaimer in the questionnaire flow, and frames all questions as self-reported preferences not clinical assessments</then>
  <verification>
    <source_files>
      <file hint="Main skill with disclaimer">src/claude/skills/assessing-entrepreneur/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-465/test_ac5_safety_disclaimers.py</test_file>
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
      name: "assessing-entrepreneur SKILL.md"
      file_path: "src/claude/skills/assessing-entrepreneur/SKILL.md"
      required_keys:
        - key: "name"
          type: "string"
          example: "assessing-entrepreneur"
          required: true
          validation: "kebab-case, 1-64 chars"
          test_requirement: "Test: Verify name field matches 'assessing-entrepreneur'"
        - key: "description"
          type: "string"
          example: "Guided self-assessment for business coaching adaptation. Use when..."
          required: true
          validation: "1-1024 chars, includes 'Use when' trigger"
          test_requirement: "Test: Verify description contains 'Use when' trigger phrase"

    - type: "Configuration"
      name: "entrepreneur-assessor subagent"
      file_path: "src/claude/agents/entrepreneur-assessor.md"
      required_keys:
        - key: "name"
          type: "string"
          example: "entrepreneur-assessor"
          required: true
          validation: "kebab-case"
          test_requirement: "Test: Verify subagent name field"
        - key: "tools"
          type: "string"
          example: "Read, Glob, Grep, AskUserQuestion"
          required: true
          validation: "Restricted tool set per principle of least privilege"
          test_requirement: "Test: Verify tools list matches expected set"

    - type: "Configuration"
      name: "Reference files directory"
      file_path: "src/claude/skills/assessing-entrepreneur/references/"
      required_keys:
        - key: "adhd-adaptation-framework.md"
          type: "file"
          required: true
          validation: "File exists, non-empty"
          test_requirement: "Test: Verify file exists and contains ADHD adaptation content"
        - key: "work-style-questionnaire.md"
          type: "file"
          required: true
          validation: "File exists, non-empty"
          test_requirement: "Test: Verify file exists and contains 6 dimensions"

  business_rules:
    - id: "BR-001"
      rule: "Assessment skill NEVER diagnoses mental health conditions"
      trigger: "Any question related to ADHD, anxiety, depression, or cognitive challenges"
      validation: "Skill content contains explicit disclaimer; no diagnostic language used"
      error_handling: "All questions framed as self-reported preferences"
      test_requirement: "Test: Grep SKILL.md for diagnostic language (must find none); verify disclaimer present"
      priority: "Critical"

    - id: "BR-002"
      rule: "Assessment covers exactly 6 dimensions"
      trigger: "Assessment workflow execution"
      validation: "Work Style, Task Completion, Motivation, Energy, Previous Attempts, Self-Reported Challenges"
      error_handling: "Missing dimension halts assessment"
      test_requirement: "Test: Verify all 6 dimension headers present in questionnaire reference"
      priority: "High"

    - id: "BR-003"
      rule: "Assessment completes in 10-15 minutes"
      trigger: "Assessment flow design"
      validation: "Questions structured for brevity with bounded options"
      error_handling: "AskUserQuestion uses 2-4 options per question"
      test_requirement: "Test: Verify questionnaire uses AskUserQuestion with bounded options"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "SKILL.md under 1000 lines"
      metric: "Line count < 1000 (target 500-800)"
      test_requirement: "Test: wc -l SKILL.md < 1000"
      priority: "High"

    - id: "NFR-002"
      category: "Performance"
      requirement: "Subagent under 500 lines"
      metric: "Line count < 500 (target 100-300)"
      test_requirement: "Test: wc -l entrepreneur-assessor.md < 500"
      priority: "High"

    - id: "NFR-003"
      category: "Security"
      requirement: "No executable code in skill files"
      metric: "Zero code blocks with executable content"
      test_requirement: "Test: Verify no shebang lines or executable patterns"
      priority: "Critical"
```

## Technical Limitations

```yaml
technical_limitations: []
# No known limitations for this story
```

## Non-Functional Requirements

### Performance
- **Skill load time:** SKILL.md < 1000 lines for token budget compliance
- **Reference loading:** On-demand only (progressive disclosure)

### Security
- **No diagnostic language:** Assessment must never imply clinical diagnosis
- **Self-reported only:** All data is user-provided, never AI-inferred

### Reliability
- **Graceful handling:** If user skips a dimension, assessment continues with defaults

## Dependencies

### Prerequisite Stories
- None (this is the foundation story for EPIC-072)

### External Dependencies
- None (framework operates within Claude Code Terminal)

### Technology Dependencies
- None (Markdown-only, no packages required)

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for structural validation

**Test Scenarios:**
1. **Happy Path:** SKILL.md exists, has valid frontmatter, < 1000 lines
2. **Edge Cases:**
   - Missing name field in frontmatter
   - Missing description field
   - SKILL.md exceeds 1000 lines
3. **Error Cases:**
   - Subagent file missing
   - Reference directory empty
   - Diagnostic language found in content

### Integration Tests

**Coverage Target:** 85%

**Test Scenarios:**
1. **Skill-Subagent Link:** SKILL.md references entrepreneur-assessor correctly
2. **Reference Discovery:** All 4 reference files exist and are linked from SKILL.md

## Acceptance Criteria Verification Checklist

### AC#1: Assessment Skill File Structure
- [ ] SKILL.md exists at correct path - **Phase:** 2 - **Evidence:** tests/STORY-465/test_ac1_skill_structure.py
- [ ] YAML frontmatter valid with name and description - **Phase:** 2 - **Evidence:** tests/STORY-465/test_ac1_skill_structure.py
- [ ] File under 1000 lines - **Phase:** 3 - **Evidence:** tests/STORY-465/test_ac1_skill_structure.py
- [ ] Description includes "Use when" trigger - **Phase:** 3 - **Evidence:** tests/STORY-465/test_ac1_skill_structure.py

### AC#2: Six-Dimension Questionnaire
- [ ] Work Style dimension present - **Phase:** 3 - **Evidence:** tests/STORY-465/test_ac2_questionnaire_dimensions.py
- [ ] Task Completion dimension present - **Phase:** 3 - **Evidence:** tests/STORY-465/test_ac2_questionnaire_dimensions.py
- [ ] Motivation dimension present - **Phase:** 3 - **Evidence:** tests/STORY-465/test_ac2_questionnaire_dimensions.py
- [ ] Energy Management dimension present - **Phase:** 3 - **Evidence:** tests/STORY-465/test_ac2_questionnaire_dimensions.py
- [ ] Previous Attempts dimension present - **Phase:** 3 - **Evidence:** tests/STORY-465/test_ac2_questionnaire_dimensions.py
- [ ] Self-Reported Challenges dimension present - **Phase:** 3 - **Evidence:** tests/STORY-465/test_ac2_questionnaire_dimensions.py

### AC#3: Entrepreneur-Assessor Subagent
- [ ] Subagent file exists at correct path - **Phase:** 2 - **Evidence:** tests/STORY-465/test_ac3_assessor_subagent.py
- [ ] YAML frontmatter valid - **Phase:** 2 - **Evidence:** tests/STORY-465/test_ac3_assessor_subagent.py
- [ ] Tools restricted to Read, Glob, Grep, AskUserQuestion - **Phase:** 3 - **Evidence:** tests/STORY-465/test_ac3_assessor_subagent.py
- [ ] Under 500 lines - **Phase:** 3 - **Evidence:** tests/STORY-465/test_ac3_assessor_subagent.py

### AC#4: Reference Files
- [ ] adhd-adaptation-framework.md exists - **Phase:** 3 - **Evidence:** tests/STORY-465/test_ac4_reference_files.py
- [ ] confidence-assessment-workflow.md exists - **Phase:** 3 - **Evidence:** tests/STORY-465/test_ac4_reference_files.py
- [ ] work-style-questionnaire.md exists - **Phase:** 3 - **Evidence:** tests/STORY-465/test_ac4_reference_files.py
- [ ] plan-calibration-engine.md exists - **Phase:** 3 - **Evidence:** tests/STORY-465/test_ac4_reference_files.py

### AC#5: Safety Disclaimers
- [ ] Disclaimer present in SKILL.md - **Phase:** 3 - **Evidence:** tests/STORY-465/test_ac5_safety_disclaimers.py
- [ ] No diagnostic language in content - **Phase:** 3 - **Evidence:** tests/STORY-465/test_ac5_safety_disclaimers.py

---

**Checklist Progress:** 0/18 items complete (0%)

---

## Definition of Done

### Implementation
- [x] assessing-entrepreneur/SKILL.md created with valid YAML frontmatter and 6-dimension questionnaire workflow
- [x] entrepreneur-assessor.md subagent created with restricted tool set
- [x] 4 reference files created in references/ directory with substantive content
- [x] All files in src/ tree (not operational .claude/)

### Quality
- [x] All 5 acceptance criteria have passing tests
- [x] Safety disclaimer verified (no diagnostic language)
- [x] SKILL.md < 1000 lines; subagent < 500 lines
- [x] Progressive disclosure pattern followed (deep content in references/)

### Testing
- [x] Unit tests for skill structure (test_ac1_skill_structure.py)
- [x] Unit tests for questionnaire dimensions (test_ac2_questionnaire_dimensions.py)
- [x] Unit tests for subagent structure (test_ac3_assessor_subagent.py)
- [x] Unit tests for reference files (test_ac4_reference_files.py)
- [x] Unit tests for safety disclaimers (test_ac5_safety_disclaimers.py)

### Documentation
- [x] SKILL.md contains clear phase descriptions for assessment workflow
- [x] Reference files contain actionable framework content (not placeholders)
- [x] Subagent system prompt describes single responsibility clearly

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| 01 Pre-Flight | ✅ Complete | Git validated, 6 context files loaded, tech-stack detected |
| 02 Red | ✅ Complete | 47 tests written, all FAIL (expected) |
| 03 Green | ✅ Complete | 6 files created, 47/47 tests PASS |
| 04 Refactor | ✅ Complete | SKILL.md reduced 36%, code-reviewer APPROVED |
| 04.5 AC Verify | ✅ Complete | 5/5 ACs PASS (HIGH confidence) |
| 05 Integration | ✅ Complete | 5/5 integration points PASS |
| 05.5 AC Verify | ✅ Complete | No regressions detected |
| 06 Deferral | ✅ Complete | No deferrals needed |
| 07 DoD Update | ✅ Complete | All DoD items marked complete |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/assessing-entrepreneur/SKILL.md | Created | ~196 |
| src/claude/agents/entrepreneur-assessor.md | Created | ~128 |
| src/claude/skills/assessing-entrepreneur/references/adhd-adaptation-framework.md | Created | ~95 |
| src/claude/skills/assessing-entrepreneur/references/confidence-assessment-workflow.md | Created | ~121 |
| src/claude/skills/assessing-entrepreneur/references/work-style-questionnaire.md | Created | ~270 |
| src/claude/skills/assessing-entrepreneur/references/plan-calibration-engine.md | Created | ~132 |
| tests/STORY-465/conftest.py | Created | ~51 |
| tests/STORY-465/test_ac1_skill_structure.py | Created | ~85 |
| tests/STORY-465/test_ac2_questionnaire_dimensions.py | Created | ~100 |
| tests/STORY-465/test_ac3_assessor_subagent.py | Created | ~80 |
| tests/STORY-465/test_ac4_reference_files.py | Created | ~90 |
| tests/STORY-465/test_ac5_safety_disclaimers.py | Created | ~76 |

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-21

- [x] assessing-entrepreneur/SKILL.md created with valid YAML frontmatter and 6-dimension questionnaire workflow - Completed: SKILL.md created at src/claude/skills/assessing-entrepreneur/SKILL.md with 9-phase assessment workflow covering all 6 dimensions via AskUserQuestion
- [x] entrepreneur-assessor.md subagent created with restricted tool set - Completed: Subagent created at src/claude/agents/entrepreneur-assessor.md with tools restricted to Read, Glob, Grep, AskUserQuestion
- [x] 4 reference files created in references/ directory with substantive content - Completed: adhd-adaptation-framework.md, confidence-assessment-workflow.md, work-style-questionnaire.md, plan-calibration-engine.md created with actionable content
- [x] All files in src/ tree (not operational .claude/) - Completed: All 6 implementation files in src/claude/ tree
- [x] All 5 acceptance criteria have passing tests - Completed: 47/47 tests pass across 5 test files
- [x] Safety disclaimer verified (no diagnostic language) - Completed: Multiple disclaimers present, no affirmative diagnostic language
- [x] SKILL.md < 1000 lines; subagent < 500 lines - Completed: SKILL.md is 196 lines, subagent is 128 lines
- [x] Progressive disclosure pattern followed (deep content in references/) - Completed: SKILL.md concise, 4 reference files contain deep documentation
- [x] Unit tests for skill structure (test_ac1_skill_structure.py) - Completed: 8 tests for AC#1
- [x] Unit tests for questionnaire dimensions (test_ac2_questionnaire_dimensions.py) - Completed: 14 tests for AC#2
- [x] Unit tests for subagent structure (test_ac3_assessor_subagent.py) - Completed: 8 tests for AC#3
- [x] Unit tests for reference files (test_ac4_reference_files.py) - Completed: 13 tests for AC#4
- [x] Unit tests for safety disclaimers (test_ac5_safety_disclaimers.py) - Completed: 3 tests for AC#5
- [x] SKILL.md contains clear phase descriptions for assessment workflow - Completed: 9 phases documented clearly
- [x] Reference files contain actionable framework content (not placeholders) - Completed: All reference files contain substantive, actionable content
- [x] Subagent system prompt describes single responsibility clearly - Completed: Single responsibility documented in entrepreneur-assessor.md

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-21 | .claude/story-requirements-analyst | Created | Story created from EPIC-072 Feature 1 | STORY-465.story.md |
| 2026-02-22 | .claude/qa-result-interpreter | QA Deep | PASSED: 47/47 tests, 0 CRITICAL/HIGH violations, 3/3 validators | - |
| 2026-03-04 | DevForgeAI AI Agent | Documentation | Generated 6 docs (README, API, Architecture, Developer Guide, Troubleshooting, Roadmap) via /document --type=all | docs/assessing-entrepreneur-README.md, docs/api/assessing-entrepreneur-API.md, docs/architecture/assessing-entrepreneur-ARCHITECTURE.md, docs/guides/assessing-entrepreneur-{DEVELOPER-GUIDE,TROUBLESHOOTING,ROADMAP}.md |

## Notes

**Design Decisions:**
- Assessment skill is sole writer of user-profile.yaml (coaching skill reads only) — prevents data coordination issues
- Gerund naming per ADR-017: `assessing-entrepreneur` (not `devforgeai-assessment`)
- Subagent uses AskUserQuestion tool to enable interactive questionnaire flow

**Source Requirements:**
- FR-001 from business-skills-framework-requirements.md
- BRAINSTORM-011 Phase 1 decisions: "Combination (self-report + guided questions) — NEVER diagnoses"

**Related ADRs:**
- ADR-017: Skill Naming Convention (gerund form)

---

Story Template Version: 2.9
Last Updated: 2026-02-21
