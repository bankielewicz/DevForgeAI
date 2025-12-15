"""
Integration Tests for STORY-035: Internet-Sleuth Framework Compliance (Phase 1 Migration)

These integration tests validate the internet-sleuth agent's compliance with DevForgeAI
framework standards and its integration with devforgeai-ideation and devforgeai-architecture skills.

Test Categories:
1. Agent File Structure and Compliance (8 tests)
2. Framework Integration Points (7 tests)
3. Context File Awareness (6 tests)
4. Output Directory Compliance (5 tests)
5. Error Handling and Security (6 tests)

Total: 32 integration tests
"""

import pytest
import re
from pathlib import Path
import yaml


# ============================================================================
# Test Category 1: Agent File Structure and Compliance
# ============================================================================

@pytest.mark.story_035
@pytest.mark.integration
class TestInternetSleuthAgentStructure:
    """Integration tests for agent file structure and DevForgeAI compliance."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Load agent file for all tests in this class."""
        self.agent_file = Path(".claude/agents/internet-sleuth.md")
        assert self.agent_file.exists(), "internet-sleuth agent not found"
        self.content = self.agent_file.read_text()

    def test_agent_file_exists(self):
        """INT-001: Agent file exists at expected location"""
        assert self.agent_file.exists(), "internet-sleuth.md not found in .claude/agents/"

    def test_agent_has_valid_yaml_frontmatter(self):
        """INT-002: Agent has valid YAML frontmatter with required fields"""
        # Extract frontmatter
        match = re.match(r'^---\n(.*?)\n---', self.content, re.DOTALL)
        assert match, "No YAML frontmatter found"

        frontmatter_text = match.group(1)
        frontmatter = yaml.safe_load(frontmatter_text)

        # Check required fields
        assert 'name' in frontmatter, "Missing 'name' field in frontmatter"
        assert frontmatter['name'] == 'internet-sleuth', "Incorrect agent name"

        assert 'description' in frontmatter, "Missing 'description' field"
        assert 'devforgeai-ideation' in frontmatter['description'], \
            "Description doesn't mention devforgeai-ideation"
        assert 'devforgeai-architecture' in frontmatter['description'], \
            "Description doesn't mention devforgeai-architecture"

        assert 'tools' in frontmatter, "Missing 'tools' field"
        assert 'model' in frontmatter, "Missing 'model' field"
        assert frontmatter['model'] == 'haiku', "Expected model: haiku"

    def test_agent_has_required_sections(self):
        """INT-003: Agent has all required DevForgeAI subagent sections"""
        required_sections = [
            '# Internet Sleuth',
            '## Purpose',
            '## When Invoked',
            '## Workflow',
            '## Framework Integration',
            '## Success Criteria',
            '## Error Handling',
            '## Integration',
            '## Token Efficiency',
            '## Security Constraints',
        ]

        for section in required_sections:
            assert section in self.content, f"Missing required section: {section}"

    def test_no_command_execution_framework(self):
        """INT-004: Agent has no command execution framework references"""
        # Check for prohibited patterns
        prohibited_patterns = [
            r'description:.*Slash command',
            r'description:.*Command to',
            r'argument-hint:',
            r'Argument Validation',
            r'\$1',  # Command argument variable
            r'\$2',
            r'AskUserQuestion.*arguments',
        ]

        for pattern in prohibited_patterns:
            assert not re.search(pattern, self.content, re.IGNORECASE), \
                f"Found prohibited command framework pattern: {pattern}"

    def test_agent_mentions_proactive_triggers(self):
        """INT-005: Agent clearly states proactive trigger scenarios"""
        when_invoked_section = self._extract_section('## When Invoked')

        assert 'Proactive triggers:' in when_invoked_section, \
            "Missing 'Proactive triggers:' subsection"
        assert 'devforgeai-ideation' in when_invoked_section, \
            "Missing devforgeai-ideation in proactive triggers"
        assert 'devforgeai-architecture' in when_invoked_section, \
            "Missing devforgeai-architecture in proactive triggers"

    def test_agent_has_explicit_invocation_example(self):
        """INT-006: Agent provides explicit invocation example with Task tool"""
        when_invoked_section = self._extract_section('## When Invoked')

        assert 'Explicit invocation:' in when_invoked_section, \
            "Missing 'Explicit invocation:' subsection"
        assert 'Task(' in when_invoked_section, \
            "Missing Task tool invocation example"
        assert 'subagent_type="internet-sleuth"' in when_invoked_section, \
            "Missing correct subagent_type parameter"

    def test_workflow_phases_defined(self):
        """INT-007: Agent workflow has clearly defined phases"""
        # Check for phase structure in full content (phases span multiple sections)
        assert '### Phase 1: Context Validation' in self.content, \
            "Missing Phase 1: Context Validation"
        assert '### Phase 2: Research Execution' in self.content, \
            "Missing Phase 2: Research Execution"
        assert '### Phase 3: Intelligence Synthesis' in self.content, \
            "Missing Phase 3: Intelligence Synthesis"
        assert '### Phase 4: Output Generation' in self.content, \
            "Missing Phase 4: Output Generation"

    def test_framework_integration_section_complete(self):
        """INT-008: Framework Integration section documents all touchpoints"""
        framework_section = self._extract_section('## Framework Integration')

        # Check context files documentation
        context_files = [
            'tech-stack.md',
            'source-tree.md',
            'dependencies.md',
            'coding-standards.md',
            'architecture-constraints.md',
            'anti-patterns.md'
        ]

        for cf in context_files:
            assert cf in framework_section, \
                f"Missing context file documentation: {cf}"

        # Check ADR integration
        assert 'ADR Integration:' in framework_section, \
            "Missing ADR Integration subsection"

        # Check skill invocation documentation
        assert 'Invoked By:' in framework_section, \
            "Missing 'Invoked By:' documentation"
        assert 'devforgeai-ideation' in framework_section, \
            "Missing devforgeai-ideation in Framework Integration"
        assert 'devforgeai-architecture' in framework_section, \
            "Missing devforgeai-architecture in Framework Integration"

    # Helper method
    def _extract_section(self, heading):
        """Extract content of a specific section."""
        pattern = re.escape(heading) + r'\n\n(.*?)(?=\n##|\Z)'
        match = re.search(pattern, self.content, re.DOTALL)
        if match:
            return match.group(1)
        return ""


