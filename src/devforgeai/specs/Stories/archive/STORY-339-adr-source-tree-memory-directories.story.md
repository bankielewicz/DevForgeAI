---
id: STORY-339
title: Create ADR for Source Tree Memory Directories
type: documentation
epic: EPIC-052
sprint: Backlog
status: QA Approved
points: 1
depends_on: ["STORY-318", "STORY-319"]
priority: High
assigned_to: Unassigned
created: 2026-01-30
format_version: "2.7"
---

# Story: Create ADR for Source Tree Memory Directories

## Description

**As a** Framework Architect,
**I want** an ADR documenting the addition of `.claude/memory/sessions/` and `.claude/memory/learning/` directories to source-tree.md,
**so that** EPIC-052 can proceed with constitutional compliance for new directory structures.

## Provenance

```xml
<provenance>
  <origin document="EPIC-052" section="Prerequisites">
    <quote>"CRITICAL: This epic requires an ADR to update devforgeai/specs/context/source-tree.md before implementation."</quote>
    <line_reference>lines 65-82</line_reference>
    <quantified_impact>Blocks all Feature 2-4 implementation until approved</quantified_impact>
  </origin>

  <decision rationale="constitutional-compliance">
    <selected>Create ADR before implementation per framework rules</selected>
    <rejected alternative="direct-modification">
      Context files are LOCKED - changes require ADR approval per architecture-constraints.md
    </rejected>
    <trade_off>1 story point overhead for constitutional compliance</trade_off>
  </decision>

  <hypothesis id="H-ADR" validation="approval-process" success_criteria="ADR approved, source-tree.md updated">
    ADR approval process validates new directory structure is appropriate for framework
  </hypothesis>
</provenance>
```

---

## Acceptance Criteria

### AC#1: ADR Document Created

```xml
<acceptance_criteria id="AC1">
  <given>No ADR exists for memory directory structure</given>
  <when>Story is completed</when>
  <then>ADR-XXX-memory-directory-structure.md exists in devforgeai/specs/adrs/</then>
  <verification>
    <source_files>
      <file hint="ADR document">devforgeai/specs/adrs/ADR-014-memory-directory-structure.md</file>
    </source_files>
    <test_file>tests/STORY-339/test_ac1_adr_exists.sh</test_file>
    <note>ADR-014 used instead of ADR-013 (ADR-013 already taken by Treelint)</note>
  </verification>
</acceptance_criteria>
```

---

### AC#2: ADR Documents New Directory Structure

```xml
<acceptance_criteria id="AC2">
  <given>ADR document is created</given>
  <when>ADR content is reviewed</when>
  <then>ADR documents sessions/ and learning/ subdirectories with rationale</then>
  <verification>
    <source_files>
      <file hint="ADR document">devforgeai/specs/adrs/ADR-014-memory-directory-structure.md</file>
    </source_files>
    <test_file>tests/STORY-339/test_ac2_adr_content.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Source Tree Updated After ADR Approval

```xml
<acceptance_criteria id="AC3">
  <given>ADR is approved</given>
  <when>Source tree is updated</when>
  <then>source-tree.md contains .claude/memory/sessions/ and .claude/memory/learning/ entries</then>
  <verification>
    <source_files>
      <file hint="Source tree context file">devforgeai/specs/context/source-tree.md</file>
    </source_files>
    <test_file>tests/STORY-339/test_ac3_source_tree_updated.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Documentation"
      name: "ADR-013-memory-directory-structure.md"
      file_path: "devforgeai/specs/adrs/ADR-013-memory-directory-structure.md"
      requirements:
        - id: "DOC-001"
          description: "Document decision to add sessions/ and learning/ subdirectories"
          testable: true
          test_requirement: "Test: Grep for 'sessions/' and 'learning/' in ADR"
          priority: "Critical"
        - id: "DOC-002"
          description: "Include rationale for multi-layer memory architecture"
          testable: true
          test_requirement: "Test: Grep for 'rationale' section in ADR"
          priority: "High"
        - id: "DOC-003"
          description: "Reference EPIC-052 as driver for change"
          testable: true
          test_requirement: "Test: Grep for 'EPIC-052' in ADR"
          priority: "High"

    - type: "Configuration"
      name: "source-tree.md"
      file_path: "devforgeai/specs/context/source-tree.md"
      required_keys:
        - key: ".claude/memory/sessions/"
          type: "directory"
          required: true
          test_requirement: "Test: Grep for sessions/ directory entry"
        - key: ".claude/memory/learning/"
          type: "directory"
          required: true
          test_requirement: "Test: Grep for learning/ directory entry"

  business_rules:
    - id: "BR-001"
      rule: "ADR must be created before source-tree.md modification"
      trigger: "Any new directory added to source-tree.md"
      validation: "ADR exists and references the directory"
      error_handling: "Block source-tree.md edit until ADR created"
      test_requirement: "Test: Verify ADR timestamp precedes source-tree.md edit"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Documentation"
      requirement: "ADR follows standard template format"
      metric: "All required ADR sections present"
      test_requirement: "Test: Validate ADR has Status, Context, Decision, Consequences sections"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Documentation

