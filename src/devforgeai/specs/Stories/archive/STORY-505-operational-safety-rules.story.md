---
id: STORY-505
title: Operational Safety Rules
type: feature
epic: EPIC-085
sprint: Sprint-18
status: QA Approved
points: 2
depends_on: []
priority: Medium
advisory: false
source_gap: null
source_story: null
assigned_to: null
created: 2026-02-27
format_version: "2.9"
---

# Story: Operational Safety Rules

## Description

**As a** DevForgeAI framework contributor,
**I want** a dedicated operational safety rules file at `.claude/rules/workflow/operational-safety.md` that consolidates and clarifies safe file-writing practices (avoiding Bash cat/echo and prohibiting `/tmp/` writes),
**so that** Claude agents have a single, unambiguous reference that prevents destructive or unreliable file operations during story development workflows.

## Acceptance Criteria

> **IMPORTANT:** XML acceptance criteria format is REQUIRED for automated verification.

### XML Acceptance Criteria Format

### AC#1: Rule 1 Cross-References Existing Anti-Pattern

```xml
<acceptance_criteria id="AC1" implements="COMP-001">
  <given>The developer opens .claude/rules/workflow/operational-safety.md</given>
  <when>They read the Rule 1 section about using Write tool (never cat/echo via Bash)</when>
  <then>The rule references anti-patterns.md Category 1 and critical-rules.md Rule 2 as authoritative sources with "See also:" and exact file paths, and does NOT restate the full anti-pattern verbatim (no duplication)</then>
</acceptance_criteria>
```

---

### AC#2: Rule 2 Prohibits /tmp/ and Mandates Project-Scoped tmp

```xml
<acceptance_criteria id="AC2" implements="COMP-001">
  <given>The operational-safety.md file exists</given>
  <when>An agent reads the Rule 2 section</when>
  <then>The rule explicitly states /tmp/ is FORBIDDEN, specifies correct path pattern as {project-root}/tmp/{story-id}/, provides wrong/correct example block, and explains rationale (portability across WSL/Windows/Linux, traceability by story)</then>
</acceptance_criteria>
```

---

### AC#3: Rule File Has Valid Structure

```xml
<acceptance_criteria id="AC3" implements="COMP-001">
  <given>The operational-safety.md file is created</given>
  <when>The file is read and parsed</when>
  <then>Contains YAML frontmatter with name, description, version, created fields; body contains exactly two numbered rules; file is under 300 lines</then>
</acceptance_criteria>
```

---

### AC#4: tmp/ Directory Path Clarification

```xml
<acceptance_criteria id="AC4" implements="COMP-001">
  <given>An agent needs to write temporary files</given>
  <when>The agent consults operational-safety.md Rule 2</when>
  <then>The rule specifies path must be constructed relative to project root (e.g., tmp/STORY-505/) and clarifies relative paths acceptable only when CWD is verified as project root</then>
</acceptance_criteria>
```

---

### AC#5: File Is Discoverable from Rules README

```xml
<acceptance_criteria id="AC5" implements="COMP-002">
  <given>operational-safety.md exists at .claude/rules/workflow/</given>
  <when>A developer reads .claude/rules/README.md</when>
  <then>The workflow/ directory is listed and the new file is discoverable</then>
</acceptance_criteria>
```

---

### Source Files Guidance

The `<source_files>` element provides hints to the ac-compliance-verifier about where implementation code is located.

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "operational-safety.md"
      file_path: ".claude/rules/workflow/operational-safety.md"
      required_keys:
        - key: "rule_1_write_tool"
          type: "object"
          required: true
          test_requirement: "Test: Rule 1 references anti-patterns.md Category 1 and critical-rules.md Rule 2 with 'See also:' format"
        - key: "rule_2_tmp_prohibition"
          type: "object"
          required: true
          test_requirement: "Test: Rule 2 contains /tmp/ prohibition, correct path pattern, and wrong/correct examples"
        - key: "yaml_frontmatter"
          type: "object"
          required: true
          test_requirement: "Test: YAML frontmatter contains name, description, version, created fields"

    - type: "Configuration"
      name: ".gitignore tmp/ entry"
      file_path: ".gitignore"
      required_keys:
        - key: "tmp_exclusion"
          type: "string"
          required: true
          test_requirement: "Test: .gitignore contains tmp/ entry to prevent accidental git tracking"

  business_rules:
    - id: "BR-001"
      rule: "Rule 1 must cross-reference, not duplicate, existing anti-patterns"
      trigger: "When operational-safety.md Rule 1 is written"
      validation: "No verbatim copy of anti-patterns.md Category 1 content"
      error_handling: "Review and refactor to use 'See also:' references"
      test_requirement: "Test: Rule 1 contains 'See also:' with paths to anti-patterns.md and critical-rules.md"
      priority: "High"
    - id: "BR-002"
      rule: "/tmp/ is forbidden; project-root/tmp/{story-id}/ is required"
      trigger: "When any agent writes temporary files"
      validation: "Path must match {project-root}/tmp/{STORY-NNN|scratch|YYYY-MM-DD}/"
      error_handling: "HALT if /tmp/ path detected"
      test_requirement: "Test: Rule 2 explicitly states /tmp/ is FORBIDDEN"
      priority: "Critical"
    - id: "BR-003"
      rule: "tmp/ must be in .gitignore"
      trigger: "Before story completion"
      validation: "Grep .gitignore for tmp/"
      error_handling: "Add entry if missing"
      test_requirement: "Test: .gitignore contains tmp/ after story completion"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Rule file load time"
      metric: "< 50ms single Read() call, file < 8 KB / 300 lines"
      test_requirement: "Test: File is under 300 lines and under 8 KB"
      priority: "Medium"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Cross-reference stability"
      metric: "All 'See also:' paths resolve via Read() without error"
      test_requirement: "Test: Read anti-patterns.md and critical-rules.md paths succeed"
      priority: "High"
