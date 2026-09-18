# Phase 6: Epic/Sprint Linking

Update epic and sprint documents to include references to newly created story.

## Overview

This phase establishes bidirectional links between the story and its parent epic/sprint documents for traceability.

**Key Updates (EPIC-051 Investigation Fix):**
- Sprint Summary table updated with story count and points
- Stories table created/updated with story details
- Change Log entry added
- Idempotent operation (no duplicate entries on re-run)

---

## Step 6.1: Update Epic File (If Associated)

**Objective:** Add story reference to epic's Stories section AND update Sprint Summary table

**If epic_id is not null:**

### Step 6.1.1: Read Epic File and Check for Existing Story

```
# Read epic file
epic_file_path = f"devforgeai/specs/Epics/{epic_id}.epic.md"
epic_content = Read(file_path=epic_file_path)

# Check if story already exists (idempotent check)
IF story_id in epic_content:
    Log: "Story {story_id} already exists in epic - skipping duplicate"
    SKIP to Step 6.2
```

### Step 6.1.2: Update or Create Stories Table

**Table Format:**
```markdown
## Stories

| Story ID | Feature | Title | Points | Status |
|----------|---------|-------|--------|--------|
| STORY-XXX | Feature N | Story title here | 8 | Backlog |
```

**Logic:**

```
# Determine story status and feature mapping
story_status = "Backlog"  # Default for new stories
feature_ref = extract_feature_from_metadata(story)  # e.g., "Feature 1" or "Feature 1.1"

# Check if ## Stories section exists
IF "## Stories" in epic_content:
    # Find the Stories table and append new row
    # Locate the last row of the table (line ending with " |")

    # Find insertion point: last table row before empty line or next section
    lines = epic_content.split("\n")
    table_end_index = find_last_table_row_index(lines, "## Stories")

    # Insert new row after last table row
    new_row = f"| {story_id} | {feature_ref} | {story_title} | {points} | {story_status} |"

    Edit(
      file_path=epic_file_path,
      old_string=lines[table_end_index],
      new_string=lines[table_end_index] + "\n" + new_row
    )

ELSE:
    # Create Stories section
    # Insert before ## Change Log, ## Next Steps, or at end

    IF "## Change Log" in epic_content:
        anchor = "## Change Log"
    ELIF "## Next Steps" in epic_content:
        anchor = "## Next Steps"
    ELSE:
        anchor = None  # Will append at end

    stories_section = """## Stories

| Story ID | Feature | Title | Points | Status |
|----------|---------|-------|--------|--------|
| """ + story_id + """ | """ + feature_ref + """ | """ + story_title + """ | """ + str(points) + """ | """ + story_status + """ |

"""

    IF anchor:
        Edit(
          file_path=epic_file_path,
          old_string=anchor,
          new_string=stories_section + anchor
        )
    ELSE:
        # Append at end of file
        Edit(
          file_path=epic_file_path,
          old_string=epic_content[-100:],  # Last 100 chars as anchor
          new_string=epic_content[-100:] + "\n\n" + stories_section
        )
```

### Step 6.1.3: Update Sprint Summary Table

**Objective:** Increment Stories count and Points for the target sprint

**Table Format:**
```markdown
### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1 | Not Started | 16 | 5 | 0 | 0 | 0 |
| **Total** | **0%** | **30** | **8** | **0** | **0** | **0** |
```

**Logic:**

