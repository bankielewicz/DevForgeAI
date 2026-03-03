"""
Test: AC#8 - JSON Output Format Compliance
Story: STORY-402
Generated: 2026-02-14

Validates that anti-pattern-scanner.md Phase 5 documents the OrphanedImportFinding
JSON output schema with all 9 required fields: smell_type, severity, file, line,
import_statement, imported_symbol, usage_count, evidence, remediation.

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


class TestAC8JsonOutputFormat:
    """AC#8: JSON Output Format Compliance in anti-pattern-scanner.md Phase 5."""

    SCANNER_PATH = 'src/claude/agents/anti-pattern-scanner.md'

    REQUIRED_FIELDS = [
        'smell_type',
        'severity',
        'file',
        'line',
        'import_statement',
        'imported_symbol',
        'usage_count',
        'evidence',
        'remediation',
    ]

    # --- Arrange (shared fixture) ---

    @pytest.fixture(autouse=True)
    def setup(self):
        """Arrange: Load the anti-pattern-scanner.md content."""
        self.content = read_file(self.SCANNER_PATH)
        self.orphaned_section = extract_orphaned_import_section(self.content)

    # --- Act & Assert ---

    def test_should_document_orphaned_import_finding_schema(self):
        """Phase 5 must document the OrphanedImportFinding output schema."""
        lower = self.content.lower()
        assert ('orphanedimportfinding' in lower or 'orphaned_import_finding' in lower or
                ('orphaned' in lower and 'finding' in lower and 'output' in lower)), \
            "Phase 5 must document OrphanedImportFinding output schema"

    @pytest.mark.parametrize("field_name", [
        'smell_type',
        'severity',
        'file',
        'line',
        'import_statement',
        'imported_symbol',
        'usage_count',
        'evidence',
        'remediation',
    ])
    def test_should_include_required_field_in_orphaned_import_schema(self, field_name):
        """Each of the 9 required fields must be present in the orphaned import schema."""
        assert self.orphaned_section, \
            "Orphaned import section not found in anti-pattern-scanner.md"
        patterns = [
            rf'`{field_name}`',
            rf'"{field_name}"',
            rf"'{field_name}'",
            rf'\b{field_name}\b',
        ]
        found = any(re.search(p, self.orphaned_section) for p in patterns)
        assert found, \
            f"Required field '{field_name}' not found in OrphanedImportFinding schema section"

    def test_should_specify_smell_type_as_orphaned_import(self):
        """Schema must specify smell_type value as 'orphaned_import'."""
        assert 'orphaned_import' in self.content, \
            "Schema must specify smell_type = 'orphaned_import'"

    def test_should_specify_severity_as_low_in_orphaned_context(self):
        """Schema must specify severity as 'LOW' in orphaned import context."""
        orphaned_low = re.search(
            r'(?i)orphaned.?import.*?severity.*?LOW',
            self.content,
            re.DOTALL
        )
        assert orphaned_low, \
            "Schema must specify severity = 'LOW' in orphaned import context"

    def test_should_include_all_nine_required_fields_in_orphaned_section(self):
        """Orphaned import schema must include all 9 required fields."""
        assert self.orphaned_section, \
            "Orphaned import section not found in anti-pattern-scanner.md"
        missing = []
        for field in self.REQUIRED_FIELDS:
            patterns = [
                rf'`{field}`',
                rf'"{field}"',
                rf"'{field}'",
                rf'\b{field}\b',
            ]
            if not any(re.search(p, self.orphaned_section) for p in patterns):
                missing.append(field)

        assert len(missing) == 0, \
            f"OrphanedImportFinding schema missing {len(missing)} fields: {missing}"

    def test_should_specify_usage_count_as_zero(self):
        """Schema must specify that usage_count is always 0 for orphaned imports."""
        assert re.search(r'usage_count.*0', self.content) or \
               re.search(r'usage.count.*zero', self.content.lower()), \
            "Schema must specify usage_count = 0 for orphaned imports"

    def test_should_include_remediation_with_removal_in_orphaned_context(self):
        """Schema must include remediation suggesting import removal in orphaned context."""
        orphaned_remediation = re.search(
            r'(?i)orphaned.?import.*?remediation.*?(remove|delete)',
            self.content,
            re.DOTALL
        )
        assert orphaned_remediation, \
            "Schema must include remediation suggesting import removal in orphaned import context"
