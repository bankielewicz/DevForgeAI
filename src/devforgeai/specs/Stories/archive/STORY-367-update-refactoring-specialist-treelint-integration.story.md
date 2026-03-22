---
id: STORY-367
title: Update refactoring-specialist Subagent with Treelint AST-Aware Structure Analysis
type: feature
epic: EPIC-057
sprint: Sprint-10
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

# Story: Update refactoring-specialist Subagent with Treelint AST-Aware Structure Analysis

## Description

**As a** refactoring-specialist subagent (the DevForgeAI code refactoring expert responsible for applying systematic improvement patterns -- Extract Method, Extract Class, Rename, Introduce Parameter Object -- while preserving tests during TDD Phase 3 Refactor),
**I want** to use Treelint's AST-aware search (`treelint search --type function --format json` and `treelint search --type class --format json`) for semantic code structure analysis before proposing refactorings, with JSON parsing of structured results and automatic fallback to Grep for unsupported languages,
**so that** I can understand actual code structure (class sizes, method counts, function complexity boundaries) by AST node type rather than text patterns (reducing false positives from comments, strings, and documentation references), achieve 40-80% token reduction in code search operations during refactoring analysis, and maintain seamless functionality across all project languages through hybrid fallback logic.

## Provenance

```xml
<provenance>
  <origin document="EPIC-057" section="Feature 6: refactoring-specialist Subagent Update">
    <quote>"Enable structure-aware refactoring with dependency awareness"</quote>
    <line_reference>lines 64-67</line_reference>
    <quantified_impact>40-80% token reduction in refactoring-focused code search operations; >50% false positive reduction vs Grep-only</quantified_impact>
  </origin>

  <decision rationale="direct-cli-integration-over-wrapper">
    <selected>Each subagent uses Treelint directly via Bash tool with reference file patterns</selected>
    <rejected alternative="wrapper-subagent">
      Architecture constraint: subagents cannot delegate to other subagents
      (Source: devforgeai/specs/context/architecture-constraints.md, lines 25-26)
    </rejected>
    <trade_off>Treelint patterns duplicated across 7 subagents vs. shared reference file approach mitigates duplication</trade_off>
  </decision>

  <decision rationale="mandatory-progressive-disclosure">
    <selected>ALL Treelint patterns extracted to references/treelint-refactoring-patterns.md</selected>
    <rejected alternative="inline-in-core-file">
      Current refactoring-specialist.md is 595 lines, already exceeding the 500-line target
      (Source: devforgeai/specs/context/tech-stack.md, lines 385-388)
    </rejected>
    <trade_off>Additional Read() call at runtime vs. token budget compliance</trade_off>
  </decision>
</provenance>
```

## Acceptance Criteria

### AC#1: Treelint Integration for Code Structure Analysis

```xml
<acceptance_criteria id="AC1" implements="TREELINT-REFACTOR-001">
  <given>The refactoring-specialist subagent (src/claude/agents/refactoring-specialist.md) is invoked during TDD Phase 3 (Refactor) or by devforgeai-qa when complexity violations are detected, and needs to analyze code structure in a project containing Python (.py), TypeScript (.ts/.tsx), or JavaScript (.js/.jsx) files to identify refactoring candidates</given>
  <when>The subagent performs code structure analysis to discover classes (for Extract Class / God Object detection) and functions (for Extract Method / Long Method detection) before proposing refactorings</when>
  <then>The subagent uses Treelint via Bash(command="treelint search --type class --format json") and Bash(command="treelint search --type function --format json") instead of text-based Grep patterns, parses the JSON response to extract symbol name, file path, line range [start, end], and signature, and uses the structured results to make informed refactoring decisions (e.g., class line count from line range, method count per class, function signature complexity)</then>
  <verification>
    <source_files>
      <file hint="Updated refactoring-specialist subagent definition">src/claude/agents/refactoring-specialist.md</file>
      <file hint="Treelint refactoring patterns reference file">src/claude/agents/refactoring-specialist/references/treelint-refactoring-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-367/test_ac1_treelint_structure_analysis.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: JSON Parsing of Treelint Search Results

```xml
<acceptance_criteria id="AC2" implements="TREELINT-REFACTOR-JSON-001">
  <given>Treelint returns a JSON response containing a results array where each entry has fields: type, name, file, lines (array of [start, end]), signature, and body</given>
  <when>The refactoring-specialist subagent receives Treelint search output for class or function discovery during refactoring analysis</when>
  <then>The subagent parses the JSON to extract: (1) class/function names for identifying refactoring targets, (2) file paths for locating source code, (3) line ranges [start, end] for calculating method/class length (end - start) to detect Long Method (>50 lines) and God Object (>500 lines) code smells, and (4) signatures for understanding parameter counts (detecting Long Parameter List smell when >4 parameters), and the parsed data is used to prioritize refactoring candidates by severity</then>
  <verification>
    <source_files>
      <file hint="Updated refactoring-specialist subagent definition">src/claude/agents/refactoring-specialist.md</file>
      <file hint="Treelint refactoring patterns reference file">src/claude/agents/refactoring-specialist/references/treelint-refactoring-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-367/test_ac2_json_parsing.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Grep Fallback for Unsupported Languages

