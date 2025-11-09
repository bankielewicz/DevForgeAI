---
id: STORY-017
title: Cross-Project Export/Import for Feedback Sessions
epic: EPIC-004
sprint: Sprint-2
status: Backlog
points: 13
priority: Medium
assigned_to: Unassigned
created: 2025-11-07
updated: 2025-11-07
tags: [feedback, export, import, portability, data-sharing, sanitization, privacy, storage]
blocked_by: STORY-013
---

# Story: Cross-Project Export/Import for Feedback Sessions

## User Story

**As a** project user running DevForgeAI workflows,
**I want** to export my feedback sessions into portable, sanitized packages and share them with DevForgeAI maintainers,
**so that** maintainers can understand issues I encountered and prioritize enhancements, while my sensitive project data remains protected.

**And as a** framework maintainer,
**I want** to import user feedback from contributed packages into my DevForgeAI project,
**so that** I can aggregate user insights, identify patterns, and make data-driven improvements to the framework.

## Acceptance Criteria

### 1. Export Command with Options
**Given** a user wants to export their feedback sessions
**When** they execute `/export-feedback [--date-range=RANGE] [--sanitize=true]`
**Then** the export command is recognized and parsed correctly
**And** supported date ranges are: `last-7-days`, `last-30-days`, `last-90-days`, `all` (default: `last-30-days`)
**And** sanitization flag defaults to `true` (secure by default)
**And** command completes successfully with confirmation message
**And** user is informed of export location and contents

---

### 2. Export Package Structure and Naming
**Given** the export operation completes successfully
**When** examining the exported file
**Then** the package is a `.zip` archive (or `.tar.gz` alternative)
**And** filename follows pattern: `.devforgeai-feedback-export-{timestamp}.zip`
**And** timestamp is ISO 8601 format: `YYYY-MM-DDTHH-MM-SS` (example: `.devforgeai-feedback-export-2025-11-07T14-30-00.zip`)
**And** archive is created in project root directory (or user-specified location via `--output`)
**And** compressed size is reasonable for sharing (typically <10MB for 30-day export)
**And** archive contents are deterministic (same input → same output for reproducibility)

---

### 3. Export Package Contents
**Given** a feedback export package is created
**When** extracting the archive
**Then** the following directory structure is present:
  - `feedback-sessions/` - Directory containing all filtered feedback session files
  - `index.json` - JSON file with metadata about exported sessions
  - `manifest.json` - Export metadata and sanitization details
**And** `feedback-sessions/` contains only files matching the date range filter
**And** file count in `feedback-sessions/` matches count in `index.json`
**And** all paths use forward slashes (cross-platform compatibility)

---

### 4. Index JSON File Format and Filtering
**Given** feedback sessions are being exported
**When** the `index.json` file is generated
**Then** it contains JSON array of session objects with structure:
```json
{
  "export_metadata": {
    "created_at": "2025-11-07T14:30:00Z",
    "exported_sessions_count": 15,
    "date_range": "last-30-days",
    "sanitization_applied": true,
    "framework_version": "1.0.1"
  },
  "sessions": [
    {
      "session_id": "550e8400-e29b-41d4-a716-446655440000",
      "original_filename": "2025-11-07T10-30-00-command-dev-success.md",
      "operation_type": "command",
      "operation_name": "/dev STORY-042",
      "status": "success",
      "timestamp": "2025-11-07T10:30:00Z",
      "file_size_bytes": 2847,
      "export_filename": "2025-11-07T10-30-00-command-dev-success.md"
    }
  ]
}
```
**And** `index.json` is sorted by timestamp (oldest first, or newest first - consistent)
**And** only sessions matching date range appear in index
**And** `sessions` array is empty if no sessions match date range
**And** index includes count of filtered sessions

---

### 5. Manifest JSON with Export Metadata and Sanitization Details
**Given** the export operation completes
**When** examining the `manifest.json` file
**Then** it contains comprehensive metadata:
```json
{
  "export_version": "1.0",
  "created_at": "2025-11-07T14:30:00Z",
  "exported_by": "DevForgeAI Framework",
  "framework_version": "1.0.1",
  "session_count": 15,
  "file_count": 15,
  "total_size_bytes": 45892,
  "date_range": {
    "filter": "last-30-days",
    "start_date": "2025-10-08T00:00:00Z",
    "end_date": "2025-11-07T23:59:59Z"
  },
  "sanitization": {
    "applied": true,
    "rules": [
      "story_ids_replaced_with_placeholders",
      "custom_field_values_removed",
      "project_context_removed",
      "sensitive_data_masked"
    ],
    "replacement_mapping": {
      "story_id_mapping": {
        "STORY-042": "STORY-001",
        "STORY-101": "STORY-002",
        "STORY-156": "STORY-003"
      },
      "field_names_preserved": [
        "operation_type",
        "status",
        "framework_version"
      ]
    }
  },
  "compatibility": {
    "min_framework_version": "1.0.0",
    "tested_on_versions": ["1.0.0", "1.0.1"]
  },
  "source_project_identifier": "hash-based-identifier"
}
```
**And** `sanitization.applied` clearly indicates if sanitization was performed
**And** replacement mappings documented for transparency
**And** manifest includes checksums (SHA-256) of all files for integrity verification

