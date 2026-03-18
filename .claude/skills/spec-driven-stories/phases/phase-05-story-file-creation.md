# Phase 05: Story File Creation

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=stories --from=04 --to=05 --project-root=.
```

| Exit Code | Action |
|-----------|--------|
| 0 | Prerequisites met. Proceed. |
| 1 | Phase 04 incomplete. HALT. |
| 127 | CLI not installed. Proceed without enforcement. |

---

## Contract

- **PURPOSE:** Assemble complete story document from phases 01-04 outputs, write to disk, verify all required sections present
- **REQUIRED SUBAGENTS:** none
- **REQUIRED ARTIFACTS:** Complete .story.md file written to `devforgeai/specs/Stories/`
- **STEP COUNT:** 5
- **REFERENCE FILES:**
  - `references/story-file-creation.md`
  - `references/story-structure-guide.md`
  - `assets/templates/story-template.md`

---

## Reference Loading [MANDATORY]

```
Read(file_path="src/claude/skills/spec-driven-stories/references/story-file-creation.md")
Read(file_path="src/claude/skills/spec-driven-stories/references/story-structure-guide.md")
Read(file_path="src/claude/skills/spec-driven-stories/assets/templates/story-template.md")
```

IF any Read fails: HALT -- "Phase 05 reference files not loaded."

Do NOT rely on memory of previous reads. Load ALL references fresh.

---

## Mandatory Steps (5)

### Step 5.1: Validate Output Directory

**EXECUTE:**
```
# Verify output directory exists and matches source-tree.md
Read(file_path="devforgeai/specs/context/source-tree.md")

output_dir = "devforgeai/specs/Stories/"
Glob(pattern="devforgeai/specs/Stories/")

IF directory does not exist:
  HALT: "Output directory {output_dir} does not exist per source-tree.md"

# Generate filename
story_slug = slugify($FEATURE_DESCRIPTION)  # lowercase, hyphens
$STORY_FILE_PATH = "devforgeai/specs/Stories/${STORY_ID}-${story_slug}.story.md"

Display: "Output path: ${STORY_FILE_PATH}"
```

**VERIFY:** Output directory exists and `$STORY_FILE_PATH` is set.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=05 --step=5.1 --project-root=.
```
Update checkpoint: `output.story_file_path = $STORY_FILE_PATH`
Update checkpoint: `phases["05"].steps_completed.append("5.1")`

---

### Step 5.2: Load Story Template

**EXECUTE:**
```
# Template already loaded in Reference Loading above
# Parse template sections and identify placeholders
template_sections = parse_template(story_template_content)

Display: "Template loaded: v2.8 ({section_count} sections)"
```

**VERIFY:** Template content is non-empty and contains YAML frontmatter markers.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=05 --step=5.2 --project-root=.
```
Update checkpoint: `phases["05"].steps_completed.append("5.2")`

---

### Step 5.3: Construct Frontmatter & Build Sections

**EXECUTE:**
```
# Build YAML frontmatter
frontmatter = {
  id: $STORY_ID,
  title: derive from $FEATURE_DESCRIPTION,
  status: "Backlog",
  priority: $PRIORITY,
  points: $POINTS,
  type: $TYPE,
  epic: $EPIC_ID or null,
  sprint: $SPRINT_ID or "Backlog",
  depends_on: $DEPENDS_ON or [],
  created: current date (YYYY-MM-DD),
  template_version: "2.8"
}

# Build document sections from phase outputs:
# - Description: from $FEATURE_DESCRIPTION
# - Acceptance Criteria: from $REQUIREMENTS_OUTPUT (Phase 02)
# - Technical Specification: from $TECH_SPEC (Phase 03)
# - UI Specification: from $UI_SPEC (Phase 04) or "N/A"
# - Non-Functional Requirements: from Phase 02 NFRs
# - Dependencies: from Phase 03 $DEPENDENCIES
# - Test Strategy: derived from AC and tech spec
# - AC Verification Checklist: generated from ACs
# - Implementation Notes: placeholder
# - Definition of Done: standard checklist
# - Change Log: initial entry
# - Notes: empty

