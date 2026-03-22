---
id: STORY-368
title: Update coverage-analyzer with Treelint AST-Aware Function-Level Coverage Mapping
type: feature
epic: EPIC-057
sprint: Sprint-11
status: QA Approved
points: 5
depends_on: ["STORY-361", "STORY-362"]
priority: Medium
advisory: false
source_gap: null
source_story: null
assigned_to: Unassigned
created: 2026-02-05
format_version: "2.8"
---

# Story: Update coverage-analyzer with Treelint AST-Aware Function-Level Coverage Mapping

## Description

**As a** coverage-analyzer subagent (the DevForgeAI QA specialist responsible for validating test coverage thresholds by architectural layer),
**I want** to use Treelint's AST-aware search (`treelint search --type function --format json`) for function-level coverage mapping, correlating coverage report uncovered line ranges with Treelint function boundaries, parsing JSON search results, and automatically falling back to Grep for unsupported languages,
**so that** I can identify specific uncovered functions (not just uncovered lines) in gap reports, provide developers with function-level remediation guidance ("add tests for `calculateCoverage` at src/coverage.py:10-45") instead of raw line numbers, and achieve 40-80% reduction in tokens consumed during code search operations while maintaining seamless functionality across all project languages through hybrid fallback logic.

## Provenance

```xml
<provenance>
  <origin document="EPIC-057" section="Feature 7: coverage-analyzer Subagent Update">
    <quote>"Enable function-level coverage mapping"</quote>
    <line_reference>lines 69-72</line_reference>
    <quantified_impact>40-80% token reduction in code search operations for coverage gap identification</quantified_impact>
  </origin>

  <decision rationale="direct-cli-integration-over-wrapper">
    <selected>Each subagent uses Treelint directly via Bash tool with reference file patterns</selected>
    <rejected alternative="wrapper-subagent">
      Architecture constraint: subagents cannot delegate to other subagents
    </rejected>
    <trade_off>Treelint patterns duplicated across 7 subagents vs. shared reference file approach mitigates duplication</trade_off>
  </decision>
</provenance>
```

## Acceptance Criteria

### AC#1: Treelint Integration for Function Enumeration

```xml
<acceptance_criteria id="AC1" implements="TREELINT-FUNC-001">
  <given>The coverage-analyzer subagent (src/claude/agents/coverage-analyzer.md) is invoked during Phase 6 (Identify Gaps) and needs to enumerate functions in files identified as under-covered, where those files contain Python (.py), TypeScript (.ts/.tsx), JavaScript (.js/.jsx), Rust (.rs), or Markdown (.md) code</given>
  <when>The subagent performs function-level gap identification to correlate uncovered lines with specific functions</when>
  <then>The subagent uses Treelint via Bash(command="treelint search --type function --format json") to enumerate all functions in the under-covered file, parses the JSON response to extract function name, file path, line range [start, end], and signature, and uses the structured results to map uncovered lines to specific function boundaries</then>
  <verification>
    <source_files>
      <file hint="Updated coverage-analyzer subagent definition">src/claude/agents/coverage-analyzer.md</file>
    </source_files>
    <test_file>tests/STORY-368/test_ac1_treelint_function_enumeration.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: JSON Parsing of Treelint Search Results

```xml
<acceptance_criteria id="AC2" implements="TREELINT-JSON-001">
  <given>Treelint returns a JSON response containing a results array where each entry has fields: type, name, file, lines (array of [start, end]), signature, and body</given>
  <when>The coverage-analyzer subagent receives Treelint search output during function enumeration in Phase 6</when>
  <then>The subagent parses the JSON to extract: (1) function names for gap reports ("uncovered function: calculateCoverage"), (2) file paths for locating source code, (3) line ranges [start, end] for correlating with coverage report uncovered_lines, and (4) function signatures for human-readable gap descriptions, and the parsed data is used to enhance the gaps array with function-level detail</then>
  <verification>
    <source_files>
      <file hint="Updated coverage-analyzer subagent definition">src/claude/agents/coverage-analyzer.md</file>
    </source_files>
    <test_file>tests/STORY-368/test_ac2_json_parsing.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Grep Fallback for Unsupported Languages

