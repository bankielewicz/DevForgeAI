---
id: STORY-371
title: Implement Code Quality Metrics Extraction via Treelint AST
type: feature
epic: EPIC-058
sprint: Sprint-12
status: QA Approved
points: 5
depends_on: []
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: Claude
created: 2026-02-05
format_version: "2.8"
---

# Story: Implement Code Quality Metrics Extraction via Treelint AST

## Description

**As a** code-quality-auditor AI subagent,
**I want** to extract function length, nesting depth, and cyclomatic complexity metrics from Treelint AST analysis via `treelint metrics` commands,
**so that** code quality assessments use structural accuracy from AST parsing rather than relying solely on language-specific tools (radon, eslint, rubocop), enabling language-agnostic quality analysis across Python, TypeScript, JavaScript, and Rust codebases.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-009" section="treelint-integration">
    <quote>"Extract function length, nesting depth, and complexity from AST for data-driven code quality assessment beyond line counting"</quote>
    <line_reference>EPIC-058, lines 44-46</line_reference>
    <quantified_impact>Enables AST-based quality metrics that are structurally accurate, replacing heuristic line-counting approaches</quantified_impact>
  </origin>

  <decision rationale="treelint-ast-supplement-not-replace">
    <selected>Treelint AST metrics supplement existing language-specific tools (radon, eslint, rubocop)</selected>
    <rejected alternative="full-replacement">
      Fully replacing language-specific tools would lose language-specific insights (e.g., Python-specific complexity patterns from radon)
    </rejected>
    <trade_off>Two metric sources require reconciliation logic but provide richer analysis</trade_off>
  </decision>

  <stakeholder role="code-quality-auditor" goal="structural-accuracy">
    <quote>"Data-driven code quality assessment beyond line counting"</quote>
    <source>EPIC-058, Feature 2 description</source>
  </stakeholder>
</provenance>
```

---

## Acceptance Criteria

### AC#1: Function length extraction from AST

```xml
<acceptance_criteria id="AC1" implements="SVC-001">
  <given>A source file exists at a valid path and is written in a Treelint-supported language (Python, TypeScript, JavaScript, Rust)</given>
  <when>The code-quality-auditor invokes treelint metrics --function-length --file path --format json</when>
  <then>The command returns a JSON response containing an array of functions, each with name, line_start, line_end, and length (integer, lines of code), and the JSON is parseable without errors</then>
  <verification>
    <source_files>
      <file hint="Code quality auditor agent">src/claude/agents/code-quality-auditor.md</file>
    </source_files>
    <test_file>tests/STORY-371/test_ac1_function_length.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Nesting depth calculation from AST structure

```xml
<acceptance_criteria id="AC2" implements="SVC-001">
  <given>A source file contains functions with nested control structures (if/else, for, while, try/catch, match/switch)</given>
  <when>The code-quality-auditor invokes treelint metrics --nesting-depth --file path --format json</when>
  <then>The command returns a JSON response containing each function's name and nesting_depth (integer, maximum nesting level within that function), where nesting depth 0 means no control structures and increments per nesting level</then>
  <verification>
    <source_files>
      <file hint="Code quality auditor agent">src/claude/agents/code-quality-auditor.md</file>
    </source_files>
    <test_file>tests/STORY-371/test_ac2_nesting_depth.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Metrics compared against configurable thresholds

```xml
<acceptance_criteria id="AC3" implements="SVC-002,BR-001">
  <given>The code-quality-auditor has loaded quality thresholds from quality-metrics.md (method max 100 lines, complexity max 10, maintainability index min 70)</given>
  <when>Treelint metrics results are parsed for a file</when>
  <then>Each function is classified as ACCEPTABLE (below threshold), WARNING (within 50% above threshold), or CRITICAL (exceeding threshold by 100%+), matching the severity levels defined in quality-metrics.md</then>
  <verification>
    <source_files>
      <file hint="Quality metrics config">src/claude/skills/devforgeai-qa/assets/config/quality-metrics.md</file>
      <file hint="Code quality auditor agent">src/claude/agents/code-quality-auditor.md</file>
    </source_files>
    <test_file>tests/STORY-371/test_ac3_threshold_classification.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Integration with code-quality-auditor workflow

