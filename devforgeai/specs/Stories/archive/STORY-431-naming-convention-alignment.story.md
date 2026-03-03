---
id: STORY-431
title: "Evaluate Gerund Naming Convention and Add Trigger Phrases"
type: feature
epic: EPIC-067
sprint: Sprint-3
status: Superseded
points: 3
depends_on: ["STORY-429", "STORY-430"]
priority: Low
assigned_to: DevForgeAI AI Agent
created: 2026-02-17
format_version: "2.9"
---

# Story: Evaluate Gerund Naming Convention and Add Trigger Phrases

## Description

**As a** DevForgeAI framework maintainer,
**I want** to evaluate whether the skill should be renamed to gerund form and add trigger phrases to the description,
**so that** the skill aligns with Anthropic's naming best practices for improved discoverability.

**Context:** This story addresses conformance analysis findings 2.1 (Low), 2.2 (Low), and 2.3 (Low). The skill uses `devforgeai-ideation` (noun form with vendor prefix) instead of the recommended gerund form (e.g., `ideating-requirements`). This may conflict with coding-standards.md naming convention.

**Analysis Source:** `devforgeai/specs/analysis/ideation-anthropic-conformance-analysis.md`, Category 2

**Known Constraint:** `devforgeai/specs/context/coding-standards.md` line 117 may lock the `devforgeai-[phase]` naming pattern. If locked, ADR required before rename.

## Acceptance Criteria

### AC#1: Naming Constraint Evaluated

```xml
<acceptance_criteria id="AC1" implements="FINDING-2.1,FINDING-2.2">
  <given>coding-standards.md may lock the current naming convention</given>
  <when>The constraint is evaluated</when>
  <then>One of: (a) ADR created to unlock naming, rename proceeds; OR (b) Findings 2.1/2.2 closed as "accepted — context file constraint takes priority" with documented justification</then>
  <verification>
    <source_files>
      <file hint="Coding standards">devforgeai/specs/context/coding-standards.md</file>
      <file hint="ADR if created">devforgeai/specs/adrs/ADR-XXX-*.md</file>
    </source_files>
    <test_file>tests/STORY-431/test_ac1_naming_evaluation.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Trigger Phrases Added to Description

```xml
<acceptance_criteria id="AC2" implements="FINDING-2.3">
  <given>SKILL.md description lacks explicit trigger phrases</given>
  <when>Description is updated</when>
  <then>Description includes trigger phrases like: 'or when the user says "I want to build" or "I have a business idea"'</then>
  <verification>
    <source_files>
      <file hint="Main skill file">.claude/skills/devforgeai-ideation/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-431/test_ac2_trigger_phrases.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: If Rename Approved - Directory and References Updated

```xml
<acceptance_criteria id="AC3">
  <given>ADR approves gerund naming (from AC1 path a)</given>
  <when>Rename is executed</when>
  <then>Directory renamed from devforgeai-ideation to ideating-requirements (or similar gerund); all references across codebase updated; skill continues to function</then>
  <verification>
    <source_files>
      <file hint="New skill directory">.claude/skills/ideating-requirements/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-431/test_ac3_rename_complete.sh</test_file>
  </verification>
</acceptance_criteria>
```

**Note:** AC3 is conditional on AC1 path (a). If AC1 results in path (b), AC3 is marked N/A.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "SKILL.md Description"
      file_path: ".claude/skills/devforgeai-ideation/SKILL.md"
      required_keys:
        - key: "description"
          type: "string"
          example: "Transform business ideas... Use when starting new projects... or when the user says 'I want to build'"
          required: true
          validation: "Must include 'Use when' clause and trigger phrases"
          test_requirement: "Test: Description contains trigger phrases"

  business_rules:
    - id: "BR-001"
      rule: "Context file constraints take priority over Anthropic best practices"
      trigger: "When evaluating naming convention"
      validation: "Check coding-standards.md for locked patterns"
      error_handling: "If locked, document as 'accepted — context file constraint'"
      test_requirement: "Test: Either ADR exists OR justification documented"
      priority: "Low"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "No regression in skill discovery or invocation"
      metric: "Skill continues to be discovered by /ideate command"
      test_requirement: "Test: /ideate successfully invokes skill after changes"
      priority: "High"
```

---

## Dependencies

### Prerequisite Stories
- [ ] **STORY-429:** Progressive Disclosure (Sprint 3, F5)
- [ ] **STORY-430:** Workflow Enhancement (Sprint 3, F6)

**Rationale:** Naming changes should be last to avoid impacting other Sprint 3 stories that reference the skill directory.

---

## Definition of Done

### Implementation
- [ ] coding-standards.md naming constraint evaluated
- [ ] Decision documented: (a) ADR + rename OR (b) accepted as is
- [ ] Trigger phrases added to SKILL.md description
- [ ] IF rename: Directory renamed, all references updated
- [ ] IF no rename: Justification documented in story Notes

### Quality
- [ ] All applicable acceptance criteria have passing tests
- [ ] No regression in skill functionality
- [ ] Skill discoverable by /ideate command

### Testing
- [ ] Test: Naming constraint evaluation documented
- [ ] Test: Trigger phrases in description
- [ ] Test: If rename, references updated
- [ ] Test: Skill invocation works

---

## Change Log

**Current Status:** Superseded by EPIC-068

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-17 15:30 | devforgeai-story-creation | Created | Story created from EPIC-067 Feature 7 | STORY-431.story.md |
| 2026-02-17 | DevForgeAI AI Agent | Superseded | Superseded by EPIC-068 (Skill Responsibility Restructure). AC#1 resolved by ADR-017. AC#3 covered by EPIC-068 F9-F11. AC#2 (trigger phrases) folded into EPIC-068 F10. | STORY-431.story.md |

## Notes

**Decision Tree:**
1. Read coding-standards.md line ~117
2. If `devforgeai-[phase]` is LOCKED:
   - Create note: "Findings 2.1/2.2 accepted — context file constraint"
   - Implement only Finding 2.3 (trigger phrases)
   - Mark AC3 as N/A
3. If naming is NOT locked or ADR approved:
   - Rename to `ideating-requirements` or similar gerund
   - Update all Glob/Grep references across codebase
   - Update /ideate command skill invocation

**Low Priority:** This story is the lowest priority in the epic. If ADR process is complex, findings can be closed as accepted without impacting overall epic success.

---

Story Template Version: 2.9
Last Updated: 2026-02-17
