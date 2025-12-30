---
name: create-stories-from-rca
description: Parse RCA documents and extract recommendations for story creation. Filters by effort threshold and sorts by priority.
---

# /create-stories-from-rca - RCA Document Parser

Parse RCA markdown files and extract structured recommendation data with priority levels, effort estimates, and success criteria.

---

## Constants and Enums

```
# Priority/Severity levels (shared between RCA document and recommendations)
VALID_PRIORITIES = [CRITICAL, HIGH, MEDIUM, LOW]
PRIORITY_ORDER = {CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3}
DEFAULT_PRIORITY = "MEDIUM"

# RCA Status values
VALID_STATUSES = [OPEN, IN_PROGRESS, RESOLVED]
DEFAULT_STATUS = "OPEN"

# Business rule: Story point to hours conversion (BR-003)
STORY_POINTS_TO_HOURS = 4
```

---

## Reusable Helpers

**Helper: validate_enum(value, valid_values, default, field_name, context)**
```
# Generic enum validation with warning on invalid values
IF value NOT IN valid_values:
    Display: "Warning: Invalid ${field_name} '${value}'${context}, defaulting to ${default}"
    RETURN default
RETURN value
```

---

## Usage

```bash
/create-stories-from-rca RCA-NNN [--threshold HOURS]

# Examples:
/create-stories-from-rca RCA-022
/create-stories-from-rca RCA-022 --threshold 2
```

---

## Argument Parsing

```
RCA_ID = null
EFFORT_THRESHOLD = 0  # Default: include all recommendations

FOR arg in arguments:
    IF arg matches "RCA-[0-9]+":
        RCA_ID = arg
    ELIF arg == "--threshold":
        NEXT_IS_THRESHOLD = true
    ELIF NEXT_IS_THRESHOLD:
        EFFORT_THRESHOLD = parse_int(arg)
        NEXT_IS_THRESHOLD = false

IF RCA_ID empty:
    Display: "Usage: /create-stories-from-rca RCA-NNN [--threshold HOURS]"
    Display: "Example: /create-stories-from-rca RCA-022 --threshold 2"
    HALT
```

---

## Phase 1: Locate RCA File (Prerequisite)

```
# Find RCA file matching ID
Glob(pattern="devforgeai/RCA/${RCA_ID}*.md")

IF no files found:
    Display: "RCA not found: ${RCA_ID}"
    Display: "Available RCAs:"
    Glob(pattern="devforgeai/RCA/RCA-*.md")
    HALT

RCA_FILE = first matching file
Display: "Parsing: ${RCA_FILE}"
```

---

## Phase 2: Parse Frontmatter (AC#1)

```
# Read RCA file content
Read(file_path="${RCA_FILE}")

# Extract YAML frontmatter between --- markers
FRONTMATTER_PATTERN = content between first "---" and second "---"

# Parse required fields
rca_document = {
    id: extract_field("id"),           # Format: RCA-NNN
    title: extract_field("title"),
    date: extract_field("date"),       # Format: YYYY-MM-DD
    severity: extract_field("severity"), # Enum: CRITICAL|HIGH|MEDIUM|LOW
    status: extract_field("status"),   # Enum: OPEN|IN_PROGRESS|RESOLVED
    reporter: extract_field("reporter"),
    recommendations: []
}

# Validate enums using reusable helper
rca_document.severity = validate_enum(severity, VALID_PRIORITIES, DEFAULT_PRIORITY, "severity", "")
rca_document.status = validate_enum(status, VALID_STATUSES, DEFAULT_STATUS, "status", "")

# Edge case: Missing frontmatter
IF no frontmatter found:
    Display: "Warning: No frontmatter found, extracting ID from filename"
    rca_document.id = extract_id_from_filename(RCA_FILE)
```

**Helper: extract_field(field_name)**
```
# Pattern: "field_name: value" or "field_name: 'value'"
Grep(pattern="^${field_name}:", path="${RCA_FILE}")
RETURN value after colon, trimmed
```

---

## Phase 3: Extract Recommendations (AC#2, AC#3, AC#4)

