# Archive Format Specification

Technical specification of the feedback export ZIP archive structure and schemas.

---

## Archive Overview

**Format:** ZIP (DEFLATE compression)
**Extension:** `.zip`
**Naming:** `.devforgeai-feedback-export-{ISO8601}-{UUID}.zip`
**Compatibility:** Cross-platform (Windows, macOS, Linux)

---

## Filename Format

### Pattern

```
.devforgeai-feedback-export-{TIMESTAMP}-{UUID}.zip
```

### Components

| Component | Format | Example | Purpose |
|-----------|--------|---------|---------|
| Prefix | Fixed string | `.devforgeai-feedback-export-` | Identifies DevForgeAI exports |
| Timestamp | ISO 8601 (YYYY-MM-DDTHH-MM-SS) | `2025-11-11T14-30-00` | Export creation time |
| UUID | 8-character hex | `abc12345` | Uniqueness guarantee |
| Extension | `.zip` | `.zip` | Archive format indicator |

### Example Filenames

```
.devforgeai-feedback-export-2025-11-11T14-30-00-abc12345.zip
.devforgeai-feedback-export-2025-11-07T09-15-42-def67890.zip
.devforgeai-feedback-export-2025-10-23T16-45-11-123abc45.zip
```

---

## Directory Structure

```
.devforgeai-feedback-export-{timestamp}-{uuid}/
├── feedback-sessions/
│   ├── 2025-11-07T10-30-00-command-dev-success.md
│   ├── 2025-11-06T14-22-15-skill-qa-success.md
│   ├── 2025-11-05T11-20-30-command-create-story-partial.md
│   └── ... (all sessions matching date range)
├── index.json
└── manifest.json
```

**Root Directory:**
- Named after archive (without .zip extension)
- Contains exactly 3 items: `feedback-sessions/`, `index.json`, `manifest.json`

**feedback-sessions/ Directory:**
- Contains all session markdown files
- Filenames use ISO 8601 timestamps
- Files sorted chronologically (by filename)
- Only sessions matching date range filter

**Metadata Files:**
- `index.json` - Session metadata and searchable index
- `manifest.json` - Export metadata and sanitization rules

---

## File Schemas

