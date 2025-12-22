# API Documentation

Programmatic interface for feedback export/import operations.

---

## Module Import

```python
from src.feedback_export_import import (
    export_feedback_sessions,
    import_feedback_sessions,
    ExportResult,
    ImportResult,
    SanitizationConfig
)
```

---

## Export API

### export_feedback_sessions()

Export feedback sessions to portable ZIP archive with sanitization.

#### Signature

```python
def export_feedback_sessions(
    date_range: str = "last-30-days",
    sanitize: bool = True,
    output_path: Optional[str] = None,
    compression_format: str = "zip"
) -> ExportResult
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `date_range` | `str` | `"last-30-days"` | Filter sessions by date: `"last-7-days"`, `"last-30-days"`, `"last-90-days"`, `"all"` |
| `sanitize` | `bool` | `True` | Apply sanitization rules (always True for user exports) |
| `output_path` | `Optional[str]` | `None` | Custom output directory (None = current directory) |
| `compression_format` | `str` | `"zip"` | Archive format: `"zip"` or `"tar.gz"` |

#### Returns

**ExportResult** - Dataclass with export results

```python
@dataclass
class ExportResult:
    success: bool                           # True if export succeeded
    archive_path: str                       # Full path to created archive
    archive_size_bytes: int                 # Compressed archive size
    sessions_exported: int                  # Number of sessions in export
    sanitization_applied: bool              # Whether sanitization was applied
    date_range_used: str                    # Date range filter used
    execution_time_ms: int                  # Export duration in milliseconds
    replacements_made: Dict[str, int]       # Count of sanitization replacements
    warnings: List[str]                     # Non-critical warnings
```

#### Raises

| Exception | When | Recovery |
|-----------|------|----------|
| `ValueError` | Invalid `date_range` parameter | Use valid range value |
| `ValueError` | No sessions match date range | Use broader range or `"all"` |
| `IOError` | Disk full or permission denied | Free space or change output location |
| `Exception` | Export generation fails | Check logs, retry |

#### Example Usage

```python
# Basic export with defaults
result = export_feedback_sessions()

if result.success:
    print(f"✅ Exported to: {result.archive_path}")
    print(f"Sessions: {result.sessions_exported}")
    print(f"Size: {result.archive_size_bytes / 1024 / 1024:.2f} MB")
else:
    print(f"❌ Export failed")

# Custom export
result = export_feedback_sessions(
    date_range="last-90-days",
    output_path="/home/user/backups/"
)

# Check replacements
if result.sanitization_applied:
    print(f"Story IDs replaced: {result.replacements_made.get('story_ids', 0)}")
    print(f"File paths masked: {result.replacements_made.get('file_paths', 0)}")
```

---

## Import API

### import_feedback_sessions()

Import feedback sessions from exported ZIP archive.

#### Signature

```python
def import_feedback_sessions(
    archive_path: str,
    validate_integrity: bool = True,
    auto_resolve_conflicts: bool = True
) -> ImportResult
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `archive_path` | `str` | Required | Path to ZIP file (absolute or relative) |
| `validate_integrity` | `bool` | `True` | Verify SHA-256 checksums during import |
| `auto_resolve_conflicts` | `bool` | `True` | Automatically suffix duplicate session IDs |

#### Returns

**ImportResult** - Dataclass with import results

```python
@dataclass
class ImportResult:
    success: bool                           # True if import succeeded
    extracted_path: str                     # Where sessions were extracted
    sessions_imported: int                  # Number of sessions imported
    duplicate_ids_found: int                # Number of ID collisions detected
    duplicate_ids_resolved: int             # Number of collisions auto-resolved
    compatibility_status: str               # "compatible", "warning", "incompatible"
    framework_version_current: str          # Current framework version
    framework_version_exported: str         # Framework version in export
    execution_time_ms: int                  # Import duration in milliseconds
    warnings: List[str]                     # Non-critical warnings
    import_summary: str                     # Human-readable summary
```

#### Raises

| Exception | When | Recovery |
|-----------|------|----------|
| `FileNotFoundError` | Archive file not found | Verify path, use absolute path |
| `ValueError` | Invalid archive format | Re-download or request re-export |
| `ValueError` | Validation fails (missing files) | Request complete export |
| `IOError` | Extraction fails | Check permissions, disk space |

#### Example Usage

