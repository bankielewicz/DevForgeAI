"""
JSON schema definitions for validation.

This module provides JSON schemas for:
- checksums.json (bundle integrity manifest)
- version.json (installation metadata)

Following OWASP A08:2021: Validate all JSON before deserialization
to prevent injection attacks and data corruption.
"""

# Schema for checksums.json
CHECKSUMS_SCHEMA = {
    "type": "object",
    "patternProperties": {
        # Keys: Relative file paths (alphanumeric, forward slashes, hyphens, underscores, dots)
        # SECURITY: Prevents ".." path traversal by rejecting at start and after "/"
        r"^(?!\.\.)(?:(?!\.\./)[\w./-])+$": {
            "type": "string",
            "pattern": r"^[a-fA-F0-9]{64}$",  # SHA256 hex string (64 chars)
            "description": "SHA256 checksum as hex string"
        }
    },
    "additionalProperties": False,
    "minProperties": 1,  # At least one file checksum required
    "description": "Mapping of relative file paths to SHA256 checksums"
}

# Schema for version.json
VERSION_SCHEMA = {
    "type": "object",
    "required": ["version", "released_at", "schema_version"],
    "properties": {
        "version": {
            "type": "string",
            "pattern": r"^\d+\.\d+\.\d+$",  # Semantic versioning (e.g., "1.0.0")
            "description": "Framework version in semver format"
        },
        "released_at": {
            "type": "string",
            "pattern": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$",  # ISO 8601 UTC timestamp
            "description": "Release timestamp in ISO 8601 format"
        },
        "schema_version": {
            "type": "string",
            "pattern": r"^\d+\.\d+$",  # Schema version (e.g., "1.0")
            "description": "Schema version for compatibility checking"
        },
        "checksum": {
            "type": "string",
            "pattern": r"^[a-fA-F0-9]{64}$",  # Optional SHA256 checksum
            "description": "Optional SHA256 checksum of version.json content"
        }
    },
    "additionalProperties": False,
    "description": "Version metadata for framework installation"
}

# Schema for bundle manifest (checksums.json + metadata)
BUNDLE_MANIFEST_SCHEMA = {
    "type": "object",
    "required": ["checksums", "metadata"],
    "properties": {
        "checksums": CHECKSUMS_SCHEMA,
        "metadata": {
            "type": "object",
            "required": ["bundled_at", "file_count"],
            "properties": {
                "bundled_at": {
                    "type": "string",
                    "pattern": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$",
                    "description": "Bundle creation timestamp"
                },
                "file_count": {
                    "type": "integer",
                    "minimum": 1,
                    "description": "Total number of files in bundle"
                },
                "bundle_version": {
                    "type": "string",
                    "pattern": r"^\d+\.\d+\.\d+$",
                    "description": "Bundle format version"
                }
            },
            "additionalProperties": False
        }
    },
    "additionalProperties": False,
    "description": "Complete bundle manifest with checksums and metadata"
}


def validate_json_schema(data: dict, schema: dict) -> tuple[bool, list[str]]:
    """
    Validate JSON data against schema.

    Uses Python's standard library for validation (no external dependencies).
    Basic type checking and pattern matching.

    Args:
        data: Parsed JSON data (dict)
        schema: JSON schema definition

    Returns:
        tuple: (is_valid: bool, errors: list[str])

    Examples:
        >>> data = {"version": "1.0.0", "released_at": "2025-11-17T00:00:00Z", "schema_version": "1.0"}
        >>> is_valid, errors = validate_json_schema(data, VERSION_SCHEMA)
        >>> if not is_valid:
        ...     print("Validation errors:", errors)
    """
    import re

    errors = []

    # Check type
    if "type" in schema:
        expected_type = schema["type"]
        if expected_type == "object" and not isinstance(data, dict):
            errors.append(f"Expected object, got {type(data).__name__}")
            return False, errors
        elif expected_type == "string" and not isinstance(data, str):
            errors.append(f"Expected string, got {type(data).__name__}")
            return False, errors
        elif expected_type == "integer" and not isinstance(data, int):
            errors.append(f"Expected integer, got {type(data).__name__}")
            return False, errors

    # Check required properties
    if "required" in schema and isinstance(data, dict):
        for required_field in schema["required"]:
            if required_field not in data:
                errors.append(f"Missing required field: {required_field}")

    # Validate properties
    if "properties" in schema and isinstance(data, dict):
        for field_name, field_schema in schema["properties"].items():
            if field_name in data:
                field_value = data[field_name]
                is_valid, field_errors = validate_json_schema(field_value, field_schema)
                if not is_valid:
                    errors.extend([f"{field_name}: {err}" for err in field_errors])

                # Check pattern for strings
                if "pattern" in field_schema and isinstance(field_value, str):
                    pattern = field_schema["pattern"]
                    if not re.match(pattern, field_value):
                        errors.append(
                            f"{field_name}: Value '{field_value}' does not match pattern {pattern}"
                        )

                # Check min/max for integers
                if isinstance(field_value, int):
                    if "minimum" in field_schema and field_value < field_schema["minimum"]:
                        errors.append(
                            f"{field_name}: Value {field_value} below minimum {field_schema['minimum']}"
                        )
                    if "maximum" in field_schema and field_value > field_schema["maximum"]:
                        errors.append(
                            f"{field_name}: Value {field_value} above maximum {field_schema['maximum']}"
                        )

    # Check pattern properties (for checksums)
    if "patternProperties" in schema and isinstance(data, dict):
        for key, value in data.items():
            matched = False
            for pattern, value_schema in schema["patternProperties"].items():
                if re.match(pattern, key):
                    matched = True
                    is_valid, value_errors = validate_json_schema(value, value_schema)
                    if not is_valid:
                        errors.extend([f"{key}: {err}" for err in value_errors])

                    # Check pattern for values
                    if "pattern" in value_schema and isinstance(value, str):
                        value_pattern = value_schema["pattern"]
                        if not re.match(value_pattern, value):
                            errors.append(
                                f"{key}: Checksum '{value}' does not match pattern {value_pattern}"
                            )
                    break

            if not matched and schema.get("additionalProperties") is False:
                errors.append(f"Property '{key}' does not match any pattern")

    # Check min properties
    if "minProperties" in schema and isinstance(data, dict):
        if len(data) < schema["minProperties"]:
            errors.append(
                f"Object has {len(data)} properties, minimum {schema['minProperties']} required"
            )

    # Check additional properties
    if schema.get("additionalProperties") is False and isinstance(data, dict):
        if "properties" in schema:
            allowed_keys = set(schema["properties"].keys())
            extra_keys = set(data.keys()) - allowed_keys
            if extra_keys:
                errors.append(f"Additional properties not allowed: {', '.join(extra_keys)}")

    return len(errors) == 0, errors