# ============================================================================
# Test Category 2: Framework Integration Points
# ============================================================================

@pytest.mark.story_035
@pytest.mark.integration
class TestInternetSleuthFrameworkIntegration:
    """Integration tests for framework integration points."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Load agent file for all tests."""
        self.agent_file = Path(".claude/agents/internet-sleuth.md")
        self.content = self.agent_file.read_text()

    def test_context_file_paths_use_devforgeai_structure(self):
        """INT-009: All context file paths use .devforgeai/ structure"""
        # Check for old paths
        old_paths = [
            r'\.claude/context/',
            r'\devforgeai/specs/research/',
        ]

        for pattern in old_paths:
            matches = re.findall(pattern, self.content)
            assert len(matches) == 0, \
                f"Found deprecated path pattern: {pattern} (matches: {matches})"

        # Verify correct paths used
        assert 'devforgeai/context/' in self.content, \
            "Missing devforgeai/context/ path"
        assert '.devforgeai/research/' in self.content, \
            "Missing .devforgeai/research/ path"

    def test_ideation_skill_compatibility(self):
        """INT-010: Agent compatible with devforgeai-ideation skill invocation"""
        # Check When Invoked section mentions ideation
        when_invoked = self._extract_section('## When Invoked')
        assert 'devforgeai-ideation' in when_invoked, \
            "Missing devforgeai-ideation in When Invoked section"

        # Check Automatic subsection
        assert 'Automatic:' in when_invoked, \
            "Missing 'Automatic:' subsection"
        assert 'devforgeai-ideation skill' in when_invoked, \
            "Missing devforgeai-ideation in Automatic triggers"
        assert 'Phase 5: Feasibility Analysis' in when_invoked, \
            "Missing Phase 5 reference for ideation skill"

    def test_architecture_skill_compatibility(self):
        """INT-011: Agent compatible with devforgeai-architecture skill invocation"""
        when_invoked = self._extract_section('## When Invoked')

        assert 'devforgeai-architecture' in when_invoked, \
            "Missing devforgeai-architecture in When Invoked section"
        assert 'Phase 2: Create Context Files' in when_invoked, \
            "Missing Phase 2 reference for architecture skill"

    def test_output_directory_compliance(self):
        """INT-012: Research outputs use .devforgeai/research/ directory"""
        # Check Phase 4 workflow
        phase4 = self._extract_section('### Phase 4: Output Generation')
        assert phase4, "Phase 4: Output Generation section not found"

        assert '.devforgeai/research/' in phase4, \
            "Missing .devforgeai/research/ in Phase 4"

        # Check output examples
        assert 'tech-eval-' in phase4, \
            "Missing technology evaluation filename pattern"
        assert 'pattern-analysis-' in phase4, \
            "Missing pattern analysis filename pattern"
        assert 'competitive-' in phase4, \
            "Missing competitive research filename pattern"

    def test_adr_integration_documented(self):
        """INT-013: ADR integration is properly documented"""
        framework_section = self._extract_section('## Framework Integration')

        assert 'ADR Integration:' in framework_section, \
            "Missing ADR Integration subsection"
        assert '.devforgeai/adrs/' in framework_section, \
            "Missing ADR directory path"
        assert 'REQUIRES ADR' in framework_section or 'REQUIRES ADR' in self.content, \
            "Missing REQUIRES ADR flag documentation"

    def test_requirements_analyst_coordination(self):
        """INT-014: Agent coordinates with requirements-analyst subagent"""
        framework_section = self._extract_section('## Framework Integration')

        assert 'requirements-analyst' in framework_section, \
            "Missing requirements-analyst coordination"
        assert 'Works With:' in framework_section or 'Coordinates with:' in framework_section, \
            "Missing 'Works With:' or 'Coordinates with:' subsection"

    def test_architect_reviewer_coordination(self):
        """INT-015: Agent coordinates with architect-reviewer subagent"""
        framework_section = self._extract_section('## Framework Integration')

        assert 'architect-reviewer' in framework_section, \
            "Missing architect-reviewer coordination"

    # Helper method
    def _extract_section(self, heading):
        """Extract content of a specific section."""
        pattern = re.escape(heading) + r'\n\n(.*?)(?=\n##|\Z)'
        match = re.search(pattern, self.content, re.DOTALL)
        if match:
            return match.group(1)
        return ""


