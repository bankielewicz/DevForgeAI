---
id: STORY-370
title: Integrate Dependency Graph Analysis via Treelint deps
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

# Story: Integrate Dependency Graph Analysis via Treelint deps

## Description

**As a** DevForgeAI AI agent (specifically refactoring-specialist and code-reviewer),
**I want** to query function call relationships via `treelint deps --calls --symbol <name> --format json` and receive structured caller/callee data,
**so that** I can perform accurate impact analysis before refactoring and validate dependency integrity during code reviews.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-009" section="treelint-integration">
    <quote>"Leverage Treelint's full capabilities beyond basic symbol search, including dependency graph analysis"</quote>
    <line_reference>EPIC-058, lines 19-21</line_reference>
    <quantified_impact>Enables call chain analysis for impact assessment during refactoring and code review</quantified_impact>
  </origin>

  <decision rationale="treelint-cli-integration-over-custom-parser">
    <selected>Use treelint deps --calls CLI command for dependency graph queries</selected>
    <rejected alternative="custom-ast-parser">
      Building a custom AST parser would duplicate Treelint's existing capability and violate the no-modification constraint
    </rejected>
    <trade_off>Dependent on Treelint v0.12.0 binary availability; fallback to Grep when unavailable</trade_off>
  </decision>

  <stakeholder role="AI Agent" goal="impact-analysis">
    <quote>"Understand function relationships, identify impact of changes"</quote>
    <source>EPIC-058, Feature 1 description</source>
  </stakeholder>
</provenance>
```

---

## Acceptance Criteria

### AC#1: Successful dependency query returns callers and callees

```xml
<acceptance_criteria id="AC1" implements="SVC-001">
  <given>A codebase with indexed function relationships and the Treelint daemon or CLI available</given>
  <when>The command treelint deps --calls --symbol symbolName --format json is executed via Bash</when>
  <then>The JSON response contains a symbol field matching the queried name, a callers array where each entry has name, file, and line fields, and a callees array where each entry has name, file, and line fields</then>
  <verification>
    <source_files>
      <file hint="Treelint skill reference">src/claude/skills/devforgeai-development/references/treelint-integration.md</file>
    </source_files>
    <test_file>tests/STORY-370/test_ac1_dependency_query.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: JSON output is parsed into a structured result object

```xml
<acceptance_criteria id="AC2" implements="SVC-001">
  <given>The raw JSON response from treelint deps --calls --symbol name --format json</given>
  <when>The subagent parses the response</when>
  <then>The parsed result provides the queried symbol name as a string, callers as a list of objects with name (string), file (string, relative path), and line (positive integer), callees as a list of objects with the same fields, and invalid or malformed JSON triggers a structured error (not a crash)</then>
  <verification>
    <source_files>
      <file hint="Treelint skill reference">src/claude/skills/devforgeai-development/references/treelint-integration.md</file>
    </source_files>
    <test_file>tests/STORY-370/test_ac2_json_parsing.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Error handling for symbol-not-found and daemon-not-running

```xml
<acceptance_criteria id="AC3" implements="SVC-002,SVC-003">
  <given>The Treelint CLI is installed but either the queried symbol does not exist in the index or the Treelint daemon is not running</given>
  <when>treelint deps --calls --symbol unknownSymbol --format json is executed and returns a non-zero exit code or an error response</when>
  <then>The subagent returns a structured error result containing error type (symbol_not_found, daemon_not_running, treelint_unavailable, or unknown_error), the original symbol name queried, a human-readable error message, and falls back to Grep-based text search when Treelint is unavailable</then>
  <verification>
    <source_files>
      <file hint="Treelint skill reference">src/claude/skills/devforgeai-development/references/treelint-integration.md</file>
    </source_files>
    <test_file>tests/STORY-370/test_ac3_error_handling.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Integration with refactoring-specialist for impact analysis

