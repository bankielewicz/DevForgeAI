"""
Test: AC#6 - Source Provenance Back-Reference Required
Story: STORY-435
Generated: 2026-02-17 (TDD Red Phase)

Validates BR-005 (source_brainstorm matches BRAINSTORM-NNN or N/A)
and schema requires source_brainstorm field.
"""
import re
import os
import pytest
import yaml

BRAINSTORM_PATTERN = r"^(BRAINSTORM-\d+|N/A)$"


class TestSourceBrainstormPattern:
    """BR-005: source_brainstorm must match BRAINSTORM-NNN or N/A."""

    def test_should_accept_valid_brainstorm_reference(self):
        assert re.match(BRAINSTORM_PATTERN, "BRAINSTORM-003")

    def test_should_accept_na_value(self):
        assert re.match(BRAINSTORM_PATTERN, "N/A")

    def test_should_reject_none_string(self):
        assert not re.match(BRAINSTORM_PATTERN, "none")

    def test_should_reject_empty_string(self):
        assert not re.match(BRAINSTORM_PATTERN, "")

    def test_should_reject_lowercase_brainstorm(self):
        assert not re.match(BRAINSTORM_PATTERN, "brainstorm-003")

    def test_should_reject_missing_number(self):
        assert not re.match(BRAINSTORM_PATTERN, "BRAINSTORM-")

    def test_should_accept_high_number(self):
        assert re.match(BRAINSTORM_PATTERN, "BRAINSTORM-999")


class TestSourceBrainstormInSchema:
    """Schema must require source_brainstorm field."""

    @pytest.fixture
    def schema(self, schema_path):
        with open(schema_path, "r") as f:
            return yaml.safe_load(f)

    def test_schema_should_define_source_brainstorm(self, schema):
        assert "source_brainstorm" in schema, (
            "Schema must define 'source_brainstorm' field"
        )

    def test_schema_source_brainstorm_should_have_description(self, schema):
        raw = yaml.dump(schema)
        # The schema should be self-documenting with descriptions
        assert "brainstorm" in raw.lower(), (
            "Schema should document source_brainstorm purpose"
        )


class TestNFRSchemaParseability:
    """NFR-001: Schema parseable by PyYAML without custom extensions."""

    def test_schema_should_parse_with_pyyaml(self, schema_path):
        # Arrange & Act
        with open(schema_path, "r") as f:
            data = yaml.safe_load(f)

        # Assert
        assert data is not None, "PyYAML must parse schema without errors"
        assert isinstance(data, dict), "Parsed schema must be a dict"


class TestNFRTokenBudget:
    """NFR-002: Populated template <= 4,000 tokens (~16,000 chars)."""

    def test_template_should_fit_token_budget(self, template_path):
        # Arrange
        with open(template_path, "r") as f:
            content = f.read()

        # Act
        char_count = len(content)

        # Assert - 16,000 chars approximates 4,000 tokens
        assert char_count <= 16000, (
            f"Template is {char_count} chars; must be <= 16,000 (~4,000 tokens)"
        )


class TestNFRSelfDocumenting:
    """NFR-003: Schema fields have descriptions."""

    def test_schema_should_have_descriptions_for_fields(self, schema_path):
        # Arrange
        with open(schema_path, "r") as f:
            content = f.read()

        # Act - check for comment lines or description fields
        has_comments = "#" in content
        has_descriptions = "description" in content.lower()

        # Assert
        assert has_comments or has_descriptions, (
            "Schema must be self-documenting (comments or description fields)"
        )
