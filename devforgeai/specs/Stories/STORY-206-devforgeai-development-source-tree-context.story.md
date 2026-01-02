---
id: STORY-206
title: Update devforgeai-development Skill to Pass source-tree.md Context to Subagents
type: enhancement
epic: EPIC-033-framework-enhancement-triage-q4-2025
sprint: Backlog
status: Backlog
points: 1
depends_on: ["STORY-203"]
priority: Medium
assigned_to: Unassigned
created: 2026-01-01
source_rca: RCA-017
source_recommendation: REC-4
format_version: "2.5"
---

# Story: Update devforgeai-development Skill to Pass source-tree.md Context to Subagents

## Description

**As a** DevForgeAI framework developer,
**I want** the devforgeai-development skill to explicitly provide source-tree.md context when invoking subagents,
**so that** there is redundant validation (defense in depth) for file location constraints.

**Context from RCA-017:**
While STORY-203 requires test-automator to validate source-tree.md independently, having the CALLING skill also read and provide context creates redundant validation. Two validation points are better than one:

1. **Caller (devforgeai-development)**: Reads source-tree.md and sets context markers
2. **Callee (test-automator)**: Reads source-tree.md and validates independently

If either validation is somehow bypassed, the other still catches violations.

**Defense in Depth Pattern:**
This follows the security principle of layered defenses. Even if one layer fails (e.g., subagent validation is skipped due to a bug), the skill-level context provides a second check.

## Acceptance Criteria

### AC#1: source-tree.md Read in Phase 1 (Red - Test First)

**Given** the devforgeai-development skill Phase 1 workflow
**When** the skill prepares to invoke test-automator
**Then** source-tree.md is read and test directory context is extracted

**Implementation Location:** `.claude/skills/devforgeai-development/SKILL.md` Phase 1

---

### AC#2: Context Markers Set Before Subagent Invocation

**Given** source-tree.md has been read
**When** test-automator is about to be invoked
**Then** explicit context markers are set in the conversation:

```markdown
**Module Under Test:** {module_name}
**Expected Test Directory:** {test_directory} (per source-tree.md)
**Constraint:** All generated tests must be in {test_directory}
```

---

### AC#3: Context Available to test-automator

**Given** context markers have been set
**When** test-automator is invoked via Task tool
**Then** the subagent has access to the context markers in the conversation

---

### AC#4: Context Extraction Logic for Common Patterns

**Given** a module path (e.g., `installer/backup.py`)
**When** the skill extracts test directory from source-tree.md
**Then** the correct pattern is identified:

| Module Path | Expected Test Directory |
|-------------|------------------------|
| `installer/*` | `installer/tests/` |
| `.claude/scripts/devforgeai_cli/*` | `.claude/scripts/devforgeai_cli/tests/` |
| `src/*` | `tests/` (default) |

---

### AC#5: Reference File Updated

**Given** the Phase 1 workflow changes
**When** implementation is complete
**Then** the relevant reference file is updated with the new step

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "SKILL.md"
      file_path: ".claude/skills/devforgeai-development/SKILL.md"
      requirements:
        - id: "CFG-001"
          description: "Add source-tree.md reading step in Phase 1"
          testable: true
          test_requirement: "Test: Grep for 'Read.*source-tree.md' in Phase 1 section"
          priority: "High"
        - id: "CFG-002"
          description: "Add context marker setting before test-automator invocation"
          testable: true
          test_requirement: "Test: Grep for 'Expected Test Directory' marker"
          priority: "High"
        - id: "CFG-003"
          description: "Add test directory extraction logic"
          testable: true
          test_requirement: "Test: Logic covers installer/, .claude/, src/ patterns"
          priority: "Medium"

    - type: "Configuration"
      name: "tdd-red-phase.md"
      file_path: ".claude/skills/devforgeai-development/references/tdd-red-phase.md"
      requirements:
        - id: "CFG-004"
          description: "Update reference with context setting step"
          testable: true
          test_requirement: "Test: Reference mentions source-tree.md context"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "Context is set BEFORE subagent invocation, not after"
      trigger: "Phase 1 Step before test-automator Task call"
      validation: "Context markers appear in conversation before Task tool"
      error_handling: "N/A - context setting is informational"
      test_requirement: "Test: Verify execution order in /dev output"
      priority: "High"

    - id: "BR-002"
      rule: "Defense in depth - context is redundant with subagent validation"
      trigger: "Design principle"
      validation: "Both skill-level context and subagent-level validation exist"
      error_handling: "Either layer can catch violations independently"
      test_requirement: "Test: Violation caught even if one layer bypassed"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Context setting adds minimal overhead"
      metric: "< 500ms additional latency"
      test_requirement: "Test: Time /dev with and without context step"
      priority: "Low"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - description: "Context markers are informational, not enforced by skill"
    mitigation: "Enforcement is done by subagent (STORY-203)"
    severity: "Low"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Minimal Overhead:**