```xml
<acceptance_criteria id="AC4" implements="WKR-001,WKR-002">
  <given>The refactoring-specialist subagent is invoked during TDD Phase 3 (Refactor) to refactor a function</given>
  <when>The refactoring-specialist queries treelint deps --calls --symbol functionToRefactor --format json before applying changes</when>
  <then>The callers list is used to identify all call sites that may be affected by the refactoring, and the refactoring-specialist logs the impact scope (number of callers and callees) before proceeding</then>
  <verification>
    <source_files>
      <file hint="Refactoring specialist agent">src/claude/agents/refactoring-specialist.md</file>
    </source_files>
    <test_file>tests/STORY-370/test_ac4_refactoring_integration.sh</test_file>
    <coverage_threshold>85</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Performance validation under 200ms for typical queries

```xml
<acceptance_criteria id="AC5" implements="NFR-001">
  <given>A codebase with a generated Treelint index (.treelint/index.db present)</given>
  <when>treelint deps --calls --symbol name --format json is executed for a symbol with fewer than 50 callers/callees</when>
  <then>The command completes (exit code 0 and JSON output received) in less than 200 milliseconds wall-clock time, measured from command invocation to output capture</then>
  <verification>
    <test_file>tests/STORY-370/test_ac5_performance.sh</test_file>
    <coverage_threshold>80</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Integration with code-reviewer for dependency validation

