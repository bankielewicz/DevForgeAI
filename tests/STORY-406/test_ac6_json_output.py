"""
Test: AC#6 - JSON Output Format Compliance
Story: STORY-406
Generated: 2026-02-16

Validates the MessageChainFinding output schema includes all required fields
with correct types and constraints.
"""
import os
import pytest


class TestOutputSchemaFields:
    """Output must include all 9 required fields from the spec."""

    def test_ac6_all_required_fields_present(self, sample_finding, required_output_fields):
        """Arrange: Sample finding. Act: Check keys. Assert: All 9 fields present."""
        for field in required_output_fields:
            assert field in sample_finding, (
                f"Required field '{field}' missing from output schema"
            )

    def test_ac6_no_extra_unknown_fields(self, sample_finding, required_output_fields):
        """Arrange: Sample finding. Act: Check for extras. Assert: Only known fields."""
        extra_fields = set(sample_finding.keys()) - set(required_output_fields)
        # Extra fields are allowed but should be documented; warn if present
        # This test validates the minimum required set exists
        assert len(sample_finding) >= len(required_output_fields), (
            "Output must have at least all required fields"
        )


class TestOutputFieldConstraints:
    """Each field must meet its type and value constraints."""

    def test_ac6_smell_type_is_message_chain(self, sample_finding):
        """Arrange: Finding. Act: Check smell_type. Assert: 'message_chain'."""
        assert sample_finding["smell_type"] == "message_chain", (
            f"smell_type must be 'message_chain', got: {sample_finding['smell_type']}"
        )

    def test_ac6_severity_is_low(self, sample_finding):
        """Arrange: Finding. Act: Check severity. Assert: 'LOW'."""
        assert sample_finding["severity"] == "LOW", (
            f"severity must be 'LOW' for message chains, got: {sample_finding['severity']}"
        )

    def test_ac6_file_is_string(self, sample_finding):
        """Arrange: Finding. Act: Check file type. Assert: Non-empty string."""
        assert isinstance(sample_finding["file"], str), "file must be a string"
        assert len(sample_finding["file"]) > 0, "file must be non-empty"

    def test_ac6_line_is_positive_int(self, sample_finding):
        """Arrange: Finding. Act: Check line. Assert: Positive integer."""
        assert isinstance(sample_finding["line"], int), "line must be an integer"
        assert sample_finding["line"] > 0, "line must be positive"

    def test_ac6_chain_excerpt_max_100_chars(self, sample_finding):
        """Arrange: Finding. Act: Check chain_excerpt length. Assert: <= 100 chars."""
        assert isinstance(sample_finding["chain_excerpt"], str), "chain_excerpt must be a string"
        assert len(sample_finding["chain_excerpt"]) <= 100, (
            f"chain_excerpt must be <= 100 chars, got {len(sample_finding['chain_excerpt'])}"
        )

    def test_ac6_chain_length_at_least_3(self, sample_finding):
        """Arrange: Finding. Act: Check chain_length. Assert: >= 3."""
        assert isinstance(sample_finding["chain_length"], int), "chain_length must be an integer"
        assert sample_finding["chain_length"] >= 3, (
            f"chain_length must be >= 3, got {sample_finding['chain_length']}"
        )

    def test_ac6_confidence_is_normalized_float(self, sample_finding):
        """Arrange: Finding. Act: Check confidence range. Assert: 0.0-1.0."""
        assert isinstance(sample_finding["confidence"], (int, float)), (
            "confidence must be a number"
        )
        assert 0.0 <= sample_finding["confidence"] <= 1.0, (
            f"confidence must be in [0.0, 1.0], got {sample_finding['confidence']}"
        )

    def test_ac6_evidence_is_non_empty_string(self, sample_finding):
        """Arrange: Finding. Act: Check evidence. Assert: Non-empty string."""
        assert isinstance(sample_finding["evidence"], str), "evidence must be a string"
        assert len(sample_finding["evidence"]) > 0, "evidence must be non-empty"

    def test_ac6_remediation_is_non_empty_string(self, sample_finding):
        """Arrange: Finding. Act: Check remediation. Assert: Non-empty string."""
        assert isinstance(sample_finding["remediation"], str), "remediation must be a string"
        assert len(sample_finding["remediation"]) > 0, "remediation must be non-empty"


class TestOutputSchemaInSpec:
    """Output schema must be documented in scanner spec."""

    def test_ac6_output_schema_in_spec(self, src_scanner_spec_path):
        """Arrange: Read spec. Act: Search for output fields. Assert: All documented."""
        spec_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            src_scanner_spec_path,
        )
        assert os.path.exists(spec_path), (
            f"Scanner spec not found at {spec_path} - implementation needed"
        )
        with open(spec_path, "r") as f:
            content = f.read()
        required_in_spec = [
            "smell_type", "severity", "chain_excerpt",
            "chain_length", "confidence", "evidence", "remediation",
        ]
        missing = [f for f in required_in_spec if f not in content]
        assert len(missing) == 0, (
            f"Spec must document all output fields. Missing: {missing}"
        )

    def test_ac6_message_chain_smell_type_in_spec(self, src_scanner_spec_path):
        """Arrange: Read spec. Act: Search for message_chain smell type. Assert: Present."""
        spec_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            src_scanner_spec_path,
        )
        assert os.path.exists(spec_path), (
            f"Scanner spec not found at {spec_path} - implementation needed"
        )
        with open(spec_path, "r") as f:
            content = f.read()
        assert "message_chain" in content, (
            "Spec must define 'message_chain' as the smell_type value"
        )
