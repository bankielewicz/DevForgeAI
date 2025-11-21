# RCA-012: Migration Script (REC-4)
## Automated Story Format Migration (v2.0 → v2.1)

**Recommendation ID:** REC-4
**Priority:** MEDIUM
**Effort:** 1.5 hours
**Purpose:** Optional automated migration for consistency

---

## Objective

Provide automated script to migrate existing stories from template v2.0 format (AC headers with checkboxes `### 1. [ ]`) to template v2.1 format (AC headers without checkboxes `### AC#1:`), enabling users to achieve visual consistency across old and new stories.

---

## Use Cases

### When to Use Migration Script

✅ **Use migration when:**
- Want consistency across all stories (old and new)
- Reviewing historical stories and find checkbox syntax confusing
- Creating documentation that references multiple stories
- Preparing stories for external review/presentation

❌ **Skip migration when:**
- Old story format doesn't bother you
- Story is complete and archived (no active work)
- Risk of script error outweighs benefit of consistency
- Time investment not justified

**Recommendation:** Migration is **optional**. Framework supports both formats.

---

## Script Implementation

### File Location

**Path:** `.claude/skills/devforgeai-story-creation/scripts/migrate-ac-headers.sh`

**Create Directory:**
```bash
mkdir -p .claude/skills/devforgeai-story-creation/scripts
```

---

### Script Content

**File:** `migrate-ac-headers.sh`

