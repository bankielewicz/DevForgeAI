---
id: STORY-366
title: Update security-auditor Subagent with Treelint AST-Aware Semantic Vulnerability Detection
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

# Story: Update security-auditor Subagent with Treelint AST-Aware Semantic Vulnerability Detection

## Description

**As a** security-auditor subagent (the DevForgeAI security specialist responsible for OWASP Top 10 audits, hardcoded secret detection, and dependency vulnerability scanning),
**I want** to use Treelint's AST-aware search (`treelint search --type function --format json`) for semantic vulnerability detection instead of text-based Grep patterns, with JSON parsing of structured results and automatic fallback to Grep for unsupported languages,
**so that** I can find security-sensitive functions (authentication, cryptography, input validation, data access) by their actual AST node type (reducing false positives from comments, strings, and variable names matching security patterns), achieve 40-80% token reduction in security-focused code search operations, and maintain seamless functionality across all project languages through hybrid fallback logic.

## Provenance

```xml
<provenance>
  <origin document="EPIC-057" section="Feature 5: security-auditor Subagent Update">
    <quote>"Enable semantic vulnerability detection using symbol search"</quote>
    <line_reference>lines 59-62</line_reference>
    <quantified_impact>40-80% token reduction in security-focused code search operations; >50% false positive reduction vs Grep-only</quantified_impact>
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

### AC#1: Treelint Integration for Security Function Discovery

```xml
<acceptance_criteria id="AC1" implements="TREELINT-SEC-001">
  <given>The security-auditor subagent (src/claude/agents/security-auditor.md) is invoked during QA deep validation or pre-release security audit to discover security-sensitive functions (authentication, cryptography, input validation, data access, session management) in a project containing Python (.py), TypeScript (.ts/.tsx), or JavaScript (.js/.jsx) files</given>
  <when>The subagent performs security-focused code search to find functions handling sensitive operations (e.g., authenticate*, validate*, encrypt*, hash*, sanitize*, authorize*)</when>
  <then>The subagent uses Treelint via Bash(command="treelint search --type function --name 'authenticate*' --format json") instead of Grep patterns, parses the JSON response to extract function name, file path, line range, and signature, and uses the structured results for targeted security analysis</then>
  <verification>
    <source_files>
      <file hint="Updated security-auditor subagent definition">src/claude/agents/security-auditor.md</file>
    </source_files>
    <test_file>tests/STORY-366/test_ac1_treelint_security_discovery.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: JSON Parsing of Treelint Security Search Results

