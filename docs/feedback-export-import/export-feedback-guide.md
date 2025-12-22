# Export Feedback Guide

Complete guide to exporting feedback sessions from your DevForgeAI project.

---

## Overview

The `/export-feedback` command creates portable ZIP packages of your feedback sessions, with automatic sanitization to protect sensitive project data.

**Use Cases:**
- Share feedback with DevForgeAI framework maintainers
- Backup feedback sessions for your records
- Transfer feedback between environments
- Contribute to framework improvement efforts

---

## Quick Start

**Basic export (last 30 days with sanitization):**
```bash
/export-feedback
```

**Custom date range:**
```bash
/export-feedback --date-range last-7-days
/export-feedback --date-range last-90-days
/export-feedback --date-range all
```

**Custom output location:**
```bash
/export-feedback --output ~/feedback-backups/
```

---

## Command Syntax

```bash
/export-feedback [--date-range RANGE] [--sanitize true] [--output PATH]
```

### Parameters

| Parameter | Required | Default | Valid Values | Description |
|-----------|----------|---------|--------------|-------------|
| `--date-range` | No | `last-30-days` | `last-7-days`, `last-30-days`, `last-90-days`, `all` | Filter sessions by creation date |
| `--sanitize` | No | `true` | `true` only | Apply privacy sanitization (always enabled) |
| `--output` | No | Current directory | Any writable path | Custom output directory |

**Note:** Sanitization is mandatory (secure by default). The `--sanitize` parameter exists for framework consistency but cannot be disabled in user exports.

---

## What Gets Exported?

### Session Files

All feedback session files matching your date range filter from:
```
devforgeai/feedback/sessions/
```

### Metadata Files

**index.json** - Searchable session metadata:
- Session IDs and timestamps
- Operation types (command, skill)
- Execution status (success, partial, failed)
- File sizes and checksums
- Date range filter used
- Total session count

**manifest.json** - Export package metadata:
- Framework version and compatibility info
- Sanitization rules applied
- Story ID replacement mappings
- Export timestamp and creator
- File integrity checksums (SHA-256)
- Archive format and compression details

### Package Structure

```
devforgeai-feedback-export-2025-11-11T14-30-00-abc12345.zip
├── feedback-sessions/
│   ├── 2025-11-07T10-30-00-command-dev-success.md
│   ├── 2025-11-06T14-22-15-skill-qa-success.md
│   └── ... (all sessions in date range)
├── index.json
└── manifest.json
```

---

## Sanitization (Privacy Protection)

### What Gets Sanitized

**Story IDs:**
- Original: `STORY-042`, `STORY-101`, `STORY-156`
- Sanitized: `STORY-001`, `STORY-002`, `STORY-003`
- Mapping: Sequential placeholders (deterministic)

**File Paths:**
- Original: `/home/user/my-private-project/src/auth/login.py`
- Sanitized: `{REMOVED}`

**Repository URLs:**
- Original: `git@github.com:mycompany/private-repo.git`
- Sanitized: `{REMOVED}`

**Custom Field Values:**
- Original: `project_name: "MySecretProject"`
- Sanitized: `project_name: ""` (field name preserved, value removed)

### What Gets Preserved

**Framework Metadata:**
- Operation types (`command`, `skill`, `subagent`)
- Execution status (`success`, `partial`, `failed`)
- Timestamps (when feedback was created)
- Framework version
- Operation names (`/dev`, `/qa`, etc.)

**Feedback Content:**
- User observations and comments
- Issue descriptions
- Suggestions and improvements
- Framework-related context

**Why Sanitization:**
- Protects your intellectual property
- Prevents sensitive data leakage
- Allows safe sharing with maintainers
- Complies with privacy best practices

**Irreversibility:**
Once exported with sanitization, original story IDs and project details **cannot be recovered** from the archive. Keep the original unsanitized feedback in `devforgeai/feedback/sessions/` for your records.

---

## Output Format

### Success Message

```
✅ Feedback Export Complete

Archive: devforgeai-feedback-export-2025-11-11T14-30-00-abc12345.zip
Size: 4.2 MB (compressed from 8.7 MB)
Sessions: 47
Date Range: last-30-days (2025-10-12 to 2025-11-11)
Sanitization: Applied
  - Story IDs: 12 unique IDs replaced with placeholders
  - Custom fields: 8 field values removed
  - File paths: 15 paths masked
  - Repository URLs: 3 URLs removed

Package Contents:
  - feedback-sessions/: 47 session files
  - index.json: Searchable metadata
  - manifest.json: Export details and sanitization rules

Next Steps:
- Share the ZIP with DevForgeAI maintainers
- Include context about issues you encountered
- Original unsanitized feedback remains in devforgeai/feedback/sessions/
```

