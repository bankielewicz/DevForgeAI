"""
Test: AC#1 - Code Smell Catalog Reference File Created
Story: STORY-407
Generated: 2026-02-16

Validates that .claude/agents/anti-pattern-scanner/references/code-smell-catalog.md
contains all 11 smell types with required sections, thresholds, and cross-references.
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CATALOG_PATH = os.path.join(
    PROJECT_ROOT,
    ".claude", "agents", "anti-pattern-scanner", "references", "code-smell-catalog.md",
)

SMELL_TYPES = [
    "god_object",
    "long_method",
    "magic_number",
    "data_class",
    "long_parameter_list",
    "commented_out_code",
    "orphaned_import",
    "dead_code",
    "placeholder_code",
    "middle_man",
    "message_chain",
]

# Human-readable names expected in the catalog
SMELL_NAMES = [
    "God Object",
    "Long Method",
    "Magic Number",
    "Data Class",
    "Long Parameter List",
    "Commented-Out Code",
    "Orphaned Import",
    "Dead Code",
    "Placeholder Code",
    "Middle Man",
    "Message Chain",
]

VALID_SEVERITIES = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
VALID_DETECTION_METHODS = ["Treelint", "Grep", "Hybrid"]


@pytest.fixture(scope="module")
def catalog_content():
    """Read catalog file content."""
    assert os.path.isfile(CATALOG_PATH), (
        f"Catalog file does not exist at {CATALOG_PATH}"
    )
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        return f.read()


class TestCatalogFileExists:
    """Tests for catalog file existence and basic structure."""

    def test_should_exist_at_correct_path(self):
        """Arrange: Expected path defined. Act: Check file. Assert: File exists."""
        assert os.path.isfile(CATALOG_PATH), (
            f"Catalog file not found at {CATALOG_PATH}"
        )

    def test_should_be_markdown_format(self, catalog_content):
        """Assert: File starts with markdown heading."""
        assert catalog_content.strip().startswith("#"), (
            "Catalog file should start with a markdown heading"
        )


class TestSummaryTable:
    """Tests for the summary table containing all 11 smell types."""

    def test_should_contain_summary_table(self, catalog_content):
        """Assert: A markdown table with pipe characters exists."""
        assert "|" in catalog_content, "Catalog should contain a summary table"

    def test_should_list_all_11_smell_types_in_table(self, catalog_content):
        """Assert: All 11 smell names appear in the catalog."""
        for name in SMELL_NAMES:
            assert name.lower() in catalog_content.lower(), (
                f"Smell type '{name}' not found in catalog"
            )

    def test_should_have_exactly_11_smell_types(self, catalog_content):
        """Assert: Exactly 11 smell type sections exist."""
        # Count level-2 or level-3 headings that match smell names
        section_count = 0
        for name in SMELL_NAMES:
            pattern = rf"#{{2,3}}\s+.*{re.escape(name)}"
            if re.search(pattern, catalog_content, re.IGNORECASE):
                section_count += 1
        assert section_count == 11, (
            f"Expected 11 smell type sections, found {section_count}"
        )

    def test_should_have_name_column_in_table(self, catalog_content):
        """Assert: Table has Name column header."""
        assert re.search(r"\|\s*Name\s*\|", catalog_content, re.IGNORECASE), (
            "Summary table should have a 'Name' column"
        )

    def test_should_have_threshold_column_in_table(self, catalog_content):
        """Assert: Table has Threshold column header."""
        assert re.search(r"\|\s*Threshold\s*\|", catalog_content, re.IGNORECASE), (
            "Summary table should have a 'Threshold' column"
        )

    def test_should_have_severity_column_in_table(self, catalog_content):
        """Assert: Table has Severity column header."""
        assert re.search(r"\|\s*Severity\s*\|", catalog_content, re.IGNORECASE), (
            "Summary table should have a 'Severity' column"
        )

    def test_should_have_detection_method_column_in_table(self, catalog_content):
        """Assert: Table has Detection Method column header."""
        assert re.search(
            r"\|\s*Detection\s*Method\s*\|", catalog_content, re.IGNORECASE
        ), "Summary table should have a 'Detection Method' column"

    def test_should_have_two_stage_column_in_table(self, catalog_content):
        """Assert: Table has Two-Stage column header."""
        assert re.search(
            r"\|\s*Two.Stage\s*\|", catalog_content, re.IGNORECASE
        ), "Summary table should have a 'Two-Stage' column"


class TestDetailedSections:
    """Tests for detailed sections per smell type."""

    @pytest.mark.parametrize("smell_name", SMELL_NAMES)
    def test_should_have_definition_section(self, catalog_content, smell_name):
        """Assert: Each smell has a definition."""
        # Look for definition keyword near the smell section
        pattern = rf"(?i){re.escape(smell_name)}.*?definition"
        assert re.search(pattern, catalog_content, re.DOTALL), (
            f"'{smell_name}' missing definition section"
        )

    @pytest.mark.parametrize("smell_name", SMELL_NAMES)
    def test_should_have_threshold_documented(self, catalog_content, smell_name):
        """Assert: Each smell has threshold(s) documented."""
        pattern = rf"(?i){re.escape(smell_name)}.*?threshold"
        assert re.search(pattern, catalog_content, re.DOTALL), (
            f"'{smell_name}' missing threshold documentation"
        )

    @pytest.mark.parametrize("smell_name", SMELL_NAMES)
    def test_should_have_severity_value(self, catalog_content, smell_name):
        """Assert: Each smell has a valid severity level."""
        # Find the section for this smell, then check severity
        pattern = rf"(?i){re.escape(smell_name)}.*?severity[:\s]*(CRITICAL|HIGH|MEDIUM|LOW)"
        assert re.search(pattern, catalog_content, re.DOTALL), (
            f"'{smell_name}' missing valid severity (CRITICAL/HIGH/MEDIUM/LOW)"
        )

    @pytest.mark.parametrize("smell_name", SMELL_NAMES)
    def test_should_have_detection_method(self, catalog_content, smell_name):
        """Assert: Each smell has detection method (Treelint/Grep/Hybrid)."""
        pattern = rf"(?i){re.escape(smell_name)}.*?(Treelint|Grep|Hybrid)"
        assert re.search(pattern, catalog_content, re.DOTALL), (
            f"'{smell_name}' missing detection method (Treelint/Grep/Hybrid)"
        )

    @pytest.mark.parametrize("smell_name", SMELL_NAMES)
    def test_should_have_two_stage_flag(self, catalog_content, smell_name):
        """Assert: Each smell has two-stage flag documented."""
        pattern = rf"(?i){re.escape(smell_name)}.*?two.stage"
        assert re.search(pattern, catalog_content, re.DOTALL), (
            f"'{smell_name}' missing two-stage flag documentation"
        )

    @pytest.mark.parametrize("smell_name", SMELL_NAMES)
    def test_should_have_json_schema(self, catalog_content, smell_name):
        """Assert: Each smell has JSON output schema documented."""
        pattern = rf"(?i){re.escape(smell_name)}.*?json"
        assert re.search(pattern, catalog_content, re.DOTALL), (
            f"'{smell_name}' missing JSON schema documentation"
        )

    @pytest.mark.parametrize("smell_name", SMELL_NAMES)
    def test_should_have_test_scenarios(self, catalog_content, smell_name):
        """Assert: Each smell has test scenarios documented."""
        pattern = rf"(?i){re.escape(smell_name)}.*?test.scenario"
        assert re.search(pattern, catalog_content, re.DOTALL), (
            f"'{smell_name}' missing test scenarios"
        )

    @pytest.mark.parametrize("smell_name", SMELL_NAMES)
    def test_should_have_false_positive_patterns(self, catalog_content, smell_name):
        """Assert: Each smell has false positive patterns documented."""
        pattern = rf"(?i){re.escape(smell_name)}.*?false.positive"
        assert re.search(pattern, catalog_content, re.DOTALL), (
            f"'{smell_name}' missing false positive patterns"
        )


class TestTestScenarioCoverage:
    """Tests for minimum test scenario counts."""

    @pytest.mark.parametrize("smell_name", SMELL_NAMES)
    def test_should_have_at_least_3_test_scenarios_per_smell(
        self, catalog_content, smell_name
    ):
        """Assert: At least 3 test scenarios per smell type (33+ total)."""
        # Find section for this smell, count numbered/bulleted test scenarios
        pattern = rf"(?is)#{{2,3}}\s+.*?{re.escape(smell_name)}.*?(?=#{{2,3}}\s|\Z)"
        section_match = re.search(pattern, catalog_content)
        assert section_match, f"Could not find section for '{smell_name}'"
        section = section_match.group(0)
        # Count items under test scenarios
        scenario_pattern = r"(?:^|\n)\s*[-*\d]+[.)]\s+"
        scenarios = re.findall(scenario_pattern, section)
        assert len(scenarios) >= 3, (
            f"'{smell_name}' has {len(scenarios)} test scenarios, need at least 3"
        )


class TestFowlerCrossReferences:
    """Tests for Fowler's refactoring catalog cross-references."""

    def test_should_contain_fowler_references(self, catalog_content):
        """Assert: Catalog references Fowler's refactoring catalog."""
        assert re.search(r"(?i)fowler", catalog_content), (
            "Catalog should reference Fowler's refactoring catalog"
        )

    def test_should_contain_refactoring_guru_or_fowler_link(self, catalog_content):
        """Assert: Contains link to refactoring resource."""
        assert re.search(
            r"(?i)(refactoring\.guru|refactoring.*catalog|fowler)", catalog_content
        ), "Catalog should contain cross-reference to Fowler/refactoring resource"