```
# Extract target sprint from story metadata
target_sprint = story.sprint  # e.g., "Sprint 1" or "Sprint-1"

# Normalize sprint name for matching
sprint_match = normalize_sprint_name(target_sprint)  # "Sprint 1"

# Find Sprint Summary table
IF "Sprint Summary" in epic_content:
    lines = epic_content.split("\n")

    # Find the row for target sprint
    FOR i, line in enumerate(lines):
        IF sprint_match in line AND "|" in line:
            # Parse current values: | Sprint 1 | Not Started | 16 | 5 | 0 | 0 | 0 |
            columns = parse_table_row(line)
            # columns = ["Sprint 1", "Not Started", "16", "5", "0", "0", "0"]

            old_points = int(columns[2])
            old_stories = int(columns[3])

            new_points = old_points + story.points
            new_stories = old_stories + 1

            # Reconstruct row
            new_row = f"| {columns[0]} | {columns[1]} | {new_points} | {new_stories} | {columns[4]} | {columns[5]} | {columns[6]} |"

            Edit(
              file_path=epic_file_path,
              old_string=line,
              new_string=new_row
            )
            BREAK

    # Also update Total row if it exists
    FOR i, line in enumerate(lines):
        IF "**Total**" in line AND "|" in line:
            columns = parse_table_row(line)
            # columns = ["**Total**", "**0%**", "**30**", "**8**", "**0**", "**0**", "**0**"]

            # Extract numeric values (remove ** formatting)
            old_total_points = int(columns[2].replace("**", ""))
            old_total_stories = int(columns[3].replace("**", ""))

            new_total_points = old_total_points + story.points
            new_total_stories = old_total_stories + 1

            # Reconstruct row with ** formatting
            new_total_row = f"| **Total** | {columns[1]} | **{new_total_points}** | **{new_total_stories}** | {columns[4]} | {columns[5]} | {columns[6]} |"

            Edit(
              file_path=epic_file_path,
              old_string=line,
              new_string=new_total_row
            )
            BREAK

ELSE:
    Log: "No Sprint Summary table found in epic - skipping update"
```

### Step 6.1.4: Update Change Log

**Objective:** Add entry to epic's Change Log section

```
today = get_current_date()  # "2026-01-30"
changelog_entry = f"| {today} | {story_id} created ({story_title}) | /create-story |"

IF "## Change Log" in epic_content:
    lines = epic_content.split("\n")

    # Find the Change Log table header row (contains "Date" and "Change")
    # Then find the last data row (before empty line or next section)

    FOR i, line in enumerate(lines):
        IF "## Change Log" in line:
            # Find last table row in this section
            last_row_index = find_last_table_row_after(lines, i)

            Edit(
              file_path=epic_file_path,
              old_string=lines[last_row_index],
              new_string=lines[last_row_index] + "\n" + changelog_entry
            )
            BREAK
```

---

## Step 6.2: Update Sprint File (If Associated)

**Objective:** Add story reference to sprint's Sprint Backlog section

**If sprint_id is not "Backlog":**

```
# Read sprint file
sprint_file_path = f"devforgeai/specs/Sprints/{sprint_id}.md"

TRY:
    sprint_content = Read(file_path=sprint_file_path)
EXCEPT FileNotFoundError:
    Log: "Sprint file not found at {sprint_file_path} - skipping sprint update"
    SKIP to Step 6.3

# Check if story already exists (idempotent check)
IF story_id in sprint_content:
    Log: "Story {story_id} already exists in sprint - skipping duplicate"
    SKIP to Step 6.3

# Find "Sprint Backlog" section and append story
IF "## Sprint Backlog" in sprint_content:
    story_entry = f"- [{story_id}] {story_title} - {status} ({points} points, Priority: {priority})"

    # Find last entry in Sprint Backlog section
    lines = sprint_content.split("\n")
    FOR i, line in enumerate(lines):
        IF "## Sprint Backlog" in line:
            # Find last bullet point or table row in this section
            last_entry_index = find_last_entry_in_section(lines, i)

            Edit(
              file_path=sprint_file_path,
              old_string=lines[last_entry_index],
              new_string=lines[last_entry_index] + "\n" + story_entry
            )
            BREAK
ELSE:
    Log: "## Sprint Backlog section not found - creating it"

    Edit(
      file_path=sprint_file_path,
      old_string="## Sprint Backlog\n",
      new_string=f"""## Sprint Backlog

- [{story_id}] {story_title} - {status} ({points} points, Priority: {priority})
"""
    )
```

