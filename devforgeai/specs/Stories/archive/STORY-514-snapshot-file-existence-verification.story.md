---
id: STORY-514
title: Add Snapshot File Existence Check to Phase 02 Gate
type: feature
epic: null
sprint: null
status: QA Approved
points: 1
depends_on: ["STORY-513"]
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: Unassigned
created: 2026-02-28
format_version: "2.9"
---

# Story: Add Snapshot File Existence Check to Phase 02 Gate

## Description

**As a** DevForgeAI orchestrator executing the implementing-stories skill,
**I want** an explicit file existence verification after snapshot creation in Phase 02,
**so that** Phase 02 cannot complete if the snapshot file was not actually written to disk.

**Context:** RCA-043 identified that the CLI gate (`phase-complete`) only checks subagent records, not artifact creation. The snapshot step is a file-creation operation with no enforcement mechanism. Adding an explicit `Glob()` check after snapshot creation creates a hard gate — if the file doesn't exist, Phase 02 halts.

**Source:** RCA-043 (Test Integrity Snapshot Skipped) / REC-2

## Acceptance Criteria

> **IMPORTANT:** XML acceptance criteria format is REQUIRED for automated verification by the ac-compliance-verifier subagent.

### XML Acceptance Criteria Format

```xml
<acceptance_criteria id="AC1" implements="COMP-XXX,COMP-YYY">
  <given>Initial context or precondition</given>
  <when>Action or event being tested</when>
  <then>Expected outcome or result</then>
</acceptance_criteria>
```

### AC#1: File Existence Verification Step Added

```xml
<acceptance_criteria id="AC1" implements="CFG-001">
  <given>The Test Integrity Snapshot section in phase-02-test-first.md instructs the orchestrator to create a snapshot file</given>
  <when>The snapshot creation step completes</when>
  <then>A file existence verification step follows immediately, using Glob to check for devforgeai/qa/snapshots/${STORY_ID}/red-phase-checksums.json, with a HALT instruction if the file is not found</then>
  <verification>
    <source_files>
      <file hint="Phase 02 workflow file">.claude/skills/implementing-stories/phases/phase-02-test-first.md</file>
    </source_files>
    <test_file>tests/STORY-514/test_ac1_existence_check.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: HALT Message Includes Diagnostic Information

```xml
<acceptance_criteria id="AC2" implements="CFG-001">
  <given>The file existence verification step is in place</given>
  <when>The Glob check fails to find the snapshot file</when>
  <then>The HALT message includes the expected file path and a clear instruction: "Snapshot file not created — cannot complete Phase 02"</then>
  <verification>
    <source_files>
      <file hint="Phase 02 workflow file">.claude/skills/implementing-stories/phases/phase-02-test-first.md</file>
    </source_files>
    <test_file>tests/STORY-514/test_ac2_halt_message.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Verification Step Appears Between Snapshot and Checkpoint

