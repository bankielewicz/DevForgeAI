---
id: STORY-363
title: Update test-automator Subagent with Treelint AST-Aware Function Discovery
type: feature
epic: EPIC-057
sprint: Sprint-9
status: QA Approved
points: 5
depends_on: ["STORY-361"]
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: Unassigned
created: 2026-02-05
format_version: "2.8"
---

# Story: Update test-automator Subagent with Treelint AST-Aware Function Discovery

## Description

**As a** test-automator subagent (the DevForgeAI TDD specialist responsible for generating test suites from acceptance criteria),
**I want** to use Treelint's AST-aware search (`treelint search --type function --format json`) for semantic function-level test discovery instead of text-based Grep patterns, with JSON parsing of structured results and automatic fallback to Grep for unsupported languages,
**so that** I can find test functions and source functions by their actual AST node type (reducing false positives from comments, strings, and variable names matching patterns), achieve 40-80% token reduction in code search operations, and maintain seamless functionality across all project languages through hybrid fallback logic.

## Provenance

```xml
<provenance>
  <origin document="EPIC-057" section="Feature 2: test-automator Subagent Update">
    <quote>"Enable function-level test discovery using treelint search --type function"</quote>
    <line_reference>lines 44-47</line_reference>
    <quantified_impact>40-80% token reduction in code search operations for test discovery</quantified_impact>
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

### AC#1: Treelint Integration for Function Discovery

```xml
<acceptance_criteria id="AC1" implements="TREELINT-FUNC-001">
  <given>The test-automator subagent (src/claude/agents/test-automator.md) is invoked during TDD Red phase to discover existing test functions or source functions in a project containing Python (.py), TypeScript (.ts/.tsx), or JavaScript (.js/.jsx) files</given>
  <when>The subagent performs function-level code search to find test functions (e.g., test_*, it(), describe()) or source functions to map test targets</when>
  <then>The subagent uses Treelint via Bash(command="treelint search --type function --name 'test_*' --format json") instead of Grep patterns, parses the JSON response to extract function name, file path, line range, and signature, and uses the structured results for test generation decisions</then>
  <verification>
    <source_files>
      <file hint="Updated test-automator subagent definition">src/claude/agents/test-automator.md</file>
    </source_files>
    <test_file>tests/STORY-363/test_ac1_treelint_function_discovery.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: JSON Parsing of Treelint Search Results

