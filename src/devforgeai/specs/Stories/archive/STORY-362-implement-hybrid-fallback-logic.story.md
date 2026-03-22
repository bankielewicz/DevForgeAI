---
id: STORY-362
title: Implement Hybrid Fallback Logic (Treelint to Grep)
type: feature
epic: EPIC-057
sprint: Sprint-10
status: QA Approved
points: 3
depends_on: ["STORY-361"]
priority: Medium
advisory: false
source_gap: null
source_story: null
assigned_to: Unassigned
created: 2026-02-04
format_version: "2.8"
---

# Story: Implement Hybrid Fallback Logic (Treelint to Grep)

## Description

**As a** DevForgeAI subagent (one of the 7 target subagents: test-automator, backend-architect, code-reviewer, security-auditor, refactoring-specialist, coverage-analyzer, anti-pattern-scanner),
**I want** automatic fallback from Treelint to the native Grep tool when I encounter a file type outside Treelint's supported language set or when the Treelint binary is unavailable,
**so that** my code search workflow completes successfully regardless of the project's programming language mix, without surfacing errors to the orchestrating skill or halting execution.

## Provenance

```xml
<provenance>
  <origin document="EPIC-057" section="Features">
    <quote>"Feature 9: Hybrid Fallback Logic Implementation - Implement automatic fallback to Grep for unsupported languages"</quote>
    <line_reference>lines 79-82</line_reference>
    <quantified_impact>Seamless experience regardless of file type, zero workflow failures when Treelint unavailable</quantified_impact>
  </origin>

  <decision rationale="per-subagent-inline-fallback">
    <selected>Each subagent implements fallback internally following shared reference pattern</selected>
    <rejected alternative="wrapper-subagent">
      Subagents cannot delegate to other subagents per architecture constraint (architecture-constraints.md, lines 24-26)
    </rejected>
    <trade_off>Slight code duplication across subagents, but respects architecture constraints and ensures isolation</trade_off>
  </decision>

  <stakeholder role="Framework Architect" goal="zero-workflow-failures">
    <quote>"Seamless experience regardless of file type"</quote>
    <source>EPIC-057, Feature 9</source>
  </stakeholder>
</provenance>
```

## Acceptance Criteria

### AC#1: Language Support Detection via File Extension Checking

```xml
<acceptance_criteria id="AC1" implements="FALLBACK-001">
  <given>A subagent receives a code search request targeting files with a specific extension (e.g., .cs, .java, .go, .py, .ts)</given>
  <when>The subagent evaluates whether to use Treelint or Grep for the search</when>
  <then>The subagent checks the target file extension against the supported language list (Python: .py, TypeScript: .ts/.tsx, JavaScript: .js/.jsx, Rust: .rs, Markdown: .md) and selects Treelint only when the extension is in the supported set, otherwise selects Grep without any error or workflow interruption</then>
  <verification>
    <source_files>
      <file hint="Treelint reference with fallback patterns">src/claude/agents/references/treelint-search-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-362/test_ac1_language_detection.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Automatic Grep Fallback for Unsupported File Types

```xml
<acceptance_criteria id="AC2" implements="FALLBACK-002">
  <given>A subagent needs to search for functions, classes, or patterns in a file type not supported by Treelint (e.g., .cs, .java, .go, .rb, .php)</given>
  <when>The subagent's language support check determines the file type is unsupported</when>
  <then>The subagent bypasses Treelint entirely and uses the native Grep tool (e.g., Grep(pattern="def |function |class ", glob="**/*.cs")) to perform text-based search, returning results without failure, and the results are usable for downstream analysis</then>
  <verification>
    <source_files>
      <file hint="Treelint reference with fallback patterns">src/claude/agents/references/treelint-search-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-362/test_ac2_grep_fallback.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Warning Message on Fallback (Not Error)

