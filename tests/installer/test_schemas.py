"""
STORY-069: Unit Tests for schemas.py - JSON Schema Validation

Tests validate JSON schema validation for checksums and version files.

Coverage targets:
- validate_json_schema(): 100%
- CHECKSUMS_SCHEMA validation: 100%
- VERSION_SCHEMA validation: 100%
- BUNDLE_MANIFEST_SCHEMA validation: 100%

Expected Result: All tests pass (implementation complete)
"""

import pytest
from installer.schemas import (
    validate_json_schema,
    CHECKSUMS_SCHEMA,
    VERSION_SCHEMA,
    BUNDLE_MANIFEST_SCHEMA,
)


class TestValidateJsonSchema:
    """Unit tests for validate_json_schema() function."""

    def test_valid_object_type(self):
        """
        Should validate correct object type.

        Arrange: Schema requiring object, provide dict
        Act: Validate schema
        Assert: Returns (True, [])
        """
        # Arrange
        schema = {"type": "object"}
        data = {"key": "value"}

        # Act
        is_valid, errors = validate_json_schema(data, schema)

        # Assert
        assert is_valid is True
        assert len(errors) == 0

    def test_invalid_type(self):
        """
        Should reject wrong type.

        Arrange: Schema requiring object, provide string
        Act: Validate schema
        Assert: Returns (False, [error])
        """
        # Arrange
        schema = {"type": "object"}
        data = "not an object"

        # Act
        is_valid, errors = validate_json_schema(data, schema)

        # Assert
        assert is_valid is False
        assert len(errors) == 1
        assert "Expected object" in errors[0]

    def test_required_fields_present(self):
        """
        Should pass when required fields exist.

        Arrange: Schema with required fields, provide complete data
        Act: Validate schema
        Assert: Returns (True, [])
        """
        # Arrange
        schema = {
            "type": "object",
            "required": ["field1", "field2"]
        }
        data = {"field1": "value1", "field2": "value2"}

        # Act
        is_valid, errors = validate_json_schema(data, schema)

        # Assert
        assert is_valid is True

    def test_required_fields_missing(self):
        """
        Should fail when required fields missing.

        Arrange: Schema with required fields, provide incomplete data
        Act: Validate schema
        Assert: Returns (False, [missing field error])
        """
        # Arrange
        schema = {
            "type": "object",
            "required": ["field1", "field2"]
        }
        data = {"field1": "value1"}  # field2 missing

        # Act
        is_valid, errors = validate_json_schema(data, schema)

        # Assert
        assert is_valid is False
        assert any("Missing required field: field2" in err for err in errors)

    def test_pattern_validation_success(self):
        """
        Should pass when string matches pattern.

        Arrange: Schema with pattern, provide matching string
        Act: Validate schema
        Assert: Returns (True, [])
        """
        # Arrange
        schema = {
            "type": "object",
            "properties": {
                "version": {
                    "type": "string",
                    "pattern": r"^\d+\.\d+\.\d+$"
                }
            }
        }
        data = {"version": "1.0.0"}

        # Act
        is_valid, errors = validate_json_schema(data, schema)

        # Assert
        assert is_valid is True

    def test_pattern_validation_failure(self):
        """
        Should fail when string doesn't match pattern.

        Arrange: Schema with pattern, provide non-matching string
        Act: Validate schema
        Assert: Returns (False, [pattern error])
        """
        # Arrange
        schema = {
            "type": "object",
            "properties": {
                "version": {
                    "type": "string",
                    "pattern": r"^\d+\.\d+\.\d+$"
                }
            }
        }
        data = {"version": "invalid"}

        # Act
        is_valid, errors = validate_json_schema(data, schema)

        # Assert
        assert is_valid is False
        assert any("does not match pattern" in err for err in errors)

    def test_integer_minimum_validation(self):
        """
        Should validate integer minimum constraint.

        Arrange: Schema with minimum, provide value below minimum
        Act: Validate schema
        Assert: Returns (False, [minimum error])
        """
        # Arrange
        schema = {
            "type": "object",
            "properties": {
                "count": {
                    "type": "integer",
                    "minimum": 1
                }
            }
        }
        data = {"count": 0}

        # Act
        is_valid, errors = validate_json_schema(data, schema)

        # Assert
        assert is_valid is False
        assert any("below minimum" in err for err in errors)

    def test_integer_maximum_validation(self):
        """
        Should validate integer maximum constraint.

        Arrange: Schema with maximum, provide value above maximum
        Act: Validate schema
        Assert: Returns (False, [maximum error])
        """
        # Arrange
        schema = {
            "type": "object",
            "properties": {
                "count": {
                    "type": "integer",
                    "maximum": 100
                }
            }
        }
        data = {"count": 101}

        # Act
        is_valid, errors = validate_json_schema(data, schema)

        # Assert
        assert is_valid is False
        assert any("above maximum" in err for err in errors)

    def test_pattern_properties_matching(self):
        """
        Should validate pattern properties.

        Arrange: Schema with patternProperties, provide matching keys
        Act: Validate schema
        Assert: Returns (True, [])
        """
        # Arrange
        schema = {
            "type": "object",
            "patternProperties": {
                r"^[a-z]+$": {
                    "type": "string",
                    "pattern": r"^[A-Z]+$"
                }
            }
        }
        data = {"abc": "XYZ", "def": "UVW"}

        # Act
        is_valid, errors = validate_json_schema(data, schema)

        # Assert
        assert is_valid is True

    def test_pattern_properties_value_mismatch(self):
        """
        Should fail when pattern property value invalid.

        Arrange: Schema with patternProperties, provide invalid value
        Act: Validate schema
        Assert: Returns (False, [value error])
        """
        # Arrange
        schema = {
            "type": "object",
            "patternProperties": {
                r"^[a-z]+$": {
                    "type": "string",
                    "pattern": r"^[A-Z]+$"
                }
            }
        }
        data = {"abc": "invalid123"}

        # Act
        is_valid, errors = validate_json_schema(data, schema)

        # Assert
        assert is_valid is False
        assert any("does not match pattern" in err for err in errors)

    def test_additional_properties_forbidden(self):
        """
        Should reject additional properties when forbidden.

        Arrange: Schema with additionalProperties=False, provide extra field
        Act: Validate schema
        Assert: Returns (False, [additional properties error])
        """
        # Arrange
        schema = {
            "type": "object",
            "properties": {
                "allowed": {"type": "string"}
            },
            "additionalProperties": False
        }
        data = {"allowed": "value", "extra": "not allowed"}

        # Act
        is_valid, errors = validate_json_schema(data, schema)

        # Assert
        assert is_valid is False
        assert any("Additional properties not allowed" in err for err in errors)

    def test_min_properties_validation(self):
        """
        Should validate minimum properties count.

        Arrange: Schema with minProperties=2, provide 1 property
        Act: Validate schema
        Assert: Returns (False, [min properties error])
        """
        # Arrange
        schema = {
            "type": "object",
            "minProperties": 2
        }
        data = {"only_one": "value"}

        # Act
        is_valid, errors = validate_json_schema(data, schema)

        # Assert
        assert is_valid is False
        assert any("minimum" in err and "required" in err for err in errors)