```bash
#!/bin/bash
#================================================================================
# Story Template Migration Script (v2.0 → v2.1)
#================================================================================
#
# Purpose: Migrate AC header format from '### 1. [ ]' to '### AC#1:'
# Version: 1.0
# Created: 2025-01-21 (RCA-012 Remediation)
# Maintained by: devforgeai-story-creation skill
#
# Usage:
#   migrate-ac-headers.sh <story-file>
#   migrate-ac-headers.sh .ai_docs/Stories/STORY-052-*.story.md
#
# Safety:
#   - Creates backup before modification (.v2.0-backup extension)
#   - Validates changes after migration
#   - Provides restore instructions if issues detected
#
#================================================================================

set -e  # Exit on error

#--- Configuration ---
BACKUP_EXT=".v2.0-backup"
RESTORE_INSTRUCTIONS="To restore: mv \"\$BACKUP_FILE\" \"\$STORY_FILE\""

#--- Argument Validation ---
STORY_FILE="$1"

if [[ -z "$STORY_FILE" ]]; then
  echo "❌ Error: No story file specified"
  echo ""
  echo "Usage: migrate-ac-headers.sh <story-file>"
  echo "Example: migrate-ac-headers.sh .ai_docs/Stories/STORY-052-user-facing-prompting-guide.story.md"
  echo ""
  exit 1
fi

if [[ ! -f "$STORY_FILE" ]]; then
  echo "❌ Error: File not found: $STORY_FILE"
  echo ""
  echo "Verify path and try again."
  exit 1
fi

#--- Display Migration Info ---
echo "========================================================================="
echo "Story Template Migration (v2.0 → v2.1)"
echo "========================================================================="
echo "File: $STORY_FILE"
echo "Date: $(date)"
echo ""

#--- Pre-Migration Validation ---
echo "[1/6] Pre-migration validation..."

# Check current format version
CURRENT_VERSION=$(grep "^format_version:" "$STORY_FILE" | grep -o '"[^"]*"' | tr -d '"')

if [[ "$CURRENT_VERSION" == "2.1" ]]; then
  echo "⚠️  Warning: Story already at v2.1 format"
  echo "    No migration needed. Exiting."
  exit 0
fi

echo "    Current version: $CURRENT_VERSION"

# Count AC headers (old format)
AC_COUNT_OLD=$(grep -c "^### [0-9]\+\. \[" "$STORY_FILE" 2>/dev/null || echo 0)

if [ $AC_COUNT_OLD -eq 0 ]; then
  echo "⚠️  Warning: No AC headers found with old format (### N. [ ])"
  echo "    Story may already be migrated or use different format."
  echo "    Exiting without changes."
  exit 0
fi

echo "    AC headers found (old format): $AC_COUNT_OLD"
echo "    ✓ Pre-migration validation passed"
echo ""

#--- Backup Original ---
echo "[2/6] Creating backup..."

BACKUP_FILE="${STORY_FILE}${BACKUP_EXT}"

cp "$STORY_FILE" "$BACKUP_FILE"

if [[ ! -f "$BACKUP_FILE" ]]; then
  echo "❌ Error: Backup creation failed"
  exit 1
fi

BACKUP_SIZE=$(stat -f%z "$BACKUP_FILE" 2>/dev/null || stat -c%s "$BACKUP_FILE" 2>/dev/null)
echo "    Backup created: $BACKUP_FILE"
echo "    Backup size: $BACKUP_SIZE bytes"
echo "    ✓ Backup complete"
echo ""

#--- Perform Migration ---
echo "[3/6] Migrating AC header format..."

# Migration 1: Update AC headers (both checked and unchecked)
# Pattern: ### N. [ ] Title → ### AC#N: Title
# Pattern: ### N. [x] Title → ### AC#N: Title

sed -i.tmp 's/^### \([0-9]\+\)\. \[\(x\| \)\] /### AC#\1: /' "$STORY_FILE"

# Migration 2: Update format_version
sed -i.tmp 's/format_version: "2.0"/format_version: "2.1"/' "$STORY_FILE"
sed -i.tmp 's/format_version: "1.0"/format_version: "2.1"/' "$STORY_FILE"

# Remove sed backup
rm -f "${STORY_FILE}.tmp"

echo "    ✓ AC headers migrated"
echo "    ✓ Format version updated"
echo ""

#--- Post-Migration Validation ---
echo "[4/6] Post-migration validation..."

# Count AC headers (new format)
AC_COUNT_NEW=$(grep -c "^### AC#[0-9]\+:" "$STORY_FILE" 2>/dev/null || echo 0)

echo "    AC headers after migration (new format): $AC_COUNT_NEW"

if [ $AC_COUNT_NEW -eq $AC_COUNT_OLD ]; then
  echo "    ✓ AC count matches (before: $AC_COUNT_OLD, after: $AC_COUNT_NEW)"
else
  echo "    ⚠️  Warning: AC count mismatch"
  echo "       Before: $AC_COUNT_OLD"
  echo "       After:  $AC_COUNT_NEW"
  echo "       Review changes manually"
fi

# Verify no old format remains
OLD_FORMAT_REMAINING=$(grep -c "^### [0-9]\+\. \[" "$STORY_FILE" 2>/dev/null || echo 0)

if [ $OLD_FORMAT_REMAINING -eq 0 ]; then
  echo "    ✓ No old format remains"
else
  echo "    ⚠️  Warning: $OLD_FORMAT_REMAINING instances of old format still present"
  echo "       Review file manually"
fi

# Verify format version
NEW_VERSION=$(grep "^format_version:" "$STORY_FILE" | grep -o '"[^"]*"' | tr -d '"')

if [[ "$NEW_VERSION" == "2.1" ]]; then
  echo "    ✓ Format version updated to 2.1"
else
  echo "    ⚠️  Warning: Format version is '$NEW_VERSION' (expected 2.1)"
fi

echo ""

#--- Summary ---
echo "[5/6] Migration summary..."
echo ""
echo "  Changes applied:"
echo "    • AC headers: ### N. [ ] → ### AC#N:"
echo "    • Count: $AC_COUNT_NEW AC headers updated"
echo "    • Format version: $CURRENT_VERSION → 2.1"
echo ""

#--- Review Instructions ---
echo "[6/6] Review and finalization..."
echo ""
echo "  Next steps:"
echo "    1. Review changes:"
echo "       diff \"$BACKUP_FILE\" \"$STORY_FILE\""
echo ""
echo "    2. If changes look correct:"
echo "       Keep migrated file (no action needed)"
echo "       Optional: rm \"$BACKUP_FILE\" (remove backup)"
echo ""
echo "    3. If issues found:"
echo "       $RESTORE_INSTRUCTIONS"
echo ""
echo "========================================================================="
echo "Migration Complete"
echo "========================================================================="
echo ""

if [ $AC_COUNT_NEW -ne $AC_COUNT_OLD ] || [ $OLD_FORMAT_REMAINING -gt 0 ]; then
  echo "⚠️  WARNINGS DETECTED - Manual review recommended"
  exit 2
else
  echo "✓ Migration successful - All validations passed"
  exit 0
fi
```