```xml
<acceptance_criteria id="AC3" implements="FALLBACK-003">
  <given>A subagent falls back from Treelint to Grep for any reason (unsupported file type, binary not found, command failure)</given>
  <when>The fallback is triggered</when>
  <then>The subagent emits a warning-level message (not error) indicating the fallback occurred with the reason (e.g., "Treelint fallback: .cs files not supported, using Grep"), and the workflow continues without halting, without exceptions, and without marking the search as failed</then>
  <verification>
    <source_files>
      <file hint="Treelint reference with fallback patterns">src/claude/agents/references/treelint-search-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-362/test_ac3_warning_not_error.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: No Workflow Failure When Treelint Binary Is Unavailable

```xml
<acceptance_criteria id="AC4" implements="FALLBACK-004">
  <given>The Treelint binary is not installed, not on PATH, or returns a non-zero exit code (exit code 127 for not found, 126 for permission denied)</given>
  <when>A subagent attempts to invoke Treelint via Bash(command="treelint search ...")</when>
  <then>The subagent detects the failure (non-zero exit code), logs a warning (e.g., "Treelint unavailable: binary not found, falling back to Grep"), and completes the search using native Grep with equivalent text-based patterns, with zero impact on the calling skill's workflow state</then>
  <verification>
    <source_files>
      <file hint="Treelint reference with fallback patterns">src/claude/agents/references/treelint-search-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-362/test_ac4_binary_unavailable.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Treelint Command Failure Fallback (Runtime Errors)

