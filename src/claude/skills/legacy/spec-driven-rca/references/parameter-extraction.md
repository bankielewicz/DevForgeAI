# Parameter Extraction Reference

**Purpose:** Context marker extraction algorithm for both tactical and strategic modes.

---

## Tactical Mode Parameters

Tactical mode is triggered by the dev workflow (spec-driven-dev, spec-driven-qa) when fix attempts fail.

### Context Markers (set by dev workflow)

| Marker | Source | Required | Format |
|--------|--------|----------|--------|
| `**Mode:** tactical` | Dev workflow | Yes | Literal string |
| `**Story ID:** STORY-NNN` | Dev workflow | Yes | STORY-{3+ digits} |
| `**Error:** {text}` | Dev workflow | Yes | Error message text |
| `**Fix Attempts:** {N}` | Dev workflow | Yes | Integer >= 2 |
| `**Phase:** {name}` | Dev workflow | Yes | Green, Integration, or QA |
| `**Failing File:** {path}` | Dev workflow | No | Absolute file path |
| `**Failing Function:** {name}` | Dev workflow | No | Function or test name |

### Extraction Algorithm (Tactical)

```
1. Search conversation for "**Mode:** tactical"
   IF found: MODE = "tactical"

2. Search for "**Story ID:**" or pattern STORY-\d{3,}
   STORY_ID = extracted value
   IF not found: Search for devforgeai/workflows/*-phase-state.json

3. Search for "**Error:**" marker or most recent error output
   ERROR_MESSAGE = extracted text (full, not summarized)

4. Search for "**Fix Attempts:**" marker
   FIX_ATTEMPTS = extracted integer
   IF not found: Count consecutive fix attempts in conversation

5. Search for "**Phase:**" marker
   WORKFLOW_PHASE = extracted value (Green | Integration | QA)

6. Search for "**Failing File:**" marker
   FAILING_FILE = extracted path
   IF not found: Extract from error output stack trace

7. Search for "**Failing Function:**" marker
   FAILING_FUNCTION = extracted name
   IF not found: Extract from test output
```

### Missing Parameter Handling (Tactical)

| Parameter | If Missing | Recovery |
|-----------|-----------|----------|
| STORY_ID | Search for active phase-state.json | HALT if no active story found |
| ERROR_MESSAGE | Look for recent test output | HALT — cannot diagnose without error |
| FIX_ATTEMPTS | Count from conversation | Default to 3 |
| WORKFLOW_PHASE | Infer from context | Default to "Green" |
| FAILING_FILE | Extract from stack trace | Note as "unknown" |
| FAILING_FUNCTION | Extract from test output | Note as "unknown" |

---

## Strategic Mode Parameters

Strategic mode is triggered by the `/rca` command.

### Context Markers (set by /rca command)

| Marker | Source | Required | Format |
|--------|--------|----------|--------|
| `**Issue Description:** {text}` | /rca command | Yes | Issue description text |
| `**Severity:** {level}` | /rca command | No | CRITICAL, HIGH, MEDIUM, LOW, or "infer" |
| `**Command:** rca` | /rca command | No | Literal string |
| `**Mode:** strategic` | /rca command | No | Literal string (default if no mode marker) |

### Extraction Algorithm (Strategic)

```
1. Search conversation for "**Mode:** strategic" or "**Command:** rca"
   IF found: MODE = "strategic"
   ELSE IF no tactical markers: MODE = "strategic" (default)

2. Search for "**Issue Description:**" marker
   ISSUE_DESCRIPTION = extracted text
   IF not found: Search for recent user message describing a breakdown

3. Search for "**Severity:**" marker
   SEVERITY = extracted value
   IF not found or "infer": Infer from keywords

4. Infer AFFECTED_COMPONENT from issue description:
   - Skill name pattern (e.g., "spec-driven-dev") -> component_type = "Skill"
   - Command pattern (e.g., "/dev", "/qa") -> component_type = "Command"
   - Subagent pattern (e.g., "diagnostic-analyst") -> component_type = "Subagent"
   - Context file pattern (e.g., "tech-stack.md") -> component_type = "Context File"
   - Workflow pattern (e.g., "story state", "quality gate") -> component_type = "Workflow"
```

### Missing Parameter Handling (Strategic)

| Parameter | If Missing | Recovery |
|-----------|-----------|----------|
| ISSUE_DESCRIPTION | AskUserQuestion with common breakdown options | HALT if user cancels |
| SEVERITY | Infer from keywords in issue description | Default to MEDIUM |
| AFFECTED_COMPONENT | AskUserQuestion to identify component type | Default to "Workflow" |

### Severity Inference Keywords

| Keywords | Severity |
|----------|----------|
| "broken", "blocking", "data loss", "cannot work" | CRITICAL |
| "failed", "violation", "bypass", "incorrect" | HIGH |
| "improvement", "gap", "unclear", "inconsistent" | MEDIUM |
| "minor", "cosmetic", "typo", "suggestion" | LOW |

---

## Mode Detection Priority

When both tactical and strategic markers are present (edge case):

```
1. Explicit "**Mode:**" marker takes highest priority
2. "**Fix Attempts:**" marker indicates tactical (dev workflow context)
3. "**Issue Description:**" without "**Fix Attempts:**" indicates strategic
4. "**Command:** rca" indicates strategic
5. No markers: AskUserQuestion to disambiguate
```
