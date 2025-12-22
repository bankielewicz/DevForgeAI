---
id: STORY-119
title: Output Format - JSON, Text, and Markdown Reports
epic: EPIC-018
sprint: SPRINT-7
status: Cancelled - see story-118 for reason
points: 3
depends_on: ["STORY-115", "STORY-117", "STORY-118"]
priority: Medium
assigned_to: Unassigned
created: 2025-12-20
format_version: "2.2"
---

# Story: Output Format - JSON, Text, and Markdown Reports

## Description

**As a** DevForgeAI user,
**I want** ast-grep violations output in JSON, text, and markdown formats,
**so that** I can integrate results with automation (JSON), review quickly (text), and include in QA reports (markdown).

**Context:** This story implements Feature 5 of EPIC-018 (ast-grep Foundation & Core Rules). It provides output formatting compatible with DevForgeAI QA reporting and includes severity mapping (CRITICAL/HIGH/MEDIUM/LOW).

## Acceptance Criteria

### AC#1: JSON Output Format

**Given** violations detected by ast-grep,
**When** the user specifies `--format json`,
**Then** output is valid JSON with schema:
```json
{
  "violations": [
    {
      "id": "SEC-001",
      "file": "src/example.py",
      "line": 42,
      "column": 15,
      "severity": "CRITICAL",
      "category": "security",
      "message": "SQL injection vulnerability detected",
      "evidence": "query = f\"SELECT * FROM users WHERE id = {user_id}\"",
      "fix": "Use parameterized queries: cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))"
    }
  ],
  "summary": {
    "total": 5,
    "critical": 2,
    "high": 1,
    "medium": 2,
    "low": 0
  },
  "metadata": {
    "analysis_method": "ast-grep",
    "version": "0.40.0",
    "timestamp": "2025-12-20T10:30:00Z",
    "files_scanned": 150,
    "scan_duration_ms": 2500
  }
}
```

---

### AC#2: Human-Readable Text Output

**Given** violations detected by ast-grep,
**When** the user specifies `--format text` (default),
**Then** output is human-readable:
```
=== ast-grep Scan Results ===

CRITICAL: SQL injection vulnerability detected
  File: src/example.py:42:15
  Rule: SEC-001 (security)
  Evidence: query = f"SELECT * FROM users WHERE id = {user_id}"
  Fix: Use parameterized queries

HIGH: God object detected (>500 lines)
  File: src/services/everything.py:1:1
  Rule: AP-001 (anti-patterns)
  Evidence: Class has 650 lines
  Fix: Split into smaller focused classes

Summary: 5 violations (2 CRITICAL, 1 HIGH, 2 MEDIUM)
Files scanned: 150 | Duration: 2.5s
```

---

### AC#3: Markdown Report Output

**Given** violations detected by ast-grep,
**When** the user specifies `--format markdown`,
**Then** output is markdown compatible with QA reports:
```markdown
# ast-grep Scan Report

**Generated:** 2025-12-20 10:30:00
**Files Scanned:** 150
**Duration:** 2.5s

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 2 |
| HIGH | 1 |
| MEDIUM | 2 |
| LOW | 0 |
| **Total** | **5** |

## CRITICAL Violations

### SEC-001: SQL injection vulnerability detected

- **File:** `src/example.py:42:15`
- **Category:** security
- **Evidence:** `query = f"SELECT * FROM users WHERE id = {user_id}"`
- **Remediation:** Use parameterized queries

## HIGH Violations

...
```

---

### AC#4: Severity Mapping

**Given** ast-grep rule output,
**When** the formatter processes results,
**Then** severity is mapped consistently:
1. CRITICAL → Red color (text), ❌ emoji (markdown)
2. HIGH → Orange color (text), ⚠️ emoji (markdown)
3. MEDIUM → Yellow color (text), ⚡ emoji (markdown)
4. LOW → Blue color (text), ℹ️ emoji (markdown)

---

### AC#5: DevForgeAI QA Integration