```xml
<acceptance_criteria id="AC3" implements="TREELINT-FALLBACK-001">
  <given>The coverage-analyzer subagent needs to enumerate functions in file types not supported by Treelint (e.g., C# .cs, Java .java, Go .go, Ruby .rb) or when the Treelint binary is unavailable (exit code 127) or fails at runtime</given>
  <when>The subagent detects an unsupported file extension or receives a non-zero exit code from Treelint</when>
  <then>The subagent falls back to using the native Grep tool (e.g., Grep(pattern="def |function |async function ", glob="**/*.cs")) following the fallback decision tree documented in the STORY-361 reference file, emits a warning-level message ("Treelint unavailable for .cs files, falling back to Grep"), and completes the function enumeration without halting the workflow</then>
  <verification>
    <source_files>
      <file hint="Updated coverage-analyzer subagent definition">src/claude/agents/coverage-analyzer.md</file>
    </source_files>
    <test_file>tests/STORY-368/test_ac3_grep_fallback.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Coverage Data Correlation with Function Symbols

```xml
<acceptance_criteria id="AC4" implements="TREELINT-COV-001">
  <given>The coverage-analyzer subagent has both (a) a list of uncovered lines from the coverage report (e.g., uncovered_lines: [145, 146, 147, 189, 190]) and (b) Treelint function enumeration results with line ranges (e.g., {name: "processOrder", lines: [140, 200]})</given>
  <when>The subagent performs gap identification in Phase 6 for a file with uncovered lines</when>
  <then>The subagent correlates uncovered lines with function boundaries by checking if each uncovered line falls within a function's [start, end] range, aggregates uncovered lines per function (e.g., "processOrder: 3 of 60 lines uncovered, 95% covered"), and enhances the gaps array to include function-level detail: function_name, function_lines [start, end], uncovered_lines_in_function, function_coverage_percentage, and function_signature</then>
  <verification>
    <source_files>
      <file hint="Updated coverage-analyzer subagent definition">src/claude/agents/coverage-analyzer.md</file>
    </source_files>
    <test_file>tests/STORY-368/test_ac4_coverage_correlation.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Performance Validation for Treelint Searches

