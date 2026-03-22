---
id: STORY-361
title: Create Treelint Skill Reference Files for Subagent Integration
type: documentation
epic: EPIC-057
sprint: Sprint-9
status: QA Approved
points: 5
depends_on: []
priority: Medium
advisory: false
source_gap: null
source_story: null
assigned_to: Unassigned
created: 2026-02-04
format_version: "2.8"
---

# Story: Create Treelint Skill Reference Files for Subagent Integration

## Description

**As a** DevForgeAI subagent developer,
**I want** Treelint usage patterns documented in shared reference files with command syntax, JSON parsing examples, fallback logic, language support matrix, and error handling,
**so that** all 7 target subagents (test-automator, backend-architect, code-reviewer, security-auditor, refactoring-specialist, coverage-analyzer, anti-pattern-scanner) can adopt consistent, well-documented Treelint search patterns without each subagent independently discovering how to use the tool.

## Provenance

```xml
<provenance>
  <origin document="EPIC-057" section="Features">
    <quote>"Feature 1: Skill Reference Files for Treelint Patterns - Create reference documentation with Treelint usage patterns for subagents"</quote>
    <line_reference>lines 39-42</line_reference>
    <quantified_impact>Consistent patterns for all 7 subagents, enabling 40-80% token reduction in code search operations</quantified_impact>
  </origin>

  <decision rationale="shared-reference-over-per-subagent-docs">
    <selected>Single shared reference file(s) loadable by all subagents via Read()</selected>
    <rejected alternative="per-subagent-inline-docs">
      Would duplicate content across 7 subagent files, violating DRY and increasing maintenance burden
    </rejected>
    <trade_off>Subagents must make an extra Read() call to load reference, but saves 7x documentation duplication</trade_off>
  </decision>

  <stakeholder role="Framework Architect" goal="token-efficiency">
    <quote>"Enable 7 high-impact DevForgeAI subagents to use Treelint for semantic code search, achieving 40-80% token reduction"</quote>
    <source>EPIC-057, Business Goal</source>
  </stakeholder>
</provenance>
```

## Acceptance Criteria

### AC#1: Treelint Search Command Pattern Reference File Created

```xml
<acceptance_criteria id="AC1" implements="DOC-001,DOC-002">
  <given>ADR-013 is approved and Treelint v0.12.0+ is listed in tech-stack.md as an approved AST-aware code search tool</given>
  <when>The reference documentation is created</when>
  <then>A shared reference file exists at a location discoverable by subagents via Read() that documents all Treelint search command patterns including: treelint search --type function, treelint search --type class, treelint map --ranked, and treelint deps --calls, each with description, expected arguments, and a complete Bash(command="treelint ...") invocation example</then>
  <verification>
    <source_files>
      <file hint="Shared Treelint reference file">src/claude/agents/references/treelint-search-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-361/test_ac1_command_patterns.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: JSON Output Parsing Examples Documented for AI Consumption

```xml
<acceptance_criteria id="AC2" implements="DOC-003">
  <given>Treelint returns JSON output when invoked with --format json</given>
  <when>A subagent reads the reference documentation</when>
  <then>The documentation includes at minimum 3 complete JSON parsing examples showing: a function search result (type, name, file, lines, signature, body fields), a class search result with member enumeration, and a treelint map --ranked result showing file importance ranking, each with raw JSON output and narrative explaining how to extract relevant information</then>
  <verification>
    <source_files>
      <file hint="Shared Treelint reference file">src/claude/agents/references/treelint-search-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-361/test_ac2_json_examples.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Fallback Logic Documentation (Treelint to Grep)