---

### Script Features

**Safety:**
- Creates backup before any changes
- Validates changes after migration
- Provides restore instructions
- Returns non-zero exit code if warnings

**Validation:**
- Counts AC headers before/after (should match)
- Verifies no old format remains
- Checks format version updated
- Reports warnings if discrepancies

**Flexibility:**
- Handles both checked `[x]` and unchecked `[ ]` in old format
- Works on v1.0 or v2.0 stories
- Skips if already v2.1 (idempotent)
- Provides diff command for review

**Output:**
- Progress indicators ([1/6] through [6/6])
- Clear success/warning messages
- Actionable next steps
- Restore instructions if needed

---

## Installation

**Create Script:**
```bash
mkdir -p .claude/skills/devforgeai-story-creation/scripts

cat > .claude/skills/devforgeai-story-creation/scripts/migrate-ac-headers.sh << 'SCRIPT'
{paste script content from above}
SCRIPT

chmod +x .claude/skills/devforgeai-story-creation/scripts/migrate-ac-headers.sh

echo "✓ Migration script installed"
```

**Verify Installation:**
```bash
ls -lh .claude/skills/devforgeai-story-creation/scripts/migrate-ac-headers.sh
# Expected: -rwxr-xr-x ... migrate-ac-headers.sh (executable)

.claude/skills/devforgeai-story-creation/scripts/migrate-ac-headers.sh
# Expected: Usage message (no arguments provided)
```

---

## Usage Examples

### Example 1: Migrate Single Story (STORY-052)

```bash
bash .claude/skills/devforgeai-story-creation/scripts/migrate-ac-headers.sh \
  .ai_docs/Stories/STORY-052-user-facing-prompting-guide.story.md
```

**Output:**
```
=========================================================================
Story Template Migration (v2.0 → v2.1)
=========================================================================
File: .ai_docs/Stories/STORY-052-user-facing-prompting-guide.story.md
Date: 2025-01-21 09:00:00

[1/6] Pre-migration validation...
    Current version: 2.0
    AC headers found (old format): 6
    ✓ Pre-migration validation passed

[2/6] Creating backup...
    Backup created: .ai_docs/Stories/STORY-052-user-facing-prompting-guide.story.md.v2.0-backup
    Backup size: 15234 bytes
    ✓ Backup complete

[3/6] Migrating AC header format...
    ✓ AC headers migrated
    ✓ Format version updated

[4/6] Post-migration validation...
    AC headers after migration (new format): 6
    ✓ AC count matches (before: 6, after: 6)
    ✓ No old format remains
    ✓ Format version updated to 2.1

[5/6] Migration summary...

  Changes applied:
    • AC headers: ### N. [ ] → ### AC#N:
    • Count: 6 AC headers updated
    • Format version: 2.0 → 2.1

[6/6] Review and finalization...

  Next steps:
    1. Review changes:
       diff ".ai_docs/Stories/STORY-052-user-facing-prompting-guide.story.md.v2.0-backup" \
            ".ai_docs/Stories/STORY-052-user-facing-prompting-guide.story.md"

    2. If changes look correct:
       Keep migrated file (no action needed)
       Optional: rm ".ai_docs/Stories/STORY-052-user-facing-prompting-guide.story.md.v2.0-backup"

    3. If issues found:
       mv ".ai_docs/Stories/STORY-052-user-facing-prompting-guide.story.md.v2.0-backup" \
          ".ai_docs/Stories/STORY-052-user-facing-prompting-guide.story.md"

=========================================================================
Migration Complete
=========================================================================

✓ Migration successful - All validations passed
```