```xml
<acceptance_criteria id="AC5" implements="FALLBACK-005">
  <given>Treelint binary is installed and supports the file type, but the command fails at runtime (malformed JSON output, timeout, parse error on malformed source code)</given>
  <when>A subagent receives a non-zero exit code or unparseable output from a Treelint command</when>
  <then>The subagent catches the failure, logs a warning (e.g., "Treelint runtime error: malformed JSON, falling back to Grep"), and retries the search using native Grep with the equivalent text-based pattern, without propagating the error to the parent skill</then>
  <verification>
    <source_files>
      <file hint="Treelint reference with fallback patterns">src/claude/agents/references/treelint-search-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-362/test_ac5_runtime_error_fallback.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Reusable Fallback Pattern Documented in Reference File

```xml
<acceptance_criteria id="AC6" implements="FALLBACK-006">
  <given>STORY-361 has created the shared reference file documenting Treelint patterns</given>
  <when>The fallback logic validation is performed</when>
  <then>The Fallback Decision Tree section contains a complete, step-by-step reusable pattern: (1) check file extension, (2) attempt Treelint if supported, (3) detect failure via exit code, (4) fall back to Grep with equivalent pattern, (5) log warning with reason, (6) return results, with specific Grep equivalents for each Treelint search type (function, class, map, deps)</then>
  <verification>
    <source_files>
      <file hint="Treelint reference with fallback patterns">src/claude/agents/references/treelint-search-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-362/test_ac6_reusable_pattern.sh</test_file>
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
      name: "Treelint Fallback Decision Tree"
      file_path: "src/claude/agents/references/treelint-search-patterns.md"
      required_keys:
        - key: "Fallback Decision Tree section"
          type: "markdown"
          required: true
          test_requirement: "Test: Reference file contains ## Fallback Decision Tree with numbered steps starting with extension check"
        - key: "Grep pattern equivalents for function search"
          type: "markdown"
          required: true
          test_requirement: "Test: Fallback section contains Grep pattern equivalent for treelint search --type function"
        - key: "Grep pattern equivalents for class search"
          type: "markdown"
          required: true
          test_requirement: "Test: Fallback section contains Grep pattern equivalent for treelint search --type class"
        - key: "Grep pattern equivalents for map/deps search"
          type: "markdown"
          required: true
          test_requirement: "Test: Fallback section contains Grep pattern equivalents for treelint map and treelint deps"
        - key: "Warning message format specification"
          type: "markdown"
          required: true
          test_requirement: "Test: Fallback section specifies warning message format with 'Treelint fallback:' prefix"

    - type: "Configuration"
      name: "Supported Language Extension Map"
      file_path: "src/claude/agents/references/treelint-search-patterns.md"
      required_keys:
        - key: "Supported extensions list"
          type: "markdown_table"
          required: true
          test_requirement: "Test: Language matrix contains exactly 7 supported extensions (.py, .ts, .tsx, .js, .jsx, .rs, .md)"
        - key: "Unsupported extensions list"
          type: "markdown_table"
          required: true
          test_requirement: "Test: Language matrix contains 4+ unsupported language rows with Grep fallback strategy"
        - key: "Catch-all row"
          type: "markdown_table"
          required: true
          test_requirement: "Test: Matrix contains wildcard/other row defaulting to Grep"

    - type: "Service"
      name: "Fallback Runtime Behavior"
      file_path: "src/claude/agents/references/treelint-search-patterns.md"
      requirements:
        - id: "FALLBACK-001"
          description: "Must check file extension against supported language list before invoking Treelint"
          implements_ac: ["AC#1"]
          testable: true
          test_requirement: "Test: Subagent evaluating .cs file selects Grep without attempting Treelint"
          priority: "Critical"
        - id: "FALLBACK-002"
          description: "Must use native Grep tool (not Bash grep) for fallback searches"
          implements_ac: ["AC#2"]
          testable: true
          test_requirement: "Test: Fallback patterns use Grep() tool syntax, not Bash(command='grep ...')"
          priority: "Critical"
        - id: "FALLBACK-003"
          description: "Must emit warning-level message (not error) on every fallback"
          implements_ac: ["AC#3"]
          testable: true
          test_requirement: "Test: Fallback message uses 'warning' terminology, zero 'error' or 'ERROR' strings"
          priority: "High"
        - id: "FALLBACK-004"
          description: "Must handle exit code 127 (not found) and 126 (permission denied) with Grep fallback"
          implements_ac: ["AC#4"]
          testable: true
          test_requirement: "Test: Exit codes 126, 127 trigger Grep fallback with appropriate warning"
          priority: "Critical"
        - id: "FALLBACK-005"
          description: "Must handle malformed JSON and runtime errors with Grep fallback"
          implements_ac: ["AC#5"]
          testable: true
          test_requirement: "Test: Non-JSON Treelint output triggers Grep fallback, not parse exception"
          priority: "High"
        - id: "FALLBACK-006"
          description: "Must provide Grep equivalents for all 4 Treelint search types"
          implements_ac: ["AC#6"]
          testable: true
          test_requirement: "Test: Count of documented Grep fallback patterns >= 4 (function, class, map, deps)"
          priority: "Critical"

  business_rules:
    - id: "BR-001"
      rule: "All Treelint failures must result in Grep fallback, never workflow HALT"
      trigger: "When Treelint returns non-zero exit code or unparseable output"
      validation: "No HALT or exception in fallback code path"
      error_handling: "Catch all exceptions, fall back to Grep, emit warning"
      test_requirement: "Test: No fallback code path contains HALT, raise, or throw statements"
      priority: "Critical"

    - id: "BR-002"
      rule: "Fallback is one-shot: Treelint fails -> Grep once, no retry of Treelint"
      trigger: "When fallback is triggered"
      validation: "Fallback path goes directly to Grep, no re-attempt of Treelint"
      error_handling: "Single fallback path with no loop"
      test_requirement: "Test: Fallback logic contains exactly one Treelint attempt and one Grep attempt per search"
      priority: "High"

    - id: "BR-003"
      rule: "Empty result set from Treelint is valid (not a failure), does not trigger fallback"
      trigger: "When Treelint returns zero results with exit code 0"
      validation: "Exit code 0 with empty results array is treated as successful search"
      error_handling: "Return empty result set to caller, no warning emitted"
      test_requirement: "Test: Treelint returning empty results array with exit 0 does not trigger Grep fallback"
      priority: "High"

    - id: "BR-004"
      rule: "Supported language list is authoritative from tech-stack.md (lines 139-147)"
      trigger: "When evaluating file extension support"
      validation: "Extension list matches tech-stack.md exactly"
      error_handling: "If discrepancy, tech-stack.md is authoritative"
      test_requirement: "Test: Supported extensions in fallback logic match tech-stack.md lines 139-147"
      priority: "Critical"

    - id: "BR-005"
      rule: "Warning messages must not contain the word 'error' or 'ERROR'"
      trigger: "When emitting fallback warning"
      validation: "Grep for 'error|ERROR' in warning message templates returns 0 matches"
      error_handling: "Replace 'error' with 'issue' or 'failure' in warning text"
      test_requirement: "Test: All warning message templates contain 'warning' and zero instances of 'error'"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Fallback decision latency"
      metric: "< 10ms for file extension check (string comparison against 7-element list)"
      test_requirement: "Test: Extension check function completes within 10ms for worst-case input"
      priority: "Medium"

    - id: "NFR-002"
      category: "Reliability"
      requirement: "Zero workflow failures from Treelint unavailability"
      metric: "100% of Treelint failures result in successful Grep fallback"
      test_requirement: "Test: All 5 failure modes (binary missing, permission denied, runtime error, unsupported type, malformed output) result in successful Grep search"
      priority: "Critical"

    - id: "NFR-003"
      category: "Reliability"
      requirement: "Warning emission on every fallback"
      metric: "100% of fallback events produce a warning message"
      test_requirement: "Test: Every fallback trigger produces exactly one warning message"
      priority: "High"

    - id: "NFR-004"
      category: "Scalability"
      requirement: "Supports all 7 target subagents without per-subagent customization"
      metric: "Single reusable pattern documented, no subagent-specific branches"
      test_requirement: "Test: Fallback pattern contains no subagent-specific logic or conditional branches by agent name"
      priority: "High"

    - id: "NFR-005"
      category: "Security"
      requirement: "Native Grep tool usage prevents shell injection"
      metric: "Zero Bash(command='grep ...') invocations in fallback patterns"
      test_requirement: "Test: All fallback patterns use Grep() tool, not Bash grep command"
      priority: "Critical"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Treelint v0.12.0"
    limitation: "Supports only 5 languages - C#, Java, Go, and others require Grep fallback"
    decision: "workaround:Grep fallback implemented for all unsupported file types"
    discovered_phase: "Architecture"
    impact: "Subagents working with unsupported languages get text-based search (lower precision than AST-based)"

  - id: TL-002
    component: "Architecture Constraints"
    limitation: "Subagents cannot delegate to wrapper subagent for centralized fallback"
    decision: "workaround:Each subagent implements fallback internally following shared reference pattern"
    discovered_phase: "Architecture"
    impact: "Slight pattern duplication across 7 subagents, mitigated by shared reference documentation"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Fallback Decision:**
