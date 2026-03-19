# Report Update Protocol

**Phase:** 06 (Source Report Update)
**Skill:** spec-driven-qa-remediation
**Purpose:** Update gap files with story references and generate enhancement report.

---

## Part 1: Gap File Updates

### Step 1: Identify Local vs Imported Files

```
LOCAL_PATH = "devforgeai/qa/reports/"
IMPORTS_PATH = "devforgeai/qa/imports/"

for each story in $CREATED_STORIES:
    if story.source_file.startswith(LOCAL_PATH):
        update_gap_file(story)
    else:
        // Imported files are read-only
        log_info("Skipping update for imported file: {story.source_file}")
```

### Step 2: Update Gap JSON

For each successfully created story linked to a local gap file:

```
1. Read the gap file:
   content = Read(file_path="{source_file}")
   gap_data = JSON.parse(content)

2. Find the gap entry:
   gap_array = gap_data[story.gap_type]  // e.g., "coverage_gaps"
   gap_entry = gap_array[story.source_index]

3. Add implemented_in field:
   gap_entry["implemented_in"] = story.story_id
   gap_entry["remediation_date"] = current_date()

4. Write updated file:
   Edit(file_path="{source_file}",
        old_string=original_gap_json,
        new_string=updated_gap_json)
```

### Step 3: Updated Gap Entry Format

**Before:**
```json
{
  "file": "src/module/file.py",
  "layer": "Business Logic",
  "current_coverage": 85.0,
  "target_coverage": 95.0
}
```

**After:**
```json
{
  "file": "src/module/file.py",
  "layer": "Business Logic",
  "current_coverage": 85.0,
  "target_coverage": 95.0,
  "implemented_in": "STORY-123",
  "remediation_date": "2026-01-15"
}
```

---

## Part 2: Enhancement Report Generation

### Step 1: Determine Report Path

```
date = current_date()  // Format: YYYY-MM-DD
report_path = "devforgeai/qa/enhancement-reports/{date}-enhancement-report.md"

// If multiple runs same day, append sequence
if file_exists(report_path):
    report_path = "devforgeai/qa/enhancement-reports/{date}-enhancement-report-{seq}.md"
```

### Step 2: Generate Report Content

Use template from `.claude/skills/spec-driven-qa-remediation/assets/templates/enhancement-report-template.md`:

Fill variables:
- `{DATE}` -> current date
- `{FILES_PROCESSED}` -> $FILES_PROCESSED
- `{TOTAL_GAPS}` -> $TOTAL_GAPS
- `{GAPS_DEDUPLICATED}` -> $GAPS_DEDUPLICATED
- `{GAPS_ABOVE_THRESHOLD}` -> $GAPS_ABOVE_THRESHOLD
- `{SELECTION_COUNT}` -> len($SELECTED_GAPS)
- `{STORIES_CREATED}` -> len($CREATED_STORIES)
- `{STORIES_FAILED}` -> len($FAILED_STORIES)
- `{GAPS_DEFERRED}` -> len($DEFERRED_GAPS)
- `{SOURCE}` -> $SOURCE
- `{MIN_SEVERITY}` -> $MIN_SEVERITY
- `{EPIC_ID}` -> $EPIC_ID or "None"
- `{CREATED_STORIES_TABLE}` -> generated table rows
- `{FAILED_STORIES_SECTION}` -> generated section
- `{DEFERRED_GAPS_SECTION}` -> generated section
- `{UPDATED_FILES_SECTION}` -> generated section

### Step 3: Write Report

```
Write(file_path=report_path, content=report_content)
```

---

## Part 3: Hook Invocation (Optional)

### Check for Hook

If `post-qa-remediation` hook is configured in `devforgeai/config/hooks.yaml`:

```yaml
post-qa-remediation:
  enabled: true
  trigger: "after_phase_06"
  actions:
    - type: "notification"
      message: "QA remediation complete: {stories_created} stories created"
```

### Invoke Hook

```
if hook_enabled("post-qa-remediation"):
    hook_context = {
        "stories_created": len($CREATED_STORIES),
        "gaps_deferred": len($DEFERRED_GAPS),
        "report_path": report_path
    }
    invoke_hook("post-qa-remediation", hook_context)
```

---

## Output Variables

| Variable | Description |
|----------|-------------|
| `$REPORTS_UPDATED` | Count of local gap files updated |
| `$ENHANCEMENT_REPORT_PATH` | Path to generated report |
| `$UPDATES_SKIPPED` | Count of imported files not updated |

---

## Error Handling

### Gap File Update Fails

```
try:
    update_gap_file(story)
except Error as e:
    log_warning("Failed to update {story.source_file}: {e}")
    // Continue - don't fail entire phase
    $UPDATE_ERRORS.append({
        "file": story.source_file,
        "error": str(e)
    })
```

### Report Generation Fails

```
try:
    Write(file_path=report_path, content=report_content)
except Error as e:
    log_error("Failed to generate enhancement report: {e}")
    // This is more serious - include in final summary
    $ENHANCEMENT_REPORT_PATH = None
```