```xml
<acceptance_criteria id="AC2" implements="TREELINT-JSON-001">
  <given>Treelint returns a JSON response containing a results array where each entry has fields: type, name, file, lines (array of [start, end]), signature, and body</given>
  <when>The test-automator subagent receives Treelint search output for function discovery</when>
  <then>The subagent parses the JSON to extract: (1) function names matching the search query, (2) file paths for locating source code, (3) line ranges [start, end] for precise Read() operations, and (4) function signatures for test stub generation, and the parsed data is used to inform test creation</then>
  <verification>
    <source_files>
      <file hint="Updated test-automator subagent definition">src/claude/agents/test-automator.md</file>
    </source_files>
    <test_file>tests/STORY-363/test_ac2_json_parsing.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Grep Fallback for Unsupported Languages

```xml
<acceptance_criteria id="AC3" implements="TREELINT-FALLBACK-001">
  <given>The test-automator subagent needs to discover functions in file types not supported by Treelint (e.g., C# .cs, Java .java, Go .go, Ruby .rb) or when the Treelint binary is unavailable (exit code 127) or fails at runtime</given>
  <when>The subagent detects an unsupported file extension or receives a non-zero exit code from Treelint</when>
  <then>The subagent falls back to using the native Grep tool (e.g., Grep(pattern="def |function |async function ", glob="**/*.cs")) following the fallback decision tree documented in the STORY-361 reference file, emits a warning-level message, and completes the function discovery without halting the workflow</then>
  <verification>
    <source_files>
      <file hint="Updated test-automator subagent definition">src/claude/agents/test-automator.md</file>
    </source_files>
    <test_file>tests/STORY-363/test_ac3_grep_fallback.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Test File to Source File Mapping Using Semantic Search

```xml
<acceptance_criteria id="AC4" implements="TREELINT-MAP-001">
  <given>The test-automator subagent needs to map test files to their corresponding source files to identify coverage gaps or generate tests for specific source functions</given>
  <when>The subagent performs test-to-source mapping for a supported language</when>
  <then>The subagent uses Treelint to: (1) search test directories for test functions, (2) identify source function names by removing the test_ prefix or extracting subjects from describe()/it() blocks, (3) search source directories for matching source functions, and (4) correlate results to build a test-to-source mapping that identifies untested functions</then>
  <verification>
    <source_files>
      <file hint="Updated test-automator subagent definition">src/claude/agents/test-automator.md</file>
    </source_files>
    <test_file>tests/STORY-363/test_ac4_test_source_mapping.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Performance Validation for Treelint Searches

```xml
<acceptance_criteria id="AC5" implements="TREELINT-PERF-001">
  <given>The test-automator subagent performs function discovery via Treelint on a typical project (up to 10,000 files)</given>
  <when>A treelint search --type function --format json command completes</when>
  <then>The search completes in less than 100 milliseconds for CLI mode (verified via the stats.elapsed_ms field in Treelint JSON output), and the total function discovery workflow adds no more than 200ms overhead compared to the previous Grep-only approach</then>
  <verification>
    <source_files>
      <file hint="Updated test-automator subagent definition">src/claude/agents/test-automator.md</file>
    </source_files>
    <test_file>tests/STORY-363/test_ac5_performance.sh</test_file>
    <coverage_threshold>80</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Progressive Disclosure Compliance (500-Line Limit)

```xml
<acceptance_criteria id="AC6" implements="TREELINT-SIZE-001">
  <given>The test-automator subagent definition file (src/claude/agents/test-automator.md) has a 500-line maximum per source-tree.md and tech-stack.md token budget constraints</given>
  <when>Treelint integration instructions are added to the test-automator subagent</when>
  <then>The updated test-automator.md file remains under 500 lines total, with Treelint-specific patterns either: (a) inlined if the file stays under 500 lines, or (b) extracted to a reference file at src/claude/agents/test-automator/references/treelint-patterns.md following ADR-012 progressive disclosure pattern, loaded on-demand via Read() instruction in the core file</then>
  <verification>
    <source_files>
      <file hint="Updated test-automator subagent definition">src/claude/agents/test-automator.md</file>
      <file hint="Optional Treelint reference file if extracted">src/claude/agents/test-automator/references/treelint-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-363/test_ac6_line_count.sh</test_file>
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
      name: "test-automator Subagent Definition"
      file_path: "src/claude/agents/test-automator.md"
      required_keys:
        - key: "Treelint Function Discovery Section"
          type: "markdown"
          example: "### Treelint-Aware Function Discovery"
          required: true
          validation: "Section must contain treelint search --type function --format json instruction"
          test_requirement: "Test: Grep for 'treelint search.*--type function.*--format json' in test-automator.md"

        - key: "JSON Parsing Instructions"
          type: "markdown"
          example: "Parse JSON results: type, name, file, lines, signature"
          required: true
          validation: "Must reference all 4 required JSON fields: name, file, lines, signature"
          test_requirement: "Test: Grep for 'name.*file.*lines.*signature' pattern in test-automator.md"

        - key: "Language Support Check"
          type: "markdown"
          example: "Check file extension: .py, .ts, .tsx, .js, .jsx, .rs, .md"
          required: true
          validation: "Must list all 7 supported extensions from tech-stack.md"
          test_requirement: "Test: Grep for '.py' AND '.ts' AND '.tsx' AND '.js' AND '.jsx' AND '.rs' AND '.md' in test-automator.md"

        - key: "Grep Fallback Section"
          type: "markdown"
          example: "### Fallback: Grep for Unsupported Languages"
          required: true
          validation: "Must reference native Grep tool (not Bash grep)"
          test_requirement: "Test: Grep for 'Grep(pattern=' fallback instruction in test-automator.md"

        - key: "Test-to-Source Mapping"
          type: "markdown"
          example: "### Test-to-Source File Mapping via Treelint"
          required: true
          validation: "Must describe bidirectional mapping between test and source functions"
          test_requirement: "Test: Grep for 'test.*source.*mapping' pattern in test-automator.md"

        - key: "Reference File Loading"
          type: "markdown"
          example: "Read(file_path=\"src/claude/agents/references/treelint-search-patterns.md\")"
          required: true
          validation: "Must contain Read() instruction for STORY-361 reference file"
          test_requirement: "Test: Grep for 'Read.*treelint.*patterns' in test-automator.md"

    - type: "Configuration"
      name: "Treelint Patterns Reference File (Conditional)"
      file_path: "src/claude/agents/test-automator/references/treelint-patterns.md"
      required_keys:
        - key: "Progressive Disclosure Extraction"
          type: "markdown"
          example: "Treelint search patterns extracted per ADR-012"
          required: false
          default: "Only created if test-automator.md exceeds 500 lines"
          validation: "If file exists, test-automator.md must contain Read() pointing to it"
          test_requirement: "Test: If treelint-patterns.md exists, verify test-automator.md references it via Read()"

  business_rules:
    - id: "BR-001"
      rule: "Treelint must be attempted first for all supported file extensions before falling back to Grep"
      trigger: "When function discovery is initiated for any file type"
      validation: "Check file extension against supported list, use Treelint if supported, Grep if not"
      error_handling: "If Treelint fails (non-zero exit), fall back to Grep with warning"
      test_requirement: "Test: test-automator.md Treelint section appears before Grep fallback section"
      priority: "Critical"

    - id: "BR-002"
      rule: "Empty Treelint results (exit code 0, zero matches) must NOT trigger Grep fallback"
      trigger: "When Treelint returns valid JSON with empty results array"
      validation: "Distinguish between exit code 0 (success, no matches) and non-zero (failure)"
      error_handling: "Return empty function list, do not invoke Grep"
      test_requirement: "Test: test-automator.md contains distinction between empty results and command failure"
      priority: "Critical"

    - id: "BR-003"
      rule: "All Treelint failures must result in successful Grep fallback with zero workflow interruption"
      trigger: "When Treelint returns non-zero exit code or malformed output"
      validation: "Workflow must never HALT due to Treelint issues"
      error_handling: "Warning-level message, Grep fallback, continue workflow"
      test_requirement: "Test: test-automator.md fallback section contains 'warning' and no 'HALT' or 'error' on Treelint failure"
      priority: "Critical"

    - id: "BR-004"
      rule: "Subagent file must remain under 500 lines; if exceeded, extract to references/"
      trigger: "After Treelint integration content is added"
      validation: "wc -l on test-automator.md <= 500"
      error_handling: "Extract Treelint patterns to references/treelint-patterns.md per ADR-012"
      test_requirement: "Test: wc -l test-automator.md <= 500; if >500, references/treelint-patterns.md exists"
      priority: "High"

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
    impact: "Projects using unsupported languages get text-based search only (no token reduction for those languages)"

  - id: TL-002
    component: "test-automator subagent"
    limitation: "Subagent is markdown documentation, not executable code - Treelint patterns are instructions, not programmatic implementations"
    decision: "workaround:Documentation-based patterns validated via structural tests (Grep for required sections)"
    discovered_phase: "Architecture"
    impact: "Tests are structural (verify sections exist in markdown) rather than functional (verify runtime behavior)"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Treelint Search:**
- Treelint search latency: < 100ms per invocation (p95) via stats.elapsed_ms
- Total discovery overhead: < 200ms additional vs. Grep-only approach
- Grep fallback latency: < 2 seconds (p95) for codebases up to 10,000 files

### Security

**Shell Injection Prevention:**
- All Treelint command arguments use simple patterns (alphanumeric + `*` wildcard only)
- Native Grep tool used for fallback (not `Bash(command="grep ...")`) per tech-stack.md constraint
- File paths from Treelint results validated before Read() to prevent path traversal

### Reliability

**Fallback Guarantees:**
- 100% of Treelint failures result in successful Grep fallback
- One-shot fallback: Treelint fails once → Grep once; no retry loops
- Empty results (exit code 0) treated as valid, NOT as failure
- All 5 failure modes handled: binary not found, permission denied, runtime error, unsupported type, malformed JSON

### Scalability

**Token Budget:**
- Core subagent file ≤ 500 lines per ADR-012
- Stateless search operations; no shared state between invocations
- Language support extensible by updating extension list only

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-361:** Create Treelint Skill Reference Files for Subagent Integration
  - **Why:** Provides the shared Treelint usage patterns referenced by test-automator
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

1. **Mixed-language projects:** Test-automator may need to discover functions across Python (.py - Treelint) and C# (.cs - Grep) in the same project. Per-file-extension decisions required, aggregating results from both tools.

2. **Non-standard test naming conventions:** Test functions may not follow `test_*` or `it()/describe()` patterns (e.g., `@pytest.mark.parametrize` decorators, nested describe blocks). Broad Treelint search first, then filter by convention.

3. **Empty results vs. command failure:** Treelint returning exit code 0 with empty results array is NOT a failure. Must distinguish from non-zero exit codes that trigger Grep fallback.

4. **Large function bodies exceeding context window:** Treelint's `body` field may contain very large functions (>500 lines). Use `lines` field for targeted `Read()` instead of consuming full body from JSON.

5. **File exceeding 500-line limit:** Current test-automator.md is 275 lines. Adding Treelint patterns (50-150 lines) may approach limit. Extract to references/ per ADR-012 if exceeded.

6. **Treelint binary version mismatch:** Pre-v0.12.0 versions lacking `--format json` support may fail with unrecognized flag error. Treat any non-zero exit code as failure and fall back to Grep.

7. **Concurrent invocations:** Multiple parallel test-automator invocations are safe (Treelint is stateless/read-only). No shared state between invocations per architecture constraint.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic (structural validation of markdown)

**Test Scenarios:**
1. **Happy Path:** test-automator.md contains Treelint search instruction for function discovery
2. **Edge Cases:**
   - Verify all 7 supported file extensions listed
   - Verify JSON parsing instruction references all required fields
   - Verify progressive disclosure compliance (≤500 lines)
3. **Error Cases:**
   - Verify Grep fallback section exists
   - Verify fallback uses warning level (not error/HALT)
   - Verify empty results handling documented

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **Reference File Loading:** Verify test-automator.md contains Read() for treelint-search-patterns.md
2. **End-to-End Pattern:** Verify Treelint → JSON parse → function list → test generation flow documented

---

## Acceptance Criteria Verification Checklist

### AC#1: Treelint Integration for Function Discovery

- [ ] test-automator.md contains `treelint search --type function` instruction - **Phase:** 2 - **Evidence:** test_ac1_treelint_function_discovery.sh
- [ ] Instruction uses `--format json` flag - **Phase:** 2 - **Evidence:** test_ac1_treelint_function_discovery.sh
- [ ] Uses Bash() tool for Treelint invocation - **Phase:** 2 - **Evidence:** test_ac1_treelint_function_discovery.sh

### AC#2: JSON Parsing of Treelint Search Results

- [ ] JSON parsing instructions reference `name` field - **Phase:** 2 - **Evidence:** test_ac2_json_parsing.sh
- [ ] JSON parsing instructions reference `file` field - **Phase:** 2 - **Evidence:** test_ac2_json_parsing.sh
- [ ] JSON parsing instructions reference `lines` field - **Phase:** 2 - **Evidence:** test_ac2_json_parsing.sh
- [ ] JSON parsing instructions reference `signature` field - **Phase:** 2 - **Evidence:** test_ac2_json_parsing.sh

### AC#3: Grep Fallback for Unsupported Languages

- [ ] Fallback section exists in test-automator.md - **Phase:** 2 - **Evidence:** test_ac3_grep_fallback.sh
- [ ] Fallback uses native Grep tool (not Bash grep) - **Phase:** 2 - **Evidence:** test_ac3_grep_fallback.sh
- [ ] Warning-level messaging on fallback - **Phase:** 2 - **Evidence:** test_ac3_grep_fallback.sh

### AC#4: Test File to Source File Mapping

- [ ] Test-to-source mapping instructions present - **Phase:** 3 - **Evidence:** test_ac4_test_source_mapping.sh
- [ ] Uses Treelint for bidirectional search - **Phase:** 3 - **Evidence:** test_ac4_test_source_mapping.sh

### AC#5: Performance Validation

- [ ] Performance target (<100ms) documented - **Phase:** 3 - **Evidence:** test_ac5_performance.sh
- [ ] stats.elapsed_ms field referenced - **Phase:** 3 - **Evidence:** test_ac5_performance.sh

### AC#6: Progressive Disclosure Compliance

- [ ] test-automator.md file line count ≤ 500 - **Phase:** 4 - **Evidence:** test_ac6_line_count.sh
- [ ] If >500 lines, reference file exists at references/treelint-patterns.md - **Phase:** 4 - **Evidence:** test_ac6_line_count.sh

---

**Checklist Progress:** 0/15 items complete (0%)

---

## Definition of Done

### Implementation
- [x] test-automator.md updated with Treelint function discovery section - Completed: Phase 3.5 Treelint-Aware Function Discovery section added (lines 94-149)
- [x] JSON parsing instructions added for Treelint response fields - Completed: JSON parsing section documents all 4 fields (name, file, lines, signature) at lines 110-122
- [x] Language support check (7 extensions) documented in subagent - Completed: All 7 supported extensions listed at line 106 (.py, .ts, .tsx, .js, .jsx, .rs, .md)
- [x] Grep fallback section with warning-level messaging added - Completed: Fallback section at lines 124-134 with warning-level message and no-HALT instruction
- [x] Test-to-source file mapping via Treelint documented - Completed: Test-to-source mapping section at lines 136-149 with bidirectional search
- [x] STORY-361 reference file loading instruction (Read()) added - Completed: Read() instruction at line 98 loads shared treelint-search-patterns.md
- [x] File size ≤ 500 lines verified (extract to references/ if needed) - Completed: File is 331 lines (169 lines under limit), no extraction needed

### Quality
- [x] All 6 acceptance criteria have passing tests - Completed: All 6 ACs verified with HIGH confidence (31/31 assertions passing)
- [x] Edge cases documented (mixed languages, empty results, version mismatch) - Completed: BR-002 empty results distinction documented, fallback covers 5 failure modes
- [x] NFRs met (performance <100ms, zero workflow interruptions) - Completed: Performance target documented at line 107, no-HALT instruction at line 133
- [x] Code coverage >95% for structural tests - Completed: 31/31 structural assertions passing (100% coverage)

### Testing
- [x] test_ac1_treelint_function_discovery.sh passes - Completed: 5/5 assertions pass
- [x] test_ac2_json_parsing.sh passes - Completed: 6/6 assertions pass
- [x] test_ac3_grep_fallback.sh passes - Completed: 6/6 assertions pass
- [x] test_ac4_test_source_mapping.sh passes - Completed: 5/5 assertions pass
- [x] test_ac5_performance.sh passes - Completed: 4/4 assertions pass
- [x] test_ac6_line_count.sh passes - Completed: 5/5 assertions pass

### Documentation
- [x] test-automator.md contains clear Treelint usage instructions - Completed: Phase 3.5 section with detailed step-by-step Treelint integration workflow
- [x] Fallback behavior documented for all failure modes - Completed: 5 failure modes documented (binary not found, permission denied, runtime error, unsupported type, malformed JSON)
- [x] Reference file loading documented (STORY-361 dependency) - Completed: Read() instruction at line 98 references src/claude/agents/references/treelint-search-patterns.md

---

## Implementation Notes

**Developer:** claude/opus
**Implemented:** 2026-02-06
**Branch:** main

- [x] test-automator.md updated with Treelint function discovery section - Completed: Phase 3.5 Treelint-Aware Function Discovery section added (lines 94-149)
- [x] JSON parsing instructions added for Treelint response fields - Completed: JSON parsing section documents all 4 fields (name, file, lines, signature) at lines 110-122
- [x] Language support check (7 extensions) documented in subagent - Completed: All 7 supported extensions listed at line 106 (.py, .ts, .tsx, .js, .jsx, .rs, .md)
- [x] Grep fallback section with warning-level messaging added - Completed: Fallback section at lines 124-134 with warning-level message and no-HALT instruction
- [x] Test-to-source file mapping via Treelint documented - Completed: Test-to-source mapping section at lines 136-149 with bidirectional search
- [x] STORY-361 reference file loading instruction (Read()) added - Completed: Read() instruction at line 98 loads shared treelint-search-patterns.md
- [x] File size ≤ 500 lines verified (extract to references/ if needed) - Completed: File is 331 lines (169 lines under limit), no extraction needed
- [x] All 6 acceptance criteria have passing tests - Completed: All 6 ACs verified with HIGH confidence (31/31 assertions passing)
- [x] Edge cases documented (mixed languages, empty results, version mismatch) - Completed: BR-002 empty results distinction documented, fallback covers 5 failure modes
- [x] NFRs met (performance <100ms, zero workflow interruptions) - Completed: Performance target documented at line 107, no-HALT instruction at line 133
- [x] Code coverage >95% for structural tests - Completed: 31/31 structural assertions passing (100% coverage)
- [x] test_ac1_treelint_function_discovery.sh passes - Completed: 5/5 assertions pass
- [x] test_ac2_json_parsing.sh passes - Completed: 6/6 assertions pass
- [x] test_ac3_grep_fallback.sh passes - Completed: 6/6 assertions pass
- [x] test_ac4_test_source_mapping.sh passes - Completed: 5/5 assertions pass
- [x] test_ac5_performance.sh passes - Completed: 4/4 assertions pass
- [x] test_ac6_line_count.sh passes - Completed: 5/5 assertions pass
- [x] test-automator.md contains clear Treelint usage instructions - Completed: Phase 3.5 section with detailed step-by-step Treelint integration workflow
- [x] Fallback behavior documented for all failure modes - Completed: 5 failure modes documented (binary not found, permission denied, runtime error, unsupported type, malformed JSON)
- [x] Reference file loading documented (STORY-361 dependency) - Completed: Read() instruction at line 98 references src/claude/agents/references/treelint-search-patterns.md

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-05 | claude/story-requirements-analyst | Created | Story created via /create-story batch mode (EPIC-057) | STORY-363-update-test-automator-treelint-integration.story.md |
| 2026-02-05 | claude/sprint-planner | Sprint Planning | Assigned to Sprint-9, status → Ready for Dev | STORY-363-update-test-automator-treelint-integration.story.md |
| 2026-02-06 | claude/opus | Development (TDD) | Implemented Treelint integration in test-automator.md (56 lines added), 6/6 ACs passing, status → Dev Complete | src/claude/agents/test-automator.md, tests/STORY-363/*.sh |
| 2026-02-06 | claude/qa-result-interpreter | QA Deep | PASS WITH WARNINGS: 31/31 tests passing, 0 blocking violations, 2 HIGH advisories (documentation-level), status → QA Approved | STORY-363-qa-report.md |

## Notes

**Design Decisions:**
- Treelint invoked directly via Bash tool per architecture constraint (subagents cannot delegate to wrapper subagent)
- Shared reference file from STORY-361 loaded via Read() to minimize duplication across 7 subagents
- Progressive disclosure (ADR-012) used if test-automator.md exceeds 500-line limit
- Structural tests (Grep for markdown sections) rather than runtime tests, since subagent is a markdown definition

**Open Questions:**
- [ ] Exact line budget for Treelint section (current file is 275 lines, ~225 lines remaining) - **Owner:** Developer - **Due:** During development

**Related ADRs:**
- ADR-012: Progressive Disclosure for Subagents
- ADR-013: Treelint Integration for AST-Aware Code Search

**References:**
- EPIC-057: Treelint Subagent Integration
- STORY-361: Create Treelint Skill Reference Files
- STORY-362: Implement Hybrid Fallback Logic
- tech-stack.md lines 104-166: Treelint approved section
- source-tree.md lines 232-262: Subagent directory rules

---

Story Template Version: 2.8
Last Updated: 2026-02-05