---

### 6. Sanitization Rules (Story IDs)
**Given** export with `--sanitize=true` is executed
**When** story ID references are encountered in feedback content
**Then** story IDs are replaced with sequential placeholders
**And** replacement pattern: `STORY-042` → `STORY-001`, `STORY-101` → `STORY-002`, etc.
**And** mapping is deterministic (same story ID always maps to same placeholder)
**And** mapping preserved in `manifest.json` under `sanitization.replacement_mapping.story_id_mapping`
**And** all occurrences of original story ID replaced throughout the export
**And** story ID replacement is case-sensitive
**And** numbered references (STORY-123) distinguished from narrative mentions

---

### 7. Sanitization Rules (Custom Fields and Context)
**Given** export with `--sanitize=true` is executed
**When** processing feedback content for sensitive data
**Then** custom field values are removed while field names are preserved
**And** project-specific context is removed:
  - File paths (`.../src/authentication/...` → `{PATH_REMOVED}`)
  - Repository names (`my-private-repo` → `{REPO_REMOVED}`)
  - Custom field values (user-defined fields emptied but named preserved)
  - Project IDs or internal identifiers
**And** framework-standard fields preserved (operation-type, status, timestamp, etc.)
**And** list of removed fields documented in manifest for transparency
**And** sanitization rules applied consistently across all session files
**And** original unsanitized version remains in user's `.devforgeai/feedback/` directory

---

### 8. Import Command and Basic Validation
**Given** a user has a feedback export package to import
**When** they execute `/import-feedback [file.zip]` or `/import-feedback --file=exported.zip`
**Then** the import command is recognized and executed
**And** file path can be absolute or relative
**And** import validates that file exists and is readable
**And** import validates that file is valid ZIP archive (tries unzip, reports error if corrupted)
**And** import validates that required files present (`index.json`, `manifest.json`, `feedback-sessions/`)
**And** import reports validation failures with remediation guidance
**And** import halts on critical validation failures (missing manifest, corrupted index)
**And** import logs all validation steps for debugging

---

### 9. Import Package Extraction and Placement
**Given** import validation succeeds
**When** extracting the imported package
**Then** package is extracted to `.devforgeai/feedback/imported/{timestamp}/`
**And** timestamp is ISO 8601 format matching export time for traceability
**And** extraction creates subdirectory structure: `imported/{timestamp}/feedback-sessions/`, `imported/{timestamp}/index.json`, `imported/{timestamp}/manifest.json`
**And** original ZIP file is NOT deleted (preserved for audit trail)
**And** extracted directory is readable and properly organized
**And** import progress is displayed (percentage complete during extraction)
**And** user is informed of extraction location

---

### 10. Merge Index Entries with Conflict Resolution
**Given** feedback is being imported
**When** merging imported session index with existing `.devforgeai/feedback-index.json`
**Then** sessions with new session IDs are added directly
**And** sessions with duplicate IDs trigger conflict resolution:
  - Duplicate IDs get suffix: `-imported-1`, `-imported-2`, etc.
  - Original session ID preserved in metadata for reference
  - Conflict documented in `conflict-resolution.log`
**And** index updated atomically (no partial state)
**And** merge preserves chronological ordering
**And** total session count updated in main index
**And** imported sessions marked with metadata flag: `"is_imported": true`
**And** import source documented: `"imported_from": "{manifest.source_project_identifier}"`

---

### 11. Import Compatibility Validation
**Given** package manifest is loaded during import
**When** validating compatibility
**Then** import checks that `min_framework_version` in manifest <= current framework version
**And** import warns if current version not in `tested_on_versions` list (warns but proceeds)
**And** version mismatch handled gracefully (no blocking, informational only)
**And** compatibility information logged for troubleshooting
**And** user notified of version mismatches before proceeding

---

