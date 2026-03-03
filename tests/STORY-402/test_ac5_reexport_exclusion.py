"""
Test: AC#5 - Re-Export Exclusion
Story: STORY-402
Generated: 2026-02-14

Validates that anti-pattern-scanner.md Phase 5 section documents re-export exclusion
to prevent false positives on re-export patterns like export { X } from './y'.

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


class TestAC5ReExportExclusion:
    """AC#5: Re-Export Exclusion in anti-pattern-scanner.md Phase 5."""

    SCANNER_PATH = 'src/claude/agents/anti-pattern-scanner.md'

    # --- Arrange (shared fixture) ---

    @pytest.fixture(autouse=True)
    def setup(self):
        """Arrange: Load the anti-pattern-scanner.md content."""
        self.content = read_file(self.SCANNER_PATH)

    # --- Act & Assert ---

    def test_should_document_reexport_exclusion(self):
        """Phase 5 must document that re-exports are excluded from orphaned import detection."""
        lower = self.content.lower()
        assert ('re-export' in lower or 'reexport' in lower or 're_export' in lower) and \
               ('exclud' in lower or 'skip' in lower or 'not flagged' in lower), \
            "Phase 5 must document re-export exclusion"

    def test_should_reference_export_from_pattern(self):
        """Phase 5 must reference the 'export { X } from' pattern."""
        assert re.search(r'export\s*\{.*\}\s*from', self.content) or \
               'export {' in self.content, \
            "Phase 5 must reference 'export { X } from' pattern"

    def test_should_explain_reexports_are_not_orphaned(self):
        """Phase 5 must explain that re-exports are intentional and not orphaned."""
        lower = self.content.lower()
        assert ('re-export' in lower or 'reexport' in lower) and \
               ('intentional' in lower or 'not orphan' in lower or 'not flagged' in lower or
                'used as' in lower or 'mechanism' in lower), \
            "Phase 5 must explain that re-exports are intentional, not orphaned"

    def test_should_list_reexport_as_exclusion_rule(self):
        """Phase 5 must list re-export as an explicit exclusion rule."""
        lower = self.content.lower()
        assert ('exclusion' in lower or 'exclude' in lower or 'exception' in lower) and \
               ('re-export' in lower or 'reexport' in lower), \
            "Phase 5 must list re-export as an exclusion rule"
