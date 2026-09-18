# QA Result Interpreter -- Output Schema

Reference content extracted from the core agent definition. Loaded during Step 8 (Return Structured Result).

---

## Structured Result Schema

```json
{
  "status": "PASSED|FAILED",
  "mode": "light|deep",
  "story_id": "STORY-XXX",
  "timestamp": "2025-11-05T14:30:00Z",

  "summary": {
    "title": "✅ Deep QA Validation PASSED",
    "body": "Story meets all quality gates and is ready for release.",
    "violations_total": 0,
    "violations_by_severity": {
      "CRITICAL": 0,
      "HIGH": 0,
      "MEDIUM": 0,
      "LOW": 0
    }
  },

  "display": {
    "template": "deep_pass_full",
    "content": "... full markdown template from Step 5 ...",
    "sections": [
      {
        "title": "Validation Results",
        "subsections": ["Test Coverage", "Code Quality", "Violations", "Spec Compliance"]
      },
      {
        "title": "Recommendation",
        "content": "✅ **APPROVE**"
      }
    ]
  },

  "remediation": {
    "violations": [
      {
        "severity": "CRITICAL",
        "type": "coverage",
        "description": "Business logic coverage below 95%",
        "fix_steps": ["Add unit tests...", "Run validation..."],
        "estimated_effort": "30 minutes"
      }
    ],
    "total_violations": 1,
    "workflow_recommendation": "return_to_dev | fix_manually | proceed_to_release"
  },

  "next_steps": [
    "Review detailed report: devforgeai/qa/reports/{STORY_ID}-qa-report.md",
    "Deploy: `/release {STORY_ID}`"
  ],

  "qa_attempt_info": {
    "attempt_number": 1,
    "previous_attempts": 0,
    "warnings": []
  },

  "gap_remediation": {
    "gap_file_generated": true,
    "gap_file_path": "devforgeai/qa/reports/{STORY_ID}-gaps.json",
    "remediation_command": "/review-qa-reports --source local",
    "recommendation": "systematic_analysis | manual_fix | none",
    "trigger_reason": "total_violations > 2 OR coverage_gaps present"
  }
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Overall result: PASSED, FAILED, or PASS_WITH_WARNINGS |
| `mode` | string | Validation mode: light or deep |
| `story_id` | string | Story identifier (e.g., STORY-567) |
| `timestamp` | string | ISO 8601 UTC timestamp of interpretation |
| `summary.title` | string | Human-readable title with status emoji |
| `summary.body` | string | One-sentence result summary |
| `summary.violations_total` | integer | Total count of all violations |
| `summary.violations_by_severity` | object | Violation count broken down by CRITICAL/HIGH/MEDIUM/LOW |
| `display.template` | string | Name of the selected display template |
| `display.content` | string | Full populated markdown template |
| `display.sections` | array | Top-level template sections for navigation |
| `remediation.violations` | array | Ordered list of violations with fix steps |
| `remediation.total_violations` | integer | Total violations requiring remediation |
| `remediation.workflow_recommendation` | string | Recommended workflow action |
| `next_steps` | array | Ordered list of recommended next actions |
| `qa_attempt_info.attempt_number` | integer | Current QA attempt number |
| `qa_attempt_info.previous_attempts` | integer | Count of prior QA attempts |
| `gap_remediation.gap_file_generated` | boolean | Whether a gaps.json file was generated |
| `gap_remediation.gap_file_path` | string | Path to gaps.json if generated |
| `gap_remediation.remediation_command` | string | CLI command for systematic remediation |
| `gap_remediation.recommendation` | string | Remediation strategy recommendation |
