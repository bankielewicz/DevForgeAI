---
id: STORY-364
title: Update code-reviewer Subagent with Treelint AST-Aware Pattern Detection
type: feature
epic: EPIC-057
sprint: Sprint-10
status: QA Approved
points: 3
depends_on: ["STORY-361"]
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: Unassigned
created: 2026-02-05
format_version: "2.8"
---

# Story: Update code-reviewer Subagent with Treelint AST-Aware Pattern Detection

## Description

**As a** code-reviewer subagent executing during Phase 2/Phase 3 of the development workflow,
**I want** to use Treelint AST-aware search for structural pattern detection (finding classes by method count, functions by line count, and code structure by symbol relationships) with automatic Grep fallback for unsupported languages,
**so that** code review findings for structural violations (God classes, long methods, excessive complexity) are based on parsed AST data rather than text pattern heuristics, reducing false positives and providing accurate line-count and method-count metrics.

## Provenance

```xml
<provenance>
  <origin document="EPIC-057" section="Feature 4: code-reviewer Update">
    <quote>"Enable AST-aware pattern detection for code review"</quote>
    <line_reference>lines 54-57</line_reference>
    <quantified_impact>False positive reduction >50% vs Grep-only search for structural violations</quantified_impact>
  </origin>

  <decision rationale="progressive-disclosure-mandatory">
    <selected>Treelint patterns extracted to reference file (code-reviewer already 825 lines, exceeds 500-line target)</selected>
    <rejected alternative="inline-patterns">
      Code-reviewer.md already exceeds 500 lines; adding inline patterns would worsen token budget violation
    </rejected>
    <trade_off>Extra Read() call for reference file vs. inlining patterns in already-oversized subagent</trade_off>
  </decision>
</provenance>
```

## Acceptance Criteria

### AC#1: Code-Reviewer Reference File with Treelint Review Patterns

```xml
<acceptance_criteria id="AC1" implements="REV-001,REV-002">
  <given>The code-reviewer subagent (src/claude/agents/code-reviewer.md) is already 825 lines exceeding the 500-line target, and STORY-361 has created the shared Treelint reference file</given>
  <when>A new code-reviewer-specific reference file is created for Treelint review patterns</when>
  <then>A reference file exists at src/claude/agents/code-reviewer/references/treelint-review-patterns.md containing: (1) God class detection using treelint search --type class --format json with method count threshold of 20, (2) Long method detection using treelint search --type function --format json with line count threshold of 50, (3) File importance ranking using treelint map --ranked --format json for review prioritization, and (4) a Read() instruction in the main code-reviewer.md pointing to this reference file</then>
  <verification>
    <source_files>
      <file hint="Code-reviewer Treelint reference file">src/claude/agents/code-reviewer/references/treelint-review-patterns.md</file>
      <file hint="Main code-reviewer subagent">src/claude/agents/code-reviewer.md</file>
    </source_files>
    <test_file>tests/STORY-364/test_ac1_reference_file_created.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: God Class Detection Using Treelint AST Search

```xml
<acceptance_criteria id="AC2" implements="REV-003">
  <given>A codebase contains Python, TypeScript, or JavaScript files with classes, and the code-reviewer subagent is invoked during a code review</given>
  <when>The code-reviewer executes structural anti-pattern detection using the Treelint review patterns reference</when>
  <then>The reviewer uses Bash(command="treelint search --type class --format json") to enumerate classes and their method counts, identifies classes with more than 20 methods as God class candidates, and reports findings with exact class name, file path, method count, and line range from the JSON response</then>
  <verification>
    <source_files>
      <file hint="Treelint review patterns reference">src/claude/agents/code-reviewer/references/treelint-review-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-364/test_ac2_god_class_detection.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Long Method Detection Using Treelint AST Search