# ============================================================================
# Test Category 3: Context File Awareness
# ============================================================================

@pytest.mark.story_035
@pytest.mark.integration
class TestInternetSleuthContextFileAwareness:
    """Integration tests for context file awareness."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Load agent file for all tests."""
        self.agent_file = Path(".claude/agents/internet-sleuth.md")
        self.content = self.agent_file.read_text()

    def test_phase1_validates_context_files(self):
        """INT-016: Phase 1 includes context file validation"""
        phase1 = self._extract_section('### Phase 1: Context Validation')
        assert phase1, "Phase 1: Context Validation not found"

        # Check for brownfield/greenfield detection
        assert 'brownfield' in phase1.lower() or 'greenfield' in phase1.lower(), \
            "Missing brownfield/greenfield mode detection"

        # Check for context file existence check
        assert 'devforgeai/context/' in phase1, \
            "Missing devforgeai/context/ path in Phase 1"

    def test_tech_stack_validation_documented(self):
        """INT-017: tech-stack.md validation is documented"""
        framework_section = self._extract_section('## Framework Integration')

        assert 'tech-stack.md' in framework_section, \
            "Missing tech-stack.md in Framework Integration"
        assert 'Locked Technologies' in framework_section or 'approved' in framework_section.lower(), \
            "Missing tech-stack.md purpose documentation"

    def test_dependencies_validation_documented(self):
        """INT-018: dependencies.md validation is documented"""
        framework_section = self._extract_section('## Framework Integration')

        assert 'dependencies.md' in framework_section, \
            "Missing dependencies.md in Framework Integration"
        assert 'Approved Packages' in framework_section or 'approved' in framework_section.lower(), \
            "Missing dependencies.md purpose documentation"

    def test_anti_patterns_validation_documented(self):
        """INT-019: anti-patterns.md validation is documented"""
        framework_section = self._extract_section('## Framework Integration')

        assert 'anti-patterns.md' in framework_section, \
            "Missing anti-patterns.md in Framework Integration"
        assert 'Forbidden Patterns' in framework_section or 'forbidden' in framework_section.lower(), \
            "Missing anti-patterns.md purpose documentation"

    def test_architecture_constraints_validation_documented(self):
        """INT-020: architecture-constraints.md validation is documented"""
        framework_section = self._extract_section('## Framework Integration')

        assert 'architecture-constraints.md' in framework_section, \
            "Missing architecture-constraints.md in Framework Integration"
        assert 'Layer Boundaries' in framework_section or 'layer' in framework_section.lower(), \
            "Missing architecture-constraints.md purpose documentation"

    def test_context_conflict_handling_documented(self):
        """INT-021: Handling of context file conflicts is documented"""
        # Check Phase 3 (Intelligence Synthesis)
        phase3 = self._extract_section('### Phase 3: Intelligence Synthesis')

        assert 'Technology Validation Against Framework' in phase3 or 'tech-stack.md' in phase3, \
            "Missing technology validation in Phase 3"

        # Check Error Handling section
        error_section = self._extract_section('## Error Handling')
        assert 'Technology Conflict with tech-stack.md' in error_section or \
               'conflict' in error_section.lower(), \
            "Missing technology conflict handling"

    # Helper method
    def _extract_section(self, heading):
        """Extract content of a specific section."""
        pattern = re.escape(heading) + r'\n\n(.*?)(?=\n##|\Z)'
        match = re.search(pattern, self.content, re.DOTALL)
        if match:
            return match.group(1)
        return ""


