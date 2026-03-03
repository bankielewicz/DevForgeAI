"""
Test: AC#5 - False Positive Suppression
Story: STORY-399
Generated: 2026-02-14

Validates that two-stage-filter-patterns.md documents suppression
of known false positive patterns (@dataclass, TypeScript interfaces, DTOs).

Tests validate STRUCTURE and CONTENT of Markdown files (not executable code).
All tests MUST FAIL initially (TDD Red phase) since the file has not been created yet.
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


class TestAC5FalsePositiveSuppression:
    """AC#5: False Positive Suppression in two-stage-filter-patterns.md."""

    FILTER_PATH = 'src/claude/agents/anti-pattern-scanner/references/two-stage-filter-patterns.md'

    # --- Act & Assert ---

    def test_should_document_dataclass_decorator_suppression(self):
        """Must document @dataclass decorator as a suppressed pattern."""
        content = read_file(self.FILTER_PATH)
        assert '@dataclass' in content, \
            "Must document @dataclass decorator suppression"

    def test_should_document_typescript_interface_exclusion(self):
        """Must document TypeScript interface exclusion from detection."""
        content = read_file(self.FILTER_PATH)
        assert re.search(r'TypeScript.*interface|interface.*TypeScript',
                         content, re.IGNORECASE), \
            "Must document TypeScript interface exclusion"

    def test_should_document_dto_with_validation_suppression(self):
        """Must document DTO with validation logic as a suppressed pattern."""
        content = read_file(self.FILTER_PATH)
        content_lower = content.lower()
        has_dto = 'dto' in content_lower
        has_validation = 'validation' in content_lower
        assert has_dto and has_validation, \
            "Must document DTO with validation logic suppression"

    def test_should_explain_confidence_below_07_for_valid_patterns(self):
        """Must explain that valid patterns receive confidence < 0.7."""
        content = read_file(self.FILTER_PATH)
        # Look for explanation linking confidence < 0.7 to valid/suppressed patterns
        assert re.search(r'confidence.*<\s*0\.7|confidence.*less.*0\.7|below.*0\.7',
                         content, re.IGNORECASE), \
            "Must explain that valid patterns receive confidence < 0.7"

    def test_should_list_at_least_three_suppression_patterns(self):
        """Must list at least 3 distinct false positive suppression patterns."""
        content = read_file(self.FILTER_PATH)
        content_lower = content.lower()
        patterns_found = 0
        if '@dataclass' in content:
            patterns_found += 1
        if re.search(r'typescript.*interface|interface.*typescript', content_lower):
            patterns_found += 1
        if 'dto' in content_lower:
            patterns_found += 1
        if 'record' in content_lower:
            patterns_found += 1
        if 'enum' in content_lower:
            patterns_found += 1
        assert patterns_found >= 3, \
            f"Must list at least 3 suppression patterns, found {patterns_found}"

    def test_should_explain_why_dataclass_is_valid(self):
        """Must explain why @dataclass is a valid pattern (not a code smell)."""
        content = read_file(self.FILTER_PATH)
        # @dataclass section should have an explanation of why it is valid
        assert re.search(r'@dataclass.*valid|@dataclass.*intentional|@dataclass.*decorator.*suppress',
                         content, re.IGNORECASE), \
            "Must explain why @dataclass decorated classes are valid patterns"

    def test_should_explain_why_interfaces_are_excluded(self):
        """Must explain why TypeScript interfaces are excluded (structural by design)."""
        content = read_file(self.FILTER_PATH)
        assert re.search(r'interface.*structural|interface.*design|interface.*not.*class',
                         content, re.IGNORECASE), \
            "Must explain that interfaces are structural by design, not data classes"