### 12. Sanitization Transparency and Reversal Information
**Given** sanitized feedback is being imported
**When** user reviews imported sessions
**Then** manifest clearly indicates that `sanitization.applied: true`
**And** replacement mappings are available for reference
**And** user understands that original story IDs cannot be recovered from sanitized export
**And** note in manifest explains: "Story IDs replaced with placeholders for privacy. Original mapping available in manifest."
**And** imported sessions marked with sanitization flag: `"was_sanitized": true`
**And** framework includes documentation on interpreting sanitized feedback

---

## Technical Specification

### Data Models

#### Export Configuration
```yaml
export_config:
  date_range: "last-30-days"      # Options: last-7-days, last-30-days, last-90-days, all
  sanitization_enabled: true       # Default: true (secure by default)
  output_path: null                # null = use default (project root), else use specified path
  include_manifest: true           # Include manifest.json
  include_index: true              # Include index.json
  compression_format: "zip"        # Options: zip, tar.gz
  compression_level: 6             # 0-9 (higher = better compression, slower)
```

#### Export Result
```json
{
  "success": true,
  "archive_path": "/absolute/path/.devforgeai-feedback-export-2025-11-07T14-30-00.zip",
  "archive_size_bytes": 45892,
  "sessions_exported": 15,
  "sanitization_applied": true,
  "date_range_used": "last-30-days",
  "execution_time_ms": 2847,
  "replacements_made": {
    "story_ids": 42,
    "field_removals": 18
  },
  "warnings": []
}
```

#### Import Configuration
```yaml
import_config:
  archive_path: "relative/or/absolute/path/to/export.zip"
  validate_integrity: true         # Verify checksums
  auto_resolve_conflicts: true     # Auto-suffix duplicates
  preserve_original_archive: true  # Keep ZIP after extraction
```

#### Import Result
```json
{
  "success": true,
  "extracted_path": "/absolute/path/.devforgeai/feedback/imported/2025-11-07T14-30-00/",
  "sessions_imported": 15,
  "duplicate_ids_found": 0,
  "duplicate_ids_resolved": 0,
  "compatibility_status": "compatible",
  "framework_version_current": "1.0.1",
  "framework_version_exported": "1.0.0",
  "execution_time_ms": 5234,
  "warnings": [],
  "import_summary": "Successfully imported 15 sessions from export created 2025-11-07T14-30-00Z"
}
```

### API Contract

#### Export Endpoint
```python
def export_feedback_sessions(
    date_range: str = "last-30-days",           # "last-7-days"|"last-30-days"|"last-90-days"|"all"
    sanitize: bool = True,                      # True = apply sanitization rules
    output_path: Optional[str] = None,          # None = project root
    compression_format: str = "zip"             # "zip"|"tar.gz"
) -> ExportResult:
    """
    Export feedback sessions to portable, shareable package.

    Returns:
        ExportResult containing archive path, session count, and status

    Raises:
        ValueError: If date_range invalid or no sessions match filter
        IOError: If disk full or permission denied
        Exception: If export generation fails
    """
```

#### Import Endpoint
```python
def import_feedback_sessions(
    archive_path: str,                          # Path to .zip or .tar.gz file
    validate_integrity: bool = True,            # Verify SHA-256 checksums
    auto_resolve_conflicts: bool = True         # Auto-suffix duplicate IDs
) -> ImportResult:
    """
    Import feedback sessions from portable package.

    Returns:
        ImportResult containing import path, session count, and status

    Raises:
        FileNotFoundError: If archive not found
        ValueError: If archive format invalid or validation fails
        IOError: If extraction fails
    """
```

### File System Layout

**After Export:**
```
project-root/
├── .devforgeai-feedback-export-2025-11-07T14-30-00.zip  ← Export package
├── .devforgeai/
│   └── feedback/
│       ├── sessions/
│       │   ├── 2025-11-07T10-30-00-command-dev-success.md       (original)
│       │   ├── 2025-11-07T10-35-15-skill-qa-success.md          (original)
│       │   └── ...
│       └── feedback-index.json                          (original)
```

**After Import:**
```
project-root/
├── .devforgeai-feedback-export-2025-11-07T14-30-00.zip           (original export)
├── .devforgeai/
│   └── feedback/
│       ├── sessions/
│       │   └── ... (original sessions unchanged)
│       ├── imported/
│       │   └── 2025-11-07T14-30-00/
│       │       ├── feedback-sessions/
│       │       │   ├── 2025-11-07T10-30-00-command-dev-success.md      (imported)
│       │       │   ├── 2025-11-07T10-35-15-skill-qa-success.md         (imported)
│       │       │   └── ...
│       │       ├── index.json                           (exported index)
│       │       └── manifest.json                        (export metadata)
│       └── feedback-index.json                          (updated with imports)
```

