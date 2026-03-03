"""
Test: AC#2 - TypeScript/JavaScript Import Detection
Story: STORY-402
Generated: 2026-02-14

Validates that anti-pattern-scanner.md Phase 5 section documents TypeScript/JavaScript
import Grep patterns for orphaned import detection, including ES6 import symbol extraction.

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


class TestAC2TypeScriptImportDetection:
    """AC#2: TypeScript/JavaScript Import Detection in anti-pattern-scanner.md Phase 5."""

    SCANNER_PATH = 'src/claude/agents/anti-pattern-scanner.md'

    # --- Arrange (shared fixture) ---

    @pytest.fixture(autouse=True)
    def setup(self):
        """Arrange: Load the anti-pattern-scanner.md content."""
        self.content = read_file(self.SCANNER_PATH)

    # --- Act & Assert ---

    def test_should_contain_typescript_import_grep_pattern(self):
        """Phase 5 must document the TS/JS import Grep pattern: ^import .+ from."""
        assert re.search(r'\^import \.\+ from', self.content) or \
               'import .+ from' in self.content, \
            "Phase 5 must contain TS/JS import Grep pattern: ^import .+ from"

    def test_should_reference_es6_import_syntax_in_orphaned_context(self):
        """Phase 5 orphaned import section must reference ES6 import syntax."""
        orphaned_es6 = re.search(
            r'(?i)orphaned.?import.*?(es6|esm|ecmascript|import\s+\{)',
            self.content,
            re.DOTALL
        )
        assert orphaned_es6, \
            "Phase 5 orphaned import section must reference ES6/ESM import syntax"

    def test_should_reference_typescript_language(self):
        """Phase 5 orphaned import section must reference TypeScript."""
        orphaned_section = re.search(
            r'(?i)orphaned.?import.*?typescript|typescript.*?orphaned.?import',
            self.content,
            re.DOTALL
        )
        assert orphaned_section, \
            "Orphaned import detection must reference TypeScript as a supported language"

    def test_should_reference_javascript_language(self):
        """Phase 5 orphaned import section must reference JavaScript."""
        orphaned_section = re.search(
            r'(?i)orphaned.?import.*?javascript|javascript.*?orphaned.?import',
            self.content,
            re.DOTALL
        )
        assert orphaned_section, \
            "Orphaned import detection must reference JavaScript as a supported language"

    def test_should_reference_es6_symbol_extraction(self):
        """Phase 5 must document symbol extraction from ES6 import statements."""
        lower = self.content.lower()
        # Must discuss extracting named imports like { X, Y } from '...'
        assert ('symbol' in lower or 'named import' in lower or 'destructur' in lower) and \
               ('extract' in lower or 'parse' in lower), \
            "Phase 5 must document ES6 import symbol extraction"

    def test_should_handle_both_named_and_default_imports_in_orphaned_context(self):
        """Phase 5 orphaned import section must document named and default import handling."""
        orphaned_named = re.search(
            r'(?i)orphaned.?import.*?(named\s+import|default\s+import|\{\s*\w+)',
            self.content,
            re.DOTALL
        )
        assert orphaned_named, \
            "Phase 5 orphaned import section must document both named and default import handling"