**Given** markdown output from ast-grep,
**When** the devforgeai-qa skill runs,
**Then** the output can be:
1. Appended to QA reports (consistent heading levels)
2. Parsed for violation counts (summary table format)
3. Used for quality gate decisions (CRITICAL count > 0 = fail)

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "OutputFormatter"
      file_path: "src/claude/scripts/devforgeai_cli/ast_grep/output_formatter.py"
      interface: "IFormatter"
      lifecycle: "Singleton"
      dependencies:
        - "json"
        - "datetime"
      requirements:
        - id: "SVC-001"
          description: "Format violations as JSON with schema validation"
          testable: true
          test_requirement: "Test: Output validates against JSON schema"
          priority: "Critical"
        - id: "SVC-002"
          description: "Format violations as human-readable text with colors"
          testable: true
          test_requirement: "Test: Text output contains ANSI color codes"
          priority: "High"
        - id: "SVC-003"
          description: "Format violations as markdown with emoji indicators"
          testable: true
          test_requirement: "Test: Markdown output contains proper heading hierarchy"
          priority: "High"

    - type: "Service"
      name: "SeverityMapper"
      file_path: "src/claude/scripts/devforgeai_cli/ast_grep/severity_mapper.py"
      interface: "IMapper"
      lifecycle: "Singleton"
      dependencies: []
      requirements:
        - id: "SVC-004"
          description: "Map severity to ANSI color codes for terminal"
          testable: true
          test_requirement: "Test: CRITICAL maps to red (31), HIGH to orange (33)"
          priority: "Medium"
        - id: "SVC-005"
          description: "Map severity to emoji for markdown"
          testable: true
          test_requirement: "Test: CRITICAL maps to ❌, HIGH to ⚠️"
          priority: "Medium"

    - type: "DataModel"
      name: "ViolationReport"
      table: "N/A (in-memory)"
      purpose: "Schema for violation output"
      fields:
        - name: "violations"
          type: "Array<Violation>"
          constraints: "Required"
          description: "List of detected violations"
          test_requirement: "Test: Empty array valid, null invalid"
        - name: "summary"
          type: "Object"
          constraints: "Required"
          description: "Count by severity"
          test_requirement: "Test: Summary counts match violations array"
        - name: "metadata"
          type: "Object"
          constraints: "Required"
          description: "Scan metadata (version, timestamp, duration)"
          test_requirement: "Test: Metadata includes all required fields"
      relationships:
        - type: "One-to-Many"
          related_entity: "Violation"
          foreign_key: "N/A"
          cascade: "N/A"
          description: "Report contains many violations"

    - type: "API"
      name: "format-output"
      endpoint: "devforgeai ast-grep scan --format <format>"
      method: "CLI"
      authentication:
        required: false
      request:
        content_type: "CLI arguments"
        schema:
          format:
            type: "string"
            required: false
            validation: "One of: json, text, markdown"
      response:
        success:
          status_code: 0
          schema:
            output: "string (formatted)"
        errors:
          - status_code: 1
            condition: "Invalid format specified"
            schema:
              error: "Invalid format. Use: json, text, or markdown"
      requirements:
        - id: "API-001"
          description: "Parse --format argument and route to formatter"
          testable: true
          test_requirement: "Test: Each format produces distinct output"
          priority: "Critical"

  business_rules:
    - id: "BR-001"
      rule: "JSON output must be valid JSON (parseable by json.loads)"
      trigger: "When --format json specified"
      validation: "json.loads(output) succeeds"
      error_handling: "Never output invalid JSON"
      test_requirement: "Test: json.loads on output succeeds for all test cases"
      priority: "Critical"
    - id: "BR-002"
      rule: "Markdown output must use consistent heading hierarchy (h1 > h2 > h3)"
      trigger: "When --format markdown specified"
      validation: "Regex check for proper heading sequence"
      error_handling: "Never skip heading levels"
      test_requirement: "Test: No h3 without preceding h2"
      priority: "High"
    - id: "BR-003"
      rule: "Text output uses ANSI colors only when terminal supports it"
      trigger: "When --format text and output to terminal"
      validation: "Check sys.stdout.isatty()"
      error_handling: "Fall back to no colors if piped"
      test_requirement: "Test: No ANSI codes when piped to file"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Formatting must add <100ms to total scan time"
      metric: "p95 formatting time <100ms for 100 violations"
      test_requirement: "Test: Format 100 violations, measure time <100ms"
      priority: "Low"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "All three formats must produce consistent data"
      metric: "Same violations in JSON/text/markdown (different representation)"
      test_requirement: "Test: Parse all formats, verify same violation count"
      priority: "High"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Formatting overhead: <100ms for 100 violations

---

### Reliability

**Consistency:**
- All formats represent the same data
- JSON is always valid and parseable
- Markdown follows proper structure

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-115:** CLI Validator Foundation
  - **Why:** Provides CLI framework and base output handling
  - **Status:** Backlog