### Export Package Contents (Detailed)

**.devforgeai-feedback-export-2025-11-07T14-30-00.zip:**
```
.devforgeai-feedback-export-2025-11-07T14-30-00/
├── feedback-sessions/
│   ├── 2025-11-07T10-30-00-command-dev-success.md
│   ├── 2025-11-07T10-35-15-skill-qa-success.md
│   ├── 2025-11-07T10-42-30-command-create-story-partial.md
│   └── ...
├── index.json
└── manifest.json
```

**index.json schema (detailed):**
```json
{
  "export_metadata": {
    "created_at": "2025-11-07T14:30:00Z",
    "exported_sessions_count": 15,
    "date_range": "last-30-days",
    "date_range_start": "2025-10-08T00:00:00Z",
    "date_range_end": "2025-11-07T23:59:59Z",
    "sanitization_applied": true,
    "framework_version": "1.0.1",
    "export_format_version": "1.0"
  },
  "sessions": [
    {
      "session_id": "550e8400-e29b-41d4-a716-446655440000",
      "original_filename": "2025-11-07T10-30-00-command-dev-success.md",
      "operation_type": "command",
      "operation_name": "/dev STORY-042",
      "status": "success",
      "timestamp": "2025-11-07T10:30:00Z",
      "file_size_bytes": 2847,
      "export_filename": "2025-11-07T10-30-00-command-dev-success.md",
      "file_sha256": "abc123def456..."
    }
  ]
}
```

**manifest.json schema (detailed):**
```json
{
  "export_version": "1.0",
  "export_format_version": "1.0",
  "created_at": "2025-11-07T14:30:00Z",
  "created_by": "DevForgeAI Framework",
  "framework_version": "1.0.1",
  "session_count": 15,
  "file_count": 15,
  "total_size_bytes": 45892,
  "archive_format": "zip",
  "date_range": {
    "filter": "last-30-days",
    "start_date": "2025-10-08T00:00:00Z",
    "end_date": "2025-11-07T23:59:59Z"
  },
  "sanitization": {
    "applied": true,
    "rules_applied": [
      "story_ids_replaced_with_placeholders",
      "custom_field_values_removed",
      "project_context_removed",
      "file_paths_masked"
    ],
    "replacement_mapping": {
      "story_id_mapping": {
        "STORY-042": "STORY-001",
        "STORY-101": "STORY-002",
        "STORY-156": "STORY-003"
      },
      "masked_fields": [
        "project_name",
        "repository_url",
        "custom_field_values"
      ],
      "preserved_fields": [
        "operation_type",
        "status",
        "framework_version",
        "timestamp",
        "user_feedback_text"
      ]
    }
  },
  "integrity": {
    "checksum_algorithm": "sha256",
    "index_file_sha256": "abc123...",
    "session_count_verified": true,
    "all_files_present": true
  },
  "compatibility": {
    "min_framework_version": "1.0.0",
    "tested_on_versions": ["1.0.0", "1.0.1"],
    "import_warnings": []
  },
  "source_project": {
    "identifier": "sha256-hash-of-project-root",
    "export_location": "project-root-directory",
    "export_hostname": "username-machine-name"
  }
}
```

### Business Rules

1. **Export Filtering:**
   - Date range filtering is based on session timestamp (when feedback was saved)
   - `last-30-days` = from 30 days ago to now (inclusive)
   - Sessions exactly 30 days ago are INCLUDED (>=start_date)
   - Timezone handling: Treat all timestamps as UTC for consistency

2. **Sanitization Defaults:**
   - `--sanitize=true` is DEFAULT (secure by default principle)
   - Sanitization cannot be disabled for standard exports (privacy protection)
   - Only framework maintainers with special flag can export unsanitized
   - Users always see warning if sanitization applied

3. **File Size Constraints:**
   - Single export limited to 100MB max (prevents huge packages)
   - If export would exceed 100MB, suggest narrower date range
   - Compression applied (ZIP with deflate, typically 50-70% compression ratio)

4. **ID Collision Resolution:**
   - If duplicate session_id found during import, append `-imported-1`
   - If `-imported-1` also exists, try `-imported-2`, etc.
   - Limit attempts to 100 (should never reach in practice)
   - Log all collisions with original and new IDs

