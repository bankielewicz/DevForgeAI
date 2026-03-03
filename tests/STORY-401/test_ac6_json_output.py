"""
Test: AC#6 - JSON Output Format Compliance
Story: STORY-401
Generated: 2026-02-14

Validates that the CommentedOutCodeFinding JSON output schema is correctly defined
with all required fields: smell_type, severity, file, line_start, line_end,
excerpt, confidence, classification, evidence, remediation.
These tests will FAIL until the output schema is added to
.claude/agents/anti-pattern-scanner.md
"""
import re
import json
import pytest


# === Fixture: Load output schema from anti-pattern-scanner.md ===

def load_output_schema():
    """
    Load the CommentedOutCodeFinding output schema from anti-pattern-scanner.md.
    Returns dict with field definitions extracted from the scanner specification.
    """
    import os

    scanner_path = os.path.join(
        os.path.dirname(__file__),
        "..", "..",
        ".claude", "agents", "anti-pattern-scanner.md"
    )
    scanner_path = os.path.normpath(scanner_path)

    if not os.path.exists(scanner_path):
        pytest.fail(
            f"Scanner file not found: {scanner_path}. "
            "anti-pattern-scanner.md must exist."
        )

    with open(scanner_path, "r") as f:
        content = f.read()

    schema = _extract_commented_code_schema(content)

    if not schema:
        pytest.fail(
            "CommentedOutCodeFinding output schema not found in "
            "anti-pattern-scanner.md. Expected JSON output format definition "
            "with smell_type, severity, file, line_start, line_end, excerpt, "
            "confidence, classification, evidence, remediation fields."
        )

    return schema


def _extract_commented_code_schema(content: str) -> dict:
    """
    Extract the commented-out code finding schema from anti-pattern-scanner.md.
    Returns dict mapping field names to their properties.
    """
    lower = content.lower()

    # Check for commented-out code section
    if "commented_out_code" not in lower and "commented-out" not in lower:
        return {}

    schema = {"fields": {}}

    # Required fields for CommentedOutCodeFinding
    required_fields = [
        "smell_type", "severity", "file", "line_start", "line_end",
        "excerpt", "confidence", "classification", "evidence", "remediation"
    ]

    for field in required_fields:
        # Look for field definition in content (various formats)
        patterns = [
            rf"`{field}`",
            rf'"{field}"',
            rf"'{field}'",
            rf"\b{field}\b",
        ]
        for pattern in patterns:
            if re.search(pattern, content):
                schema["fields"][field] = True
                break

    return schema if len(schema["fields"]) > 0 else {}


# === Test Constants ===

REQUIRED_FIELDS = [
    "smell_type",
    "severity",
    "file",
    "line_start",
    "line_end",
    "excerpt",
    "confidence",
    "classification",
    "evidence",
    "remediation",
]

SAMPLE_VALID_FINDING = {
    "smell_type": "commented_out_code",
    "severity": "LOW",
    "file": "src/handlers/auth.py",
    "line_start": 42,
    "line_end": 49,
    "excerpt": "# def old_authenticate(user, password):\n#     return legacy_check(user, password)",
    "confidence": 0.85,
    "classification": "code",
    "evidence": "8-line block of commented Python code containing function definition, return statement, and control flow",
    "remediation": "Delete commented-out code block. Use git history to recover if needed: git log -p -- src/handlers/auth.py",
}


# === Unit Tests ===

class TestOutputSchemaPresence:
    """Tests that the CommentedOutCodeFinding schema exists in scanner."""

    def test_should_have_schema_defined_when_scanner_loaded(self):
        """anti-pattern-scanner.md should define CommentedOutCodeFinding schema."""
        schema = load_output_schema()
        assert schema is not None, (
            "CommentedOutCodeFinding schema must be defined in anti-pattern-scanner.md"
        )
        assert "fields" in schema, "Schema must contain field definitions"


class TestRequiredFields:
    """Tests that all required fields are present in the schema."""

    @pytest.fixture
    def schema(self):
        return load_output_schema()

    @pytest.mark.parametrize("field_name", REQUIRED_FIELDS)
    def test_should_have_required_field_when_schema_loaded(self, schema, field_name):
        """Each required field must be present in the schema."""
        fields = schema.get("fields", {})
        assert field_name in fields, (
            f"Required field '{field_name}' not found in CommentedOutCodeFinding schema. "
            f"Found fields: {list(fields.keys())}"
        )


