---
id: STORY-350
title: Update tech-stack.md with Treelint
type: documentation
epic: EPIC-055
sprint: Backlog
status: QA Approved
points: 3
depends_on: ["STORY-349"]
priority: P0 - Critical
assigned_to: Unassigned
created: 2026-01-31
format_version: "2.7"
---

# Story: Update tech-stack.md with Treelint

## Description

**As an** AI Agent (subagent/skill),
**I want** Treelint documented in tech-stack.md as an approved tool,
**so that** I can validate my usage against constitutional constraints and know when to use Treelint vs Grep for code search operations.

This story adds Treelint to the "Static Analysis Tools" section of tech-stack.md, replacing the "FUTURE: Tree-sitter Integration (PLANNED)" section with an "APPROVED: Treelint (ADR-013)" section. The update establishes Treelint as the official AST-aware code search tool for DevForgeAI subagents.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-009" section="solution-overview">
    <quote>"Integrate Treelint (AST-aware code search CLI using tree-sitter) into DevForgeAI to provide semantic code navigation that returns functions and classes instead of raw line matches"</quote>
    <line_reference>treelint-integration-requirements.md, lines 27-29</line_reference>
    <quantified_impact>AI agents can validate Treelint usage against constitutional constraints</quantified_impact>
  </origin>

  <decision rationale="constitutional-documentation">
    <selected>Add Treelint to tech-stack.md Static Analysis Tools section</selected>
    <rejected alternative="separate-tools-file">
      Would fragment constitutional documents; tech-stack.md is the single source of truth for tools
    </rejected>
    <trade_off>Increases tech-stack.md length by ~50 lines</trade_off>
  </decision>

  <stakeholder role="AI Agent" goal="constraint-validation">
    <quote>"AI agents can validate Treelint usage against constitutional constraints"</quote>
    <source>EPIC-055, User Story 2</source>
  </stakeholder>

  <hypothesis id="H1" validation="subagent-invocation" success_criteria="Subagents reference tech-stack.md for Treelint guidance">
    Documenting Treelint in tech-stack.md will enable subagents to self-validate their tool usage
  </hypothesis>
</provenance>
```

---

## Acceptance Criteria

### AC#1: Treelint Added to Static Analysis Tools Section

```xml
<acceptance_criteria id="AC1" implements="COMP-001">
  <given>tech-stack.md has a "Static Analysis Tools" section with "FUTURE: Tree-sitter Integration (PLANNED)"</given>
  <when>The tech-stack.md update completes</when>
  <then>A new "APPROVED: Treelint (ADR-013)" subsection exists with status "✅ APPROVED", version constraint "v0.12.0+", and reference to ADR-013</then>
  <verification>
    <source_files>
      <file hint="Constitutional tech-stack">devforgeai/specs/context/tech-stack.md</file>
    </source_files>
    <test_file>tests/STORY-350/test_ac1_treelint_section.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Version Constraint Specified

```xml
<acceptance_criteria id="AC2" implements="COMP-001">
  <given>Treelint section is added to tech-stack.md</given>
  <when>The section content is reviewed</when>
  <then>Version constraint "v0.12.0+" is specified with rationale explaining minimum version requirement</then>
  <verification>
    <source_files>
      <file hint="Constitutional tech-stack">devforgeai/specs/context/tech-stack.md</file>
    </source_files>
    <test_file>tests/STORY-350/test_ac2_version_constraint.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Usage Examples for Subagent Integration Provided

```xml
<acceptance_criteria id="AC3" implements="COMP-001">
  <given>Treelint section exists in tech-stack.md</given>
  <when>A subagent reads the section for guidance</when>
  <then>At least 3 usage examples are provided showing treelint commands with --format json flag for AI consumption</then>
  <verification>
    <source_files>
      <file hint="Constitutional tech-stack">devforgeai/specs/context/tech-stack.md</file>
    </source_files>
    <test_file>tests/STORY-350/test_ac3_usage_examples.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Fallback Behavior Documented

