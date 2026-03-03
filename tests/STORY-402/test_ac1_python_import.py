"""
Test: AC#1 - Python Import Detection
Story: STORY-402
Generated: 2026-02-14

Validates that anti-pattern-scanner.md Phase 5 section documents Python import
Grep patterns for orphaned import detection, including symbol extraction.

Tests validate STRUCTURE and CONTENT of Markdown files (not executable code).
All tests MUST FAIL initially (TDD Red phase) since content has not been added yet.
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def read_file(relative_path):
    """Read a file relative to the project root."""
    full_path = os.path.join(PROJECT_ROOT, relative_path)
    with open(full_path, 'r') as f:
        return f.read()


class TestAC1PythonImportDetection:
    """AC#1: Python Import Detection in anti-pattern-scanner.md Phase 5."""

    SCANNER_PATH = 'src/claude/agents/anti-pattern-scanner.md'

    # --- Arrange (shared fixture) ---

    @pytest.fixture(autouse=True)
    def setup(self):
        """Arrange: Load the anti-pattern-scanner.md content."""
        self.content = read_file(self.SCANNER_PATH)

    # --- Act & Assert ---

    def test_should_contain_orphaned_import_detection_in_phase5(self):
        """Phase 5 must include orphaned import detection alongside existing smells."""
        assert 'orphaned import' in self.content.lower() or 'orphaned_import' in self.content.lower(), \
            "Phase 5 must reference 'orphaned import' or 'orphaned_import' detection"

    def test_should_contain_python_import_grep_pattern(self):
        """Phase 5 must document the Python import Grep pattern: ^(import |from .+ import )."""
        assert re.search(r'\^\(import \|from \.\+ import \)', self.content) or \
               re.search(r'\^import\b.*\^from\b', self.content), \
            "Phase 5 must contain Python import Grep pattern: ^(import |from .+ import )"

    def test_should_reference_python_import_statement_in_orphaned_context(self):
        """Phase 5 orphaned import section must reference Python import and from...import."""
        # Must mention both import and from...import in the orphaned import context
        orphaned_with_import = re.search(
            r'(?i)orphaned.?import.*?(import\s+\S+|from\s+\S+\s+import)',
            self.content,
            re.DOTALL
        )
        assert orphaned_with_import, \
            "Phase 5 orphaned import section must reference 'import X' and 'from X import Y' patterns"

    def test_should_reference_symbol_extraction_from_imports(self):
        """Phase 5 must document how to extract the imported symbol name."""
        lower = self.content.lower()
        assert 'symbol' in lower and ('extract' in lower or 'parse' in lower), \
            "Phase 5 must document symbol extraction from import statements"

    def test_should_list_orphaned_import_alongside_existing_code_smells(self):
        """Orphaned import must appear alongside existing code smell types in Phase 5."""
        phase5_pattern = re.search(
            r'(?i)(phase\s*5|code\s*smell).*?(orphaned.?import)',
            self.content,
            re.DOTALL
        )
        assert phase5_pattern, \
            "Orphaned import must be listed as a code smell in Phase 5 section"

    def test_should_reference_python_language_for_import_detection(self):
        """Phase 5 orphaned import section must explicitly reference Python language."""
        # Look for Python mentioned in the orphaned import context
        orphaned_section = re.search(
            r'(?i)orphaned.?import.*?python|python.*?orphaned.?import',
            self.content,
            re.DOTALL
        )
        assert orphaned_section, \
            "Orphaned import detection must reference Python as a supported language"
