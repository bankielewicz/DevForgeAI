---
id: STORY-359
title: Add Treelint Usage Guidance to anti-patterns.md
type: documentation
epic: EPIC-056
sprint: Backlog
status: QA Approved
points: 3
depends_on: ["STORY-349"]
priority: High
advisory: false
assigned_to: Unassigned
created: 2026-02-04
format_version: "2.8"
---

# Story: Add Treelint Usage Guidance to anti-patterns.md

## Description

**As a** DevForgeAI framework contributor,
**I want** anti-patterns.md to include a "Code Search Tool Selection" category (Category 11) documenting when to use Treelint versus Grep,
**so that** subagent authors and framework maintainers avoid wasting tokens on unsupported file types and avoid missing AST-aware precision when it is available.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-009" section="treelint-integration">
    <quote>"AI agents make correct tool choices without trial-and-error"</quote>
    <line_reference>EPIC-056, Feature 3 User Value</line_reference>
    <quantified_impact>99.93% token reduction validated in RESEARCH-007 when using Treelint vs Grep for semantic code search</quantified_impact>
  </origin>

  <decision rationale="anti-pattern-category-format">
    <selected>Add as Category 11 following existing anti-patterns.md format (SEVERITY, FORBIDDEN, Correct, Rationale)</selected>
    <rejected alternative="separate-tool-selection-guide">
      A separate guide would not be discovered by the anti-pattern-scanner subagent during validation
    </rejected>
    <trade_off>Adds ~60-70 lines to anti-patterns.md but ensures automatic detection by existing framework validation</trade_off>
  </decision>
</provenance>
```

---

## Acceptance Criteria

### AC#1: Category 11 Section Structure

```xml
<acceptance_criteria id="AC1" implements="COMP-001">
  <given>anti-patterns.md exists at devforgeai/specs/context/anti-patterns.md with Categories 1-10</given>
  <when>the new "Code Search Tool Selection" section is added as Category 11</when>
  <then>Category 11 is inserted after Category 10 and before the "Anti-Pattern Detection Protocol" section, follows the existing format pattern (Category title with SEVERITY level, FORBIDDEN block with Wrong/Correct examples, and Rationale), and the file header version is bumped from 1.0 to 1.1 with updated date</then>
  <verification>
    <source_files>
      <file hint="Target context file">devforgeai/specs/context/anti-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-359/test_ac1_category_structure.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Anti-Pattern for Using Treelint on Unsupported File Types

```xml
<acceptance_criteria id="AC2" implements="COMP-001">
  <given>Category 11 exists in anti-patterns.md</given>
  <when>a reader looks up guidance on Treelint usage for unsupported file types</when>
  <then>a FORBIDDEN anti-pattern is documented with severity level assigned, showing Wrong example (using Treelint for unsupported extensions like .cs, .java, .go, .sql), Correct example (using Grep for those file types), and Rationale explaining token waste from error responses</then>
  <verification>
    <source_files>
      <file hint="Target context file">devforgeai/specs/context/anti-patterns.md</file>
      <file hint="Supported languages reference">devforgeai/specs/context/tech-stack.md</file>
    </source_files>
    <test_file>tests/STORY-359/test_ac2_unsupported_antipattern.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Anti-Pattern for Using Grep When Treelint Available

```xml
<acceptance_criteria id="AC3" implements="COMP-001">
  <given>Category 11 exists in anti-patterns.md</given>
  <when>a reader looks up guidance on Grep usage for supported file types when Treelint is available</when>
  <then>a FORBIDDEN anti-pattern is documented with severity level assigned, showing Wrong example (using Grep for Python/TypeScript/JavaScript/Rust/Markdown semantic search when Treelint available), Correct example (using Treelint search/map/deps with --format json), and Rationale citing 99.93% token reduction from ADR-013/RESEARCH-007</then>
  <verification>
    <source_files>
      <file hint="Target context file">devforgeai/specs/context/anti-patterns.md</file>
      <file hint="ADR reference">devforgeai/specs/adrs/ADR-013-treelint-integration.md</file>
    </source_files>
    <test_file>tests/STORY-359/test_ac3_grep_misuse_antipattern.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Treelint Recommended Languages Documented

