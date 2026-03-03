"""
Shared utility functions for user-input-guidance tests

This module consolidates common test helper functions to reduce code duplication:
- JSON validation (loading, schema checking)
- Markdown parsing (section extraction, counting)
- File operations (existence checking)
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional


# JSON Validation Functions

def load_results_json(json_file: Path) -> Optional[List[Dict[str, Any]]]:
    """
    Load results from JSON file safely.

    Args:
        json_file: Path to JSON file

    Returns:
        List of result dictionaries, or None if file doesn't exist/invalid

    Raises:
        json.JSONDecodeError: If JSON is malformed
    """
    if not json_file.exists():
        return None

    with open(json_file, 'r') as f:
        data = json.load(f)

    return data.get('results', [])


def validate_json_schema(results: List[Dict[str, Any]],
                        required_fields: List[str]) -> List[str]:
    """
    Validate JSON schema against required fields.

    Args:
        results: List of result entries to validate
        required_fields: List of field names that must be present

    Returns:
        List of missing fields (empty if all present)
    """
    missing_fields = []

    if not results:
        return required_fields

    first_entry = results[0]
    for field in required_fields:
        if field not in first_entry:
            missing_fields.append(field)

    return missing_fields


def is_valid_json_file(file_path: Path) -> bool:
    """
    Check if file is valid JSON.

    Args:
        file_path: Path to file to validate

    Returns:
        True if file exists and contains valid JSON
    """
    if not file_path.exists():
        return False

    try:
        json.loads(file_path.read_text())
        return True
    except json.JSONDecodeError:
        return False


# Markdown Parsing Functions

def extract_markdown_section(content: str, section_marker: str,
                           end_marker: str = '\n# ') -> str:
    """
    Extract markdown section between markers.

    Args:
        content: Full markdown content
        section_marker: Text to find section start (case-insensitive)
        end_marker: Text that marks section end (default: next # heading)

    Returns:
        Extracted section text, or empty string if not found
    """
    idx = content.lower().find(section_marker.lower())
    if idx < 0:
        return ''

    section = content[idx:]
    end_idx = section.find(end_marker)
    if end_idx > 0:
        section = section[:end_idx]

    return section


def count_numbered_items(text: str, max_num: int = 10) -> int:
    """
    Count numbered list items in text (1. 2. 3. etc).

    Args:
        text: Text to search
        max_num: Maximum number to check for

    Returns:
        Count of consecutive numbered items found
    """
    count = 0
    for i in range(1, max_num + 1):
        if f'\n{i}. ' in text or f'\n{i}) ' in text:
            count += 1
        else:
            break  # Stop at first gap

    return count


def count_bullet_items(text: str) -> int:
    """
    Count bullet list items in text (- ).

    Args:
        text: Text to search

    Returns:
        Count of bullet items
    """
    return text.count('- ')


def extract_fixture_references(content: str) -> List[str]:
    """
    Extract fixture references from markdown (baseline-NN, enhanced-NN, etc).

    Args:
        content: Markdown content

    Returns:
        List of fixture identifiers found
    """
    fixtures = set()

    # Look for patterns: baseline-01, enhanced-02, fixture-03, Fixture 4, etc.
    for i in range(1, 11):
        patterns = [
            f'baseline-{i:02d}',
            f'enhanced-{i:02d}',
            f'fixture-{i:02d}',
            f'Fixture {i}'
        ]

        for pattern in patterns:
            if pattern in content:
                fixtures.add(f'{i:02d}')
                break

    return sorted(list(fixtures))


# File Operation Helpers

def file_contains_text(file_path: Path, text: str, case_sensitive: bool = False) -> bool:
    """
    Check if file contains specific text.

    Args:
        file_path: Path to file
        text: Text to search for
        case_sensitive: If False, does case-insensitive search

    Returns:
        True if text found in file
    """
    if not file_path.exists():
        return False

    content = file_path.read_text()
    if case_sensitive:
        return text in content
    else:
        return text.lower() in content.lower()


def file_matches_pattern(file_path: Path, pattern: str) -> bool:
    """
    Check if file content matches pattern (substring search).

    Args:
        file_path: Path to file
        pattern: Pattern to search for (substring)

    Returns:
        True if pattern found in file
    """
    return file_contains_text(file_path, pattern, case_sensitive=True)
