"""
Unit tests for STORY-035 AC4: Standard subagent sections present

Tests verify the agent structure follows DevForgeAI subagent template:
- ## When Invoked (proactive triggers + explicit invocation)
- ## Framework Integration (invoked by which skills, requires what context)
- ## Success Criteria (measurable checklist with token budget <40K)
- ## Integration (works with which other skills/subagents)
"""

import pytest
import re
from pathlib import Path


@pytest.mark.story_035
@pytest.mark.acceptance_criteria
@pytest.mark.unit
class TestAC4SubagentSections:
    """Test suite for AC4: Standard subagent sections present"""

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
    def when_invoked_section(self, agent_content):
        """Extract When Invoked section"""
        match = re.search(
            r'## When Invoked\s*\n(.*?)(?=\n##|\Z)',
            agent_content,
            re.DOTALL | re.IGNORECASE
        )
        if match:
            return match.group(1)
        return ""

    @pytest.fixture
    def framework_integration_section(self, agent_content):
        """Extract Framework Integration section"""
        match = re.search(
            r'## Framework Integration\s*\n(.*?)(?=\n##|\Z)',
            agent_content,
            re.DOTALL | re.IGNORECASE
        )
        if match:
            return match.group(1)
        return ""

    @pytest.fixture
    def success_criteria_section(self, agent_content):
        """Extract Success Criteria section"""
        match = re.search(
            r'## Success Criteria\s*\n(.*?)(?=\n##|\Z)',
            agent_content,
            re.DOTALL | re.IGNORECASE
        )
        if match:
            return match.group(1)
        return ""

    @pytest.fixture
    def integration_section(self, agent_content):
        """Extract Integration section"""
        match = re.search(
            r'## Integration\s*\n(.*?)(?=\n##|\Z)',
            agent_content,
            re.DOTALL | re.IGNORECASE
        )
        if match:
            return match.group(1)
        return ""

    def test_when_invoked_section_exists(self, agent_content):
        """
        AC4 / COMP-006: Agent must have 'When Invoked' section

        Arrange: Load agent file content
        Act: Search for ## When Invoked heading
        Assert: Section exists
        """
        # Act
        has_section = bool(re.search(r'## When Invoked', agent_content, re.IGNORECASE))

        # Assert
        assert has_section, "Missing required section '## When Invoked'"

    def test_when_invoked_has_proactive_triggers(self, when_invoked_section):
        """
        AC4 / COMP-006: When Invoked section must list proactive triggers

        Arrange: Extract When Invoked section
        Act: Search for trigger scenarios
        Assert: Contains proactive trigger examples
        """
        # Act
        has_proactive_triggers = bool(re.search(r'proactive|automatic|trigger', when_invoked_section, re.IGNORECASE))

        # Assert
        assert has_proactive_triggers, \
            "'When Invoked' section must document proactive trigger scenarios"

    def test_when_invoked_mentions_devforgeai_ideation(self, when_invoked_section):
        """
        COMP-006: When Invoked section must mention devforgeai-ideation

        Arrange: Extract When Invoked section
        Act: Search for devforgeai-ideation
        Assert: Skill mentioned as invoking context
        """
        # Act
        has_ideation = bool(re.search(r'devforgeai-ideation', when_invoked_section, re.IGNORECASE))

        # Assert
        assert has_ideation, \
            "'When Invoked' section must mention 'devforgeai-ideation' as invoking skill"

    def test_when_invoked_mentions_devforgeai_architecture(self, when_invoked_section):
        """
        COMP-006: When Invoked section must mention devforgeai-architecture

        Arrange: Extract When Invoked section
        Act: Search for devforgeai-architecture
        Assert: Skill mentioned as invoking context
        """
        # Act
        has_architecture = bool(re.search(r'devforgeai-architecture', when_invoked_section, re.IGNORECASE))

        # Assert
        assert has_architecture, \
            "'When Invoked' section must mention 'devforgeai-architecture' as invoking skill"

    def test_when_invoked_has_explicit_invocation_pattern(self, when_invoked_section):
        """
        AC4: When Invoked section should show explicit invocation pattern

        Arrange: Extract When Invoked section
        Act: Search for Task invocation example
        Assert: Contains Task(...) invocation syntax
        """
        # Act
        has_task_invocation = bool(re.search(r'Task\s*\(', when_invoked_section, re.IGNORECASE))

        # Assert
        assert has_task_invocation, \
            "'When Invoked' section should include Task(...) invocation example"

    def test_framework_integration_section_exists(self, agent_content):
        """
        AC4 / COMP-004: Agent must have 'Framework Integration' section

        Arrange: Load agent file content
        Act: Search for ## Framework Integration heading
        Assert: Section exists
        """
        # Act
        has_section = bool(re.search(r'## Framework Integration', agent_content, re.IGNORECASE))

        # Assert
        assert has_section, "Missing required section '## Framework Integration'"

    def test_framework_integration_documents_invoking_skills(self, framework_integration_section):
        """
        AC4: Framework Integration section must document which skills invoke this subagent

        Arrange: Extract Framework Integration section
        Act: Search for skill invocation documentation
        Assert: Contains "invoked by" or similar phrasing
        """
        # Act
        has_invocation_docs = bool(re.search(
            r'invoked by|called by|used by|triggered by',
            framework_integration_section,
            re.IGNORECASE
        ))

        # Assert
        assert has_invocation_docs, \
            "'Framework Integration' section must document which skills invoke this subagent"

    def test_framework_integration_documents_required_context(self, framework_integration_section):
        """
        AC4: Framework Integration section must document required context

        Arrange: Extract Framework Integration section
        Act: Search for context requirements
        Assert: Contains "requires" or "depends on" language
        """
        # Act
        has_context_reqs = bool(re.search(
            r'requires|depends on|needs|expects',
            framework_integration_section,
            re.IGNORECASE
        ))

        # Assert
        assert has_context_reqs, \
            "'Framework Integration' section must document required context/dependencies"

    def test_success_criteria_section_exists(self, agent_content):
        """
        AC4 / COMP-007: Agent must have 'Success Criteria' section

        Arrange: Load agent file content
        Act: Search for ## Success Criteria heading
        Assert: Section exists
        """
        # Act
        has_section = bool(re.search(r'## Success Criteria', agent_content, re.IGNORECASE))

        # Assert
        assert has_section, "Missing required section '## Success Criteria'"

    def test_success_criteria_is_measurable_checklist(self, success_criteria_section):
        """
        AC4 / COMP-007: Success Criteria must be measurable checklist

        Arrange: Extract Success Criteria section
        Act: Check for checkbox format (- [ ])
        Assert: Contains checkboxes
        """
        # Act
        has_checkboxes = bool(re.search(r'- \[ \]', success_criteria_section))

        # Assert
        assert has_checkboxes, \
            "'Success Criteria' section must use checklist format (- [ ])"

    def test_success_criteria_includes_token_budget(self, success_criteria_section):
        """
        AC4 / COMP-007: Success Criteria must include token budget (<40K)

        Arrange: Extract Success Criteria section
        Act: Search for token budget reference
        Assert: Contains 40K or 40,000 token reference
        """
        # Act
        has_token_budget = bool(re.search(
            r'40[,\s]*000|40K|token.*budget',
            success_criteria_section,
            re.IGNORECASE
        ))

        # Assert
        assert has_token_budget, \
            "'Success Criteria' section must include token budget reference (<40K tokens)"

    def test_integration_section_exists(self, agent_content):
        """
        AC4 / COMP-008: Agent must have 'Integration' section

        Arrange: Load agent file content
        Act: Search for ## Integration heading
        Assert: Section exists
        """
        # Act
        has_section = bool(re.search(r'## Integration', agent_content, re.IGNORECASE))

        # Assert
        assert has_section, "Missing required section '## Integration'"

    def test_integration_lists_devforgeai_ideation(self, integration_section):
        """
        AC4 / COMP-008: Integration section must list devforgeai-ideation

        Arrange: Extract Integration section
        Act: Search for devforgeai-ideation
        Assert: Skill mentioned
        """
        # Act
        has_ideation = bool(re.search(r'devforgeai-ideation', integration_section, re.IGNORECASE))

        # Assert
        assert has_ideation, \
            "'Integration' section must list 'devforgeai-ideation' as invoking skill"

    def test_integration_lists_devforgeai_architecture(self, integration_section):
        """
        AC4 / COMP-008: Integration section must list devforgeai-architecture

        Arrange: Extract Integration section
        Act: Search for devforgeai-architecture
        Assert: Skill mentioned
        """
        # Act
        has_architecture = bool(re.search(r'devforgeai-architecture', integration_section, re.IGNORECASE))

        # Assert
        assert has_architecture, \
            "'Integration' section must list 'devforgeai-architecture' as invoking skill"

    def test_comp_006_007_008_all_sections_present(self, agent_content):
        """
        COMP-006/007/008: Verify all 3 new sections present

        Arrange: Load agent file content
        Act: Check for When Invoked, Success Criteria, Integration sections
        Assert: All 3 sections exist
        """
        # Act
        sections = {
            'When Invoked': bool(re.search(r'## When Invoked', agent_content, re.IGNORECASE)),
            'Success Criteria': bool(re.search(r'## Success Criteria', agent_content, re.IGNORECASE)),
            'Integration': bool(re.search(r'## Integration', agent_content, re.IGNORECASE))
        }

        missing_sections = [name for name, exists in sections.items() if not exists]

        # Assert
        assert len(missing_sections) == 0, \
            f"COMP-006/007/008 FAILED: Missing required sections: {missing_sections}"

    @pytest.mark.edge_case
    def test_sections_follow_devforgeai_formatting_conventions(self, agent_content):
        """
        AC4: Sections must follow DevForgeAI formatting conventions

        Arrange: Load agent file content
        Act: Verify section formatting (## heading level, proper markdown)
        Assert: All sections use level 2 headings
        """
        # Act
        required_sections = [
            'When Invoked',
            'Framework Integration',
            'Success Criteria',
            'Integration'
        ]

        incorrect_formatting = []
        for section in required_sections:
            # Check for level 2 heading (##)
            pattern = rf'^## {section}$'
            if not re.search(pattern, agent_content, re.MULTILINE | re.IGNORECASE):
                incorrect_formatting.append(section)

        # Assert
        assert len(incorrect_formatting) == 0, \
            f"Sections with incorrect heading level: {incorrect_formatting} (must use '## Heading')"

    @pytest.mark.edge_case
    def test_success_criteria_has_multiple_measurable_items(self, success_criteria_section):
        """
        Edge case: Success Criteria should have multiple measurable items

        Arrange: Extract Success Criteria section
        Act: Count checklist items
        Assert: At least 3 checklist items present
        """
        # Act
        checkbox_count = len(re.findall(r'- \[ \]', success_criteria_section))

        # Assert
        assert checkbox_count >= 3, \
            f"'Success Criteria' section should have at least 3 measurable items (found: {checkbox_count})"

    def test_integration_section_documents_coordination(self, integration_section):
        """
        Best practice: Integration section should document how skills coordinate

        Arrange: Extract Integration section
        Act: Search for coordination language
        Assert: Contains coordination documentation
        """
        # Act
        coordination_keywords = ['coordinate', 'invoke', 'call', 'use', 'integrate', 'work with']
        has_coordination = any(
            keyword in integration_section.lower() for keyword in coordination_keywords
        )

        # Assert
        assert has_coordination, \
            "'Integration' section should document how skills coordinate with this subagent"
