"""
Test: AC#3 - Symbol Usage Search
Story: STORY-402
Generated: 2026-02-14

Validates that anti-pattern-scanner.md Phase 5 section documents same-file symbol
usage search, excluding the import line itself, and flagging when usage_count = 0.

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


class TestAC3SymbolUsageSearch:
    """AC#3: Symbol Usage Search in anti-pattern-scanner.md Phase 5."""

    SCANNER_PATH = 'src/claude/agents/anti-pattern-scanner.md'

    # --- Arrange (shared fixture) ---

    @pytest.fixture(autouse=True)
    def setup(self):
        """Arrange: Load the anti-pattern-scanner.md content."""
        self.content = read_file(self.SCANNER_PATH)

    # --- Act & Assert ---

    def test_should_document_same_file_symbol_usage_search(self):
        """Phase 5 must document searching the same file for symbol usage."""
        lower = self.content.lower()
        assert ('same file' in lower or 'same-file' in lower) and \
               ('usage' in lower or 'search' in lower), \
            "Phase 5 must document same-file symbol usage search"

    def test_should_specify_excluding_import_line_from_search(self):
        """Phase 5 must specify that the import line itself is excluded from usage search."""
        lower = self.content.lower()
        assert ('exclud' in lower or 'skip' in lower or 'ignor' in lower) and \
               ('import line' in lower or 'import statement' in lower), \
            "Phase 5 must specify excluding the import line from usage search"

    def test_should_specify_usage_count_zero_triggers_flagging(self):
        """Phase 5 must specify that usage_count = 0 triggers flagging as orphaned."""
        assert re.search(r'usage_count\s*[=]=?\s*0', self.content) or \
               re.search(r'usage.count.*0', self.content.lower()), \
            "Phase 5 must specify that usage_count = 0 triggers orphaned import flagging"

    def test_should_document_grep_based_usage_search_in_orphaned_context(self):
        """Phase 5 orphaned import section must document Grep-based symbol usage search."""
        orphaned_grep = re.search(
            r'(?i)orphaned.?import.*?grep.*?(usage|symbol)',
            self.content,
            re.DOTALL
        )
        assert orphaned_grep, \
            "Phase 5 orphaned import section must document Grep-based symbol usage search"

    def test_should_reference_symbol_name_in_search(self):
        """Phase 5 must reference searching for the imported symbol name."""
        lower = self.content.lower()
        assert 'symbol' in lower and 'search' in lower, \
            "Phase 5 must reference searching for the imported symbol name"

    def test_should_document_flagging_unused_imports(self):
        """Phase 5 must document that imports with zero usage are flagged."""
        lower = self.content.lower()
        assert ('flag' in lower or 'report' in lower or 'detect' in lower) and \
               ('unused' in lower or 'orphan' in lower), \
            "Phase 5 must document flagging unused/orphaned imports"