- Extension check: < 10ms (string comparison against 7-element list)
- Total fallback overhead: < 50ms additional latency vs direct Grep
- Grep search: < 2 seconds (p95) on codebases up to 10,000 files

---

### Security

**Shell Injection Prevention:**
- All fallback patterns use native Grep tool, not Bash grep
- No credential or secret exposure in warning messages
- File extension extracted via last-dot-split (no path traversal)

---

### Reliability

**Zero-Failure Guarantee:**
- 100% of Treelint failures result in successful Grep fallback
- All 5+ failure modes have defined Grep recovery paths
- One-shot fallback: no retry loops
- 100% of fallback events emit warning messages

---

### Scalability

**Reusable Pattern:**
- Single pattern for all 7 target subagents + future subagents
- Language list extensible by adding extensions
- No shared state between parallel subagent invocations

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-361:** Create Treelint Skill Reference Files for Subagent Integration
  - **Why:** Documents the fallback patterns that this story validates at runtime
  - **Status:** Backlog

### External Dependencies

- [ ] **Treelint v0.12.0+ binary:** Must be available for testing supported language paths
  - **Owner:** EPIC-055
  - **ETA:** Before sprint start
  - **Status:** In Progress
  - **Impact if delayed:** Can validate fallback behavior (Grep paths) but not Treelint success paths