```xml
<acceptance_criteria id="AC4" implements="COMP-001">
  <given>Treelint section exists in tech-stack.md</given>
  <when>A subagent encounters an unsupported file type</when>
  <then>Documentation specifies that Grep should be used as fallback when Treelint is unavailable or file type is unsupported, with explicit language support table</then>
  <verification>
    <source_files>
      <file hint="Constitutional tech-stack">devforgeai/specs/context/tech-stack.md</file>
    </source_files>
    <test_file>tests/STORY-350/test_ac4_fallback_behavior.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Treelint NOT in PROHIBITED Sections

```xml
<acceptance_criteria id="AC5" implements="COMP-001">
  <given>tech-stack.md has various PROHIBITED sections</given>
  <when>The file is searched for "treelint" in PROHIBITED contexts</when>
  <then>Treelint does NOT appear in any PROHIBITED section or with ❌ prefix</then>
  <verification>
    <source_files>
      <file hint="Constitutional tech-stack">devforgeai/specs/context/tech-stack.md</file>
    </source_files>
    <test_file>tests/STORY-350/test_ac5_not_prohibited.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
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
      name: "tech-stack.md"
      file_path: "devforgeai/specs/context/tech-stack.md"
      required_keys:
        - key: "Version"
          type: "semver"
          example: "1.4"
          required: true
          validation: "Increment from 1.3 to 1.4"
          test_requirement: "Test: Verify version incremented"
        - key: "Last Updated"
          type: "date"
          example: "2026-01-31"
          required: true
          validation: "Must be current date"
          test_requirement: "Test: Verify last updated date is today"

  business_rules:
    - id: "BR-001"
      rule: "ADR-013 must be APPROVED before tech-stack.md can be updated"
      trigger: "When attempting to add Treelint section"
      validation: "Check ADR-013 status equals 'APPROVED'"
      error_handling: "HALT with message: 'STORY-349 (ADR approval) must complete first'"
      test_requirement: "Test: Verify dependency on STORY-349"
      priority: "Critical"

    - id: "BR-002"
      rule: "Treelint section must replace FUTURE Tree-sitter section"
      trigger: "When adding Treelint section"
      validation: "FUTURE section removed or updated to APPROVED"
      error_handling: "Flag if both FUTURE and APPROVED sections exist"
      test_requirement: "Test: Verify no duplicate tree-sitter sections"
      priority: "High"

    - id: "BR-003"
      rule: "All treelint commands must include --format json"
      trigger: "When documenting usage examples"
      validation: "Every treelint command example includes --format json"
      error_handling: "Warn if example missing JSON format flag"
      test_requirement: "Test: Verify all examples have --format json"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "tech-stack.md must remain valid Markdown"
      metric: "Zero Markdown syntax errors after update"
      test_requirement: "Test: Validate Markdown structure"
      priority: "High"

    - id: "NFR-002"
      category: "Performance"
      requirement: "File size should not exceed context file limit"
      metric: "tech-stack.md stays under 600 lines (per source-tree.md)"
      test_requirement: "Test: Verify line count under limit"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations: []
# No known limitations for this documentation-focused story
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- N/A - Documentation update, no runtime performance requirements

### Security

**Authentication:**
- None - Framework documentation update

### Reliability

**Error Handling:**
- All tech-stack.md updates should maintain valid Markdown
- Version number must be incremented atomically with content changes

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-349:** Approve ADR-013 Treelint Integration
  - **Why:** ADR must be APPROVED before tech-stack.md can reference it
  - **Status:** Backlog (must complete first)

### External Dependencies

None.

### Technology Dependencies

None - Documentation update only.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ (shell script assertions)

**Test Scenarios:**
1. **Happy Path:** Treelint section added with all required content
2. **Edge Cases:**
   - FUTURE section already removed
   - File already has Treelint section (idempotent)
3. **Error Cases:**
   - Malformed Markdown after edit
   - Missing required subsections

### Integration Tests

**Coverage Target:** 85%