```xml
<acceptance_criteria id="AC5" implements="TREELINT-PERF-001">
  <given>The coverage-analyzer subagent performs function enumeration via Treelint on a typical project (up to 10,000 files)</given>
  <when>A treelint search --type function --format json command completes</when>
  <then>The search completes in less than 100 milliseconds for CLI mode (verified via the stats.elapsed_ms field in Treelint JSON output), and the total function enumeration adds no more than 200ms overhead compared to the previous line-only gap identification approach</then>
  <verification>
    <source_files>
      <file hint="Updated coverage-analyzer subagent definition">src/claude/agents/coverage-analyzer.md</file>
    </source_files>
    <test_file>tests/STORY-368/test_ac5_performance.sh</test_file>
    <coverage_threshold>80</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Progressive Disclosure Compliance (500-Line Limit)

```xml
<acceptance_criteria id="AC6" implements="TREELINT-SIZE-001">
  <given>The coverage-analyzer subagent definition file (src/claude/agents/coverage-analyzer.md) has a 500-line maximum per source-tree.md and tech-stack.md token budget constraints, and currently stands at 393 lines</given>
  <when>Treelint integration instructions are added to the coverage-analyzer subagent</when>
  <then>The updated coverage-analyzer.md file remains under 500 lines total, with Treelint-specific patterns either: (a) inlined if the file stays under 500 lines, or (b) extracted to a reference file at src/claude/agents/coverage-analyzer/references/treelint-patterns.md following ADR-012 progressive disclosure pattern, loaded on-demand via Read() instruction in the core file</then>
  <verification>
    <source_files>
      <file hint="Updated coverage-analyzer subagent definition">src/claude/agents/coverage-analyzer.md</file>
      <file hint="Optional Treelint reference file if extracted">src/claude/agents/coverage-analyzer/references/treelint-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-368/test_ac6_line_count.sh</test_file>
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
      name: "coverage-analyzer Subagent Definition"
      file_path: "src/claude/agents/coverage-analyzer.md"
      required_keys:
        - key: "Treelint Function Enumeration Section"
          type: "markdown"
          example: "### Treelint-Aware Function Enumeration"
          required: true
          validation: "Section must contain treelint search --type function --format json instruction"
          test_requirement: "Test: Grep for 'treelint search.*--type function.*--format json' in coverage-analyzer.md"

        - key: "JSON Parsing Instructions"
          type: "markdown"
          example: "Parse JSON results: type, name, file, lines, signature"
          required: true
          validation: "Must reference all 4 required JSON fields: name, file, lines, signature"
          test_requirement: "Test: Grep for 'name.*file.*lines.*signature' pattern in coverage-analyzer.md"

        - key: "Language Support Check"
          type: "markdown"
          example: "Check file extension: .py, .ts, .tsx, .js, .jsx, .rs, .md"
          required: true
          validation: "Must list all 7 supported extensions from tech-stack.md"
          test_requirement: "Test: Grep for '.py' AND '.ts' AND '.tsx' AND '.js' AND '.jsx' AND '.rs' AND '.md' in coverage-analyzer.md"

        - key: "Grep Fallback Section"
          type: "markdown"
          example: "### Fallback: Grep for Unsupported Languages"
          required: true
          validation: "Must reference native Grep tool (not Bash grep)"
          test_requirement: "Test: Grep for 'Grep(pattern=' fallback instruction in coverage-analyzer.md"

        - key: "Coverage-to-Function Correlation"
          type: "markdown"
          example: "### Coverage Data Correlation with Function Boundaries"
          required: true
          validation: "Must describe mapping uncovered_lines to function [start, end] ranges"
          test_requirement: "Test: Grep for 'uncovered.*function.*lines' or 'correlat' pattern in coverage-analyzer.md"

        - key: "Reference File Loading"
          type: "markdown"
          example: "Read(file_path=\"src/claude/agents/references/treelint-search-patterns.md\")"
          required: true
          validation: "Must contain Read() instruction for STORY-361 reference file"
          test_requirement: "Test: Grep for 'Read.*treelint.*patterns' in coverage-analyzer.md"

    - type: "Configuration"
      name: "Treelint Patterns Reference File (Conditional)"
      file_path: "src/claude/agents/coverage-analyzer/references/treelint-patterns.md"
      required_keys:
        - key: "Progressive Disclosure Extraction"
          type: "markdown"
          example: "Treelint search patterns extracted per ADR-012"
          required: false
          default: "Only created if coverage-analyzer.md exceeds 500 lines"
          validation: "If file exists, coverage-analyzer.md must contain Read() pointing to it"
          test_requirement: "Test: If treelint-patterns.md exists, verify coverage-analyzer.md references it via Read()"

  business_rules:
    - id: "BR-001"
      rule: "Treelint must be attempted first for all supported file extensions before falling back to Grep"
      trigger: "When function enumeration is initiated for any file type"
      validation: "Check file extension against supported list, use Treelint if supported, Grep if not"
      error_handling: "If Treelint fails (non-zero exit), fall back to Grep with warning"
      test_requirement: "Test: coverage-analyzer.md Treelint section appears before Grep fallback section"
      priority: "Critical"

    - id: "BR-002"
      rule: "Empty Treelint results (exit code 0, zero matches) must NOT trigger Grep fallback"
      trigger: "When Treelint returns valid JSON with empty results array"
      validation: "Distinguish between exit code 0 (success, no matches) and non-zero (failure)"
      error_handling: "Return empty function list, do not invoke Grep"
      test_requirement: "Test: coverage-analyzer.md contains distinction between empty results and command failure"
      priority: "Critical"

    - id: "BR-003"
      rule: "All Treelint failures must result in successful Grep fallback with zero workflow interruption"
      trigger: "When Treelint returns non-zero exit code or malformed output"
      validation: "Workflow must never HALT due to Treelint issues"
      error_handling: "Warning-level message, Grep fallback, continue workflow"
      test_requirement: "Test: coverage-analyzer.md fallback section contains 'warning' and no 'HALT' or 'error' on Treelint failure"
      priority: "Critical"

    - id: "BR-004"
      rule: "Subagent file must remain under 500 lines; if exceeded, extract to references/"
      trigger: "After Treelint integration content is added"
      validation: "wc -l on coverage-analyzer.md <= 500"
      error_handling: "Extract Treelint patterns to references/treelint-patterns.md per ADR-012"
      test_requirement: "Test: wc -l coverage-analyzer.md <= 500; if >500, references/treelint-patterns.md exists"
      priority: "High"

    - id: "BR-005"
      rule: "Uncovered lines outside any function boundary must be reported separately as module-level code"
      trigger: "When correlating uncovered lines with function boundaries in Phase 6"
      validation: "Lines not within any function [start, end] range categorized as 'module-level'"
      error_handling: "Include module-level uncovered code in gaps array with function_name: null"
      test_requirement: "Test: coverage-analyzer.md mentions handling of uncovered lines outside function boundaries"
      priority: "High"

    - id: "BR-006"
      rule: "Nested function boundaries must attribute uncovered lines to the innermost function"
      trigger: "When multiple function ranges overlap for a given uncovered line"
      validation: "Use smallest enclosing function range for attribution"
      error_handling: "Log if overlap detected, attribute to most specific function"
      test_requirement: "Test: coverage-analyzer.md addresses nested function handling"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Treelint search latency under 100ms"
      metric: "< 100ms per search (p95) as reported by stats.elapsed_ms in JSON response"
      test_requirement: "Test: Verify performance target documented in subagent instructions"
      priority: "High"

    - id: "NFR-002"
      category: "Reliability"
      requirement: "Zero workflow interruptions from Treelint failures"
      metric: "100% of Treelint failures result in successful Grep fallback"
      test_requirement: "Test: Verify fallback covers all 5 failure modes (binary not found, permission denied, runtime error, unsupported type, malformed JSON)"
      priority: "Critical"

    - id: "NFR-003"
      category: "Security"
      requirement: "Shell injection prevention in Treelint commands"
      metric: "All search patterns use alphanumeric + wildcard only; no shell metacharacters"
      test_requirement: "Test: Verify command examples use simple patterns without $, backtick, |, ;, & characters"
      priority: "High"

    - id: "NFR-004"
      category: "Scalability"
      requirement: "Progressive disclosure for token budget compliance"
      metric: "Core subagent file <= 500 lines per ADR-012"
      test_requirement: "Test: wc -l on final file <= 500"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Treelint"
    limitation: "Only supports 5 languages (Python, TypeScript, JavaScript, Rust, Markdown) - C#, Java, Go, Ruby not supported"
    decision: "workaround:Grep fallback for unsupported languages"
    discovered_phase: "Architecture"
    impact: "Projects using unsupported languages get line-level coverage gaps only (no function-level mapping for those languages)"

  - id: TL-002
    component: "coverage-analyzer subagent"
    limitation: "Subagent is markdown documentation, not executable code - Treelint patterns are instructions, not programmatic implementations"
    decision: "workaround:Documentation-based patterns validated via structural tests (Grep for required sections)"
    discovered_phase: "Architecture"
    impact: "Tests are structural (verify sections exist in markdown) rather than functional (verify runtime behavior)"

  - id: TL-003
    component: "coverage-analyzer subagent"
    limitation: "Current file is 393 lines with only 107 lines remaining before 500-line limit"
    decision: "workaround:Monitor line count during development; extract to references/ if exceeded per ADR-012"
    discovered_phase: "Architecture"
    impact: "May require progressive disclosure extraction if Treelint integration exceeds ~100 lines"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Treelint Search:**