```xml
<acceptance_criteria id="AC4" implements="SVC-003,SVC-004">
  <given>The code-quality-auditor subagent is invoked for a story's quality analysis</given>
  <when>Treelint is available (verified via treelint --version returning v0.12.0+)</when>
  <then>The auditor uses Treelint metrics as the primary source for function length and nesting depth, supplementing (not replacing) existing language-specific tools (radon, eslint, rubocop), and the combined results appear in the auditor's output under the metrics key</then>
  <verification>
    <source_files>
      <file hint="Code quality auditor agent">src/claude/agents/code-quality-auditor.md</file>
    </source_files>
    <test_file>tests/STORY-371/test_ac4_auditor_integration.sh</test_file>
    <coverage_threshold>85</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: JSON output format documented and parsed

```xml
<acceptance_criteria id="AC5" implements="SVC-001,SVC-005">
  <given>The Treelint metrics command produces JSON output</given>
  <when>The code-quality-auditor parses the response</when>
  <then>The parser validates the JSON against the expected schema (file: string, functions: array of objects with name, line_start, line_end, length, nesting_depth, complexity), and logs a structured error if the schema does not match</then>
  <verification>
    <source_files>
      <file hint="Code quality auditor agent">src/claude/agents/code-quality-auditor.md</file>
    </source_files>
    <test_file>tests/STORY-371/test_ac5_json_schema_validation.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Error handling for unavailable Treelint or unsupported files

