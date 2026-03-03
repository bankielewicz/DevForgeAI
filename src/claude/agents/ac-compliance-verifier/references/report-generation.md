# Report Generation

**Purpose:** Generate structured verification reports in JSON format.

---

## Verification Report Format

Output verification report in this format:

```json
{
  "story_id": "STORY-XXX",
  "verification_timestamp": "2026-01-19T12:00:00Z",
  "verifier": "ac-compliance-verifier",
  "technique": "fresh-context",
  "results": {
    "total_acs": 5,
    "passed": 4,
    "failed": 1,
    "skipped": 0
  },
  "details": [
    {
      "ac_id": "AC1",
      "title": "AC Title",
      "status": "PASS",
      "evidence": {
        "file": "path/to/file.md",
        "lines": "10-25",
        "snippet": "relevant code snippet"
      },
      "notes": "Verification notes"
    }
  ],
  "overall_status": "PARTIAL",
  "blocking_failures": ["AC3"],
  "recommendations": ["Fix AC3 before proceeding to QA"]
}
```

---

## Report Field Specifications

### Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `story_id` | String | **Yes** | Story identifier (e.g., "STORY-269") |
| `verification_timestamp` | ISO8601 | **Yes** | When verification was performed |
| `verifier` | String | **Yes** | Always "ac-compliance-verifier" |
| `technique` | String | **Yes** | Always "fresh-context" |
| `results` | Object | **Yes** | Summary statistics |
| `details` | Array | **Yes** | Per-AC verification details |
| `overall_status` | Enum | **Yes** | PASS, PARTIAL, or FAIL |
| `blocking_failures` | Array<String> | No | AC IDs that failed |
| `recommendations` | Array<String> | No | Remediation suggestions |

### Results Object

| Field | Type | Description |
|-------|------|-------------|
| `total_acs` | Integer | Total ACs in story |
| `passed` | Integer | ACs that passed verification |
| `failed` | Integer | ACs that failed verification |
| `skipped` | Integer | ACs that couldn't be verified |

### Details Array Entry

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ac_id` | String | **Yes** | AC identifier (e.g., "AC1") |
| `title` | String | No | AC title/description |
| `status` | Enum | **Yes** | PASS, FAIL, or BLOCKED |
| `evidence` | Object | No | Supporting evidence |
| `notes` | String | No | Verification notes |

### Evidence Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | String | **Yes** | File path where evidence found |
| `lines` | String | No | Line range (e.g., "10-25") |
| `snippet` | String | No | Code excerpt (max 500 chars) |

---

## Overall Status Determination

| Status | Condition |
|--------|-----------|
| `PASS` | All ACs passed |
| `PARTIAL` | Some ACs passed, some failed |
| `FAIL` | All ACs failed or critical blocker found |

---

## Anti-Pattern Detection Report

When anti-pattern violations are found, include in report:

```json
{
  "ac_id": "AC1",
  "verification_status": "PASS",
  "anti_pattern_scan": {
    "enabled": true,
    "violations_found": 2,
    "blocking_violations": 1,
    "status": "FLAGGED",
    "violations": [
      {
        "category": "Tool Usage Violations",
        "severity": "CRITICAL",
        "file_path": "src/utils/file_helper.py",
        "line_number": 45,
        "description": "Using Bash for file read operation"
      },
      {
        "category": "Narrative Documentation",
        "severity": "MEDIUM",
        "file_path": ".claude/skills/custom-skill/SKILL.md",
        "line_number": 120,
        "description": "Prose detected: 'should first consider'"
      }
    ]
  }
}
```

---

## Tool Restrictions (READ-ONLY)

**Allowed tools:**
- `Read` - Read file contents
- `Grep` - Search for patterns
- `Glob` - Find files by pattern

**NOT allowed (enforced by tool list):**
- Write - Cannot create files
- Edit - Cannot modify files
- Bash - Cannot execute commands
- WebFetch - Cannot access network
- WebSearch - Cannot search internet

**Rationale:** Verification must be read-only to ensure it cannot accidentally modify or "fix" issues it finds. All findings must be reported, not auto-corrected.

---

## Response Constraints

- Limit response to 1000 words maximum
- Use structured JSON for verification results
- Include file paths and line numbers as evidence
- No code snippets longer than 10 lines
- Focus on verification, not explanation

---

## Integration Points

**Invoked by:**
- implementing-stories skill (Phase 4.5, Phase 5.5)
- devforgeai-qa skill (deep validation mode)
- Manual invocation for verification

**Reports to:**
- Story file (verification checklist update)
- QA reports directory
- Phase state tracking

---

## Example Invocation

```
Task(
  subagent_type="ac-compliance-verifier",
  description="Verify ACs for STORY-269",
  prompt="Verify all acceptance criteria for STORY-269 using fresh-context technique. Report PASS/FAIL for each AC with evidence."
)
```

---

**Version:** 1.0
**Extracted from:** ac-compliance-verifier.md (STORY-334)
