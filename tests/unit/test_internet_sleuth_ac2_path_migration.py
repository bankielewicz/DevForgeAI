"""
Unit tests for STORY-035 AC2: Path references updated to DevForgeAI structure

Tests verify all file path references use DevForgeAI conventions:
- devforgeai/context/ (NOT .claude/context/)
- .devforgeai/adrs/ (NOT .claude/adrs/)
- .devforgeai/research/ (NOT devforgeai/specs/research/ or .bmad-core)
- devforgeai/specs/Stories/ (correct)
- devforgeai/specs/Epics/ (correct)
"""

import pytest
import re
from pathlib import Path


@pytest.mark.story_035
@pytest.mark.acceptance_criteria
@pytest.mark.unit
class TestAC2PathMigration:
    """Test suite for AC2: Path references updated to DevForgeAI structure"""

    @pytest.fixture
    def agent_file_path(self):
        """Path to internet-sleuth agent file"""
        return Path(".claude/agents/internet-sleuth.md")

    @pytest.fixture
    def agent_content(self, agent_file_path):
        """Load agent file content"""
        assert agent_file_path.exists(), f"Agent file not found: {agent_file_path}"
        return agent_file_path.read_text()

    def test_no_old_context_path_references(self, agent_content):
        """
        AC2 / COMP-003: No references to old .claude/context/ path

        Arrange: Load agent file content
        Act: Search for old path pattern
        Assert: Zero matches found
        """
        # Act
        old_context_matches = re.findall(r'\.claude/context/', agent_content)

        # Assert
        assert len(old_context_matches) == 0, \
            f"Found {len(old_context_matches)} references to deprecated path '.claude/context/' - must use 'devforgeai/context/'"

    def test_no_old_adrs_path_references(self, agent_content):
        """
        AC2 / COMP-003: No references to old .claude/adrs/ path

        Arrange: Load agent file content
        Act: Search for old path pattern
        Assert: Zero matches found
        """
        # Act
        old_adrs_matches = re.findall(r'\.claude/adrs/', agent_content)

        # Assert
        assert len(old_adrs_matches) == 0, \
            f"Found {len(old_adrs_matches)} references to deprecated path '.claude/adrs/' - must use '.devforgeai/adrs/'"

    def test_no_bmad_core_path_references(self, agent_content):
        """
        AC2 / COMP-003: No references to old .bmad-core/ path

        Arrange: Load agent file content
        Act: Search for old path pattern
        Assert: Zero matches found
        """
        # Act
        bmad_core_matches = re.findall(r'\.bmad-core/', agent_content)

        # Assert
        assert len(bmad_core_matches) == 0, \
            f"Found {len(bmad_core_matches)} references to deprecated path '.bmad-core/' - legacy path must be removed"

    def test_no_old_research_path_references(self, agent_content):
        """
        AC2: No references to old devforgeai/specs/research/ path (use .devforgeai/research/)

        Arrange: Load agent file content
        Act: Search for old research path pattern
        Assert: Zero matches found
        """
        # Act
        old_research_matches = re.findall(r'\devforgeai/specs/research/', agent_content)

        # Assert
        assert len(old_research_matches) == 0, \
            f"Found {len(old_research_matches)} references to deprecated path 'devforgeai/specs/research/' - must use '.devforgeai/research/'"

    def test_uses_new_devforgeai_context_path(self, agent_content):
        """
        AC2 / COMP-003: Must use new devforgeai/context/ path

        Arrange: Load agent file content
        Act: Search for new path pattern
        Assert: At least one match found
        """
        # Act
        new_context_matches = re.findall(r'\devforgeai/context/', agent_content)

        # Assert
        assert len(new_context_matches) > 0, \
            "No references to 'devforgeai/context/' found - agent must document context file location"

    def test_uses_new_devforgeai_adrs_path(self, agent_content):
        """
        AC2 / COMP-003: Must use new .devforgeai/adrs/ path

        Arrange: Load agent file content
        Act: Search for new path pattern
        Assert: At least one match found
        """
        # Act
        new_adrs_matches = re.findall(r'\.devforgeai/adrs/', agent_content)

        # Assert
        assert len(new_adrs_matches) > 0, \
            "No references to '.devforgeai/adrs/' found - agent must document ADR check workflow"

    def test_uses_new_devforgeai_research_path(self, agent_content):
        """
        AC2 / AC6: Must use new .devforgeai/research/ output path

        Arrange: Load agent file content
        Act: Search for new research path pattern
        Assert: At least one match found
        """
        # Act
        new_research_matches = re.findall(r'\.devforgeai/research/', agent_content)

        # Assert
        assert len(new_research_matches) > 0, \
            "No references to '.devforgeai/research/' found - agent must document research output location"

    def test_uses_ai_docs_stories_path_correctly(self, agent_content):
        """
        AC2: Verify devforgeai/specs/Stories/ path present (DevForgeAI standard)

        Arrange: Load agent file content
        Act: Search for stories path pattern
        Assert: At least one match found
        """
        # Act
        stories_matches = re.findall(r'\devforgeai/specs/Stories/', agent_content)

        # Assert
        assert len(stories_matches) > 0, \
            "No references to 'devforgeai/specs/Stories/' found - agent should document story integration"

    def test_uses_ai_docs_epics_path_correctly(self, agent_content):
        """
        AC2: Verify devforgeai/specs/Epics/ path present (DevForgeAI standard)

        Arrange: Load agent file content
        Act: Search for epics path pattern
        Assert: At least one match found
        """
        # Act
        epics_matches = re.findall(r'\devforgeai/specs/Epics/', agent_content)

        # Assert
        assert len(epics_matches) > 0, \
            "No references to 'devforgeai/specs/Epics/' found - agent should document epic integration"

    @pytest.mark.edge_case
    def test_no_mixed_path_conventions(self, agent_content):
        """
        Edge case: Ensure no mixing of old and new path conventions

        Arrange: Load agent file content
        Act: Count old vs new path references
        Assert: Zero old paths, multiple new paths
        """
        # Act
        old_paths = (
            len(re.findall(r'\.claude/context/', agent_content)) +
            len(re.findall(r'\.claude/adrs/', agent_content)) +
            len(re.findall(r'\.bmad-core/', agent_content)) +
            len(re.findall(r'\devforgeai/specs/research/', agent_content))
        )

        new_paths = (
            len(re.findall(r'\devforgeai/context/', agent_content)) +
            len(re.findall(r'\.devforgeai/adrs/', agent_content)) +
            len(re.findall(r'\.devforgeai/research/', agent_content))
        )

        # Assert
        assert old_paths == 0, f"Found {old_paths} old path references - all must be migrated"
        assert new_paths >= 3, f"Found only {new_paths} new path references - expected at least 3 (context, adrs, research)"

    @pytest.mark.edge_case
    def test_path_references_use_correct_format(self, agent_content):
        """
        Edge case: Path references should use consistent format (no trailing slashes in documentation)

        Arrange: Load agent file content
        Act: Extract all .devforgeai/ path references
        Assert: Paths follow consistent format
        """
        # Act
        all_devforgeai_paths = re.findall(r'\.devforgeai/[a-z]+/', agent_content)

        # Assert
        assert len(all_devforgeai_paths) > 0, "No .devforgeai/ paths found"

        # Check valid subdirectories
        valid_subdirs = {'context/', 'adrs/', 'research/', 'qa/', 'deployment/', 'specs/'}
        for path in all_devforgeai_paths:
            subdir = path.replace('.devforgeai/', '')
            assert subdir in valid_subdirs, \
                f"Invalid .devforgeai subdirectory: {subdir} (valid: {valid_subdirs})"

    def test_no_absolute_paths_to_context_files(self, agent_content):
        """
        Best practice: Context file references should use relative paths

        Arrange: Load agent file content
        Act: Search for absolute path patterns
        Assert: No absolute paths to context files
        """
        # Act
        absolute_path_matches = re.findall(r'/home/|/Users/|C:\\|/mnt/', agent_content)

        # Assert
        assert len(absolute_path_matches) == 0, \
            f"Found {len(absolute_path_matches)} absolute paths - use relative paths for portability"

    @pytest.mark.business_rule
    def test_comp_003_all_path_references_migrated(self, agent_content):
        """
        COMP-003: Comprehensive path migration test

        Arrange: Load agent file content
        Act: Count old vs new path references
        Assert: Zero old paths, at least 3 new paths (context, adrs, research)
        """
        # Act
        old_count = (
            len(re.findall(r'\.claude/context/', agent_content)) +
            len(re.findall(r'\.claude/adrs/', agent_content)) +
            len(re.findall(r'\.bmad-core/', agent_content)) +
            len(re.findall(r'\devforgeai/specs/research/', agent_content))
        )

        new_count = (
            len(re.findall(r'\devforgeai/context/', agent_content)) +
            len(re.findall(r'\.devforgeai/adrs/', agent_content)) +
            len(re.findall(r'\.devforgeai/research/', agent_content))
        )

        # Assert
        assert old_count == 0, f"COMP-003 FAILED: {old_count} old path references remain (must be 0)"
        assert new_count >= 3, f"COMP-003 FAILED: Only {new_count} new path references (expected ≥3)"
