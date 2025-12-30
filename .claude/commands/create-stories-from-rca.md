---
name: create-stories-from-rca
description: Parse RCA documents and extract recommendations for story creation. Filters by effort threshold and sorts by priority.
---

# /create-stories-from-rca - RCA Document Parser

Parse RCA markdown files, extract structured recommendation data, and interactively select which recommendations to convert to user stories.

**Interactive Selection Flow:**
1. Parse RCA document and extract recommendations (Phases 1-4)
2. Display recommendation summary table with REC ID, Priority, Title, Effort (Phase 6)
3. Prompt user to select recommendations using multiSelect (Phase 7)
4. Handle selection: All, Individual, or Cancel (Phase 8)
5. Pass selected recommendations to batch story creation (Phase 9)

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

**Helper: format_effort_estimate(effort_hours)**
```
# Reusable effort formatting - returns "Nh" or "N/A"
RETURN "${effort_hours}h" IF effort_hours ELSE "N/A"
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

## Phase 6: Display Recommendation Summary Table (AC#1)

```
# function display_recommendation_table($1 = rca_document.recommendations)
# Display formatted table (readable in 80-char terminal)
# Uses printf-style padding for align column width formatting
IF rca_document.recommendations.length > 0:
    Display: ""
    Display: "┌─────────┬──────────┬────────────────────────────────────┬────────┐"
    Display: "│ REC ID  │ Priority │ Title                              │ Effort │"
    Display: "├─────────┼──────────┼────────────────────────────────────┼────────┤"

    FOR rec in rca_document.recommendations:
        # Truncate title to fit 34 chars
        display_title = rec.title[:34] IF len(rec.title) > 34 ELSE rec.title.ljust(34)
        effort_str = format_effort_estimate(rec.effort_hours)
        Display: "│ ${rec.id.ljust(7)} │ ${rec.priority.ljust(8)} │ ${display_title} │ ${effort_str.rjust(6)} │"

    Display: "└─────────┴──────────┴────────────────────────────────────┴────────┘"
    Display: ""
```

---

## Phase 7: Interactive Selection (AC#2, AC#3, AC#4)

```
# function prompt_user_for_selection($1 = recommendations_array)
# Integrates with STORY-155 RCA parser output format
# Returns selected_options after user selection

# Edge case: No recommendations after filtering
IF rca_document.recommendations.length == 0:
    Display: "No recommendations meet effort threshold. Exiting."
    HALT

# Build options array for AskUserQuestion
options = []

# Add "All recommendations" option first (recommended)
options.append({
    label: "All recommendations (Recommended)",
    description: "Create stories for all ${rca_document.recommendations.length} eligible recommendations"
})

# Add individual recommendation options
FOR rec in rca_document.recommendations:
    effort_str = format_effort_estimate(rec.effort_hours)
    options.append({
        label: "${rec.id}: ${rec.title[:30]}",
        description: "Priority: ${rec.priority}, Effort: ${effort_str}"
    })

# Add "None - cancel" option last
options.append({
    label: "None - cancel",
    description: "Exit without creating stories"
})

# Prompt user with multiSelect: true
AskUserQuestion(
    questions=[{
        question: "Which recommendations should be converted to stories?",
        header: "Select",
        multiSelect: true,
        options: options
    }]
)

# Capture user selection
# echo selected_recs, return selection for downstream
user_selection = captured from AskUserQuestion response
```

---

## Phase 8: Handle Selection

```
selected_recommendations = []

# Handle "None - cancel" option - exit gracefully without creating stories
# if "None" or if cancel detected: return early, skip creation, prevents downstream
# echo "No recommendations" message printed before exit (no cleanup required)
IF user_selection contains "None - cancel":
    Display: "No recommendations selected. Exiting."
    return 0  # exit 0 gracefully
    HALT

# Handle "All recommendations" option - Handles "All" selection
# Excludes ineligible recommendations (already filtered in Phase 4)
# if All = true: selected_recommendations = all eligible
IF user_selection contains "All recommendations":
    selected_recommendations = rca_document.recommendations  # All = selected
    Display: "Selected all ${selected_recommendations.length} recommendations"

# Handle individual selections
ELSE:
    FOR selection in user_selection:
        # Extract REC ID from selection label
        IF selection matches "REC-[0-9]+":
            rec_id = extract REC ID
            rec = find_recommendation_by_id(rec_id)
            IF rec:
                selected_recommendations.append(rec)
            ELSE:
                Display: "Warning: Invalid REC ID '${rec_id}', ignoring"

    # Handle "Other" (custom comma-separated input)
    IF user_selection contains custom text:
        custom_ids = parse comma-separated REC IDs
        FOR rec_id in custom_ids:
            rec = find_recommendation_by_id(rec_id)
            IF rec:
                selected_recommendations.append(rec)
            ELSE:
                Display: "Warning: Invalid REC ID '${rec_id}', ignoring"

# Validate minimum selection (BR-001)
IF selected_recommendations.length == 0:
    Display: "No valid recommendations selected. Please try again."
    GOTO Phase 7  # Re-prompt

Display: "Selected ${selected_recommendations.length} recommendation(s) for story creation"
```

---

## Phase 9: Pass to Batch Story Creation (AC#5)

```
# Selected recommendations passed to next phase - pass selection forward
# No data loss in transformation - all fields complete and intact
# Output format compatible with batch creation - expected format for batch
# Preserve all metadata for batch creation (BR-002)
batch_input = {
    rca_document: {
        id: rca_document.id,
        title: rca_document.title,
        severity: rca_document.severity
    },
    selected_recommendations: selected_recommendations,
    selection_count: selected_recommendations.length
}

# Each recommendation preserves full metadata:
# - id (REC-N)
# - priority (CRITICAL|HIGH|MEDIUM|LOW)
# - title (string)
# - description (string)
# - effort_hours (integer|null)
# - effort_points (integer|null)
# - success_criteria (array)

Display: ""
Display: "Proceeding to batch story creation with ${selection_count} recommendation(s)..."
Display: ""

# Return batch_input for next phase (batch story creation)
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
  "recommendations_count": "integer",
  "selected_recommendations": [
    {
      "id": "REC-N",
      "priority": "CRITICAL|HIGH|MEDIUM|LOW",
      "title": "string",
      "description": "string",
      "effort_hours": "integer|null",
      "effort_points": "integer|null",
      "success_criteria": ["string"]
    }
  ],
  "selection_count": "integer",
  "selection_mode": "all|individual|cancel"
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
| Single recommendation | Still display selection prompt (allow cancel) |
| No recommendations after filter | Display "No recommendations meet effort threshold" and exit |
| User selects "Other" | Parse comma-separated REC IDs from custom input |
| Invalid REC ID in selection | Log warning and ignore invalid entries |

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
