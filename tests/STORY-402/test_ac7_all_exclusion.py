"""
Test: AC#7 - Python __all__ Exclusion
Story: STORY-402
Generated: 2026-02-14

Validates that anti-pattern-scanner.md Phase 5 section documents __all__ handling,
where symbols listed in __all__ are considered used (exported as public API).

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


class TestAC7AllExclusion:
    """AC#7: Python __all__ Exclusion in anti-pattern-scanner.md Phase 5."""

    SCANNER_PATH = 'src/claude/agents/anti-pattern-scanner.md'

    # --- Arrange (shared fixture) ---

    @pytest.fixture(autouse=True)
    def setup(self):
        """Arrange: Load the anti-pattern-scanner.md content."""
        self.content = read_file(self.SCANNER_PATH)

    # --- Act & Assert ---

    def test_should_document_dunder_all_handling(self):
        """Phase 5 must document __all__ handling for Python files."""
        assert '__all__' in self.content, \
            "Phase 5 must document __all__ handling for Python orphaned import detection"

    def test_should_specify_symbols_in_all_are_used(self):
        """Phase 5 must specify that symbols listed in __all__ are considered used."""
        lower = self.content.lower()
        has_all = '__all__' in self.content
        has_used = 'used' in lower or 'considered used' in lower or 'not orphaned' in lower or \
                   'not flagged' in lower
        assert has_all and has_used, \
            "Phase 5 must specify that symbols in __all__ are considered used"

    def test_should_reference_public_api_context(self):
        """Phase 5 must reference that __all__ defines the public API."""
        lower = self.content.lower()
        assert ('public api' in lower or 'public interface' in lower or
                'exported' in lower or 'module api' in lower) and '__all__' in self.content, \
            "Phase 5 must reference that __all__ defines the public API"

    def test_should_document_all_parsing_logic(self):
        """Phase 5 must document how to parse __all__ list for symbol names."""
        lower = self.content.lower()
        assert '__all__' in self.content and \
               ('parse' in lower or 'extract' in lower or 'read' in lower), \
            "Phase 5 must document parsing __all__ to extract symbol names"

    def test_should_list_all_as_exclusion_rule(self):
        """Phase 5 must list __all__ as an exclusion rule for orphaned imports."""
        lower = self.content.lower()
        has_all = '__all__' in self.content
        has_exclusion = 'exclusion' in lower or 'exclude' in lower or 'exception' in lower or \
                        'skip' in lower
        assert has_all and has_exclusion, \
            "Phase 5 must list __all__ as an exclusion rule"