```xml
<acceptance_criteria id="AC3" implements="TREELINT-REFACTOR-FALLBACK-001">
  <given>The refactoring-specialist subagent needs to analyze code structure in file types not supported by Treelint (e.g., C# .cs, Java .java, Go .go) or when the Treelint binary is unavailable (exit code 127) or fails at runtime</given>
  <when>The subagent detects an unsupported file extension or receives a non-zero exit code from Treelint</when>
  <then>The subagent falls back to using the native Grep tool (e.g., Grep(pattern="class |function |def ", glob="**/*.cs")) following the fallback decision tree documented in the STORY-361 reference file, emits a warning-level message noting reduced analysis precision, and completes the code structure analysis without halting the workflow</then>
  <verification>
    <source_files>
      <file hint="Updated refactoring-specialist subagent definition">src/claude/agents/refactoring-specialist.md</file>
      <file hint="Treelint refactoring patterns reference file">src/claude/agents/refactoring-specialist/references/treelint-refactoring-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-367/test_ac3_grep_fallback.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Refactoring-Specific Treelint Patterns (Code Smell Detection)

```xml
<acceptance_criteria id="AC4" implements="TREELINT-REFACTOR-PATTERNS-001">
  <given>The refactoring-specialist subagent needs predefined Treelint search patterns mapped to specific code smells from the Fowler refactoring catalog (Long Method, Large Class/God Object, Duplicate Code, Long Parameter List, Complex Conditional)</given>
  <when>The subagent is updated with Treelint integration instructions</when>
  <then>The subagent documentation (in reference file) includes Treelint search patterns for at least 4 refactoring scenarios: (1) God Object detection via treelint search --type class --format json followed by line range analysis (classes >500 lines), (2) Long Method detection via treelint search --type function --format json followed by line range analysis (functions >50 lines), (3) Extract Class candidates via treelint map --ranked --format json to identify files with highest symbol density, and (4) Long Parameter List detection via function signature analysis from Treelint results (>4 parameters), each with specific Treelint command examples and refactoring action recommendations</then>
  <verification>
    <source_files>
      <file hint="Updated refactoring-specialist subagent definition">src/claude/agents/refactoring-specialist.md</file>
      <file hint="Treelint refactoring patterns reference file">src/claude/agents/refactoring-specialist/references/treelint-refactoring-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-367/test_ac4_refactoring_patterns.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Progressive Disclosure Compliance (500-Line Limit with Mandatory Extraction)

