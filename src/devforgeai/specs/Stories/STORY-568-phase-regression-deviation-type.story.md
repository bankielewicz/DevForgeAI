---
id: STORY-568
title: Add Phase Regression Deviation Type to Workflow-Deviation-Protocol
type: feature
epic: EPIC-087
sprint: null
status: Backlog
points: 1
depends_on: []
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: null
created: 2026-03-03
format_version: "2.9"
---

# Story: Add Phase Regression Deviation Type to Workflow-Deviation-Protocol

## Description

**As a** DevForgeAI orchestrator,
**I want** "Phase Regression" added as a deviation type in workflow-deviation-protocol.md,
**so that** backward phase transitions are recognized as a legitimate (if unusual) workflow path with documented rules, not treated as an error or violation.

**Source:** RCA-047 (REC-3) — Orchestrator Test Modification Phase Violation

**Context:** The workflow-deviation-protocol.md defines 3 deviation types: Phase Skipping, Subagent Omission, and Out-of-Sequence. Phase Regression (backward transition) is not recognized. Adding it completes the deviation taxonomy and enables proper consent-based backward transitions.

## Acceptance Criteria

### AC#1: Phase Regression in Deviation Types Table

```xml
<acceptance_criteria id="AC1" implements="REC-3">
  <given>The workflow-deviation-protocol.md Deviation Types table exists with 3 rows</given>
  <when>The story is implemented</when>
  <then>The table has 4 rows including "Phase Regression" with description "Return from Phase N to earlier Phase M (M &lt; N)" and trigger "Test infrastructure defect, subagent output defect"</then>
  <verification>
    <source_files>
      <file hint="Deviation protocol">src/claude/skills/implementing-stories/references/workflow-deviation-protocol.md</file>
    </source_files>
    <test_file>tests/STORY-568/test_ac1_deviation_table.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Phase Regression Rules Documented

```xml
<acceptance_criteria id="AC2" implements="REC-3">
  <given>Phase Regression deviation type is added</given>
  <when>Reading the Phase Regression rules section</when>
  <then>Rules document: must use test-folder-protection AskUserQuestion, must re-invoke authorized subagent, must regenerate integrity snapshots, maximum 2 regressions per story per phase</then>
  <verification>
    <source_files>
      <file hint="Deviation protocol">src/claude/skills/implementing-stories/references/workflow-deviation-protocol.md</file>
    </source_files>
    <test_file>tests/STORY-568/test_ac2_regression_rules.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Snapshot Regeneration Rule

```xml
<acceptance_criteria id="AC3" implements="REC-3">
  <given>Phase Regression rules exist</given>
  <when>Reading the rules</when>
  <then>A rule states "MUST regenerate any integrity snapshots (e.g., red-phase checksums) after re-execution"</then>
  <verification>
    <source_files>
      <file hint="Deviation protocol">src/claude/skills/implementing-stories/references/workflow-deviation-protocol.md</file>
    </source_files>
    <test_file>tests/STORY-568/test_ac3_snapshot_rule.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

**Target File:** `src/claude/skills/implementing-stories/references/workflow-deviation-protocol.md`
**Change Type:** Replace the `## Deviation Types` section (approximately lines 8-16)

### Current State (REPLACE THIS)

```markdown
## Deviation Types

| Type | Description | Trigger |
|------|-------------|---------|
| **Phase Skipping** | Skip Phase N to N+2 | Claude considers phase unnecessary |
| **Subagent Omission** | Skip required subagent | Claude believes subagent adds no value |
| **Out-of-Sequence** | Execute N+1 before N | Claude wants to parallelize/reorder |

**BLOCKING subagents = MANDATORY (cannot omit).** Conditional subagents = OPTIONAL (may skip with reason).
```

### Target State (REPLACE WITH THIS)

```markdown
## Deviation Types

| Type | Description | Trigger |
|------|-------------|---------|
| **Phase Skipping** | Skip Phase N to N+2 | Claude considers phase unnecessary |
| **Subagent Omission** | Skip required subagent | Claude believes subagent adds no value |
| **Out-of-Sequence** | Execute N+1 before N | Claude wants to parallelize/reorder |
| **Phase Regression** | Return from Phase N to earlier Phase M (M < N) | Test infrastructure defect, subagent output defect, or other defect requiring earlier-phase re-execution |

**BLOCKING subagents = MANDATORY (cannot omit).** Conditional subagents = OPTIONAL (may skip with reason).

**Phase Regression rules:**
- MUST be initiated via test-folder-protection AskUserQuestion "Return to Phase 02" option (for test defects)
- MUST re-invoke the authorized subagent for the target phase (e.g., test-automator for Phase 02)
- MUST regenerate any integrity snapshots (e.g., red-phase checksums) after re-execution
- Maximum 2 regressions per story per phase
```