5. **Archive Format:**
   - ZIP is default (better cross-platform support)
   - tar.gz available as alternative (for Unix-only users)
   - All paths use forward slashes (even on Windows) for portability

6. **Metadata Preservation:**
   - All imported sessions marked with `"is_imported": true`
   - Source of import recorded: `"imported_from": "{manifest.source_project_identifier}"`
   - Import timestamp recorded: `"imported_at": "2025-11-07T15:00:00Z"`
   - Allows filtering imported vs local feedback later

### Dependencies

- **ZIP Library:** Native library for archive creation/extraction (no external dependency)
- **JSON Processing:** Standard library JSON parsing
- **Hashing:** SHA-256 for integrity verification
- **Feedback Storage:** STORY-013 (Feedback File Persistence) for reading session files
- **Feedback Index:** STORY-016 (Searchable Metadata Index) for maintaining consolidated index
- **Feedback Templates:** STORY-010 (Feedback Template Engine) for rendered content

### Integration Points

- **Feedback Collection:** Export reads from `.devforgeai/feedback/sessions/` (created by STORY-013)
- **Feedback Index:** Export includes filtered subset of `.devforgeai/feedback/feedback-index.json`
- **Index Merging:** Import updates main index with imported sessions
- **Framework Reporting:** Exported feedback can be analyzed by DevForgeAI maintainers for insights
- **User Sharing:** Users share exported packages with maintainers via email, GitHub issues, etc.

---

## Edge Cases

### 1. Empty Date Range (No Sessions Match Filter)
**Scenario:** User exports with `--date-range=last-7-days` but no sessions created in last 7 days
**Expected:** Export succeeds but with 0 sessions, warning displayed
**Handling:** Create valid archive with empty `feedback-sessions/` directory, index shows 0 sessions
**Test:** Create feedback, wait 8+ days (mock time), attempt export with 7-day range

---

### 2. Extremely Large Export (Multiple Months of Data)
**Scenario:** User exports 90 days of feedback with 5000+ sessions (exceeds 100MB)
**Expected:** Export fails with informative error suggesting narrower date range
**Handling:** Check total size before compression, reject if would exceed limit
**Test:** Create 5000+ mock feedback sessions, verify 100MB limit enforced

---

### 3. Duplicate Session IDs During Import
**Scenario:** Importing two packages with overlapping session IDs (both contain STORY-042 feedback)
**Expected:** IDs resolved without collision, original preserved in first import
**Handling:** Auto-suffix with `-imported-N`, log collisions, update index
**Test:** Import two packages with identical session IDs, verify both preserved with different IDs

---

### 4. Corrupted Export Archive
**Scenario:** User provides `.zip` file that is incomplete or corrupted
**Expected:** Import fails with clear error message
**Handling:** Validate ZIP integrity during extraction, catch exceptions, report error
**Test:** Create truncated ZIP file (missing last 10% of data), verify import fails gracefully

---

### 5. Missing Required Files in Archive
**Scenario:** User exports with archive missing `manifest.json` or `index.json`
**Expected:** Import fails with error explaining missing file
**Handling:** Validate file presence before extraction, enumerate expected files
**Test:** Create archive missing required files, verify import fails with specific error

---

### 6. Version Mismatch (Old Framework Version Export)
**Scenario:** Importing feedback exported with Framework 0.9 into Framework 1.0.1
**Expected:** Import warns about version mismatch but proceeds (backward compatible)
**Handling:** Check `min_framework_version`, warn if current < min, continue on soft errors
**Test:** Create manifest with `min_framework_version: 2.0`, verify warning but successful import

---

### 7. Story ID Mapping Conflicts During Sanitization
**Scenario:** Two different stories map to same placeholder (STORY-001 ← ??)
**Expected:** Should never happen with sequential mapping, but mapping is idempotent
**Handling:** Use deterministic hash-based mapping, verify bijection (1-to-1 mapping)
**Test:** Sanitize multiple times, verify same IDs always map to same placeholders

---

### 8. Unicode Content in Feedback (Export/Import Round-Trip)
**Scenario:** Feedback contains emoji, Chinese characters, Arabic text, special symbols
**Expected:** Content round-trips correctly (export → import → no corruption)
**Handling:** Use UTF-8 encoding, specify encoding in manifest, test round-trip
**Test:** Include emoji (🚀), Chinese (中文), Arabic (العربية), verify integrity after import

---

### 9. Symlink Attack During Import Extraction
**Scenario:** Malicious archive contains symlink attempting to escape `.devforgeai/` directory
**Expected:** Extraction safely contained within import directory, symlink not followed
**Handling:** Use safe extraction method, validate all paths stay within target directory
**Test:** Create archive with `../../../etc/passwd` symlink, verify extraction fails or contained