**Review Changes:**
```bash
diff .ai_docs/Stories/STORY-052-user-facing-prompting-guide.story.md.v2.0-backup \
     .ai_docs/Stories/STORY-052-user-facing-prompting-guide.story.md

# Expected diff:
# - ### 1. [ ] Document Completeness
# + ### AC#1: Document Completeness
#
# - ### 2. [ ] Example Quality
# + ### AC#2: Example Quality
#
# ... (6 total changes)
#
# - format_version: "2.0"
# + format_version: "2.1"
```

**If Satisfied, Remove Backup:**
```bash
rm .ai_docs/Stories/STORY-052-user-facing-prompting-guide.story.md.v2.0-backup
echo "✓ Backup removed - migration finalized"
```

---

### Example 2: Migrate Multiple Stories (Batch Mode)

**Migrate All Stories in Current Sprint:**
```bash
for story in .ai_docs/Stories/STORY-052*.story.md \
             .ai_docs/Stories/STORY-053*.story.md \
             .ai_docs/Stories/STORY-054*.story.md; do

  echo "Migrating: $story"
  bash .claude/skills/devforgeai-story-creation/scripts/migrate-ac-headers.sh "$story"
  echo ""
done

echo "✓ Batch migration complete"
echo "Review changes with: git diff .ai_docs/Stories/"
```

---

### Example 3: Dry-Run Mode (Preview Changes)

**Modify Script for Dry-Run:**
```bash
# Add --dry-run flag handling
if [[ "$2" == "--dry-run" ]]; then
  echo "[DRY RUN MODE] - No changes will be made"
  echo ""

  # Show what WOULD change (without modifying file)
  echo "Changes that would be applied:"
  grep "^### [0-9]\+\. \[" "$STORY_FILE" | while read line; do
    old_line="$line"
    new_line=$(echo "$line" | sed 's/^### \([0-9]\+\)\. \[\(x\| \)\] /### AC#\1: /')
    echo "  - $old_line"
    echo "  + $new_line"
    echo ""
  done

  exit 0
fi
```

**Usage:**
```bash
bash migrate-ac-headers.sh STORY-052-*.story.md --dry-run
# Shows preview without modifying file
```

---

## Testing

### Test Scenario 1: Migrate v2.0 Story with Unchecked AC Headers

**Test Story:** STORY-052 (has `### 1. [ ]` format)

**Before Migration:**
```markdown
### 1. [ ] Document Completeness - Core Content Coverage
### 2. [ ] Example Quality and Realism
### 3. [ ] Command-Specific Guidance Accuracy
format_version: "2.0"
```

**After Migration:**
```markdown
### AC#1: Document Completeness - Core Content Coverage
### AC#2: Example Quality and Realism
### AC#3: Command-Specific Guidance Accuracy
format_version: "2.1"
```