```xml
<acceptance_criteria id="AC4" implements="COMP-001">
  <given>Category 11 exists in anti-patterns.md</given>
  <when>a reader checks which languages Treelint is recommended for</when>
  <then>the section explicitly lists Python (.py), TypeScript (.ts, .tsx), JavaScript (.js, .jsx), Rust (.rs), and Markdown (.md) as Treelint-supported languages matching tech-stack.md lines 139-147, and explicitly states Grep is the correct tool for all other languages, simple text-pattern searches, and as fallback when Treelint is unavailable</then>
  <verification>
    <source_files>
      <file hint="Target context file">devforgeai/specs/context/anti-patterns.md</file>
      <file hint="Language support table">devforgeai/specs/context/tech-stack.md</file>
    </source_files>
    <test_file>tests/STORY-359/test_ac4_supported_languages.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Enforcement Checklist Updated

```xml
<acceptance_criteria id="AC5" implements="COMP-001">
  <given>anti-patterns.md has an "Enforcement Checklist" section with 9 existing items</given>
  <when>Category 11 is added</when>
  <then>a new checklist item is added referencing code search tool selection (e.g., "Use Treelint for supported languages, Grep for unsupported"), bringing the total to 10 items and maintaining consistency with existing checklist format</then>
  <verification>
    <source_files>
      <file hint="Enforcement checklist section">devforgeai/specs/context/anti-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-359/test_ac5_enforcement_checklist.sh</test_file>
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
      name: "anti-patterns.md Category 11"
      file_path: "devforgeai/specs/context/anti-patterns.md"
      required_keys:
        - key: "Category 11 header"
          type: "string"
          example: "### Category 11: Code Search Tool Selection (SEVERITY: MEDIUM)"
          required: true
          validation: "Must be Category 11, after Category 10, before Anti-Pattern Detection Protocol"
          test_requirement: "Test: Grep for 'Category 11' returns exactly 1 match"
        - key: "Unsupported file types anti-pattern"
          type: "string"
          required: true
          validation: "Must include FORBIDDEN block with Wrong/Correct/Rationale"
          test_requirement: "Test: Grep for Treelint + unsupported FORBIDDEN block"
        - key: "Grep misuse anti-pattern"
          type: "string"
          required: true
          validation: "Must include FORBIDDEN block with Wrong/Correct/Rationale"
          test_requirement: "Test: Grep for Grep + Treelint available FORBIDDEN block"
        - key: "Supported languages list"
          type: "string"
          required: true
          validation: "Must list Python, TypeScript, JavaScript, Rust, Markdown with extensions"
          test_requirement: "Test: Grep for all 5 language names and extensions"
        - key: "Enforcement checklist item"
          type: "string"
          required: true
          validation: "Must add 1 new item to existing 9-item checklist"
          test_requirement: "Test: Count checklist items = 10"
        - key: "Version bump"
          type: "string"
          example: "1.1"
          required: true
          validation: "Must increment from 1.0 to 1.1"
          test_requirement: "Test: Grep for Version: 1.1"

  business_rules:
    - id: "BR-001"
      rule: "LOCKED status marker must remain unchanged"
      trigger: "Any modification to anti-patterns.md"
      validation: "Line 3 must contain **Status**: LOCKED"
      error_handling: "HALT if LOCKED marker modified or removed"
      test_requirement: "Test: Verify line 3 contains exact LOCKED marker"
      priority: "Critical"
    - id: "BR-002"
      rule: "Existing Categories 1-10 must be preserved byte-identical"
      trigger: "Adding Category 11"
      validation: "Lines 1-213 must remain unchanged"
      error_handling: "HALT if any existing content modified"
      test_requirement: "Test: Diff anti-patterns.md before/after for lines 1-213"
      priority: "Critical"
    - id: "BR-003"
      rule: "Severity values must use existing scale only"
      trigger: "Assigning severity to new anti-patterns"
      validation: "Only CRITICAL, HIGH, or MEDIUM permitted"
      error_handling: "HALT if non-standard severity used"
      test_requirement: "Test: Grep Category 11 severity values against allowed set"
      priority: "High"
    - id: "BR-004"
      rule: "Language list must match tech-stack.md exactly"
      trigger: "Documenting supported languages"
      validation: "5 languages matching tech-stack.md lines 139-147"
      error_handling: "HALT if language list differs from tech-stack.md"
      test_requirement: "Test: Cross-reference language list against tech-stack.md"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "All 6 context files pass framework validation after change"
      metric: "100% validation pass rate"
      test_requirement: "Test: Run context-validator against all 6 context files"
      priority: "Critical"
    - id: "NFR-002"
      category: "Performance"
      requirement: "anti-patterns.md remains within context file size limit"
      metric: "File under 600 lines (~24,000 characters) per tech-stack.md limits"
      test_requirement: "Test: Count lines in anti-patterns.md, verify < 600"
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
- File size increase: < 3 KB (~60-70 lines added to anti-patterns.md)
- No runtime performance impact (documentation-only)
- AI agent context loading: < 300 additional tokens

### Security
- No secrets or credentials in examples
- No external URLs (reference ADR-013 via relative path only)

