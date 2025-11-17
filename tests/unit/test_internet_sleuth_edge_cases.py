"""
Unit tests for STORY-035 Edge Cases

Tests verify agent handles edge case scenarios correctly:
1. Greenfield projects without context files
2. Brownfield projects with incomplete context
3. Conflicting technology recommendations
4. ADR-required scenarios
5. Token budget exceeded during analysis
6. Private repositories requiring authentication
7. Framework-aware coordination with existing subagents
"""

import pytest
import re
from pathlib import Path


@pytest.mark.story_035
@pytest.mark.edge_case
@pytest.mark.unit
class TestInternetSleuthEdgeCases:
    """Test suite for edge case scenarios"""

    @pytest.fixture
    def agent_file_path(self):
        """Path to internet-sleuth agent file"""
        return Path(".claude/agents/internet-sleuth.md")

    @pytest.fixture
    def agent_content(self, agent_file_path):
        """Load agent file content"""
        assert agent_file_path.exists(), f"Agent file not found: {agent_file_path}"
        return agent_file_path.read_text()

    def test_edge_case_1_greenfield_mode_documented(self, agent_content):
        """
        Edge Case 1: Greenfield projects without context files

        Arrange: Load agent file content
        Act: Search for greenfield mode handling
        Assert: Greenfield mode behavior documented
        """
        # Act
        has_greenfield = bool(re.search(r'greenfield', agent_content, re.IGNORECASE))
        has_no_context_handling = bool(re.search(
            r'context.*not.*exist|missing.*context|no.*context.*file',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        assert has_greenfield or has_no_context_handling, \
            "Edge Case 1: Agent must document greenfield mode (no context files) handling"

    def test_edge_case_1_recommends_tech_stack_for_greenfield(self, agent_content):
        """
        Edge Case 1: Greenfield mode should output tech-stack.md recommendations

        Arrange: Load agent file content
        Act: Search for recommendation behavior
        Assert: Documents providing initial tech stack recommendations
        """
        # Act
        has_recommendations = bool(re.search(
            r'recommend.*tech-stack|initial.*technolog|suggest.*stack',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        assert has_recommendations, \
            "Edge Case 1: Agent should document providing tech-stack.md recommendations for greenfield projects"

    def test_edge_case_2_brownfield_incomplete_context_halt_behavior(self, agent_content):
        """
        Edge Case 2: Brownfield with 4 of 6 context files must HALT

        Arrange: Load agent file content
        Act: Search for HALT behavior on missing context files
        Assert: HALT and error handling documented
        """
        # Act
        has_halt = bool(re.search(r'HALT|halt', agent_content, re.IGNORECASE))
        has_missing_files_check = bool(re.search(
            r'missing.*file|incomplete.*context|validate.*exist',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        assert has_halt and has_missing_files_check, \
            "Edge Case 2: Agent must document HALT behavior when context files incomplete"

    def test_edge_case_2_recommends_create_context_command(self, agent_content):
        """
        Edge Case 2: Should recommend /create-context for incomplete context

        Arrange: Load agent file content
        Act: Search for /create-context recommendation
        Assert: Command mentioned in error recovery
        """
        # Act
        has_create_context = bool(re.search(r'/create-context', agent_content))

        # Assert
        assert has_create_context, \
            "Edge Case 2: Agent should recommend '/create-context' command when context incomplete"

    def test_edge_case_3_technology_conflict_requires_adr_message(self, agent_content):
        """
        Edge Case 3: Technology conflicts must trigger 'REQUIRES ADR' message

        Arrange: Load agent file content
        Act: Search for REQUIRES ADR pattern
        Assert: Message documented for conflicts
        """
        # Act
        has_requires_adr = bool(re.search(r'REQUIRES ADR', agent_content))

        # Assert
        assert has_requires_adr, \
            "Edge Case 3: Agent must document 'REQUIRES ADR' message for technology conflicts"

    def test_edge_case_3_conflict_triggers_askuserquestion(self, agent_content):
        """
        Edge Case 3: Technology conflicts should use AskUserQuestion

        Arrange: Load agent file content
        Act: Search for AskUserQuestion with 2 options (update tech-stack or adjust scope)
        Assert: AskUserQuestion pattern documented
        """
        # Act
        has_askuserquestion = bool(re.search(r'AskUserQuestion', agent_content))

        # Check for conflict resolution options
        has_update_option = bool(re.search(
            r'update.*tech-stack.*ADR|ADR.*update.*tech-stack',
            agent_content,
            re.IGNORECASE
        ))
        has_adjust_scope = bool(re.search(
            r'adjust.*scope|scope.*existing.*stack',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        assert has_askuserquestion, "Edge Case 3: Must use AskUserQuestion for conflict resolution"
        assert has_update_option and has_adjust_scope, \
            "Edge Case 3: Must document 2 options: (1) Update tech-stack with ADR, (2) Adjust research scope"

    def test_edge_case_4_adr_check_before_new_technology(self, agent_content):
        """
        Edge Case 4: Agent must check .devforgeai/adrs/ for existing ADRs

        Arrange: Load agent file content
        Act: Search for ADR check workflow
        Assert: Check documented with proper ADR naming format
        """
        # Act
        has_adr_check = bool(re.search(r'check.*\.devforgeai/adrs/', agent_content, re.IGNORECASE))
        has_adr_naming = bool(re.search(r'ADR-\d{3}-|ADR-\{NNN\}-', agent_content))

        # Assert
        assert has_adr_check, \
            "Edge Case 4: Agent must document checking .devforgeai/adrs/ before technology recommendations"
        assert has_adr_naming, \
            "Edge Case 4: Agent must document proper ADR naming format (ADR-{NNN}-{technology-decision}.md)"

    def test_edge_case_5_token_budget_progressive_disclosure(self, agent_content):
        """
        Edge Case 5: Large repository analysis must use progressive disclosure

        Arrange: Load agent file content
        Act: Search for progressive disclosure strategy
        Assert: Strategy documented (initial scan + detailed analysis)
        """
        # Act
        has_progressive = bool(re.search(r'progressive.*disclos', agent_content, re.IGNORECASE))
        has_token_budget = bool(re.search(r'40[,\s]*000|40K.*token', agent_content, re.IGNORECASE))

        # Assert
        assert has_progressive and has_token_budget, \
            "Edge Case 5: Agent must document progressive disclosure strategy for token budget management"

    def test_edge_case_5_large_repo_partial_analysis(self, agent_content):
        """
        Edge Case 5: Large repositories should return partial analysis + summary

        Arrange: Load agent file content
        Act: Search for large repository handling
        Assert: Documents returning summary with link to full repo
        """
        # Act
        has_large_repo_handling = bool(re.search(
            r'large.*repositor|>1000.*file|partial.*analysis',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        assert has_large_repo_handling, \
            "Edge Case 5: Agent must document handling for large repositories (>1000 files)"

    def test_edge_case_6_private_repo_authentication_error(self, agent_content):
        """
        Edge Case 6: Private repositories must handle authentication failures

        Arrange: Load agent file content
        Act: Search for authentication error handling
        Assert: Structured error with gh CLI link documented
        """
        # Act
        has_auth_error = bool(re.search(
            r'403|401|authentication.*fail|access.*denied|private.*repositor',
            agent_content,
            re.IGNORECASE
        ))

        has_gh_cli_link = bool(re.search(r'gh.*auth|cli\.github\.com', agent_content, re.IGNORECASE))

        # Assert
        assert has_auth_error, \
            "Edge Case 6: Agent must document authentication failure handling for private repos"
        assert has_gh_cli_link, \
            "Edge Case 6: Error message should include GitHub CLI setup link (gh auth login)"

    def test_edge_case_6_no_retry_for_auth_failures(self, agent_content):
        """
        Edge Case 6: Agent must NOT retry auth failures (403, 401)

        Arrange: Load agent file content
        Act: Search for retry logic documentation
        Assert: Auth failures excluded from retry logic
        """
        # Act
        # Find retry logic section
        retry_section = re.search(
            r'retry.*\n(.*?)(?=\n##|\Z)',
            agent_content,
            re.DOTALL | re.IGNORECASE
        )

        if retry_section:
            retry_text = retry_section.group(1)
            excludes_auth = bool(re.search(
                r'do not retry.*403|do not retry.*401|not retry.*auth',
                retry_text,
                re.IGNORECASE
            ))
        else:
            excludes_auth = False

        # Assert
        assert excludes_auth or 'retry' not in agent_content.lower(), \
            "Edge Case 6: Agent must NOT retry authentication failures (403, 401)"

    def test_edge_case_7_reads_epic_file_for_context(self, agent_content):
        """
        Edge Case 7: Agent must read .ai_docs/Epics/{EPIC-ID}.epic.md for context

        Arrange: Load agent file content
        Act: Search for epic file reading workflow
        Assert: Documents reading epic for context before research
        """
        # Act
        has_epic_read = bool(re.search(r'\.ai_docs/Epics/|read.*epic', agent_content, re.IGNORECASE))

        # Assert
        assert has_epic_read, \
            "Edge Case 7: Agent must document reading epic file for context during ideation phase"

    def test_edge_case_7_recommendations_reference_epic_features(self, agent_content):
        """
        Edge Case 7: Recommendations should align with epic scope and features

        Arrange: Load agent file content
        Act: Search for epic alignment language
        Assert: Documents ensuring alignment with epic
        """
        # Act
        has_alignment = bool(re.search(
            r'align.*epic|epic.*scope|feature.*requirement|epic.*context',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        assert has_alignment, \
            "Edge Case 7: Agent must document ensuring recommendations align with epic scope"

    def test_all_edge_cases_have_documented_behavior(self, agent_content):
        """
        Comprehensive: Verify all 7 edge cases have some documentation

        Arrange: Load agent file content
        Act: Check for keywords related to each edge case
        Assert: At least 5 of 7 edge cases have documented behavior
        """
        # Act
        edge_case_keywords = {
            'greenfield': r'greenfield|no.*context.*file',
            'brownfield_incomplete': r'incomplete.*context|missing.*file.*HALT',
            'technology_conflict': r'REQUIRES ADR|conflict.*tech',
            'adr_check': r'check.*adrs/|existing.*ADR',
            'token_budget': r'progressive.*disclos|40K.*token',
            'auth_failure': r'403|401|authentication.*fail',
            'epic_context': r'epic\.md|read.*epic'
        }

        documented_cases = sum(
            1 for pattern in edge_case_keywords.values()
            if re.search(pattern, agent_content, re.IGNORECASE)
        )

        # Assert
        assert documented_cases >= 5, \
            f"Only {documented_cases}/7 edge cases documented (expected ≥5 for comprehensive coverage)"

    def test_edge_case_handling_uses_framework_patterns(self, agent_content):
        """
        Best practice: Edge case handling should use DevForgeAI patterns

        Arrange: Load agent file content
        Act: Check for framework pattern usage in edge cases
        Assert: Uses HALT, AskUserQuestion, structured errors
        """
        # Act
        framework_patterns = {
            'HALT': bool(re.search(r'HALT', agent_content)),
            'AskUserQuestion': bool(re.search(r'AskUserQuestion', agent_content)),
            'structured_error': bool(re.search(r'structured.*error|error.*format', agent_content, re.IGNORECASE))
        }

        used_patterns = sum(1 for used in framework_patterns.values() if used)

        # Assert
        assert used_patterns >= 2, \
            f"Only {used_patterns}/3 framework patterns used (expected ≥2: HALT, AskUserQuestion, structured errors)"