- source-tree.md reading: < 500ms
- Context marker setting: < 100ms

### Reliability

**Defense in Depth:**
- Skill provides context (layer 1)
- Subagent validates independently (layer 2)
- Either layer catches violations

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-203:** Add source-tree.md Validation to test-automator Phase 2
  - **Why:** Establishes subagent-level validation that this story complements
  - **Status:** Backlog

---

## Test Strategy

### Unit Tests

**Coverage Target:** Verify context markers appear in output

**Test Scenarios:**
1. Run `/dev STORY-X` for installer module
2. Verify "Expected Test Directory: installer/tests/" appears in output
3. Verify context appears BEFORE test-automator invocation

**Test File Location:** `tests/STORY-206/test-source-tree-context.sh`

---

### Integration Tests

**Coverage Target:** Verify defense in depth works

**Test Scenarios:**
1. Run `/dev` with correct test directory → succeeds
2. Attempt wrong directory with context markers → blocked by test-automator
3. Verify both context markers and validation message appear in logs

---

## Acceptance Criteria Verification Checklist

### AC#1: source-tree.md Read in Phase 1

- [ ] Read() call added to Phase 1 - **Phase:** 3 - **Evidence:** SKILL.md diff

### AC#2: Context Markers Set Before Subagent Invocation

- [ ] Context marker template defined - **Phase:** 3 - **Evidence:** SKILL.md content
- [ ] Markers include module, directory, constraint - **Phase:** 3 - **Evidence:** content review

### AC#3: Context Available to test-automator

- [ ] Context appears in /dev output - **Phase:** 5 - **Evidence:** test output
- [ ] Context appears before Task tool call - **Phase:** 5 - **Evidence:** execution order

### AC#4: Context Extraction Logic for Common Patterns

- [ ] installer/ pattern documented - **Phase:** 3 - **Evidence:** SKILL.md content
- [ ] .claude/ pattern documented - **Phase:** 3 - **Evidence:** SKILL.md content
- [ ] Default pattern for src/ documented - **Phase:** 3 - **Evidence:** SKILL.md content

### AC#5: Reference File Updated

- [ ] tdd-red-phase.md updated - **Phase:** 3 - **Evidence:** diff

---

**Checklist Progress:** 0/10 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] source-tree.md reading added to Phase 1
- [ ] Context markers template added (Module, Directory, Constraint)
- [ ] Test directory extraction logic for common patterns
- [ ] Context set BEFORE test-automator Task invocation
- [ ] tdd-red-phase.md reference updated

### Quality
- [ ] All 5 acceptance criteria verified
- [ ] Context markers visible in /dev output
- [ ] Defense in depth principle documented

### Testing
- [ ] Unit tests verify context markers appear
- [ ] Integration tests verify execution order
- [ ] Manual testing with sample story

### Documentation
- [ ] Reference file updated
- [ ] Context setting rationale documented (defense in depth)

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-01 12:00 | claude/devforgeai-story-creation | Created | Story created from RCA-017 REC-4 | STORY-206-devforgeai-development-source-tree-context.story.md |

## Notes

**Design Decisions:**
- Context is informational, not enforced (enforcement is subagent's job)
- Defense in depth provides redundant validation
- Context markers improve debugging (visible in /dev output)

**Source RCA:**
- RCA-017: test-automator Source Tree Constraint Violation
- Recommendation: REC-4 (MEDIUM priority)
- Expected Impact: Adds second validation layer for source-tree.md constraints

**Defense in Depth Diagram:**
```
/dev STORY-X
    │
    ├─ Phase 1: Read source-tree.md (LAYER 1 - This Story)
    │   └─ Set context: "Expected Test Directory: installer/tests/"
    │
    └─ Phase 1: Invoke test-automator (LAYER 2 - STORY-203)
        └─ test-automator reads source-tree.md independently
        └─ Validates test paths against extracted directory
        └─ HALT if mismatch
```

**Relationship to STORY-203:**
- STORY-203: Subagent reads and validates (enforcement)
- STORY-206: Skill reads and provides context (informational + backup)
- Together: Defense in depth with redundant validation

---

**Story Template Version:** 2.5
**Last Updated:** 2026-01-01
