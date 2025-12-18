"""
Unit tests for STORY-035 AC3: Context file awareness integrated

Tests verify the internet-sleuth agent references all 6 DevForgeAI context files:
- tech-stack.md (locked technologies)
- source-tree.md (project structure)
- dependencies.md (approved packages)
- coding-standards.md (code patterns)
- architecture-constraints.md (layer boundaries)
- anti-patterns.md (forbidden patterns)

Agent must check ADRs before recommending technology changes.
"""

import pytest
import re
from pathlib import Path


@pytest.mark.story_035
@pytest.mark.acceptance_criteria
@pytest.mark.unit
class TestAC3ContextFileAwareness:
    """Test suite for AC3: Context file awareness integrated"""

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
    def framework_integration_section(self, agent_content):
        """Extract Framework Integration section"""
        match = re.search(
            r'## Framework Integration\s*\n(.*?)(?=\n##|\Z)',
            agent_content,
            re.DOTALL | re.IGNORECASE
        )
        assert match, "## Framework Integration section not found in agent file"
        return match.group(1)

    def test_framework_integration_section_exists(self, agent_content):
        """
        AC3 / AC4: Agent must have Framework Integration section

        Arrange: Load agent file content
        Act: Search for ## Framework Integration heading
        Assert: Section exists
        """
        # Act
        has_section = bool(re.search(r'## Framework Integration', agent_content, re.IGNORECASE))

        # Assert
        assert has_section, "Missing required section '## Framework Integration'"

    def test_references_tech_stack_context_file(self, framework_integration_section):
        """
        AC3 / COMP-004: Must reference tech-stack.md context file

        Arrange: Extract Framework Integration section
        Act: Search for tech-stack.md reference
        Assert: File mentioned with purpose
        """
        # Act
        has_tech_stack = bool(re.search(r'tech-stack\.md', framework_integration_section, re.IGNORECASE))

        # Assert
        assert has_tech_stack, "Framework Integration section must reference 'tech-stack.md'"

    def test_references_source_tree_context_file(self, framework_integration_section):
        """
        AC3 / COMP-004: Must reference source-tree.md context file

        Arrange: Extract Framework Integration section
        Act: Search for source-tree.md reference
        Assert: File mentioned with purpose
        """
        # Act
        has_source_tree = bool(re.search(r'source-tree\.md', framework_integration_section, re.IGNORECASE))

        # Assert
        assert has_source_tree, "Framework Integration section must reference 'source-tree.md'"

    def test_references_dependencies_context_file(self, framework_integration_section):
        """
        AC3 / COMP-004: Must reference dependencies.md context file

        Arrange: Extract Framework Integration section
        Act: Search for dependencies.md reference
        Assert: File mentioned with purpose
        """
        # Act
        has_dependencies = bool(re.search(r'dependencies\.md', framework_integration_section, re.IGNORECASE))

        # Assert
        assert has_dependencies, "Framework Integration section must reference 'dependencies.md'"

    def test_references_coding_standards_context_file(self, framework_integration_section):
        """
        AC3 / COMP-004: Must reference coding-standards.md context file

        Arrange: Extract Framework Integration section
        Act: Search for coding-standards.md reference
        Assert: File mentioned with purpose
        """
        # Act
        has_coding_standards = bool(re.search(r'coding-standards\.md', framework_integration_section, re.IGNORECASE))

        # Assert
        assert has_coding_standards, "Framework Integration section must reference 'coding-standards.md'"

    def test_references_architecture_constraints_context_file(self, framework_integration_section):
        """
        AC3 / COMP-004: Must reference architecture-constraints.md context file

        Arrange: Extract Framework Integration section
        Act: Search for architecture-constraints.md reference
        Assert: File mentioned with purpose
        """
        # Act
        has_arch_constraints = bool(re.search(r'architecture-constraints\.md', framework_integration_section, re.IGNORECASE))

        # Assert
        assert has_arch_constraints, "Framework Integration section must reference 'architecture-constraints.md'"

    def test_references_anti_patterns_context_file(self, framework_integration_section):
        """
        AC3 / COMP-004: Must reference anti-patterns.md context file

        Arrange: Extract Framework Integration section
        Act: Search for anti-patterns.md reference
        Assert: File mentioned with purpose
        """
        # Act
        has_anti_patterns = bool(re.search(r'anti-patterns\.md', framework_integration_section, re.IGNORECASE))

        # Assert
        assert has_anti_patterns, "Framework Integration section must reference 'anti-patterns.md'"

    def test_comp_004_all_six_context_files_listed(self, framework_integration_section):
        """
        COMP-004: All 6 context files must be listed in Framework Integration section

        Arrange: Extract Framework Integration section
        Act: Count context file references
        Assert: All 6 files present
        """
        # Act
        context_files = [
            'tech-stack.md',
            'source-tree.md',
            'dependencies.md',
            'coding-standards.md',
            'architecture-constraints.md',
            'anti-patterns.md'
        ]

        found_files = []
        missing_files = []

        for file in context_files:
            if re.search(re.escape(file), framework_integration_section, re.IGNORECASE):
                found_files.append(file)
            else:
                missing_files.append(file)

        # Assert
        assert len(found_files) == 6, \
            f"COMP-004 FAILED: Only {len(found_files)}/6 context files found. Missing: {missing_files}"

    def test_context_files_have_purpose_documented(self, framework_integration_section):
        """
        AC3: Each context file should have purpose documented

        Arrange: Extract Framework Integration section
        Act: Check if files have associated descriptions
        Assert: Files mentioned with purpose/description nearby
        """
        # Act
        context_files_with_purpose = [
            (r'tech-stack\.md', ['locked', 'technology', 'technologies']),
            (r'source-tree\.md', ['structure', 'organization', 'directory']),
            (r'dependencies\.md', ['packages', 'approved', 'dependencies']),
            (r'coding-standards\.md', ['patterns', 'conventions', 'standards']),
            (r'architecture-constraints\.md', ['layer', 'boundaries', 'constraints']),
            (r'anti-patterns\.md', ['forbidden', 'avoid', 'anti-pattern'])
        ]

        missing_purpose = []

        for file_pattern, purpose_keywords in context_files_with_purpose:
            # Find file mention
            file_match = re.search(file_pattern, framework_integration_section, re.IGNORECASE)
            if not file_match:
                missing_purpose.append(file_pattern.replace(r'\.', '.'))
                continue

            # Check for purpose keywords within 200 chars of file mention
            start_pos = max(0, file_match.start() - 100)
            end_pos = min(len(framework_integration_section), file_match.end() + 100)
            context_text = framework_integration_section[start_pos:end_pos].lower()

            has_purpose = any(keyword in context_text for keyword in purpose_keywords)
            if not has_purpose:
                missing_purpose.append(file_pattern.replace(r'\.', '.'))

        # Assert
        assert len(missing_purpose) == 0, \
            f"Context files missing purpose documentation: {missing_purpose}"

    def test_context_files_have_when_to_check_guidance(self, framework_integration_section):
        """
        AC3: Each context file should have "when to check" guidance

        Arrange: Extract Framework Integration section
        Act: Look for phrases indicating when to consult files
        Assert: Guidance present (when/before/check/validate keywords)
        """
        # Act
        guidance_keywords = ['when', 'before', 'check', 'validate', 'consult', 'reference']
        has_guidance = any(keyword in framework_integration_section.lower() for keyword in guidance_keywords)

        # Assert
        assert has_guidance, \
            "Framework Integration section must provide 'when to check' guidance for context files"

    def test_adr_awareness_workflow_present(self, agent_content):
        """
        AC3 / COMP-005: Agent must check ADRs before technology recommendations

        Arrange: Load agent file content
        Act: Search for ADR check workflow
        Assert: ADR check step documented with devforgeai/specs/adrs/ reference
        """
        # Act
        has_adr_check = bool(re.search(r'devforgeai/specs/adrs/', agent_content))
        has_adr_workflow = bool(re.search(r'ADR|adr|Architecture Decision Record', agent_content, re.IGNORECASE))

        # Assert
        assert has_adr_check, "Agent must reference 'devforgeai/specs/adrs/' directory for ADR awareness"
        assert has_adr_workflow, "Agent must document ADR check workflow"

    @pytest.mark.edge_case
    def test_adr_workflow_includes_askuserquestion_for_conflicts(self, agent_content):
        """
        COMP-005 / Edge case: ADR workflow should use AskUserQuestion for conflicts

        Arrange: Load agent file content
        Act: Search for AskUserQuestion in ADR workflow context
        Assert: AskUserQuestion mentioned for conflict resolution
        """
        # Act
        # Find sections mentioning ADR
        adr_sections = re.findall(
            r'(.{200}(?:ADR|adr|Architecture Decision Record).{200})',
            agent_content,
            re.IGNORECASE
        )

        has_askuserquestion = any('AskUserQuestion' in section for section in adr_sections)

        # Assert
        assert has_askuserquestion, \
            "ADR workflow should include AskUserQuestion for technology conflict resolution"

    @pytest.mark.business_rule
    def test_br_001_agent_halts_if_context_files_missing(self, agent_content):
        """
        BR-001: Agent must HALT with error if context files missing

        Arrange: Load agent file content
        Act: Search for HALT or error handling for missing context files
        Assert: Error handling documented
        """
        # Act
        has_halt_logic = bool(re.search(r'HALT|halt|error|missing.*context', agent_content, re.IGNORECASE))
        has_context_check = bool(re.search(r'check.*exist|validate.*context|missing.*file', agent_content, re.IGNORECASE))

        # Assert
        assert has_halt_logic and has_context_check, \
            "BR-001: Agent must document HALT behavior when context files missing"

    @pytest.mark.business_rule
    def test_br_002_requires_adr_message_for_tech_not_in_stack(self, agent_content):
        """
        BR-002: Agent must return 'REQUIRES ADR' message for tech not in tech-stack.md

        Arrange: Load agent file content
        Act: Search for "REQUIRES ADR" or equivalent message
        Assert: Message documented
        """
        # Act
        has_requires_adr = bool(re.search(r'REQUIRES ADR|require.*ADR|ADR.*required', agent_content, re.IGNORECASE))

        # Assert
        assert has_requires_adr, \
            "BR-002: Agent must document 'REQUIRES ADR' message for technology conflicts"

    def test_framework_aware_not_autonomous(self, agent_content):
        """
        AC3: Agent must NOT operate autonomously (framework-aware behavior required)

        Arrange: Load agent file content
        Act: Check for framework-aware language
        Assert: No autonomous decision-making language present
        """
        # Act
        # Negative: Should NOT have autonomous language
        autonomous_patterns = [
            r'automatically update',
            r'auto-update',
            r'autonomously modify',
            r'proceed without approval'
        ]

        autonomous_found = []
        for pattern in autonomous_patterns:
            if re.search(pattern, agent_content, re.IGNORECASE):
                autonomous_found.append(pattern)

        # Positive: Should HAVE framework-aware language
        framework_aware_patterns = [
            r'framework',
            r'AskUserQuestion',
            r'user approval',
            r'HALT'
        ]

        framework_aware_found = sum(
            1 for pattern in framework_aware_patterns
            if re.search(pattern, agent_content, re.IGNORECASE)
        )

        # Assert
        assert len(autonomous_found) == 0, \
            f"Agent contains autonomous decision-making language: {autonomous_found} (violates framework-aware requirement)"
        assert framework_aware_found >= 2, \
            "Agent must include framework-aware language (AskUserQuestion, user approval, HALT, etc.)"
