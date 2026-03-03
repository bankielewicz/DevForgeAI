"""
Feedback indexer module for DevForgeAI.

Scans all feedback data sources in devforgeai/feedback/ and builds
a unified index at devforgeai/feedback/index.json.

Uses Python stdlib only: json, pathlib, os, re, datetime.
"""

import datetime
import json
import os
import re
from pathlib import Path


# Files at the root of devforgeai/feedback/ that are NOT feedback data
_EXCLUDED_ROOT_FILES = {
    "USER-GUIDE.md",
    "MAINTAINER-GUIDE.md",
    "GRACEFUL-DEGRADATION.md",
    "RETENTION-POLICY.md",
    "IMPLEMENTATION-COMPLETE.md",
    "QUESTION-BANK-COMPLETION-SUMMARY.md",
    "questions.md",
    "config.yaml",
    "schema.json",
    "questions.yaml",
    "question-defaults.yaml",
    "index.json",
    "feedback-index.json",
    "feedback-register.md",
}

# Directories under devforgeai/feedback/ that are NOT feedback data
_EXCLUDED_DIRS = {"question-bank", "logs", "imported"}

# Subdirectories under ai-analysis/ to exclude
_EXCLUDED_AI_ANALYSIS_SUBDIRS = {"aggregated", "imports"}

# Regex pattern to identify artifact folder names (STORY-NNN, EPIC-NNN, RCA-NNN)
_ARTIFACT_PATTERN = re.compile(r"^(STORY|EPIC|RCA)-\d+$")

# Regex patterns for root-level report filenames
_REPORT_PATTERNS = [
    re.compile(r"^code-review-.*\.md$"),
    re.compile(r"^integration-test-report-.*\.md$"),
    re.compile(r".*-coverage-analysis\.md$"),
    re.compile(r".*-dev-complete-summary\.md$"),
]

# Regex to extract story ID from filenames
_STORY_ID_PATTERN = re.compile(r"(STORY-\d+)")


def _file_mtime_iso(filepath: Path) -> str:
    """Get file modification time as ISO 8601 string in UTC."""
    mtime = os.path.getmtime(str(filepath))
    dt = datetime.datetime.fromtimestamp(mtime, tz=datetime.timezone.utc)
    return dt.isoformat()


def _extract_timestamp_from_json(data: dict) -> str:
    """Extract timestamp from JSON data, checking multiple field locations."""
    # Direct timestamp field
    if "timestamp" in data and isinstance(data["timestamp"], str):
        return data["timestamp"]
    # analysis_date field
    if "analysis_date" in data and isinstance(data["analysis_date"], str):
        return data["analysis_date"]
    # Nested ai_analysis.timestamp
    if "ai_analysis" in data and isinstance(data["ai_analysis"], dict):
        nested = data["ai_analysis"]
        if "timestamp" in nested and isinstance(nested["timestamp"], str):
            return nested["timestamp"]
    return ""


def _is_report_filename(filename: str) -> bool:
    """Check if a filename matches root-level report patterns."""
    for pattern in _REPORT_PATTERNS:
        if pattern.match(filename):
            return True
    return False