### index.json Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["export_metadata", "sessions"],
  "properties": {
    "export_metadata": {
      "type": "object",
      "required": ["created_at", "exported_sessions_count", "date_range", "sanitization_applied", "framework_version"],
      "properties": {
        "created_at": {
          "type": "string",
          "format": "date-time",
          "description": "Export creation timestamp (ISO 8601 UTC)"
        },
        "exported_sessions_count": {
          "type": "integer",
          "minimum": 0,
          "description": "Number of sessions in this export"
        },
        "date_range": {
          "type": "string",
          "enum": ["last-7-days", "last-30-days", "last-90-days", "all"],
          "description": "Date range filter applied"
        },
        "date_range_start": {
          "type": "string",
          "format": "date-time",
          "description": "Start of date range (ISO 8601 UTC)"
        },
        "date_range_end": {
          "type": "string",
          "format": "date-time",
          "description": "End of date range (ISO 8601 UTC)"
        },
        "sanitization_applied": {
          "type": "boolean",
          "const": true,
          "description": "Always true for user exports"
        },
        "framework_version": {
          "type": "string",
          "pattern": "^\\d+\\.\\d+\\.\\d+$",
          "description": "DevForgeAI framework version (semver)"
        },
        "export_format_version": {
          "type": "string",
          "const": "1.0",
          "description": "Export format version"
        }
      }
    },
    "sessions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["session_id", "original_filename", "operation_type", "status", "timestamp"],
        "properties": {
          "session_id": {
            "type": "string",
            "format": "uuid",
            "description": "Unique session identifier"
          },
          "original_filename": {
            "type": "string",
            "description": "Filename in feedback-sessions/ directory"
          },
          "operation_type": {
            "type": "string",
            "enum": ["command", "skill", "subagent"],
            "description": "Type of operation"
          },
          "operation_name": {
            "type": "string",
            "description": "Command/skill/subagent name"
          },
          "status": {
            "type": "string",
            "enum": ["success", "partial", "failed"],
            "description": "Execution outcome"
          },
          "timestamp": {
            "type": "string",
            "format": "date-time",
            "description": "Session creation time (ISO 8601 UTC)"
          },
          "file_size_bytes": {
            "type": "integer",
            "minimum": 0,
            "description": "File size in bytes"
          },
          "export_filename": {
            "type": "string",
            "description": "Filename in archive"
          },
          "file_sha256": {
            "type": "string",
            "pattern": "^[a-f0-9]{64}$",
            "description": "SHA-256 checksum for integrity"
          }
        }
      }
    }
  }
}
```

---

### manifest.json Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["export_version", "created_at", "framework_version", "session_count"],
  "properties": {
    "export_version": {
      "type": "string",
      "const": "1.0",
      "description": "Export format version"
    },
    "export_format_version": {
      "type": "string",
      "const": "1.0"
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "created_by": {
      "type": "string",
      "const": "DevForgeAI Framework"
    },
    "framework_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "session_count": {
      "type": "integer",
      "minimum": 0
    },
    "file_count": {
      "type": "integer",
      "minimum": 0
    },
    "total_size_bytes": {
      "type": "integer",
      "minimum": 0
    },
    "archive_format": {
      "type": "string",
      "enum": ["zip", "tar.gz"]
    },
    "date_range": {
      "type": "object",
      "required": ["filter", "start_date", "end_date"],
      "properties": {
        "filter": {
          "type": "string",
          "enum": ["last-7-days", "last-30-days", "last-90-days", "all"]
        },
        "start_date": {
          "type": "string",
          "format": "date-time"
        },
        "end_date": {
          "type": "string",
          "format": "date-time"
        }
      }
    },
    "sanitization": {
      "type": "object",
      "required": ["applied", "rules_applied"],
      "properties": {
        "applied": {
          "type": "boolean",
          "const": true
        },
        "rules_applied": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": [
              "story_ids_replaced_with_placeholders",
              "custom_field_values_removed",
              "project_context_removed",
              "file_paths_masked",
              "repository_urls_removed"
            ]
          }
        },
        "replacement_mapping": {
          "type": "object",
          "properties": {
            "story_id_mapping": {
              "type": "object",
              "description": "Original story ID → Placeholder mapping"
            },
            "masked_fields": {
              "type": "array",
              "items": {"type": "string"}
            },
            "preserved_fields": {
              "type": "array",
              "items": {"type": "string"}
            }
          }
        }
      }
    },
    "integrity": {
      "type": "object",
      "properties": {
        "checksum_algorithm": {
          "type": "string",
          "const": "sha256"
        },
        "index_file_sha256": {
          "type": "string",
          "pattern": "^[a-f0-9]{64}$"
        },
        "session_count_verified": {
          "type": "boolean"
        },
        "all_files_present": {
          "type": "boolean"
        }
      }
    },
    "compatibility": {
      "type": "object",
      "required": ["min_framework_version", "tested_on_versions"],
      "properties": {
        "min_framework_version": {
          "type": "string",
          "pattern": "^\\d+\\.\\d+\\.\\d+$"
        },
        "tested_on_versions": {
          "type": "array",
          "items": {
            "type": "string",
            "pattern": "^\\d+\\.\\d+\\.\\d+$"
          }
        },
        "import_warnings": {
          "type": "array",
          "items": {"type": "string"}
        }
      }
    },
    "source_project": {
      "type": "object",
      "properties": {
        "identifier": {
          "type": "string",
          "description": "Anonymized project hash"
        },
        "export_location": {
          "type": "string",
          "description": "Generic location description"
        },
        "export_hostname": {
          "type": "string",
          "description": "Generic hostname (no specific machine)"
        }
      }
    }
  }
}
```

---

## Compression

### Algorithm

**Method:** ZIP DEFLATE (RFC 1951)
**Level:** 6 (default balance of speed vs compression)
**Ratio:** Typically 50-70% compression

