---
id: STORY-315
title: Add Story Creation Method Guidance to CLAUDE.md
type: documentation
epic: null
sprint: Backlog
status: QA Approved
points: 1
depends_on: []
priority: Critical
created: 2026-01-25
updated: 2026-01-25
format_version: "2.7"
source_rca: RCA-028
source_recommendation: REC-1
---

# STORY-315: Add Story Creation Method Guidance to CLAUDE.md

## Description

**As a** DevForgeAI user or Claude agent,
**I want** explicit guidance in CLAUDE.md that mandates using the `/create-story` skill for story creation,
**so that** validation gates are never bypassed and stories always pass constitution compliance.

**Source:** RCA-028 (Manual Story Creation Ground Truth Validation Failure)

---

## Provenance

```xml
<provenance>
  <origin document="RCA-028" section="Recommendations">
    <quote>"CRITICAL: REC-1 - Add Story Creation Method Guidance to CLAUDE.md"</quote>
    <line_reference>devforgeai/RCA/RCA-028-manual-story-creation-ground-truth-validation-failure.md, lines 197-250</line_reference>
    <quantified_impact>Prevents all future manual story creation without validation</quantified_impact>
  </origin>
  <decision rationale="Root cause prevention">
    <selected>Add explicit rule to CLAUDE.md mandating skill usage</selected>
    <rejected>Rely on developer discipline (failed in RCA-028)</rejected>
    <trade_off>Some loss of flexibility, but ensures quality</trade_off>
  </decision>
</provenance>
```

---

## Acceptance Criteria

### AC#1: CLAUDE.md contains story creation requirements section

```xml
<acceptance_criteria id="AC1">
  <given>CLAUDE.md file</given>
  <when>User reads framework guidance</when>
  <then>A "Story Creation Requirements" section exists after "## Workflow" section</then>
  <verification>
    <source_files>
      <file hint="Framework guidance">CLAUDE.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Section mandates /create-story skill usage

```xml
<acceptance_criteria id="AC2">
  <given>The Story Creation Requirements section</given>
  <when>Read by Claude agent</when>
  <then>It contains "MANDATORY" directive requiring /create-story skill</then>
  <verification>
    <source_files>
      <file hint="Framework guidance">CLAUDE.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Forbidden patterns are documented

```xml
<acceptance_criteria id="AC3">
  <given>The Story Creation Requirements section</given>
  <when>Read by Claude agent</when>
  <then>It lists forbidden patterns: direct Write() calls, batch creation without skill, skipping skill "for efficiency"</then>
  <verification>
    <source_files>
      <file hint="Framework guidance">CLAUDE.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Exception process is documented

```xml
<acceptance_criteria id="AC4">
  <given>The Story Creation Requirements section</given>
  <when>Urgent need to bypass skill</when>
  <then>An exception process exists requiring: AskUserQuestion confirmation, Read ALL target files, Verify against source-tree.md</then>
  <verification>
    <source_files>
      <file hint="Framework guidance">CLAUDE.md</file>
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
      name: "CLAUDE.md Update"
      file_path: "CLAUDE.md"
      requirements:
        - id: "DOC-001"
          description: "Add 'Story Creation Requirements (RCA-028)' section after Workflow section"
          testable: true
          test_requirement: "Test: Grep for '## Story Creation Requirements' in CLAUDE.md"
          priority: "Critical"
        - id: "DOC-002"
          description: "Include MANDATORY directive for /create-story skill"
          testable: true
          test_requirement: "Test: Grep for 'MANDATORY' and '/create-story' in section"
          priority: "Critical"
        - id: "DOC-003"
          description: "Document forbidden patterns with ❌ markers"
          testable: true
          test_requirement: "Test: Grep for 'Forbidden:' and '❌' markers"
          priority: "High"
        - id: "DOC-004"
          description: "Document exception process with AskUserQuestion requirement"
          testable: true
          test_requirement: "Test: Grep for 'Exception Process' and 'AskUserQuestion'"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "All story files must be created using /create-story skill"
      test_requirement: "Test: Manual creation triggers HALT per new guidance"
```

---

## Content to Add

**File:** `CLAUDE.md`
**Location:** After "## Workflow" section (line 211)

```markdown
---

## Story Creation Requirements (RCA-028)

**MANDATORY:** Story files MUST be created using the `/create-story` skill or command.