**ADR Format:**
- Follows ADR template in `devforgeai/specs/adrs/`
- Contains: Status, Context, Decision, Consequences, References sections

### Compliance

**Constitutional Compliance:**
- source-tree.md is LOCKED - requires ADR for modifications
- Changes follow architecture-constraints.md rules

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-318:** Add Observation Schema to High-Frequency Subagents
  - **Why:** EPIC-051 must be in progress for EPIC-052 to make sense
  - **Status:** Complete

- [x] **STORY-319:** Create Observation Extractor Subagent
  - **Why:** Memory system requires observations to store
  - **Status:** Complete

### External Dependencies

- [ ] **EPIC-051 Completion:** Framework Feedback Capture System
  - **Owner:** DevForgeAI Core
  - **ETA:** Feb 9, 2026
  - **Status:** In Progress
  - **Impact if delayed:** EPIC-052 cannot complete without observation data

---

## Test Strategy

### Unit Tests

**Coverage Target:** N/A (documentation story)

**Test Scenarios:**
1. **ADR Exists:** Verify ADR file created in correct location
2. **ADR Content:** Verify required sections present
3. **Source Tree Updated:** Verify new directories added

---

## Acceptance Criteria Verification Checklist

### AC#1: ADR Document Created

- [x] ADR file exists at devforgeai/specs/adrs/ADR-014-memory-directory-structure.md - **Phase:** 3 - **Evidence:** File existence check
- [x] ADR has valid frontmatter - **Phase:** 3 - **Evidence:** YAML parse validation

### AC#2: ADR Documents New Directory Structure

- [x] ADR contains sessions/ directory description - **Phase:** 3 - **Evidence:** Grep pattern match
- [x] ADR contains learning/ directory description - **Phase:** 3 - **Evidence:** Grep pattern match
- [x] ADR contains rationale section - **Phase:** 3 - **Evidence:** Section header check

### AC#3: Source Tree Updated After ADR Approval

- [x] source-tree.md contains memory/sessions/ entry - **Phase:** 3 - **Evidence:** Grep pattern match
- [x] source-tree.md contains memory/learning/ entry - **Phase:** 3 - **Evidence:** Grep pattern match
- [x] Version updated in source-tree.md (3.5) - **Phase:** 3 - **Evidence:** Version increment check

---

**Checklist Progress:** 8/8 items complete (100%)

---

## Definition of Done

### Implementation
- [x] ADR-014-memory-directory-structure.md created (Note: ADR-014 used as ADR-013 already assigned to Treelint)
- [x] ADR approved (status: APPROVED)
- [x] source-tree.md updated with new directories (sessions/, learning/)
- [x] Version incremented in source-tree.md (3.4 → 3.5)

### Quality
- [x] ADR follows standard template (Context, Decision, Consequences, Alternatives)
- [x] All required sections present (verified by tests)
- [x] References EPIC-052 correctly (4 references found)

### Documentation
- [x] ADR documents rationale for multi-layer memory architecture
- [x] source-tree.md version history updated with ADR-014 reference

---

## Implementation Notes

- [x] ADR-014-memory-directory-structure.md created (Note: ADR-014 used as ADR-013 already assigned to Treelint) - Completed: 2026-02-02
- [x] ADR approved (status: APPROVED) - Completed: 2026-02-02
- [x] source-tree.md updated with new directories (sessions/, learning/) - Completed: 2026-02-02
- [x] Version incremented in source-tree.md (3.4 → 3.5) - Completed: 2026-02-02
- [x] ADR follows standard template (Context, Decision, Consequences, Alternatives) - Completed: 2026-02-02
- [x] All required sections present (verified by tests) - Completed: 2026-02-02
- [x] References EPIC-052 correctly (4 references found) - Completed: 2026-02-02
- [x] ADR documents rationale for multi-layer memory architecture - Completed: 2026-02-02
- [x] source-tree.md version history updated with ADR-014 reference - Completed: 2026-02-02

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-02

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-30 14:00 | claude/create-story | Created | Story created for EPIC-052 ADR prerequisite | STORY-339.story.md |
| 2026-02-02 10:40 | claude/qa-result-interpreter | QA Deep | PASSED: 100% traceability, 0 violations, 3/3 tests | STORY-339-qa-report.md |

## Notes

**Design Decisions:**
- ADR number is 014 (ADR-013 was already assigned to Treelint Integration)
- Directory structure follows EPIC-052 specification exactly

**Open Questions:**
- [ ] Should archive/ subdirectory under sessions/ be included? - **Owner:** Framework Architect - **Due:** Sprint Planning

**Related ADRs:**
- ADR-012: Subagent Progressive Disclosure (similar pattern for directory additions)

**References:**
- EPIC-052: Framework Feedback Display & Memory System (lines 65-82)
- architecture-constraints.md: Context File Enforcement (lines 81-100)

---

Story Template Version: 2.7
Last Updated: 2026-01-30