class TestChecksumsSchemaValidation:
    """Unit tests for CHECKSUMS_SCHEMA validation."""

    def test_valid_checksums(self):
        """
        Should validate correct checksums format.

        Arrange: Valid checksums dict
        Act: Validate against CHECKSUMS_SCHEMA
        Assert: Returns (True, [])
        """
        # Arrange
        data = {
            "claude/agents/test.md": "a" * 64,
            "devforgeai/context/tech-stack.md": "b" * 64,
        }

        # Act
        is_valid, errors = validate_json_schema(data, CHECKSUMS_SCHEMA)

        # Assert
        assert is_valid is True

    def test_invalid_hash_length(self):
        """
        Should reject checksums with wrong length.

        Arrange: Checksum with 32 chars instead of 64
        Act: Validate against CHECKSUMS_SCHEMA
        Assert: Returns (False, [pattern error])
        """
        # Arrange
        data = {
            "test.md": "a" * 32  # Too short
        }

        # Act
        is_valid, errors = validate_json_schema(data, CHECKSUMS_SCHEMA)

        # Assert
        assert is_valid is False

    def test_invalid_hash_characters(self):
        """
        Should reject checksums with non-hex characters.

        Arrange: Checksum with invalid characters
        Act: Validate against CHECKSUMS_SCHEMA
        Assert: Returns (False, [pattern error])
        """
        # Arrange
        data = {
            "test.md": "g" * 64  # 'g' not in hex
        }

        # Act
        is_valid, errors = validate_json_schema(data, CHECKSUMS_SCHEMA)

        # Assert
        assert is_valid is False

    def test_empty_checksums(self):
        """
        Should reject empty checksums object.

        Arrange: Empty dict
        Act: Validate against CHECKSUMS_SCHEMA
        Assert: Returns (False, [minProperties error])
        """
        # Arrange
        data = {}

        # Act
        is_valid, errors = validate_json_schema(data, CHECKSUMS_SCHEMA)

        # Assert
        assert is_valid is False
        assert any("minimum" in err for err in errors)

    def test_invalid_file_path(self):
        """
        Should reject file paths with invalid characters.

        Arrange: Path with special characters
        Act: Validate against CHECKSUMS_SCHEMA
        Assert: Returns (False, [pattern error])
        """
        # Arrange
        data = {
            "../etc/passwd": "a" * 64  # Path traversal
        }

        # Act
        is_valid, errors = validate_json_schema(data, CHECKSUMS_SCHEMA)

        # Assert
        assert is_valid is False