**Why:** The skill contains validation gates that:
- Verify target files exist before referencing them
- Validate test paths against source-tree.md
- Enforce Read-Quote-Cite-Verify protocol
- Generate verified_violations sections with line numbers

**Forbidden:**
- ❌ Creating story files via direct Write() calls
- ❌ "Batch creating" stories from plan specifications
- ❌ Skipping skill "for efficiency"

**Exception Process:**
IF urgent need to create stories without skill:
1. Use AskUserQuestion to confirm user accepts risk
2. Read ALL target files to verify they exist
3. Verify ALL file paths against source-tree.md
4. Document verification in story file Notes section

**Reference:** RCA-028 (Manual Story Creation Ground Truth Validation Failure)

---
```

---

## Definition of Done

### Implementation
- [x] Section added to CLAUDE.md after Workflow section
- [x] MANDATORY directive present
- [x] Forbidden patterns documented with ❌ markers
- [x] Exception process documented
- [x] RCA-028 reference included

### Testing
- [x] Grep confirms section exists
- [x] Grep confirms all required elements present
- [x] Manual test: Read CLAUDE.md, section visible

### Documentation
- [x] RCA-028 updated with "Implemented in: STORY-315"

---

## AC Verification Checklist

### AC#1: Section exists in CLAUDE.md
- [x] Section added after Workflow - **Phase:** 3 - **Evidence:** CLAUDE.md line 221
- [x] Test TC-AC1 created - **Phase:** 2 - **Evidence:** devforgeai/tests/STORY-315/TEST-SPECIFICATION.md

### AC#2: Mandates skill usage
- [x] MANDATORY directive present - **Phase:** 3 - **Evidence:** CLAUDE.md line 223
- [x] Test TC-AC2 created - **Phase:** 2 - **Evidence:** devforgeai/tests/STORY-315/TEST-SPECIFICATION.md

### AC#3: Forbidden patterns documented
- [x] Three forbidden patterns listed - **Phase:** 3 - **Evidence:** CLAUDE.md lines 232-234
- [x] Test TC-AC3 created - **Phase:** 2 - **Evidence:** devforgeai/tests/STORY-315/TEST-SPECIFICATION.md

### AC#4: Exception process documented
- [x] Four-step exception process - **Phase:** 3 - **Evidence:** CLAUDE.md lines 237-240
- [x] Test TC-AC4 created - **Phase:** 2 - **Evidence:** devforgeai/tests/STORY-315/TEST-SPECIFICATION.md

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-25 | claude/opus | Created | Story created from RCA-028 REC-1 | STORY-315 |
| 2026-01-26 | claude/opus | Phase 02-05 | TDD implementation complete | CLAUDE.md, src/CLAUDE.md, TEST-SPECIFICATION.md |
| 2026-01-26 | claude/opus | Phase 07 | DoD checkboxes updated | STORY-315 |
| 2026-01-26 | claude/qa-result-interpreter | QA Deep | PASSED: Coverage N/A (docs), 0 violations | - |

---

## Implementation Notes

- [x] Section added to CLAUDE.md after Workflow section - Completed: Line 221 in CLAUDE.md, Line 136 in src/CLAUDE.md
- [x] MANDATORY directive present - Completed: Line 223 in CLAUDE.md
- [x] Forbidden patterns documented with ❌ markers - Completed: Lines 231-234 in CLAUDE.md (3 patterns)
- [x] Exception process documented - Completed: Lines 236-241 in CLAUDE.md (4 steps)
- [x] RCA-028 reference included - Completed: Line 243 in CLAUDE.md
- [x] Grep confirms section exists - Completed: TEST-SPECIFICATION.md TC-AC1-4 all PASS
- [x] Grep confirms all required elements present - Completed: 4 pattern matches verified
- [x] Manual test: Read CLAUDE.md, section visible - Completed: Verified in Phase 05 integration
- [x] RCA-028 updated with "Implemented in: STORY-315" - Completed: Line 198 in RCA-028

---

## Notes

**Source RCA:** RCA-028: Manual Story Creation Ground Truth Validation Failure
**Recommendation ID:** REC-1 (CRITICAL)
**Estimated Effort:** 30 minutes

**References:**
- devforgeai/RCA/RCA-028-manual-story-creation-ground-truth-validation-failure.md
- CLAUDE.md
