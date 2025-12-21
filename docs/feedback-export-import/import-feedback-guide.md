# Import Feedback Guide

Complete guide to importing feedback sessions from exported packages.

---

## Overview

The `/import-feedback` command imports feedback sessions from ZIP packages created by `/export-feedback`, enabling feedback aggregation and cross-project sharing.

**Use Cases:**
- Import feedback shared by other DevForgeAI users
- Restore feedback from backups
- Aggregate feedback from multiple projects
- Framework maintainers: Collect user feedback for analysis

---

## Quick Start

**Basic import:**
```bash
/import-feedback path/to/export.zip
```

**Import from different locations:**
```bash
# Relative path
/import-feedback ./exports/feedback-export.zip

# Absolute path
/import-feedback ~/Downloads/feedback-export-2025-11-11.zip

# Windows path
/import-feedback C:\Users\Name\feedback-export.zip
```

---

## Command Syntax

```bash
/import-feedback <archive-path>
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `<archive-path>` | Yes | Path to ZIP file (absolute or relative) |

**Examples:**
- `./export.zip` - Current directory
- `../shared/export.zip` - Parent directory
- `/home/user/exports/export.zip` - Absolute path

---

## What Gets Imported?

### Session Files

All feedback sessions from the archive are extracted to:
```
devforgeai/feedback/imported/{export-timestamp}/
├── feedback-sessions/
│   ├── 2025-11-07T10-30-00-command-dev-success.md
│   ├── 2025-11-06T14-22-15-skill-qa-success.md
│   └── ...
├── index.json
└── manifest.json
```

**Key Details:**
- Directory uses timestamp from original export
- Original ZIP file is preserved (not deleted)
- Sessions are marked with `is_imported: true` flag
- Source project tracked via `imported_from` metadata

### Index Updates

Your main feedback index (`devforgeai/feedback/feedback-index.json`) is updated to include imported sessions:

**Before import:**
```json
{
  "sessions": [
    {...}, // Your original 50 sessions
  ]
}
```

**After import:**
```json
{
  "sessions": [
    {...}, // Your original 50 sessions
    {...}, // Imported session 1 (marked: is_imported: true)
    {...}, // Imported session 2 (marked: is_imported: true)
    // ... 47 more imported sessions
  ]
}
```

---

## Conflict Resolution

### Duplicate Session IDs

If imported sessions have IDs that already exist in your project:

**Automatic Resolution:**
1. Original ID detected as duplicate
2. New ID generated with suffix: `{original-id}-imported-1`
3. If that also exists: `{original-id}-imported-2`
4. Collision logged in: `devforgeai/feedback/imported/{timestamp}/conflict-resolution.log`
5. Original ID preserved in metadata for reference

**Example:**
```
Importing session: 550e8400-e29b-41d4-a716-446655440000
Status: ID already exists in main index

Resolution:
  New ID: 550e8400-e29b-41d4-a716-446655440000-imported-1
  Metadata: original_id: 550e8400-e29b-41d4-a716-446655440000
  Logged: conflict-resolution.log

Result: Both sessions preserved with different IDs
```

**Collision Log Format:**
```
2025-11-11T14:30:00Z - Session ID Collision Detected
  Original ID: 550e8400-e29b-41d4-a716-446655440000
  New ID: 550e8400-e29b-41d4-a716-446655440000-imported-1
  Source: devforgeai-feedback-export-2025-11-07T10-00-00.zip
  Action: Auto-resolved with suffix
```

### No Data Loss

- **All sessions imported** (no sessions skipped)
- **No overwrites** (original sessions never modified)
- **Unique IDs guaranteed** (automatic suffix generation)
- **Audit trail maintained** (all conflicts logged)

---

## Validation Checks

Import performs 8 validation checks before proceeding:

### 1. File Existence
```
Check: Does archive file exist?
Error: FileNotFoundError if missing
```

### 2. ZIP Format Validation
```
Check: Is file a valid ZIP archive?
Error: "Not a valid ZIP archive" if corrupted
```

### 3. Required Files Check
```
Check: Does archive contain index.json, manifest.json, feedback-sessions/?
Error: Lists missing files if incomplete
```

### 4. JSON Schema Validation
```
Check: Are index.json and manifest.json valid JSON?
Error: "Invalid JSON in {file}" if malformed
```

### 5. Manifest Required Fields
```
Check: Does manifest have export_version, created_at, framework_version?
Error: Lists missing required fields
```

### 6. Framework Version Compatibility
```
Check: Is min_framework_version <= current framework version?
Warning: "Not tested on this version" if not in tested_on_versions
```

### 7. Checksum Verification (Optional)
```
Check: Do SHA-256 checksums match for integrity?
Warning: Displayed if checksums don't match (not blocking)
```

### 8. Path Traversal Prevention
```
Check: All paths within archive are safe (no ../, no absolute paths)
Error: "Unsafe path detected" if attack attempt
```

**Validation Result:**
- ✅ All checks pass: Import proceeds
- ❌ Critical failure: Import halted with clear error
- ⚠️ Warnings: Import proceeds with notifications

---

## Output Format

### Success Message

```
✅ Feedback Import Complete

