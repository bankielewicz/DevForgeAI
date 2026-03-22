---
id: STORY-330
title: Update source-tree.md for Subagent References
type: refactor
epic: EPIC-053
sprint: Sprint-1
status: QA Approved
points: 1
depends_on: []
priority: High
assigned_to: TBD
created: 2026-01-29
format_version: "2.7"
---

# Story: Update source-tree.md for Subagent References

## Description

**As a** framework maintainer,
**I want** source-tree.md updated to allow `references/` subdirectories for subagents exceeding 500 lines,
**so that** oversized subagents can be refactored using progressive disclosure while maintaining constitutional compliance.

## Provenance

```xml
<provenance>
  <origin document="EPIC-053" section="Feature 0: Constitutional Update">
    <quote>"Problem: source-tree.md line 582 prohibits subagent subdirectories. Solution: Update source-tree.md to allow references/ subdirectories for subagents >500 lines"</quote>
    <line_reference>lines 56-61</line_reference>
    <quantified_impact>Enables refactoring of 26 oversized subagents (81% of total)</quantified_impact>
  </origin>

  <decision rationale="progressive-disclosure-for-token-efficiency">
    <selected>Allow references/ subdirectories for subagents exceeding 500 lines</selected>
    <rejected alternative="raise-limit">Raising the 500-line limit doesn't solve token efficiency problem</rejected>
    <rejected alternative="split-subagents">Creates coordination complexity; single-responsibility already followed</rejected>
    <trade_off>More files to maintain, but 60-80% token reduction per invocation</trade_off>
  </decision>

  <hypothesis id="H1" validation="line-count-measurement" success_criteria="All 4 CRITICAL subagents reduced to ≤300 lines">
    Progressive disclosure pattern will achieve constitutional compliance while maintaining subagent functionality
  </hypothesis>
</provenance>
```

---

## Acceptance Criteria

### AC#1: Remove Prohibition on Subagent Subdirectories

```xml
<acceptance_criteria id="AC1">
  <given>source-tree.md line 582 states "NO subdirectories in `.claude/agents/`"</given>
  <when>the constitutional update is applied</when>
  <then>the blanket prohibition is removed and replaced with conditional permission for references/ subdirectories only when subagent exceeds 500 lines</then>
  <verification>
    <source_files>
      <file hint="Constitutional document">devforgeai/specs/context/source-tree.md</file>
    </source_files>
    <test_file>tests/STORY-330/test_ac1_prohibition_removed.py</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Add Progressive Disclosure Pattern for Subagents

```xml
<acceptance_criteria id="AC2">
  <given>tech-stack.md lines 355-358 prescribe progressive disclosure for oversized components</given>
  <when>the source-tree.md .claude/agents/ section is updated</when>
  <then>a new rule is added specifying: "references/ subdirectory ALLOWED for subagents exceeding 500 lines (progressive disclosure per tech-stack.md)"</then>
  <verification>
    <source_files>
      <file hint="Constitutional document">devforgeai/specs/context/source-tree.md</file>
    </source_files>
    <test_file>tests/STORY-330/test_ac2_progressive_disclosure_rule.py</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Document Directory Structure Pattern

```xml
<acceptance_criteria id="AC3">
  <given>ADR-012 defines the approved directory pattern for subagent progressive disclosure</given>
  <when>source-tree.md is updated</when>
  <then>the directory structure example shows the new pattern with {subagent-name}/ containing references/ subdirectory alongside the main {subagent-name}.md file</then>
  <verification>
    <source_files>
      <file hint="Constitutional document">devforgeai/specs/context/source-tree.md</file>
    </source_files>
    <test_file>tests/STORY-330/test_ac3_directory_structure_example.py</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Maintain Backward Compatibility

```xml
<acceptance_criteria id="AC4">
  <given>6 existing subagents are under 500 lines and require no refactoring</given>
  <when>the source-tree.md update is applied</when>
  <then>the updated rules explicitly state that subagents under 500 lines remain as single .md files with no subdirectory required</then>
  <verification>
    <source_files>
      <file hint="Constitutional document">devforgeai/specs/context/source-tree.md</file>
    </source_files>
    <test_file>tests/STORY-330/test_ac4_backward_compatibility.py</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Cross-Reference ADR-012