### Structured Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "workflow-deviation-protocol"
      file_path: "src/claude/skills/implementing-stories/references/workflow-deviation-protocol.md"
      required_keys:
        - key: "Deviation Types table"
          type: "array"
          example: "4-row table with Phase Regression row"
          required: true
          validation: "Table has 4 rows (not 3)"
          test_requirement: "Test: Verify 4 rows in Deviation Types table"
        - key: "Phase Regression rules"
          type: "object"
          example: "4 rules for regression behavior"
          required: true
          validation: "All 4 rules present"
          test_requirement: "Test: Verify Phase Regression rules section"

  business_rules:
    - id: "BR-001"
      rule: "Phase Regression must be initiated via test-folder-protection AskUserQuestion"
      trigger: "When regression is requested"
      validation: "Rules reference test-folder-protection"
      error_handling: "N/A - documentation rule"
      test_requirement: "Test: Rules mention test-folder-protection"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "Deviation protocol must remain consistent after addition"
      metric: "Existing 3 types unchanged, 4th added correctly"
      test_requirement: "Test: Existing types preserved"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Performance

N/A — documentation change

### Security

N/A

### Scalability

N/A

### Reliability

**Error Handling:** Additive change, no risk to existing deviation types

### Observability

N/A

---

## Dependencies

### Prerequisite Stories

- None (standalone documentation change)

### Advisory Dependencies

- **STORY-567** (phase regression backward transition) — The Phase Regression deviation type documented here is the concept implemented by STORY-567 in the SKILL.md. Can be implemented in any order since both are additive documentation changes.

### External Dependencies

- None

### Technology Dependencies

- None

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Phase Regression row present in table
2. **Edge Cases:**
   - Existing 3 types preserved
   - Rules section present with all 4 rules
3. **Error Cases:**
   - Table row count validation

### Integration Tests

**Coverage Target:** 85%

**Test Scenarios:**
1. **Consistency:** Deviation types match SKILL.md Phase Regression references

---

## Acceptance Criteria Verification Checklist

### AC#1: Deviation Table

- [ ] Table has 4 rows - **Phase:** 3 - **Evidence:** test_ac1
- [ ] "Phase Regression" row present - **Phase:** 3 - **Evidence:** test_ac1

### AC#2: Regression Rules

- [ ] 4 rules documented - **Phase:** 3 - **Evidence:** test_ac2
- [ ] Max 2 regressions rule present - **Phase:** 3 - **Evidence:** test_ac2

### AC#3: Snapshot Rule

- [ ] Snapshot regeneration rule present - **Phase:** 3 - **Evidence:** test_ac3

---

**Checklist Progress:** 0/5 items complete (0%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
See: .claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Implementation Notes

*To be filled during development*

## Definition of Done

### Implementation
- [ ] Deviation Types table has 4 rows (added Phase Regression)
- [ ] Phase Regression description and trigger documented
- [ ] Phase Regression rules section with 4 rules
- [ ] Existing 3 deviation types unchanged

### Quality
- [ ] All 3 acceptance criteria have passing tests
- [ ] No broken references

### Testing
- [ ] Unit tests for table (test_ac1)
- [ ] Unit tests for rules (test_ac2)
- [ ] Unit tests for snapshot rule (test_ac3)

### Documentation
- [ ] workflow-deviation-protocol.md updated
- [ ] Story Implementation Notes completed

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-03-03 | .claude/story-requirements-analyst | Created | Story created from RCA-047 REC-3 | STORY-568.story.md |

## Notes

**Source:** RCA-047 — Orchestrator Test Modification Phase Violation
**Source Recommendation:** REC-3 — Add "Phase Regression" deviation type to workflow-deviation-protocol

**Design Decisions:**
- Additive change: existing 3 types unchanged
- Consent protocol already exists in workflow-deviation-protocol; Phase Regression uses same mechanism

**References:**
- RCA-047: devforgeai/RCA/RCA-047-orchestrator-test-modification-phase-violation.md
- workflow-deviation-protocol.md: src/claude/skills/implementing-stories/references/workflow-deviation-protocol.md

---

Story Template Version: 2.9
Last Updated: 2026-03-03