```xml
<acceptance_criteria id="AC5" implements="TREELINT-REFACTOR-SIZE-001">
  <given>The refactoring-specialist subagent definition file (src/claude/agents/refactoring-specialist.md) is currently 595 lines, already exceeding the 500-line maximum per source-tree.md and tech-stack.md token budget constraints (target: 100-300 lines, maximum: 500 lines per tech-stack.md lines 385-388)</given>
  <when>Treelint integration instructions are added to the refactoring-specialist subagent</when>
  <then>The updated refactoring-specialist.md core file is reduced to 500 lines or fewer by extracting content (Treelint patterns and/or existing refactoring catalog examples) to reference files under src/claude/agents/refactoring-specialist/references/, with the core file containing Read() instructions to load reference files on demand following ADR-012 progressive disclosure pattern</then>
  <verification>
    <source_files>
      <file hint="Updated refactoring-specialist subagent definition">src/claude/agents/refactoring-specialist.md</file>
      <file hint="Treelint refactoring patterns reference file">src/claude/agents/refactoring-specialist/references/treelint-refactoring-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-367/test_ac5_line_count.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Ranked File Map for Refactoring Prioritization

```xml
<acceptance_criteria id="AC6" implements="TREELINT-REFACTOR-MAP-001">
  <given>The refactoring-specialist subagent needs to prioritize which files to refactor first based on structural complexity (number of classes, functions, and overall symbol density)</given>
  <when>The subagent begins Step 1 (Detect Code Smells) of its workflow to identify the highest-priority refactoring targets</when>
  <then>The subagent uses Treelint via Bash(command="treelint map --ranked --format json") to generate a ranked file importance map, parses the JSON response to identify files with highest symbol counts, largest classes, and most complex function signatures, and uses this ranking to prioritize refactoring efforts on the most impactful files first</then>
  <verification>
    <source_files>
      <file hint="Updated refactoring-specialist subagent definition">src/claude/agents/refactoring-specialist.md</file>
      <file hint="Treelint refactoring patterns reference file">src/claude/agents/refactoring-specialist/references/treelint-refactoring-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-367/test_ac6_ranked_file_map.sh</test_file>
    <coverage_threshold>80</coverage_threshold>
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
      name: "refactoring-specialist Subagent Definition"
      file_path: "src/claude/agents/refactoring-specialist.md"
      required_keys:
        - key: "Treelint Code Structure Analysis Section"
          type: "markdown"
          example: "### Treelint-Aware Code Structure Analysis"
          required: true
          validation: "Section must contain treelint search --type function --format json and treelint search --type class --format json instructions"
          test_requirement: "Test: Grep for 'treelint search.*--type function.*--format json' and 'treelint search.*--type class.*--format json' in refactoring-specialist.md or its reference files"

        - key: "JSON Parsing Instructions"
          type: "markdown"
          example: "Parse JSON results: type, name, file, lines, signature"
          required: true
          validation: "Must reference all 4 required JSON fields: name, file, lines, signature"
          test_requirement: "Test: Grep for 'name.*file.*lines.*signature' pattern in refactoring-specialist.md or reference files"

        - key: "Language Support Check"
          type: "markdown"
          example: "Check file extension: .py, .ts, .tsx, .js, .jsx, .rs, .md"
          required: true
          validation: "Must list supported extensions from tech-stack.md"
          test_requirement: "Test: Grep for '.py' AND '.ts' AND '.js' in refactoring-specialist.md or reference files"

        - key: "Grep Fallback Section"
          type: "markdown"
          example: "### Fallback: Grep for Unsupported Languages"
          required: true
          validation: "Must reference native Grep tool (not Bash grep)"
          test_requirement: "Test: Grep for 'Grep(pattern=' fallback instruction in refactoring-specialist.md or reference files"

        - key: "Refactoring Pattern Categories"
          type: "markdown"
          example: "### Treelint-Powered Code Smell Detection"
          required: true
          validation: "Must document at least 4 refactoring-specific Treelint patterns"
          test_requirement: "Test: Grep for 'God Object' AND 'Long Method' AND 'Long Parameter' AND 'Extract' in refactoring-specialist.md or reference files"

        - key: "Reference File Loading"
          type: "markdown"
          example: "Read(file_path=\"src/claude/agents/references/treelint-search-patterns.md\")"
          required: true
          validation: "Must contain Read() instruction for STORY-361 reference file"
          test_requirement: "Test: Grep for 'Read.*treelint.*patterns' in refactoring-specialist.md"

        - key: "Ranked Map Integration"
          type: "markdown"
          example: "treelint map --ranked --format json"
          required: true
          validation: "Must contain treelint map command for file prioritization"
          test_requirement: "Test: Grep for 'treelint map.*--ranked.*--format json' in refactoring-specialist.md or reference files"

    - type: "Configuration"
      name: "Treelint Refactoring Patterns Reference File"
      file_path: "src/claude/agents/refactoring-specialist/references/treelint-refactoring-patterns.md"
      required_keys:
        - key: "Progressive Disclosure Extraction"
          type: "markdown"
          example: "Treelint refactoring search patterns extracted per ADR-012"
          required: true
          default: "REQUIRED since refactoring-specialist.md is 595 lines (exceeds 500-line limit)"
          validation: "File must exist AND refactoring-specialist.md must contain Read() pointing to it"
          test_requirement: "Test: File exists at path AND refactoring-specialist.md references it via Read()"

  business_rules:
    - id: "BR-001"
      rule: "Treelint must be attempted first for all supported file extensions before falling back to Grep"
      trigger: "When code structure analysis is initiated for any file type"
      validation: "Check file extension against supported list, use Treelint if supported, Grep if not"
      error_handling: "If Treelint fails (non-zero exit), fall back to Grep with warning"
      test_requirement: "Test: refactoring-specialist.md Treelint section appears before Grep fallback section"
      priority: "Critical"

    - id: "BR-002"
      rule: "Empty Treelint results (exit code 0, zero matches) must NOT trigger Grep fallback"
      trigger: "When Treelint returns valid JSON with empty results array"
      validation: "Distinguish between exit code 0 (success, no matches) and non-zero (failure)"
      error_handling: "Return empty results, do not invoke Grep"
      test_requirement: "Test: refactoring-specialist.md contains distinction between empty results and command failure"
      priority: "Critical"

    - id: "BR-003"
      rule: "All Treelint failures must result in successful Grep fallback with zero workflow interruption"
      trigger: "When Treelint returns non-zero exit code or malformed output"
      validation: "Workflow must never HALT due to Treelint issues"
      error_handling: "Warning-level message, Grep fallback, continue workflow"
      test_requirement: "Test: refactoring-specialist.md fallback section contains 'warning' and no 'HALT' on Treelint failure"
      priority: "Critical"

    - id: "BR-004"
      rule: "Core subagent file must be reduced to 500 lines or fewer; Treelint patterns AND excess existing content extracted to references/"
      trigger: "After Treelint integration content is added"
      validation: "wc -l on refactoring-specialist.md <= 500"
      error_handling: "Extract refactoring catalog examples and Treelint patterns to references/ per ADR-012"
      test_requirement: "Test: wc -l refactoring-specialist.md <= 500 AND references/treelint-refactoring-patterns.md exists"
      priority: "High"

    - id: "BR-005"
      rule: "Line range from Treelint results must be used to calculate method/class size for code smell detection"
      trigger: "When analyzing Treelint JSON results for refactoring candidates"
      validation: "lines[1] - lines[0] used to determine function length (>50 = Long Method) and class size (>500 = God Object)"
      error_handling: "If lines array missing, fall back to Read() + manual line count"
      test_requirement: "Test: Reference file contains line range calculation examples for code smell thresholds"
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
      metric: "Core subagent file <= 500 lines per ADR-012; reference files loaded on demand"
      test_requirement: "Test: wc -l on refactoring-specialist.md <= 500"
      priority: "High"
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
    impact: "Projects using unsupported languages get text-based search only (no token reduction or structural analysis improvement for those languages)"

  - id: TL-002
    component: "refactoring-specialist subagent"
    limitation: "Current file is 595 lines - already exceeds 500-line target. Adding Treelint patterns (50-100 lines) makes extraction to references/ MANDATORY, not optional"
    decision: "workaround:Extract Treelint patterns AND existing refactoring catalog examples to references/ per ADR-012"
    discovered_phase: "Architecture"
    impact: "Must restructure refactoring-specialist.md, moving ~200+ lines of refactoring catalog examples to a reference file to bring core file under 500 lines while adding Treelint content"

  - id: TL-003
    component: "Treelint code smell detection"
    limitation: "Treelint provides structural data (line ranges, symbol names) but cannot calculate cyclomatic complexity directly - complexity still requires manual analysis or separate tooling"
    decision: "workaround:Use Treelint for structure discovery (class/method enumeration, line counts) and continue manual complexity analysis for conditional logic"
    discovered_phase: "Architecture"
    impact: "Cyclomatic complexity calculation remains unchanged; Treelint improves symbol discovery but not complexity measurement"

  - id: TL-004
    component: "refactoring-specialist subagent"
    limitation: "Subagent is markdown documentation, not executable code - Treelint patterns are instructions for AI agent behavior, not programmatic implementations"
    decision: "workaround:Documentation-based patterns validated via structural tests (Grep for required sections in markdown)"
    discovered_phase: "Architecture"
    impact: "Tests are structural (verify sections exist in markdown) rather than functional (verify runtime behavior)"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Treelint Search:**