def _scan_ai_analysis(feedback_dir: Path, entries: list, errors: list) -> int:
    """
    Scan ai-analysis directory for JSON and MD files in artifact folders.

    Returns count of files processed (including errors).
    """
    ai_dir = feedback_dir / "ai-analysis"
    if not ai_dir.is_dir():
        return 0

    count = 0
    for artifact_dir in sorted(ai_dir.iterdir()):
        if not artifact_dir.is_dir():
            continue
        # Skip excluded subdirectories
        if artifact_dir.name in _EXCLUDED_AI_ANALYSIS_SUBDIRS:
            continue
        # Only process artifact folders matching STORY-NNN, EPIC-NNN, RCA-NNN
        if not _ARTIFACT_PATTERN.match(artifact_dir.name):
            continue

        artifact_id = artifact_dir.name

        # Walk all files recursively in this artifact folder
        for root, _dirs, files in os.walk(str(artifact_dir)):
            root_path = Path(root)
            for filename in sorted(files):
                filepath = root_path / filename

                # Skip index.json at any level within ai-analysis
                if filename == "index.json":
                    continue

                if filename.endswith(".json"):
                    count += 1
                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            data = json.load(f)
                    except (json.JSONDecodeError, OSError) as exc:
                        rel_path = filepath.relative_to(feedback_dir)
                        errors.append(
                            f"Failed to parse: {rel_path}: {type(exc).__name__}"
                        )
                        continue

                    timestamp = _extract_timestamp_from_json(data)
                    if not timestamp:
                        timestamp = _file_mtime_iso(filepath)

                    rel_path = filepath.relative_to(feedback_dir)
                    stem = filepath.stem
                    entry_id = f"{artifact_id}-{stem}"

                    entries.append({
                        "id": entry_id,
                        "timestamp": timestamp,
                        "source_type": "ai-analysis",
                        "story-id": artifact_id,
                        "file-path": str(rel_path).replace("\\", "/"),
                        "tags": ["ai-analysis"],
                    })

                elif filename.endswith(".md"):
                    count += 1
                    timestamp = _file_mtime_iso(filepath)
                    rel_path = filepath.relative_to(feedback_dir)
                    stem = filepath.stem
                    entry_id = f"{artifact_id}-{stem}"

                    entries.append({
                        "id": entry_id,
                        "timestamp": timestamp,
                        "source_type": "ai-analysis",
                        "story-id": artifact_id,
                        "file-path": str(rel_path).replace("\\", "/"),
                        "tags": ["ai-analysis"],
                    })

    return count


def _scan_code_reviews(feedback_dir: Path, entries: list, errors: list) -> int:
    """
    Scan code-review/ and code-reviews/ directories for markdown files.

    Returns count of files processed.
    """
    count = 0
    for dir_name in ("code-review", "code-reviews"):
        cr_dir = feedback_dir / dir_name
        if not cr_dir.is_dir():
            continue

        for filepath in sorted(cr_dir.iterdir()):
            if not filepath.is_file():
                continue
            if not filepath.name.endswith(".md"):
                continue

            count += 1
            timestamp = _file_mtime_iso(filepath)
            rel_path = filepath.relative_to(feedback_dir)
            stem = filepath.stem
            entry_id = f"code-review-{stem}"

            # Extract story ID from filename
            story_match = _STORY_ID_PATTERN.search(filepath.name)
            story_id = story_match.group(1) if story_match else ""

            entry = {
                "id": entry_id,
                "timestamp": timestamp,
                "source_type": "code-review",
                "file-path": str(rel_path).replace("\\", "/"),
                "tags": ["code-review"],
            }
            if story_id:
                entry["story-id"] = story_id

            entries.append(entry)

    return count


def _scan_root_reports(feedback_dir: Path, entries: list, errors: list) -> int:
    """
    Scan root-level feedback directory for report files.

    Returns count of files processed.
    """
    count = 0
    if not feedback_dir.is_dir():
        return 0

    for filepath in sorted(feedback_dir.iterdir()):
        if not filepath.is_file():
            continue
        if filepath.name in _EXCLUDED_ROOT_FILES:
            continue
        if not filepath.name.endswith(".md"):
            continue
        if not _is_report_filename(filepath.name):
            continue

        count += 1
        timestamp = _file_mtime_iso(filepath)
        rel_path = filepath.relative_to(feedback_dir)
        stem = filepath.stem
        entry_id = f"report-{stem}"

        # Extract story ID from filename
        story_match = _STORY_ID_PATTERN.search(filepath.name)
        story_id = story_match.group(1) if story_match else ""

        entry = {
            "id": entry_id,
            "timestamp": timestamp,
            "source_type": "report",
            "file-path": str(rel_path).replace("\\", "/"),
            "tags": ["report"],
        }
        if story_id:
            entry["story-id"] = story_id

        entries.append(entry)

    return count