```xml
<acceptance_criteria id="AC3" implements="DOC-004">
  <given>Treelint supports only Python (.py), TypeScript (.ts, .tsx), JavaScript (.js, .jsx), Rust (.rs), and Markdown (.md) file types</given>
  <when>A subagent encounters an unsupported file type or Treelint is unavailable</when>
  <then>The reference documentation includes a decision tree specifying: Step 1 check file extension against supported list, Step 2 attempt Treelint if supported, Step 3 fall back to Grep if unsupported or command fails, Step 4 log warning on fallback (not error), with specific Grep pattern equivalents for each Treelint search type</then>
  <verification>
    <source_files>
      <file hint="Shared Treelint reference file">src/claude/agents/references/treelint-search-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-361/test_ac3_fallback_logic.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Language Support Matrix with File Extension Mapping

```xml
<acceptance_criteria id="AC4" implements="DOC-005">
  <given>Treelint v0.12.0+ supports 5 languages via tree-sitter parsers</given>
  <when>A subagent needs to determine whether Treelint can handle a given file</when>
  <then>The reference documentation includes a language support matrix table with columns Language, File Extensions, Treelint Support Status, Fallback Strategy, and Notes covering 9+ entries: Python (.py), TypeScript (.ts/.tsx), JavaScript (.js/.jsx), Rust (.rs), Markdown (.md) as supported, and C# (.cs), Java (.java), Go (.go), Other (*) as unsupported with Grep fallback</then>
  <verification>
    <source_files>
      <file hint="Shared Treelint reference file">src/claude/agents/references/treelint-search-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-361/test_ac4_language_matrix.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Error Handling Patterns for Treelint Unavailability and Failures