- Treelint search latency: < 100ms per invocation (p95) via stats.elapsed_ms
- Treelint map (ranked): < 500ms per invocation (p95) for codebases up to 1,000 files
- Total refactoring analysis overhead: < 1 second additional vs. Grep-only approach for combined class + function + map queries
- Grep fallback latency: < 2 seconds (p95) for codebases up to 10,000 files

### Security

**Shell Injection Prevention:**
- All Treelint command arguments use simple patterns (alphanumeric + `*` wildcard only)
- Native Grep tool used for fallback (not `Bash(command="grep ...")`) per tech-stack.md constraint
- File paths from Treelint results validated before Read() to prevent path traversal

### Reliability

**Fallback Guarantees:**
- 100% of Treelint failures result in successful Grep fallback
- One-shot fallback: Treelint fails once -> Grep once; no retry loops
- Empty results (exit code 0) treated as valid, NOT as failure
- All 5 failure modes handled: binary not found, permission denied, runtime error, unsupported type, malformed JSON

### Scalability

**Token Budget:**
- Core subagent file reduced to <= 500 lines (from current 595) per ADR-012
- Reference files loaded on demand via Read() instructions
- Stateless search operations; no shared state between invocations
- Refactoring patterns extensible by adding new Treelint search commands to reference file

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-361:** Create Treelint Skill Reference Files for Subagent Integration
  - **Why:** Provides the shared Treelint usage patterns referenced by refactoring-specialist
  - **Status:** Backlog

