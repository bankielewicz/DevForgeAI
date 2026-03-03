"""
Test: AC#6 - Side-Effect Import Exclusion
Story: STORY-402
Generated: 2026-02-14

Validates that anti-pattern-scanner.md Phase 5 section documents side-effect import
exclusion to prevent false positives on imports like import './polyfill' that have
no imported symbol.

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


class TestAC6SideEffectExclusion:
    """AC#6: Side-Effect Import Exclusion in anti-pattern-scanner.md Phase 5."""

    SCANNER_PATH = 'src/claude/agents/anti-pattern-scanner.md'

    # --- Arrange (shared fixture) ---

    @pytest.fixture(autouse=True)
    def setup(self):
        """Arrange: Load the anti-pattern-scanner.md content."""
        self.content = read_file(self.SCANNER_PATH)

    # --- Act & Assert ---

    def test_should_document_side_effect_import_exclusion(self):
        """Phase 5 must document that side-effect imports are excluded."""
        lower = self.content.lower()
        assert ('side-effect' in lower or 'side effect' in lower or 'sideeffect' in lower) and \
               ('exclud' in lower or 'skip' in lower or 'not flagged' in lower), \
            "Phase 5 must document side-effect import exclusion"

    def test_should_reference_polyfill_import_pattern(self):
        """Phase 5 must reference the import './polyfill' pattern as an example."""
        assert "import './polyfill'" in self.content or \
               "import './polyfill'" in self.content.replace('"', "'") or \
               re.search(r"import\s+['\"]\.?/", self.content), \
            "Phase 5 must reference import './polyfill' pattern or similar side-effect import"

    def test_should_explain_no_symbol_binding(self):
        """Phase 5 must explain that side-effect imports have no symbol to check."""
        lower = self.content.lower()
        assert ('no symbol' in lower or 'no imported symbol' in lower or
                'no binding' in lower or 'no named' in lower), \
            "Phase 5 must explain that side-effect imports have no symbol to check"

    def test_should_list_side_effect_as_exclusion_rule(self):
        """Phase 5 must list side-effect import as an explicit exclusion rule."""
        lower = self.content.lower()
        assert ('exclusion' in lower or 'exclude' in lower or 'exception' in lower) and \
               ('side-effect' in lower or 'side effect' in lower), \
            "Phase 5 must list side-effect import as an exclusion rule"

    def test_should_reference_css_or_style_imports_in_orphaned_context(self):
        """Phase 5 orphaned import section should reference CSS/style/polyfill as side-effect examples."""
        orphaned_css = re.search(
            r'(?i)orphaned.?import.*?(css|polyfill|\.css)',
            self.content,
            re.DOTALL
        )
        assert orphaned_css, \
            "Phase 5 orphaned import section should reference CSS/style/polyfill as side-effect examples"