def _scan_sessions(feedback_dir: Path, entries: list, errors: list) -> int:
    """
    Scan sessions/ directory for markdown files (backward compatibility).

    Returns count of files processed. Silently skips if directory doesn't exist.
    """
    sessions_dir = feedback_dir / "sessions"
    if not sessions_dir.is_dir():
        return 0

    count = 0
    for filepath in sorted(sessions_dir.iterdir()):
        if not filepath.is_file():
            continue
        if not filepath.name.endswith(".md"):
            continue

        count += 1
        timestamp = _file_mtime_iso(filepath)
        rel_path = filepath.relative_to(feedback_dir)
        stem = filepath.stem
        entry_id = f"session-{stem}"

        entries.append({
            "id": entry_id,
            "timestamp": timestamp,
            "source_type": "session",
            "file-path": str(rel_path).replace("\\", "/"),
            "tags": ["session"],
        })

    return count


def reindex_all_feedback(project_root: str, output_format: str = "text") -> int:
    """
    Scan all feedback sources and build unified index.

    Args:
        project_root: Path to project root directory.
        output_format: 'text' or 'json'.

    Returns:
        Exit code: 0 for success, 1 for error.

    Side effects:
        - Writes devforgeai/feedback/index.json
        - Prints results to stdout
    """
    root = Path(project_root)
    feedback_dir = root / "devforgeai" / "feedback"

    if not feedback_dir.is_dir():
        if output_format == "json":
            print(json.dumps({
                "status": "error",
                "message": f"Feedback directory not found: {feedback_dir}",
            }))
        else:
            print(f"Error: Feedback directory not found: {feedback_dir}")
        return 1

    entries: list = []
    errors: list = []

    # Scan all sources
    ai_count = _scan_ai_analysis(feedback_dir, entries, errors)
    cr_count = _scan_code_reviews(feedback_dir, entries, errors)
    report_count = _scan_root_reports(feedback_dir, entries, errors)
    session_count = _scan_sessions(feedback_dir, entries, errors)

    # Sort entries by timestamp (newest first)
    entries.sort(key=lambda e: e.get("timestamp", ""), reverse=True)

    # Build source summary
    source_summary = {
        "ai-analysis": sum(1 for e in entries if e["source_type"] == "ai-analysis"),
        "session": sum(1 for e in entries if e["source_type"] == "session"),
        "code-review": sum(1 for e in entries if e["source_type"] == "code-review"),
        "report": sum(1 for e in entries if e["source_type"] == "report"),
    }

    total_files = ai_count + cr_count + report_count + session_count
    indexed_count = len(entries)
    error_count = len(errors)

    # Build index
    now_utc = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    index = {
        "version": "2.0",
        "last-updated": now_utc,
        "feedback-sessions": entries,
        "source_summary": source_summary,
    }

    # Write index file
    index_path = feedback_dir / "index.json"
    try:
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2)
    except OSError as exc:
        if output_format == "json":
            print(json.dumps({
                "status": "error",
                "message": f"Failed to write index: {exc}",
            }))
        else:
            print(f"Error: Failed to write index: {exc}")
        return 1

    # Print results
    if output_format == "json":
        result = {
            "status": "success",
            "total_files": total_files,
            "indexed_count": indexed_count,
            "error_count": error_count,
            "sources_scanned": source_summary,
            "errors": errors,
            "version": "2.0",
        }
        print(json.dumps(result))
    else:
        print("\u2705 Reindex completed successfully")
        print()
        print(f"Total files processed: {total_files}")
        print(f"Successfully indexed: {indexed_count}")
        print(f"Errors encountered: {error_count}")
        print()
        print("Sources scanned:")
        print(f"  AI analysis files: {source_summary['ai-analysis']}")
        print(f"  Code review files: {source_summary['code-review']}")
        print(f"  Root report files: {source_summary['report']}")
        print(f"  Session files: {source_summary['session']}")
        print()
        print(f"Index file: devforgeai/feedback/index.json")
        print(f"Index version: 2.0")

    return 0