- [ ] **STORY-362:** Implement Hybrid Fallback Logic (Treelint to Grep)
  - **Why:** Provides the fallback decision tree and language support matrix
  - **Status:** Backlog

### External Dependencies

- [ ] **EPIC-055 (Treelint Foundation):** ADR-013 approved, tech-stack.md updated, Treelint binary distributed
  - **Owner:** Framework Architect
  - **Status:** Planning

- [ ] **EPIC-056 (Context Files):** source-tree.md and anti-patterns.md updated for Treelint
  - **Owner:** Framework Architect
  - **Status:** Planning

### Technology Dependencies

- [ ] **Treelint:** v0.12.0+ binary
  - **Purpose:** AST-aware code search CLI
  - **Approved:** Yes (ADR-013)
  - **Added to dependencies.md:** Yes (v1.1)

---

## Edge Cases

1. **Current file already over 500-line limit:** refactoring-specialist.md is 595 lines. Adding Treelint patterns (50-100 lines) makes extraction MANDATORY. Must extract both Treelint patterns AND existing refactoring catalog examples (lines 101-368, approximately 267 lines of code smell examples and refactoring patterns) to reference files. Core file adds Read() instructions for on-demand loading.

2. **Mixed-language projects:** refactoring-specialist may need to analyze structure across Python (.py - Treelint) and C# (.cs - Grep) in the same project. Per-file-extension decisions required, aggregating results from both tools for a unified view of refactoring candidates.

