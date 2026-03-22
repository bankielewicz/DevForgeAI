---
id: STORY-317
title: Update Plan File Template with Verification Checklist
type: documentation
epic: null
sprint: Backlog
status: QA Approved
points: 1
depends_on: ["STORY-315", "STORY-316"]
priority: Medium
created: 2026-01-25
updated: 2026-01-25
format_version: "2.7"
source_rca: RCA-028
source_recommendation: REC-3
---

# STORY-317: Update Plan File Template with Verification Checklist

## Description

**As a** DevForgeAI user or Claude agent creating plan files,
**I want** a verification checklist embedded in plan file templates,
**so that** verification status is visible and tracked within the plan itself.

**Source:** RCA-028 (Manual Story Creation Ground Truth Validation Failure)

---

## Provenance

```xml
<provenance>
  <origin document="RCA-028" section="Recommendations">
    <quote>"MEDIUM: REC-3 - Update Plan File Template with Verification Checklist"</quote>
    <line_reference>devforgeai/RCA/RCA-028-manual-story-creation-ground-truth-validation-failure.md, lines 305-340</line_reference>
    <quantified_impact>Embeds verification into plan creation process</quantified_impact>
  </origin>
  <decision rationale="Visibility at point of use">
    <selected>Add checklist section to plan files</selected>
    <rejected>Rely on external rule file only (not visible in plan)</rejected>
    <trade_off>Plans become slightly longer, but verification is visible</trade_off>
  </decision>
</provenance>
```

---

## Acceptance Criteria

### AC#1: Plan file guidance includes verification checklist section

```xml
<acceptance_criteria id="AC1">
  <given>Plan mode documentation or templates</given>
  <when>New plan file is created</when>
  <then>Plan includes "Story Verification Checklist" section</then>
  <verification>
    <source_files>
      <file hint="Plan guidance">CLAUDE.md (Plan File Convention section)</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Checklist includes file existence verification

```xml
<acceptance_criteria id="AC2">
  <given>The Story Verification Checklist section</given>
  <when>Read by user or Claude agent</when>
  <then>It contains checkbox: "All target files verified to exist (Read each file)"</then>
  <verification>
    <source_files>
      <file hint="Plan guidance">CLAUDE.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Checklist includes source-tree.md verification

```xml
<acceptance_criteria id="AC3">
  <given>The Story Verification Checklist section</given>
  <when>Read by user or Claude agent</when>
  <then>It contains checkbox: "All test paths match source-tree.md patterns"</then>
  <verification>
    <source_files>
      <file hint="Plan guidance">CLAUDE.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Checklist includes deleted file check

```xml
<acceptance_criteria id="AC4">
  <given>The Story Verification Checklist section</given>
  <when>Read by user or Claude agent</when>
  <then>It contains checkbox: "No references to deleted files (check git status)"</then>
  <verification>
    <source_files>
      <file hint="Plan guidance">CLAUDE.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Checklist includes verification status indicator

```xml
<acceptance_criteria id="AC5">
  <given>The Story Verification Checklist section</given>
  <when>Verification is complete or not</when>
  <then>A status indicator shows: "⬜ Not Verified" or "✅ Verified"</then>
  <verification>
    <source_files>
      <file hint="Plan guidance">CLAUDE.md</file>
    </source_files>
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
      name: "CLAUDE.md Plan Convention Update"
      file_path: "CLAUDE.md"
      requirements:
        - id: "DOC-001"
          description: "Add verification checklist to Plan File Convention section"
          testable: true
          test_requirement: "Test: Grep for 'Story Verification Checklist' in CLAUDE.md"
          priority: "High"
        - id: "DOC-002"
          description: "Include 5 verification checkboxes"
          testable: true
          test_requirement: "Test: Count checkbox items in checklist section"
          priority: "High"
        - id: "DOC-003"
          description: "Include status indicator guidance"
          testable: true
          test_requirement: "Test: Grep for 'Not Verified' and 'Verified' status"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "Plan files with story specifications must include verification checklist"
      test_requirement: "Test: New plans created include checklist section"
```

---

## Content to Add

**File:** `CLAUDE.md`
**Location:** Within "## Plan File Convention" section

```markdown
### Story Verification Checklist (RCA-028)

**Include in plan files that contain story specifications:**

```markdown
## Story Verification Checklist

Before creating stories from this plan:

- [ ] All target files verified to exist (Read each file)
- [ ] All test paths match source-tree.md patterns
- [ ] No references to deleted files (check git status)
- [ ] All dependencies verified to exist
- [ ] Exact edits specified (not vague "update X")

**Status:** ⬜ Not Verified / ✅ Verified
```

**When to update status:**
- After completing all verification checks: Change to ✅ Verified
- Before story creation: Must show ✅ Verified

**Reference:** RCA-028 (Manual Story Creation Ground Truth Validation Failure)
```

---

## Definition of Done

### Implementation
- [x] Verification checklist guidance added to CLAUDE.md Plan File Convention
- [x] 5 checkbox items documented
- [x] Status indicator guidance included
- [x] RCA-028 reference present

### Testing
- [x] Grep confirms checklist section in CLAUDE.md
- [x] Grep confirms all 5 checkboxes present
- [ ] Manual test: Create new plan, verify checklist is included

### Documentation
- [ ] RCA-028 updated with "Implemented in: STORY-317"

---

## AC Verification Checklist

### AC#1: Checklist section exists
- [x] Section added to CLAUDE.md - **Phase:** 3 - **Evidence:** Line 148

### AC#2: File existence checkbox
- [x] Checkbox present - **Phase:** 3 - **Evidence:** Line 157

### AC#3: source-tree.md checkbox
- [x] Checkbox present - **Phase:** 3 - **Evidence:** Line 158

### AC#4: Deleted file checkbox
- [x] Checkbox present - **Phase:** 3 - **Evidence:** Line 159

### AC#5: Status indicator
- [x] Status indicator documented - **Phase:** 3 - **Evidence:** Line 163

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-25 | claude/opus | Created | Story created from RCA-028 REC-3 | STORY-317 |
| 2026-01-26 | claude/opus | Dev Complete | Added Story Verification Checklist to CLAUDE.md Plan File Convention section | CLAUDE.md |
| 2026-01-26 | claude/qa-result-interpreter | QA Deep | PASSED: Traceability 100%, 5/5 ACs verified, 0 violations | - |

## Implementation Notes

- [x] Verification checklist guidance added to CLAUDE.md Plan File Convention - Completed: Added subsection at line 148
- [x] 5 checkbox items documented - Completed: Lines 157-161 contain all 5 verification checkboxes
- [x] Status indicator guidance included - Completed: Line 163 shows "⬜ Not Verified / ✅ Verified"
- [x] RCA-028 reference present - Completed: Referenced in heading (line 148) and footer (line 170)
- [x] Grep confirms checklist section in CLAUDE.md - Completed: Pattern "Story Verification Checklist" found at lines 148, 153
- [x] Grep confirms all 5 checkboxes present - Completed: All 5 checkbox patterns verified at lines 157-161

---

## Notes

**Source RCA:** RCA-028: Manual Story Creation Ground Truth Validation Failure
**Recommendation ID:** REC-3 (MEDIUM)
**Estimated Effort:** 30 minutes
**Depends on:** STORY-315, STORY-316 (foundation stories should be in place first)

**References:**
- devforgeai/RCA/RCA-028-manual-story-creation-ground-truth-validation-failure.md
- CLAUDE.md (Plan File Convention section)
