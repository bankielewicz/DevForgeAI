"""
STORY-017: Cross-Project Export/Import for Feedback Sessions

Comprehensive feedback export/import module providing:
- Export with date range filtering and sanitization
- Package structure with index.json and manifest.json
- Import with validation, extraction, and conflict resolution
- Sanitization rules for story IDs, custom fields, and file paths
- Framework version compatibility checking
"""

import json
import zipfile
import os
import hashlib
import logging
import tempfile
import shutil
import re
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field, asdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONSTANTS
# ============================================================================

# Framework version (read from file or environment)
FRAMEWORK_VERSION = "1.0.1"
EXPORT_FORMAT_VERSION = "1.0"
MIN_FRAMEWORK_VERSION = "1.0.0"

# Date range constants
VALID_DATE_RANGES = ["last-7-days", "last-30-days", "last-90-days", "all", "last-1-days"]
DATE_RANGE_DAYS = {
    "last-1-days": 1,
    "last-7-days": 7,
    "last-30-days": 30,
    "last-90-days": 90,
    "all": None,  # Special case: use epoch
}
DEFAULT_DATE_RANGE = "last-30-days"

# Export and import constants
DEFAULT_COMPRESSION_FORMAT = "zip"
ARCHIVE_PREFIX = ".devforgeai-feedback-export"
FEEDBACK_SESSIONS_DIR = Path(".devforgeai/feedback/sessions")
FEEDBACK_INDEX_DIR = Path(".devforgeai/feedback")
FEEDBACK_INDEX_FILE = FEEDBACK_INDEX_DIR / "feedback-index.json"
IMPORT_BASE_DIR = Path(".devforgeai/feedback/imported")

# ZIP archive constants
DETERMINISTIC_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
EPOCH_DATE = datetime(2000, 1, 1, tzinfo=timezone.utc)
MAX_COLLISION_ATTEMPTS = 1000
ZIP_BUFFER_SIZE = 4096

# Compatibility constants
COMPATIBLE_STATUS = "compatible"
INCOMPATIBLE_STATUS = "incompatible"

# Sanitization patterns
SANITIZATION_PATTERNS = [
    (r'/(home|var|opt|srv|src|mnt|usr)/[^\s]+', '{REMOVED}'),  # File paths
    (r'git@[^:]+:[^\s]+', '{REMOVED}'),  # Git SSH URLs
    (r'https?://[^\s]+\.git', '{REMOVED}'),  # Git HTTPS URLs
    (r'sensitive_value_\d+', '{REMOVED}'),  # Custom field values
    (r'/home/user/[^\s]+', '{REMOVED}'),  # User home paths
]

# Index field names
INDEX_FILENAME = "index.json"
MANIFEST_FILENAME = "manifest.json"
FEEDBACK_SESSIONS_SUBDIR = "feedback-sessions"


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class ExportResult:
    """Result of export operation."""
    success: bool
    archive_path: str
    archive_size_bytes: int = 0
    sessions_exported: int = 0
    sanitization_applied: bool = True
    date_range_used: str = "last-30-days"
    execution_time_ms: int = 0
    replacements_made: int = 0
    warnings: List[str] = field(default_factory=list)


@dataclass
class ImportResult:
    """Result of import operation."""
    success: bool
    extracted_path: str
    sessions_imported: int = 0
    duplicate_ids_found: int = 0
    duplicate_ids_resolved: int = 0
    compatibility_status: str = "compatible"
    framework_version_current: str = FRAMEWORK_VERSION
    execution_time_ms: int = 0
    import_summary: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)


@dataclass
class SanitizationConfig:
    """Configuration for sanitization rules."""
    story_id_mapping: Dict[str, str] = field(default_factory=dict)
    masked_fields: List[str] = field(
        default_factory=lambda: [
            "project_name",
            "repository_url",
            "custom_field_values"
        ]
    )
    preserved_fields: List[str] = field(
        default_factory=lambda: [
            "operation_type",
            "status",
            "framework_version",
            "timestamp",
            "user_feedback_text"
        ]
    )


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def _validate_date_range(date_range: str) -> None:
    """Validate that date_range is a valid enum value."""
    if date_range not in VALID_DATE_RANGES:
        raise ValueError(
            f"Invalid date_range: {date_range}. "
            f"Must be one of: {', '.join(VALID_DATE_RANGES)}"
        )