### Size Examples

| Uncompressed | Compressed | Ratio | Sessions |
|--------------|------------|-------|----------|
| 1.5 MB | 0.8 MB | 53% | 10 |
| 8.7 MB | 4.2 MB | 48% | 50 |
| 35 MB | 18 MB | 51% | 200 |
| 140 MB | 70 MB | 50% | 1000 |

---

## Version Compatibility

### Format Version

**Current:** 1.0 (initial release)

**Future Versions:**
- 1.1: May add optional fields (backward compatible)
- 2.0: Breaking changes (incompatible with 1.x)

### Framework Version

**Compatibility Check:**
```
manifest.min_framework_version <= current_framework_version
```

**Example:**
- Export created with: Framework 1.0.0
- Import into: Framework 1.0.1
- Result: ✅ Compatible (1.0.0 <= 1.0.1)

**If incompatible:**
- Warning displayed but import proceeds
- May encounter parsing errors
- Recommendation: Upgrade framework

---

## Integrity Verification

### SHA-256 Checksums

All files include checksums for integrity verification:

**index.json:**
```json
{
  "integrity": {
    "checksum_algorithm": "sha256",
    "index_file_sha256": "abc123def456...",
    "all_files_present": true
  }
}
```

**Session files:**
```json
{
  "sessions": [
    {
      "file_sha256": "789ghi012jkl..."
    }
  ]
}
```

### Verification Process (Import)

1. Read manifest checksums
2. Calculate actual checksums for all files
3. Compare calculated vs documented
4. Warn if mismatch detected (not blocking)
5. Log integrity status

**Why Not Blocking:**
- Minor corruption shouldn't prevent import
- User can decide based on warning
- Checksums validate transport integrity

---

## Cross-Platform Compatibility

### Path Separators

**All paths use forward slashes:**
```
feedback-sessions/2025-11-07T10-30-00-command-dev-success.md  ✅
feedback-sessions\2025-11-07T10-30-00-command-dev-success.md  ❌
```

**Why:** Forward slashes work on all platforms (Windows, macOS, Linux).

### Line Endings

**Markdown files:** LF (Unix-style `\n`)
**JSON files:** LF (Unix-style `\n`)

**Why:** Consistency across platforms, smaller file size.

### Character Encoding

**All files:** UTF-8 encoding
**Supports:** Emoji 🚀, Chinese 中文, Arabic العربية, etc.

---

## Implementation Details

### Compression Settings

```python
import zipfile

with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("index.json", json.dumps(index, indent=2))
    zf.writestr("manifest.json", json.dumps(manifest, indent=2))
    for session_file in session_files:
        zf.write(session_file, arcname=f"feedback-sessions/{basename}")
```

### Deterministic Output

**Same input produces same output:**
- Session ordering: Sorted by timestamp
- JSON formatting: Consistent indentation (2 spaces)
- Path separators: Always forward slashes
- Timestamps: Always UTC

**Ensures:**
- Reproducible exports
- Easy comparison (diff two exports)
- Reliable testing

---

## Size Limits

### Maximum Export Size

**Limit:** 100 MB (compressed)

**Why:**
- Easy to email (most email limits: 25-50 MB)
- Quick to download/upload
- Prevents huge unwieldy packages
- Forces focused date ranges

**If limit exceeded:**
```
ERROR: Export would exceed 100MB limit

Estimated size: 142 MB (compressed)
Sessions: 2,847
Date range: all

Suggestion: Use narrower date range
  /export-feedback --date-range last-30-days (estimated: 35 MB)
```

---

## Security Features

### Path Traversal Prevention

**Attack Pattern (blocked):**
```
Archive contains: ../../../etc/passwd
```

**Prevention:**
- All paths validated before extraction
- Paths starting with `/` or `../` rejected
- Absolute paths blocked
- Symlinks not followed

### Safe Extraction

