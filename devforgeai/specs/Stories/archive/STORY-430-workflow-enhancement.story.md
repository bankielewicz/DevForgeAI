---
id: STORY-430
title: "Add Checklist Tracking and Chain-of-Thought Guidance"
type: feature
epic: EPIC-067
sprint: Sprint-3
status: Deferred
points: 2
depends_on: ["STORY-428"]
priority: Medium
assigned_to: DevForgeAI AI Agent
created: 2026-02-17
format_version: "2.9"
---

# Story: Add Checklist Tracking and Chain-of-Thought Guidance

## Description

**As a** DevForgeAI framework maintainer,
**I want** to add a checklist tracking instruction to the Success Criteria and chain-of-thought guidance for complexity scoring,
**so that** Claude actively tracks completion during execution and reasons through complexity scores for improved accuracy and auditability.

**Context:** This story addresses conformance analysis findings 6.1 (Medium) and 7.2 (Medium). Finding 6.1 notes the Success Criteria checklist lacks a "Copy and track" instruction. Finding 7.2 notes complexity scoring (Phase 3) lacks explicit chain-of-thought guidance.

**Analysis Source:** `devforgeai/specs/analysis/ideation-anthropic-conformance-analysis.md`, Categories 6, 7

## Acceptance Criteria

### AC#1: Checklist Tracking Instruction Added

```xml
<acceptance_criteria id="AC1" implements="FINDING-6.1">
  <given>SKILL.md Success Criteria section has a checklist without tracking instruction</given>
  <when>The section is updated</when>
  <then>A "Copy this checklist and update it as you complete each phase:" instruction is added before the checklist items</then>
  <verification>
    <source_files>
      <file hint="Main skill file">.claude/skills/devforgeai-ideation/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-430/test_ac1_checklist_instruction.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Chain-of-Thought Added to Complexity Scoring

```xml
<acceptance_criteria id="AC2" implements="FINDING-7.2">
  <given>complexity-assessment-workflow.md lacks explicit thinking guidance</given>
  <when>CoT guidance is added</when>
  <then>The workflow includes instructions to use &lt;thinking&gt; tags when scoring each dimension, with example showing reasoning before score assignment</then>
  <verification>
    <source_files>
      <file hint="Complexity workflow">.claude/skills/devforgeai-ideation/references/complexity-assessment-workflow.md</file>
    </source_files>
    <test_file>tests/STORY-430/test_ac2_cot_guidance.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: CoT Example Demonstrates All 4 Dimensions

```xml
<acceptance_criteria id="AC3">
  <given>CoT guidance is being added</given>
  <when>Example is reviewed</when>
  <then>Example shows reasoning for all 4 dimensions: Functional (0-20), Technical (0-20), Team/Org (0-10), NFR (0-10) with explicit &lt;thinking&gt; and &lt;score&gt; XML tags</then>
  <verification>
    <source_files>
      <file hint="Complexity workflow">.claude/skills/devforgeai-ideation/references/complexity-assessment-workflow.md</file>
    </source_files>
    <test_file>tests/STORY-430/test_ac3_cot_completeness.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "Success Criteria Tracking"
      file_path: ".claude/skills/devforgeai-ideation/SKILL.md"
      required_keys:
        - key: "tracking_instruction"
          type: "string"
          example: "Copy this checklist and update it as you complete each phase:"
          required: true
          test_requirement: "Test: Success Criteria contains 'Copy this checklist'"

    - type: "Configuration"
      name: "CoT Guidance"
      file_path: ".claude/skills/devforgeai-ideation/references/complexity-assessment-workflow.md"
      required_keys:
        - key: "thinking_tags"
          type: "string"
          example: "<thinking>...</thinking>"
          required: true
          test_requirement: "Test: Workflow contains <thinking> tag guidance"
        - key: "score_tags"
          type: "string"
          example: "<score>...</score>"
          required: true
          test_requirement: "Test: Workflow contains <score> tag guidance"

  business_rules:
    - id: "BR-001"
      rule: "Checklist pattern requires copy instruction"
      trigger: "Validating workflow patterns"
      validation: "If checklist exists, 'Copy' instruction must precede it"
      test_requirement: "Test: Grep for 'Copy this checklist'"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "Improved complexity scoring accuracy through explicit reasoning"
      metric: "Scores include reasoning trail for all 4 dimensions"
      test_requirement: "Test: CoT example covers all 4 dimensions"
      priority: "Medium"
```

---

## Definition of Done

### Implementation
- [ ] "Copy this checklist and update it" instruction added to Success Criteria
- [ ] <thinking> tag guidance added to complexity-assessment-workflow.md
- [ ] CoT example shows reasoning for all 4 scoring dimensions
- [ ] <score> tag used for final score output

### Quality
- [ ] All 3 acceptance criteria have passing tests
- [ ] CoT example is realistic and demonstrates expected quality
- [ ] No regression in complexity assessment functionality

### Testing
- [ ] Test: Checklist tracking instruction present
- [ ] Test: <thinking> and <score> tags in complexity workflow
- [ ] Test: All 4 dimensions in CoT example

---

## Change Log

**Current Status:** Deferred — Blocked by EPIC-068

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-17 15:30 | devforgeai-story-creation | Created | Story created from EPIC-067 Feature 6 | STORY-430.story.md |
| 2026-02-17 | DevForgeAI AI Agent | Deferred | Blocked by EPIC-068 (Skill Responsibility Restructure). complexity-assessment-workflow.md moves to architecture skill — file path will be invalid. Re-evaluate after EPIC-068 Sprint 1. | STORY-430.story.md |

## Notes

**Quick Win:** This story is 2 points because changes are small text additions in 2 files. CoT example can be adapted from Anthropic's chain-of-thought.md examples.

**Anthropic Reference:**
- Checklist pattern: best-practices.md lines 402-403
- Chain of thought: `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/chain-of-thought.md`

---

Story Template Version: 2.9
Last Updated: 2026-02-17