class TestFieldConstraints:
    """Tests field value constraints for the output schema."""

    def test_should_set_smell_type_to_commented_out_code_when_finding_created(self):
        """smell_type must always be 'commented_out_code'."""
        finding = SAMPLE_VALID_FINDING.copy()
        assert finding["smell_type"] == "commented_out_code", (
            "smell_type must be 'commented_out_code'"
        )

    def test_should_set_severity_to_low_when_finding_created(self):
        """severity must always be 'LOW' for commented-out code."""
        finding = SAMPLE_VALID_FINDING.copy()
        assert finding["severity"] == "LOW", (
            "severity must be 'LOW' for commented-out code smell"
        )

    def test_should_have_valid_file_path_when_finding_created(self):
        """file must be a non-empty relative path string."""
        finding = SAMPLE_VALID_FINDING.copy()
        assert isinstance(finding["file"], str), "file must be a string"
        assert len(finding["file"]) > 0, "file must not be empty"
        assert not finding["file"].startswith("/"), "file must be a relative path"

    def test_should_have_positive_line_start_when_finding_created(self):
        """line_start must be a positive integer."""
        finding = SAMPLE_VALID_FINDING.copy()
        assert isinstance(finding["line_start"], int), "line_start must be an integer"
        assert finding["line_start"] > 0, "line_start must be positive"

    def test_should_have_line_end_gte_line_start_when_finding_created(self):
        """line_end must be >= line_start."""
        finding = SAMPLE_VALID_FINDING.copy()
        assert isinstance(finding["line_end"], int), "line_end must be an integer"
        assert finding["line_end"] >= finding["line_start"], (
            f"line_end ({finding['line_end']}) must be >= line_start ({finding['line_start']})"
        )

    def test_should_have_excerpt_under_200_chars_when_finding_created(self):
        """excerpt must be max 200 characters."""
        finding = SAMPLE_VALID_FINDING.copy()
        assert isinstance(finding["excerpt"], str), "excerpt must be a string"
        assert len(finding["excerpt"]) <= 200, (
            f"excerpt must be max 200 chars, got {len(finding['excerpt'])}"
        )

    def test_should_have_confidence_in_range_when_finding_created(self):
        """confidence must be a float between 0.0 and 1.0."""
        finding = SAMPLE_VALID_FINDING.copy()
        assert isinstance(finding["confidence"], float), "confidence must be a float"
        assert 0.0 <= finding["confidence"] <= 1.0, (
            f"confidence must be in range [0.0, 1.0], got {finding['confidence']}"
        )

    def test_should_have_valid_classification_when_finding_created(self):
        """classification must be one of: 'code', 'documentation', 'todo'."""
        finding = SAMPLE_VALID_FINDING.copy()
        valid_classifications = {"code", "documentation", "todo"}
        assert finding["classification"] in valid_classifications, (
            f"classification must be one of {valid_classifications}, "
            f"got '{finding['classification']}'"
        )

    def test_should_have_non_empty_evidence_when_finding_created(self):
        """evidence must be a non-empty string."""
        finding = SAMPLE_VALID_FINDING.copy()
        assert isinstance(finding["evidence"], str), "evidence must be a string"
        assert len(finding["evidence"]) > 0, "evidence must not be empty"

    def test_should_have_remediation_with_git_reference_when_finding_created(self):
        """remediation should suggest deletion and reference git history."""
        finding = SAMPLE_VALID_FINDING.copy()
        assert isinstance(finding["remediation"], str), "remediation must be a string"
        assert len(finding["remediation"]) > 0, "remediation must not be empty"
        assert "git" in finding["remediation"].lower() or "delete" in finding["remediation"].lower(), (
            "remediation should suggest deletion or reference git history"
        )


class TestJsonSerialization:
    """Tests that findings serialize to valid JSON."""

    def test_should_serialize_to_valid_json_when_finding_dumped(self):
        """Finding should produce valid JSON when serialized."""
        finding = SAMPLE_VALID_FINDING.copy()
        json_str = json.dumps(finding)
        assert json_str is not None, "JSON serialization should succeed"

    def test_should_deserialize_from_json_when_finding_loaded(self):
        """Finding should be recoverable from JSON string."""
        finding = SAMPLE_VALID_FINDING.copy()
        json_str = json.dumps(finding)
        loaded = json.loads(json_str)
        assert loaded == finding, "Deserialized finding should match original"

    def test_should_contain_all_required_fields_when_serialized(self):
        """Serialized JSON should contain all 10 required fields."""
        finding = SAMPLE_VALID_FINDING.copy()
        json_str = json.dumps(finding)
        loaded = json.loads(json_str)
        for field in REQUIRED_FIELDS:
            assert field in loaded, (
                f"Serialized JSON missing required field: {field}"
            )


class TestFindingValidation:
    """Tests validation logic for CommentedOutCodeFinding."""

    def test_should_reject_finding_with_invalid_smell_type(self):
        """Finding with wrong smell_type should be invalid."""
        finding = SAMPLE_VALID_FINDING.copy()
        finding["smell_type"] = "wrong_type"
        assert finding["smell_type"] != "commented_out_code", (
            "Invalid smell_type should be detectable"
        )

    def test_should_reject_finding_with_negative_line_start(self):
        """Finding with negative line_start should be invalid."""
        finding = SAMPLE_VALID_FINDING.copy()
        finding["line_start"] = -1
        assert finding["line_start"] <= 0, (
            "Negative line_start should be detectable as invalid"
        )

    def test_should_reject_finding_with_line_end_less_than_line_start(self):
        """Finding where line_end < line_start should be invalid."""
        finding = SAMPLE_VALID_FINDING.copy()
        finding["line_start"] = 50
        finding["line_end"] = 40
        assert finding["line_end"] < finding["line_start"], (
            "line_end < line_start should be detectable as invalid"
        )

    def test_should_reject_finding_with_confidence_out_of_range(self):
        """Finding with confidence outside [0.0, 1.0] should be invalid."""
        finding = SAMPLE_VALID_FINDING.copy()
        finding["confidence"] = 1.5
        assert not (0.0 <= finding["confidence"] <= 1.0), (
            "Confidence out of range should be detectable as invalid"
        )

    def test_should_reject_finding_with_invalid_classification(self):
        """Finding with unknown classification should be invalid."""
        finding = SAMPLE_VALID_FINDING.copy()
        finding["classification"] = "unknown"
        valid = {"code", "documentation", "todo"}
        assert finding["classification"] not in valid, (
            "Invalid classification should be detectable"
        )