```

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Rule enforcement"
    limitation: "Prompt-level rules are advisory; cannot programmatically intercept Write tool calls"
    decision: "workaround:prompt-level rule provides guidance; /qa skill validates compliance"
    discovered_phase: "Architecture"
    impact: "Agents may still write to /tmp/ if they ignore rules; detection happens during QA"
```

## Non-Functional Requirements (NFRs)

### Performance

**File Size:**
- Target: < 300 lines, < 8 KB
- Load time: < 50ms (single Read() call)

### Security

**No Secrets:**
- No credentials in rule file
- tmp/ path examples use placeholder story IDs

### Scalability

**Extensible:**
- Rule format supports addition of Rule 3, 4, etc. without restructuring
- Each rule uses self-contained ### Rule N: block

### Reliability

**Idempotent:**
- Write() overwrites cleanly without partial content
- Cross-references verified at implementation time
- .gitignore coverage verified before completion

### Observability

**Discoverability:**
- grep for "operational-safety" resolves in single Grep call
- Listed in .claude/rules/README.md

## Dependencies

### Prerequisite Stories

None — this story has no blocking dependencies.

### External Dependencies

None.

### Technology Dependencies

None — uses existing .claude/rules/ directory structure.

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**
1. **Happy Path:** Rule file exists with correct content
2. **Edge Cases:**
   - Rule 1 temptation to duplicate — verify cross-reference only
   - WSL path ambiguity for tmp/ location
   - Story ID not yet known — fallback naming (scratch/)
   - Existing tmp/ directory from prior run
3. **Error Cases:**
   - Cross-referenced files missing → implementation HALTS
   - .gitignore missing tmp/ entry → add it

### Integration Tests

**Coverage Target:** 85%+ for application layer

**Test Scenarios:**
1. **.gitignore Integration:** tmp/ entry present after completion
2. **Rules Discovery:** File listed in .claude/rules/README.md or discoverable via glob

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

### AC#1: Rule 1 Cross-References

- [x] "See also:" references anti-patterns.md - **Phase:** 2 - **Evidence:** rule file lines 16-18
- [x] "See also:" references critical-rules.md - **Phase:** 2 - **Evidence:** rule file lines 16-18
- [x] No verbatim duplication - **Phase:** 2 - **Evidence:** test_should_not_duplicate_anti_patterns_verbatim PASS

### AC#2: Rule 2 /tmp/ Prohibition

- [x] /tmp/ stated as FORBIDDEN - **Phase:** 2 - **Evidence:** rule file line 24
- [x] Correct path pattern documented - **Phase:** 2 - **Evidence:** rule file lines 28-30
- [x] Wrong/correct example block - **Phase:** 2 - **Evidence:** rule file lines 32-44

### AC#3: Valid Structure

- [x] YAML frontmatter present - **Phase:** 2 - **Evidence:** rule file lines 1-6
- [x] Under 300 lines - **Phase:** 2 - **Evidence:** 57 lines

### AC#4: Path Clarification

- [x] Project-root relative path specified - **Phase:** 2 - **Evidence:** rule file lines 26-46

### AC#5: Discoverable

- [x] Rules README lists or covers workflow/ - **Phase:** 2 - **Evidence:** README.md line 10

---