```python
# Basic import
result = import_feedback_sessions("export.zip")

if result.success:
    print(f"✅ Imported to: {result.extracted_path}")
    print(f"Sessions: {result.sessions_imported}")

    if result.duplicate_ids_found > 0:
        print(f"⚠️ Resolved {result.duplicate_ids_resolved} duplicate IDs")
        print(f"Check: conflict-resolution.log")
else:
    print(f"❌ Import failed")

# Import with custom validation
result = import_feedback_sessions(
    archive_path="/path/to/export.zip",
    validate_integrity=True,
    auto_resolve_conflicts=True
)

# Check compatibility
if result.compatibility_status == "warning":
    print(f"⚠️ Version mismatch:")
    print(f"  Exported: {result.framework_version_exported}")
    print(f"  Current: {result.framework_version_current}")
```

---

## Data Classes

### ExportResult

```python
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class ExportResult:
    """Result of export operation."""
    success: bool
    archive_path: str
    archive_size_bytes: int
    sessions_exported: int
    sanitization_applied: bool
    date_range_used: str
    execution_time_ms: int
    replacements_made: Dict[str, int] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    def __str__(self) -> str:
        """Human-readable summary."""
        return (
            f"ExportResult(success={self.success}, "
            f"sessions={self.sessions_exported}, "
            f"size={self.archive_size_bytes / 1024:.1f} KB)"
        )
```

### ImportResult

```python
@dataclass
class ImportResult:
    """Result of import operation."""
    success: bool
    extracted_path: str
    sessions_imported: int
    duplicate_ids_found: int
    duplicate_ids_resolved: int
    compatibility_status: str
    framework_version_current: str
    framework_version_exported: str
    execution_time_ms: int
    warnings: List[str] = field(default_factory=list)
    import_summary: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    def __str__(self) -> str:
        """Human-readable summary."""
        return (
            f"ImportResult(success={self.success}, "
            f"sessions={self.sessions_imported}, "
            f"duplicates={self.duplicate_ids_resolved})"
        )
```

### SanitizationConfig

```python
@dataclass
class SanitizationConfig:
    """Sanitization configuration."""
    story_id_mapping: Dict[str, str] = field(default_factory=dict)
    masked_fields: List[str] = field(default_factory=list)
    preserved_fields: List[str] = field(default_factory=list)
    rules_applied: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
```

---

## Advanced Usage

### Batch Export

```python
def export_all_projects(projects: List[str], output_dir: str):
    """Export feedback from multiple projects."""
    results = []

    for project_path in projects:
        os.chdir(project_path)
        result = export_feedback_sessions(
            date_range="all",
            output_path=output_dir
        )
        results.append(result)

    # Summary
    total_sessions = sum(r.sessions_exported for r in results)
    total_size = sum(r.archive_size_bytes for r in results)

    print(f"Exported {len(results)} projects")
    print(f"Total sessions: {total_sessions}")
    print(f"Total size: {total_size / 1024 / 1024:.2f} MB")

    return results
```

### Batch Import

```python
def import_all_archives(archive_dir: str):
    """Import all ZIP archives from directory."""
    archives = Path(archive_dir).glob("*.zip")
    results = []

    for archive in archives:
        result = import_feedback_sessions(str(archive))
        results.append(result)

    # Summary
    total_imported = sum(r.sessions_imported for r in results)
    total_conflicts = sum(r.duplicate_ids_resolved for r in results)

    print(f"Imported {len(results)} archives")
    print(f"Total sessions: {total_imported}")
    print(f"Conflicts resolved: {total_conflicts}")

    return results
```

### Custom Sanitization (Framework Maintainers Only)

```python
# NOTE: Sanitization cannot be disabled in export_feedback_sessions()
# This is internal-only for framework development

from feedback_export_import import _sanitize_content, _build_story_id_mapping

def custom_export_with_sanitization(content: str, story_ids: List[str]):
    """Apply custom sanitization rules."""
    # Build mapping
    mapping = _build_story_id_mapping(story_ids)

    # Create config
    config = SanitizationConfig(
        story_id_mapping=mapping,
        masked_fields=["project_name", "client_id"],
        preserved_fields=["operation_type", "status", "timestamp"]
    )

    # Sanitize
    sanitized = _sanitize_content(content, config)

    return sanitized, config
```

---

## Error Handling Patterns

### Try-Except Pattern