```xml
<acceptance_criteria id="AC6" implements="SVC-003,SVC-006">
  <given>Treelint is not installed, returns a version below v0.12.0, the target file does not exist, or the file language is not supported by Treelint</given>
  <when>The code-quality-auditor attempts to invoke Treelint metrics</when>
  <then>The auditor falls back to the existing language-specific tool chain (radon for Python, eslint for JS/TS, rubocop for Ruby) without halting the workflow, logs a warning message identifying the fallback reason, and the final quality report still contains all required metrics sections</then>
  <verification>
    <source_files>
      <file hint="Code quality auditor agent">src/claude/agents/code-quality-auditor.md</file>
    </source_files>
    <test_file>tests/STORY-371/test_ac6_error_fallback.sh</test_file>
    <coverage_threshold>85</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "TreelintMetricsIntegration"
      file_path: "src/claude/agents/code-quality-auditor.md"
      interface: "Bash CLI invocation + JSON parsing"
      lifecycle: "Per-invocation (stateless)"
      dependencies:
        - "Treelint CLI v0.12.0+"
        - "Bash tool"
        - "quality-metrics.md (thresholds)"
      requirements:
        - id: "SVC-001"
          description: "Invoke treelint metrics commands (--function-length, --nesting-depth, --complexity) and parse JSON response into structured metrics data"
          testable: true
          test_requirement: "Test: Invoke treelint metrics --function-length --file src/main.py --format json and verify JSON contains functions array with length values"
          priority: "Critical"
          implements_ac: ["AC1", "AC2", "AC5"]
        - id: "SVC-002"
          description: "Classify each function as ACCEPTABLE/WARNING/CRITICAL based on configurable thresholds from quality-metrics.md"
          testable: true
          test_requirement: "Test: Function with 120 lines classified as WARNING (threshold 100), function with 250 lines classified as CRITICAL"
          priority: "High"
          implements_ac: ["AC3"]
        - id: "SVC-003"
          description: "Detect Treelint availability via version check and fall back to language-specific tools when unavailable"
          testable: true
          test_requirement: "Test: When Treelint is not installed, auditor completes analysis using radon/eslint with warning in report"
          priority: "Critical"
          implements_ac: ["AC4", "AC6"]
        - id: "SVC-004"
          description: "Detect file language via extension mapping and skip Treelint for unsupported languages"
          testable: true
          test_requirement: "Test: .py/.ts/.js/.rs files use Treelint; .cs/.go/.java files skip Treelint immediately"
          priority: "High"
          implements_ac: ["AC4"]
        - id: "SVC-005"
          description: "Validate JSON response schema with required fields (file, functions array with name/line_start/line_end/length/nesting_depth/complexity)"
          testable: true
          test_requirement: "Test: Malformed JSON (missing functions key) triggers structured error log and fallback"
          priority: "High"
          implements_ac: ["AC5"]
        - id: "SVC-006"
          description: "Handle file-not-found, syntax errors, and parse failures with structured error responses"
          testable: true
          test_requirement: "Test: Non-existent file path returns structured error with file path and error type"
          priority: "High"
          implements_ac: ["AC6"]

  business_rules:
    - id: "BR-001"
      rule: "Treelint metrics supplement but do not replace existing language-specific tools"
      trigger: "When both Treelint and language-specific tools are available"
      validation: "Final report contains metrics from both sources with source attribution"
      error_handling: "If Treelint fails, language-specific tools provide complete metrics"
      test_requirement: "Test: Report contains Treelint metrics AND radon metrics for Python files when both available"
      priority: "Critical"
    - id: "BR-002"
      rule: "Threshold classifications align with quality-metrics.md severity levels"
      trigger: "When classifying functions by metric values"
      validation: "ACCEPTABLE/WARNING/CRITICAL match documented threshold ranges"
      error_handling: "If thresholds missing from config, use framework defaults (complexity_warning=15, complexity_critical=20)"
      test_requirement: "Test: When quality-metrics.md is missing, default thresholds are applied correctly"
      priority: "High"
    - id: "BR-003"
      rule: "Empty function arrays are valid results (not errors)"
      trigger: "When analyzing files with no function definitions"
      validation: "Result type is success with empty functions array"
      error_handling: "Report file as ACCEPTABLE (no violations possible in empty function list)"
      test_requirement: "Test: File with only imports/constants returns success with empty functions array"
      priority: "Medium"
    - id: "BR-004"
      rule: "Nested functions/closures reported as separate entries with own metrics"
      trigger: "When file contains nested function definitions"
      validation: "Parent and child functions both appear in results with independent metrics"
      error_handling: "Parent length includes nested function lines; nesting_depth counts control structures not nested functions"
      test_requirement: "Test: Python file with nested def returns both parent and nested function as separate entries"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Single file metrics extraction completes within 500ms"
      metric: "< 500ms (p95) for files up to 1,000 lines"
      test_requirement: "Test: Measure execution time of metrics command for 1000-line file; assert < 500ms"
      priority: "High"
    - id: "NFR-002"
      category: "Performance"
      requirement: "Batch analysis of 100 files completes within 30 seconds"
      metric: "< 30 seconds total elapsed time for 100-file batch"
      test_requirement: "Test: Analyze 100 files sequentially; assert total time < 30s"
      priority: "Medium"
    - id: "NFR-003"
      category: "Reliability"
      requirement: "Graceful fallback to language-specific tools on any Treelint failure"
      metric: "100% of analyses complete even when Treelint is unavailable"
      test_requirement: "Test: Remove Treelint from PATH; verify auditor completes full analysis via fallback tools"
      priority: "Critical"
    - id: "NFR-004"
      category: "Security"
      requirement: "File path inputs sanitized against path traversal"
      metric: "Zero path traversal vulnerabilities"
      test_requirement: "Test: Pass file paths with ../ sequences; verify rejection or normalization to project root"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Treelint v0.12.0"
    limitation: "Language support limited to Python, TypeScript, JavaScript, Rust, Markdown"
    decision: "workaround:Use language-specific tools (radon, eslint, rubocop) for unsupported languages"
    discovered_phase: "Architecture"
    impact: "C#, Go, Java files cannot use Treelint metrics; existing tool chain provides coverage"
  - id: TL-002
    component: "Treelint metrics --complexity"
    limitation: "Cyclomatic complexity calculation may differ from language-specific tools (radon, eslint)"
    decision: "workaround:Report Treelint complexity alongside language-specific complexity with source attribution"
    discovered_phase: "Architecture"
    impact: "Slight metric differences between Treelint and radon/eslint may cause confusion; documentation clarifies"
  - id: TL-003
    component: "Treelint metrics"
    limitation: "Files with syntax errors cannot be AST-parsed"
    decision: "workaround:Skip metrics for files with parse errors; note in report as skipped"
    discovered_phase: "Architecture"
    impact: "Incomplete metrics for files with syntax errors; language-specific tools may also fail on same files"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- **Single file metrics:** < 500ms (p95) for files up to 1,000 lines
- **Large file metrics:** < 2,000ms (p95) for files up to 10,000 lines
- **Batch 100 files:** < 30 seconds total elapsed time

**Throughput:**
- Support up to 10 concurrent file analyses via independent Bash invocations
- Scales linearly with file count

**Performance Test:**
- Measure per-file metrics extraction time
- Verify batch processing within time budget
- Verify no memory issues (< 50 MB per invocation)

---

### Security

**Authentication:**
- None required (local filesystem operations)

**Data Protection:**
- File path sanitization against path traversal (no `../` beyond project root)
- No credentials or secrets in Treelint commands
- Treelint binary version verified before execution

**Security Testing:**
- [ ] No path traversal vulnerabilities
- [ ] No command injection via file paths
- [ ] No write operations to source files
- [ ] Treelint version verification prevents running unknown binaries

---

### Reliability

**Error Handling:**
- Structured error responses for all failure modes
- Graceful fallback to language-specific tools
- Partial results accepted (successful files included, failed files skipped)

**Retry Logic:**
- No retry on Treelint failure (deterministic command)
- Fallback chain provides alternative results

---

### Scalability

**Codebase Size:**
- Compatible with project sizes up to 50,000 source files
- Stateless invocations (no cross-file state)
- Concurrent file analysis supported (up to 10 parallel)

---

## Dependencies

### Prerequisite Stories

- [ ] **EPIC-057 Stories:** Basic Treelint integration must be working
  - **Why:** This story extends Treelint integration with metrics commands
  - **Status:** In Progress

### External Dependencies

- [ ] **Treelint v0.12.0:** Must support `metrics` command with `--function-length`, `--nesting-depth`, `--complexity` flags
  - **Owner:** Treelint project
  - **Status:** Available
  - **Impact if delayed:** Story cannot proceed without metrics command support

### Technology Dependencies

- [ ] **Treelint CLI v0.12.0+**
  - **Purpose:** Provides `metrics` command for AST-based quality analysis
  - **Approved:** Yes (per EPIC-055/056/057/058 initiative)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for core metrics parsing and classification

**Test Scenarios:**
1. **Happy Path:** Successful metrics extraction for Python/TS/JS/Rust files
2. **Edge Cases:**
   - Empty file (no functions)
   - Large file (1000+ functions)
   - Nested functions/closures
   - Unsupported file extension
3. **Error Cases:**
   - File not found
   - Treelint not installed
   - Malformed JSON response
   - File with syntax errors
   - Treelint version below v0.12.0

---

### Integration Tests

**Coverage Target:** 85%+ for auditor workflow integration

**Test Scenarios:**
1. **Auditor integration:** Full quality analysis using Treelint + language-specific tools
2. **Fallback chain:** Analysis completes when Treelint unavailable

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

### AC#1: Function length extraction from AST

- [x] Treelint metrics --function-length command executes - **Phase:** 2 - **Evidence:** test_ac1_function_length.sh
- [x] JSON response contains functions array with length values - **Phase:** 3 - **Evidence:** test_ac1_function_length.sh
- [x] Each function has name, line_start, line_end, length fields - **Phase:** 3 - **Evidence:** test_ac1_function_length.sh

### AC#2: Nesting depth calculation from AST

- [x] Treelint metrics --nesting-depth command executes - **Phase:** 2 - **Evidence:** test_ac2_nesting_depth.sh
- [x] JSON response contains nesting_depth per function - **Phase:** 3 - **Evidence:** test_ac2_nesting_depth.sh
- [x] Nesting depth increments per control structure level - **Phase:** 3 - **Evidence:** test_ac2_nesting_depth.sh

### AC#3: Threshold classification

- [x] Thresholds loaded from quality-metrics.md - **Phase:** 3 - **Evidence:** test_ac3_threshold_classification.sh
- [x] Functions classified as ACCEPTABLE/WARNING/CRITICAL - **Phase:** 3 - **Evidence:** test_ac3_threshold_classification.sh
- [x] Default thresholds used when config missing - **Phase:** 3 - **Evidence:** test_ac3_threshold_classification.sh

### AC#4: Auditor workflow integration

- [x] Treelint version check in auditor Phase 1 - **Phase:** 4 - **Evidence:** test_ac4_auditor_integration.sh
- [x] Treelint metrics used as primary source when available - **Phase:** 4 - **Evidence:** test_ac4_auditor_integration.sh
- [x] Combined results from Treelint + language tools - **Phase:** 4 - **Evidence:** test_ac4_auditor_integration.sh

### AC#5: JSON schema validation

- [x] JSON parsed against expected schema - **Phase:** 3 - **Evidence:** test_ac5_json_schema_validation.sh
- [x] Schema mismatch triggers structured error - **Phase:** 3 - **Evidence:** test_ac5_json_schema_validation.sh

### AC#6: Error handling and fallback

- [x] Treelint unavailable triggers fallback to radon/eslint - **Phase:** 3 - **Evidence:** test_ac6_error_fallback.sh
- [x] Warning logged with fallback reason - **Phase:** 3 - **Evidence:** test_ac6_error_fallback.sh
- [x] Final report complete even without Treelint - **Phase:** 4 - **Evidence:** test_ac6_error_fallback.sh

---

**Checklist Progress:** 17/17 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Treelint metrics invocation added to code-quality-auditor workflow
- [x] Version detection logic (treelint --version >= v0.12.0)
- [x] Language support detection via file extension mapping
- [x] JSON response schema validation
- [x] Threshold classification logic (ACCEPTABLE/WARNING/CRITICAL)
- [x] Fallback logic to radon/eslint/rubocop
- [x] File path sanitization against path traversal
- [x] Nested function handling (separate entries with own metrics)

### Quality
- [x] All 6 acceptance criteria have passing tests
- [x] Edge cases covered (empty files, large files, nested functions, unsupported languages, syntax errors)
- [x] Path traversal prevention validated
- [x] NFRs met (< 500ms single file, < 30s batch 100 files)
- [x] Code coverage > 95% for core logic, > 85% for integrations

### Testing
- [x] Unit tests for metrics extraction and JSON parsing
- [x] Unit tests for threshold classification
- [x] Unit tests for error handling and fallback chain
- [x] Integration tests for auditor workflow
- [x] Performance tests for single file and batch analysis

### Documentation
- [x] Treelint metrics integration documented in code-quality-auditor agent
- [x] JSON response schema documented
- [x] Threshold configuration documented
- [x] Fallback behavior documented

---

## Implementation Notes

### Implementation DoD
- [x] Treelint metrics invocation added to code-quality-auditor workflow - Completed: Phase 03, added `treelint metrics` CLI invocations for --function-length, --nesting-depth, --complexity in code-quality-auditor.md
- [x] Version detection logic (treelint --version >= v0.12.0) - Completed: Phase 03, version check gates all Treelint metrics operations
- [x] Language support detection via file extension mapping - Completed: Phase 03, .py/.ts/.js/.rs mapped to Treelint; unsupported extensions skip to language-specific tools
- [x] JSON response schema validation - Completed: Phase 03, validates required fields (file, functions array with name/line_start/line_end/length/nesting_depth/complexity)
- [x] Threshold classification logic (ACCEPTABLE/WARNING/CRITICAL) - Completed: Phase 03, thresholds loaded from quality-metrics.md with framework defaults as fallback
- [x] Fallback logic to radon/eslint/rubocop - Completed: Phase 03, graceful fallback chain when Treelint unavailable or fails
- [x] File path sanitization against path traversal - Completed: Phase 03, rejects paths with ../ beyond project root
- [x] Nested function handling (separate entries with own metrics) - Completed: Phase 03, parent and nested functions reported as separate entries with independent metrics

### Quality DoD
- [x] All 6 acceptance criteria have passing tests - Completed: Phase 04.5, ac-compliance-verifier confirmed 17/17 checklist items
- [x] Edge cases covered (empty files, large files, nested functions, unsupported languages, syntax errors) - Completed: Phase 02-03, test scenarios in all 6 test files
- [x] Path traversal prevention validated - Completed: Phase 05, integration test confirms rejection of traversal paths
- [x] NFRs met (< 500ms single file, < 30s batch 100 files) - Completed: Phase 05, performance thresholds validated
- [x] Code coverage > 95% for core logic, > 85% for integrations - Completed: Phase 05.5, coverage targets met

### Testing DoD
- [x] Unit tests for metrics extraction and JSON parsing - Completed: Phase 02, test_ac1_function_length.sh, test_ac5_json_schema_validation.sh
- [x] Unit tests for threshold classification - Completed: Phase 02, test_ac3_threshold_classification.sh
- [x] Unit tests for error handling and fallback chain - Completed: Phase 02, test_ac6_error_fallback.sh
- [x] Integration tests for auditor workflow - Completed: Phase 05, test_ac4_auditor_integration.sh
- [x] Performance tests for single file and batch analysis - Completed: Phase 05, validated in integration-tester run

### Documentation DoD
- [x] Treelint metrics integration documented in code-quality-auditor agent - Completed: Phase 03, full workflow documented in src/claude/agents/code-quality-auditor.md
- [x] JSON response schema documented - Completed: Phase 03, schema definition in agent doc
- [x] Threshold configuration documented - Completed: Phase 03, threshold sources and defaults documented
- [x] Fallback behavior documented - Completed: Phase 03, fallback chain and warning logging documented

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-08 | claude/qa-result-interpreter | QA Deep | PASSED: 41/41 tests passed (100%), 2/2 validators passed, 0 violations | STORY-371.story.md |
| 2026-02-06 | claude/sprint-planner | Sprint Assignment | Assigned to Sprint-12: Treelint Advanced Features & Validation Rollout. Status transitioned from Backlog to Ready for Dev. | STORY-371.story.md |
| 2026-02-05 | claude/story-requirements-analyst | Created | Story created from EPIC-058 Feature 2 | STORY-371.story.md |

## Notes

**Design Decisions:**
- Treelint supplements (not replaces) existing language-specific tools for richer analysis
- Threshold classification aligns with quality-metrics.md severity levels
- Language detection via file extension prevents unnecessary Treelint invocations
- Nested functions reported as separate entries with independent metrics

**Open Questions:**
- [ ] Exact Treelint `metrics` command flags to be validated against v0.12.0 release - **Owner:** Framework Architect - **Due:** Before development
- [ ] Nesting depth threshold values to be confirmed (proposed: 4 warning, 8 critical) - **Owner:** Framework Architect - **Due:** Sprint planning

**Related ADRs:**
- None (follows established patterns from EPIC-057)

**References:**
- EPIC-058: Treelint Advanced Features
- BRAINSTORM-009: Treelint Integration Initiative
- quality-metrics.md: Code quality thresholds
- Treelint v0.12.0 documentation

---

Story Template Version: 2.8
Last Updated: 2026-02-05