```xml
<acceptance_criteria id="AC5">
  <given>ADR-012 is the authoritative decision record for this constitutional change</given>
  <when>source-tree.md is updated</when>
  <then>a reference to ADR-012 is added in the .claude/agents/ section documenting the rationale for allowing references/ subdirectories</then>
  <verification>
    <source_files>
      <file hint="Constitutional document">devforgeai/specs/context/source-tree.md</file>
    </source_files>
    <test_file>tests/STORY-330/test_ac5_adr_reference.py</test_file>
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
      name: "source-tree.md"
      file_path: "devforgeai/specs/context/source-tree.md"
      purpose: "Constitutional document defining framework directory structure"
      required_keys:
        - key: ".claude/agents/ Rules"
          type: "markdown_section"
          example: "Rules section with progressive disclosure pattern"
          required: true
          validation: "Must contain conditional permission for references/ subdirectories"
          test_requirement: "Test: Grep for 'references/' permission rule exists"
        - key: "Directory structure example"
          type: "markdown_codeblock"
          example: "Code block showing {subagent}.md + {subagent}/references/ pattern"
          required: true
          validation: "Must show side-by-side structure"
          test_requirement: "Test: Validate directory tree example present"
        - key: "ADR-012 reference"
          type: "markdown_link"
          example: "(per ADR-012)"
          required: true
          validation: "Must reference ADR-012 for decision traceability"
          test_requirement: "Test: Grep for 'ADR-012' returns match"
      requirements:
        - id: "CFG-001"
          description: "Remove blanket prohibition on subagent subdirectories"
          testable: true
          test_requirement: "Test: Grep for 'NO subdirectories' in .claude/agents section returns 0 matches"
          priority: "Critical"
        - id: "CFG-002"
          description: "Add conditional permission for references/ when subagent >500 lines"
          testable: true
          test_requirement: "Test: Section contains '500 lines' threshold rule"
          priority: "Critical"
        - id: "CFG-003"
          description: "Add directory structure example per ADR-012"
          testable: true
          test_requirement: "Test: Code block shows {subagent}.md alongside {subagent}/references/"
          priority: "High"
        - id: "CFG-004"
          description: "Maintain backward compatibility statement"
          testable: true
          test_requirement: "Test: Section states subagents <=500 lines remain single-file"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Subagents MUST exceed 500 lines to qualify for references/ subdirectory"
      trigger: "When evaluating if subagent can have subdirectory"
      validation: "Line count measured by wc -l or equivalent"
      error_handling: "Subagents at or below 500 lines remain single .md file"
      test_requirement: "Test: Verify threshold is '>500' not '>=500'"
      priority: "Critical"
    - id: "BR-002"
      rule: "Subdirectory MUST be named 'references/' (exact, lowercase)"
      trigger: "When creating subagent subdirectory"
      validation: "No alternatives like refs/, reference/, or References/"
      error_handling: "Reject non-conforming directory names"
      test_requirement: "Test: Document specifies 'references/' exactly"
      priority: "High"
    - id: "BR-003"
      rule: "Parent directory MUST match subagent filename without .md extension"
      trigger: "When organizing subagent with references"
      validation: "test-automator.md -> test-automator/references/"
      error_handling: "Naming mismatch blocks refactoring"
      test_requirement: "Test: Example shows matching names"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Document update adds minimal content"
      metric: "< 50 lines added to source-tree.md"
      test_requirement: "Test: Diff shows <50 lines added"
      priority: "Medium"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "No conflicts with other constitutional documents"
      metric: "0 conflicts with tech-stack.md, anti-patterns.md, coding-standards.md"
      test_requirement: "Test: Constitutional validation passes after update"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations: []
# No limitations identified - this is a straightforward documentation update
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Document Size:**
- source-tree.md update adds < 50 lines (minimal impact on context loading)
- No measurable impact on parse time

---

### Security

**No security implications:** Constitutional document update only, no code execution changes.

---

### Reliability

**Backward Compatibility:** 100% - existing small subagents unchanged
**Constitutional Consistency:** 0 conflicts with other context files after update
**ADR Alignment:** 100% alignment with ADR-012 approved pattern

---

### Scalability

**Supports all 26 oversized subagents:** Pattern applicable to all subagents exceeding 500 lines
**Future-proof:** Pattern works for subagents not yet created

---

## Dependencies

### Prerequisite Stories

- [ ] **None** - This is a prerequisite for STORY-331, STORY-332, STORY-333, STORY-334

### External Dependencies

- [x] **ADR-012:** Subagent Progressive Disclosure Architecture (approved)
  - **Status:** Approved
  - **Impact:** Provides the approved pattern this story implements

### Technology Dependencies

- [ ] **None** - No new packages required (markdown documentation only)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 100% of acceptance criteria

**Test Scenarios:**
1. **AC1 - Prohibition Removed:** Verify "NO subdirectories" text is NOT in updated .claude/agents/ section
2. **AC2 - Progressive Disclosure Rule:** Verify rule for references/ when >500 lines exists
3. **AC3 - Directory Structure Example:** Verify code block shows correct pattern
4. **AC4 - Backward Compatibility:** Verify statement about subagents <=500 lines
5. **AC5 - ADR Reference:** Verify ADR-012 is referenced in section

### Edge Cases

1. **Subagent at exactly 500 lines:** Threshold is ">500" (strictly greater than)
2. **Multiple reference files:** Pattern accommodates many reference files
3. **Nested subdirectories:** Pattern prohibits deeper nesting beyond references/
4. **Naming conflicts:** Pattern clarifies {subagent}.md and {subagent}/ coexist

---

## Acceptance Criteria Verification Checklist

### AC#1: Remove Prohibition on Subagent Subdirectories

- [x] Original prohibition text identified (line 582) - **Phase:** 2 - **Evidence:** source-tree.md line 582
- [x] Blanket prohibition removed - **Phase:** 3 - **Evidence:** Edit applied to line 582
- [x] Conditional permission added - **Phase:** 3 - **Evidence:** Line 582 now allows references/ for >500 lines

### AC#2: Add Progressive Disclosure Pattern for Subagents

- [x] tech-stack.md reference verified - **Phase:** 2 - **Evidence:** Lines 355-358 (progressive disclosure)
- [x] New rule added specifying >500 line threshold - **Phase:** 3 - **Evidence:** Lines 582, 588
- [x] Rule aligned with tech-stack.md enforcement section - **Phase:** 4 - **Evidence:** Validated by context-validator

### AC#3: Document Directory Structure Pattern

- [x] ADR-012 pattern extracted - **Phase:** 2 - **Evidence:** ADR-012 read (lines 52-62)
- [x] Directory structure code block added - **Phase:** 3 - **Evidence:** Lines 590-598
- [x] Pattern shows {subagent}.md + {subagent}/references/ - **Phase:** 4 - **Evidence:** test_example_shows_coexistence_pattern PASSED

### AC#4: Maintain Backward Compatibility

- [x] Backward compatibility statement added - **Phase:** 3 - **Evidence:** Line 583
- [x] Small subagents (<= 500 lines) explicitly covered - **Phase:** 4 - **Evidence:** test_backward_compatibility_statement_exists PASSED

### AC#5: Cross-Reference ADR-012

- [x] ADR-012 reference added to section - **Phase:** 3 - **Evidence:** Lines 582, 586
- [x] Reference provides decision traceability - **Phase:** 4 - **Evidence:** test_adr_reference_provides_context PASSED

---

**Checklist Progress:** 14/14 items complete (100%)

---

## Definition of Done

### Implementation
- [x] source-tree.md .claude/agents/ section updated
- [x] Blanket prohibition removed
- [x] Conditional permission for references/ added
- [x] Directory structure example added
- [x] Backward compatibility statement added
- [x] ADR-012 reference added

### Quality
- [x] All 5 acceptance criteria have passing tests
- [x] Edge cases documented (threshold, naming, nesting)
- [x] Constitutional consistency validated (no conflicts with other context files)
- [x] ADR-012 alignment verified

### Testing
- [x] Test: Prohibition text removed from section
- [x] Test: Progressive disclosure rule present
- [x] Test: Directory example shows correct pattern
- [x] Test: Backward compatibility statement exists
- [x] Test: ADR-012 referenced in section

### Documentation
- [x] source-tree.md Version number incremented
- [x] source-tree.md Last Updated date updated
- [x] Change documented in source-tree.md changelog (if exists)

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent (claude/opus)
**Implemented:** 2026-01-30
**Branch:** main

- [x] source-tree.md .claude/agents/ section updated - Completed: Lines 576-605 modified with progressive disclosure pattern
- [x] Blanket prohibition removed - Completed: Line 582 changed from "NO subdirectories" to conditional ALLOWED permission
- [x] Conditional permission for references/ added - Completed: Line 582 now allows references/ for subagents >500 lines
- [x] Directory structure example added - Completed: Lines 590-598 show test-automator.md + test-automator/references/ pattern
- [x] Backward compatibility statement added - Completed: Line 583 states ≤500 line subagents remain single .md files
- [x] ADR-012 reference added - Completed: Referenced in lines 582, 586 and version header
- [x] All 5 acceptance criteria have passing tests - Completed: 11 tests across 5 test files (100% pass rate)
- [x] Edge cases documented (threshold, naming, nesting) - Completed: Lines 600-604 document pattern requirements
- [x] Constitutional consistency validated (no conflicts with other context files) - Completed: context-validator confirmed no conflicts
- [x] ADR-012 alignment verified - Completed: Pattern matches ADR-012 lines 52-62 exactly
- [x] source-tree.md Version number incremented - Completed: Version 3.4
- [x] source-tree.md Last Updated date updated - Completed: 2026-01-30

### TDD Workflow Summary

**Phase 02 (Red):** Generated 11 tests across 5 files covering all 5 ACs
**Phase 03 (Green):** Updated source-tree.md lines 576-605 via backend-architect
**Phase 04 (Refactor):** Documentation quality reviewed - no changes needed
**Phase 05 (Integration):** Cross-component consistency validated with tech-stack.md, architecture-constraints.md, ADR-012

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-29 09:00 | claude/story-requirements-analyst | Created | Story created from EPIC-053 Feature 0 | STORY-330.story.md |
| 2026-01-30 | claude/opus | Development Complete | TDD workflow complete, all 5 ACs verified | source-tree.md, tests/STORY-330/*.py |
| 2026-01-30 | claude/qa-result-interpreter | QA Deep | PASSED: Tests 11/11, Validators 2/2, 0 violations | - |

## Notes

**Design Decisions:**
- Threshold is ">500" (strictly greater than) to avoid ambiguity at exactly 500 lines
- Only `references/` subdirectory allowed (not custom names) for consistency
- Pattern mirrors skills progressive disclosure for framework consistency

**Related ADRs:**
- [ADR-012: Subagent Progressive Disclosure Architecture](../adrs/ADR-012-subagent-progressive-disclosure.md)

**References:**
- EPIC-053: Subagent Progressive Disclosure Refactoring
- RESEARCH-006: Subagent Progressive Disclosure Analysis
- tech-stack.md lines 355-358 (enforcement section)
- source-tree.md lines 572-621 (.claude/agents/ section)

---

Story Template Version: 2.7
Last Updated: 2026-01-29