Archive: feedback-export-2025-11-11T14-30-00-abc12345.zip
Extracted to: devforgeai/feedback/imported/2025-11-11T14-30-00/

Sessions Imported: 47
Duplicate IDs Resolved: 3
  - ID ending ...440000 → ...440000-imported-1
  - ID ending ...550111 → ...550111-imported-1
  - ID ending ...660222 → ...660222-imported-1

Compatibility:
  Framework Version (Exported): 1.0.0
  Framework Version (Current): 1.0.1
  Status: ✅ Compatible
  Warnings: None

Sanitization Status:
  Applied: Yes
  Story IDs: Placeholders (STORY-001, STORY-002, etc.)
  Original IDs: Not recoverable from export

Index Updated:
  Previous sessions: 50
  Imported sessions: 47
  Total sessions: 97
  Location: devforgeai/feedback/feedback-index.json

Next Steps:
  - Browse imported sessions in devforgeai/feedback/imported/
  - Search index: /feedback-search
  - Update searchable index: /feedback-reindex
```

---

## Use Cases & Examples

### Import Shared Feedback from Another User

**Scenario:** Framework maintainer sent you export for testing.

```bash
# Download their export
# Import into your project
/import-feedback ~/Downloads/user-feedback-export.zip

# Result: Sessions imported, searchable in your index
```

### Restore from Backup

**Scenario:** Accidentally deleted feedback directory, need to restore.

```bash
# Import from backup
/import-feedback ~/backups/feedback-export-2025-11-01.zip

# Result: Feedback restored to imported/ directory
```

### Aggregate Multi-Project Feedback

**Scenario:** Running DevForgeAI on 3 projects, want consolidated feedback.

```bash
# Export from each project
cd ~/project1 && /export-feedback --date-range all
cd ~/project2 && /export-feedback --date-range all
cd ~/project3 && /export-feedback --date-range all

# Import all into single project
cd ~/devforgeai-main
/import-feedback ~/project1/devforgeai-feedback-export-*.zip
/import-feedback ~/project2/devforgeai-feedback-export-*.zip
/import-feedback ~/project3/devforgeai-feedback-export-*.zip

# Result: All 3 projects' feedback in one index
```

---

## Imported Session Metadata

All imported sessions are marked with special metadata:

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000-imported-1",
  "original_id": "550e8400-e29b-41d4-a716-446655440000",
  "is_imported": true,
  "imported_from": "sha256-hash-of-source-project",
  "imported_at": "2025-11-11T14:30:00Z",
  "was_sanitized": true,
  "operation_type": "command",
  "status": "success",
  "timestamp": "2025-11-07T10:30:00Z"
}
```

**Metadata Fields:**
- `is_imported` - Distinguishes imported from local sessions
- `imported_from` - Tracks source project (anonymized hash)
- `imported_at` - When import occurred
- `original_id` - Original session ID (before conflict resolution)
- `was_sanitized` - Indicates if content was sanitized

---

## Atomic Operations

### Import Guarantees

**All-or-Nothing:**
- If import fails, no partial state created
- Main index not modified on failure
- Extraction directory created only on success
- Original ZIP always preserved

**Atomicity Mechanism:**
1. Validate archive completely before extraction
2. Extract to temporary directory
3. Merge index in-memory
4. Write index atomically (temp file + rename)
5. Commit on success, rollback on failure

**No Risk of Corruption:**
- Original feedback never modified
- Failed imports leave no artifacts
- Main index always in valid state
- Easy to retry on failure

---

## Rollback

### Undo an Import

If you want to remove imported sessions:

```bash
# 1. Identify import directory
ls devforgeai/feedback/imported/

# 2. Delete the import directory
rm -rf devforgeai/feedback/imported/2025-11-11T14-30-00/

# 3. Rebuild index (removes deleted sessions)
/feedback-reindex
```

**Result:** Imported sessions removed, index updated.

---

## Performance

### Import Speed

| Sessions | Archive Size | Import Time | Notes |
|----------|--------------|-------------|-------|
| 10-50 | 0.5-2 MB | <1 second | Very fast |
| 50-200 | 2-8 MB | 1-2 seconds | Typical |
| 200-500 | 8-20 MB | 2-3 seconds | Near target |
| 500+ | 20-100 MB | 3-5 seconds | Large imports |

**Import is faster than export** (no compression needed, just extraction and merging).

---

## Related Documentation

- **Export Guide:** `export-feedback-guide.md` - Creating export packages
- **Sanitization Guide:** `sanitization-guide.md` - Privacy protection details
- **Conflict Resolution:** `conflict-resolution-guide.md` - Duplicate ID handling
- **Troubleshooting:** `troubleshooting-guide.md` - Error solutions
- **API Documentation:** `api-documentation.md` - Programmatic usage

---

**Last Updated:** 2025-11-11
**Version:** 1.0
**Story:** STORY-017