**Validation:**
- [ ] All AC headers converted
- [ ] Numbering preserved (1→#1, 2→#2, etc.)
- [ ] Checkbox syntax removed
- [ ] Format version updated
- [ ] File otherwise unchanged
- [ ] Backup created successfully

---

### Test Scenario 2: Migrate v2.0 Story with CHECKED AC Headers

**Test Story:** STORY-007 (has `### 1. [x]` format)

**Before Migration:**
```markdown
### 1. [x] Retrospective Triggered at Operation Completion
### 2. [x] Failed Command with Root Cause Feedback
format_version: "2.0"
```

**After Migration:**
```markdown
### AC#1: Retrospective Triggered at Operation Completion
### AC#2: Failed Command with Root Cause Feedback
format_version: "2.1"
```

**Validation:**
- [ ] Checked status `[x]` removed (no longer relevant)
- [ ] AC headers converted to definition format
- [ ] No checkbox syntax remains
- [ ] Format version updated

---

### Test Scenario 3: Migrate v1.0 Story

**Test Story:** Hypothetical v1.0 story

**Before:**
```markdown
### 1. [ ] Acceptance Criterion
format_version: "1.0"
```

**After:**
```markdown
### AC#1: Acceptance Criterion
format_version: "2.1"
```

**Validation:**
- [ ] Script handles v1.0 → v2.1 migration (skips v2.0)
- [ ] Format version updated correctly

---

### Test Scenario 4: Story Already v2.1 (Idempotent)

**Test Story:** Story created after Phase 1 implementation

**Before:**
```markdown
### AC#1: Already Migrated
format_version: "2.1"
```

**Expected Behavior:**
```
⚠️  Warning: Story already at v2.1 format
    No migration needed. Exiting.
```

**Validation:**
- [ ] Script detects v2.1 format
- [ ] Exits without changes (idempotent)
- [ ] No backup created
- [ ] File untouched

---

### Test Scenario 5: Story with No AC Headers

**Test Story:** Story with unusual structure (no ACs)

**Expected Behavior:**
```
⚠️  Warning: No AC headers found with old format (### N. [ ])
    Story may already be migrated or use different format.
    Exiting without changes.
```

**Validation:**
- [ ] Script handles missing AC headers gracefully
- [ ] Exits without error
- [ ] File untouched

---

## Edge Cases & Handling

### Edge Case 1: AC Header with Complex Title (Special Characters)

**Before:**
```markdown
### 1. [ ] User Authentication (OAuth 2.0) - Social Login
```

**After:**
```markdown
### AC#1: User Authentication (OAuth 2.0) - Social Login
```

**Handling:** Regex preserves everything after the checkbox, including special characters

---

### Edge Case 2: Malformed AC Header

**Before:**
```markdown
###2. [ ]Missing Spaces
```

**After:**
```markdown
###2. [ ]Missing Spaces  (unchanged - malformed, not matched by regex)
```

**Handling:** Script only matches well-formed headers. Malformed headers require manual fix.

---

### Edge Case 3: False Positive (Non-AC Header with Similar Format)

**Before:**
```markdown
### 1. [ ] This is a checklist item, not an AC header
```

**After:**
```markdown
### AC#1: This is a checklist item, not an AC header  (incorrectly migrated)
```

**Handling:**
- **Issue:** Script cannot distinguish AC headers from other `### N. [ ]` patterns
- **Likelihood:** Low (only AC section uses this format in template)
- **Mitigation:** Review diff before finalizing, restore if incorrect
- **Prevention:** Manual review required for edge cases

---

## Rollback Procedure

**If migration corrupts story file:**

### Immediate Restore
```bash
# Restore from backup
mv "${STORY_FILE}.v2.0-backup" "$STORY_FILE"

echo "✓ Story restored from backup"
```

**Validation:**
```bash
# Verify restoration
grep "^### [0-9]\. \[" "$STORY_FILE"
# Expected: Old format restored (AC headers with checkboxes)

grep "format_version" "$STORY_FILE"
# Expected: Original version (2.0 or 1.0)
```

---

### Document Issue

**If script failed:**
```bash
cat > .devforgeai/RCA/RCA-012/MIGRATION-ISSUES.md << 'EOF'
# Migration Script Issues

**Date:** YYYY-MM-DD
**Story:** {STORY-ID}
**Issue:** {What went wrong}

**Symptoms:**
- {Observed behavior}

**Diagnosis:**
- {Why it failed}

**Resolution:**
- {How to fix}

**Prevention:**
- {How to prevent in future}
EOF
```

---

## Documentation

### Add Usage Guide to devforgeai-story-creation Skill

**File:** `.claude/skills/devforgeai-story-creation/SKILL.md`

**Section:** Add after "Story Template Versions"

**Content:**
```markdown
### Migrating Old Stories to v2.1 (Optional)

**Purpose:** Update v1.0/v2.0 stories to v2.1 format for visual consistency

**Migration Script:**
```bash
bash .claude/skills/devforgeai-story-creation/scripts/migrate-ac-headers.sh <story-file>
```

**What Gets Changed:**
- AC headers: `### 1. [ ]` → `### AC#1:`
- Format version: `"2.0"` → `"2.1"`

**Safety:**
- Backup created automatically (.v2.0-backup)
- Restore instructions provided
- Validation confirms changes correct

**When to Migrate:**
- Want consistency across all stories
- Preparing stories for review/presentation
- Find checkbox syntax confusing

**When to Skip:**
- Old format doesn't bother you
- Story is archived (no active work)
- Migration risk outweighs benefit

**See:** RCA-012/MIGRATION-SCRIPT.md for complete documentation
```

**Effort:** 15 minutes (documentation addition)

---

## Effort Summary

| Task | Time | Cumulative |
|------|------|------------|
| Script creation | 45 min | 45 min |
| Testing (5 scenarios) | 30 min | 1h 15min |
| Documentation | 15 min | 1h 30min |
| **Total** | **1.5 hours** | - |

**Per-Story Migration:**
- Run script: 30 seconds
- Review diff: 2 minutes
- Finalize (keep or restore): 30 seconds
- **Per story:** ~3 minutes

**Batch Migration (57 stories):**
- Script execution: ~15 minutes
- Review changes: ~1 hour
- **Total:** ~1.25 hours

---

## Success Criteria

**Script is successful when:**

- [ ] Script created and executable
- [ ] All 5 test scenarios pass
- [ ] Backup created before changes
- [ ] AC headers migrated correctly
- [ ] Format version updated
- [ ] Validation confirms no data loss
- [ ] Restore from backup works
- [ ] User can migrate stories without errors
- [ ] Documentation added to skill

**User Experience:**
- "Migration was easy and safe"
- "I reviewed changes with diff before keeping"
- "Backup gave me confidence to try migration"
- "Now all my stories have consistent format"

---

## Optional Enhancements

### Enhancement 1: Batch Mode Flag

**Add `--batch` flag:**
```bash
if [[ "$2" == "--batch" ]]; then
  # Skip interactive confirmations
  # Auto-remove backups if migration successful
  # Quieter output (one line per story)
fi
```

**Usage:**
```bash
for story in .ai_docs/Stories/*.story.md; do
  migrate-ac-headers.sh "$story" --batch
done
```

**Effort:** +30 minutes

---

### Enhancement 2: Rollback All Mode

**Add companion script: `rollback-migrations.sh`**
```bash
#!/bin/bash
# Restore all stories from .v2.0-backup files

for backup in .ai_docs/Stories/*.v2.0-backup; do
  original="${backup%.v2.0-backup}"
  mv "$backup" "$original"
  echo "✓ Restored: $(basename $original)"
done
```

**Effort:** +15 minutes

---

### Enhancement 3: Migration Report

**Add `--report` flag generating summary:**
```markdown
# Migration Report

**Date:** YYYY-MM-DD
**Stories Migrated:** {count}
**Success:** {count}
**Failures:** {count}

## Migrated Stories
- STORY-052: 6 AC headers updated ✓
- STORY-053: 5 AC headers updated ✓
...

## Failures
- STORY-XXX: {error description}
```

**Effort:** +45 minutes

---

## Related Documents

- **INDEX.md** - RCA-012 navigation
- **REMEDIATION-PLAN.md** - Phase 4 overview (REC-4)
- **IMPLEMENTATION-GUIDE.md** - Step 4.1 (detailed execution)
- **TEMPLATE-REFACTORING.md** - REC-1 (what format migration achieves)
- **TESTING-PLAN.md** - Migration testing strategy

---

**REC-4 Status:** Ready for Implementation
**Effort:** 1.5 hours (script + testing + documentation)
**Priority:** MEDIUM (optional enhancement for consistency)
**User Decision:** Optional use (framework supports both formats)