**Checklist Progress:** 10/10 items complete (100%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
See: .claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-27

- [x] operational-safety.md created at .claude/rules/workflow/ - Completed: 57-line markdown rule file created with YAML frontmatter and 2 rules
- [x] Rule 1: Cross-reference to anti-patterns.md Category 1 and critical-rules.md Rule 2 - Completed: "See also:" references with exact file paths, no verbatim duplication
- [x] Rule 2: /tmp/ prohibition with correct path pattern and examples - Completed: /tmp/ stated as FORBIDDEN, {project-root}/tmp/{story-id}/ pattern documented with wrong/correct examples
- [x] YAML frontmatter with name, description, version, created - Completed: All 4 fields present in frontmatter
- [x] .gitignore includes tmp/ entry - Completed: tmp/ entry already present in .gitignore (line 3)
- [x] Rules README acknowledges the new file - Completed: workflow/ directory listed in .claude/rules/README.md structure table
- [x] All 5 acceptance criteria have passing tests - Completed: 28 tests covering all 5 ACs (100% pass rate)
- [x] Edge cases covered (WSL paths, missing story ID, prior artifacts) - Completed: WSL portability rationale documented, fallback naming covered
- [x] Cross-references verified via Read() - Completed: anti-patterns.md and critical-rules.md verified to exist
- [x] File within size limits (< 300 lines) - Completed: 57 lines (19% of limit)
- [x] Unit tests for rule file content validation - Completed: test_ac1, test_ac2, test_ac3, test_ac4 (25 tests)
- [x] Unit tests for cross-reference integrity - Completed: test_should_have_referenced_files_exist verifies both files
- [x] Unit test for .gitignore entry - Completed: test_should_have_tmp_in_gitignore
- [x] Integration test for rules discovery - Completed: test_should_have_workflow_listed_in_rules_readme
- [x] Rule file contains clear rationale for each rule - Completed: Portability and traceability rationale in Rule 2
- [x] Wrong/correct examples provided - Completed: Wrong/Correct example blocks for /tmp/ usage
- [x] WSL-specific path note included - Completed: WSL/Windows/Linux portability mentioned in rationale

## Definition of Done

### Implementation
- [x] operational-safety.md created at .claude/rules/workflow/
- [x] Rule 1: Cross-reference to anti-patterns.md Category 1 and critical-rules.md Rule 2
- [x] Rule 2: /tmp/ prohibition with correct path pattern and examples
- [x] YAML frontmatter with name, description, version, created
- [x] .gitignore includes tmp/ entry
- [x] Rules README acknowledges the new file

### Quality
- [x] All 5 acceptance criteria have passing tests
- [x] Edge cases covered (WSL paths, missing story ID, prior artifacts)
- [x] Cross-references verified via Read()
- [x] File within size limits (< 300 lines)

### Testing
- [x] Unit tests for rule file content validation
- [x] Unit tests for cross-reference integrity
- [x] Unit test for .gitignore entry
- [x] Integration test for rules discovery

### Documentation
- [x] Rule file contains clear rationale for each rule
- [x] Wrong/correct examples provided
- [x] WSL-specific path note included

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Phase 02 (Red) | ✅ Complete | 28 tests written, 25 failing (correct RED state) |
| Phase 03 (Green) | ✅ Complete | operational-safety.md created, 28/28 tests passing |
| Phase 04 (Refactor) | ✅ Complete | No refactoring needed (57-line file) |
| Phase 05 (Integration) | ✅ Complete | 28/28 tests passing including integration |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| .claude/rules/workflow/operational-safety.md | Created | 57 |
| tests/STORY-505/conftest.py | Created | 47 |
| tests/STORY-505/test_ac1_rule1_cross_references.py | Created | 93 |
| tests/STORY-505/test_ac2_rule2_tmp_prohibition.py | Created | 84 |
| tests/STORY-505/test_ac3_file_structure.py | Created | 70 |
| tests/STORY-505/test_ac4_path_clarification.py | Created | 39 |
| tests/STORY-505/test_ac5_discoverability.py | Created | 44 |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-27 12:00 | .claude/story-requirements-analyst | Created | Story created from EPIC-085 Feature 5 | STORY-505.story.md |
| 2026-02-27 | /validate-stories | Status Update | Status changed from Backlog to Ready for Dev | STORY-505.story.md |
| 2026-02-27 | .claude/qa-result-interpreter | QA Deep | PASSED: 28/28 tests, 0 blocking violations, 3/3 validators | STORY-505.story.md |

## Notes

**Design Decisions:**
- Rule 1 uses cross-references (not duplication) to avoid stale content if anti-patterns.md is updated
- /tmp/ prohibition is WSL-motivated — /tmp/ resolves to Linux filesystem, not project directory
- Fallback naming (scratch/, ISO date) for when story ID is not yet assigned
- tmp/ must be in .gitignore to prevent accidental tracking

**Related ADRs:**
- [ADR-025: QA Diff Regression Detection](../adrs/ADR-025-qa-diff-regression-detection.md)

**References:**
- EPIC-085: QA Diff Regression Detection and Test Integrity System
- Feature 5: Operational Safety Rules (FR-005)

---

Story Template Version: 2.9
Last Updated: 2026-02-27