```python
try:
    result = export_feedback_sessions(date_range="last-30-days")

    if result.success:
        print(f"✅ Export successful: {result.archive_path}")
    else:
        print(f"❌ Export failed")
        for warning in result.warnings:
            print(f"  ⚠️ {warning}")

except ValueError as e:
    print(f"❌ Invalid parameters: {e}")
    print("Use: last-7-days, last-30-days, last-90-days, or all")

except IOError as e:
    print(f"❌ File system error: {e}")
    print("Check permissions and disk space")

except Exception as e:
    print(f"❌ Unexpected error: {e}")
    print("Check logs for details")
```

### Validation Pattern

```python
def safe_export(date_range: str, output_dir: str):
    """Export with validation."""
    # Validate date range
    valid_ranges = ["last-7-days", "last-30-days", "last-90-days", "all"]
    if date_range not in valid_ranges:
        raise ValueError(f"Invalid date_range. Use: {valid_ranges}")

    # Validate output directory
    if not os.path.exists(output_dir):
        raise ValueError(f"Output directory not found: {output_dir}")

    if not os.access(output_dir, os.W_OK):
        raise ValueError(f"No write permission: {output_dir}")

    # Safe to export
    return export_feedback_sessions(
        date_range=date_range,
        output_path=output_dir
    )
```

---

## Type Hints

All functions include comprehensive type hints:

```python
def export_feedback_sessions(
    date_range: str = "last-30-days",
    sanitize: bool = True,
    output_path: Optional[str] = None,
    compression_format: str = "zip"
) -> ExportResult:
    ...

def import_feedback_sessions(
    archive_path: str,
    validate_integrity: bool = True,
    auto_resolve_conflicts: bool = True
) -> ImportResult:
    ...
```

**Type checking:**
```bash
mypy src/feedback_export_import.py
# All type hints validated
```

---

## Testing

### Unit Test Examples

```python
import pytest
from feedback_export_import import export_feedback_sessions

def test_export_with_last_7_days():
    """Test export with 7-day date range."""
    result = export_feedback_sessions(date_range="last-7-days")

    assert result.success
    assert result.date_range_used == "last-7-days"
    assert result.sessions_exported >= 0
    assert os.path.exists(result.archive_path)

def test_export_with_invalid_date_range():
    """Test export rejects invalid date range."""
    with pytest.raises(ValueError, match="Invalid date_range"):
        export_feedback_sessions(date_range="invalid-range")
```

### Integration Test Example

```python
def test_export_then_import_roundtrip(temp_project_dir):
    """Test complete export→import workflow."""
    # Export
    export_result = export_feedback_sessions(date_range="all")
    assert export_result.success

    # Import
    import_result = import_feedback_sessions(export_result.archive_path)
    assert import_result.success
    assert import_result.sessions_imported == export_result.sessions_exported

    # Verify data integrity
    assert import_result.duplicate_ids_found == 0  # First import, no conflicts
```

---

## Performance Considerations

### Optimization Tips

**1. Use appropriate date range:**
```python
# Faster (fewer sessions)
export_feedback_sessions(date_range="last-7-days")

# Slower (more sessions)
export_feedback_sessions(date_range="all")
```

**2. Batch exports:**
```python
# Don't export repeatedly in loop
for project in projects:
    result = export_feedback_sessions()  # ❌ Inefficient

# Better: Export once per project
result = export_feedback_sessions(date_range="all")  # ✅ One export
```

**3. Check size before export:**
```python
import os
from pathlib import Path

feedback_dir = Path("devforgeai/feedback/sessions")
total_size = sum(f.stat().st_size for f in feedback_dir.glob("*.md"))

if total_size > 100 * 1024 * 1024:  # 100MB
    print("Warning: Large export, consider narrower date range")
```

---

## Logging

### Log Configuration

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Log Messages

**Export:**
```
2025-11-11 14:30:00 - feedback_export_import - INFO - Starting export with date_range=last-30-days
2025-11-11 14:30:01 - feedback_export_import - INFO - Found 47 sessions matching date range
2025-11-11 14:30:01 - feedback_export_import - INFO - Applying sanitization rules
2025-11-11 14:30:02 - feedback_export_import - INFO - Replaced 12 story IDs
2025-11-11 14:30:03 - feedback_export_import - INFO - Created archive: devforgeai-feedback-export-2025-11-11T14-30-00-abc12345.zip
2025-11-11 14:30:03 - feedback_export_import - INFO - Export complete (2847 ms)
```