- Treelint search latency: < 100ms per invocation (p95) via stats.elapsed_ms
- Total function enumeration overhead: < 200ms additional vs. previous line-only gap identification
- Grep fallback latency: < 2 seconds (p95) for codebases up to 10,000 files
- No increase in overall coverage-analyzer execution time targets: small projects < 10s, medium < 30s, large < 60s (existing targets preserved)

### Security

**Shell Injection Prevention:**
- All Treelint command arguments use simple patterns (alphanumeric + `*` wildcard only)
- Native Grep tool used for fallback (not `Bash(command="grep ...")`) per tech-stack.md constraint
- File paths from Treelint results validated before Read() to prevent path traversal
- No privilege escalation: coverage-analyzer remains read-only (no Write/Edit tools)

### Reliability

**Fallback Guarantees:**
- 100% of Treelint failures result in successful Grep fallback
- One-shot fallback: Treelint fails once → Grep once; no retry loops
- Empty results (exit code 0) treated as valid, NOT as failure
- All 5 failure modes handled: binary not found, permission denied, runtime error, unsupported type, malformed JSON
- Graceful degradation: if Treelint unavailable for all files, coverage-analyzer produces line-level gaps only (pre-Treelint behavior preserved)

### Scalability

**Token Budget:**
- Core subagent file ≤ 500 lines per ADR-012
- Stateless search operations; no shared state between invocations
- Language support extensible by updating extension list only
- Token usage increase: < 500 additional tokens for Treelint-related instructions vs. current 7K baseline

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-361:** Create Treelint Skill Reference Files for Subagent Integration
  - **Why:** Provides the shared Treelint usage patterns referenced by coverage-analyzer
  - **Status:** Backlog