```xml
<acceptance_criteria id="AC3" implements="CFG-001">
  <given>STORY-513 has moved the snapshot section before the validation checkpoint</given>
  <when>This story adds the file existence verification</when>
  <then>The verification step appears after the snapshot creation instruction and before the Validation Checkpoint, in logical sequence: Create → Verify → Checkpoint</then>
  <verification>
    <source_files>
      <file hint="Phase 02 workflow file">.claude/skills/implementing-stories/phases/phase-02-test-first.md</file>
    </source_files>
    <test_file>tests/STORY-514/test_ac3_position.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### Source Files Guidance

All ACs target the same file: `.claude/skills/implementing-stories/phases/phase-02-test-first.md`

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "phase-02-test-first.md"
      file_path: ".claude/skills/implementing-stories/phases/phase-02-test-first.md"
      required_keys:
        - key: "Snapshot file existence verification block"
          type: "string"
          example: "Glob(pattern='devforgeai/qa/snapshots/${STORY_ID}/red-phase-checksums.json') with HALT on not found"
          required: true
          test_requirement: "Test: Grep for Glob pattern checking snapshot file existence in phase-02-test-first.md"
        - key: "HALT message for missing snapshot"
          type: "string"
          example: "HALT 'Snapshot file not created — cannot complete Phase 02'"
          required: true
          test_requirement: "Test: Grep for HALT message containing 'Snapshot file not created' in the verification block"

  business_rules:
    - id: "BR-001"
      rule: "Phase 02 must verify snapshot file exists before reaching the Validation Checkpoint"
      trigger: "After snapshot creation step, before Validation Checkpoint"
      validation: "Glob check for red-phase-checksums.json returns a match"
      error_handling: "HALT with diagnostic message if file not found"
      test_requirement: "Test: Verify Glob check and HALT instruction present between snapshot and checkpoint sections"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "File existence check prevents false positive phase completion"
      metric: "0% chance of Phase 02 completing without snapshot file on disk"
      test_requirement: "Test: Verification block contains both Glob check and HALT fallback"
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

**Response Time:** N/A — workflow file change

---

### Security

**Authentication:** None required
**Authorization:** None required
**Data Protection:** N/A

---

### Scalability

N/A — static workflow file

---

### Reliability

**Error Handling:**
- Verification step must include clear HALT message with expected path
- No silent failures permitted

---

### Observability

N/A — static workflow file change

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-513:** Move Test Integrity Snapshot Before Phase 02 Validation Checkpoint
  - **Why:** The snapshot section must be positioned before the checkpoint before we can add verification between them
  - **Status:** Backlog

### External Dependencies

None

### Technology Dependencies

None

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Glob verification block present after snapshot section
2. **Edge Cases:**
   - HALT message includes expected file path pattern
   - Verification appears before Validation Checkpoint
3. **Error Cases:**
   - Missing verification block (should fail test)

---

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **File structure:** Complete file parses correctly with new verification block

---

## Acceptance Criteria Verification Checklist

### AC#1: File Existence Verification Step Added

- [x] Glob check for snapshot file present in phase file - **Phase:** 3 - **Evidence:** phase-02-test-first.md
- [x] HALT instruction present if file not found - **Phase:** 3 - **Evidence:** phase-02-test-first.md

### AC#2: HALT Message Includes Diagnostic Information

- [x] HALT message contains expected path pattern - **Phase:** 2 - **Evidence:** tests/STORY-514/test_ac2_halt_message.sh
- [x] Message text is clear and actionable - **Phase:** 3 - **Evidence:** phase-02-test-first.md

### AC#3: Verification Step Appears Between Snapshot and Checkpoint

- [x] Verification block line number > snapshot section line number - **Phase:** 2 - **Evidence:** tests/STORY-514/test_ac3_position.sh
- [x] Verification block line number < checkpoint section line number - **Phase:** 2 - **Evidence:** tests/STORY-514/test_ac3_position.sh

---

**Checklist Progress:** 6/6 items complete (100%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
When filling in the Implementation Notes section during /dev workflow:
1. DoD items MUST be placed DIRECTLY under "## Implementation Notes" header
2. NO ### subsection headers (like "### Definition of Done Status") before DoD items
3. The extract_section() validator stops at the first ### header it encounters
4. If DoD items are under a ### subsection, the validator cannot find them → commit blocked
5. The ### Additional Notes subsection is OK because it comes AFTER DoD items
See: .claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-28

- [x] File existence verification step added after snapshot creation in phase-02-test-first.md - Completed: Added ### Snapshot File Existence Verification (STORY-514) section with Glob check and HALT
- [x] Glob pattern checks for devforgeai/qa/snapshots/${STORY_ID}/red-phase-checksums.json - Completed: Glob pattern uses correct path with runtime ${STORY_ID} template variable
- [x] HALT instruction with clear diagnostic message if file not found - Completed: HALT "Snapshot file not created — cannot complete Phase 02"
- [x] Verification step positioned between snapshot creation and Validation Checkpoint - Completed: Inserted after "Execute snapshot creation per the reference." and before "## Validation Checkpoint"
- [x] All 3 acceptance criteria have passing tests - Completed: 9/9 unit tests pass across 3 AC test files
- [x] File structure validates correctly - Completed: 24/24 integration tests pass
- [x] No broken cross-references - Completed: Verified via integration test
- [x] Unit tests for verification block presence - Completed: tests/STORY-514/test_ac1_existence_check.sh (3 tests)
- [x] Unit tests for HALT message content - Completed: tests/STORY-514/test_ac2_halt_message.sh (3 tests)
- [x] Unit tests for verification position - Completed: tests/STORY-514/test_ac3_position.sh (3 tests)
- [x] Integration test for complete file structure - Completed: tests/STORY-514/test_integration_file_structure.sh (24 tests)
- [x] Story file created with complete specification - Completed: Story created from RCA-043/REC-2
- [x] RCA-043 updated with story link for REC-2 - Completed: Deferred — RCA-043 already references STORY-514 in its recommendations

## Definition of Done

### Implementation
- [x] File existence verification step added after snapshot creation in phase-02-test-first.md
- [x] Glob pattern checks for devforgeai/qa/snapshots/${STORY_ID}/red-phase-checksums.json
- [x] HALT instruction with clear diagnostic message if file not found
- [x] Verification step positioned between snapshot creation and Validation Checkpoint

### Quality
- [x] All 3 acceptance criteria have passing tests
- [x] File structure validates correctly
- [x] No broken cross-references

### Testing
- [x] Unit tests for verification block presence
- [x] Unit tests for HALT message content
- [x] Unit tests for verification position
- [x] Integration test for complete file structure

### Documentation
- [x] Story file created with complete specification
- [x] RCA-043 updated with story link for REC-2

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-28 10:00 | .claude/story-requirements-analyst | Created | Story created from RCA-043/REC-2 | STORY-514.story.md |
| 2026-02-28 | .claude/qa-result-interpreter | QA Deep | PASSED: 33/33 tests, 0 violations, 3/3 validators | - |

## Notes

**Source RCA:** RCA-043 (Test Integrity Snapshot Skipped)
**Source Recommendation:** REC-2 (Add Snapshot File Existence Check to Phase Gate)

**Design Decisions:**
- Use Glob() tool for file existence check (consistent with framework patterns)
- HALT message includes the expected file path for debugging
- Verification block is 3 lines: Glob call, IF not found, HALT message
- **IMPORTANT:** `${STORY_ID}` in the code block below is a **template placeholder** that must remain literally as `${STORY_ID}` in the phase file. It is NOT a variable to expand during implementation. The orchestrator expands it at runtime when executing Phase 02 for a specific story.

**Exact Edit Specification:**
After STORY-513 relocates the snapshot section, it will appear immediately before the `## Validation Checkpoint` heading. Insert the following verification block between the end of the snapshot creation instructions and the `## Validation Checkpoint` heading. To locate the insertion point, search for the string `Execute snapshot creation per the reference.` — insert immediately after that line (and its trailing `---` separator):
```
Glob(pattern="devforgeai/qa/snapshots/${STORY_ID}/red-phase-checksums.json")
IF not found: HALT "Snapshot file not created — cannot complete Phase 02"
```

**Note:** The `${STORY_ID}` above is a literal template variable. Do NOT replace it with an actual story ID. It gets expanded at runtime by the orchestrator.

**References:**
- RCA-043: devforgeai/RCA/RCA-043-test-integrity-snapshot-skipped.md
- STORY-513: devforgeai/specs/Stories/STORY-513-move-snapshot-before-validation-checkpoint.story.md

---

Story Template Version: 2.9
Last Updated: 2026-02-28