**Test Scenarios:**
1. **Dependency Check:** Verify STORY-349 completion check
2. **Context Validation:** Verify subagents can read and parse Treelint guidance

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

### AC#1: Treelint Added to Static Analysis Tools Section

- [x] New "APPROVED: Treelint (ADR-013)" section created - **Phase:** 3 - **Evidence:** tech-stack.md lines ~98-166
- [x] Status shows "✅ APPROVED" - **Phase:** 3 - **Evidence:** tech-stack.md
- [x] ADR-013 reference included - **Phase:** 3 - **Evidence:** tech-stack.md
- [x] Test validates section exists - **Phase:** 2 - **Evidence:** test_ac1_treelint_section.sh

### AC#2: Version Constraint Specified

- [x] "v0.12.0+" version constraint documented - **Phase:** 3 - **Evidence:** tech-stack.md
- [x] Rationale for minimum version provided - **Phase:** 3 - **Evidence:** tech-stack.md
- [x] Test validates version constraint - **Phase:** 2 - **Evidence:** test_ac2_version_constraint.sh

### AC#3: Usage Examples for Subagent Integration Provided

- [x] `treelint search --type function --format json` example - **Phase:** 3 - **Evidence:** tech-stack.md
- [x] `treelint map --ranked --format json` example - **Phase:** 3 - **Evidence:** tech-stack.md
- [x] `treelint deps --calls --format json` example - **Phase:** 3 - **Evidence:** tech-stack.md
- [x] Test validates 3+ examples with --format json - **Phase:** 2 - **Evidence:** test_ac3_usage_examples.sh

### AC#4: Fallback Behavior Documented

- [x] Grep fallback guidance documented - **Phase:** 3 - **Evidence:** tech-stack.md
- [x] Language support table added (Python, TS, JS, Rust, Markdown) - **Phase:** 3 - **Evidence:** tech-stack.md
- [x] Test validates fallback section - **Phase:** 2 - **Evidence:** test_ac4_fallback_behavior.sh

### AC#5: Treelint NOT in PROHIBITED Sections

- [x] No "❌ treelint" entries in file - **Phase:** 3 - **Evidence:** tech-stack.md
- [x] No treelint in PROHIBITED lists - **Phase:** 3 - **Evidence:** tech-stack.md
- [x] Test validates no prohibited references - **Phase:** 2 - **Evidence:** test_ac5_not_prohibited.sh

---

**Checklist Progress:** 15/15 items complete (100%)

---

## Definition of Done

### Implementation
- [x] "APPROVED: Treelint (ADR-013)" section added to tech-stack.md - Completed: Lines 98-166 in tech-stack.md
- [x] "FUTURE: Tree-sitter Integration (PLANNED)" section updated/replaced - Completed: Replaced with APPROVED: Treelint section
- [x] Version constraint v0.12.0+ documented with rationale - Completed: Lines 108, 110-114 with 4-point rationale
- [x] 3+ usage examples with --format json flag - Completed: 6 examples in lines 127-163
- [x] Fallback behavior to Grep documented - Completed: Lines 149-163 with integration pattern
- [x] Language support table included - Completed: Lines 139-147 with 5 languages
- [x] tech-stack.md version incremented to 1.4 - Completed: Line 5
- [x] Last Updated date set to current date - Completed: Line 4 (2026-01-31)

### Quality
- [x] All 5 acceptance criteria have passing tests - Completed: 5/5 tests pass
- [x] tech-stack.md remains valid Markdown - Completed: Light QA passed
- [x] File stays under 600 line limit - Completed: 560 lines
- [x] No treelint in PROHIBITED sections - Completed: Verified in AC#5 test

### Testing
- [x] test_ac1_treelint_section.sh passes - Completed: All 4 assertions pass
- [x] test_ac2_version_constraint.sh passes - Completed: Both assertions pass
- [x] test_ac3_usage_examples.sh passes - Completed: All 4 assertions pass
- [x] test_ac4_fallback_behavior.sh passes - Completed: All 6 assertions pass
- [x] test_ac5_not_prohibited.sh passes - Completed: Both assertions pass