- [x] **STORY-362:** Implement Hybrid Fallback Logic (Treelint to Grep)
  - **Why:** Provides the fallback decision tree used when Treelint is unavailable
  - **Status:** Backlog

### External Dependencies

- [x] **EPIC-055 (Treelint Foundation):** ADR-013 approved, tech-stack.md updated, Treelint binary distributed
  - **Owner:** Framework Architect
  - **Status:** Planning

- [x] **EPIC-056 (Context Files):** source-tree.md and anti-patterns.md updated for Treelint
  - **Owner:** Framework Architect
  - **Status:** Planning

### Technology Dependencies

- [x] **Treelint:** v0.12.0+ binary
  - **Purpose:** AST-aware code search CLI
  - **Approved:** Yes (ADR-013)
  - **Added to dependencies.md:** Yes (v1.1)

---

## Edge Cases

1. **Mixed-language projects with partial Treelint coverage:** Coverage-analyzer may need to enumerate functions across Python (.py - Treelint) and C# (.cs - Grep) in the same project. Per-file-extension decisions are required, aggregating function-level results from Treelint with line-level results from Grep without confusing the two granularity levels in the final gap report.

2. **Empty Treelint results vs. command failure:** Treelint returning exit code 0 with an empty results array (no functions in file) is NOT a failure and must NOT trigger Grep fallback. Must distinguish from non-zero exit codes (binary not found, runtime error) that do trigger fallback. An empty results array means the file has no function declarations (e.g., a constants file), which is valid information.

3. **Uncovered lines outside any function boundary:** Coverage reports may show uncovered lines in module-level code, class-level initializers, or global statements that do not fall within any function's [start, end] range. These lines must be reported separately as "module-level uncovered code" without being silently dropped from the gaps array.

4. **Large function bodies exceeding context window:** Treelint's `body` field may contain very large functions (>500 lines). Coverage-analyzer should use the `lines` field [start, end] for targeted `Read()` of relevant uncovered sections instead of consuming the full body from JSON, preventing context window exhaustion.

5. **File at 393 lines approaching 500-line limit:** Current coverage-analyzer.md is 393 lines. Adding Treelint patterns (estimated 50-100 lines) may approach or exceed the 500-line limit. Must monitor line count during development and extract to `src/claude/agents/coverage-analyzer/references/treelint-patterns.md` per ADR-012 if exceeded.

6. **Treelint binary version mismatch:** Pre-v0.12.0 Treelint versions lacking `--format json` support may fail with an unrecognized flag error. Any non-zero exit code must be treated as failure and trigger Grep fallback, with a warning noting the version requirement (v0.12.0+).

7. **Overlapping function boundaries (nested functions):** In Python and JavaScript, functions can be nested (inner functions defined inside outer functions). An uncovered line may fall within both the outer and inner function's line range. The coverage correlation must attribute the line to the most specific (innermost) function to avoid double-counting.

8. **Concurrent invocations during parallel QA:** Multiple parallel coverage-analyzer invocations are safe because Treelint is stateless and read-only. No shared state between invocations per architecture constraint.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic (structural validation of markdown)

**Test Scenarios:**
1. **Happy Path:** coverage-analyzer.md contains Treelint function enumeration instruction in Phase 6
2. **Edge Cases:**
   - Verify all 7 supported file extensions listed
   - Verify JSON parsing instruction references all required fields
   - Verify progressive disclosure compliance (≤500 lines)
   - Verify coverage-to-function correlation logic documented
3. **Error Cases:**
   - Verify Grep fallback section exists
   - Verify fallback uses warning level (not error/HALT)
   - Verify empty results handling documented
   - Verify module-level code handling documented

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **Reference File Loading:** Verify coverage-analyzer.md contains Read() for treelint-search-patterns.md
2. **End-to-End Pattern:** Verify Treelint → JSON parse → function list → coverage correlation → enhanced gaps documented

---

## Acceptance Criteria Verification Checklist

### AC#1: Treelint Integration for Function Enumeration

- [x] coverage-analyzer.md contains `treelint search --type function` instruction in Phase 6 - **Phase:** 2 - **Evidence:** test_ac1_treelint_function_enumeration.sh
- [x] Instruction uses `--format json` flag - **Phase:** 2 - **Evidence:** test_ac1_treelint_function_enumeration.sh
- [x] Uses Bash() tool for Treelint invocation - **Phase:** 2 - **Evidence:** test_ac1_treelint_function_enumeration.sh

