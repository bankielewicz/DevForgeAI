"""
Shared test fixtures for STORY-402: Orphaned Import Detection.

Provides common scanner content fixture and helper functions
used across all 8 AC test files.
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SCANNER_PATH = 'src/claude/agents/anti-pattern-scanner.md'


def read_file(relative_path):
    """Read a file relative to the project root."""
    full_path = os.path.join(PROJECT_ROOT, relative_path)
    with open(full_path, 'r') as f:
        return f.read()


def extract_orphaned_import_section(content):
    """Extract the orphaned import section from the scanner content.

    Returns the text from the first mention of 'orphaned import' (case-insensitive)
    to the next major section heading (## or end of file).
    Returns empty string if no orphaned import section found.
    """
    match = re.search(
        r'(?i)(orphaned.?import.*?)(?=\n## |\Z)',
        content,
        re.DOTALL
    )
    return match.group(1) if match else ''


@pytest.fixture
def scanner_content():
    """Load anti-pattern-scanner.md content for all STORY-402 tests."""
    return read_file(SCANNER_PATH)


@pytest.fixture
def orphaned_section(scanner_content):
    """Extract just the orphaned import section from scanner content."""
    return extract_orphaned_import_section(scanner_content)