# Populate provenance section if brainstorm/epic chain available
IF $EPIC_ID is not null:
  Read epic file for provenance data
  Add ## Provenance section with brainstorm -> epic -> story chain

$STORY_CONTENT = assemble full document from frontmatter + all sections
```

**VERIFY:** `$STORY_CONTENT` contains YAML frontmatter and all section headers.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=05 --step=5.3 --project-root=.
```
Update checkpoint: `phases["05"].steps_completed.append("5.3")`

---

### Step 5.4: Write to Disk

**EXECUTE:**
```
Write(file_path=$STORY_FILE_PATH, content=$STORY_CONTENT)
```

**VERIFY:**
```
Glob(pattern=$STORY_FILE_PATH)
IF not found: HALT -- "Story file was NOT written to disk."

Read(file_path=$STORY_FILE_PATH)
IF content is empty: HALT -- "Story file written but empty."
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=05 --step=5.4 --project-root=.
```
Update checkpoint: `phases["05"].steps_completed.append("5.4")`

---

### Step 5.5: Verify Required Sections (absorbs Phase 5-6 Gate)

**EXECUTE:**
```
# Read the written file fresh
story_content = Read(file_path=$STORY_FILE_PATH)

# MUST-match ## headers (12 required)
required_h2_headers = [
    "^## Description",
    "^## Acceptance Criteria",
    "^## Technical Specification",
    "^## Technical Limitations",
    "^## Non-Functional Requirements",
    "^## Dependencies",
    "^## Test Strategy",
    "^## Acceptance Criteria Verification Checklist",
    "^## Implementation Notes",
    "^## Definition of Done",
    "^## Change Log",
    "^## Notes"
]

# MUST-match ### subsections (16 required)
required_h3_subsections = [
    "^### Performance",
    "^### Security",
    "^### Scalability",
    "^### Reliability",
    "^### Observability",
    "^### Prerequisite Stories",
    "^### External Dependencies",
    "^### Technology Dependencies",
    "^### Unit Tests",
    "^### Integration Tests",
    "^### Implementation",
    "^### Quality",
    "^### Testing",
    "^### Documentation",
    "^### TDD Workflow Summary",
    "^### Files Created"
]

missing_sections = []

FOR each pattern in required_h2_headers:
    IF NOT Grep(pattern=pattern, path=$STORY_FILE_PATH):
        missing_sections.append(pattern)

FOR each pattern in required_h3_subsections:
    IF NOT Grep(pattern=pattern, path=$STORY_FILE_PATH):
        missing_sections.append(pattern)

IF missing_sections is NOT empty:
    HALT: "Phase 5-6 Gate FAILED: Missing {len(missing_sections)} required sections"
    Display missing sections list
    DO NOT proceed

Display: "Phase 5-6 Gate PASSED: All 28 required sections (12 ## + 16 ###) confirmed present"
```

**VERIFY:** Zero missing sections. All 28 sections present.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=05 --step=5.5 --project-root=.
```
Update checkpoint: `phases["05"].steps_completed.append("5.5")`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=stories --phase=05 --checkpoint-passed --project-root=.
```

## Exit Verification Checklist

- [ ] Story file exists on disk at `$STORY_FILE_PATH`
- [ ] File is non-empty
- [ ] All 12 required ## headers present
- [ ] All 16 required ### subsections present
- [ ] YAML frontmatter is valid
- [ ] Story ID in frontmatter matches `$STORY_ID`

IF any unchecked: HALT -- "Phase 05 exit criteria not met"

## Phase Transition Display

```
Display: "Phase 05 complete. Story file written: ${STORY_FILE_PATH}"
Display: "28/28 required sections verified."
Display: "Proceeding to Phase 06: Epic/Sprint Linking..."
```