### AC#2: JSON Parsing of Treelint Search Results

- [x] JSON parsing instructions reference `name` field - **Phase:** 2 - **Evidence:** test_ac2_json_parsing.sh
- [x] JSON parsing instructions reference `file` field - **Phase:** 2 - **Evidence:** test_ac2_json_parsing.sh
- [x] JSON parsing instructions reference `lines` field - **Phase:** 2 - **Evidence:** test_ac2_json_parsing.sh
- [x] JSON parsing instructions reference `signature` field - **Phase:** 2 - **Evidence:** test_ac2_json_parsing.sh

### AC#3: Grep Fallback for Unsupported Languages

- [x] Fallback section exists in coverage-analyzer.md - **Phase:** 2 - **Evidence:** test_ac3_grep_fallback.sh
- [x] Fallback uses native Grep tool (not Bash grep) - **Phase:** 2 - **Evidence:** test_ac3_grep_fallback.sh
- [x] Warning-level messaging on fallback - **Phase:** 2 - **Evidence:** test_ac3_grep_fallback.sh

### AC#4: Coverage Data Correlation with Function Symbols

- [x] Coverage-to-function correlation instructions present - **Phase:** 3 - **Evidence:** test_ac4_coverage_correlation.sh
- [x] Uses Treelint line ranges for boundary mapping - **Phase:** 3 - **Evidence:** test_ac4_coverage_correlation.sh
- [x] Module-level uncovered code handled separately - **Phase:** 3 - **Evidence:** test_ac4_coverage_correlation.sh

### AC#5: Performance Validation

- [x] Performance target (<100ms) documented - **Phase:** 3 - **Evidence:** test_ac5_performance.sh
- [x] stats.elapsed_ms field referenced - **Phase:** 3 - **Evidence:** test_ac5_performance.sh

### AC#6: Progressive Disclosure Compliance

- [x] coverage-analyzer.md file line count ≤ 500 - **Phase:** 4 - **Evidence:** test_ac6_line_count.sh
- [x] If >500 lines, reference file exists at references/treelint-patterns.md - **Phase:** 4 - **Evidence:** test_ac6_line_count.sh

---

**Checklist Progress:** 17/17 items complete (100%)

---

## Definition of Done

### Implementation
- [x] coverage-analyzer.md updated with Treelint function enumeration section in Phase 6 - Completed: Treelint-Aware Function Enumeration section added at line 252 with treelint search --type function --format json instruction
- [x] JSON parsing instructions added for Treelint response fields (name, file, lines, signature) - Completed: Step 6.6 Parse JSON Response Fields at line 269 references all 4 fields
- [x] Language support check (7 extensions) documented in subagent - Completed: Supported extensions (.py, .ts, .tsx, .js, .jsx, .rs, .md) listed in Step 6.5
- [x] Grep fallback section with warning-level messaging added - Completed: Fallback section at line 275 with Grep(pattern=) and warning-level messaging
- [x] Coverage-to-function correlation logic documented (mapping uncovered_lines to function boundaries) - Completed: Coverage Data Correlation section at line 287 with Steps 6.7-6.9
- [x] Module-level uncovered code handling documented - Completed: Module-level code handling at line 291 with function_name: null attribution
- [x] STORY-361 reference file loading instruction (Read()) added - Completed: Read() instructions at lines 258-259 for both shared and coverage-analyzer-specific reference files
- [x] File size ≤ 500 lines verified (extract to references/ if needed) - Completed: File is 441 lines (under 500 limit), reference file extracted to src/claude/agents/coverage-analyzer/references/treelint-patterns.md (234 lines)

### Quality
- [x] All 6 acceptance criteria have passing tests - Completed: 35/35 tests passing across 6 test files, ac-compliance-verifier confirmed 6/6 PASS
- [x] Edge cases documented (mixed languages, empty results, nested functions, module-level code) - Completed: Edge cases section covers all 8 scenarios including mixed-language projects and nested function boundaries
- [x] NFRs met (performance <100ms, zero workflow interruptions) - Completed: Performance target documented at line 271, fallback ensures zero workflow interruptions
- [x] Code coverage >95% for structural tests - Completed: 35 structural tests covering all 6 ACs with comprehensive edge case validation