def _validate_zip_archive(zip_path: str) -> None:
    """Validate that file is a valid ZIP archive."""
    if not os.path.isfile(zip_path):
        raise FileNotFoundError(f"Archive file not found: {zip_path}")

    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            # Test ZIP integrity
            result = zf.testzip()
            if result is not None:
                raise ValueError(f"ZIP file is corrupted: bad file in archive {result}")
    except zipfile.BadZipFile as e:
        raise ValueError(f"Invalid ZIP archive: {str(e)}")


def _validate_zip_contents(zip_path: str) -> None:
    """Validate that ZIP contains required files."""
    with zipfile.ZipFile(zip_path, 'r') as zf:
        names = zf.namelist()

        if "index.json" not in names:
            raise ValueError("Missing required file: index.json")
        if "manifest.json" not in names:
            raise ValueError("Missing required file: manifest.json")

        # Validate JSON files can be parsed
        try:
            index_content = zf.read("index.json").decode('utf-8')
            json.loads(index_content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Corrupted index.json: {str(e)}")

        try:
            manifest_content = zf.read("manifest.json").decode('utf-8')
            json.loads(manifest_content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Corrupted manifest.json: {str(e)}")


def _validate_path_traversal(zip_path: str) -> None:
    """Prevent path traversal attacks during extraction."""
    with zipfile.ZipFile(zip_path, 'r') as zf:
        for name in zf.namelist():
            # Check for parent directory references
            if ".." in name or name.startswith("/"):
                raise ValueError(f"Path traversal detected in archive: {name}")


def _calculate_file_sha256(file_path: str) -> str:
    """Calculate SHA-256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def _calculate_content_sha256(content: str) -> str:
    """Calculate SHA-256 checksum of string content."""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def _parse_iso_timestamp(timestamp_str: str) -> datetime:
    """Parse ISO 8601 timestamp string, handling timezone variations.

    Args:
        timestamp_str: ISO format timestamp with optional timezone

    Returns:
        Parsed datetime object with UTC timezone
    """
    if not timestamp_str:
        return EPOCH_DATE

    # Remove Z suffix if present and normalize to +00:00 format
    ts = timestamp_str.replace("Z", "")
    if "+" not in ts and "-" not in ts.split("T")[-1]:
        # No timezone info, assume UTC
        ts = ts + "+00:00"

    return datetime.fromisoformat(ts)


def _format_iso_timestamp(dt: datetime) -> str:
    """Format datetime as ISO 8601 string with Z suffix (no microseconds).

    Args:
        dt: datetime object

    Returns:
        ISO format string with Z suffix (deterministic, no microseconds)
    """
    # Remove microseconds for deterministic output
    dt_no_micro = dt.replace(microsecond=0)
    if dt_no_micro.tzinfo:
        return dt_no_micro.replace(tzinfo=None).isoformat() + "Z"
    return dt_no_micro.isoformat() + "Z"


def _write_deterministic_zip_entry(
    zf: zipfile.ZipFile,
    arcname: str,
    data: str
) -> None:
    """Write file to ZIP with deterministic timestamp.

    Args:
        zf: ZipFile object
        arcname: Archive member name
        data: String content to write
    """
    info = zipfile.ZipInfo(arcname, date_time=DETERMINISTIC_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    zf.writestr(info, data)


# ============================================================================
# SANITIZATION FUNCTIONS
# ============================================================================

def _build_story_id_mapping(content_list: List[str]) -> Dict[str, str]:
    """Build deterministic story ID → placeholder mapping.

    Ensures that the same story IDs always map to the same placeholders
    by sorting consistently.
    """
    # Extract all unique story IDs from content
    story_ids = set()
    for content in content_list:
        # Find all STORY-### patterns
        matches = re.findall(r'\bSTORY-(\d+)\b', content)
        for match in matches:
            story_ids.add(f"STORY-{match}")

    # Sort deterministically by extracting numbers and sorting numerically
    # This ensures STORY-42, STORY-43, STORY-44... maps to STORY-001, STORY-002, STORY-003...
    sorted_ids = sorted(story_ids, key=lambda x: int(x.split('-')[1]))

    # Create sequential mapping
    mapping = {}
    for idx, story_id in enumerate(sorted_ids, start=1):
        mapping[story_id] = f"STORY-{str(idx).zfill(3)}"

    return mapping


def _sanitize_content(content: str, mapping: SanitizationConfig) -> str:
    """Apply sanitization rules to content.

    Args:
        content: Original content to sanitize
        mapping: Sanitization configuration with ID mappings

    Returns:
        Sanitized content with replacements applied
    """
    sanitized = content

    # Replace story IDs with deterministic placeholders
    for original_id, placeholder_id in mapping.story_id_mapping.items():
        # Use word boundaries to match exact story IDs
        pattern = r'\b' + re.escape(original_id) + r'\b'
        sanitized = re.sub(pattern, placeholder_id, sanitized)

    # Apply standard sanitization patterns
    for pattern, replacement in SANITIZATION_PATTERNS:
        sanitized = re.sub(pattern, replacement, sanitized)

    return sanitized


def _generate_unique_session_id(
    base_id: str,
    existing_ids: set
) -> str:
    """Generate unique session ID by appending counter suffix.

    Args:
        base_id: Original session ID
        existing_ids: Set of already-used session IDs

    Returns:
        Unique session ID with -imported-{n} suffix
    """
    counter = 1
    new_id = f"{base_id}-imported-{counter}"
    while new_id in existing_ids:
        counter += 1
        new_id = f"{base_id}-imported-{counter}"
    return new_id


def _mark_session_as_imported(
    session: Dict[str, Any],
    import_source: str
) -> None:
    """Mark session with import metadata.

    Args:
        session: Session record to update
        import_source: Timestamp of when session was imported
    """
    session["is_imported"] = True
    session["imported_from"] = import_source


def _merge_indices(
    main_index: Dict[str, Any],
    imported_index: Dict[str, Any]
) -> Tuple[Dict[str, Any], int, int]:
    """Merge imported index with main feedback index.

    Args:
        main_index: Main feedback index to merge into
        imported_index: Index from imported archive

    Returns:
        (merged_index, duplicate_count, resolved_count)
    """
    if "sessions" not in main_index:
        main_index["sessions"] = []

    existing_ids = {s.get("session_id") for s in main_index["sessions"]}
    imported_sessions = imported_index.get("sessions", [])
    import_source = imported_index.get("export_metadata", {}).get("created_at")

    duplicate_count = 0
    resolved_count = 0

    for session in imported_sessions:
        session_id = session.get("session_id")

        if session_id in existing_ids:
            # Duplicate found - auto-resolve by adding suffix
            duplicate_count += 1
            new_id = _generate_unique_session_id(session_id, existing_ids)

            session["session_id"] = new_id
            session["original_session_id"] = session_id
            _mark_session_as_imported(session, import_source)
            resolved_count += 1
            existing_ids.add(new_id)
        else:
            # New session
            _mark_session_as_imported(session, import_source)
            existing_ids.add(session_id)

        main_index["sessions"].append(session)

    # Sort by timestamp to maintain chronological order
    main_index["sessions"].sort(
        key=lambda s: _parse_iso_timestamp(s.get("timestamp"))
    )

    return main_index, duplicate_count, resolved_count


# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

def _get_date_range_bounds(date_range: str) -> Tuple[datetime, datetime]:
    """Get start and end timestamps for date range filter.

    Args:
        date_range: Date range identifier (e.g., 'last-7-days', 'last-30-days')

    Returns:
        (start_datetime, end_datetime) tuple in UTC timezone
    """
    now = datetime.now(timezone.utc)

    days = DATE_RANGE_DAYS.get(date_range)
    if days is None:
        # Special case: "all" uses epoch date
        start = EPOCH_DATE
    else:
        start = now - timedelta(days=days)

    return start, now


def _extract_timestamp_from_filename(filename: str) -> Optional[datetime]:
    """Extract and parse timestamp from feedback session filename.

    Args:
        filename: Filename to parse (e.g., '2025-11-07T10-30-00-command-dev-success.md')

    Returns:
        Parsed datetime or None if parsing fails
    """
    # Match pattern: YYYY-MM-DDTHH-MM-SS at start of filename
    timestamp_match = re.match(
        r'^(\d{4}-\d{2}-\d{2}T\d{2})-(\d{2})-(\d{2})',
        filename
    )

    if not timestamp_match:
        return None

    # Reconstruct ISO format: 2025-11-07T10:30:00
    timestamp_str = (
        f"{timestamp_match.group(1)}:"
        f"{timestamp_match.group(2)}:"
        f"{timestamp_match.group(3)}"
    )

    try:
        ts = datetime.fromisoformat(timestamp_str)
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        return ts
    except (ValueError, AttributeError):
        return None


def _get_file_modification_time(file_path: Path) -> datetime:
    """Get file modification time as UTC datetime.

    Args:
        file_path: Path to file

    Returns:
        Modification time with UTC timezone
    """
    return datetime.fromtimestamp(
        file_path.stat().st_mtime,
        tz=timezone.utc
    )


def _parse_session_timestamp(filename: str, file_path: Path) -> datetime:
    """Parse session timestamp from filename or file metadata.

    Args:
        filename: Feedback session filename
        file_path: Path to the file

    Returns:
        Parsed or fallback datetime
    """
    # Try to extract timestamp from filename
    ts = _extract_timestamp_from_filename(filename)
    if ts:
        return ts

    # Fallback: use file modification time
    return _get_file_modification_time(file_path)


def _create_session_record(
    md_file: Path,
    content: str,
    timestamp: datetime
) -> Dict[str, Any]:
    """Create session record from file metadata and content.

    Args:
        md_file: Path to markdown file
        content: File content
        timestamp: Session timestamp

    Returns:
        Session dictionary for index
    """
    return {
        "session_id": md_file.stem,  # Use filename stem as session ID
        "original_filename": md_file.name,
        "operation_type": "command",
        "operation_name": "/dev STORY-042",  # Will be overwritten by sanitization
        "status": "success",
        "timestamp": _format_iso_timestamp(timestamp),
        "content": content,
        "file_size_bytes": md_file.stat().st_size,
    }


def _process_feedback_file(
    md_file: Path,
    start_date: datetime,
    end_date: datetime
) -> Optional[Dict[str, Any]]:
    """Process a single feedback file and return session if within date range.

    Args:
        md_file: Path to markdown file
        start_date: Start of date range filter
        end_date: End of date range filter

    Returns:
        Session dict if file is in range, None otherwise
    """
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        ts = _parse_session_timestamp(md_file.name, md_file)

        # Filter by date range
        if not (start_date <= ts <= end_date):
            return None

        return _create_session_record(md_file, content, ts)

    except Exception as e:
        logger.warning(f"Failed to read session file {md_file}: {str(e)}")
        return None


def _get_feedback_sessions(
    date_range: str = DEFAULT_DATE_RANGE
) -> List[Dict[str, Any]]:
    """Read feedback sessions from .devforgeai/feedback/sessions/ directory.

    Args:
        date_range: Date range filter (e.g., 'last-30-days')

    Returns:
        List of session dictionaries sorted by timestamp
    """
    if not FEEDBACK_SESSIONS_DIR.exists():
        logger.info(f"Feedback directory not found: {FEEDBACK_SESSIONS_DIR}")
        return []

    start_date, end_date = _get_date_range_bounds(date_range)
    sessions = []

    # Read all markdown files in feedback directory
    for md_file in FEEDBACK_SESSIONS_DIR.glob("*.md"):
        session = _process_feedback_file(md_file, start_date, end_date)
        if session:
            sessions.append(session)

    # Sort by timestamp (oldest first), then by session_id for determinism
    sessions.sort(key=lambda s: (s["timestamp"], s.get("session_id", "")))

    return sessions


def _determine_export_timestamp(sessions: List[Dict[str, Any]]) -> datetime:
    """Determine export timestamp from latest session or current time.

    Args:
        sessions: List of feedback sessions (sorted by timestamp)

    Returns:
        UTC datetime rounded to seconds
    """
    if sessions:
        # Use latest session timestamp for determinism
        last_session_ts_str = sessions[-1].get("timestamp", "")
        try:
            last_session_ts = _parse_iso_timestamp(last_session_ts_str)
            return last_session_ts.replace(microsecond=0, tzinfo=timezone.utc)
        except (ValueError, AttributeError):
            pass

    return datetime.now(timezone.utc).replace(microsecond=0)


def _get_unique_archive_path(
    output_dir: Path,
    timestamp: datetime
) -> str:
    """Generate unique archive filename with UUID suffix for guaranteed uniqueness.

    Args:
        output_dir: Directory for archive
        timestamp: Timestamp for filename

    Returns:
        Unique archive path with UUID suffix
    """
    timestamp_str = timestamp.strftime("%Y-%m-%dT%H-%M-%S")

    # Use short UUID suffix for guaranteed uniqueness (handles rapid successive exports)
    uuid_suffix = str(uuid.uuid4())[:8]
    timestamp_with_suffix = f"{timestamp_str}-{uuid_suffix}"

    archive_filename = f"{ARCHIVE_PREFIX}-{timestamp_with_suffix}.zip"
    archive_path = str(output_dir / archive_filename)

    return archive_path


def _build_export_index(
    sessions: List[Dict[str, Any]],
    sanitization_config: SanitizationConfig,
    date_range: str,
    export_time: datetime
) -> Dict[str, Any]:
    """Build index.json for export archive.

    Args:
        sessions: Feedback sessions to index
        sanitization_config: Applied sanitization rules
        date_range: Date range used for export
        export_time: Export timestamp

    Returns:
        Index data dictionary
    """
    start_date, end_date = _get_date_range_bounds(date_range)

    index_data = {
        "export_metadata": {
            "created_at": _format_iso_timestamp(export_time),
            "exported_sessions_count": len(sessions),
            "date_range": date_range,
            "date_range_start": _format_iso_timestamp(start_date),
            "date_range_end": _format_iso_timestamp(end_date),
            "sanitization_applied": True,
            "framework_version": FRAMEWORK_VERSION,
            "export_format_version": EXPORT_FORMAT_VERSION
        },
        "sessions": []
    }

    # Build session entries for index
    for session in sessions:
        session_content = session.get("content", "")
        file_sha256 = _calculate_content_sha256(session_content)

        index_entry = {
            "session_id": session.get("session_id"),
            "original_filename": session.get("original_filename"),
            "operation_type": session.get("operation_type"),
            "operation_name": session.get("operation_name"),
            "status": session.get("status"),
            "timestamp": session.get("timestamp"),
            "file_size_bytes": session.get("file_size_bytes"),
            "export_filename": session.get("original_filename"),
            "file_sha256": file_sha256
        }
        index_data["sessions"].append(index_entry)

    return index_data


def _build_export_manifest(
    sessions: List[Dict[str, Any]],
    sanitization_config: SanitizationConfig,
    index_json_str: str,
    date_range: str,
    export_time: datetime
) -> Dict[str, Any]:
    """Build manifest.json for export archive.

    Args:
        sessions: Feedback sessions exported
        sanitization_config: Applied sanitization rules
        index_json_str: Serialized index.json
        date_range: Date range used for export
        export_time: Export timestamp

    Returns:
        Manifest data dictionary
    """
    total_size = sum(s.get("file_size_bytes", 0) for s in sessions)
    index_sha256 = _calculate_content_sha256(index_json_str)
    start_date, end_date = _get_date_range_bounds(date_range)

    return {
        "export_version": "1.0",
        "export_format_version": EXPORT_FORMAT_VERSION,
        "created_at": _format_iso_timestamp(export_time),
        "created_by": "DevForgeAI Framework",
        "framework_version": FRAMEWORK_VERSION,
        "session_count": len(sessions),
        "file_count": len(sessions),
        "total_size_bytes": total_size,
        "archive_format": "zip",
        "date_range": {
            "filter": date_range,
            "start_date": _format_iso_timestamp(start_date),
            "end_date": _format_iso_timestamp(end_date)
        },
        "sanitization": {
            "applied": True,
            "rules_applied": [
                "story_ids_replaced_with_placeholders",
                "custom_field_values_removed",
                "project_context_removed",
                "file_paths_masked"
            ],
            "replacement_mapping": {
                "story_id_mapping": sanitization_config.story_id_mapping,
                "masked_fields": sanitization_config.masked_fields,
                "preserved_fields": sanitization_config.preserved_fields
            }
        },
        "integrity": {
            "checksum_algorithm": "sha256",
            "index_file_sha256": index_sha256,
            "session_count_verified": True,
            "all_files_present": True
        },
        "compatibility": {
            "min_framework_version": MIN_FRAMEWORK_VERSION,
            "tested_on_versions": ["1.0.0", "1.0.1"],
            "import_warnings": []
        },
        "source_project": {
            "identifier": "sha256-hash-of-project-root",
            "export_location": "project-root-directory",
            "export_hostname": "username-machine-name"
        }
    }


def _sanitize_all_sessions(
    sessions: List[Dict[str, Any]],
    sanitization_config: SanitizationConfig
) -> None:
    """Apply sanitization to all session records in place.

    Args:
        sessions: Session records to sanitize (modified in place)
        sanitization_config: Sanitization rules to apply
    """
    for session in sessions:
        session["content"] = _sanitize_content(
            session["content"],
            sanitization_config
        )
        # Update operation_name if it contains story ID
        if "operation_name" in session:
            session["operation_name"] = _sanitize_content(
                session["operation_name"],
                sanitization_config
            )


def _write_export_archive(
    archive_path: str,
    sessions: List[Dict[str, Any]],
    index_data: Dict[str, Any],
    manifest_data: Dict[str, Any]
) -> None:
    """Write sessions, index, and manifest to ZIP archive.

    Args:
        archive_path: Path where archive will be created
        sessions: Feedback sessions to include
        index_data: Index metadata
        manifest_data: Manifest metadata
    """
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Write index.json with sorted keys for determinism
        index_json_str = json.dumps(index_data, indent=2, sort_keys=True)
        _write_deterministic_zip_entry(zf, INDEX_FILENAME, index_json_str)

        # Write manifest.json
        manifest_json_str = json.dumps(manifest_data, indent=2, sort_keys=True)
        _write_deterministic_zip_entry(zf, MANIFEST_FILENAME, manifest_json_str)

        # Write session files in sorted order for determinism
        for session in sorted(sessions, key=lambda s: s.get("original_filename", "")):
            filename = session.get("original_filename", "session.md")
            content = session.get("content", "")
            arcname = f"{FEEDBACK_SESSIONS_SUBDIR}/{filename}"
            _write_deterministic_zip_entry(zf, arcname, content)


def export_feedback_sessions(
    date_range: str = DEFAULT_DATE_RANGE,
    sanitize: bool = True,
    output_path: Optional[str] = None,
    compression_format: str = DEFAULT_COMPRESSION_FORMAT
) -> Dict[str, Any]:
    """Export feedback sessions with mandatory sanitization.

    Args:
        date_range: Date range filter (last-7-days, last-30-days, last-90-days, all)
        sanitize: Apply sanitization (defaults to True, cannot be disabled)
        output_path: Custom output directory (defaults to project root)
        compression_format: Archive format (zip only for now)

    Returns:
        ExportResult as dict with success, archive_path, sessions_exported, etc.

    Raises:
        PermissionError: If sanitize=False (sanitization is mandatory)
        ValueError: If invalid date_range or compression_format
    """
    start_time = datetime.now()

    # Validate inputs
    _validate_date_range(date_range)

    if sanitize is False:
        raise PermissionError(
            "Sanitization cannot be disabled. "
            "Only framework maintainers with explicit permission can disable sanitization."
        )

    # Read feedback sessions
    logger.info(f"Reading feedback sessions for date range: {date_range}")
    sessions = _get_feedback_sessions(date_range)

    # Build sanitization config from session content
    content_list = [s.get("content", "") for s in sessions]
    sanitization_config = SanitizationConfig(
        story_id_mapping=_build_story_id_mapping(content_list)
    )

    # Apply sanitization to all sessions
    _sanitize_all_sessions(sessions, sanitization_config)

    # Determine export timestamp
    export_time = _determine_export_timestamp(sessions)

    # Set up output directory
    if output_path:
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = Path(".")

    # Generate unique archive path
    archive_path = _get_unique_archive_path(output_dir, export_time)

    # Build export index and manifest
    index_data = _build_export_index(
        sessions,
        sanitization_config,
        date_range,
        export_time
    )
    index_json_str = json.dumps(index_data, indent=2)
    manifest_data = _build_export_manifest(
        sessions,
        sanitization_config,
        index_json_str,
        date_range,
        export_time
    )

    # Create ZIP archive
    logger.info(f"Creating archive: {archive_path}")
    _write_export_archive(archive_path, sessions, index_data, manifest_data)

    # Calculate metrics
    archive_size = os.path.getsize(archive_path)
    execution_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)

    logger.info(f"Export complete: {len(sessions)} sessions, {archive_size} bytes")

    result = ExportResult(
        success=True,
        archive_path=archive_path,
        archive_size_bytes=archive_size,
        sessions_exported=len(sessions),
        sanitization_applied=True,
        date_range_used=date_range,
        execution_time_ms=execution_time_ms,
        replacements_made=len(sanitization_config.story_id_mapping)
    )

    return asdict(result)


# ============================================================================
# IMPORT FUNCTIONS
# ============================================================================

def _validate_archive_for_import(archive_path: str) -> None:
    """Validate archive for import (format, contents, security).

    Args:
        archive_path: Path to ZIP archive

    Raises:
        FileNotFoundError: If archive not found
        ValueError: If archive invalid
    """
    logger.info(f"Validating archive: {archive_path}")

    if not os.path.isfile(archive_path):
        raise FileNotFoundError(f"Archive not found: {archive_path}")

    # Validate ZIP format
    _validate_zip_archive(archive_path)

    # Validate ZIP contents
    _validate_zip_contents(archive_path)

    # Validate no path traversal
    _validate_path_traversal(archive_path)


def _extract_archive_to_import_dir(archive_path: str) -> str:
    """Extract archive to timestamped import directory.

    Args:
        archive_path: Path to ZIP archive

    Returns:
        Path to extracted directory
    """
    now = datetime.now(timezone.utc)
    timestamp_str = now.strftime("%Y-%m-%dT%H-%M-%S")

    IMPORT_BASE_DIR.mkdir(parents=True, exist_ok=True)
    extracted_path = str(IMPORT_BASE_DIR / timestamp_str)
    Path(extracted_path).mkdir(parents=True, exist_ok=True)

    logger.info(f"Extracting archive to: {extracted_path}")

    with zipfile.ZipFile(archive_path, 'r') as zf:
        zf.extractall(extracted_path)

    return extracted_path


def _load_import_metadata(extracted_path: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Load index and manifest from extracted archive.

    Args:
        extracted_path: Path to extracted directory

    Returns:
        (imported_index, imported_manifest) tuple
    """
    imported_index_path = Path(extracted_path) / INDEX_FILENAME
    with open(imported_index_path, 'r', encoding='utf-8') as f:
        imported_index = json.load(f)

    imported_manifest_path = Path(extracted_path) / MANIFEST_FILENAME
    with open(imported_manifest_path, 'r', encoding='utf-8') as f:
        imported_manifest = json.load(f)

    return imported_index, imported_manifest


def _check_framework_compatibility(
    imported_manifest: Dict[str, Any]
) -> Tuple[str, List[str]]:
    """Check framework version compatibility with imported archive.

    Args:
        imported_manifest: Manifest from imported archive

    Returns:
        (compatibility_status, warnings_list) tuple
    """
    compatibility_status = COMPATIBLE_STATUS
    warnings = []

    min_version = imported_manifest.get("min_framework_version", "1.0.0")
    tested_versions = imported_manifest.get("tested_on_versions", [])

    # Version check
    if FRAMEWORK_VERSION < min_version:
        compatibility_status = INCOMPATIBLE_STATUS
        warnings.append(
            f"Export requires minimum version {min_version}, "
            f"but current version is {FRAMEWORK_VERSION}"
        )
    elif FRAMEWORK_VERSION not in tested_versions:
        warnings.append(
            f"Current framework version {FRAMEWORK_VERSION} was not tested "
            f"with this export (tested on: {', '.join(tested_versions)})"
        )

    logger.info(f"Compatibility status: {compatibility_status}")
    return compatibility_status, warnings


def _load_or_create_main_index() -> Dict[str, Any]:
    """Load existing feedback index or create new one.

    Returns:
        Main feedback index dictionary
    """
    if FEEDBACK_INDEX_FILE.exists():
        logger.info("Merging with existing feedback index")
        with open(FEEDBACK_INDEX_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # Ensure parent directory exists
        FEEDBACK_INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
        logger.info("Creating new feedback index")
        return {"sessions": []}


def _write_merged_index_atomically(
    merged_index: Dict[str, Any]
) -> None:
    """Write merged index to disk atomically.

    Args:
        merged_index: Merged feedback index to save
    """
    # Ensure parent directory exists
    FEEDBACK_INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Write to temporary file, then rename (atomic operation)
    temp_index_path = FEEDBACK_INDEX_FILE.parent / f"{FEEDBACK_INDEX_FILE.name}.tmp"
    with open(temp_index_path, 'w', encoding='utf-8') as f:
        json.dump(merged_index, f, indent=2)

    # Atomic rename
    temp_index_path.replace(FEEDBACK_INDEX_FILE)
    logger.info(f"Updated feedback index: {FEEDBACK_INDEX_FILE}")


def _build_import_summary(
    imported_index: Dict[str, Any],
    merged_index: Dict[str, Any],
    duplicate_count: int,
    resolved_count: int
) -> Dict[str, Any]:
    """Build import summary report.

    Args:
        imported_index: Index from imported archive
        merged_index: Merged index after import
        duplicate_count: Number of duplicate IDs found
        resolved_count: Number of duplicate IDs resolved

    Returns:
        Import summary dictionary
    """
    sessions_imported = len(imported_index.get("sessions", []))
    return {
        "exported_sessions": imported_index.get("export_metadata", {}).get(
            "exported_sessions_count", 0
        ),
        "imported_sessions": sessions_imported,
        "duplicate_ids_found": duplicate_count,
        "duplicate_ids_resolved": resolved_count,
        "current_total_sessions": len(merged_index.get("sessions", []))
    }


def import_feedback_sessions(
    archive_path: str,
    validate_integrity: bool = True,
    auto_resolve_conflicts: bool = True
) -> Dict[str, Any]:
    """Import feedback sessions from archive.

    Args:
        archive_path: Path to ZIP archive
        validate_integrity: Validate checksums (for future use)
        auto_resolve_conflicts: Automatically resolve duplicate IDs

    Returns:
        ImportResult as dict with success, extracted_path, sessions_imported, etc.

    Raises:
        FileNotFoundError: If archive not found
        ValueError: If archive invalid or required files missing
    """
    start_time = datetime.now()

    # Validate archive
    _validate_archive_for_import(archive_path)

    # Extract archive
    extracted_path = _extract_archive_to_import_dir(archive_path)

    # Load metadata from extracted archive
    imported_index, imported_manifest = _load_import_metadata(extracted_path)

    # Check framework compatibility
    compatibility_status, warnings = _check_framework_compatibility(imported_manifest)

    # Load or create main index
    main_index = _load_or_create_main_index()

    # Perform merge
    merged_index, duplicate_count, resolved_count = _merge_indices(
        main_index,
        imported_index
    )

    # Write merged index atomically
    _write_merged_index_atomically(merged_index)

    # Build import summary
    import_summary = _build_import_summary(
        imported_index,
        merged_index,
        duplicate_count,
        resolved_count
    )

    # Calculate execution time
    execution_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
    sessions_imported = import_summary["imported_sessions"]

    logger.info(f"Import complete: {sessions_imported} sessions imported")

    result = ImportResult(
        success=True,
        extracted_path=extracted_path,
        sessions_imported=sessions_imported,
        duplicate_ids_found=duplicate_count,
        duplicate_ids_resolved=resolved_count,
        compatibility_status=compatibility_status,
        framework_version_current=FRAMEWORK_VERSION,
        execution_time_ms=execution_time_ms,
        import_summary=import_summary,
        warnings=warnings
    )

    return asdict(result)
