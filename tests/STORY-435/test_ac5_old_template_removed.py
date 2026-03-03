"""
Test: AC#5 - Old Template Removed
Story: STORY-435
Generated: 2026-02-17 (TDD Red Phase)

Validates that old requirements-spec-template.md is removed and
new requirements-template.md exists.
"""
import os
import pytest


class TestOldTemplateRemoved:
    """Old requirements-spec-template.md must not exist."""

    def test_old_template_should_not_exist(self, old_template_path):
        # Arrange
        path = old_template_path

        # Act & Assert
        assert not os.path.isfile(path), (
            f"Old template should be removed: {path}"
        )


class TestNewTemplateExists:
    """New requirements-template.md must exist."""

    def test_new_template_should_exist(self, template_path):
        # Arrange
        path = template_path

        # Act & Assert
        assert os.path.isfile(path), (
            f"New template must exist: {path}"
        )


class TestTemplateDirectoryContents:
    """Templates directory should contain new files, not old."""

    def test_directory_should_contain_schema(self, templates_dir):
        schema = os.path.join(templates_dir, "requirements-schema.yaml")
        assert os.path.isfile(schema), (
            f"Schema file must exist in templates dir: {schema}"
        )

    def test_directory_should_contain_new_template(self, templates_dir):
        template = os.path.join(templates_dir, "requirements-template.md")
        assert os.path.isfile(template), (
            f"New template must exist in templates dir: {template}"
        )

    def test_directory_should_not_contain_old_template(self, templates_dir):
        old = os.path.join(templates_dir, "requirements-spec-template.md")
        assert not os.path.isfile(old), (
            f"Old template must be removed from templates dir: {old}"
        )