# ============================================================================
# Test Category 4: Output Directory Compliance
# ============================================================================

@pytest.mark.story_035
@pytest.mark.integration
class TestInternetSleuthOutputCompliance:
    """Integration tests for output directory compliance."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Load agent file for all tests."""
        self.agent_file = Path(".claude/agents/internet-sleuth.md")
        self.content = self.agent_file.read_text()

    def test_research_output_directory_documented(self):
        """INT-022: .devforgeai/research/ directory is documented"""
        # Check Phase 4
        phase4 = self._extract_section('### Phase 4: Output Generation')

        assert '.devforgeai/research/' in phase4, \
            "Missing .devforgeai/research/ in Phase 4"

    def test_filename_conventions_documented(self):
        """INT-023: Filename conventions are documented"""
        phase4 = self._extract_section('### Phase 4: Output Generation')

        # Check for filename patterns
        patterns = [
            'tech-eval-',
            'pattern-analysis-',
            'competitive-',
        ]

        for pattern in patterns:
            assert pattern in phase4, \
                f"Missing filename pattern: {pattern}"

        # Check for date format
        assert 'YYYY-MM-DD' in phase4 or '{YYYY-MM-DD}' in phase4, \
            "Missing date format in filename convention"

    def test_directory_creation_documented(self):
        """INT-024: Directory creation is documented in Phase 4"""
        phase4 = self._extract_section('### Phase 4: Output Generation')

        assert 'Create Research Directory' in phase4 or 'create directory' in phase4.lower(), \
            "Missing directory creation step"
        assert '755' in phase4 or 'permissions' in phase4.lower(), \
            "Missing permissions documentation"

    def test_repository_cleanup_documented(self):
        """INT-025: Repository cleanup is documented"""
        phase4 = self._extract_section('### Phase 4: Output Generation')

        assert 'Repository Cleanup' in phase4 or 'cleanup' in phase4.lower(), \
            "Missing repository cleanup step"
        assert '7 days' in phase4, \
            "Missing cleanup timeframe"

    def test_output_examples_provided(self):
        """INT-026: Output examples are provided"""
        # Check for example output section
        assert 'Research Output Directory:' in self.content or \
               '`.devforgeai/research/`' in self.content, \
            "Missing research output directory examples"

        # Check for at least one filename example
        assert 'tech-eval-react-patterns' in self.content or \
               'pattern-analysis-' in self.content or \
               'competitive-' in self.content, \
            "Missing filename examples"

    # Helper method
    def _extract_section(self, heading):
        """Extract content of a specific section."""
        pattern = re.escape(heading) + r'\n\n(.*?)(?=\n##|\Z)'
        match = re.search(pattern, self.content, re.DOTALL)
        if match:
            return match.group(1)
        return ""


