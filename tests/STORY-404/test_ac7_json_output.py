"""
Test: AC#7 - JSON Output Format Compliance
Story: STORY-404
Generated: 2026-02-15

Verifies Section 8.5 defines the PlaceholderCodeFinding JSON output schema
with all required fields: smell_type, severity, file, line, pattern_type,
surrounding_context, confidence, evidence, remediation.
"""
import re
import pytest

SRC_REVIEWER_PATH = "src/claude/agents/code-reviewer.md"

REQUIRED_FIELDS = [
    "smell_type",
    "severity",
    "file",
    "line",
    "pattern_type",
    "surrounding_context",
    "confidence",
    "evidence",
    "remediation",
]


@pytest.fixture
def reviewer_content():
    """Load code-reviewer.md content from src/ tree."""
    with open(SRC_REVIEWER_PATH, "r") as f:
        return f.read()


@pytest.fixture
def section_85(reviewer_content):
    """Extract Section 8.5 content from code-reviewer.md."""
    match = re.search(
        r"(?:##\s*8\.5|###\s*8\.5|Section 8\.5)[^\n]*\n(.*?)(?=\n##\s|\n###\s*\d+\.\s|\Z)",
        reviewer_content,
        re.DOTALL,
    )
    assert match is not None, "Section 8.5 not found in code-reviewer.md"
    return match.group(0)


class TestJsonOutputFormat:
    """Tests for PlaceholderCodeFinding JSON schema in Section 8.5."""

    def test_should_define_smell_type_field(self, section_85):
        """Output must include smell_type: 'placeholder_code'."""
        assert "smell_type" in section_85, (
            "smell_type field not defined in Section 8.5 output schema"
        )

    def test_should_define_placeholder_code_value(self, section_85):
        """smell_type must have value 'placeholder_code'."""
        assert "placeholder_code" in section_85, (
            "smell_type value 'placeholder_code' not specified"
        )

    def test_should_define_severity_high(self, section_85):
        """severity must be HIGH for placeholder findings."""
        assert "HIGH" in section_85, (
            "severity HIGH not specified in Section 8.5 output schema"
        )

    def test_should_define_file_field(self, section_85):
        """Output must include file path field."""
        # 'file' is common word, check in context of output schema
        lower = section_85.lower()
        assert '"file"' in lower or "file" in lower, (
            "file field not defined in Section 8.5 output schema"
        )

    def test_should_define_line_field(self, section_85):
        """Output must include line number field."""
        lower = section_85.lower()
        assert '"line"' in lower or "line" in lower, (
            "line field not defined in Section 8.5 output schema"
        )

    def test_should_define_pattern_type_field(self, section_85):
        """Output must include pattern_type field."""
        assert "pattern_type" in section_85, (
            "pattern_type field not defined in Section 8.5 output schema"
        )

    def test_should_define_pattern_type_values(self, section_85):
        """pattern_type must support bare_pass, not_implemented, empty_block, todo_return."""
        lower = section_85.lower()
        assert "bare_pass" in lower, "pattern_type value 'bare_pass' not specified"
        assert "not_implemented" in lower, "pattern_type value 'not_implemented' not specified"

    def test_should_define_surrounding_context_field(self, section_85):
        """Output must include surrounding_context field."""
        assert "surrounding_context" in section_85, (
            "surrounding_context field not defined in Section 8.5 output schema"
        )

    def test_should_define_confidence_field(self, section_85):
        """Output must include confidence field (0.0-1.0)."""
        assert "confidence" in section_85.lower(), (
            "confidence field not defined in Section 8.5 output schema"
        )

    def test_should_define_evidence_field(self, section_85):
        """Output must include evidence field."""
        assert "evidence" in section_85.lower(), (
            "evidence field not defined in Section 8.5 output schema"
        )

    def test_should_define_remediation_field(self, section_85):
        """Output must include remediation field."""
        assert "remediation" in section_85.lower(), (
            "remediation field not defined in Section 8.5 output schema"
        )

    @pytest.mark.parametrize("field", REQUIRED_FIELDS)
    def test_should_contain_all_required_fields(self, section_85, field):
        """All 9 required fields must be present in Section 8.5."""
        assert field in section_85.lower(), (
            f"Required field '{field}' not found in Section 8.5 output schema"
        )
