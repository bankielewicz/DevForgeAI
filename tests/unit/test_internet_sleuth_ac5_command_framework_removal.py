"""
Unit tests for STORY-035 AC5: Command Execution Framework pattern removed

Tests verify all custom command syntax removed and replaced with DevForgeAI patterns:
- No "Command Execution Framework" section
- No custom command syntax (*research, *competitive-analysis, etc.)
- No command parsing logic
- Replaced with narrative "Research Capabilities" or "Workflow" section
"""

import pytest
import re
from pathlib import Path


@pytest.mark.story_035
@pytest.mark.acceptance_criteria
@pytest.mark.unit
class TestAC5CommandFrameworkRemoval:
    """Test suite for AC5: Command Execution Framework pattern removed"""

    @pytest.fixture
    def agent_file_path(self):
        """Path to internet-sleuth agent file"""
        return Path(".claude/agents/internet-sleuth.md")

    @pytest.fixture
    def agent_content(self, agent_file_path):
        """Load agent file content"""
        assert agent_file_path.exists(), f"Agent file not found: {agent_file_path}"
        return agent_file_path.read_text()

    def test_no_command_execution_framework_heading(self, agent_content):
        """
        AC5 / COMP-009: No 'Command Execution Framework' section

        Arrange: Load agent file content
        Act: Search for "Command Execution Framework" heading
        Assert: Zero matches found
        """
        # Act
        has_command_framework = bool(re.search(r'## Command Execution Framework', agent_content, re.IGNORECASE))

        # Assert
        assert not has_command_framework, \
            "COMP-009 FAILED: Found 'Command Execution Framework' section (must be removed)"

    def test_no_step_1_load_decision_history(self, agent_content):
        """
        COMP-009: No 'Step 1: Load Decision History' pattern

        Arrange: Load agent file content
        Act: Search for legacy workflow step
        Assert: Zero matches found
        """
        # Act
        has_step_1 = bool(re.search(r'Step 1: Load Decision History', agent_content, re.IGNORECASE))

        # Assert
        assert not has_step_1, \
            "COMP-009 FAILED: Found legacy 'Step 1: Load Decision History' (must be removed)"

    def test_no_step_2_load_dependencies(self, agent_content):
        """
        COMP-009: No 'Step 2: Load Dependencies' pattern

        Arrange: Load agent file content
        Act: Search for legacy workflow step
        Assert: Zero matches found
        """
        # Act
        has_step_2 = bool(re.search(r'Step 2: Load Dependencies', agent_content, re.IGNORECASE))

        # Assert
        assert not has_step_2, \
            "COMP-009 FAILED: Found legacy 'Step 2: Load Dependencies' (must be removed)"

    def test_no_available_commands_section(self, agent_content):
        """
        COMP-010: No 'Available Commands' section

        Arrange: Load agent file content
        Act: Search for "Available Commands" heading
        Assert: Zero matches found
        """
        # Act
        has_available_commands = bool(re.search(r'## Available Commands', agent_content, re.IGNORECASE))

        # Assert
        assert not has_available_commands, \
            "COMP-010 FAILED: Found 'Available Commands' section (must be removed)"

    def test_no_research_command_syntax(self, agent_content):
        """
        COMP-010: No *research command syntax

        Arrange: Load agent file content
        Act: Search for *research command pattern
        Assert: Zero matches found
        """
        # Act
        has_research_cmd = bool(re.search(r'\*research\s+\{', agent_content))

        # Assert
        assert not has_research_cmd, \
            "COMP-010 FAILED: Found '*research' command syntax (must be removed)"

    def test_no_competitive_analysis_command_syntax(self, agent_content):
        """
        COMP-010: No *competitive-analysis command syntax

        Arrange: Load agent file content
        Act: Search for *competitive-analysis command pattern
        Assert: Zero matches found
        """
        # Act
        has_competitive_cmd = bool(re.search(r'\*competitive-analysis\s+\{', agent_content))

        # Assert
        assert not has_competitive_cmd, \
            "COMP-010 FAILED: Found '*competitive-analysis' command syntax (must be removed)"

    def test_no_technology_monitoring_command_syntax(self, agent_content):
        """
        COMP-010: No *technology-monitoring command syntax

        Arrange: Load agent file content
        Act: Search for *technology-monitoring command pattern
        Assert: Zero matches found
        """
        # Act
        has_tech_monitoring_cmd = bool(re.search(r'\*technology-monitoring\s+\{', agent_content))

        # Assert
        assert not has_tech_monitoring_cmd, \
            "COMP-010 FAILED: Found '*technology-monitoring' command syntax (must be removed)"

    def test_no_repository_archaeology_command_syntax(self, agent_content):
        """
        COMP-010: No *repository-archaeology command syntax

        Arrange: Load agent file content
        Act: Search for *repository-archaeology command pattern
        Assert: Zero matches found
        """
        # Act
        has_repo_arch_cmd = bool(re.search(r'\*repository-archaeology\s+\{', agent_content))

        # Assert
        assert not has_repo_arch_cmd, \
            "COMP-010 FAILED: Found '*repository-archaeology' command syntax (must be removed)"

    def test_no_market_intelligence_command_syntax(self, agent_content):
        """
        COMP-010: No *market-intelligence command syntax

        Arrange: Load agent file content
        Act: Search for *market-intelligence command pattern
        Assert: Zero matches found
        """
        # Act
        has_market_intel_cmd = bool(re.search(r'\*market-intelligence\s+\{', agent_content))

        # Assert
        assert not has_market_intel_cmd, \
            "COMP-010 FAILED: Found '*market-intelligence' command syntax (must be removed)"

    def test_no_validate_research_command_syntax(self, agent_content):
        """
        COMP-010: No *validate-research command syntax

        Arrange: Load agent file content
        Act: Search for *validate-research command pattern
        Assert: Zero matches found
        """
        # Act
        has_validate_cmd = bool(re.search(r'\*validate-research', agent_content))

        # Assert
        assert not has_validate_cmd, \
            "COMP-010 FAILED: Found '*validate-research' command syntax (must be removed)"

    def test_comp_009_010_all_command_patterns_removed(self, agent_content):
        """
        COMP-009/010: Comprehensive test - all command framework patterns removed

        Arrange: Load agent file content
        Act: Search for all legacy command patterns
        Assert: Zero matches for any pattern
        """
        # Act
        legacy_patterns = [
            r'## Command Execution Framework',
            r'Step 1: Load Decision History',
            r'Step 2: Load Dependencies',
            r'## Available Commands',
            r'\*research\s+\{',
            r'\*competitive-analysis',
            r'\*technology-monitoring',
            r'\*repository-archaeology',
            r'\*market-intelligence',
            r'\*validate-research'
        ]

        found_patterns = []
        for pattern in legacy_patterns:
            if re.search(pattern, agent_content, re.IGNORECASE):
                found_patterns.append(pattern)

        # Assert
        assert len(found_patterns) == 0, \
            f"COMP-009/010 FAILED: Found {len(found_patterns)} legacy command patterns: {found_patterns}"

    def test_has_research_capabilities_or_workflow_section(self, agent_content):
        """
        COMP-011: Must have narrative 'Research Capabilities' or 'Workflow' section

        Arrange: Load agent file content
        Act: Search for replacement section headings
        Assert: At least one narrative section exists
        """
        # Act
        has_research_capabilities = bool(re.search(r'## Research Capabilities', agent_content, re.IGNORECASE))
        has_workflow = bool(re.search(r'## Workflow', agent_content, re.IGNORECASE))
        has_methodology = bool(re.search(r'## Research Methodology', agent_content, re.IGNORECASE))

        # Assert
        assert has_research_capabilities or has_workflow or has_methodology, \
            "COMP-011 FAILED: Must have narrative section (## Research Capabilities, ## Workflow, or ## Research Methodology)"

    def test_narrative_section_uses_prose_not_commands(self, agent_content):
        """
        COMP-011: Narrative section must use prose workflow, not command syntax

        Arrange: Load agent file content
        Act: Extract Research Capabilities/Workflow section, check for prose vs commands
        Assert: No command syntax patterns in narrative section
        """
        # Act
        # Find Research Capabilities or Workflow section
        section_match = re.search(
            r'## (?:Research Capabilities|Workflow|Research Methodology)\s*\n(.*?)(?=\n##|\Z)',
            agent_content,
            re.DOTALL | re.IGNORECASE
        )

        if not section_match:
            pytest.skip("No narrative section found (separate test will catch this)")

        section_content = section_match.group(1)

        # Check for command syntax in narrative section
        command_patterns = [
            r'\*[a-z]+-[a-z]+',  # *command-name pattern
            r'Execute:.*\*',      # Execute: *command pattern
            r'Command:.*\*'       # Command: *command pattern
        ]

        found_commands = []
        for pattern in command_patterns:
            if re.search(pattern, section_content):
                found_commands.append(pattern)

        # Assert
        assert len(found_commands) == 0, \
            f"Narrative section contains command syntax (must use prose): {found_commands}"

    @pytest.mark.edge_case
    def test_no_command_parsing_logic_in_agent(self, agent_content):
        """
        Edge case: Ensure no command parsing logic remains

        Arrange: Load agent file content
        Act: Search for command parsing patterns
        Assert: No parsing logic found
        """
        # Act
        parsing_patterns = [
            r'parse.*command',
            r'extract.*\*',
            r'match.*command',
            r'if.*\*[a-z]+'
        ]

        found_parsing = []
        for pattern in parsing_patterns:
            if re.search(pattern, agent_content, re.IGNORECASE):
                found_parsing.append(pattern)

        # Assert
        assert len(found_parsing) == 0, \
            f"Found command parsing logic (must be removed): {found_parsing}"

    @pytest.mark.edge_case
    def test_no_dependencies_field_in_command_documentation(self, agent_content):
        """
        Edge case: Old command syntax included Dependencies field

        Arrange: Load agent file content
        Act: Search for "Dependencies: .claude/tasks/" pattern
        Assert: No old dependency patterns found
        """
        # Act
        has_old_dependencies = bool(re.search(r'Dependencies:\s+\.claude/tasks/', agent_content))

        # Assert
        assert not has_old_dependencies, \
            "Found old command Dependencies pattern (must be removed)"

    def test_simplified_capabilities_focus_on_research_tasks(self, agent_content):
        """
        AC5: Capabilities section should focus on research tasks (not command execution)

        Arrange: Load agent file content
        Act: Extract capabilities section, verify focus on tasks
        Assert: Section describes research capabilities, not command execution
        """
        # Act
        # Find Research Capabilities or similar section
        section_match = re.search(
            r'## (?:Research Capabilities|Capabilities|Advanced.*Capabilities)\s*\n(.*?)(?=\n##|\Z)',
            agent_content,
            re.DOTALL | re.IGNORECASE
        )

        if not section_match:
            pytest.skip("No capabilities section found")

        section_content = section_match.group(1)

        # Check for research task keywords
        research_keywords = [
            'repository archaeology',
            'pattern mining',
            'competitive analysis',
            'technology trends',
            'market intelligence',
            'web research'
        ]

        found_keywords = sum(
            1 for keyword in research_keywords
            if keyword.lower() in section_content.lower()
        )

        # Assert
        assert found_keywords >= 3, \
            f"Capabilities section should focus on research tasks (found only {found_keywords}/6 keywords)"

    def test_no_command_prefix_execution_framework_in_any_section(self, agent_content):
        """
        Comprehensive: Ensure no command execution framework patterns anywhere

        Arrange: Load agent file content
        Act: Search entire file for any command framework patterns
        Assert: Zero matches across entire file
        """
        # Act
        framework_patterns = [
            r'command execution',
            r'execute command',
            r'command prefix',
            r'command workflow',
            r'command resolution'
        ]

        found_framework_refs = []
        for pattern in framework_patterns:
            matches = re.findall(pattern, agent_content, re.IGNORECASE)
            if matches:
                found_framework_refs.extend(matches)

        # Assert
        assert len(found_framework_refs) == 0, \
            f"Found {len(found_framework_refs)} command framework references (must be removed): {found_framework_refs}"
