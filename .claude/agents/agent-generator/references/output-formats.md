# Output Format Specifications

**Purpose:** Structured output schemas for subagent results and reports.

---

## Standard Subagent Output Schema

All subagents returning structured data should use this JSON format:

```json
{
  "status": "SUCCESS|ERROR|PARTIAL",
  "result_type": "{specific_result_type}",
  "display": {
    "template": "```markdown\n[Complete user-facing markdown template]\n```",
    "title": "{Result title}",
    "summary": "{One-sentence summary}",
    "sections": [
      {
        "heading": "{Section name}",
        "content": "{Section content}"
      }
    ]
  },
  "data": {
    "{extracted_field_1}": "{value}",
    "{extracted_field_2}": "{value}",
    "metrics": {
      "{metric_name}": "{metric_value}"
    }
  },
  "validation": {
    "passes": ["{check_name}", ...],
    "warnings": [
      {"check": "{check_name}", "message": "{warning}", "suggestion": "{fix}"}
    ],
    "failures": [
      {"check": "{check_name}", "message": "{error}", "remediation": "{how_to_fix}"}
    ]
  },
  "recommendations": {
    "next_steps": ["{action_1}", "{action_2}", ...],
    "remediation": ["{fix_1}", "{fix_2}", ...],
    "priority": "HIGH|MEDIUM|LOW"
  },
  "metadata": {
    "timestamp": "{ISO_8601_timestamp}",
    "subagent": "{subagent_name}",
    "framework_version": "1.0"
  }
}
```

---

## Field Definitions

### status (REQUIRED)

| Value | Meaning |
|-------|---------|
| `SUCCESS` | Task completed successfully, all validations passed |
| `ERROR` | Task failed, cannot continue |
| `PARTIAL` | Task partially completed, some issues found |

### result_type (REQUIRED)

Specific type identifier for the result. Examples:
- `subagent_generated`
- `validation_report`
- `code_analysis`
- `qa_result`
- `deployment_status`

### display (REQUIRED)

Pre-formatted content ready for user display.

**template:** Complete markdown ready to display to user
**title:** Short title for the result
**summary:** One-sentence summary
**sections:** Array of heading/content pairs for structured display

### data (OPTIONAL)

Extracted data for programmatic use by calling skill/command.

### validation (OPTIONAL)

Validation results with categorized checks.

### recommendations (OPTIONAL)

Actionable next steps and remediation guidance.

### metadata (REQUIRED)

Execution metadata for tracing and debugging.

---

## Output Format by Subagent Type

### Generation Subagents (agent-generator, test-automator)

```json
{
  "status": "SUCCESS",
  "result_type": "generation_result",
  "display": {
    "template": "## Generated Files\n\n| File | Lines | Status |\n|------|-------|--------|\n| test-automator.md | 250 | ✅ Created |",
    "title": "Subagent Generated",
    "summary": "Successfully generated 1 subagent file",
    "sections": [
      {
        "heading": "Generated Files",
        "content": "- test-automator.md (250 lines)"
      },
      {
        "heading": "Next Steps",
        "content": "1. Restart Claude Code terminal\n2. Test invocation"
      }
    ]
  },
  "data": {
    "files_created": ["test-automator.md"],
    "total_lines": 250,
    "validation_passed": true
  },
  "recommendations": {
    "next_steps": [
      "Restart Claude Code terminal to load new subagent",
      "Test with: /agents to verify listing",
      "Test invocation with explicit command"
    ],
    "priority": "MEDIUM"
  },
  "metadata": {
    "timestamp": "2026-01-30T10:30:00Z",
    "subagent": "agent-generator",
    "framework_version": "1.0"
  }
}
```

### Validation Subagents (context-validator, coverage-analyzer)