---

## Step 6.3: Verify Linking

**Objective:** Validate updates succeeded

**Validate updates:**
```
# Re-read epic file
if epic_id:
    epic_content = Read(file_path=epic_file_path)
    if story_id not in epic_content:
        ERROR: Epic linking failed
        Log: "ERROR: Story {story_id} not found in epic after update"
        # Retry with alternate approach or report to user
        RECOVERY: retry_epic_update_with_fallback()

# Re-read sprint file
if sprint_id != "Backlog":
    sprint_content = Read(file_path=sprint_file_path)
    if story_id not in sprint_content:
        ERROR: Sprint linking failed
        Log: "ERROR: Story {story_id} not found in sprint after update"
        # Retry or report to user
        RECOVERY: retry_sprint_update_with_fallback()
```

---

## Helper Functions

### normalize_sprint_name(sprint_id)
```
# Convert various sprint formats to standard form
# "Sprint-1" -> "Sprint 1"
# "sprint_1" -> "Sprint 1"
# "Sprint 1" -> "Sprint 1"

return sprint_id.replace("-", " ").replace("_", " ").title()
```

### parse_table_row(line)
```
# Parse markdown table row into list of values
# "| Sprint 1 | Not Started | 16 | 5 |" -> ["Sprint 1", "Not Started", "16", "5"]

columns = line.split("|")
return [col.strip() for col in columns if col.strip()]
```

### find_last_table_row_index(lines, section_header)
```
# Find the index of the last table row in a section
# Returns index of line ending with " |" before next section or empty line

in_section = False
last_row_index = -1

FOR i, line in enumerate(lines):
    IF section_header in line:
        in_section = True
        CONTINUE
    IF in_section:
        IF line.strip().endswith("|") AND line.strip().startswith("|"):
            last_row_index = i
        ELIF line.strip() == "" OR line.startswith("##"):
            BREAK

return last_row_index
```

### extract_feature_from_metadata(story)
```
# Extract feature reference from story metadata
# If story has feature_number in metadata, use it
# Otherwise, return "N/A"

IF story.feature_number:
    return f"Feature {story.feature_number}"
ELIF story.feature_name:
    return story.feature_name
ELSE:
    return "N/A"
```

---

## Output

**Phase 6 produces:**
- ✅ Epic file updated with story in Stories table (if applicable)
- ✅ Epic Sprint Summary table updated with new counts (if applicable)
- ✅ Epic Change Log updated with story creation entry
- ✅ Sprint file updated with story reference (if applicable)
- ✅ Links verified functional
- ✅ Idempotent: No duplicates on re-run

---

## Error Handling

**Error 1: Epic file not found**
- **Detection:** epic_id specified but file doesn't exist at devforgeai/specs/Epics/{epic_id}.epic.md
- **Recovery:** Ask user if epic ID correct, or create story without epic association

**Error 2: Sprint file not found**
- **Detection:** sprint_id specified but file doesn't exist at devforgeai/specs/Sprints/{sprint_id}.md
- **Recovery:** Ask user if sprint ID correct, or set sprint to "Backlog"

**Error 3: Edit failed (section not found)**
- **Detection:** "## Stories" or "## Sprint Backlog" section missing, Edit tool fails
- **Recovery:** Create section in correct location, retry Edit

**Error 4: Verification failed (story ID not in file after update)**
- **Detection:** Re-read shows story_id missing from updated file
- **Recovery:** Retry Edit with different old_string anchor, or manually insert

**Error 5: Table parsing failed**
- **Detection:** Cannot parse Sprint Summary table columns
- **Recovery:** Log warning, skip table update, continue with other updates

See `error-handling.md` for comprehensive error recovery procedures.

---

## Next Phase

**After Phase 6 completes →** Phase 7: Self-Validation

Load `story-validation-workflow.md` for Phase 7 workflow.