```
# Find all recommendation sections: ### REC-N: PRIORITY - Title
Grep(pattern="^### REC-[0-9]+:", path="${RCA_FILE}", output_mode="content")

FOR each recommendation_header in matches:
    # Parse header: ### REC-1: HIGH - Fix Database Connection
    rec = {
        id: extract "REC-N" from header,
        priority: extract priority (CRITICAL|HIGH|MEDIUM|LOW),
        title: extract title after " - ",
        description: "",
        effort_hours: null,
        effort_points: null,
        success_criteria: []
    }

    # Validate priority using reusable helper
    rec.priority = validate_enum(priority, VALID_PRIORITIES, DEFAULT_PRIORITY, "priority", " for ${rec.id}")

    # Extract description (content between this header and next ### or end)
    rec.description = extract_section_content(rec.id)

    # Extract effort estimate (AC#3)
    effort_line = Grep(pattern="\\*\\*Effort Estimate:\\*\\*", section_content)
    IF effort_line found:
        IF contains "hours":
            rec.effort_hours = parse_int(hours_value)
        ELIF contains "story points" OR contains "points":
            rec.effort_points = parse_int(points_value)
            # BR-003: Convert story points to hours using constant
            rec.effort_hours = rec.effort_points * STORY_POINTS_TO_HOURS

    # Extract success criteria (AC#4)
    IF section contains "**Success Criteria:**":
        criteria_section = content after "**Success Criteria:**" until next "**" or "###"
        FOR each line matching "- [ ]" OR "- [x]" pattern:
            rec.success_criteria.append(checkbox_text)

    rca_document.recommendations.append(rec)

Display: "Found ${rca_document.recommendations.length} recommendations"
```

---

## Phase 4: Filter and Sort (AC#5)

```
# BR-001: Filter by effort threshold
IF EFFORT_THRESHOLD > 0:
    filtered_recommendations = []
    FOR rec in rca_document.recommendations:
        IF rec.effort_hours >= EFFORT_THRESHOLD:
            filtered_recommendations.append(rec)
        ELSE:
            Display: "Filtered out: ${rec.id} (effort: ${rec.effort_hours}h < threshold: ${EFFORT_THRESHOLD}h)"

    rca_document.recommendations = filtered_recommendations

# BR-002: Sort by priority using PRIORITY_ORDER constant
rca_document.recommendations.sort(key=lambda r: PRIORITY_ORDER[r.priority])

Display: "After filtering: ${rca_document.recommendations.length} recommendations"
```

---

## Phase 5: Display Results

```
Display: ""
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: "  RCA Document: ${rca_document.id}"
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: ""
Display: "**Title:** ${rca_document.title}"
Display: "**Date:** ${rca_document.date}"
Display: "**Severity:** ${rca_document.severity}"
Display: "**Status:** ${rca_document.status}"
Display: "**Reporter:** ${rca_document.reporter}"
Display: ""

IF rca_document.recommendations.length == 0:
    Display: "No recommendations found (or all filtered out)."
ELSE:
    Display: "## Recommendations (${rca_document.recommendations.length})"
    Display: ""

    FOR rec in rca_document.recommendations:
        Display: "### ${rec.id}: ${rec.priority} - ${rec.title}"
        Display: ""
        Display: "${rec.description}"
        Display: ""

        IF rec.effort_hours:
            Display: "**Effort:** ${rec.effort_hours} hours"
            IF rec.effort_points:
                Display: " (${rec.effort_points} story points)"

        IF rec.success_criteria.length > 0:
            Display: ""
            Display: "**Success Criteria:**"
            FOR criterion in rec.success_criteria:
                Display: "- [ ] ${criterion}"

        Display: ""
        Display: "---"
        Display: ""

Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

---

## Return Value

```json
{
  "rca_document": {
    "id": "RCA-NNN",
    "title": "string",
    "date": "YYYY-MM-DD",
    "severity": "CRITICAL|HIGH|MEDIUM|LOW",
    "status": "OPEN|IN_PROGRESS|RESOLVED",
    "reporter": "string",
    "recommendations": [
      {
        "id": "REC-N",
        "priority": "CRITICAL|HIGH|MEDIUM|LOW",
        "title": "string",
        "description": "string",
        "effort_hours": "integer|null",
        "effort_points": "integer|null",
        "success_criteria": ["string"]
      }
    ]
  },
  "filter_applied": "boolean",
  "threshold_hours": "integer",
  "recommendations_count": "integer"
}
```

---

## Edge Cases Handled

| Edge Case | Behavior |
|-----------|----------|
| Missing frontmatter | Extract ID from filename, log warning |
| No recommendations | Return empty array, display message |
| Missing effort estimate | Return null for effort_hours |
| Malformed priority | Default to MEDIUM, log warning |
| Malformed severity | Default to MEDIUM, log warning |
| Malformed status | Default to OPEN, log warning |
| Story points format | Convert to hours (1 point = 4 hours) per BR-003 |
| All filtered out | Return empty array, display filter message |

---

## Business Rules

| Rule | Implementation |
|------|----------------|
| BR-001: Effort Threshold | Filter where effort_hours >= threshold |
| BR-002: Priority Sorting | CRITICAL(0) > HIGH(1) > MEDIUM(2) > LOW(3) |
| BR-003: Story Point Conversion | 1 story point = 4 hours |

---

## Non-Functional Requirements

| Requirement | Implementation |
|-------------|----------------|
| Performance <500ms | Single file read, in-memory parsing |
| Zero external deps | Uses only Read, Glob, Grep (Claude Code native) |
| Graceful degradation | Warnings for malformed data, no exceptions |
| Read-only | No file modifications, display only |
