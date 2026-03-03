"""
Test: AC#4 - JSON Output Format Compliance
Story: STORY-399
Generated: 2026-02-14

Validates that anti-pattern-scanner.md or two-stage-filter-patterns.md
documents the DataClassFinding output schema with all required fields.

Tests validate STRUCTURE and CONTENT of Markdown files (not executable code).
All tests MUST FAIL initially (TDD Red phase) since content has not been added yet.
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

SCANNER_PATH = 'src/claude/agents/anti-pattern-scanner.md'
FILTER_PATH = 'src/claude/agents/anti-pattern-scanner/references/two-stage-filter-patterns.md'

REQUIRED_FIELDS = [
    'smell_type',
    'severity',
    'class_name',
    'file',
    'line',
    'method_count',
    'property_count',
    'confidence',
    'evidence',
    'remediation',
]


def read_combined_content():
    """Read content from both source files for output schema validation."""
    combined = ''
    for path in [SCANNER_PATH, FILTER_PATH]:
        full_path = os.path.join(PROJECT_ROOT, path)
        if os.path.isfile(full_path):
            with open(full_path, 'r') as f:
                combined += f.read() + '\n'
    return combined


class TestAC4JsonOutput:
    """AC#4: JSON Output Format Compliance - DataClassFinding schema."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Arrange: Load combined content from scanner and filter files."""
        self.content = read_combined_content()

    # --- Act & Assert ---

    def test_should_document_dataclassfinding_schema(self):
        """Must document the DataClassFinding output schema."""
        assert re.search(r'DataClassFinding|data.?class.?finding',
                         self.content, re.IGNORECASE), \
            "Must document the DataClassFinding output schema"

    @pytest.mark.parametrize('field', REQUIRED_FIELDS)
    def test_should_contain_required_field(self, field):
        """Each required field must be documented in the output schema."""
        assert field in self.content, \
            f"Output schema must document required field: '{field}'"

    def test_should_specify_smell_type_as_data_class(self):
        """smell_type field must be fixed as 'data_class'."""
        # Look for smell_type being set to "data_class"
        assert re.search(r'smell_type.*["\']?data_class["\']?|["\']?data_class["\']?.*smell_type',
                         self.content), \
            "smell_type must be documented as fixed value 'data_class'"

    def test_should_specify_severity_as_medium(self):
        """severity field must be fixed as 'MEDIUM'."""
        assert re.search(r'severity.*MEDIUM|MEDIUM.*severity', self.content), \
            "severity must be documented as fixed value 'MEDIUM'"

    def test_should_specify_confidence_range(self):
        """confidence field must be documented as range 0.0-1.0."""
        assert re.search(r'0\.0.*1\.0|confidence.*range|confidence.*float',
                         self.content, re.IGNORECASE), \
            "confidence must be documented as float in range 0.0-1.0"

    def test_should_contain_all_ten_required_fields(self):
        """All 10 required fields must be present in the documentation."""
        missing = [f for f in REQUIRED_FIELDS if f not in self.content]
        assert len(missing) == 0, \
            f"Missing required fields in output schema: {missing}"