3. **Empty results vs. command failure:** Treelint returning exit code 0 with empty results array (no classes/functions found) is NOT a failure -- the file may simply have no symbols. Must distinguish from non-zero exit codes that trigger Grep fallback.

4. **Large class bodies exceeding context window:** Treelint's `body` field for God Object classes may be very large (>500 lines). Use `lines` field for targeted `Read()` with offset/limit instead of consuming full body from JSON. Calculate class size from `lines[1] - lines[0]`.

5. **Treelint binary version mismatch:** Pre-v0.12.0 versions lacking `--format json` or `treelint map` support may fail with unrecognized flag error. Treat any non-zero exit code as failure and fall back to Grep.

6. **Concurrent invocations:** Multiple parallel refactoring-specialist invocations (e.g., during parallel story development) are safe since Treelint is stateless/read-only. No shared state between invocations per architecture constraint.

7. **Functions inside classes vs. standalone functions:** Treelint `--type function` may return both methods within classes and standalone functions. When calculating "methods per class" for God Object detection, the refactoring-specialist must correlate function results with class results using file path and line range containment (function lines within class lines).

8. **Cyclomatic complexity not provided by Treelint:** Treelint provides structural data (line ranges, symbol counts) but not cyclomatic complexity. The refactoring-specialist's existing complexity calculation logic must be preserved and used alongside Treelint structural data.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic (structural validation of markdown)

**Test Scenarios:**
1. **Happy Path:** refactoring-specialist.md contains Treelint search instructions for class and function discovery
2. **Edge Cases:**
   - Verify supported file extensions listed
   - Verify JSON parsing instruction references all required fields
   - Verify progressive disclosure compliance (<=500 lines AND reference file exists)
   - Verify at least 4 refactoring-specific Treelint patterns documented
   - Verify treelint map --ranked integration documented
3. **Error Cases:**
   - Verify Grep fallback section exists
   - Verify fallback uses warning level (not error/HALT)
   - Verify empty results handling documented

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **Reference File Loading:** Verify refactoring-specialist.md contains Read() for treelint-refactoring-patterns.md
2. **End-to-End Pattern:** Verify Treelint -> JSON parse -> code smell detection -> refactoring recommendation flow documented

---

## Acceptance Criteria Verification Checklist

### AC#1: Treelint Integration for Code Structure Analysis

- [ ] refactoring-specialist.md or reference file contains `treelint search --type class` instruction - **Phase:** 2 - **Evidence:** test_ac1_treelint_structure_analysis.sh
- [ ] refactoring-specialist.md or reference file contains `treelint search --type function` instruction - **Phase:** 2 - **Evidence:** test_ac1_treelint_structure_analysis.sh
- [ ] Instructions use `--format json` flag - **Phase:** 2 - **Evidence:** test_ac1_treelint_structure_analysis.sh
- [ ] Uses Bash() tool for Treelint invocation - **Phase:** 2 - **Evidence:** test_ac1_treelint_structure_analysis.sh

### AC#2: JSON Parsing of Treelint Search Results

- [ ] JSON parsing instructions reference `name` field - **Phase:** 2 - **Evidence:** test_ac2_json_parsing.sh
- [ ] JSON parsing instructions reference `file` field - **Phase:** 2 - **Evidence:** test_ac2_json_parsing.sh
- [ ] JSON parsing instructions reference `lines` field - **Phase:** 2 - **Evidence:** test_ac2_json_parsing.sh
- [ ] JSON parsing instructions reference `signature` field - **Phase:** 2 - **Evidence:** test_ac2_json_parsing.sh

### AC#3: Grep Fallback for Unsupported Languages

- [ ] Fallback section exists in refactoring-specialist.md or reference files - **Phase:** 2 - **Evidence:** test_ac3_grep_fallback.sh
- [ ] Fallback uses native Grep tool (not Bash grep) - **Phase:** 2 - **Evidence:** test_ac3_grep_fallback.sh
- [ ] Warning-level messaging on fallback - **Phase:** 2 - **Evidence:** test_ac3_grep_fallback.sh