# ============================================================================
# Test Category 5: Error Handling and Security
# ============================================================================

@pytest.mark.story_035
@pytest.mark.integration
class TestInternetSleuthErrorHandlingAndSecurity:
    """Integration tests for error handling and security."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Load agent file for all tests."""
        self.agent_file = Path(".claude/agents/internet-sleuth.md")
        self.content = self.agent_file.read_text()

    def test_error_handling_section_exists(self):
        """INT-027: Error Handling section exists and is comprehensive"""
        error_section = self._extract_section('## Error Handling')
        assert error_section, "Error Handling section not found"

        # Check for specific error scenarios
        error_scenarios = [
            'Missing Context Files',
            'Technology Conflict',
            'Repository Access Denied',
            'GitHub API Rate Limit',
            'Large Repository',
            'Greenfield Project',
            'Invalid Repository URL',
        ]

        found_scenarios = sum(1 for scenario in error_scenarios if scenario in error_section)
        assert found_scenarios >= 5, \
            f"Expected at least 5 error scenarios, found {found_scenarios}"

    def test_environment_variable_usage_documented(self):
        """INT-028: Environment variable usage is documented"""
        security_section = self._extract_section('## Security Constraints')

        assert 'GITHUB_TOKEN' in security_section, \
            "Missing GITHUB_TOKEN environment variable documentation"
        assert 'environment variable' in security_section.lower(), \
            "Missing environment variable usage documentation"

    def test_no_hardcoded_credentials(self):
        """INT-029: No hardcoded credentials in agent file"""
        # Check for common credential patterns
        credential_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api[_-]?key\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
            r'ghp_[A-Za-z0-9]{36}',  # GitHub personal access token
            r'gho_[A-Za-z0-9]{36}',  # GitHub OAuth token
        ]

        for pattern in credential_patterns:
            matches = re.findall(pattern, self.content, re.IGNORECASE)
            # Filter out documentation examples
            real_matches = [m for m in matches if 'example' not in m.lower() and
                          'GITHUB_TOKEN' not in m]
            assert len(real_matches) == 0, \
                f"Found potential hardcoded credential: {pattern}"

    def test_secret_redaction_documented(self):
        """INT-030: Secret redaction is documented"""
        security_section = self._extract_section('## Security Constraints')

        assert 'Secret Redaction' in security_section or 'redact' in security_section.lower(), \
            "Missing secret redaction documentation"
        assert '[REDACTED]' in security_section, \
            "Missing redaction placeholder example"

    def test_graceful_degradation_documented(self):
        """INT-031: Graceful degradation is documented"""
        # Check in full content (may be in Reliability section instead of Error Handling)
        assert 'Graceful Degradation' in self.content or \
               ('graceful' in self.content.lower() and 'degradation' in self.content.lower()), \
            "Missing graceful degradation documentation"

    def test_structured_error_responses_documented(self):
        """INT-032: Structured error responses are documented"""
        error_section = self._extract_section('## Error Handling')

        assert 'structured' in error_section.lower() or \
               'JSON' in error_section, \
            "Missing structured error response documentation"

    # Helper method
    def _extract_section(self, heading):
        """Extract content of a specific section."""
        pattern = re.escape(heading) + r'\n\n(.*?)(?=\n##|\Z)'
        match = re.search(pattern, self.content, re.DOTALL)
        if match:
            return match.group(1)
        return ""


# ============================================================================
# Test Execution Summary
# ============================================================================

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "story_035: Integration tests for STORY-035"
    )
    config.addinivalue_line(
        "markers", "integration: Integration test marker"
    )