### Testing
- [x] test_ac1_treelint_function_enumeration.sh passes - Completed: 6/6 tests pass
- [x] test_ac2_json_parsing.sh passes - Completed: 7/7 tests pass
- [x] test_ac3_grep_fallback.sh passes - Completed: 7/7 tests pass
- [x] test_ac4_coverage_correlation.sh passes - Completed: 7/7 tests pass
- [x] test_ac5_performance.sh passes - Completed: 4/4 tests pass
- [x] test_ac6_line_count.sh passes - Completed: 4/4 tests pass

### Documentation
- [x] coverage-analyzer.md contains clear Treelint usage instructions for Phase 6 - Completed: Treelint-Aware Function Enumeration section with step-by-step workflow (Steps 6.4-6.9)
- [x] Fallback behavior documented for all 5 failure modes - Completed: Fallback section covers binary not found, permission denied, runtime error, unsupported type, malformed JSON
- [x] Coverage-to-function correlation algorithm documented - Completed: Reference file treelint-patterns.md lines 117-160 provides full correlation algorithm with pseudocode
- [x] Reference file loading documented (STORY-361 dependency) - Completed: Read() for treelint-search-patterns.md (shared) and treelint-patterns.md (coverage-analyzer-specific)

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent (claude/opus)
**Implemented:** 2026-02-07
**Branch:** main

- [x] coverage-analyzer.md updated with Treelint function enumeration section in Phase 6 - Completed: Treelint-Aware Function Enumeration section added at line 252 with treelint search --type function --format json instruction
- [x] JSON parsing instructions added for Treelint response fields (name, file, lines, signature) - Completed: Step 6.6 Parse JSON Response Fields at line 269 references all 4 fields
- [x] Language support check (7 extensions) documented in subagent - Completed: Supported extensions (.py, .ts, .tsx, .js, .jsx, .rs, .md) listed in Step 6.5
- [x] Grep fallback section with warning-level messaging added - Completed: Fallback section at line 275 with Grep(pattern=) and warning-level messaging
- [x] Coverage-to-function correlation logic documented (mapping uncovered_lines to function boundaries) - Completed: Coverage Data Correlation section at line 287 with Steps 6.7-6.9
- [x] Module-level uncovered code handling documented - Completed: Module-level code handling at line 291 with function_name: null attribution
- [x] STORY-361 reference file loading instruction (Read()) added - Completed: Read() instructions at lines 258-259 for both shared and coverage-analyzer-specific reference files
- [x] File size ≤ 500 lines verified (extract to references/ if needed) - Completed: File is 441 lines (under 500 limit), reference file extracted to src/claude/agents/coverage-analyzer/references/treelint-patterns.md (234 lines)
- [x] All 6 acceptance criteria have passing tests - Completed: 35/35 tests passing across 6 test files, ac-compliance-verifier confirmed 6/6 PASS
- [x] Edge cases documented (mixed languages, empty results, nested functions, module-level code) - Completed: Edge cases section covers all 8 scenarios including mixed-language projects and nested function boundaries
- [x] NFRs met (performance <100ms, zero workflow interruptions) - Completed: Performance target documented at line 271, fallback ensures zero workflow interruptions
- [x] Code coverage >95% for structural tests - Completed: 35 structural tests covering all 6 ACs with comprehensive edge case validation
- [x] test_ac1_treelint_function_enumeration.sh passes - Completed: 6/6 tests pass
- [x] test_ac2_json_parsing.sh passes - Completed: 7/7 tests pass
- [x] test_ac3_grep_fallback.sh passes - Completed: 7/7 tests pass
- [x] test_ac4_coverage_correlation.sh passes - Completed: 7/7 tests pass
- [x] test_ac5_performance.sh passes - Completed: 4/4 tests pass
- [x] test_ac6_line_count.sh passes - Completed: 4/4 tests pass
- [x] coverage-analyzer.md contains clear Treelint usage instructions for Phase 6 - Completed: Treelint-Aware Function Enumeration section with step-by-step workflow (Steps 6.4-6.9)
- [x] Fallback behavior documented for all 5 failure modes - Completed: Fallback section covers binary not found, permission denied, runtime error, unsupported type, malformed JSON
- [x] Coverage-to-function correlation algorithm documented - Completed: Reference file treelint-patterns.md lines 117-160 provides full correlation algorithm with pseudocode
- [x] Reference file loading documented (STORY-361 dependency) - Completed: Read() for treelint-search-patterns.md (shared) and treelint-patterns.md (coverage-analyzer-specific)