```python
def safe_extract(archive_path, extract_to):
    with zipfile.ZipFile(archive_path, 'r') as zf:
        for name in zf.namelist():
            # Block path traversal
            if name.startswith('/') or '..' in name:
                raise ValueError(f"Unsafe path: {name}")

            # Ensure within target directory
            full_path = os.path.join(extract_to, name)
            if not os.path.abspath(full_path).startswith(os.path.abspath(extract_to)):
                raise ValueError(f"Path escape: {name}")

        # Safe to extract
        zf.extractall(extract_to)
```

---

## Example Archive

### Small Export (10 sessions, last-7-days)

```
Archive: .devforgeai-feedback-export-2025-11-11T14-30-00-abc12345.zip
Size: 847 KB (compressed from 1.6 MB)

Contents:
.devforgeai-feedback-export-2025-11-11T14-30-00-abc12345/
├── feedback-sessions/ (10 files, 1.5 MB)
│   ├── 2025-11-11T10-00-00-command-dev-success.md (142 KB)
│   ├── 2025-11-10T14-30-15-skill-qa-partial.md (87 KB)
│   └── ... (8 more)
├── index.json (12 KB)
└── manifest.json (8 KB)
```

### Medium Export (100 sessions, last-30-days)

```
Archive: .devforgeai-feedback-export-2025-11-11T14-30-00-def67890.zip
Size: 4.2 MB (compressed from 8.7 MB)

Contents:
.devforgeai-feedback-export-2025-11-11T14-30-00-def67890/
├── feedback-sessions/ (100 files, 8.5 MB)
├── index.json (87 KB)
└── manifest.json (45 KB)
```

### Large Export (500 sessions, last-90-days)

```
Archive: .devforgeai-feedback-export-2025-11-11T14-30-00-123abc45.zip
Size: 18.7 MB (compressed from 42 MB)

Contents:
.devforgeai-feedback-export-2025-11-11T14-30-00-123abc45/
├── feedback-sessions/ (500 files, 41 MB)
├── index.json (412 KB)
└── manifest.json (187 KB)
```

---

## Migration & Evolution

### Format Versioning

**Current Version:** 1.0

**Version Compatibility:**
- Exports include `export_format_version: "1.0"` in manifest
- Imports check version before processing
- Future versions: Backward compatible when possible
- Breaking changes: Increment major version (2.0, 3.0)

### Planned Enhancements (Future)

**Version 1.1 (Potential):**
- tar.gz compression support
- Differential exports (only new sessions)
- Encrypted archives (password-protected)
- Additional metadata fields

**Version 2.0 (Potential Breaking Changes):**
- New sanitization rules
- Different directory structure
- Enhanced metadata schema
- Binary format option

---

## Validation Tools

### Manual Verification

```bash
# Unzip to temp directory
unzip .devforgeai-feedback-export-*.zip -d /tmp/verify/

# Check structure
ls /tmp/verify/.devforgeai-feedback-export-*/

# Validate JSON
cat /tmp/verify/*/index.json | jq .
cat /tmp/verify/*/manifest.json | jq .

# Count sessions
ls /tmp/verify/*/feedback-sessions/ | wc -l

# Check file sizes
du -sh /tmp/verify/*/feedback-sessions/
```

### Programmatic Validation

```python
import zipfile
import json

def validate_export_archive(archive_path):
    """Validate export archive structure and content."""
    with zipfile.ZipFile(archive_path, 'r') as zf:
        # Check required files
        namelist = zf.namelist()
        assert "index.json" in namelist
        assert "manifest.json" in namelist
        assert any(n.startswith("feedback-sessions/") for n in namelist)

        # Validate JSON schemas
        index = json.loads(zf.read("index.json"))
        manifest = json.loads(zf.read("manifest.json"))

        # Verify counts match
        assert len(index["sessions"]) == manifest["session_count"]

        return True
```

---

## Related Documentation

- **Export Guide:** `export-feedback-guide.md`
- **Import Guide:** `import-feedback-guide.md`
- **Sanitization Guide:** `sanitization-guide.md`
- **API Documentation:** `api-documentation.md`

---

**Last Updated:** 2025-11-11
**Version:** 1.0
**Story:** STORY-017