class TestVersionSchemaValidation:
    """Unit tests for VERSION_SCHEMA validation."""

    def test_valid_version(self):
        """
        Should validate correct version format.

        Arrange: Valid version dict
        Act: Validate against VERSION_SCHEMA
        Assert: Returns (True, [])
        """
        # Arrange
        data = {
            "version": "1.0.0",
            "released_at": "2025-11-17T00:00:00Z",
            "schema_version": "1.0"
        }

        # Act
        is_valid, errors = validate_json_schema(data, VERSION_SCHEMA)

        # Assert
        assert is_valid is True

    def test_missing_required_field(self):
        """
        Should reject version missing required field.

        Arrange: Version without schema_version
        Act: Validate against VERSION_SCHEMA
        Assert: Returns (False, [missing field error])
        """
        # Arrange
        data = {
            "version": "1.0.0",
            "released_at": "2025-11-17T00:00:00Z"
            # schema_version missing
        }

        # Act
        is_valid, errors = validate_json_schema(data, VERSION_SCHEMA)

        # Assert
        assert is_valid is False
        assert any("schema_version" in err for err in errors)

    def test_invalid_version_format(self):
        """
        Should reject invalid semantic version.

        Arrange: Version not in x.y.z format
        Act: Validate against VERSION_SCHEMA
        Assert: Returns (False, [pattern error])
        """
        # Arrange
        data = {
            "version": "1.0",  # Missing patch version
            "released_at": "2025-11-17T00:00:00Z",
            "schema_version": "1.0"
        }

        # Act
        is_valid, errors = validate_json_schema(data, VERSION_SCHEMA)

        # Assert
        assert is_valid is False

    def test_invalid_timestamp_format(self):
        """
        Should reject invalid ISO 8601 timestamp.

        Arrange: Timestamp not in ISO 8601 format
        Act: Validate against VERSION_SCHEMA
        Assert: Returns (False, [pattern error])
        """
        # Arrange
        data = {
            "version": "1.0.0",
            "released_at": "2025-11-17",  # Missing time component
            "schema_version": "1.0"
        }

        # Act
        is_valid, errors = validate_json_schema(data, VERSION_SCHEMA)

        # Assert
        assert is_valid is False

    def test_optional_checksum_field(self):
        """
        Should accept optional checksum field.

        Arrange: Version with optional checksum
        Act: Validate against VERSION_SCHEMA
        Assert: Returns (True, [])
        """
        # Arrange
        data = {
            "version": "1.0.0",
            "released_at": "2025-11-17T00:00:00Z",
            "schema_version": "1.0",
            "checksum": "a" * 64
        }

        # Act
        is_valid, errors = validate_json_schema(data, VERSION_SCHEMA)

        # Assert
        assert is_valid is True

    def test_additional_properties_forbidden(self):
        """
        Should reject extra fields not in schema.

        Arrange: Version with unexpected field
        Act: Validate against VERSION_SCHEMA
        Assert: Returns (False, [additional properties error])
        """
        # Arrange
        data = {
            "version": "1.0.0",
            "released_at": "2025-11-17T00:00:00Z",
            "schema_version": "1.0",
            "extra_field": "not allowed"
        }

        # Act
        is_valid, errors = validate_json_schema(data, VERSION_SCHEMA)

        # Assert
        assert is_valid is False
        assert any("Additional properties" in err for err in errors)