### Technology Dependencies

- [ ] **Treelint** v0.12.0+
  - **Purpose:** AST-aware code search (primary tool)
  - **Approved:** Yes (ADR-013)
  - **Added to dependencies.md:** Yes

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for fallback logic paths

**Test Scenarios:**
1. **Happy Path:** Supported file type (.py) → Treelint used, results returned
2. **Fallback Path:** Unsupported file type (.cs) → Grep used, results returned, warning emitted
3. **Edge Cases:**
   - Binary not found (exit 127) → Grep fallback + warning
   - Permission denied (exit 126) → Grep fallback + warning
   - Malformed JSON → Grep fallback + warning
   - Empty result from Treelint (exit 0) → NOT a fallback trigger
   - Mixed-language project → per-file decision
   - Extensionless files → Grep default
4. **Error Cases:**
   - Both Treelint and Grep return empty → valid empty result, no error

### Integration Tests

**Coverage Target:** 85%+ for subagent reference loading + fallback execution

**Test Scenarios:**
1. **Subagent loads reference file and follows fallback pattern**
2. **Concurrent subagents with different file types make independent decisions**

---

## Acceptance Criteria Verification Checklist

### AC#1: Language Support Detection

- [ ] Extension check against supported list implemented - **Phase:** 2 - **Evidence:** Reference file decision tree step 1
- [ ] Supported extensions match tech-stack.md (7 extensions) - **Phase:** 2 - **Evidence:** Grep match count
- [ ] Unsupported extension routes to Grep without Treelint attempt - **Phase:** 2 - **Evidence:** Test for .cs file

### AC#2: Automatic Grep Fallback