### AC#4: Refactoring-Specific Treelint Patterns

- [ ] God Object detection pattern documented (class >500 lines via line range) - **Phase:** 3 - **Evidence:** test_ac4_refactoring_patterns.sh
- [ ] Long Method detection pattern documented (function >50 lines via line range) - **Phase:** 3 - **Evidence:** test_ac4_refactoring_patterns.sh
- [ ] Extract Class candidates via treelint map --ranked - **Phase:** 3 - **Evidence:** test_ac4_refactoring_patterns.sh
- [ ] Long Parameter List detection via signature analysis - **Phase:** 3 - **Evidence:** test_ac4_refactoring_patterns.sh

### AC#5: Progressive Disclosure Compliance

- [ ] refactoring-specialist.md file line count <= 500 - **Phase:** 4 - **Evidence:** test_ac5_line_count.sh
- [ ] Reference file exists at references/treelint-refactoring-patterns.md - **Phase:** 4 - **Evidence:** test_ac5_line_count.sh
- [ ] Core file contains Read() instruction for reference file - **Phase:** 4 - **Evidence:** test_ac5_line_count.sh

### AC#6: Ranked File Map for Refactoring Prioritization

- [ ] treelint map --ranked --format json command documented - **Phase:** 3 - **Evidence:** test_ac6_ranked_file_map.sh
- [ ] JSON parsing for ranked results documented - **Phase:** 3 - **Evidence:** test_ac6_ranked_file_map.sh

---

**Checklist Progress:** 0/20 items complete (0%)

---

## Definition of Done

### Implementation
- [x] refactoring-specialist.md updated with Treelint code structure analysis section
- [x] JSON parsing instructions added for Treelint response fields (name, file, lines, signature)
- [x] Language support check (supported extensions) documented in subagent
- [x] Grep fallback section with warning-level messaging added
- [x] 4+ refactoring-specific Treelint patterns documented (God Object, Long Method, Extract Class, Long Parameter List)
- [x] treelint map --ranked integration added for refactoring prioritization
- [x] STORY-361 reference file loading instruction (Read()) added
- [x] File size reduced to <= 500 lines (extract to references/ per ADR-012)
- [x] Treelint refactoring patterns reference file created at references/treelint-refactoring-patterns.md

### Quality
- [x] All 6 acceptance criteria have passing tests
- [x] Edge cases documented (mixed languages, empty results, version mismatch, concurrent invocations, class vs function correlation)
- [x] NFRs met (performance <100ms, zero workflow interruptions, shell injection prevention)
- [x] Code coverage >95% for structural tests

### Testing
- [x] test_ac1_treelint_structure_analysis.sh passes
- [x] test_ac2_json_parsing.sh passes
- [x] test_ac3_grep_fallback.sh passes
- [x] test_ac4_refactoring_patterns.sh passes
- [x] test_ac5_line_count.sh passes
- [x] test_ac6_ranked_file_map.sh passes

### Documentation
- [x] refactoring-specialist.md contains clear Treelint usage instructions for code structure analysis
- [x] Refactoring-specific Treelint patterns documented with code smell thresholds
- [x] Fallback behavior documented for all failure modes
- [x] Reference file loading documented (STORY-361 dependency)

---

## QA Validation History

| Date | Mode | Result | Report |
|------|------|--------|--------|
| 2026-02-07 | Deep | ✅ PASSED (40/40 tests, 6/6 ACs, 34/34 sub-checks) | devforgeai/qa/reports/STORY-367-qa-report.md |

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-05 | claude/story-requirements-analyst | Created | Story created via /create-story (EPIC-057 Feature 6: refactoring-specialist) | STORY-367-update-refactoring-specialist-treelint-integration.story.md |
| 2026-02-05 | claude/sprint-planner | Sprint Planning | Assigned to Sprint-10, status → Ready for Dev | STORY-367-update-refactoring-specialist-treelint-integration.story.md |
| 2026-02-07 | claude/devforgeai-development | Dev Complete | TDD workflow completed - all 6 ACs passing, 40/40 tests | refactoring-specialist.md, treelint-refactoring-patterns.md |
| 2026-02-07 | claude/devforgeai-qa | QA Approved | Deep QA: 40/40 tests, 6/6 ACs, 34/34 sub-checks, 0 blocking violations | STORY-367-qa-report.md |

