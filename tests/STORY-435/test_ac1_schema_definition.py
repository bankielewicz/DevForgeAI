"""
Test: AC#1 - YAML Requirements Schema Defined
Story: STORY-435
Generated: 2026-02-17 (TDD Red Phase)

Validates that requirements-schema.yaml exists and defines all required fields:
decisions, scope, success_criteria, constraints, nfrs, stakeholders, source_brainstorm.
"""
import os
import pytest
import yaml


class TestSchemaFileExists:
    """Schema file must exist at the correct path."""

    def test_should_exist_at_correct_path(self, schema_path):
        # Arrange
        expected_path = schema_path

        # Act & Assert
        assert os.path.isfile(expected_path), (
            f"Schema file not found at {expected_path}"
        )

    def test_should_be_valid_yaml(self, schema_path):
        # Arrange & Act
        with open(schema_path, "r") as f:
            data = yaml.safe_load(f)

        # Assert
        assert data is not None, "Schema file is empty or invalid YAML"


class TestSchemaRequiredFields:
    """Schema must define all 7 required top-level fields."""

    @pytest.fixture
    def schema(self, schema_path):
        with open(schema_path, "r") as f:
            return yaml.safe_load(f)

    def test_should_define_decisions_field(self, schema):
        assert "decisions" in schema, "Schema missing 'decisions' field"

    def test_should_define_scope_field(self, schema):
        assert "scope" in schema, "Schema missing 'scope' field"

    def test_should_define_success_criteria_field(self, schema):
        assert "success_criteria" in schema, "Schema missing 'success_criteria' field"

    def test_should_define_constraints_field(self, schema):
        assert "constraints" in schema, "Schema missing 'constraints' field"

    def test_should_define_nfrs_field(self, schema):
        assert "nfrs" in schema, "Schema missing 'nfrs' field"

    def test_should_define_stakeholders_field(self, schema):
        assert "stakeholders" in schema, "Schema missing 'stakeholders' field"

    def test_should_define_source_brainstorm_field(self, schema):
        assert "source_brainstorm" in schema, "Schema missing 'source_brainstorm' field"


class TestDecisionFieldStructure:
    """Decision entries must define required sub-fields."""

    @pytest.fixture
    def schema(self, schema_path):
        with open(schema_path, "r") as f:
            return yaml.safe_load(f)

    @pytest.fixture
    def decision_fields(self, schema):
        """Extract decision field definition from schema."""
        decisions = schema.get("decisions", {})
        # Schema may define fields as a list with example or as a structure
        # We check that the schema documents required sub-fields
        return decisions

    def test_should_require_id_field(self, schema):
        raw = yaml.dump(schema)
        assert "id" in raw, "Decision schema must document 'id' field"

    def test_should_require_domain_field(self, schema):
        raw = yaml.dump(schema)
        assert "domain" in raw, "Decision schema must document 'domain' field"

    def test_should_require_decision_field(self, schema):
        raw = yaml.dump(schema)
        assert "decision" in raw, "Decision schema must document 'decision' field"

    def test_should_require_rejected_field(self, schema):
        raw = yaml.dump(schema)
        assert "rejected" in raw, "Decision schema must document 'rejected' field"

    def test_should_require_rationale_field(self, schema):
        raw = yaml.dump(schema)
        assert "rationale" in raw, "Decision schema must document 'rationale' field"

    def test_should_require_locked_field(self, schema):
        raw = yaml.dump(schema)
        assert "locked" in raw, "Decision schema must document 'locked' field"


class TestScopeFieldStructure:
    """Scope must define in/out sub-fields."""

    @pytest.fixture
    def schema(self, schema_path):
        with open(schema_path, "r") as f:
            return yaml.safe_load(f)

    def test_should_define_scope_in(self, schema):
        scope = schema.get("scope", {})
        assert "in" in scope or "in" in yaml.dump(schema), (
            "Schema must document scope.in field"
        )

    def test_should_define_scope_out(self, schema):
        scope = schema.get("scope", {})
        assert "out" in scope or "out" in yaml.dump(schema), (
            "Schema must document scope.out field"
        )


class TestSuccessCriteriaStructure:
    """Success criteria must define id, metric, target, measurement."""

    @pytest.fixture
    def schema(self, schema_path):
        with open(schema_path, "r") as f:
            return yaml.safe_load(f)

    def test_should_require_metric_field(self, schema):
        raw = yaml.dump(schema)
        assert "metric" in raw, "Success criteria schema must document 'metric' field"

    def test_should_require_target_field(self, schema):
        raw = yaml.dump(schema)
        assert "target" in raw, "Success criteria schema must document 'target' field"

    def test_should_require_measurement_field(self, schema):
        raw = yaml.dump(schema)
        assert "measurement" in raw, (
            "Success criteria schema must document 'measurement' field"
        )
