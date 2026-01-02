---
id: STORY-168
title: "RCA-012 Story Migration Script"
type: enhancement
priority: Medium
points: 3
status: Backlog
epic: N/A
sprint: N/A
created: 2025-12-31
source_rca: RCA-012
source_recommendation: REC-4
tags: [rca-012, migration, story-template, automation]
---

# STORY-168: RCA-012 Story Migration Script

## User Story

**As a** DevForgeAI framework user,
**I want** an optional script to update old stories from template v2.0 to v2.1,
**So that** I can have consistency in AC header format across all my stories if desired.

## Background

After STORY-165 updates the template, existing stories will still have the old format with `### 1. [ ]` AC headers. RCA-012 REC-4 provides an optional migration script for users who want to update their existing stories to the new format.

This is **optional** - users can keep old format if preferred. The script provides:
- Automated find/replace for AC headers
- Backup creation before modification
- format_version update in YAML frontmatter

## Acceptance Criteria

### AC#1: Migration Script Created
**Given** the DevForgeAI framework
**When** I look in `.claude/scripts/`
**Then** there should be a `migrate-ac-headers.sh` script

**Note:** Script placed in `.claude/scripts/` per source-tree.md line 288 (DevForgeAI CLI tools location).

### AC#2: Script Performs Find/Replace
**Given** a story with old format `### 1. [ ] Title`
**When** I run the migration script on that story
**Then** the AC headers should change to `### AC#1: Title`

### AC#3: Script Creates Backup
**Given** a story file being migrated
**When** the script runs
**Then** a backup file (`.backup`) should be created before modification

### AC#4: Script Updates format_version
**Given** a story with `format_version: "2.0"`
**When** the migration script runs
**Then** `format_version` should be updated to `"2.1"`

### AC#5: Script Handles Multiple Stories
**Given** a directory with multiple stories
**When** I run the script with a directory path
**Then** all `.story.md` files should be migrated

## Technical Specification

### File to Create

**`.claude/scripts/migrate-ac-headers.sh`**

(Placed in `.claude/scripts/` per source-tree.md line 288 - DevForgeAI CLI tools location)

### Script Content

```bash
#!/bin/bash
# Migrate story template v2.0 → v2.1 (remove AC header checkboxes)
# Usage: migrate-ac-headers.sh <story-file-or-directory>

TARGET="$1"

if [[ -z "$TARGET" ]]; then
  echo "Usage: migrate-ac-headers.sh <story-file-or-directory>"
  echo ""
  echo "Examples:"
  echo "  migrate-ac-headers.sh devforgeai/specs/Stories/STORY-052.story.md"
  echo "  migrate-ac-headers.sh devforgeai/specs/Stories/"
  exit 1
fi

migrate_file() {
  local file="$1"

  if [[ ! -f "$file" ]]; then
    echo "Error: File not found: $file"
    return 1
  fi

  # Backup original
  cp "$file" "$file.backup"

  # Replace AC header format: ### N. [ ] → ### AC#N:
  sed -i 's/^### \([0-9]\+\)\. \[ \] /### AC#\1: /' "$file"

  # Update format_version in YAML frontmatter
  sed -i 's/format_version: "2.0"/format_version: "2.1"/' "$file"

  echo "✓ Migrated: $file"
  echo "  Backup: $file.backup"
}

if [[ -d "$TARGET" ]]; then
  # Directory mode - migrate all story files
  for file in "$TARGET"/*.story.md; do
    if [[ -f "$file" ]]; then
      migrate_file "$file"
    fi
  done
else
  # Single file mode
  migrate_file "$TARGET"
fi

echo ""
echo "Migration complete!"
echo "To undo, restore from .backup files"
```

### Usage Documentation

Create `migrate-ac-headers.md` documentation explaining:
- When to use the script
- How to run it
- How to undo (restore from backup)
- Why this migration is optional

## Edge Cases

1. **No matching patterns** - Script should not error if story already in v2.1 format
2. **Permission issues** - Script should check write permissions
3. **Non-story files** - Script should only process `.story.md` files
4. **Already migrated** - Running twice should be idempotent (no harm)

## Definition of Done

### Implementation
- [ ] migrate-ac-headers.sh script created
- [ ] Script handles single file migration
- [ ] Script handles directory migration
- [ ] Script creates backups before modification
- [ ] Script updates format_version
- [ ] Script is executable (chmod +x)

### Testing
- [ ] Test with single story file
- [ ] Test with directory of stories
- [ ] Verify backup created
- [ ] Verify AC headers changed correctly
- [ ] Verify format_version updated
- [ ] Test idempotency (run twice, no errors)

### Documentation
- [ ] Usage documentation created
- [ ] RCA-012 updated with implementation status

## Non-Functional Requirements

### Safety
- Always create backup before modification
- Non-destructive (original can be restored)

### Idempotency
- Running multiple times should be safe

## Effort Estimate

- **Story Points:** 3 (1 SP = 4 hours)
- **Estimated Hours:** 1.5 hours
- **Complexity:** Medium (bash script + testing)

## Dependencies

- STORY-165 (template format change) - must be done first

## References

- Source RCA: `devforgeai/RCA/RCA-012/ANALYSIS.md`
- REC-4 Section: Lines 532-592

---

## Implementation Notes
<!-- Filled in by devforgeai-development skill -->
*To be completed during development*

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | /create-stories-from-rca | Story created from RCA-012 REC-4 |