### Archive Filename Format

**Pattern:** `devforgeai-feedback-export-{TIMESTAMP}-{UUID}.zip`

**Example:** `devforgeai-feedback-export-2025-11-11T14-30-00-abc12345.zip`

**Components:**
- Prefix: `devforgeai-feedback-export-`
- Timestamp: ISO 8601 format (YYYY-MM-DDTHH-MM-SS)
- UUID: 8-character unique suffix (prevents collisions)
- Extension: `.zip`

**Why UUID Suffix:**
- Guarantees uniqueness even with rapid successive exports
- Prevents filename collisions when exporting multiple times per second
- Ensures deterministic naming while avoiding overwrites

---

## Date Range Filters

### Available Ranges

| Filter | Description | Sessions Included | Typical Count |
|--------|-------------|-------------------|---------------|
| `last-7-days` | Last week | Past 7 days (inclusive) | 10-30 sessions |
| `last-30-days` | Last month (default) | Past 30 days (inclusive) | 50-150 sessions |
| `last-90-days` | Last quarter | Past 90 days (inclusive) | 150-500 sessions |
| `all` | Everything | From project start to now | 500+ sessions |

### How Filtering Works

**Date calculation:**
- **Start date:** Current date minus N days (at 00:00:00 UTC)
- **End date:** Current date and time (UTC)
- **Inclusive:** Sessions exactly N days old are INCLUDED

**Example (today is 2025-11-11):**
```
--date-range last-7-days
├─ Start: 2025-11-04T00:00:00Z
├─ End: 2025-11-11T14:30:00Z (current time)
└─ Includes: All sessions from Nov 4-11
```

**Timezone:**
All timestamps are in UTC. Local timezone conversions are handled automatically.

---

## Use Cases & Examples

### Share Feedback with Maintainers

**Scenario:** You encountered a bug and want to send feedback to help improve the framework.

```bash
# Export last 7 days (recent issues)
/export-feedback --date-range last-7-days

# Result: devforgeai-feedback-export-2025-11-11T14-30-00-abc12345.zip

# Email to: devforgeai-support@example.com
# Or attach to GitHub issue
```

### Backup Before Major Changes

**Scenario:** About to upgrade framework, want backup of all feedback.

```bash
# Export everything to safe location
/export-feedback --date-range all --output ~/backups/devforgeai/

# Result: ~/backups/devforgeai/devforgeai-feedback-export-2025-11-11T14-30-00-abc12345.zip
```

### Weekly Feedback Summary

**Scenario:** Weekly routine to archive and share feedback.

```bash
# Every Monday, export last 7 days
/export-feedback --date-range last-7-days

# Review locally or share with team
```

### Debugging Session Export

**Scenario:** Specific issue occurred yesterday, need to share just recent feedback.

```bash
# Export last 7 days to focus on recent problem
/export-feedback --date-range last-7-days --output ~/Desktop/

# Smaller archive, easier to review
```

---

## Performance

### Export Speed

| Sessions | Archive Size | Export Time | Notes |
|----------|--------------|-------------|-------|
| 10-50 | 0.5-2 MB | <1 second | Very fast |
| 50-200 | 2-8 MB | 1-3 seconds | Typical 30-day export |
| 200-500 | 8-20 MB | 3-5 seconds | Near target limit |
| 500-1000 | 20-50 MB | 5-10 seconds | Approaching 100MB limit |
| 1000+ | 50-100 MB | 10-20 seconds | May hit size limit |

**If export exceeds 100MB:**
- Command fails with error message
- Suggestion: Use narrower date range
- Example: Use `last-30-days` instead of `all`

### Compression Ratio

- **Typical:** 50-70% compression
- **Best case:** 70-80% (lots of repetitive text)
- **Worst case:** 30-50% (lots of unique content)
- **Algorithm:** ZIP deflate (standard compression)

---

## File Locations

### Source (Original Feedback)

```
devforgeai/feedback/
├── sessions/
│   ├── 2025-11-07T10-30-00-command-dev-success.md     ← Original (unsanitized)
│   ├── 2025-11-06T14-22-15-skill-qa-success.md        ← Original (unsanitized)
│   └── ...
└── feedback-index.json                                 ← Master index
```

**These files are NEVER modified** by export operations.

### Export Output (Default)

```
project-root/
└── devforgeai-feedback-export-2025-11-11T14-30-00-abc12345.zip
```

### Export Output (Custom)

```bash
/export-feedback --output ~/Desktop/exports/
```

