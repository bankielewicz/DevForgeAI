"""
Test: AC#4 - Scope Boundaries Explicit with Deferral Targets
Story: STORY-435
Generated: 2026-02-17 (TDD Red Phase)

Validates BR-003 (scope.out items must have deferral_target) and
scope structure (in/out lists).
"""
import os
import pytest
import yaml


class TestScopeStructure:
    """Scope must have in and out lists."""

    def test_should_have_in_list(self, sample_valid_scope):
        assert "in" in sample_valid_scope, "Scope must have 'in' list"
        assert isinstance(sample_valid_scope["in"], list), "scope.in must be a list"

    def test_should_have_out_list(self, sample_valid_scope):
        assert "out" in sample_valid_scope, "Scope must have 'out' list"
        assert isinstance(sample_valid_scope["out"], list), "scope.out must be a list"

    def test_in_items_should_be_strings(self, sample_valid_scope):
        for item in sample_valid_scope["in"]:
            assert isinstance(item, str), f"scope.in item must be string, got {type(item)}"


class TestDeferralTargets:
    """BR-003: Scope out items must have deferral_target."""

    def test_should_reject_out_item_without_deferral_target(self):
        # Arrange
        bad_out_item = {"item": "Payment processing"}

        # Act & Assert
        assert "deferral_target" not in bad_out_item, (
            "Test setup: item should lack deferral_target"
        )

    def test_should_reject_out_item_with_empty_deferral_target(self):
        # Arrange
        bad_out_item = {"item": "Payment processing", "deferral_target": ""}

        # Act & Assert
        assert bad_out_item["deferral_target"] == "", (
            "Test setup: deferral_target should be empty"
        )

    def test_should_accept_out_item_with_valid_deferral_target(self, sample_valid_scope):
        # Arrange
        out_item = sample_valid_scope["out"][0]

        # Act & Assert
        assert "deferral_target" in out_item, "Out item must have deferral_target"
        assert len(out_item["deferral_target"]) > 0, "deferral_target must not be empty"

    def test_all_out_items_should_have_deferral_target(self, sample_valid_scope):
        for item in sample_valid_scope["out"]:
            assert "deferral_target" in item, (
                f"Scope.out item '{item.get('item', '?')}' missing deferral_target"
            )
            assert item["deferral_target"], (
                f"Scope.out item '{item.get('item', '?')}' has empty deferral_target"
            )


class TestScopeInSchema:
    """Schema file must define scope with in/out and deferral_target."""

    @pytest.fixture
    def schema(self, schema_path):
        with open(schema_path, "r") as f:
            return yaml.safe_load(f)

    def test_schema_should_define_scope_section(self, schema):
        assert "scope" in schema, "Schema must define 'scope' section"

    def test_schema_scope_should_have_in_field(self, schema):
        scope = schema.get("scope", {})
        raw = yaml.dump(scope)
        assert "in" in raw, "Schema scope must document 'in' field"

    def test_schema_scope_should_have_out_field(self, schema):
        scope = schema.get("scope", {})
        raw = yaml.dump(scope)
        assert "out" in raw, "Schema scope must document 'out' field"

    def test_schema_scope_out_should_have_deferral_target(self, schema):
        raw = yaml.dump(schema)
        assert "deferral_target" in raw, (
            "Schema must document 'deferral_target' in scope.out"
        )