### Reliability
- Existing Categories 1-10 must remain byte-identical
- Anti-Pattern Detection Protocol section preserved (repositioned after Category 11)
- All 9 existing enforcement checklist items preserved
- LOCKED marker integrity maintained

### Scalability
- Sequential category numbering supports future additions (Category 12+)
- Language list references tech-stack.md as single source of truth
- Severity levels use existing scale (no new levels)

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-349:** Approve ADR-013 Treelint Integration
  - **Why:** ADR-013 must be approved before adding Treelint references to context files
  - **Status:** QA Approved

### External Dependencies
None.

### Technology Dependencies
None.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ structural validation

**Test Scenarios:**
1. **Happy Path:** Category 11 present with 2 anti-patterns, supported language list, enforcement checklist item
2. **Edge Cases:**
   - Grep remains valid for simple text patterns even in supported languages
   - Treelint unavailable fallback documented (Grep is correct when Treelint not installed)
   - Mixed-language projects use per-file-type tool selection
   - Markdown AST search vs text search distinction
   - Severity level consistency with existing categories
3. **Error Cases:**
   - Missing anti-pattern (fewer than 2 FORBIDDEN blocks)
   - Missing language from supported list
   - Invalid severity value
   - Existing categories modified

### Integration Tests

**Coverage Target:** 85%

**Test Scenarios:**
1. **Context Validation:** All 6 context files pass framework validation
2. **Cross-Reference:** Language list matches tech-stack.md

---

## Acceptance Criteria Verification Checklist

### AC#1: Category 11 Section Structure

- [ ] Category 11 header present in anti-patterns.md - **Phase:** 2 - **Evidence:** tests/STORY-359/test_ac1_category_structure.sh
- [ ] Positioned after Category 10 and before Anti-Pattern Detection Protocol - **Phase:** 2 - **Evidence:** Grep for section ordering
- [ ] Follows existing format (SEVERITY, FORBIDDEN, Correct, Rationale) - **Phase:** 2 - **Evidence:** Grep for format elements
- [ ] Version bumped to 1.1 - **Phase:** 2 - **Evidence:** Grep

### AC#2: Unsupported File Types Anti-Pattern

- [ ] FORBIDDEN block for unsupported file types present - **Phase:** 2 - **Evidence:** tests/STORY-359/test_ac2_unsupported_antipattern.sh
- [ ] Wrong example shows Treelint with unsupported extensions - **Phase:** 2 - **Evidence:** Grep
- [ ] Correct example shows Grep for those types - **Phase:** 2 - **Evidence:** Grep
- [ ] Severity level assigned - **Phase:** 2 - **Evidence:** Grep

### AC#3: Grep Misuse Anti-Pattern

- [ ] FORBIDDEN block for Grep misuse present - **Phase:** 2 - **Evidence:** tests/STORY-359/test_ac3_grep_misuse_antipattern.sh
- [ ] Wrong example shows Grep for supported languages - **Phase:** 2 - **Evidence:** Grep
- [ ] Correct example shows Treelint with --format json - **Phase:** 2 - **Evidence:** Grep
- [ ] ADR-013/RESEARCH-007 token reduction cited - **Phase:** 2 - **Evidence:** Grep

### AC#4: Supported Languages Documented

- [ ] All 5 languages listed with extensions - **Phase:** 2 - **Evidence:** tests/STORY-359/test_ac4_supported_languages.sh
- [ ] Grep recommended for unsupported languages - **Phase:** 2 - **Evidence:** Grep
- [ ] Grep noted as fallback when Treelint unavailable - **Phase:** 2 - **Evidence:** Grep

### AC#5: Enforcement Checklist Updated

- [ ] New checklist item added - **Phase:** 2 - **Evidence:** tests/STORY-359/test_ac5_enforcement_checklist.sh
- [ ] Total checklist items = 10 - **Phase:** 2 - **Evidence:** Grep count

---

**Checklist Progress:** 0/16 items complete (0%)

---

## Definition of Done

### Implementation
- [x] Category 11 "Code Search Tool Selection" added to anti-patterns.md
- [x] Anti-pattern: Using Treelint for unsupported file types (with severity)
- [x] Anti-pattern: Using Grep when Treelint available for supported language (with severity)
- [x] Supported languages list: Python, TypeScript, JavaScript, Rust, Markdown (with extensions)
- [x] Grep recommended for: unsupported languages, simple text patterns, Treelint unavailable
- [x] ADR-013 referenced in rationale
- [x] Enforcement checklist updated (10th item added)
- [x] Version bumped from 1.0 to 1.1
- [x] Last Updated date set to implementation date
- [x] LOCKED status marker preserved