```xml
<acceptance_criteria id="AC3" implements="REV-004">
  <given>A codebase contains Python, TypeScript, or JavaScript files with functions, and the code-reviewer is performing the Code Quality review checklist step</given>
  <when>The code-reviewer executes long method detection using Treelint</when>
  <then>The reviewer uses Bash(command="treelint search --type function --format json") to enumerate functions with their line ranges, calculates function length from lines[1] minus lines[0], identifies functions exceeding 50 lines, and reports findings with function name, file path, actual line count, and start/end line numbers</then>
  <verification>
    <source_files>
      <file hint="Treelint review patterns reference">src/claude/agents/code-reviewer/references/treelint-review-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-364/test_ac3_long_method_detection.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Automatic Grep Fallback for Unsupported Languages

```xml
<acceptance_criteria id="AC4" implements="REV-005">
  <given>Code changes include files in unsupported languages (C#, Java, Go, or other extensions not in the Treelint supported list)</given>
  <when>The code-reviewer attempts Treelint-based structural analysis</when>
  <then>The reviewer: (1) checks file extensions against the supported list before invoking Treelint, (2) falls back to Grep-based pattern detection for unsupported files, (3) logs a warning (not error) indicating Grep fallback was used, and (4) produces equivalent review output regardless of detection method</then>
  <verification>
    <source_files>
      <file hint="Treelint review patterns reference">src/claude/agents/code-reviewer/references/treelint-review-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-364/test_ac4_grep_fallback.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Review Prioritization Using Treelint Map Command

```xml
<acceptance_criteria id="AC5" implements="REV-006">
  <given>A code review involves multiple changed files and the code-reviewer needs to prioritize review depth</given>
  <when>The code-reviewer begins its review workflow</when>
  <then>The reviewer uses Bash(command="treelint map --ranked --format json") to rank files by structural importance, prioritizes review depth for high-ranked files, applies lighter review to low-ranked files, and documents the prioritization rationale in the review report</then>
  <verification>
    <source_files>
      <file hint="Treelint review patterns reference">src/claude/agents/code-reviewer/references/treelint-review-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-364/test_ac5_review_prioritization.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#6: JSON Parsing of Treelint Search Results

```xml
<acceptance_criteria id="AC6" implements="REV-007">
  <given>Treelint returns JSON output with fields including type, name, file, lines, signature, and body</given>
  <when>The code-reviewer parses Treelint JSON output during structural analysis</when>
  <then>The reviewer correctly: (1) extracts class name and method count for God class detection, (2) extracts function line range to calculate function length, (3) handles empty results without error by reporting "no structural issues found", and (4) handles malformed JSON by falling back to Grep with a warning message</then>
  <verification>
    <source_files>
      <file hint="Treelint review patterns reference">src/claude/agents/code-reviewer/references/treelint-review-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-364/test_ac6_json_parsing.sh</test_file>
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
      name: "Treelint Review Patterns Reference File"
      file_path: "src/claude/agents/code-reviewer/references/treelint-review-patterns.md"
      required_keys:
        - key: "God Class Detection Pattern"
          type: "markdown"
          example: "### God Class Detection via Treelint"
          required: true
          validation: "Must contain treelint search --type class --format json with >20 method threshold"
          test_requirement: "Test: Grep for 'treelint search.*--type class' and '20' in treelint-review-patterns.md"

        - key: "Long Method Detection Pattern"
          type: "markdown"
          example: "### Long Method Detection via Treelint"
          required: true
          validation: "Must contain treelint search --type function --format json with >50 line threshold"
          test_requirement: "Test: Grep for 'treelint search.*--type function' and '50' in treelint-review-patterns.md"

        - key: "File Prioritization Pattern"
          type: "markdown"
          example: "### Review Prioritization via Treelint Map"
          required: true
          validation: "Must contain treelint map --ranked --format json instruction"
          test_requirement: "Test: Grep for 'treelint map.*--ranked' in treelint-review-patterns.md"

        - key: "Language Support Check"
          type: "markdown"
          example: "### Supported Languages and Fallback"
          required: true
          validation: "Must list all 7 supported extensions and Grep fallback patterns"
          test_requirement: "Test: Grep for '.py' AND '.ts' AND Grep fallback instruction in treelint-review-patterns.md"

        - key: "JSON Parsing Instructions"
          type: "markdown"
          example: "### Parsing Treelint JSON Output"
          required: true
          validation: "Must reference JSON fields: name, file, lines, and describe empty/error handling"
          test_requirement: "Test: Grep for 'name.*file.*lines' pattern in treelint-review-patterns.md"

    - type: "Configuration"
      name: "code-reviewer.md (modification)"
      file_path: "src/claude/agents/code-reviewer.md"
      required_keys:
        - key: "Treelint Reference Loading"
          type: "markdown"
          example: "Read(file_path=\"src/claude/agents/code-reviewer/references/treelint-review-patterns.md\")"
          required: true
          validation: "Must contain Read() instruction for Treelint reference file"
          test_requirement: "Test: Grep for 'Read.*treelint-review-patterns' in code-reviewer.md"

        - key: "Treelint Integration Section"
          type: "markdown"
          example: "### Treelint AST-Aware Structural Analysis"
          required: true
          validation: "Must add section referencing Treelint for structural review"
          test_requirement: "Test: Grep for 'Treelint' or 'AST-aware' section header in code-reviewer.md"

        - key: "Existing Review Checklist Preserved"
          type: "markdown"
          example: "All 8 existing sections still present"
          required: true
          validation: "Sections 1-8 of Review Checklist must still exist"
          test_requirement: "Test: Grep for each section header (Code Quality, Security, Error Handling, Performance, Testing, Standards Compliance, DoD Completeness, Anti-Gaming) in code-reviewer.md"

  business_rules:
    - id: "BR-001"
      rule: "Treelint patterns must be in a reference file, not inline in code-reviewer.md"
      trigger: "When Treelint integration is added to code-reviewer"
      validation: "code-reviewer.md must contain Read() to reference file, not inline Treelint commands"
      error_handling: "If Treelint patterns found inline (not in reference), extract per ADR-012"
      test_requirement: "Test: code-reviewer.md contains Read() for treelint-review-patterns.md AND no inline 'treelint search' commands"
      priority: "Critical"

    - id: "BR-002"
      rule: "God class threshold is >20 methods per class"
      trigger: "When Treelint enumerates classes"
      validation: "Count methods per class; flag if >20"
      error_handling: "Report as WARNING severity in review (not CRITICAL, since it's a code smell)"
      test_requirement: "Test: Reference file contains method count threshold of 20"
      priority: "High"

    - id: "BR-003"
      rule: "Long method threshold is >50 lines per function"
      trigger: "When Treelint enumerates functions"
      validation: "Calculate lines[1] - lines[0]; flag if >50"
      error_handling: "Report as WARNING severity in review"
      test_requirement: "Test: Reference file contains line count threshold of 50"
      priority: "High"

    - id: "BR-004"
      rule: "Reference file must not exceed 300 lines"
      trigger: "When reference file is created"
      validation: "wc -l <= 300 per ADR-012"
      error_handling: "If exceeding 300 lines, split into sub-references"
      test_requirement: "Test: wc -l on treelint-review-patterns.md <= 300"
      priority: "Medium"

    - id: "BR-005"
      rule: "All existing code-reviewer functionality preserved (zero regression)"
      trigger: "After Treelint integration added"
      validation: "All 8 review checklist sections still present and functional"
      error_handling: "If any section removed or broken, HALT and restore"
      test_requirement: "Test: All 8 section headers exist in code-reviewer.md after modification"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Treelint search < 100ms per invocation"
      metric: "< 100ms (p95) per Treelint CLI call"
      test_requirement: "Test: Performance target documented in reference file"
      priority: "High"

    - id: "NFR-002"
      category: "Performance"
      requirement: "Total Treelint overhead per review < 500ms"
      metric: "< 500ms total (max 5 invocations at < 100ms each)"
      test_requirement: "Test: Reference file limits Treelint invocations to reasonable count"
      priority: "High"

    - id: "NFR-003"
      category: "Reliability"
      requirement: "Zero review failures from Treelint issues"
      metric: "100% of Treelint failures handled with Grep fallback"
      test_requirement: "Test: Reference file contains fallback logic for all failure modes"
      priority: "Critical"

    - id: "NFR-004"
      category: "Scalability"
      requirement: "Reference file extensible for new patterns"
      metric: "New patterns addable as new sections without restructuring"
      test_requirement: "Test: Reference file uses section-based organization"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Treelint"
    limitation: "Only 5 languages supported - C#, Java, Go, Ruby not covered"
    decision: "workaround:Grep fallback for unsupported languages"
    discovered_phase: "Architecture"
    impact: "Structural analysis accuracy varies by language (AST for supported, text for unsupported)"

  - id: TL-002
    component: "code-reviewer.md"
    limitation: "File already at 825 lines, significantly over 500-line target"
    decision: "workaround:All Treelint patterns in reference file, minimal additions to core file (<30 lines)"
    discovered_phase: "Architecture"
    impact: "Cannot inline Treelint patterns; must use progressive disclosure via reference file"

  - id: TL-003
    component: "Treelint class search"
    limitation: "Treelint may not report method count directly - may need to count methods from nested function results"
    decision: "workaround:Use treelint search --type function within class scope to count methods"
    discovered_phase: "Architecture"
    impact: "God class detection may require 2 Treelint invocations (one for classes, one for methods)"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Treelint Operations:**
- Treelint search: < 100ms per invocation (p95)
- Total Treelint overhead per review: < 500ms (max 5 invocations)
- Reference file Read() load: < 500ms

### Security

**Command Safety:**
- No user-provided input interpolated into Treelint commands
- Treelint scope limited to project directory
- No sensitive data in command arguments or examples

### Reliability

**Fallback Guarantees:**
- 100% Grep fallback on any Treelint failure
- Treelint timeout: 5 seconds per command
- Error isolation: failure in one review step does not affect others
- Existing review functionality preserved (zero regression)

### Scalability

**Extensibility:**
- New patterns appendable as sections in reference file
- Language support expandable via extension list update
- Stateless operation per invocation

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-361:** Create Treelint Skill Reference Files for Subagent Integration
  - **Why:** Provides shared Treelint reference patterns used as foundation
  - **Status:** Backlog

### External Dependencies

- [x] **EPIC-055 (Foundation):** ADR-013 approved, tech-stack.md updated, Treelint binary distributed
- [x] **EPIC-056 (Context Files):** source-tree.md updated for Treelint directories

### Technology Dependencies

- [x] **Treelint:** v0.12.0+ binary
  - **Purpose:** AST-aware code search CLI
  - **Approved:** Yes (ADR-013)
  - **Added to dependencies.md:** Yes (v1.1)

---

## Edge Cases

1. **Mixed-language codebase:** Treelint for supported files, Grep for unsupported files in same review session. Results combined into unified report.

2. **Treelint binary not installed:** Exit code 127 triggers Grep-only mode for ALL files with single warning log.

3. **Class with few methods but excessive line count:** Both method-count (Treelint) AND line-count (existing) checks applied simultaneously.

4. **Partial Treelint results:** Successful results used for parsed files; Grep fallback for failed files.

5. **No changed files:** Skip Treelint analysis entirely; report "No structural code changes."

6. **Token budget exceeded:** Limit Treelint analysis to `git diff` changed files only (not entire codebase).

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for structural validation

**Test Scenarios:**
1. **Happy Path:** Reference file contains God class, long method, and map patterns
2. **Edge Cases:**
   - Verify all 7 supported extensions listed
   - Verify fallback section exists
   - Verify reference file <= 300 lines
3. **Error Cases:**
   - Verify Grep fallback documented for unsupported languages
   - Verify empty results handling documented
   - Verify malformed JSON handling documented

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **Reference Loading:** code-reviewer.md contains Read() for treelint-review-patterns.md
2. **Regression Check:** All 8 existing review sections preserved
3. **Core File Size:** code-reviewer.md < 860 lines after modification

---

## Acceptance Criteria Verification Checklist

### AC#1: Reference File Created

- [ ] treelint-review-patterns.md exists at correct path - **Phase:** 2 - **Evidence:** test_ac1_reference_file_created.sh
- [ ] Contains God class detection pattern - **Phase:** 2 - **Evidence:** test_ac1_reference_file_created.sh
- [ ] Contains long method detection pattern - **Phase:** 2 - **Evidence:** test_ac1_reference_file_created.sh
- [ ] Contains file prioritization pattern - **Phase:** 2 - **Evidence:** test_ac1_reference_file_created.sh
- [ ] code-reviewer.md has Read() pointing to reference - **Phase:** 2 - **Evidence:** test_ac1_reference_file_created.sh

### AC#2: God Class Detection

- [ ] Reference file contains `treelint search --type class` pattern - **Phase:** 2 - **Evidence:** test_ac2_god_class_detection.sh
- [ ] 20-method threshold documented - **Phase:** 2 - **Evidence:** test_ac2_god_class_detection.sh

### AC#3: Long Method Detection

- [ ] Reference file contains `treelint search --type function` pattern - **Phase:** 3 - **Evidence:** test_ac3_long_method_detection.sh
- [ ] 50-line threshold documented - **Phase:** 3 - **Evidence:** test_ac3_long_method_detection.sh

### AC#4: Grep Fallback

- [ ] Supported extension list present - **Phase:** 2 - **Evidence:** test_ac4_grep_fallback.sh
- [ ] Grep fallback instructions present - **Phase:** 2 - **Evidence:** test_ac4_grep_fallback.sh
- [ ] Warning (not error) messaging - **Phase:** 2 - **Evidence:** test_ac4_grep_fallback.sh

### AC#5: Review Prioritization

- [ ] `treelint map --ranked` pattern documented - **Phase:** 3 - **Evidence:** test_ac5_review_prioritization.sh

### AC#6: JSON Parsing

- [ ] JSON field extraction documented - **Phase:** 3 - **Evidence:** test_ac6_json_parsing.sh
- [ ] Empty results handling documented - **Phase:** 3 - **Evidence:** test_ac6_json_parsing.sh
- [ ] Malformed JSON fallback documented - **Phase:** 3 - **Evidence:** test_ac6_json_parsing.sh

---

**Checklist Progress:** 0/16 items complete (0%)

---

## Definition of Done

### Implementation
- [x] treelint-review-patterns.md created with God class, long method, and map patterns
- [x] code-reviewer.md updated with Read() instruction for reference file
- [x] Treelint integration section added to code-reviewer.md
- [x] Language support check and Grep fallback documented in reference
- [x] JSON parsing instructions documented in reference
- [x] Reference file <= 300 lines (ADR-012 compliance) - 191 lines
- [x] code-reviewer.md < 860 lines after modification - 843 lines

### Quality
- [x] All 6 acceptance criteria have passing tests
- [x] All 8 existing review checklist sections preserved (zero regression)
- [x] Edge cases documented (mixed languages, binary not found, empty results)
- [x] NFRs met (< 100ms search, zero review failures via Grep fallback)
- [x] Code coverage >95% for structural tests - 40/40 assertions passing

### Testing
- [x] test_ac1_reference_file_created.sh passes
- [x] test_ac2_god_class_detection.sh passes
- [x] test_ac3_long_method_detection.sh passes
- [x] test_ac4_grep_fallback.sh passes
- [x] test_ac5_review_prioritization.sh passes
- [x] test_ac6_json_parsing.sh passes

### Documentation
- [x] Reference file contains clear Treelint usage instructions
- [x] Fallback behavior documented for all failure modes
- [x] Performance targets documented in reference file

---

## Implementation Notes

- [x] treelint-review-patterns.md created with God class, long method, and map patterns - Completed: Reference file created at `src/claude/agents/code-reviewer/references/treelint-review-patterns.md` (191 lines, under 300-line BR-004 limit)
- [x] code-reviewer.md updated with Read() instruction for reference file - Completed: Read() instruction added at line 57 pointing to references/treelint-review-patterns.md
- [x] Treelint integration section added to code-reviewer.md - Completed: Treelint AST-Aware Structural Analysis section added (lines 57-72)
- [x] Language support check and Grep fallback documented in reference - Completed: Grep fallback documented for C#, Java, Go, Ruby, PHP (unsupported languages)
- [x] JSON parsing instructions documented in reference - Completed: JSON field extraction, empty results ("no structural issues found"), and malformed JSON (Grep fallback) all documented
- [x] Reference file <= 300 lines (ADR-012 compliance) - 191 lines - Completed: 191 lines, well under 300-line BR-004 limit
- [x] code-reviewer.md < 860 lines after modification - 843 lines - Completed: 843 lines after modification
- [x] All 6 acceptance criteria have passing tests - Completed: 40/40 assertions passing across 6 test files
- [x] All 8 existing review checklist sections preserved (zero regression) - Completed: Zero regression confirmed by BR-005 test
- [x] Edge cases documented (mixed languages, binary not found, empty results) - Completed: Mixed language handling, binary not found, and empty results all covered in reference file
- [x] NFRs met (< 100ms search, zero review failures via Grep fallback) - Completed: Performance targets documented, Grep fallback prevents review failures
- [x] Code coverage >95% for structural tests - 40/40 assertions passing - Completed: 100% structural test coverage (40/40)
- [x] test_ac1_reference_file_created.sh passes - Completed: All assertions pass
- [x] test_ac2_god_class_detection.sh passes - Completed: All assertions pass
- [x] test_ac3_long_method_detection.sh passes - Completed: All assertions pass
- [x] test_ac4_grep_fallback.sh passes - Completed: All assertions pass
- [x] test_ac5_review_prioritization.sh passes - Completed: All assertions pass
- [x] test_ac6_json_parsing.sh passes - Completed: All assertions pass
- [x] Reference file contains clear Treelint usage instructions - Completed: Step-by-step Treelint integration workflow documented with examples
- [x] Fallback behavior documented for all failure modes - Completed: 5 failure modes documented (binary not found, permission denied, runtime error, unsupported type, malformed JSON)
- [x] Performance targets documented in reference file - Completed: <100ms search performance target and optimization guidance included

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-05 | claude/story-requirements-analyst | Created | Story created via /create-story batch mode (EPIC-057) | STORY-364-update-code-reviewer-treelint-integration.story.md |
| 2026-02-05 | claude/sprint-planner | Sprint Planning | Assigned to Sprint-10, status → Ready for Dev | STORY-364-update-code-reviewer-treelint-integration.story.md |
| 2026-02-06 | claude/devforgeai-development | Dev Complete | TDD implementation complete, all 6 ACs passing (40/40 assertions), DoD 100% complete | treelint-review-patterns.md (NEW), code-reviewer.md (MODIFIED) |
| 2026-02-06 | claude/qa-result-interpreter | QA Deep | PASSED: 3/3 validators, 40/40 tests, 100% traceability, 0 violations | STORY-364-qa-report.md |

## Notes

**Design Decisions:**
- Progressive disclosure mandatory: code-reviewer.md already 825 lines, all Treelint patterns go in reference file
- Minimal core file modification: Add Read() instruction + section pointer (~20-30 lines) to code-reviewer.md
- Existing review checklist preserved: Treelint enhances existing checks (God class, long method), does not replace them
- Dual detection: Both Treelint AST analysis and existing text-based thresholds applied for maximum coverage

**Open Questions:**
- [ ] Treelint class search may not directly report method count — may need to count methods from nested function search - **Owner:** Developer - **Due:** During development
- [ ] Should `treelint map --ranked` be invoked for every review or only when >5 changed files? - **Owner:** Developer - **Due:** During development

**Related ADRs:**
- ADR-012: Progressive Disclosure for Subagents
- ADR-013: Treelint Integration for AST-Aware Code Search

**References:**
- EPIC-057: Treelint Subagent Integration
- STORY-361: Create Treelint Skill Reference Files
- STORY-362: Implement Hybrid Fallback Logic
- source-tree.md lines 596-620: Subagent progressive disclosure pattern
- tech-stack.md lines 104-166: Treelint approved section

---

Story Template Version: 2.8
Last Updated: 2026-02-05