### TDD Workflow Summary

**Phase 02 (Red): Test-First Design**
- Generated 35 comprehensive tests covering all 6 acceptance criteria
- Tests placed in tests/STORY-368/ (6 test files + run_all_tests.sh)
- All tests follow structural validation pattern (Grep for markdown sections)

**Phase 03 (Green): Implementation**
- Implemented via backend-architect subagent
- Added Treelint-Aware Function Enumeration section (lines 252-295) to coverage-analyzer.md
- Created reference file at src/claude/agents/coverage-analyzer/references/treelint-patterns.md (234 lines)
- All 35 tests passing (100% pass rate)

**Phase 04 (Refactor): Code Quality**
- Code reviewed by refactoring-specialist and code-reviewer subagents
- No refactoring needed - implementation is clean and concise (48 new lines in core file)
- All tests remain green after review

**Phase 05 (Integration): Full Validation**
- Integration tester validated 7 integration points
- JSON field format mismatch fixed during integration
- All tests confirmed GREEN (35/35)

### Files Created/Modified

**Modified:**
- src/claude/agents/coverage-analyzer.md (393 → 441 lines, +48 lines for Treelint integration)

**Created:**
- src/claude/agents/coverage-analyzer/references/treelint-patterns.md (234 lines - function enumeration, JSON parsing, fallback logic, correlation algorithm)
- tests/STORY-368/test_ac1_treelint_function_enumeration.sh
- tests/STORY-368/test_ac2_json_parsing.sh
- tests/STORY-368/test_ac3_grep_fallback.sh
- tests/STORY-368/test_ac4_coverage_correlation.sh
- tests/STORY-368/test_ac5_performance.sh
- tests/STORY-368/test_ac6_line_count.sh
- tests/STORY-368/run_all_tests.sh

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-05 | claude/story-requirements-analyst | Created | Story created via /create-story (EPIC-057 Feature 7: coverage-analyzer) | STORY-368-update-coverage-analyzer-treelint-integration.story.md |
| 2026-02-05 | claude/sprint-planner | Sprint Planning | Assigned to Sprint-11, status → Ready for Dev | STORY-368-update-coverage-analyzer-treelint-integration.story.md |
| 2026-02-07 | claude/opus | DoD Update (Phase 07) | Development complete, all 22 DoD items marked [x], 35/35 tests passing, 6/6 ACs verified PASS | src/claude/agents/coverage-analyzer.md, src/claude/agents/coverage-analyzer/references/treelint-patterns.md, tests/STORY-368/*.sh |
| 2026-02-07 | claude/qa-result-interpreter | QA Deep | PASSED: Coverage 100%, 35/35 tests, 3/3 validators, 0 blocking violations | devforgeai/qa/reports/STORY-368-qa-report.md |

## Notes

**Design Decisions:**
- Treelint invoked directly via Bash tool per architecture constraint (subagents cannot delegate to wrapper subagent)
- Shared reference file from STORY-361 loaded via Read() to minimize duplication across 7 subagents
- Progressive disclosure (ADR-012) used if coverage-analyzer.md exceeds 500-line limit
- Structural tests (Grep for markdown sections) rather than runtime tests, since subagent is a markdown definition
- Coverage-to-function correlation is the unique differentiator for this story vs. other subagent updates (AC#4)

**Open Questions:**
- [x] Exact line budget for Treelint section (current file is 393 lines, ~107 lines remaining) - **Resolved:** File grew to 441 lines (+48), well within 500-line limit. Reference file handles detailed patterns (234 lines).
- [x] Whether enhanced gaps output format (with function_name, function_coverage_percentage) requires changes to the coverage-analyzer output contract JSON schema - **Resolved:** Enhanced gap output documented as extension fields in the gaps array; backward-compatible with existing gap schema.

**Related ADRs:**
- ADR-012: Progressive Disclosure for Subagents
- ADR-013: Treelint Integration for AST-Aware Code Search

**References:**
- EPIC-057: Treelint Subagent Integration
- STORY-361: Create Treelint Skill Reference Files
- STORY-362: Implement Hybrid Fallback Logic
- STORY-363: Update test-automator with Treelint (sibling pattern)
- tech-stack.md lines 104-166: Treelint approved section
- source-tree.md lines 232-262: Subagent directory rules

---

Story Template Version: 2.8
Last Updated: 2026-02-05