### Quality
- [x] All 5 acceptance criteria have passing tests
- [x] Existing Categories 1-10 byte-identical (diff verification)
- [x] Severity levels use valid values (CRITICAL, HIGH, or MEDIUM)
- [x] Language list matches tech-stack.md exactly
- [x] Format consistent with existing category pattern

### Testing
- [x] tests/STORY-359/test_ac1_category_structure.py passes
- [x] tests/STORY-359/test_ac2_unsupported_antipattern.py passes
- [x] tests/STORY-359/test_ac3_grep_misuse_antipattern.py passes
- [x] tests/STORY-359/test_ac4_supported_languages.py passes
- [x] tests/STORY-359/test_ac5_enforcement_checklist.py passes
- [x] Context-validator passes for all 6 context files

### Documentation
- [x] anti-patterns.md updated (primary deliverable)
- [ ] EPIC-056 Stories table updated with STORY-359 (deferred: epic update is separate admin task)

---

## Implementation Notes

- [x] Category 11 "Code Search Tool Selection" added to anti-patterns.md - Completed: 2026-02-05
- [x] Anti-pattern: Using Treelint for unsupported file types (with severity) - Completed: 2026-02-05
- [x] Anti-pattern: Using Grep when Treelint available for supported language (with severity) - Completed: 2026-02-05
- [x] Supported languages list: Python, TypeScript, JavaScript, Rust, Markdown (with extensions) - Completed: 2026-02-05
- [x] Grep recommended for: unsupported languages, simple text patterns, Treelint unavailable - Completed: 2026-02-05
- [x] ADR-013 referenced in rationale - Completed: 2026-02-05
- [x] Enforcement checklist updated (10th item added) - Completed: 2026-02-05
- [x] Version bumped from 1.0 to 1.1 - Completed: 2026-02-05
- [x] Last Updated date set to implementation date - Completed: 2026-02-05
- [x] LOCKED status marker preserved - Completed: 2026-02-05
- [x] All 5 acceptance criteria have passing tests - Completed: 2026-02-05
- [x] Existing Categories 1-10 byte-identical (diff verification) - Completed: 2026-02-05
- [x] Severity levels use valid values (CRITICAL, HIGH, or MEDIUM) - Completed: 2026-02-05
- [x] Language list matches tech-stack.md exactly - Completed: 2026-02-05
- [x] Format consistent with existing category pattern - Completed: 2026-02-05
- [x] tests/STORY-359/test_ac1_category_structure.py passes - Completed: 2026-02-05
- [x] tests/STORY-359/test_ac2_unsupported_antipattern.py passes - Completed: 2026-02-05
- [x] tests/STORY-359/test_ac3_grep_misuse_antipattern.py passes - Completed: 2026-02-05
- [x] tests/STORY-359/test_ac4_supported_languages.py passes - Completed: 2026-02-05
- [x] tests/STORY-359/test_ac5_enforcement_checklist.py passes - Completed: 2026-02-05
- [x] Context-validator passes for all 6 context files - Completed: 2026-02-05
- [x] anti-patterns.md updated (primary deliverable) - Completed: 2026-02-05

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-04 | claude/story-requirements-analyst | Created | Story created from EPIC-056 Feature 3 | STORY-359-add-treelint-guidance-anti-patterns.story.md |
| 2026-02-05 | claude/dev | Implemented | Added Category 11 to anti-patterns.md | devforgeai/specs/context/anti-patterns.md |
| 2026-02-05 | claude/qa-result-interpreter | QA Deep | PASSED: 53/53 tests, 1/1 validators, 0 violations | - |

## Notes

**Design Decisions:**
- Added as Category 11 (sequential numbering) following existing format pattern
- Two anti-patterns within one category (unsupported types, Grep misuse) — mirrors Category 1 pattern which has multiple forbidden examples
- Grep explicitly noted as valid for simple text patterns even in supported languages (prevents over-application of Treelint anti-pattern)
- Treelint unavailable fallback explicitly documented (prevents false positives in environments without Treelint)

**Edge Cases:**
- Simple text patterns (TODOs, string literals) in supported files: Grep remains valid
- Markdown: AST search adds value for heading structure; Grep for content search
- Mixed-language projects: per-file-type tool selection, not per-project
- Treelint not installed: Grep is correct fallback, not an anti-pattern

**Related ADRs:**
- [ADR-013: Treelint Integration](../adrs/ADR-013-treelint-integration.md)

**References:**
- [EPIC-056: Treelint Context File Integration](../Epics/EPIC-056-treelint-context-file-integration.epic.md)
- [tech-stack.md](../context/tech-stack.md) — Treelint language support table (lines 139-147)
- [RESEARCH-007: Treelint Token Reduction](../research/) — 99.93% token reduction evidence

---

Story Template Version: 2.8
Last Updated: 2026-02-04