### Documentation
- [x] tech-stack.md is self-documenting - Completed: Section includes purpose, examples, fallback
- [x] EPIC-055 Stories table updated with this story ID - Completed: Line 285 in EPIC-055

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-01
**Branch:** main

- [x] "APPROVED: Treelint (ADR-013)" section added to tech-stack.md - Completed: Lines 98-166 in tech-stack.md
- [x] "FUTURE: Tree-sitter Integration (PLANNED)" section updated/replaced - Completed: Replaced with APPROVED: Treelint section
- [x] Version constraint v0.12.0+ documented with rationale - Completed: Lines 108, 110-114 with 4-point rationale
- [x] 3+ usage examples with --format json flag - Completed: 6 examples in lines 127-163
- [x] Fallback behavior to Grep documented - Completed: Lines 149-163 with integration pattern
- [x] Language support table included - Completed: Lines 139-147 with 5 languages
- [x] tech-stack.md version incremented to 1.4 - Completed: Line 5
- [x] Last Updated date set to current date - Completed: Line 4 (2026-01-31)
- [x] All 5 acceptance criteria have passing tests - Completed: 5/5 tests pass
- [x] tech-stack.md remains valid Markdown - Completed: Light QA passed
- [x] File stays under 600 line limit - Completed: 560 lines
- [x] No treelint in PROHIBITED sections - Completed: Verified in AC#5 test
- [x] test_ac1_treelint_section.sh passes - Completed: All 4 assertions pass
- [x] test_ac2_version_constraint.sh passes - Completed: Both assertions pass
- [x] test_ac3_usage_examples.sh passes - Completed: All 4 assertions pass
- [x] test_ac4_fallback_behavior.sh passes - Completed: All 6 assertions pass
- [x] test_ac5_not_prohibited.sh passes - Completed: Both assertions pass
- [x] tech-stack.md is self-documenting - Completed: Section includes purpose, examples, fallback
- [x] EPIC-055 Stories table updated with this story ID - Completed: Line 285 in EPIC-055

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-31 12:15 | claude/story-requirements-analyst | Created | Story created from EPIC-055 Feature 2 | STORY-350-update-tech-stack-treelint.story.md |
| 2026-02-01 | claude/opus | TDD Development | Completed all TDD phases, all tests pass | tech-stack.md, tests/STORY-350/*.sh |
| 2026-02-01 | claude/opus | DoD Update (Phase 07) | Development complete, all 18 DoD items verified | STORY-350-update-tech-stack-treelint.story.md |
| 2026-02-01 | claude/qa-result-interpreter | QA Deep | PASSED: 18/18 tests, 100% traceability, 0 violations | devforgeai/qa/reports/STORY-350-qa-report.md |

## Notes

**Design Decisions:**
- Story type is `documentation` because it modifies a constitutional context file
- Phase 05 (Integration) will be skipped per story type classification
- Depends on STORY-349 to ensure ADR governance process is followed

**Content to Add:**

The new Treelint section should include:
1. Status: ✅ APPROVED with ADR reference
2. Version: v0.12.0+ (minimum version with daemon support)
3. Purpose: AST-aware code search for subagents
4. Usage examples with --format json
5. Language support table
6. Fallback guidance (Grep for unsupported types)
7. Integration pattern (Bash tool invocation)

**Open Questions:**
- None

**Related ADRs:**
- [ADR-013: Treelint Integration](../adrs/ADR-013-treelint-integration.md)
- [ADR-007: Remove ast-grep](../adrs/ADR-007-remove-ast-grep-adopt-treesitter.md) - Previous decision this builds upon

**References:**
- [EPIC-055: Treelint Foundation & Distribution](../Epics/EPIC-055-treelint-foundation-distribution.epic.md)
- [treelint-integration-requirements.md](../requirements/treelint-integration-requirements.md)
- [tech-stack.md](../context/tech-stack.md) - Target file for updates

---

Story Template Version: 2.7
Last Updated: 2026-01-31
