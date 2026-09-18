---
name: srfd-format
description: Structured Recommendation Feedback Document (SRFD) format specification for DevForgeAI feedback system
version: "1.0.0"
---

# SRFD Format Specification

Defines the canonical structure, validation rules, and index template for Structured Recommendation Feedback Documents (SRFDs).

## Section Structure

Each SRFD document contains the following sections in order:

| Section | Status | Description |
|---------|--------|-------------|
| Session Summary | Required | Overview of the workflow session that produced this SRFD |
| Metadata | Required | Story ID, workflow type, date, epic, sprint, and analysis metadata |
| Constraint Analysis | Required | Analysis of context file constraint effectiveness during the workflow |
| Recommendations | Required | Actionable framework improvement recommendations with affected files |
| Patterns Observed | Optional | Recurring positive patterns identified during the workflow |
| Anti-Patterns Detected | Optional | Framework anti-patterns encountered during the workflow |

### Session Summary (Required)

Provide a brief overview of the completed workflow session:
- Story ID and workflow type (dev/qa)
- Duration and phase count
- Observation count processed

### Metadata (Required)

Structured metadata fields for indexing and search:
- story_id: The STORY-NNN identifier
- workflow_type: "dev" or "qa"
- analysis_date: ISO8601 timestamp
- epic: Parent epic identifier (from story YAML frontmatter)
- sprint: Sprint identifier (from story YAML frontmatter)
- observations_processed: Count of observations analyzed

### Constraint Analysis (Required)

Describe how the 6 context files (devforgeai/specs/context/) influenced the workflow:
- Which constraints prevented violations
- Which constraints caused friction
- Effectiveness assessment per context file

### Recommendations (Required)

Each recommendation must include:
- title: Action verb + target
- description: Specific, non-aspirational guidance
- affected_files: Array of concrete file paths
- implementation_code: Steps or code to implement
- effort_estimate: "15 min", "30 min", "1 hour", "2 hours", or "4 hours"
- priority: HIGH, MEDIUM, or LOW

### Patterns Observed (Optional)

List recurring positive patterns that worked well during the workflow.

### Anti-Patterns Detected (Optional)

List any anti-patterns encountered, with file:line references.

---

## Validation Rules

The following validation rules enforce SRFD document integrity:

1. All required sections must be present in the document
2. Each mandatory field must be populated (not empty or placeholder)
3. Recommendations must not contain aspirational language ("could", "might", "consider")
4. All affected_files entries must be specific paths (not globs)
5. effort_estimate must use a valid format string
6. The metadata section must contain story_id and analysis_date fields
7. Constraint analysis must reference at least one context file

---

## SRFD Index Template

The srfd-index.json file tracks all generated SRFD documents. If srfd-index.json does not exist, create it from this template:

```json
{
  "schema_version": "1.0.0",
  "description": "SRFD index tracking all generated Structured Recommendation Feedback Documents",
  "entries": []
}
```

Each entry in the `"entries"` array must contain:

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique SRFD identifier (e.g., "SRFD-STORY-234-2026-04-08") |
| path | string | Relative path to the SRFD file |
| source_story | string | Story ID that generated this SRFD |
| workflow | string | Workflow type ("dev" or "qa") |
| generated | string | ISO8601 date when the SRFD was generated |
| recommendation_count | integer | Total recommendations in the SRFD |
| open_count | integer | Recommendations not yet implemented |
| implemented_count | integer | Recommendations already implemented |