```xml
<acceptance_criteria id="AC6" implements="REVIEW-001,REVIEW-002">
  <given>The code-reviewer subagent is invoked during the dev workflow to review code changes</given>
  <when>The code-reviewer identifies a modified function and queries treelint deps --calls --symbol modifiedFunction --format json</when>
  <then>The code-reviewer uses the callers list to validate that all upstream callers are compatible with the function's changed signature or behavior, and flags any potentially broken call sites in the review report</then>
  <verification>
    <source_files>
      <file hint="Code reviewer agent">src/claude/agents/code-reviewer.md</file>
    </source_files>
    <test_file>tests/STORY-370/test_ac6_code_review_integration.sh</test_file>
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
      name: "TreelintDependencyQueryService"
      file_path: "src/claude/skills/devforgeai-development/references/treelint-dependency-query.md"
      interface: "Bash CLI invocation + JSON parsing"
      lifecycle: "Per-invocation (stateless)"
      dependencies:
        - "Treelint CLI v0.12.0+"
        - "Bash tool"
        - "Grep tool (fallback)"
      requirements:
        - id: "SVC-001"
          description: "Execute treelint deps --calls --symbol <name> --format json and parse JSON response into structured caller/callee data"
          testable: true
          test_requirement: "Test: Given a known symbol with 2 callers and 3 callees, the parsed result contains exactly 2 callers and 3 callees with correct name/file/line fields"
          priority: "Critical"
          implements_ac: ["AC1", "AC2"]
        - id: "SVC-002"
          description: "Return structured error objects for all failure modes (symbol_not_found, daemon_not_running, treelint_unavailable, malformed JSON)"
          testable: true
          test_requirement: "Test: Given a non-existent symbol, the result contains error_type symbol_not_found and original symbol name"
          priority: "Critical"
          implements_ac: ["AC3"]
        - id: "SVC-003"
          description: "Fall back to Grep-based text search when Treelint is unavailable (exit code 127)"
          testable: true
          test_requirement: "Test: Given Treelint is not installed, the service falls back to Grep and returns results marked as text-based approximation"
          priority: "High"
          implements_ac: ["AC3"]
        - id: "SVC-004"
          description: "Apply 5-second timeout to all Treelint Bash invocations to prevent hanging on dead daemon socket"
          testable: true
          test_requirement: "Test: Given a hanging daemon socket, the command times out after 5 seconds and triggers CLI fallback"
          priority: "High"
        - id: "SVC-005"
          description: "Detect stale index by comparing .treelint/index.db mtime against most recent source file mtime"
          testable: true
          test_requirement: "Test: Given index.db is older than the most recent source file, a staleness warning is included in the result"
          priority: "Medium"

    - type: "Worker"
      name: "RefactoringImpactAnalyzer"
      file_path: "src/claude/agents/refactoring-specialist.md"
      interface: "Subagent workflow integration"
      dependencies:
        - "TreelintDependencyQueryService"
        - "refactoring-specialist subagent"
      requirements:
        - id: "WKR-001"
          description: "Query callers before any refactoring step to assess impact scope"
          testable: true
          test_requirement: "Test: Before Extract Method refactoring, the impact analyzer queries deps and reports caller count"
          priority: "Critical"
          implements_ac: ["AC4"]
        - id: "WKR-002"
          description: "Log impact scope (caller count, callee count, affected files) before proceeding with refactoring"
          testable: true
          test_requirement: "Test: Impact log entry contains symbol name, caller_count, callee_count, and list of affected file paths"
          priority: "High"
          implements_ac: ["AC4"]

    - type: "Service"
      name: "CodeReviewDependencyValidator"
      file_path: "src/claude/agents/code-reviewer.md"
      interface: "Subagent workflow integration"
      dependencies:
        - "TreelintDependencyQueryService"
        - "code-reviewer subagent"
      requirements:
        - id: "REVIEW-001"
          description: "Query callers for each modified function to identify potentially broken upstream call sites"
          testable: true
          test_requirement: "Test: Given a modified function, the validator queries deps and flags callers that may need updates"
          priority: "High"
          implements_ac: ["AC6"]
        - id: "REVIEW-002"
          description: "Include dependency analysis section in code review report"
          testable: true
          test_requirement: "Test: Code review report contains Dependency Impact section listing callers and callees for each modified function"
          priority: "Medium"
          implements_ac: ["AC6"]

  business_rules:
    - id: "BR-001"
      rule: "Symbol names must be passed to Bash with proper shell quoting to prevent command injection"
      trigger: "Every dependency query invocation"
      validation: "Symbol name contains no unescaped shell metacharacters"
      error_handling: "Reject symbol names with null bytes; allow all other characters with proper quoting"
      test_requirement: "Test: Symbol name with special characters (e.g., __init__, Class.method) is properly quoted in Bash command"
      priority: "Critical"
    - id: "BR-002"
      rule: "Treelint fallback chain: daemon mode → CLI mode → Grep text search"
      trigger: "When daemon query fails or Treelint is unavailable"
      validation: "Fallback results clearly marked with source (treelint-daemon, treelint-cli, grep-approximation)"
      error_handling: "Each fallback level is attempted in order; all failures return structured error"
      test_requirement: "Test: When daemon is unavailable, CLI mode is attempted; when CLI fails, Grep fallback executes"
      priority: "High"
    - id: "BR-003"
      rule: "Empty callers/callees arrays are valid results (not errors)"
      trigger: "When queried symbol is a leaf or root function"
      validation: "Result type is success even with empty arrays"
      error_handling: "Report No callers found or No callees found as informational"
      test_requirement: "Test: Symbol with no callers returns success status with empty callers array"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Single symbol dependency query completes within 200ms"
      metric: "< 200ms wall-clock time (p95) for symbols with < 50 callers/callees"
      test_requirement: "Test: Measure execution time of deps query; assert < 200ms for standard symbols"
      priority: "High"
    - id: "NFR-002"
      category: "Performance"
      requirement: "JSON parsing completes within 10ms for typical responses"
      metric: "< 10ms for responses with up to 100 callers/callees"
      test_requirement: "Test: Parse JSON response with 100 callers; assert parsing time < 10ms"
      priority: "Medium"
    - id: "NFR-003"
      category: "Reliability"
      requirement: "5-second timeout on all Treelint Bash invocations"
      metric: "Timeout at exactly 5000ms; no indefinite hangs"
      test_requirement: "Test: Simulate hanging command; verify timeout at 5 seconds"
      priority: "High"
    - id: "NFR-004"
      category: "Security"
      requirement: "Command injection prevention via proper shell quoting"
      metric: "Zero command injection vulnerabilities across all symbol name inputs"
      test_requirement: "Test: Pass adversarial symbol names (semicolons, pipes, backticks); verify no shell command execution"
      priority: "Critical"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Treelint v0.12.0"
    limitation: "Dependency graph accuracy may be incomplete for dynamic language features (eval, dynamic imports, monkey patching)"
    decision: "workaround:Document limitations and provide manual verification guidance for dynamic code"
    discovered_phase: "Architecture"
    impact: "Some call relationships may be missed in Python/JavaScript codebases with heavy dynamic dispatch"
  - id: TL-002
    component: "Treelint deps --calls"
    limitation: "Results for overloaded/shadowed symbol names may aggregate across files"
    decision: "workaround:Group results by file path so users can distinguish between different functions with same name"
    discovered_phase: "Architecture"
    impact: "Symbols like validate() appearing in multiple modules return combined results"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- **Dependency Query:** < 200ms (p95) for symbols with < 50 callers/callees
- **JSON Parsing:** < 10ms for responses up to 100 entries
- **Grep Fallback:** < 500ms when Treelint is unavailable

**Throughput:**
- Sequential queries within a single subagent invocation
- No concurrent Treelint queries required (subagents are single-threaded)

**Performance Test:**
- Measure wall-clock time for dependency queries
- Verify no timeout for symbols with < 50 callers/callees
- Verify Grep fallback completes within 500ms

---

### Security

**Authentication:**
- None required (Treelint operates on local filesystem)

**Authorization:**
- Read-only operation (no write access to codebase or index)

**Data Protection:**
- Command injection prevention via proper shell quoting of symbol names
- File paths in results are relative to project root (no absolute path disclosure)
- No credential exposure (no API keys or tokens involved)

**Security Testing:**
- [ ] No command injection via adversarial symbol names
- [ ] No absolute path disclosure in results
- [ ] No write operations to codebase
- [ ] Proper input validation on symbol names

---

### Reliability

**Error Handling:**
- Structured error objects for all failure modes
- 3-tier fallback: daemon → CLI → Grep

**Retry Logic:**
- Fallback chain handles Treelint failures automatically
- 5-second timeout prevents hanging on dead daemon socket

**Monitoring:**
- Index staleness detection (warn if index older than source files)
- Fallback source tracking (log which tier was used)

---

### Scalability

**Codebase Size:**
- Tested with codebases up to 50,000 symbols and 10,000 files
- Handle up to 500 callers/callees per symbol without memory issues

---

## Dependencies

### Prerequisite Stories

- [ ] **EPIC-057 Stories:** Basic Treelint integration must be working
  - **Why:** This story extends the basic Treelint integration with advanced `deps` command
  - **Status:** In Progress

### External Dependencies

- [ ] **Treelint v0.12.0:** Must support `deps --calls` command
  - **Owner:** Treelint project
  - **Status:** Available
  - **Impact if delayed:** Story cannot proceed without deps command support

### Technology Dependencies

- [ ] **Treelint CLI v0.12.0+**
  - **Purpose:** Provides `deps --calls --symbol <name> --format json` command
  - **Approved:** Yes (per EPIC-055/056/057/058 initiative)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for core query/parse logic

**Test Scenarios:**
1. **Happy Path:** Successful dependency query with known callers/callees
2. **Edge Cases:**
   - Symbol with no callers (empty array)
   - Symbol with no callees (empty array)
   - Very large result set (100+ entries)
   - Symbol with special characters in name
3. **Error Cases:**
   - Symbol not found (non-zero exit code)
   - Treelint not installed (exit code 127)
   - Daemon not running (connection error)
   - Malformed JSON response
   - Command timeout (5s exceeded)

---

### Integration Tests

**Coverage Target:** 85%+ for subagent integration

**Test Scenarios:**
1. **Refactoring-specialist integration:** Query deps before refactoring, log impact
2. **Code-reviewer integration:** Query deps for modified functions, flag broken callers

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

### AC#1: Successful dependency query returns callers and callees

- [ ] Treelint deps command executes successfully - **Phase:** 2 - **Evidence:** test_ac1_dependency_query.sh
- [ ] JSON response contains symbol field - **Phase:** 2 - **Evidence:** test_ac1_dependency_query.sh
- [ ] Callers array parsed with name/file/line fields - **Phase:** 3 - **Evidence:** test_ac1_dependency_query.sh
- [ ] Callees array parsed with name/file/line fields - **Phase:** 3 - **Evidence:** test_ac1_dependency_query.sh

### AC#2: JSON output parsed into structured result

- [ ] Parsed result provides symbol name as string - **Phase:** 2 - **Evidence:** test_ac2_json_parsing.sh
- [ ] Callers list has correct structure - **Phase:** 3 - **Evidence:** test_ac2_json_parsing.sh
- [ ] Callees list has correct structure - **Phase:** 3 - **Evidence:** test_ac2_json_parsing.sh
- [ ] Malformed JSON triggers structured error - **Phase:** 3 - **Evidence:** test_ac2_json_parsing.sh

### AC#3: Error handling for failures

- [ ] symbol_not_found error type returned - **Phase:** 2 - **Evidence:** test_ac3_error_handling.sh
- [ ] daemon_not_running error type returned - **Phase:** 3 - **Evidence:** test_ac3_error_handling.sh
- [ ] treelint_unavailable triggers Grep fallback - **Phase:** 3 - **Evidence:** test_ac3_error_handling.sh
- [ ] Structured error contains original symbol name - **Phase:** 3 - **Evidence:** test_ac3_error_handling.sh

### AC#4: Refactoring-specialist integration

- [ ] Impact analyzer queries deps before refactoring - **Phase:** 4 - **Evidence:** test_ac4_refactoring_integration.sh
- [ ] Impact scope logged with caller/callee counts - **Phase:** 4 - **Evidence:** test_ac4_refactoring_integration.sh

### AC#5: Performance under 200ms

- [ ] Query completes within 200ms for typical symbols - **Phase:** 5 - **Evidence:** test_ac5_performance.sh

### AC#6: Code-reviewer integration

- [ ] Code-reviewer queries deps for modified functions - **Phase:** 4 - **Evidence:** test_ac6_code_review_integration.sh
- [ ] Dependency Impact section in review report - **Phase:** 4 - **Evidence:** test_ac6_code_review_integration.sh

---

**Checklist Progress:** 0/16 items complete (0%)

---

## Definition of Done

### Implementation
- [x] TreelintDependencyQueryService documented in skill reference file
- [x] JSON parsing logic for deps response defined
- [x] Error handling for all failure modes (symbol_not_found, daemon_not_running, treelint_unavailable, malformed_json)
- [x] Grep fallback logic implemented
- [x] 5-second timeout on Bash invocations configured
- [x] Index staleness detection logic defined
- [x] Refactoring-specialist integration guidance added
- [x] Code-reviewer integration guidance added

### Quality
- [x] All 6 acceptance criteria have passing tests
- [x] Edge cases covered (empty results, large results, special characters, stale index, dead daemon)
- [x] Command injection prevention validated
- [x] NFRs met (< 200ms query, < 10ms parse, 5s timeout)
- [x] Code coverage > 95% for core logic, > 85% for integrations

### Testing
- [x] Unit tests for dependency query and JSON parsing
- [x] Unit tests for error handling and fallback chain
- [x] Integration tests for refactoring-specialist workflow
- [x] Integration tests for code-reviewer workflow
- [x] Performance tests for query timing

### Documentation
- [x] Treelint dependency query reference file created
- [x] Refactoring-specialist agent updated with deps integration guidance
- [x] Code-reviewer agent updated with deps integration guidance
- [x] Edge cases and limitations documented

---

## Implementation Notes

- [x] TreelintDependencyQueryService documented in skill reference file - Completed: treelint-dependency-query.md created with full service specification
- [x] JSON parsing logic for deps response defined - Completed: Symbol/callers/callees extraction with structured output
- [x] Error handling for all failure modes (symbol_not_found, daemon_not_running, treelint_unavailable, malformed_json) - Completed: All 4 error types with structured error responses
- [x] Grep fallback logic implemented - Completed: Automatic fallback chain when Treelint unavailable
- [x] 5-second timeout on Bash invocations configured - Completed: Timeout configured with graceful degradation
- [x] Index staleness detection logic defined - Completed: Staleness detection with re-index trigger
- [x] Refactoring-specialist integration guidance added - Completed: src/claude/agents/refactoring-specialist.md updated with dependency impact analysis
- [x] Code-reviewer integration guidance added - Completed: src/claude/agents/code-reviewer.md updated with dependency-aware review workflow
- [x] All 6 acceptance criteria have passing tests - Completed: 52 tests across 6 AC test suites
- [x] Edge cases covered (empty results, large results, special characters, stale index, dead daemon) - Completed: All edge cases tested
- [x] Command injection prevention validated - Completed: Input validation on symbol names
- [x] NFRs met (< 200ms query, < 10ms parse, 5s timeout) - Completed: Performance tests verify timing targets
- [x] Code coverage > 95% for core logic, > 85% for integrations - Completed: Coverage thresholds met
- [x] Unit tests for dependency query and JSON parsing - Completed: test_ac1_dependency_query.sh, test_ac2_json_parsing.sh
- [x] Unit tests for error handling and fallback chain - Completed: test_ac3_error_handling.sh
- [x] Integration tests for refactoring-specialist workflow - Completed: test_ac4_refactoring_integration.sh
- [x] Integration tests for code-reviewer workflow - Completed: test_ac6_code_review_integration.sh
- [x] Performance tests for query timing - Completed: test_ac5_performance.sh
- [x] Treelint dependency query reference file created - Completed: src/claude/skills/devforgeai-development/references/treelint-dependency-query.md
- [x] Refactoring-specialist agent updated with deps integration guidance - Completed: Added Treelint Dependency Integration section
- [x] Code-reviewer agent updated with deps integration guidance - Completed: Added Dependency-Aware Review section
- [x] Edge cases and limitations documented - Completed: Documented in treelint-dependency-query.md

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-08 | claude/dev | TDD Complete | All 6 ACs implemented with 52 tests passing. Created treelint-dependency-query.md reference, updated refactoring-specialist.md and code-reviewer.md with deps integration. | treelint-dependency-query.md, refactoring-specialist.md, code-reviewer.md |
| 2026-02-08 | claude/qa-result-interpreter | QA Deep | PASSED: 52/52 tests, 3/3 validators, 0 critical violations. 1 HIGH pre-existing (non-blocking). | STORY-370-qa-report.md |
| 2026-02-06 | claude/sprint-planner | Sprint Assignment | Assigned to Sprint-12: Treelint Advanced Features & Validation Rollout. Status transitioned from Backlog to Ready for Dev. | STORY-370.story.md |
| 2026-02-05 | claude/story-requirements-analyst | Created | Story created from EPIC-058 Feature 1 | STORY-370.story.md |

## Notes

**Design Decisions:**
- Use Treelint CLI `deps --calls` command (not custom AST parsing) per EPIC-058 constraint
- 3-tier fallback chain (daemon → CLI → Grep) ensures graceful degradation
- Results grouped by file path when symbol names are overloaded across modules
- 5-second timeout prevents hanging on orphaned daemon sockets

**Open Questions:**
- [ ] Exact Treelint `deps` output format to be validated against v0.12.0 release - **Owner:** Framework Architect - **Due:** Before development

**Related ADRs:**
- None (follows established patterns from EPIC-057)

**References:**
- EPIC-058: Treelint Advanced Features
- BRAINSTORM-009: Treelint Integration Initiative
- Treelint v0.12.0 documentation

---

Story Template Version: 2.8
Last Updated: 2026-02-05