```xml
<acceptance_criteria id="AC5" implements="DOC-006">
  <given>Treelint may not be installed, may be an unsupported version, or may fail during execution</given>
  <when>A subagent encounters a Treelint error</when>
  <then>The reference documentation includes error handling patterns for at minimum 4 failure scenarios: binary not found (exit code 127), version too old (missing --format json), empty results (valid query, no matches), and malformed JSON (parse error), each with detection method, example error output, recommended response, and whether to fall back to Grep or report error</then>
  <verification>
    <source_files>
      <file hint="Shared Treelint reference file">src/claude/agents/references/treelint-search-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-361/test_ac5_error_handling.sh</test_file>
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
      name: "treelint-search-patterns.md"
      file_path: "src/claude/agents/references/treelint-search-patterns.md"
      required_keys:
        - key: "Search Command Patterns section"
          type: "markdown"
          required: true
          test_requirement: "Test: File contains ## Search Command Patterns heading with 4 command pattern subsections"
        - key: "JSON Output Parsing section"
          type: "markdown"
          required: true
          test_requirement: "Test: File contains ## JSON Output Parsing heading with 3+ JSON code block examples"
        - key: "Fallback Decision Tree section"
          type: "markdown"
          required: true
          test_requirement: "Test: File contains ## Fallback Decision Tree heading with step-by-step fallback logic"
        - key: "Language Support Matrix section"
          type: "markdown"
          required: true
          test_requirement: "Test: File contains language support table with 9+ rows"
        - key: "Error Handling Patterns section"
          type: "markdown"
          required: true
          test_requirement: "Test: File contains ## Error Handling heading with 4+ failure scenario subsections"

  business_rules:
    - id: "BR-001"
      rule: "All Treelint command examples must use --format json flag for machine-parseable output"
      trigger: "When documenting Treelint command patterns"
      validation: "Grep for 'treelint' commands without '--format json' should return 0 matches"
      error_handling: "Add --format json to any command missing it"
      test_requirement: "Test: All treelint command invocations in reference file include --format json flag"
      priority: "Critical"

    - id: "BR-002"
      rule: "Every documented Treelint search type must have a corresponding Grep fallback pattern"
      trigger: "When documenting search patterns"
      validation: "Count Treelint patterns equals count of Grep fallback patterns"
      error_handling: "Add missing Grep fallback for any undocumented pattern"
      test_requirement: "Test: For each treelint search pattern, a corresponding Grep fallback exists in Fallback section"
      priority: "Critical"

    - id: "BR-003"
      rule: "Reference file must not exceed 400 lines per tech-stack.md token budget"
      trigger: "When file is created or updated"
      validation: "Line count check: wc -l < 400"
      error_handling: "Split into multiple reference files per ADR-012 progressive disclosure"
      test_requirement: "Test: wc -l on reference file returns value < 400"
      priority: "High"

    - id: "BR-004"
      rule: "All version references must specify v0.12.0+ as minimum Treelint version"
      trigger: "When referencing Treelint version"
      validation: "All version strings match v0.12.0 or higher"
      error_handling: "Update version reference to v0.12.0+"
      test_requirement: "Test: Reference file contains 'v0.12.0' as minimum version, no references to lower versions"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Reference file load time via Read() tool"
      metric: "< 500ms per file read (standard file I/O)"
      test_requirement: "Test: Read(file_path=reference_file) completes within normal file I/O time"
      priority: "Medium"

    - id: "NFR-002"
      category: "Performance"
      requirement: "Reference file size within token budget"
      metric: "< 400 lines (~16,000 characters) per file"
      test_requirement: "Test: File line count < 400 and character count < 16,000"
      priority: "High"

    - id: "NFR-003"
      category: "Reliability"
      requirement: "100% fallback coverage for all documented search types"
      metric: "Every Treelint command has a Grep equivalent documented"
      test_requirement: "Test: Count of Treelint patterns == count of Grep fallback patterns in document"
      priority: "Critical"

    - id: "NFR-004"
      category: "Reliability"
      requirement: "All error scenarios have defined recovery paths"
      metric: "4+ error scenarios documented with detection + recovery for each"
      test_requirement: "Test: Error handling section contains 4+ subsections each with 'Detection' and 'Recovery' labels"
      priority: "High"

    - id: "NFR-005"
      category: "Scalability"
      requirement: "Extensible language matrix format"
      metric: "Table format allows adding rows without restructuring document"
      test_requirement: "Test: Language matrix uses standard markdown table format with consistent columns"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Treelint v0.12.0"
    limitation: "Supports only 5 languages (Python, TypeScript, JavaScript, Rust, Markdown) - C#, Java, Go, and others not supported"
    decision: "workaround:Grep fallback documented for unsupported languages"
    discovered_phase: "Architecture"
    impact: "Subagents working with C#, Java, or Go projects must always use Grep patterns instead of Treelint"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Reference File Size:**
- Each reference file: < 400 lines (~16,000 characters)
- Total documentation: < 800 lines across all files (if split)
- No runtime performance impact (read-only reference material)

---

### Security

**Content Safety:**
- Zero secrets, credentials, API keys, or tokens in reference files
- All examples use placeholder values (e.g., `"validate*"` not actual function names)
- Input sanitization guidance: Document that subagents must quote/escape user-provided search terms in Treelint commands

---

### Scalability

**Extensibility:**
- Language matrix table format allows adding new language rows
- New Treelint commands can be appended as new sections
- Documentation is subagent-agnostic (usable by all 7 targets + future subagents)
- Progressive disclosure compatible per ADR-012

---

### Reliability

**Documentation Integrity:**
- Valid Markdown with no broken links or missing sections
- Version pinning: All examples specify v0.12.0+ requirement
- 100% fallback coverage for all documented search types
- All error scenarios have defined recovery paths

---

## Dependencies

### Prerequisite Stories

- [ ] **EPIC-055 (Foundation):** ADR-013 approved, tech-stack.md updated with Treelint
  - **Why:** Reference files cite ADR-013 and tech-stack.md as authoritative sources
  - **Status:** In Progress

- [ ] **EPIC-056 (Context Files):** source-tree.md and anti-patterns.md updated
  - **Why:** Reference file placement must comply with source-tree.md
  - **Status:** In Progress

### External Dependencies

- [ ] **Treelint v0.12.0+ binary:** Must be available for validation of documented command patterns
  - **Owner:** EPIC-055
  - **ETA:** Before sprint start
  - **Status:** In Progress
  - **Impact if delayed:** Documentation can be written but command examples cannot be validated

### Technology Dependencies

- [ ] **Treelint** v0.12.0+
  - **Purpose:** AST-aware code search tool documented by this story
  - **Approved:** Yes (ADR-013)
  - **Added to dependencies.md:** Yes (EPIC-055)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for documentation structure validation

**Test Scenarios:**
1. **Happy Path:** Reference file exists, contains all required sections, all patterns documented
2. **Edge Cases:**
   - File exceeds 400 lines (should fail validation)
   - Missing fallback pattern for a search type (should fail validation)
   - Treelint command without --format json (should fail validation)
3. **Error Cases:**
   - Reference file not found at expected path
   - Malformed markdown (broken table, unclosed code blocks)
   - Version reference below v0.12.0

### Integration Tests

**Coverage Target:** 85%+ for subagent reference loading

**Test Scenarios:**
1. **Subagent Read Test:** Verify Read(file_path="...") returns valid markdown content
2. **Pattern Completeness:** Verify all 4 search types have both Treelint and Grep examples

---

## Acceptance Criteria Verification Checklist

### AC#1: Treelint Search Command Pattern Reference File Created

- [ ] Reference file created at documented path - **Phase:** 2 - **Evidence:** src/claude/agents/references/treelint-search-patterns.md
- [ ] Contains `treelint search --type function` pattern - **Phase:** 2 - **Evidence:** Grep match in reference file
- [ ] Contains `treelint search --type class` pattern - **Phase:** 2 - **Evidence:** Grep match in reference file
- [ ] Contains `treelint map --ranked` pattern - **Phase:** 2 - **Evidence:** Grep match in reference file
- [ ] Contains `treelint deps --calls` pattern - **Phase:** 2 - **Evidence:** Grep match in reference file
- [ ] Each pattern has Bash() invocation example - **Phase:** 2 - **Evidence:** Grep for Bash(command= in reference file

### AC#2: JSON Output Parsing Examples Documented

- [ ] Function search JSON example present - **Phase:** 2 - **Evidence:** JSON code block with "type": "function"
- [ ] Class search JSON example present - **Phase:** 2 - **Evidence:** JSON code block with "type": "class"
- [ ] Map ranked JSON example present - **Phase:** 2 - **Evidence:** JSON code block with ranked results
- [ ] Each example has parsing narrative - **Phase:** 2 - **Evidence:** Explanatory text after each JSON block

### AC#3: Fallback Logic Documentation

- [ ] Decision tree with 4 steps documented - **Phase:** 2 - **Evidence:** Numbered steps in Fallback section
- [ ] Grep equivalents for function search - **Phase:** 2 - **Evidence:** Grep pattern for function search
- [ ] Grep equivalents for class search - **Phase:** 2 - **Evidence:** Grep pattern for class search
- [ ] Warning (not error) on fallback specified - **Phase:** 2 - **Evidence:** "warning" keyword in fallback documentation

### AC#4: Language Support Matrix

- [ ] Table with 5 required columns - **Phase:** 2 - **Evidence:** Markdown table header row
- [ ] 5 supported languages listed - **Phase:** 2 - **Evidence:** Python, TypeScript, JavaScript, Rust, Markdown rows
- [ ] 4+ unsupported languages listed - **Phase:** 2 - **Evidence:** C#, Java, Go, Other rows

### AC#5: Error Handling Patterns

- [ ] Binary not found scenario - **Phase:** 2 - **Evidence:** Error handling subsection
- [ ] Version too old scenario - **Phase:** 2 - **Evidence:** Error handling subsection
- [ ] Empty results scenario - **Phase:** 2 - **Evidence:** Error handling subsection
- [ ] Malformed JSON scenario - **Phase:** 2 - **Evidence:** Error handling subsection
- [ ] Each scenario has detection + recovery - **Phase:** 2 - **Evidence:** Labeled sections per scenario

---

**Checklist Progress:** 0/24 items complete (0%)

---

## Definition of Done

### Implementation
- [x] Shared Treelint reference file created at `src/claude/agents/references/treelint-search-patterns.md`
- [x] All 4 Treelint search command patterns documented with complete syntax
- [x] At least 3 JSON output parsing examples included
- [x] Fallback decision tree documented with Grep equivalents for each search type
- [x] Language support matrix table with 9+ entries created
- [x] Error handling patterns for 4+ failure scenarios documented
- [x] File size < 400 lines per tech-stack.md token budget

### Quality
- [x] All 5 acceptance criteria have passing tests
- [x] Every Treelint pattern has corresponding Grep fallback (BR-002)
- [x] All command examples include --format json flag (BR-001)
- [x] Version references specify v0.12.0+ minimum (BR-004)
- [x] No vague terms (all metrics measurable)

### Testing
- [x] Structural tests validate all required sections exist
- [x] Pattern tests validate command syntax and JSON examples
- [x] Line count validation confirms < 400 lines
- [x] Integration test confirms subagent Read() loads successfully

### Documentation
- [x] Reference file follows ADR-012 progressive disclosure pattern
- [x] Reference file cites ADR-013 for Treelint approval
- [x] Reference file cites tech-stack.md for language support (lines 139-147)

---

## Implementation Notes

- [x] Shared Treelint reference file created at `src/claude/agents/references/treelint-search-patterns.md` - Completed: File created, 276 lines
- [x] All 4 Treelint search command patterns documented with complete syntax - Completed: function, class, map --ranked, deps --calls
- [x] At least 3 JSON output parsing examples included - Completed: 3 examples with parsing guidance
- [x] Fallback decision tree documented with Grep equivalents for each search type - Completed: 4-step tree with 4 Grep patterns
- [x] Language support matrix table with 9+ entries created - Completed: 9 entries (5 supported + 4 unsupported)
- [x] Error handling patterns for 4+ failure scenarios documented - Completed: binary not found, version old, empty results, malformed JSON
- [x] File size < 400 lines per tech-stack.md token budget - Completed: 276 lines (69% of budget)
- [x] All 5 acceptance criteria have passing tests - Completed: tests/STORY-361/*.sh
- [x] Every Treelint pattern has corresponding Grep fallback (BR-002) - Completed: 4/4 patterns
- [x] All command examples include --format json flag (BR-001) - Completed: All commands validated
- [x] Version references specify v0.12.0+ minimum (BR-004) - Completed: 3 references
- [x] No vague terms (all metrics measurable) - Completed: All metrics explicit
- [x] Structural tests validate all required sections exist - Completed: 5 AC tests
- [x] Pattern tests validate command syntax and JSON examples - Completed: 47 assertions
- [x] Line count validation confirms < 400 lines - Completed: 276 < 400
- [x] Integration test confirms subagent Read() loads successfully - Completed: 24/24 tests
- [x] Reference file follows ADR-012 progressive disclosure pattern - Completed: Placed in references/ subdirectory
- [x] Reference file cites ADR-013 for Treelint approval - Completed: Referenced in document
- [x] Reference file cites tech-stack.md for language support (lines 139-147) - Completed: Referenced in document

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-04 15:00 | claude/story-requirements-analyst | Created | Story created from EPIC-057 Feature 1 (Batch mode) | STORY-361-create-treelint-skill-reference-files.story.md |
| 2026-02-05 | claude/sprint-planner | Sprint Planning | Assigned to Sprint-9, status → Ready for Dev | STORY-361-create-treelint-skill-reference-files.story.md |
| 2026-02-06 | claude/qa-result-interpreter | QA Deep | PASS WITH WARNINGS: 63/63 tests passed, 1 HIGH (design decision) | STORY-361-qa-report.md |
| 2026-02-06 | claude/qa-result-interpreter | QA Remediation | Status → In Development: 7 gaps identified (1 HIGH, 4 MEDIUM, 2 LOW), gaps.json created | STORY-361-gaps.json |
| 2026-02-06 | claude/dev-workflow | Remediation Complete | Fixed all 7 gaps: YAML frontmatter added, Grep syntax fixed (3), status marker fixed, citations updated, source-tree.md updated for shared references | treelint-search-patterns.md, source-tree.md |
| 2026-02-06 | claude/qa-result-interpreter | QA Deep (Post-Remediation) | PASSED: All 7 gaps verified fixed, 0 violations, 63/63 tests passed, quality score 92/100 | STORY-361-qa-report.md |

## Notes

**Design Decisions:**
- Shared reference file approach chosen over per-subagent inline documentation to avoid 7x duplication
- Reference file placed in `src/claude/agents/references/` per ADR-012 progressive disclosure pattern for subagents
- File extension-based language detection chosen for simplicity and reliability

**Open Questions:**
- [ ] Exact file path for shared reference: `src/claude/agents/references/treelint-search-patterns.md` or alternative? - **Owner:** Framework Architect - **Due:** Before dev start

**Related ADRs:**
- ADR-013: Treelint Integration for AST-Aware Code Search
- ADR-012: Progressive Disclosure Pattern for Subagents
- ADR-007: Remove ast-grep and Evaluate Tree-sitter

**References:**
- EPIC-057: Treelint Subagent Integration
- tech-stack.md: Treelint section (lines 98-166)
- source-tree.md: Subagent reference directories (lines 588-621)

---

Story Template Version: 2.8
Last Updated: 2026-02-04
