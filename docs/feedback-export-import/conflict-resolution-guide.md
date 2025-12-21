# Conflict Resolution Guide

Understanding and managing duplicate session IDs during feedback import.

---

## Overview

When importing feedback packages, session ID conflicts can occur if the same session appears in multiple imports. DevForgeAI automatically resolves conflicts using an ID suffixing strategy.

**Automatic Resolution:** No user intervention required
**Data Preservation:** All sessions imported (no data loss)
**Audit Trail:** All conflicts logged

---

## What Is a Conflict?

**Conflict occurs when:**
- Importing a session with ID that already exists in your main feedback index
- Happens when:
  - Importing same package twice
  - Importing from multiple sources with overlapping sessions
  - Re-importing after partial delete

**Example:**
```
Your index has: session-id-123
Importing:      session-id-123  ← CONFLICT!
```

---

## Automatic Resolution Strategy

### Step-by-Step Process

**1. Detect Conflict**
```
Importing session: 550e8400-e29b-41d4-a716-446655440000
Checking main index...
Status: ID already exists ❌
```

**2. Generate Unique ID**
```
Original: 550e8400-e29b-41d4-a716-446655440000
Attempt 1: 550e8400-e29b-41d4-a716-446655440000-imported-1
Check: Available ✅
New ID: 550e8400-e29b-41d4-a716-446655440000-imported-1
```

**3. Preserve Original ID**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000-imported-1",
  "original_id": "550e8400-e29b-41d4-a716-446655440000",
  "is_imported": true,
  "imported_at": "2025-11-11T14:30:00Z"
}
```

**4. Log Collision**
```
devforgeai/feedback/imported/2025-11-11T14-30-00/conflict-resolution.log

2025-11-11T14:30:00Z - Session ID Collision
  Original ID: 550e8400-e29b-41d4-a716-446655440000
  New ID: 550e8400-e29b-41d4-a716-446655440000-imported-1
  Source: feedback-export-2025-11-07T10-00-00-abc12345.zip
  Resolution: Auto-suffix applied
  Status: Resolved
```

**5. Update Index**
```
Main index updated atomically:
  - Original session preserved (ID: ...440000)
  - Imported session added (ID: ...440000-imported-1)
  - Total sessions: increased by 1
```

---

## Suffix Generation

### Algorithm

**Pattern:** `{original-id}-imported-{N}`

**Collision Counter:**
```
-imported-1  (first collision)
-imported-2  (if -imported-1 also exists)
-imported-3  (if -imported-2 also exists)
...
-imported-N  (up to MAX_COLLISION_ATTEMPTS = 100)
```

**Example Progression:**
```
Original session:   550e8400-e29b-41d4-a716-446655440000
First import:       550e8400-e29b-41d4-a716-446655440000-imported-1
Second import:      550e8400-e29b-41d4-a716-446655440000-imported-2
Third import:       550e8400-e29b-41d4-a716-446655440000-imported-3
```

**Why Sequential:**
- Predictable (users can anticipate suffix)
- Auditable (clear collision count)
- Reversible (can map back to original)

---

## Collision Scenarios

### Scenario 1: Import Same Package Twice

**Setup:**
```bash
# First import
/import-feedback export-2025-11-07.zip
# Result: 50 sessions imported with original IDs

# Second import (same package)
/import-feedback export-2025-11-07.zip
# Result: 50 sessions imported with -imported-1 suffix
```

**Outcome:**
```
Main index now has:
  - 50 original sessions (from first import)
  - 50 duplicate sessions (with -imported-1 suffix)
  - Total: 100 sessions

All conflicts logged in: conflict-resolution.log
```

---

### Scenario 2: Import from Multiple Overlapping Sources

**Setup:**
```bash
# Project A exports (sessions 1-50)
cd ~/project-a
/export-feedback --date-range last-30-days
# Result: export-a.zip (50 sessions)

# Project B exports (sessions 40-70, overlaps with A on 40-50)
cd ~/project-b
/export-feedback --date-range last-30-days
# Result: export-b.zip (30 sessions, 10 overlap with A)

# Main project imports both
cd ~/devforgeai-main
/import-feedback ~/project-a/export-a.zip  # 50 sessions imported
/import-feedback ~/project-b/export-b.zip  # 30 sessions, 10 conflicts
```

**Outcome:**
```
Sessions 1-39:  From export-a (original IDs)
Sessions 40-50: From export-a (original IDs)
Sessions 40-50: From export-b (IDs with -imported-1 suffix) ← Duplicates
Sessions 51-70: From export-b (original IDs)

Total: 80 sessions (50 from A + 30 from B, with 10 duplicates resolved)
```

---

### Scenario 3: Partial Re-Import After Deletion

**Setup:**
```bash
# Import package
/import-feedback export.zip
# Result: 50 sessions imported

