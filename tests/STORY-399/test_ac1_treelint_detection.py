"""
Test: AC#1 - Treelint-Based Data Class Detection
Story: STORY-399
Generated: 2026-02-14

Validates that anti-pattern-scanner.md Phase 5 section contains
data class detection instructions using Treelint AST queries.

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


class TestAC1TreelintDetection:
    """AC#1: Treelint-Based Data Class Detection in anti-pattern-scanner.md Phase 5."""

    SCANNER_PATH = 'src/claude/agents/anti-pattern-scanner.md'

    # --- Arrange (shared fixture) ---

    @pytest.fixture(autouse=True)
    def setup(self):
        """Arrange: Load the anti-pattern-scanner.md content."""
        self.content = read_file(self.SCANNER_PATH)

    # --- Act & Assert ---

    def test_should_contain_data_class_detection_in_phase5(self):
        """Phase 5 (Code Smells) must include data class detection alongside existing smells."""
        # The content should mention data class detection in the Phase 5 context
        assert 'data class' in self.content.lower() or 'data_class' in self.content.lower(), \
            "Phase 5 must reference 'data class' or 'data_class' detection"

    def test_should_reference_treelint_search_class_query(self):
        """Phase 5 must reference a treelint search --type class query."""
        assert 'treelint search --type class' in self.content, \
            "Phase 5 must contain 'treelint search --type class' query reference"

    def test_should_contain_method_count_threshold(self):
        """Threshold logic must specify method_count < 3."""
        # Look for method_count threshold reference
        assert re.search(r'method_count\s*[<]\s*3', self.content), \
            "Phase 5 must specify threshold 'method_count < 3'"

    def test_should_contain_property_count_threshold(self):
        """Threshold logic must specify property_count > 2."""
        assert re.search(r'property_count\s*[>]\s*2', self.content), \
            "Phase 5 must specify threshold 'property_count > 2'"

    def test_should_contain_combined_threshold_logic(self):
        """Threshold must combine both conditions with AND logic."""
        # Look for AND combination of method_count and property_count
        assert re.search(r'method_count.*AND.*property_count|property_count.*AND.*method_count',
                         self.content, re.IGNORECASE), \
            "Phase 5 must combine method_count and property_count with AND logic"

    def test_should_reference_json_members_methods(self):
        """Must reference parsing members.methods from Treelint JSON output."""
        assert 'members.methods' in self.content, \
            "Phase 5 must reference 'members.methods' JSON field for Treelint parsing"

    def test_should_reference_json_members_properties(self):
        """Must reference parsing members.properties from Treelint JSON output."""
        assert 'members.properties' in self.content, \
            "Phase 5 must reference 'members.properties' JSON field for Treelint parsing"

    def test_should_list_data_class_alongside_existing_smells(self):
        """Data class detection must appear alongside god objects, long methods, magic numbers."""
        # Verify data class is listed as a code smell in Phase 5
        phase5_pattern = re.search(
            r'(?i)(phase\s*5|code\s*smell).*?(data.?class)',
            self.content,
            re.DOTALL
        )
        assert phase5_pattern, \
            "Data class must be listed as a code smell in Phase 5 section"

    def test_should_contain_format_json_flag(self):
        """Treelint query must use --format json for AI consumption."""
        assert '--format json' in self.content, \
            "Treelint query must include '--format json' flag for structured output"