```json
{
  "status": "PARTIAL",
  "result_type": "validation_report",
  "display": {
    "template": "## Validation Results\n\n| Check | Status | Details |\n|-------|--------|--------|\n| tech-stack.md | ✅ | Valid |\n| coverage | ⚠️ | 82% (below 85% threshold) |",
    "title": "Validation Complete",
    "summary": "Validation passed with 1 warning",
    "sections": [
      {
        "heading": "Passes",
        "content": "- tech-stack.md compliance\n- source-tree.md compliance"
      },
      {
        "heading": "Warnings",
        "content": "- Coverage 82% below 85% application layer threshold"
      }
    ]
  },
  "data": {
    "coverage": {
      "business_logic": 96,
      "application": 82,
      "infrastructure": 78
    }
  },
  "validation": {
    "passes": ["tech-stack-compliance", "source-tree-compliance", "business-logic-coverage"],
    "warnings": [
      {
        "check": "application-coverage",
        "message": "Coverage 82% below 85% threshold",
        "suggestion": "Add tests for uncovered application layer code"
      }
    ],
    "failures": []
  },
  "recommendations": {
    "remediation": [
      "Add tests for OrderService.ProcessAsync method",
      "Add tests for error handling paths"
    ],
    "priority": "MEDIUM"
  },
  "metadata": {
    "timestamp": "2026-01-30T10:30:00Z",
    "subagent": "coverage-analyzer",
    "framework_version": "1.0"
  }
}
```

### Review Subagents (code-reviewer, security-auditor)

```json
{
  "status": "ERROR",
  "result_type": "review_report",
  "display": {
    "template": "## Code Review Results\n\n### Critical Issues\n\n1. **SQL Injection vulnerability** (OrderRepository.cs:45)\n   - Query string concatenation detected\n   - Remediation: Use parameterized queries",
    "title": "Code Review: Issues Found",
    "summary": "1 critical issue, 2 warnings found",
    "sections": [
      {
        "heading": "Critical Issues",
        "content": "1. SQL Injection (OrderRepository.cs:45)"
      },
      {
        "heading": "Warnings",
        "content": "1. Missing null check (OrderService.cs:22)\n2. Unused variable (OrderController.cs:15)"
      }
    ]
  },
  "data": {
    "issues": [
      {
        "severity": "CRITICAL",
        "type": "security",
        "file": "OrderRepository.cs",
        "line": 45,
        "message": "SQL injection vulnerability"
      }
    ]
  },
  "validation": {
    "passes": ["code-style", "naming-conventions"],
    "warnings": [
      {"check": "null-safety", "message": "Missing null check", "suggestion": "Add null check before method call"}
    ],
    "failures": [
      {"check": "sql-injection", "message": "String concatenation in SQL query", "remediation": "Use parameterized queries"}
    ]
  },
  "recommendations": {
    "remediation": [
      "Replace string concatenation with parameterized query",
      "Add input validation for user-provided values"
    ],
    "priority": "HIGH"
  },
  "metadata": {
    "timestamp": "2026-01-30T10:30:00Z",
    "subagent": "security-auditor",
    "framework_version": "1.0"
  }
}
```

---

## Summary Report Format (Batch Operations)

For batch operations (e.g., generating multiple subagents):

```markdown
# Subagent Generation Report

**Generated**: 2026-01-30T10:30:00Z
**Total Subagents**: 5

## Generated Subagents

| Name | Priority | Tools | Model | Token Target | Status |
|------|----------|-------|-------|--------------|--------|
| test-automator | Critical | 5 | sonnet | < 50K | ✅ Generated |
| backend-architect | Critical | 6 | sonnet | < 50K | ✅ Generated |
| context-validator | Critical | 3 | haiku | < 10K | ✅ Generated |
| code-reviewer | High | 4 | inherit | < 30K | ✅ Generated |
| frontend-developer | Critical | 5 | sonnet | < 50K | ✅ Generated |

## Validation Results

**YAML Frontmatter:**
- ✅ All valid

**System Prompts:**
- ✅ All > 200 lines
- ✅ All sections present

**Tool Access:**
- ✅ Native tools used
- ✅ No unauthorized Bash usage

## Next Steps

1. **Restart Claude Code terminal** to load new subagents
2. **Test invocation**: `/agents` command should show all generated subagents
3. **Validate functionality**: Test explicit invocation for each subagent
4. **Integration testing**: Test with DevForgeAI skills

## File Locations

All subagents created in: `.claude/agents/`

**Critical Priority** (Days 6-7):
- test-automator.md
- backend-architect.md
- context-validator.md
- code-reviewer.md
- frontend-developer.md
```

---

## Contract Guarantees

All subagent output MUST guarantee:

- ✅ Always returns valid JSON (if structured output)
- ✅ `status` field always present (SUCCESS|ERROR|PARTIAL)
- ✅ `display.template` always present (never empty)
- ✅ All fields follow schema above
- ✅ No interpretation needed by caller (complete formatting in template)
- ✅ `metadata.timestamp` in ISO 8601 format
- ✅ `metadata.subagent` matches invoking subagent name
