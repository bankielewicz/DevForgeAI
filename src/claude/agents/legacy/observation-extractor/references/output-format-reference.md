# Observation Extractor - Output Format Reference

Observations are structured as JSON objects following this schema:

```json
{
  "observations": [
    {
      "id": "obs-{phase}-{sequence}",
      "phase": "{two_digit_phase}",
      "category": "{one_of_seven_values}",
      "note": "Description (max 200 chars, truncate with ...)",
      "severity": "{low|medium|high}",
      "files": ["path/to/file.py"],
      "source_subagent": "{subagent_name}",
      "extraction_rule": "{rule_name}"
    }
  ]
}
```

**ID Format Example:**
- `obs-02-001` - First observation from Phase 02
- `obs-04-015` - Fifteenth observation from Phase 04

**Category Values (7 approved):**
- `friction` - Pain points, blockers, difficulties
- `success` - What worked well
- `pattern` - Architecture/design patterns observed
- `gap` - Missing coverage, unmet requirements
- `idea` - Improvement suggestions
- `bug` - Bugs discovered
- `warning` - Non-blocking concerns

**Severity Values (3 approved):**
- `low` - Minor, can be addressed later
- `medium` - Should be addressed soon
- `high` - Requires immediate attention

**Note Truncation Example:**
- Input (250 chars): "Very long description that exceeds the maximum length and needs to be shortened..."
- Output (200 chars max): "Very long description that exceeds the maximum length and needs to be..."