- [x] **STORY-117:** Core Security Rules
  - **Why:** Provides violations to format
  - **Status:** Backlog

- [x] **STORY-118:** Core Anti-pattern Rules
  - **Why:** Provides violations to format
  - **Status:** Backlog

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for formatters

**Test Scenarios:**
1. **Happy Path:** Format 10 violations in each format
2. **Edge Cases:**
   - Empty violations (no issues found)
   - Single violation
   - 1000+ violations (performance)
   - Unicode in file paths
3. **Error Cases:**
   - Invalid format argument
   - Malformed violation data

---

## Acceptance Criteria Verification Checklist

### AC#1: JSON Output Format

- [ ] Valid JSON output - **Phase:** 03 - **Evidence:** test_json_valid.py
- [ ] Schema matches spec - **Phase:** 03 - **Evidence:** test_json_schema.py
- [ ] Summary counts correct - **Phase:** 03 - **Evidence:** test_json_summary.py
- [ ] Metadata included - **Phase:** 03 - **Evidence:** test_json_metadata.py

### AC#2: Human-Readable Text Output

- [ ] Violations formatted - **Phase:** 03 - **Evidence:** test_text_format.py
- [ ] Color codes present - **Phase:** 03 - **Evidence:** test_text_colors.py
- [ ] Summary line present - **Phase:** 03 - **Evidence:** test_text_summary.py

### AC#3: Markdown Report Output

- [ ] Proper heading hierarchy - **Phase:** 03 - **Evidence:** test_markdown_headings.py
- [ ] Table formatting correct - **Phase:** 03 - **Evidence:** test_markdown_table.py
- [ ] Emoji indicators present - **Phase:** 03 - **Evidence:** test_markdown_emoji.py

### AC#4: Severity Mapping

- [ ] CRITICAL = red/❌ - **Phase:** 03 - **Evidence:** test_severity_critical.py
- [ ] HIGH = orange/⚠️ - **Phase:** 03 - **Evidence:** test_severity_high.py
- [ ] MEDIUM = yellow/⚡ - **Phase:** 03 - **Evidence:** test_severity_medium.py
- [ ] LOW = blue/ℹ️ - **Phase:** 03 - **Evidence:** test_severity_low.py

### AC#5: DevForgeAI QA Integration

- [ ] Appendable to QA reports - **Phase:** 05 - **Evidence:** test_qa_integration.py
- [ ] Parseable summary table - **Phase:** 05 - **Evidence:** test_qa_parsing.py
- [ ] Quality gate compatible - **Phase:** 05 - **Evidence:** test_qa_gate.py

---

**Checklist Progress:** 0/17 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] OutputFormatter class with json(), text(), markdown() methods
- [ ] SeverityMapper class with color and emoji mappings
- [ ] --format argument integrated into CLI
- [ ] Default format is text

### Quality
- [ ] All 5 acceptance criteria have passing tests
- [ ] JSON always parseable (100% valid)
- [ ] Markdown heading hierarchy correct (100%)
- [ ] Code coverage >95% for formatters

### Testing
- [ ] Unit tests for JSON format (8+ test cases)
- [ ] Unit tests for text format (6+ test cases)
- [ ] Unit tests for markdown format (6+ test cases)
- [ ] Integration tests with QA skill (3+ scenarios)

### Documentation
- [ ] CLI help updated with --format option
- [ ] Output format examples in README
- [ ] JSON schema documented

---

## Workflow History

### 2025-12-20 14:30:00 - Status: Ready for Dev
- Added to SPRINT-7: Sprint 7 - AST-Grep
- Transitioned from Backlog to Ready for Dev
- Sprint capacity: 32 points
- Priority in sprint: [5 of 5]

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- Text format is default (most common use case: manual review)
- JSON includes metadata for automation and debugging
- Markdown designed to append directly to QA reports
- ANSI colors disabled when output is piped (not a TTY)

**QA Integration Points:**
- devforgeai-qa skill can append markdown directly to reports
- JSON summary enables programmatic quality gate decisions
- Severity counts used for pass/fail determination

**References:**
- [EPIC-018: ast-grep Foundation & Core Rules](../Epics/EPIC-018-astgrep-foundation-core-rules.epic.md)
- [DevForgeAI QA Report Format](../../qa/reports/README.md)

---

**Story Template Version:** 2.2
**Created:** 2025-12-20
