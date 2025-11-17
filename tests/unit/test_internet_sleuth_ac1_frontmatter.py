"""
Unit tests for STORY-035 AC1: Frontmatter compliance with DevForgeAI subagent standard

Tests verify the internet-sleuth agent frontmatter follows DevForgeAI conventions:
- Required fields: name, description, tools, model
- Optional field: color
- Deprecated fields forbidden: command_prefix, output_format
"""

import pytest
import yaml
import re
from pathlib import Path


@pytest.mark.story_035
@pytest.mark.acceptance_criteria
@pytest.mark.unit
class TestAC1FrontmatterCompliance:
    """Test suite for AC1: Frontmatter compliance"""

    @pytest.fixture
    def agent_file_path(self):
        """Path to internet-sleuth agent file"""
        return Path(".claude/agents/internet-sleuth.md")

    @pytest.fixture
    def agent_content(self, agent_file_path):
        """Load agent file content"""
        assert agent_file_path.exists(), f"Agent file not found: {agent_file_path}"
        return agent_file_path.read_text()

    @pytest.fixture
    def frontmatter_yaml(self, agent_content):
        """Extract and parse YAML frontmatter"""
        # Extract YAML between --- delimiters
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', agent_content, re.DOTALL)
        assert match, "No YAML frontmatter found in agent file"

        yaml_content = match.group(1)
        parsed = yaml.safe_load(yaml_content)
        assert parsed is not None, "Failed to parse YAML frontmatter"
        return parsed

    def test_frontmatter_has_required_field_name(self, frontmatter_yaml):
        """
        AC1: Frontmatter must contain 'name' field

        Arrange: Load frontmatter YAML
        Act: Check for 'name' field
        Assert: Field exists and is non-empty
        """
        # Act
        has_name = 'name' in frontmatter_yaml

        # Assert
        assert has_name, "Missing required field 'name' in frontmatter"
        assert frontmatter_yaml['name'], "Field 'name' is empty"
        assert isinstance(frontmatter_yaml['name'], str), "Field 'name' must be string"

    def test_frontmatter_name_uses_kebab_case(self, frontmatter_yaml):
        """
        AC1: Name field must use kebab-case format

        Arrange: Load frontmatter YAML
        Act: Validate name format
        Assert: Name matches kebab-case pattern (lowercase, hyphens only)
        """
        # Act
        name = frontmatter_yaml.get('name', '')
        is_kebab_case = bool(re.match(r'^[a-z][a-z0-9-]*$', name))

        # Assert
        assert is_kebab_case, f"Field 'name' must be kebab-case, got: {name}"

    def test_frontmatter_has_required_field_description(self, frontmatter_yaml):
        """
        AC1: Frontmatter must contain 'description' field

        Arrange: Load frontmatter YAML
        Act: Check for 'description' field
        Assert: Field exists and is non-empty
        """
        # Act
        has_description = 'description' in frontmatter_yaml

        # Assert
        assert has_description, "Missing required field 'description' in frontmatter"
        assert frontmatter_yaml['description'], "Field 'description' is empty"
        assert isinstance(frontmatter_yaml['description'], str), "Field 'description' must be string"

    def test_frontmatter_description_includes_proactive_triggers(self, frontmatter_yaml):
        """
        COMP-002: Description must include proactive trigger scenarios

        Arrange: Load frontmatter YAML
        Act: Check description for 'ideation' and 'architecture' keywords
        Assert: Both keywords present
        """
        # Act
        description = frontmatter_yaml.get('description', '').lower()
        has_ideation = 'ideation' in description
        has_architecture = 'architecture' in description

        # Assert
        assert has_ideation, "Field 'description' must include 'ideation' trigger scenario"
        assert has_architecture, "Field 'description' must include 'architecture' trigger scenario"

    def test_frontmatter_has_required_field_tools(self, frontmatter_yaml):
        """
        AC1: Frontmatter must contain 'tools' field

        Arrange: Load frontmatter YAML
        Act: Check for 'tools' field
        Assert: Field exists and is non-empty string
        """
        # Act
        has_tools = 'tools' in frontmatter_yaml

        # Assert
        assert has_tools, "Missing required field 'tools' in frontmatter"
        assert frontmatter_yaml['tools'], "Field 'tools' is empty"
        assert isinstance(frontmatter_yaml['tools'], str), "Field 'tools' must be string (comma-separated)"

    def test_frontmatter_tools_comma_separated(self, frontmatter_yaml):
        """
        AC1: Tools field must be comma-separated list

        Arrange: Load frontmatter YAML
        Act: Parse tools field
        Assert: Contains valid tool names separated by commas
        """
        # Act
        tools_str = frontmatter_yaml.get('tools', '')
        tools_list = [t.strip() for t in tools_str.split(',')]

        # Assert
        assert len(tools_list) > 0, "Field 'tools' must contain at least one tool"

        valid_tools = {'Read', 'Write', 'Edit', 'Bash', 'Glob', 'Grep', 'WebSearch', 'WebFetch'}
        for tool in tools_list:
            assert tool in valid_tools, f"Unknown tool '{tool}' in frontmatter (valid: {valid_tools})"

    def test_frontmatter_has_required_field_model(self, frontmatter_yaml):
        """
        AC1: Frontmatter must contain 'model' field

        Arrange: Load frontmatter YAML
        Act: Check for 'model' field
        Assert: Field exists and is valid value
        """
        # Act
        has_model = 'model' in frontmatter_yaml

        # Assert
        assert has_model, "Missing required field 'model' in frontmatter"
        assert frontmatter_yaml['model'], "Field 'model' is empty"

        valid_models = {'haiku', 'sonnet', 'inherit'}
        model_value = frontmatter_yaml['model']
        assert model_value in valid_models, f"Field 'model' must be one of {valid_models}, got: {model_value}"

    def test_frontmatter_optional_field_color(self, frontmatter_yaml):
        """
        AC1: Color field is optional but if present must be valid

        Arrange: Load frontmatter YAML
        Act: Check for 'color' field
        Assert: If present, is non-empty string
        """
        # Act
        has_color = 'color' in frontmatter_yaml

        # Assert (optional field)
        if has_color:
            assert frontmatter_yaml['color'], "Field 'color' if present must be non-empty"
            assert isinstance(frontmatter_yaml['color'], str), "Field 'color' must be string"

    def test_frontmatter_forbids_deprecated_command_prefix(self, frontmatter_yaml):
        """
        AC1: Frontmatter must NOT contain deprecated 'command_prefix' field

        Arrange: Load frontmatter YAML
        Act: Check for 'command_prefix' field
        Assert: Field does not exist
        """
        # Act
        has_command_prefix = 'command_prefix' in frontmatter_yaml

        # Assert
        assert not has_command_prefix, "Deprecated field 'command_prefix' found in frontmatter (incompatible with DevForgeAI)"

    def test_frontmatter_forbids_deprecated_output_format(self, frontmatter_yaml):
        """
        AC1: Frontmatter must NOT contain deprecated 'output_format' field

        Arrange: Load frontmatter YAML
        Act: Check for 'output_format' field
        Assert: Field does not exist
        """
        # Act
        has_output_format = 'output_format' in frontmatter_yaml

        # Assert
        assert not has_output_format, "Deprecated field 'output_format' found in frontmatter (framework handles this)"

    def test_frontmatter_yaml_valid_syntax(self, agent_content):
        """
        AC1: Frontmatter must be valid YAML syntax

        Arrange: Load agent file content
        Act: Attempt to parse YAML frontmatter
        Assert: No YAML parsing errors
        """
        # Act
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', agent_content, re.DOTALL)
        assert match, "No YAML frontmatter found"

        yaml_content = match.group(1)

        # Assert
        try:
            parsed = yaml.safe_load(yaml_content)
            assert parsed is not None, "YAML parsed as None (empty frontmatter)"
        except yaml.YAMLError as e:
            pytest.fail(f"YAML frontmatter syntax error: {e}")

    def test_frontmatter_completeness_all_required_fields(self, frontmatter_yaml):
        """
        AC1: Verify ALL required fields present in single test

        Arrange: Load frontmatter YAML
        Act: Check for all required fields
        Assert: All 4 required fields present
        """
        # Act
        required_fields = {'name', 'description', 'tools', 'model'}
        present_fields = set(frontmatter_yaml.keys())
        missing_fields = required_fields - present_fields

        # Assert
        assert len(missing_fields) == 0, f"Missing required frontmatter fields: {missing_fields}"

    @pytest.mark.edge_case
    def test_frontmatter_no_extra_unexpected_fields(self, frontmatter_yaml):
        """
        Edge case: Frontmatter should only contain known fields

        Arrange: Load frontmatter YAML
        Act: Check for unexpected fields
        Assert: Warn if unexpected fields found
        """
        # Act
        known_fields = {'name', 'description', 'tools', 'model', 'color', 'icon'}
        present_fields = set(frontmatter_yaml.keys())
        unexpected_fields = present_fields - known_fields

        # Assert (soft warning, not failure)
        if unexpected_fields:
            pytest.skip(f"Found unexpected frontmatter fields: {unexpected_fields} (review if intentional)")
