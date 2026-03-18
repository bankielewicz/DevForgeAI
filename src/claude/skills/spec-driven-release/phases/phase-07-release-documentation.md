# Phase 07: Release Documentation

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --workflow=release --from=06 --to=07 --project-root=.
```

## Contract

PURPOSE: Generate release notes, update story status to Released, update CHANGELOG.md, archive story file.
REQUIRED SUBAGENTS: none
REQUIRED ARTIFACTS: Release notes file, updated story file, updated CHANGELOG.md, archived story
STEP COUNT: 6 mandatory steps

---

## Mandatory Steps

### Step 7.1: Load Release Documentation Reference

EXECUTE: Load release documentation reference and release notes template.
```
Read(file_path=".claude/skills/spec-driven-release/references/release-documentation.md")
Read(file_path=".claude/skills/spec-driven-release/assets/templates/release-notes-template.md")
```
VERIFY: Both files loaded successfully (non-empty Read responses).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=07 --step=7.1 --project-root=.`

---

### Step 7.2: Generate Release Notes

EXECUTE: Populate release notes template and write to releases directory.
```
# Determine version from story or build results
$VERSION = story.version OR $BUILD_RESULTS[0].version OR "1.0.0"

# Populate template with release data
release_notes = template populated with:
    - VERSION: ${VERSION}
    - STORY_ID: ${STORY_ID}
    - STORY_TITLE: from story file
    - CHANGES: acceptance criteria completed
    - QA_STATUS: "QA Approved"
    - COVERAGE: from QA report (if available)
    - DEPLOYMENT_STRATEGY: ${DEPLOYMENT_STRATEGY}
    - ENVIRONMENT: ${ENVIRONMENT}
    - TIMESTAMPS: start_time, end_time
    - ROLLBACK_COMMAND: ${PRODUCTION_DEPLOY_RESULT.rollback_command} (if applicable)

# Ensure releases directory exists
Glob(pattern="devforgeai/releases/")
IF directory does not exist:
    # Will be created by Write

Write(file_path="devforgeai/releases/release-${VERSION}-${STORY_ID}.md", content=release_notes)

Display: "Release notes generated: devforgeai/releases/release-${VERSION}-${STORY_ID}.md"
```
VERIFY: Release notes file exists at `devforgeai/releases/release-${VERSION}-${STORY_ID}.md`.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=07 --step=7.2 --project-root=.`

---

### Step 7.3: Update Story Status to Released

EXECUTE: Update story file status from "QA Approved" to "Released".
```
Read(file_path="devforgeai/specs/Stories/${STORY_ID}.story.md")

# Update current status
Grep(pattern="Current Status.*QA Approved", path="devforgeai/specs/Stories/${STORY_ID}.story.md", output_mode="content")

IF found:
    Edit(file_path="devforgeai/specs/Stories/${STORY_ID}.story.md",
         old_string="**Current Status:** QA Approved",
         new_string="**Current Status:** Released")
ELSE:
    # Try alternate status format
    Grep(pattern="Current Status.*Releasing", path="devforgeai/specs/Stories/${STORY_ID}.story.md", output_mode="content")
    IF found:
        Edit(file_path="devforgeai/specs/Stories/${STORY_ID}.story.md",
             old_string="**Current Status:** Releasing",
             new_string="**Current Status:** Released")
    ELSE:
        Display: "Warning: Could not find status to update. Manual update may be needed."

# Verify update
Grep(pattern="Current Status.*Released", path="devforgeai/specs/Stories/${STORY_ID}.story.md", output_mode="content")
Display: "Story status updated to: Released"
```
VERIFY: Story file contains "Current Status: Released" (via Grep confirmation).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=07 --step=7.3 --project-root=.`

---

### Step 7.4: Update Story Change Log

EXECUTE: Append release entry to story change log.
```
Read(file_path="devforgeai/specs/Stories/${STORY_ID}.story.md")

# Find the change log table in the story
Grep(pattern="Change Log|Changelog", path="devforgeai/specs/Stories/${STORY_ID}.story.md", output_mode="content")

# Append release entry
$TIMESTAMP = current ISO 8601 timestamp
$CHANGE_ENTRY = "| ${TIMESTAMP} | .claude/deployment-engineer | Released | Deployed ${VERSION} to ${ENVIRONMENT} | CHANGELOG.md |"

# Find the last row in the change log table and append after it
Edit(file_path="devforgeai/specs/Stories/${STORY_ID}.story.md",
     old_string=last_change_log_entry,
     new_string="${last_change_log_entry}\n${CHANGE_ENTRY}")

Display: "Story change log updated with release entry"
```
VERIFY: Change log entry appended to story file (Grep for "Released" and "Deployed" in change log).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=07 --step=7.4 --project-root=.`

---

### Step 7.5: Update CHANGELOG.md

EXECUTE: Add release entry to project CHANGELOG.md if it exists.
```
Glob(pattern="CHANGELOG.md")

IF CHANGELOG.md exists:
    Read(file_path="CHANGELOG.md")

    # Add entry under [Unreleased] section
    Grep(pattern="## \\[Unreleased\\]", path="CHANGELOG.md", output_mode="content")

    IF [Unreleased] section found:
        $STORY_TITLE = extracted from story file
        Edit(file_path="CHANGELOG.md",
             old_string="## [Unreleased]",
             new_string="## [Unreleased]\n\n- ${STORY_TITLE} ([${STORY_ID}])")

        # Add reference link at bottom of file
        # Append: [${STORY_ID}]: devforgeai/specs/Stories/archive/${STORY_ID}.story.md
        Display: "CHANGELOG.md updated with ${STORY_ID} entry"
    ELSE:
        Display: "Warning: No [Unreleased] section found in CHANGELOG.md"
ELSE:
    Display: "No CHANGELOG.md found at project root (skipped)"
```
VERIFY: Either CHANGELOG.md updated with entry OR no CHANGELOG.md exists (skipped).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=07 --step=7.5 --project-root=.`

---

### Step 7.6: Archive Story File

EXECUTE: Move story file to archive directory.
```
# Ensure archive directory exists
Glob(pattern="devforgeai/specs/Stories/archive/")
IF directory does not exist:
    Bash(command="mkdir -p devforgeai/specs/Stories/archive/")

# Move story to archive
Bash(command="git mv devforgeai/specs/Stories/${STORY_ID}.story.md devforgeai/specs/Stories/archive/${STORY_ID}.story.md 2>/dev/null || mv devforgeai/specs/Stories/${STORY_ID}.story.md devforgeai/specs/Stories/archive/")

# Verify archive
Glob(pattern="devforgeai/specs/Stories/archive/${STORY_ID}*.story.md")

IF archived file found:
    Display: "Story archived: devforgeai/specs/Stories/archive/${STORY_ID}.story.md"
ELSE:
    Display: "Warning: Story archive verification failed. Check manually."
```
VERIFY: Story file exists at archive location `devforgeai/specs/Stories/archive/${STORY_ID}.story.md`.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=07 --step=7.6 --project-root=.`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --workflow=release --phase=07 --checkpoint-passed --project-root=.
```

## Phase 07 Completion Display

```
Phase 07 Complete: Release Documentation
  Release Notes: devforgeai/releases/release-${VERSION}-${STORY_ID}.md
  Story Status: Released
  CHANGELOG: ${changelog_updated ? 'Updated' : 'Skipped'}
  Archive: devforgeai/specs/Stories/archive/${STORY_ID}.story.md
  Audit trail complete
```