```
~/Desktop/exports/
└── devforgeai-feedback-export-2025-11-11T14-30-00-abc12345.zip
```

---

## Error Handling

### Common Errors

**"No sessions match date range"**
```
ERROR: No feedback sessions found for date range: last-7-days

Searched: devforgeai/feedback/sessions/
Found: 0 sessions in range (2025-11-04 to 2025-11-11)

Suggestions:
  - Use broader date range: --date-range last-30-days
  - Check if feedback directory exists
  - Verify feedback sessions were created
```

**Solution:** Use broader date range or check if feedback exists.

---

**"Export size exceeds 100MB limit"**
```
ERROR: Export would exceed 100MB limit

Estimated size: 142 MB (uncompressed)
Sessions: 2,847
Date range: all

Suggestion: Use narrower date range
  /export-feedback --date-range last-30-days
```

**Solution:** Filter to smaller date range.

---

**"Permission denied writing to output directory"**
```
ERROR: Cannot write to output directory

Path: /root/exports/
Error: [Errno 13] Permission denied

Suggestion: Choose writable directory
  /export-feedback --output ~/Documents/
```

**Solution:** Use directory with write permissions.

---

**"Feedback directory not found"**
```
ERROR: Feedback directory does not exist

Expected: devforgeai/feedback/sessions/
Found: Directory not found

Suggestion: No feedback has been collected yet.
  Run DevForgeAI commands (/dev, /qa, etc.) to generate feedback first.
```

**Solution:** Generate feedback by running framework commands.

---

## Advanced Usage

### Programmatic Export (Python)

```python
from src.feedback_export_import import export_feedback_sessions

# Export with custom parameters
result = export_feedback_sessions(
    date_range="last-30-days",
    sanitize=True,
    output_path="~/exports/",
    compression_format="zip"
)

# Check result
if result["success"]:
    print(f"✅ Exported to: {result['archive_path']}")
    print(f"Sessions: {result['sessions_exported']}")
    print(f"Size: {result['archive_size_bytes']} bytes")
else:
    print(f"❌ Export failed: {result.get('error')}")
```

### Automated Exports (Cron/Scheduler)

```bash
#!/bin/bash
# Weekly export script

cd /path/to/devforgeai/project
/export-feedback --date-range last-7-days --output ~/weekly-backups/

# Optional: Upload to cloud storage
# aws s3 cp devforgeai-feedback-export-*.zip s3://my-bucket/
```

---

## FAQ

**Q: Can I export without sanitization?**
A: No. Sanitization is mandatory for user exports to protect sensitive data. Only framework maintainers with special flags can export unsanitized (for internal debugging).

**Q: How do I know what was sanitized?**
A: Check `manifest.json` in the exported archive. It lists all replacement mappings and masked fields.

**Q: Is sanitization reversible?**
A: No. Once exported, original story IDs and project details cannot be recovered. Keep the original unsanitized feedback in `devforgeai/feedback/sessions/` if you need it.

**Q: Can I export multiple times?**
A: Yes. Each export gets a unique filename (UUID suffix) so they don't overwrite each other.

**Q: What format is the archive?**
A: Standard ZIP format (deflate compression). Opens with any ZIP tool on Windows, macOS, or Linux.

**Q: Can I view the export contents?**
A: Yes. Unzip the archive and read the markdown files and JSON metadata files.

**Q: How large are typical exports?**
A: 30-day exports are typically 2-10 MB (compressed). Depends on feedback volume.

**Q: What if I hit the 100MB limit?**
A: Use a narrower date range (e.g., `last-30-days` instead of `all`). The limit prevents huge packages that are hard to share.

**Q: Does export affect my original feedback?**
A: No. Original feedback in `devforgeai/feedback/sessions/` is never modified. Exports are read-only operations.

**Q: Can I export from multiple projects and merge?**
A: Yes! Export from each project, then use `/import-feedback` to merge them into a single project. See Import Guide for details.

---

## Related Documentation

- **Import Guide:** `import-feedback-guide.md` - How to import exported packages
- **Sanitization Guide:** `sanitization-guide.md` - What gets sanitized and why
- **Archive Format:** `archive-format-spec.md` - Technical specification of ZIP structure
- **Troubleshooting:** `troubleshooting-guide.md` - Common issues and solutions
- **API Documentation:** `api-documentation.md` - Programmatic usage

---

## Command Reference

**Location:** `.claude/commands/export-feedback.md`

**Implementation:** `src/feedback_export_import.py` - `export_feedback_sessions()` function

**Tests:** `tests/test_feedback_export_import.py` - 117 comprehensive tests

---

**Last Updated:** 2025-11-11
**Version:** 1.0
**Story:** STORY-017
