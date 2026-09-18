# QA Result Interpreter -- Examples

Reference content extracted from the core agent definition. Loaded on-demand for invocation patterns.

---

## Example 1: Interpret Deep Mode Pass Report

```
Task(
  subagent_type="qa-result-interpreter",
  description="Interpret QA results for STORY-567",
  prompt="Interpret QA validation results for STORY-567. QA report path: devforgeai/qa/reports/STORY-567-qa-report.md. Validation mode: deep. Story status: Dev Complete. Parse report and generate user-friendly display template with approval recommendation."
)
```

## Example 2: Interpret Deep Mode Fail with Multiple Violations

```
Task(
  subagent_type="qa-result-interpreter",
  description="Interpret QA failure report for STORY-890",
  prompt="Interpret QA validation failure for STORY-890. QA report: devforgeai/qa/reports/STORY-890-qa-report.md. Mode: deep. Result contains coverage gaps and anti-pattern violations. Generate remediation guidance and recommend workflow (return to dev or systematic analysis). Return structured JSON with display template."
)
```