- [ ] Grep pattern for function search documented - **Phase:** 2 - **Evidence:** Grep(pattern= in reference
- [ ] Grep pattern for class search documented - **Phase:** 2 - **Evidence:** Grep(pattern= in reference
- [ ] Results usable by subagent downstream - **Phase:** 3 - **Evidence:** Integration test

### AC#3: Warning Message (Not Error)

- [ ] Warning format specified - **Phase:** 2 - **Evidence:** "Treelint fallback:" prefix in docs
- [ ] Zero "error"/"ERROR" in warning messages - **Phase:** 2 - **Evidence:** Grep for error returns 0
- [ ] Workflow continues after warning - **Phase:** 3 - **Evidence:** No HALT after warning

### AC#4: Binary Unavailable Handling

- [ ] Exit code 127 handling documented - **Phase:** 2 - **Evidence:** Error handling section
- [ ] Exit code 126 handling documented - **Phase:** 2 - **Evidence:** Error handling section
- [ ] Grep fallback succeeds when binary missing - **Phase:** 3 - **Evidence:** Test execution

### AC#5: Runtime Error Fallback

- [ ] Malformed JSON handling - **Phase:** 2 - **Evidence:** Error handling section
- [ ] Non-zero exit code handling - **Phase:** 2 - **Evidence:** Error handling section
- [ ] Grep fallback after runtime error - **Phase:** 3 - **Evidence:** Test execution

### AC#6: Reusable Pattern

- [ ] Decision tree with 6 steps documented - **Phase:** 2 - **Evidence:** Numbered steps
- [ ] Grep equivalents for 4 search types - **Phase:** 2 - **Evidence:** Function, class, map, deps
- [ ] Pattern is subagent-agnostic - **Phase:** 2 - **Evidence:** No agent-specific branches

---

**Checklist Progress:** 0/20 items complete (0%)

---

## Definition of Done

### Implementation
- [x] Fallback decision tree documented in STORY-361 reference file
- [x] Language extension check as first gate in decision tree
- [x] Grep pattern equivalents for all 4 Treelint search types
- [x] Warning message format specified (not error)
- [x] Exit code handling for 127, 126, 1, and other non-zero codes
- [x] Malformed JSON output handling documented
- [x] Empty result set distinguished from failure (BR-003)

### Quality
- [x] All 6 acceptance criteria have passing tests
- [x] Zero "error"/"ERROR" in fallback warning messages (BR-005)
- [x] One-shot fallback verified (no retry loops) (BR-002)
- [x] Extension list matches tech-stack.md lines 139-147 (BR-004)
- [x] All Treelint failures route to Grep (BR-001)

### Testing
- [x] Structural tests validate decision tree exists
- [x] Pattern tests validate Grep equivalents for each search type
- [x] Exit code tests for 0, 1, 126, 127
- [x] Warning message format validation
- [x] Integration test: subagent loads reference and follows pattern

### Documentation
- [x] Fallback patterns integrated into STORY-361 reference file
- [x] Warning message format documented
- [x] Edge cases documented (mixed-language, extensionless files, version mismatch)

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-04 15:15 | claude/story-requirements-analyst | Created | Story created from EPIC-057 Feature 9 (Batch mode) | STORY-362-implement-hybrid-fallback-logic.story.md |
| 2026-02-05 | claude/sprint-planner | Sprint Planning | Assigned to Sprint-10, status → Ready for Dev | STORY-362-implement-hybrid-fallback-logic.story.md |
| 2026-02-06 | claude/backend-architect | /dev Phase 03 | Implemented 6-step fallback decision tree, exit code handling, warning format | src/claude/agents/references/treelint-search-patterns.md |
| 2026-02-06 | claude/dev-result-interpreter | /dev Phase 10 | Dev Complete: 6/6 ACs passed, 41 tests, all DoD items complete | STORY-362-implement-hybrid-fallback-logic.story.md |
| 2026-02-06 | claude/qa-result-interpreter | QA Deep | PASSED: 41/41 tests, 3/3 validators, 0 blocking violations | devforgeai/qa/reports/STORY-362-qa-report.md |

## Implementation Notes

- Extended Fallback Decision Tree from 4 to 6 steps (AC#6)
- Added Step 3: Detect failure via exit code (127, 126, 1+)
- Added Step 5: Log warning with fallback reason
- Added Step 6: Return results to caller
- Added Warning Message Format section with `Treelint fallback:` prefix (AC#3)
- Updated Scenario 1 to include exit code 126 (permission denied) (AC#4)
- Replaced "error" with "failure" in warning examples to comply with BR-005
- All 41 tests passing across 6 AC test files

## Notes

**Design Decisions:**
- Per-subagent inline fallback chosen over wrapper subagent due to architecture constraint (subagents cannot delegate to other subagents)
- Warning-level messages chosen over error-level to prevent workflow interruption
- One-shot fallback (no retry) chosen for simplicity and predictability
- Empty results distinguished from failures to prevent unnecessary fallbacks

**Open Questions:**
- [ ] Should version detection be implemented or just rely on command failure? - **Owner:** Framework Architect - **Due:** Before dev start

**Related ADRs:**
- ADR-013: Treelint Integration for AST-Aware Code Search
- ADR-007: Remove ast-grep and Evaluate Tree-sitter

**References:**
- EPIC-057: Treelint Subagent Integration
- STORY-361: Treelint Skill Reference Files (dependency)
- tech-stack.md: Treelint language support (lines 139-147)
- architecture-constraints.md: Subagent isolation rules (lines 60-63)

---

Story Template Version: 2.8
Last Updated: 2026-02-04