## Implementation Notes

- [x] refactoring-specialist.md updated with Treelint code structure analysis section - Completed: Added Treelint-Aware Code Structure Analysis section at lines 61-90 in src/claude/agents/refactoring-specialist.md
- [x] JSON parsing instructions added for Treelint response fields (name, file, lines, signature) - Completed: Documented in reference file lines 55-118 with parsing patterns
- [x] Language support check (supported extensions) documented in subagent - Completed: Supported extensions (.py, .ts, .tsx, .js, .jsx, .rs, .md) documented in reference file line 45
- [x] Grep fallback section with warning-level messaging added - Completed: Fallback section at reference file lines 257-318 with warning-level messaging
- [x] 4+ refactoring-specific Treelint patterns documented (God Object, Long Method, Extract Class, Long Parameter List) - Completed: 4 patterns documented at reference file lines 122-218
- [x] treelint map --ranked integration added for refactoring prioritization - Completed: Ranked File Map section at reference file lines 222-254
- [x] STORY-361 reference file loading instruction (Read()) added - Completed: Read() instructions at core file lines 65-68
- [x] File size reduced to <= 500 lines (extract to references/ per ADR-012) - Completed: Core file reduced from 595 to 378 lines (36% reduction)
- [x] Treelint refactoring patterns reference file created at references/treelint-refactoring-patterns.md - Completed: Created src/claude/agents/refactoring-specialist/references/treelint-refactoring-patterns.md (335 lines)

## Notes

**Design Decisions:**
- Treelint invoked directly via Bash tool per architecture constraint (subagents cannot delegate to wrapper subagent)
- Shared reference file from STORY-361 loaded via Read() to minimize duplication across 7 subagents
- Progressive disclosure (ADR-012) MANDATORY since current refactoring-specialist.md is 595 lines (already over 500-line limit); must extract existing refactoring catalog examples (~267 lines) AND Treelint patterns to reference files
- Structural tests (Grep for markdown sections) rather than runtime tests, since subagent is a markdown definition
- 4 refactoring-specific patterns (God Object, Long Method, Extract Class candidates, Long Parameter List) mapped to Fowler catalog code smells
- treelint map --ranked integration unique to refactoring-specialist (not used by most sibling stories) for file-level prioritization
- Combined approach: Treelint for AST-aware structure discovery + existing complexity calculation for cyclomatic analysis

**Open Questions:**
- [ ] How much of the existing refactoring catalog (lines 101-368) to extract vs. keep inline -- balance between core file size and immediate utility - **Owner:** Developer - **Due:** During development
- [ ] Whether to create one reference file (treelint-refactoring-patterns.md) or two (treelint-patterns.md + refactoring-catalog.md) for the extracted content - **Owner:** Developer - **Due:** During development

**Related ADRs:**
- ADR-012: Progressive Disclosure for Subagents
- ADR-013: Treelint Integration for AST-Aware Code Search

**References:**
- EPIC-057: Treelint Subagent Integration
- STORY-361: Create Treelint Skill Reference Files
- STORY-362: Implement Hybrid Fallback Logic
- tech-stack.md lines 104-166: Treelint approved section
- tech-stack.md lines 385-388: Subagent size limits
- source-tree.md lines 593-626: Subagent progressive disclosure pattern
- architecture-constraints.md lines 25-26: Subagent delegation prohibition
- Martin Fowler's Refactoring Catalog: Code smell definitions and thresholds

---

Story Template Version: 2.8
Last Updated: 2026-02-05