**Import:**
```
2025-11-11 14:35:00 - feedback_export_import - INFO - Starting import from: export.zip
2025-11-11 14:35:00 - feedback_export_import - INFO - Validating archive format
2025-11-11 14:35:01 - feedback_export_import - INFO - Extracting to: devforgeai/feedback/imported/2025-11-11T14-30-00/
2025-11-11 14:35:02 - feedback_export_import - INFO - Merging 47 sessions into main index
2025-11-11 14:35:02 - feedback_export_import - INFO - Resolved 3 duplicate IDs
2025-11-11 14:35:03 - feedback_export_import - INFO - Import complete (3127 ms)
```

---

## Constants

```python
# Date range options
VALID_DATE_RANGES = ["last-7-days", "last-30-days", "last-90-days", "all"]

# Date range to days mapping
DATE_RANGE_DAYS = {
    "last-7-days": 7,
    "last-30-days": 30,
    "last-90-days": 90
}

# Archive naming
ARCHIVE_PREFIX = "devforgeai-feedback-export"

# Limits
MAX_EXPORT_SIZE_MB = 100
MAX_COLLISION_ATTEMPTS = 100

# Framework standard fields (preserved during sanitization)
FRAMEWORK_STANDARD_FIELDS = [
    "session_id",
    "operation_type",
    "operation_name",
    "status",
    "timestamp",
    "duration_ms",
    "framework_version"
]
```

---

## Helper Functions

### Public Helpers (Available for Use)

```python
# None - all helpers are module-private (_prefix)
# Use main API functions instead
```

### Private Helpers (Internal Only)

```python
# Validation
_validate_date_range(date_range: str) -> None
_validate_zip_archive(zip_path: str) -> bool
_validate_zip_contents(zip_path: str) -> Tuple[bool, List[str]]
_validate_path_traversal(path: str) -> bool
_validate_manifest(manifest: Dict) -> Tuple[bool, List[str]]

# Sanitization
_build_story_id_mapping(story_ids: List[str]) -> Dict[str, str]
_sanitize_content(content: str, config: SanitizationConfig) -> str

# Index operations
_merge_indices(main_index: Dict, imported_index: Dict) -> Dict
_generate_unique_session_id(session_id: str, existing_ids: Set[str]) -> str

# File operations
_calculate_file_sha256(file_path: str) -> str
_get_date_range_bounds(date_range: str) -> Tuple[datetime, datetime]
```

---

## Integration Examples

### CI/CD Integration

```python
# Nightly export for backup
import schedule
import time

def nightly_export():
    """Run nightly feedback export."""
    result = export_feedback_sessions(
        date_range="last-7-days",
        output_path="/backups/feedback/"
    )

    if result.success:
        print(f"✅ Backup created: {result.archive_path}")
        # Optional: Upload to cloud storage
    else:
        print(f"❌ Backup failed")
        # Send alert

schedule.every().day.at("02:00").do(nightly_export)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Web Service Endpoint

```python
from flask import Flask, jsonify, request, send_file

app = Flask(__name__)

@app.route('/api/export-feedback', methods=['POST'])
def api_export():
    """API endpoint for feedback export."""
    data = request.json
    date_range = data.get('date_range', 'last-30-days')

    result = export_feedback_sessions(date_range=date_range)

    if result.success:
        return send_file(
            result.archive_path,
            mimetype='application/zip',
            as_attachment=True
        )
    else:
        return jsonify({"error": "Export failed"}), 500

@app.route('/api/import-feedback', methods=['POST'])
def api_import():
    """API endpoint for feedback import."""
    file = request.files['archive']
    temp_path = f"/tmp/{file.filename}"
    file.save(temp_path)

    result = import_feedback_sessions(temp_path)

    return jsonify(result.to_dict())
```

---

## Related Documentation

- **Export Guide:** `export-feedback-guide.md` - User-facing export documentation
- **Import Guide:** `import-feedback-guide.md` - User-facing import documentation
- **Archive Format:** `archive-format-spec.md` - ZIP structure specification
- **Sanitization:** `sanitization-guide.md` - Privacy protection details

---

**Last Updated:** 2025-11-11
**Version:** 1.0
**Story:** STORY-017