class TestBundleManifestSchemaValidation:
    """Unit tests for BUNDLE_MANIFEST_SCHEMA validation."""

    def test_valid_bundle_manifest(self):
        """
        Should validate complete bundle manifest.

        Arrange: Valid manifest with checksums and metadata
        Act: Validate against BUNDLE_MANIFEST_SCHEMA
        Assert: Returns (True, [])
        """
        # Arrange
        data = {
            "checksums": {
                "test.md": "a" * 64
            },
            "metadata": {
                "bundled_at": "2025-11-17T00:00:00Z",
                "file_count": 1
            }
        }

        # Act
        is_valid, errors = validate_json_schema(data, BUNDLE_MANIFEST_SCHEMA)

        # Assert
        assert is_valid is True

    def test_missing_checksums(self):
        """
        Should reject manifest without checksums.

        Arrange: Manifest missing checksums field
        Act: Validate against BUNDLE_MANIFEST_SCHEMA
        Assert: Returns (False, [missing field error])
        """
        # Arrange
        data = {
            "metadata": {
                "bundled_at": "2025-11-17T00:00:00Z",
                "file_count": 1
            }
        }

        # Act
        is_valid, errors = validate_json_schema(data, BUNDLE_MANIFEST_SCHEMA)

        # Assert
        assert is_valid is False
        assert any("checksums" in err for err in errors)

    def test_missing_metadata(self):
        """
        Should reject manifest without metadata.

        Arrange: Manifest missing metadata field
        Act: Validate against BUNDLE_MANIFEST_SCHEMA
        Assert: Returns (False, [missing field error])
        """
        # Arrange
        data = {
            "checksums": {
                "test.md": "a" * 64
            }
        }

        # Act
        is_valid, errors = validate_json_schema(data, BUNDLE_MANIFEST_SCHEMA)

        # Assert
        assert is_valid is False
        assert any("metadata" in err for err in errors)

    def test_invalid_file_count(self):
        """
        Should reject negative file count.

        Arrange: Metadata with file_count=0
        Act: Validate against BUNDLE_MANIFEST_SCHEMA
        Assert: Returns (False, [minimum error])
        """
        # Arrange
        data = {
            "checksums": {
                "test.md": "a" * 64
            },
            "metadata": {
                "bundled_at": "2025-11-17T00:00:00Z",
                "file_count": 0  # Below minimum
            }
        }

        # Act
        is_valid, errors = validate_json_schema(data, BUNDLE_MANIFEST_SCHEMA)

        # Assert
        assert is_valid is False
        assert any("below minimum" in err for err in errors)