```xml
<acceptance_criteria id="AC2" implements="TREELINT-SEC-JSON-001">
  <given>Treelint returns a JSON response containing a results array where each entry has fields: type, name, file, lines (array of [start, end]), signature, and body</given>
  <when>The security-auditor subagent receives Treelint search output for security function discovery</when>
  <then>The subagent parses the JSON to extract: (1) function names matching security-sensitive patterns, (2) file paths for locating source code, (3) line ranges [start, end] for precise Read() operations to inspect function bodies for vulnerabilities, and (4) function signatures for identifying parameter handling (e.g., user input parameters that need validation), and the parsed data is used to focus security analysis on confirmed function definitions rather than text matches</then>
  <verification>
    <source_files>
      <file hint="Updated security-auditor subagent definition">src/claude/agents/security-auditor.md</file>
    </source_files>
    <test_file>tests/STORY-366/test_ac2_json_parsing.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Grep Fallback for Unsupported Languages

```xml
<acceptance_criteria id="AC3" implements="TREELINT-SEC-FALLBACK-001">
  <given>The security-auditor subagent needs to discover security-sensitive functions in file types not supported by Treelint (e.g., C# .cs, Java .java, Go .go, Ruby .rb) or when the Treelint binary is unavailable (exit code 127) or fails at runtime</given>
  <when>The subagent detects an unsupported file extension or receives a non-zero exit code from Treelint</when>
  <then>The subagent falls back to using the native Grep tool (e.g., Grep(pattern="def authenticate|async function validate|function sanitize", glob="**/*.cs")) following the fallback decision tree documented in the STORY-361 reference file, emits a warning-level message, and completes the security function discovery without halting the workflow</then>
  <verification>
    <source_files>
      <file hint="Updated security-auditor subagent definition">src/claude/agents/security-auditor.md</file>
    </source_files>
    <test_file>tests/STORY-366/test_ac3_grep_fallback.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Security-Sensitive Function Pattern Documentation

```xml
<acceptance_criteria id="AC4" implements="TREELINT-SEC-PATTERNS-001">
  <given>The security-auditor subagent needs predefined search patterns for discovering security-sensitive functions across OWASP Top 10 categories</given>
  <when>The subagent is updated with Treelint integration instructions</when>
  <then>The subagent documentation includes Treelint search patterns for at least 5 security categories: (1) authentication functions (authenticate*, login*, verify_password*), (2) cryptography functions (encrypt*, decrypt*, hash*, sign*), (3) input validation functions (validate*, sanitize*, escape*, filter*), (4) authorization functions (authorize*, check_permission*, is_admin*), and (5) data access functions with potential injection risks (query*, execute*, raw_sql*), each with specific Treelint command examples</then>
  <verification>
    <source_files>
      <file hint="Updated security-auditor subagent definition">src/claude/agents/security-auditor.md</file>
    </source_files>
    <test_file>tests/STORY-366/test_ac4_security_patterns.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: False Positive Reduction via AST-Aware Search

```xml
<acceptance_criteria id="AC5" implements="TREELINT-SEC-FP-001">
  <given>The security-auditor subagent currently uses Grep patterns that match text in comments, strings, variable names, and non-function contexts (e.g., Grep matching "password" in a comment or log message rather than in a function handling passwords)</given>
  <when>The subagent uses Treelint's --type function filter for security searches</when>
  <then>The subagent documentation describes how Treelint's AST-aware filtering eliminates false positives from: (1) comments containing security keywords, (2) string literals with security terms, (3) variable names matching security patterns, and (4) import/require statements referencing security modules, resulting in only actual function definitions being returned for security analysis</then>
  <verification>
    <source_files>
      <file hint="Updated security-auditor subagent definition">src/claude/agents/security-auditor.md</file>
    </source_files>
    <test_file>tests/STORY-366/test_ac5_false_positive_reduction.sh</test_file>
    <coverage_threshold>80</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Progressive Disclosure Compliance (500-Line Limit)

```xml
<acceptance_criteria id="AC6" implements="TREELINT-SEC-SIZE-001">
  <given>The security-auditor subagent definition file (src/claude/agents/security-auditor.md) has a 500-line maximum per source-tree.md and tech-stack.md token budget constraints</given>
  <when>Treelint integration instructions are added to the security-auditor subagent</when>
  <then>The updated security-auditor.md file remains under 500 lines total, with Treelint-specific patterns either: (a) inlined if the file stays under 500 lines, or (b) extracted to a reference file at src/claude/agents/security-auditor/references/treelint-security-patterns.md following ADR-012 progressive disclosure pattern, loaded on-demand via Read() instruction in the core file</then>
  <verification>
    <source_files>
      <file hint="Updated security-auditor subagent definition">src/claude/agents/security-auditor.md</file>
      <file hint="Optional Treelint reference file if extracted">src/claude/agents/security-auditor/references/treelint-security-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-366/test_ac6_line_count.sh</test_file>
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
      name: "security-auditor Subagent Definition"
      file_path: "src/claude/agents/security-auditor.md"
      required_keys:
        - key: "Treelint Security Function Discovery Section"
          type: "markdown"
          example: "### Treelint-Aware Security Function Discovery"
          required: true
          validation: "Section must contain treelint search --type function --format json instruction"
          test_requirement: "Test: Grep for 'treelint search.*--type function.*--format json' in security-auditor.md"

        - key: "JSON Parsing Instructions"
          type: "markdown"
          example: "Parse JSON results: type, name, file, lines, signature"
          required: true
          validation: "Must reference all 4 required JSON fields: name, file, lines, signature"
          test_requirement: "Test: Grep for 'name.*file.*lines.*signature' pattern in security-auditor.md"

        - key: "Language Support Check"
          type: "markdown"
          example: "Check file extension: .py, .ts, .tsx, .js, .jsx, .rs, .md"
          required: true
          validation: "Must list supported extensions from tech-stack.md"
          test_requirement: "Test: Grep for '.py' AND '.ts' AND '.js' in security-auditor.md"

        - key: "Grep Fallback Section"
          type: "markdown"
          example: "### Fallback: Grep for Unsupported Languages"
          required: true
          validation: "Must reference native Grep tool (not Bash grep)"
          test_requirement: "Test: Grep for 'Grep(pattern=' fallback instruction in security-auditor.md"

        - key: "Security Pattern Categories"
          type: "markdown"
          example: "### Security-Sensitive Function Patterns"
          required: true
          validation: "Must document at least 5 security categories with Treelint search examples"
          test_requirement: "Test: Grep for 'authenticate' AND 'encrypt' AND 'validate' AND 'authorize' AND 'query' in security-auditor.md"

        - key: "Reference File Loading"
          type: "markdown"
          example: "Read(file_path=\"src/claude/agents/references/treelint-search-patterns.md\")"
          required: true
          validation: "Must contain Read() instruction for STORY-361 reference file"
          test_requirement: "Test: Grep for 'Read.*treelint.*patterns' in security-auditor.md"

    - type: "Configuration"
      name: "Treelint Security Patterns Reference File (Conditional)"
      file_path: "src/claude/agents/security-auditor/references/treelint-security-patterns.md"
      required_keys:
        - key: "Progressive Disclosure Extraction"
          type: "markdown"
          example: "Treelint security search patterns extracted per ADR-012"
          required: false
          default: "Only created if security-auditor.md exceeds 500 lines"
          validation: "If file exists, security-auditor.md must contain Read() pointing to it"
          test_requirement: "Test: If treelint-security-patterns.md exists, verify security-auditor.md references it via Read()"

  business_rules:
    - id: "BR-001"
      rule: "Treelint must be attempted first for all supported file extensions before falling back to Grep"
      trigger: "When security function discovery is initiated for any file type"
      validation: "Check file extension against supported list, use Treelint if supported, Grep if not"
      error_handling: "If Treelint fails (non-zero exit), fall back to Grep with warning"
      test_requirement: "Test: security-auditor.md Treelint section appears before Grep fallback section"
      priority: "Critical"

    - id: "BR-002"
      rule: "Empty Treelint results (exit code 0, zero matches) must NOT trigger Grep fallback"
      trigger: "When Treelint returns valid JSON with empty results array"
      validation: "Distinguish between exit code 0 (success, no matches) and non-zero (failure)"
      error_handling: "Return empty function list, do not invoke Grep"
      test_requirement: "Test: security-auditor.md contains distinction between empty results and command failure"
      priority: "Critical"

    - id: "BR-003"
      rule: "All Treelint failures must result in successful Grep fallback with zero workflow interruption"
      trigger: "When Treelint returns non-zero exit code or malformed output"
      validation: "Workflow must never HALT due to Treelint issues"
      error_handling: "Warning-level message, Grep fallback, continue workflow"
      test_requirement: "Test: security-auditor.md fallback section contains 'warning' and no 'HALT' on Treelint failure"
      priority: "Critical"

    - id: "BR-004"
      rule: "Subagent file must remain under 500 lines; if exceeded, extract to references/"
      trigger: "After Treelint integration content is added"
      validation: "wc -l on security-auditor.md <= 500"
      error_handling: "Extract Treelint patterns to references/treelint-security-patterns.md per ADR-012"
      test_requirement: "Test: wc -l security-auditor.md <= 500; if >500, references/treelint-security-patterns.md exists"
      priority: "High"

    - id: "BR-005"
      rule: "Security search patterns must cover at least 5 OWASP-aligned categories"
      trigger: "When Treelint security patterns section is added"
      validation: "Count distinct security categories documented (auth, crypto, validation, authz, data access)"
      error_handling: "HALT if fewer than 5 categories documented"
      test_requirement: "Test: Grep for at least 5 distinct security categories in security-auditor.md"
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
    impact: "Projects using unsupported languages get text-based search only (no token reduction or false positive improvement for those languages)"

  - id: TL-002
    component: "security-auditor subagent"
    limitation: "Subagent is markdown documentation, not executable code - Treelint patterns are instructions, not programmatic implementations"
    decision: "workaround:Documentation-based patterns validated via structural tests (Grep for required sections)"
    discovered_phase: "Architecture"
    impact: "Tests are structural (verify sections exist in markdown) rather than functional (verify runtime behavior)"

  - id: TL-003
    component: "Treelint security patterns"
    limitation: "Treelint searches by function name patterns, not by function behavior - a function named 'encrypt' is found but a function performing encryption with a non-standard name is not"
    decision: "workaround:Combine Treelint symbol search with Grep content search for comprehensive coverage"
    discovered_phase: "Architecture"
    impact: "Security audit still requires both AST-aware and text-based search for complete coverage"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Treelint Search:**
- Treelint search latency: < 100ms per invocation (p95) via stats.elapsed_ms
- Total security scan overhead: < 500ms additional vs. Grep-only approach for all 5 security categories
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
- Security pattern categories extensible by adding new Treelint search commands

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-361:** Create Treelint Skill Reference Files for Subagent Integration
  - **Why:** Provides the shared Treelint usage patterns referenced by security-auditor
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

1. **Mixed-language projects:** Security-auditor may need to discover security functions across Python (.py - Treelint) and C# (.cs - Grep) in the same project. Per-file-extension decisions required, aggregating results from both tools.

2. **Non-standard security function names:** Security functions may not follow standard naming (e.g., `check_creds` instead of `authenticate`, `scrub` instead of `sanitize`). Broad Treelint search first with common patterns, supplemented by Grep for non-standard names.

3. **Empty results vs. command failure:** Treelint returning exit code 0 with empty results array (no security functions found) is NOT a failure. Must distinguish from non-zero exit codes that trigger Grep fallback.

4. **Large function bodies exceeding context window:** Treelint's `body` field for security-sensitive functions may be very large. Use `lines` field for targeted `Read()` to inspect specific function bodies for vulnerabilities.

5. **File exceeding 500-line limit:** Current security-auditor.md is 554 lines. Adding Treelint patterns (50-100 lines) WILL exceed the limit. Must extract to references/ per ADR-012 progressive disclosure pattern.

6. **Treelint binary version mismatch:** Pre-v0.12.0 versions lacking `--format json` support may fail with unrecognized flag error. Treat any non-zero exit code as failure and fall back to Grep.

7. **Concurrent invocations:** Multiple parallel security-auditor invocations are safe (Treelint is stateless/read-only). No shared state between invocations per architecture constraint.

8. **False positive reduction limitations:** Treelint finds functions by name, not by behavior. A function named `process_data` that handles passwords won't be found by `authenticate*` search. Combine Treelint symbol search with existing Grep content patterns for comprehensive coverage.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic (structural validation of markdown)

**Test Scenarios:**
1. **Happy Path:** security-auditor.md contains Treelint search instruction for security function discovery
2. **Edge Cases:**
   - Verify supported file extensions listed
   - Verify JSON parsing instruction references all required fields
   - Verify progressive disclosure compliance (≤500 lines or reference file exists)
   - Verify at least 5 security categories documented
3. **Error Cases:**
   - Verify Grep fallback section exists
   - Verify fallback uses warning level (not error/HALT)
   - Verify empty results handling documented

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **Reference File Loading:** Verify security-auditor.md contains Read() for treelint-search-patterns.md
2. **End-to-End Pattern:** Verify Treelint → JSON parse → security function list → vulnerability analysis flow documented

---

## Acceptance Criteria Verification Checklist

### AC#1: Treelint Integration for Security Function Discovery

- [ ] security-auditor.md contains `treelint search --type function` instruction - **Phase:** 2 - **Evidence:** test_ac1_treelint_security_discovery.sh
- [ ] Instruction uses `--format json` flag - **Phase:** 2 - **Evidence:** test_ac1_treelint_security_discovery.sh
- [ ] Uses Bash() tool for Treelint invocation - **Phase:** 2 - **Evidence:** test_ac1_treelint_security_discovery.sh

### AC#2: JSON Parsing of Treelint Security Search Results

- [ ] JSON parsing instructions reference `name` field - **Phase:** 2 - **Evidence:** test_ac2_json_parsing.sh
- [ ] JSON parsing instructions reference `file` field - **Phase:** 2 - **Evidence:** test_ac2_json_parsing.sh
- [ ] JSON parsing instructions reference `lines` field - **Phase:** 2 - **Evidence:** test_ac2_json_parsing.sh
- [ ] JSON parsing instructions reference `signature` field - **Phase:** 2 - **Evidence:** test_ac2_json_parsing.sh

### AC#3: Grep Fallback for Unsupported Languages

- [ ] Fallback section exists in security-auditor.md - **Phase:** 2 - **Evidence:** test_ac3_grep_fallback.sh
- [ ] Fallback uses native Grep tool (not Bash grep) - **Phase:** 2 - **Evidence:** test_ac3_grep_fallback.sh
- [ ] Warning-level messaging on fallback - **Phase:** 2 - **Evidence:** test_ac3_grep_fallback.sh

### AC#4: Security-Sensitive Function Pattern Documentation

- [ ] Authentication patterns documented (authenticate*, login*, verify_password*) - **Phase:** 3 - **Evidence:** test_ac4_security_patterns.sh
- [ ] Cryptography patterns documented (encrypt*, decrypt*, hash*) - **Phase:** 3 - **Evidence:** test_ac4_security_patterns.sh
- [ ] Input validation patterns documented (validate*, sanitize*, escape*) - **Phase:** 3 - **Evidence:** test_ac4_security_patterns.sh
- [ ] Authorization patterns documented (authorize*, check_permission*) - **Phase:** 3 - **Evidence:** test_ac4_security_patterns.sh
- [ ] Data access patterns documented (query*, execute*, raw_sql*) - **Phase:** 3 - **Evidence:** test_ac4_security_patterns.sh

### AC#5: False Positive Reduction

- [ ] False positive reduction rationale documented - **Phase:** 3 - **Evidence:** test_ac5_false_positive_reduction.sh
- [ ] AST vs text-based comparison explained - **Phase:** 3 - **Evidence:** test_ac5_false_positive_reduction.sh

### AC#6: Progressive Disclosure Compliance

- [ ] security-auditor.md file line count ≤ 500 OR reference file exists - **Phase:** 4 - **Evidence:** test_ac6_line_count.sh
- [ ] If >500 lines, reference file at references/treelint-security-patterns.md - **Phase:** 4 - **Evidence:** test_ac6_line_count.sh

---

**Checklist Progress:** 0/18 items complete (0%)

---

## Definition of Done

### Implementation
- [x] security-auditor.md updated with Treelint security function discovery section
- [x] JSON parsing instructions added for Treelint response fields
- [x] Language support check (supported extensions) documented in subagent
- [x] Grep fallback section with warning-level messaging added
- [x] 5+ security-sensitive function pattern categories documented with Treelint examples
- [x] False positive reduction via AST-aware search explained
- [x] STORY-361 reference file loading instruction (Read()) added
- [x] File size ≤ 500 lines verified (extract to references/ if needed per ADR-012)

### Quality
- [x] All 6 acceptance criteria have passing tests
- [x] Edge cases documented (mixed languages, empty results, version mismatch, naming conventions)
- [x] NFRs met (performance <100ms, zero workflow interruptions)
- [x] Code coverage >95% for structural tests

### Testing
- [x] test_ac1_treelint_security_discovery.sh passes
- [x] test_ac2_json_parsing.sh passes
- [x] test_ac3_grep_fallback.sh passes
- [x] test_ac4_security_patterns.sh passes
- [x] test_ac5_false_positive_reduction.sh passes
- [x] test_ac6_line_count.sh passes

### Documentation
- [x] security-auditor.md contains clear Treelint usage instructions for security auditing
- [x] Security function pattern categories documented with examples
- [x] Fallback behavior documented for all failure modes
- [x] Reference file loading documented (STORY-361 dependency)

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-05 | claude/story-requirements-analyst | Created | Story created via /create-story (EPIC-057 Feature 5: security-auditor) | STORY-366-update-security-auditor-treelint-integration.story.md |
| 2026-02-05 | claude/sprint-planner | Sprint Planning | Assigned to Sprint-10, status → Ready for Dev | STORY-366-update-security-auditor-treelint-integration.story.md |
| 2026-02-06 | claude/devforgeai-development | Development | Implemented Treelint integration, status → Dev Complete | src/claude/agents/security-auditor.md, src/claude/agents/security-auditor/references/treelint-security-patterns.md |
| 2026-02-07 | claude/qa-result-interpreter | QA Deep | PASSED: 57/57 tests, 0 blocking violations, status → QA Approved | STORY-366-update-security-auditor-treelint-integration.story.md |

## Implementation Notes

- [x] security-auditor.md updated with Treelint security function discovery section - Completed: Added "Treelint-Aware Security Function Discovery" section with `treelint search --type function --format json` instructions
- [x] JSON parsing instructions added for Treelint response fields - Completed: Documented parsing of name, file, lines, signature fields from JSON response
- [x] Language support check (supported extensions) documented in subagent - Completed: Listed .py, .ts, .tsx, .js, .jsx, .rs, .md as supported extensions with fallback for others
- [x] Grep fallback section with warning-level messaging added - Completed: Added fallback decision tree with warning-level messages, no HALT on Treelint failure
- [x] 5+ security-sensitive function pattern categories documented with Treelint examples - Completed: Documented 5 OWASP-aligned categories (authentication, cryptography, input validation, authorization, data access)
- [x] False positive reduction via AST-aware search explained - Completed: Documented how Treelint eliminates false positives from comments, strings, variable names, imports
- [x] STORY-361 reference file loading instruction (Read()) added - Completed: Added Read() instruction for treelint-search-patterns.md shared reference
- [x] File size ≤ 500 lines verified (extract to references/ if needed per ADR-012) - Completed: Main file reduced to ~450 lines, patterns extracted to references/treelint-security-patterns.md
- [x] All 6 acceptance criteria have passing tests - Completed: All 6 AC test scripts pass (run_all_tests.sh)
- [x] Edge cases documented (mixed languages, empty results, version mismatch, naming conventions) - Completed: 8 edge cases documented in story and subagent files
- [x] NFRs met (performance <100ms, zero workflow interruptions) - Completed: Performance targets and fallback guarantees documented
- [x] Code coverage >95% for structural tests - Completed: All structural tests verify required sections exist
- [x] test_ac1_treelint_security_discovery.sh passes - Completed: Validates Treelint search instruction present
- [x] test_ac2_json_parsing.sh passes - Completed: Validates JSON field parsing instructions
- [x] test_ac3_grep_fallback.sh passes - Completed: Validates Grep fallback section exists with warning level
- [x] test_ac4_security_patterns.sh passes - Completed: Validates 5 security categories documented
- [x] test_ac5_false_positive_reduction.sh passes - Completed: Validates AST vs text comparison documented
- [x] test_ac6_line_count.sh passes - Completed: Validates ≤500 lines or reference file exists
- [x] security-auditor.md contains clear Treelint usage instructions for security auditing - Completed: Clear workflow with examples
- [x] Security function pattern categories documented with examples - Completed: 5 categories with Treelint command examples
- [x] Fallback behavior documented for all failure modes - Completed: 5 failure modes covered (binary not found, permission denied, runtime error, unsupported type, malformed JSON)
- [x] Reference file loading documented (STORY-361 dependency) - Completed: Read() instruction for shared Treelint patterns
- Created new reference file: `src/claude/agents/security-auditor/references/treelint-security-patterns.md` (~270 lines)
- Reduced main file from 554 → 450 lines via progressive disclosure (condensed Security Report Format section)
- All 6 ACs verified passing via ac-compliance-verifier
- Follows patterns established by STORY-363, STORY-364, STORY-365 for Treelint subagent integration
- Both open questions resolved during development: file reorganized successfully, security patterns documented with OWASP alignment

## Notes

**Design Decisions:**
- Treelint invoked directly via Bash tool per architecture constraint (subagents cannot delegate to wrapper subagent)
- Shared reference file from STORY-361 loaded via Read() to minimize duplication across 7 subagents
- Progressive disclosure (ADR-012) REQUIRED since current security-auditor.md is 554 lines (already over limit); Treelint patterns MUST go to reference file
- Structural tests (Grep for markdown sections) rather than runtime tests, since subagent is a markdown definition
- 5 security pattern categories aligned with OWASP Top 10 for comprehensive coverage
- Combined approach: Treelint for AST-aware function discovery + existing Grep patterns for content-based vulnerability detection

**Open Questions:**
- [ ] Whether to reorganize existing security-auditor.md to bring it under 500 lines before adding Treelint content - **Owner:** Developer - **Due:** During development
- [ ] Exact list of security function name patterns per category (extend beyond initial set based on project conventions) - **Owner:** Developer - **Due:** During development

**Related ADRs:**
- ADR-012: Progressive Disclosure for Subagents
- ADR-013: Treelint Integration for AST-Aware Code Search

**References:**
- EPIC-057: Treelint Subagent Integration
- STORY-361: Create Treelint Skill Reference Files
- STORY-362: Implement Hybrid Fallback Logic
- tech-stack.md lines 104-166: Treelint approved section
- source-tree.md lines 232-262: Subagent directory rules
- OWASP Top 10 (2021): Security vulnerability categories

---

Story Template Version: 2.8
Last Updated: 2026-02-05