---

### 10. Concurrent Export/Import Operations
**Scenario:** Two users simultaneously export while one imports
**Expected:** Operations complete independently without interference
**Handling:** Use unique filenames (timestamp), atomic operations, no locking needed
**Test:** Simulate concurrent export/import via multiple processes, verify all succeed

---

### 11. Export with No Feedback Sessions Created Yet
**Scenario:** User runs `/export-feedback` on fresh project with zero feedback sessions
**Expected:** Export succeeds with empty package, warning that no sessions to export
**Handling:** Validate that feedback directory exists, return count of 0
**Test:** Fresh project, attempt export before running any commands

---

### 12. Permission Denied on Import Directory Creation
**Scenario:** User lacks write permissions to `.devforgeai/feedback/imported/`
**Expected:** Import fails with clear error about directory permissions
**Handling:** Check directory permissions before import, provide guidance on fixing
**Test:** Create read-only `.devforgeai/` directory, attempt import

---

### 13. Archive Filename Already Exists
**Scenario:** User exports twice on same day (same timestamp down to second)
**Expected:** Second export either overwrites or gets UUID suffix in filename
**Handling:** Check if file exists, append UUID if collision detected
**Test:** Export, wait <1 second, export again

---

### 14. Sanitization with Special Characters in Story Names
**Scenario:** Story names contain special characters: `STORY-#42`, `STORY(Draft)`, etc.
**Expected:** Sanitization handles all characters correctly in mapping
**Handling:** Escape special characters in JSON, preserve in mapping dict
**Test:** Create feedback with non-standard story ID formats, verify sanitization works

---

### 15. Import with Pre-Existing Imported Sessions from Same Source
**Scenario:** User imports same export package twice (realizes they did it twice)
**Expected:** Second import detects duplicate source, warns, still succeeds with new IDs
**Handling:** Track source_project identifier in metadata, warn of re-import
**Test:** Import package, import same package again

---

## Data Validation Rules

1. **Date Range Validation:**
   - Must be one of: `last-7-days`, `last-30-days`, `last-90-days`, `all`
   - Case-sensitive
   - Cannot be null or empty
   - Day calculation includes current day (0-N days ago, inclusive)

2. **Archive Path Validation:**
   - Must point to readable file
   - Must be valid ZIP or tar.gz format
   - Cannot be directory path
   - Cannot contain path traversal sequences (`../`, `..\\`)

3. **Session ID Validation (Import):**
   - Must be valid UUID format (36 chars with hyphens)
   - No duplicates allowed (auto-resolve with suffixes)
   - Must match session_id in both index.json and session files

4. **Manifest Validation:**
   - Required fields: export_version, created_at, session_count, framework_version
   - Schema version must be compatible (1.0 currently supported)
   - Timestamp must be valid ISO 8601 format

5. **Index Validation:**
   - Must be valid JSON
   - Sessions array must exist (can be empty)
   - Each session must have: session_id, timestamp, operation_type, status
   - Session count must match file count in feedback-sessions/

6. **File Path Validation:**
   - All paths in archive must be within extracted directory
   - No absolute paths allowed
   - No path traversal escape attempts
   - Forward slashes only (cross-platform)

---

## Non-Functional Requirements

### Performance
- **Export operation:** <5 seconds for typical 30-day export (100-200 sessions)
- **Import operation:** <3 seconds for typical package extraction
- **Compression:** ZIP deflate compression, typically 50-70% reduction
- **Archive generation:** Parallel file reading (if available), streaming writes
- **Sanitization:** <100ms processing overhead per session (minimal impact)

### Security & Privacy
- **Sanitization accuracy:** 100% - All story IDs replaced correctly
- **Data scrubbing:** Complete removal of sensitive fields (no partial masking)
- **Symlink safety:** Archive extraction prevents symlink attacks via safe path validation
- **File permissions:** Archive created with 0600 permissions (user read/write only)
- **No cleartext secrets:** Framework ensures no API keys, tokens, or credentials in exported feedback

### Reliability
- **Data integrity:** SHA-256 checksums verify all files after import
- **Atomic operations:** Export and import use atomic write patterns (no partial state)
- **Graceful failure:** All errors provide actionable guidance for recovery
- **Backward compatibility:** Imports work across framework versions (with warnings)
- **Audit trail:** All export/import operations logged with timestamps and parameters