# Delete some imported sessions manually
rm devforgeai/feedback/imported/2025-11-11T14-30-00/feedback-sessions/2025-11-07*.md

# Rebuild index
/feedback-reindex

# Re-import same package (to restore deleted sessions)
/import-feedback export.zip
```

**Outcome:**
```
Deleted sessions: Restored with -imported-1 suffix
Remaining sessions: Now appear twice (original + -imported-1)

Recommendation: Delete entire import directory before re-import
```

---

## Conflict Logs

### Log Format

**Location:** `devforgeai/feedback/imported/{timestamp}/conflict-resolution.log`

**Content:**
```
2025-11-11T14:30:00Z - Session ID Collision Detected
  Import Source: feedback-export-2025-11-07T10-00-00-abc12345.zip
  Original ID: 550e8400-e29b-41d4-a716-446655440000
  New ID: 550e8400-e29b-41d4-a716-446655440000-imported-1
  Resolution: Auto-suffix applied
  Status: Resolved successfully

2025-11-11T14:30:05Z - Session ID Collision Detected
  Import Source: feedback-export-2025-11-07T10-00-00-abc12345.zip
  Original ID: 661f9511-f39c-52e5-b827-557766551111
  New ID: 661f9511-f39c-52e5-b827-557766551111-imported-1
  Resolution: Auto-suffix applied
  Status: Resolved successfully

2025-11-11T14:30:10Z - Import Summary
  Total Sessions: 50
  Conflicts Detected: 3
  Conflicts Resolved: 3
  Failed Resolutions: 0
```

---

## Manual Conflict Resolution

### When Automatic Resolution Insufficient

**Rare case:** Need to merge duplicate sessions (not just import both)

**Manual Process:**
1. Identify duplicate sessions (check conflict log)
2. Review both versions (original vs imported)
3. Choose which to keep
4. Delete the other session file
5. Rebuild index: `/feedback-reindex`

**Example:**
```bash
# Find duplicates
grep "imported-1" devforgeai/feedback/feedback-index.json

# Review both versions
cat devforgeai/feedback/sessions/2025-11-07T10-00-00-command-dev-success.md
cat devforgeai/feedback/imported/*/feedback-sessions/2025-11-07T10-00-00-command-dev-success.md

# Delete one (if truly duplicate content)
rm devforgeai/feedback/imported/*/feedback-sessions/2025-11-07T10-00-00-command-dev-success.md

# Rebuild index
/feedback-reindex
```

---

## Prevention Strategies

### Avoid Conflicts Entirely

**1. Don't Import Same Package Twice**
```bash
# Keep track of what you've imported
ls devforgeai/feedback/imported/
# Check timestamp before re-import
```

**2. Export with Unique Timestamps**
```bash
# Exports automatically get unique UUID suffix
# Different timestamps prevent most conflicts
```

**3. Delete Before Re-Import**
```bash
# If you must re-import, delete old import first
rm -rf devforgeai/feedback/imported/2025-11-11T14-30-00/
/feedback-reindex
# Then re-import
/import-feedback export.zip
```

---

## Edge Cases

### Case 1: 100 Collisions (Unlikely)

**Scenario:** Importing packages where same session appears 100+ times

**Behavior:**
- First 100 collisions: Auto-resolved with -imported-1 through -imported-100
- After 100: Import fails with error

**Solution:** This is pathological (shouldn't happen in practice). Delete old imports before re-importing.

---

### Case 2: Different Content, Same ID

**Scenario:** Two different sessions happen to have identical UUIDs (extremely rare)

**Behavior:**
- Automatic suffix applied (both sessions preserved)
- User should manually review to determine if truly duplicate
- Collision logged for audit

**Solution:** Review conflict log, compare session content, delete one if true duplicate.

---

### Case 3: Metadata-Only Conflict

**Scenario:** Session ID conflicts but file content is identical

**Behavior:**
- Still imported with suffix (duplicate preserved)
- User can manually deduplicate later

**Future Enhancement:** Content-based deduplication (detect identical files)

---

## Troubleshooting

**"Too many collision attempts (100)"**
- Delete old import directories
- Clean up main index
- Re-import from fresh state

**"Conflict log file not found"**
- No conflicts occurred during import
- Check if import completed successfully

**"Original ID not in metadata"**
- Bug in conflict resolution
- Report to DevForgeAI maintainers

---

## Related Documentation

- **Import Guide:** `import-feedback-guide.md`
- **Export Guide:** `export-feedback-guide.md`
- **Troubleshooting:** `troubleshooting-guide.md`

---

**Last Updated:** 2025-11-11
**Version:** 1.0
**Story:** STORY-017