### Usability
- **Clear messaging:** User informed of export/import progress and results
- **Error guidance:** All validation failures provide remediation steps
- **Progress indication:** Large operations (>10s) show percentage complete
- **Default security:** Sanitization enabled by default (no opt-in required)
- **Cross-platform:** Works on Linux, macOS, Windows with same commands/paths

### Maintainability
- **Code clarity:** Export/import logic well-documented with inline comments
- **Extensibility:** Archive format supports future metadata additions
- **Diagnostic info:** Manifest and logs enable troubleshooting
- **Format stability:** Export format versioned for future compatibility
- **Testing:** All operations include unit tests, integration tests, and edge case coverage

### Scalability
- **File count:** Support 10,000+ sessions in single export
- **Archive size:** Compress to <100MB for easy sharing
- **Batch operations:** Allow multiple exports/imports in single session
- **Memory efficiency:** Stream large files (don't load entire archive in memory)
- **Performance degradation:** Linear growth with session count (no exponential complexity)

---

## Definition of Done

### Implementation
- [ ] `/export-feedback` command created with argument parsing
  - [ ] `--date-range` parameter with validation (last-7-days, last-30-days, last-90-days, all)
  - [ ] `--sanitize` parameter (default true)
  - [ ] `--output` parameter for custom output path
- [ ] Export package generation
  - [ ] ZIP archive creation with deflate compression
  - [ ] Filename follows pattern: `.devforgeai-feedback-export-{timestamp}.zip`
  - [ ] Directory structure: `feedback-sessions/`, `index.json`, `manifest.json`
- [ ] Sanitization implementation
  - [ ] Story ID replacement with sequential placeholders (STORY-001, STORY-002, etc.)
  - [ ] Custom field value removal (preserve field names)
  - [ ] Project context removal (file paths, repo names, identifiers)
  - [ ] Deterministic mapping (same input → same output across exports)
- [ ] Index JSON generation
  - [ ] Proper schema with session metadata
  - [ ] Filtered by date range
  - [ ] Correct session count matching file count
- [ ] Manifest JSON generation
  - [ ] Complete metadata (version, dates, sanitization rules, compatibility)
  - [ ] Replacement mappings documented
  - [ ] SHA-256 checksums for integrity verification
- [ ] `/import-feedback` command created with argument parsing
  - [ ] File path parameter (absolute or relative)
  - [ ] Archive validation (ZIP format, required files present)
  - [ ] Compatibility checking (version comparison)
  - [ ] Extract to `.devforgeai/feedback/imported/{timestamp}/`
- [ ] Conflict resolution during import
  - [ ] Detect duplicate session IDs
  - [ ] Auto-suffix duplicates (e.g., `-imported-1`, `-imported-2`)
  - [ ] Log all collisions
- [ ] Index merging
  - [ ] Update main feedback index with imported sessions
  - [ ] Preserve chronological ordering
  - [ ] Mark imported sessions with metadata flags
  - [ ] Atomic merge (no partial state)

### Quality
- [ ] All 12 acceptance criteria have passing tests
- [ ] Edge cases covered (all 15 scenarios tested)
- [ ] Data validation enforced (6 validation categories)
- [ ] NFRs met (export <5s, import <3s, 100% sanitization accuracy, secure by default)
- [ ] Code coverage >95% for export/import logic
- [ ] No hardcoded file paths (uses framework standards)
- [ ] Security validated (no symlink attacks, no data leakage)

### Testing
- [ ] Unit tests: Date range filtering (20+ cases)
- [ ] Unit tests: Sanitization logic (30+ cases - story ID mapping, field removal, context masking)
- [ ] Unit tests: Archive creation (15+ cases - naming, structure, compression)
- [ ] Unit tests: Manifest generation (20+ cases - schema, validation, checksums)
- [ ] Unit tests: Import validation (25+ cases - ZIP format, required files, schema)
- [ ] Unit tests: Conflict resolution (15+ cases - ID collisions, suffixing)
- [ ] Integration tests: End-to-end export (create sessions → export → validate package)
- [ ] Integration tests: End-to-end import (extract → validate → merge → verify)
- [ ] E2E test: Export then import round-trip (verify data integrity)
- [ ] E2E test: Sanitization verification (all sensitive data masked)
- [ ] E2E test: Duplicate ID handling (import same package twice)
- [ ] E2E test: Cross-platform (Linux, macOS, Windows)
- [ ] E2E test: Large export (1000+ sessions) within 100MB limit

### Documentation
- [ ] Export command usage guide (syntax, examples, troubleshooting)
- [ ] Import command usage guide (syntax, examples, troubleshooting)
- [ ] Sanitization explanation (what's masked, what's preserved, why)
- [ ] Archive format specification (ZIP structure, file schemas, version info)
- [ ] Conflict resolution procedure (how to handle duplicate IDs)
- [ ] Troubleshooting guide (common issues and solutions)
- [ ] API documentation for programmatic use (export_feedback, import_feedback functions)

### Release Readiness
- [ ] Export creates archive in readable format for sharing
- [ ] Import validates archive integrity before extraction
- [ ] Sanitization enabled by default (secure defaults principle)
- [ ] All operations provide clear success/failure messages
- [ ] Logs include timestamps and operation details
- [ ] User can export and share feedback without exposing sensitive data
- [ ] Framework maintainers can import and analyze aggregate feedback

---

## Implementation Notes

### Sanitization Algorithm (Recommended)

**Step 1: Build Story ID Mapping**
```
- Scan all feedback content for story ID patterns (STORY-\d+)
- Collect unique story IDs: [STORY-042, STORY-101, STORY-156]
- Sort alphabetically
- Map sequentially: STORY-042→STORY-001, STORY-101→STORY-002, STORY-156→STORY-003
```

**Step 2: Apply Story ID Replacements**
```
- Read each feedback session file
- Use regex: s/STORY-\d+/STORY-{mapped_id}/g for exact matches
- Preserve replacements in manifest
- Document mapping in index.json
```

**Step 3: Remove Custom Fields**
```
- Parse YAML frontmatter
- Identify custom fields (not in framework standard list)
- Set values to empty or null
- Preserve field names for schema consistency
```

**Step 4: Mask Project Context**
```
- Remove file paths: Replace /path/to/project with {REMOVED}
- Remove repo names: Replace git@github.com:user/repo with {REMOVED}
- Remove identifiers: Hash-based project IDs removed
- Preserve timestamps and operational metadata
```

### Archive Creation (Recommended)

**Use Python zipfile library (standard, cross-platform):**
```python
import zipfile
import os

with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    # Add feedback sessions
    for session_file in feedback_files:
        zf.write(session_file, arcname=f"feedback-sessions/{basename}")

    # Add index.json
    zf.writestr("index.json", index_json_content)

    # Add manifest.json
    zf.writestr("manifest.json", manifest_json_content)
```

**Why zipfile:**
- Standard Python library (no external dependency)
- Cross-platform (Windows, macOS, Linux)
- Good compression (deflate)
- Readily extractable by users

### Import Extraction (Recommended)

**Use Python zipfile for extraction with safety checks:**
```python
def safe_extract(archive_path, extract_to):
    """Extract archive safely, preventing symlink attacks."""
    with zipfile.ZipFile(archive_path, 'r') as zf:
        # Validate all paths
        for name in zf.namelist():
            # Check for path traversal
            if name.startswith('/') or '..' in name:
                raise ValueError(f"Unsafe path in archive: {name}")

            # Ensure path within target directory
            full_path = os.path.join(extract_to, name)
            if not os.path.abspath(full_path).startswith(os.path.abspath(extract_to)):
                raise ValueError(f"Path escape attempt: {name}")

        # Safe to extract
        zf.extractall(extract_to)
```

**Why safe extraction:**
- Prevents symlink attacks
- Prevents directory traversal (`../../../etc/passwd`)
- Validates all paths before extraction
- Provides clear error on security violations

### Progress Indication

**For large operations:**
```
Export Progress: [████████████░░░░░░░░░░░░░░░░░░░░░░░] 35% (35/100 sessions)
Time elapsed: 1m 23s | Estimated remaining: 2m 34s
```

---

## Workflow History

- **2025-11-07:** Story created from EPIC-005 (Framework Integration)
- **2025-11-07:** Comprehensive AC (12 criteria) + edge cases (15) + NFRs + technical spec created
- **2025-11-07:** User story refined for clarity and security emphasis

---

## References

- **Related:** STORY-013 (Feedback File Persistence - provides session files)
- **Related:** STORY-016 (Searchable Metadata Index - maintains consolidated index)
- **Related:** STORY-010 (Feedback Template Engine - provides rendered feedback content)
- **Related:** EPIC-005 (Framework Integration - parent epic)
- **Tech:** ZIP archive format (ISO 26262 standard)
- **Tech:** JSON schemas (RFC 7159)
- **Tech:** UTF-8 encoding (RFC 3629)
- **Security:** Path traversal prevention (OWASP)
- **Security:** Symlink attack prevention (secure file operations)
