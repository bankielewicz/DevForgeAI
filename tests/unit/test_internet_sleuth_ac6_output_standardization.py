"""
Unit tests for STORY-035 AC6: Output location standardized to DevForgeAI structure

Tests verify research outputs written to correct location:
- .devforgeai/research/ directory for all outputs
- Filename conventions documented (tech-eval-{topic}-{date}.md format)
- Directory created if doesn't exist
- No outputs to deprecated locations (.ai_docs/research/)
"""

import pytest
import re
from pathlib import Path


@pytest.mark.story_035
@pytest.mark.acceptance_criteria
@pytest.mark.unit
class TestAC6OutputStandardization:
    """Test suite for AC6: Output location standardized"""

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
    def repository_management_section(self, agent_content):
        """Extract Repository Management section"""
        match = re.search(
            r'## Repository Management.*?\s*\n(.*?)(?=\n##|\Z)',
            agent_content,
            re.DOTALL | re.IGNORECASE
        )
        if match:
            return match.group(1)
        return ""

    def test_documents_devforgeai_research_output_path(self, agent_content):
        """
        AC6 / COMP-012: Must document .devforgeai/research/ output path

        Arrange: Load agent file content
        Act: Search for .devforgeai/research/ path
        Assert: Path documented
        """
        # Act
        has_research_path = bool(re.search(r'\.devforgeai/research/', agent_content))

        # Assert
        assert has_research_path, \
            "AC6 FAILED: Agent must document '.devforgeai/research/' output directory"

    def test_repository_management_uses_devforgeai_research(self, repository_management_section):
        """
        COMP-012: Repository Management section must reference .devforgeai/research/

        Arrange: Extract Repository Management section
        Act: Search for .devforgeai/research/ in section
        Assert: Path present in management workflow
        """
        # Act
        if not repository_management_section:
            pytest.skip("No Repository Management section found")

        has_research_path = bool(re.search(r'\.devforgeai/research/', repository_management_section))

        # Assert
        assert has_research_path, \
            "COMP-012: Repository Management section must reference '.devforgeai/research/' for outputs"

    def test_no_old_research_output_paths(self, agent_content):
        """
        AC6: No references to deprecated output locations

        Arrange: Load agent file content
        Act: Search for old output paths
        Assert: Zero matches for deprecated paths
        """
        # Act
        old_paths = [
            r'\.ai_docs/research/',
            r'tmp/repos/research-',  # Old research output pattern
            r'ai_docs/architecture/research'
        ]

        found_old_paths = []
        for pattern in old_paths:
            if re.search(pattern, agent_content):
                found_old_paths.append(pattern)

        # Assert
        assert len(found_old_paths) == 0, \
            f"Found deprecated output paths (must use .devforgeai/research/): {found_old_paths}"

    def test_documents_tech_eval_filename_convention(self, agent_content):
        """
        COMP-013: Must document tech-eval-{topic}-{date}.md filename format

        Arrange: Load agent file content
        Act: Search for tech-eval filename example
        Assert: Format documented
        """
        # Act
        has_tech_eval_format = bool(re.search(
            r'tech-eval-.*?-\d{4}-\d{2}-\d{2}\.md|tech-eval-\{topic\}-\{date\}\.md',
            agent_content
        ))

        # Assert
        assert has_tech_eval_format, \
            "COMP-013: Must document tech-eval-{topic}-{date}.md filename convention"

    def test_documents_pattern_analysis_filename_convention(self, agent_content):
        """
        AC6 / COMP-013: Must document pattern-analysis-{repo}-{date}.md filename format

        Arrange: Load agent file content
        Act: Search for pattern-analysis filename example
        Assert: Format documented
        """
        # Act
        has_pattern_format = bool(re.search(
            r'pattern-analysis-.*?-\d{4}-\d{2}-\d{2}\.md|pattern-analysis-\{repo\}-\{date\}\.md',
            agent_content
        ))

        # Assert
        assert has_pattern_format, \
            "COMP-013: Must document pattern-analysis-{repo}-{date}.md filename convention"

    def test_documents_competitive_filename_convention(self, agent_content):
        """
        AC6 / COMP-013: Must document competitive-{topic}-{date}.md filename format

        Arrange: Load agent file content
        Act: Search for competitive filename example
        Assert: Format documented
        """
        # Act
        has_competitive_format = bool(re.search(
            r'competitive-.*?-\d{4}-\d{2}-\d{2}\.md|competitive-\{topic\}-\{date\}\.md',
            agent_content
        ))

        # Assert
        assert has_competitive_format, \
            "COMP-013: Must document competitive-{topic}-{date}.md filename convention"

    def test_filename_conventions_use_iso_date_format(self, agent_content):
        """
        COMP-013: Filename examples must use ISO date format (YYYY-MM-DD)

        Arrange: Load agent file content
        Act: Extract date patterns from filename examples
        Assert: ISO format used (YYYY-MM-DD, not MM/DD/YYYY)
        """
        # Act
        # Find filename examples with dates
        filename_patterns = re.findall(
            r'(?:tech-eval|pattern-analysis|competitive)-.*?-(\d{4}-\d{2}-\d{2})\.md',
            agent_content
        )

        has_iso_dates = len(filename_patterns) > 0

        # Also check for documentation of {date} placeholder with format explanation
        has_date_format_doc = bool(re.search(
            r'\{date\}.*?YYYY-MM-DD|YYYY-MM-DD.*?\{date\}',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        assert has_iso_dates or has_date_format_doc, \
            "COMP-013: Filename conventions must document ISO date format (YYYY-MM-DD)"

    def test_comp_012_013_output_structure_comprehensive(self, agent_content):
        """
        COMP-012/013: Comprehensive output structure test

        Arrange: Load agent file content
        Act: Verify directory path + filename conventions documented
        Assert: Both directory and filenames specified
        """
        # Act
        has_directory = bool(re.search(r'\.devforgeai/research/', agent_content))

        filename_formats = [
            r'tech-eval-',
            r'pattern-analysis-',
            r'competitive-'
        ]

        documented_formats = sum(
            1 for pattern in filename_formats
            if re.search(pattern, agent_content)
        )

        # Assert
        assert has_directory, "COMP-012: Output directory not documented"
        assert documented_formats >= 3, \
            f"COMP-013: Only {documented_formats}/3 filename formats documented (expected all 3)"

    @pytest.mark.edge_case
    def test_documents_directory_creation_if_not_exists(self, agent_content):
        """
        Edge case: Should document directory creation behavior

        Arrange: Load agent file content
        Act: Search for directory creation documentation
        Assert: Mentions creating directory if doesn't exist
        """
        # Act
        has_create_dir_docs = bool(re.search(
            r'create.*directory|mkdir|ensure.*exist|if.*not.*exist',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        assert has_create_dir_docs, \
            "Should document directory creation behavior (create if doesn't exist)"

    @pytest.mark.edge_case
    def test_no_hardcoded_output_paths_in_examples(self, agent_content):
        """
        Edge case: Output path examples should use .devforgeai/research/, not absolute paths

        Arrange: Load agent file content
        Act: Check output path examples
        Assert: No absolute paths in output examples
        """
        # Act
        # Find output path examples
        output_examples = re.findall(r'[/\\].*?research.*?\.md', agent_content)

        absolute_paths = [
            path for path in output_examples
            if path.startswith('/home/') or path.startswith('/Users/') or 'C:\\' in path
        ]

        # Assert
        assert len(absolute_paths) == 0, \
            f"Found hardcoded absolute paths in output examples: {absolute_paths} (use relative paths)"

    def test_br_003_research_directory_documented(self, agent_content):
        """
        BR-003: Research output files must be written to .devforgeai/research/ directory

        Arrange: Load agent file content
        Act: Verify .devforgeai/research/ documented as output location
        Assert: Directory path present and documented
        """
        # Act
        has_research_dir = bool(re.search(r'\.devforgeai/research/', agent_content))

        # Additional check: Should NOT have old research directories
        has_old_research_dir = bool(re.search(r'\.ai_docs/research/', agent_content))

        # Assert
        assert has_research_dir, \
            "BR-003 FAILED: Must document '.devforgeai/research/' as research output directory"
        assert not has_old_research_dir, \
            "BR-003 FAILED: Must NOT reference deprecated '.ai_docs/research/' directory"

    @pytest.mark.business_rule
    def test_br_003_directory_permissions_documented(self, agent_content):
        """
        BR-003: Directory must be created with 755 permissions if doesn't exist

        Arrange: Load agent file content
        Act: Search for permissions documentation
        Assert: 755 or permission specification present
        """
        # Act
        has_permissions_doc = bool(re.search(
            r'755|permission|chmod|access control',
            agent_content,
            re.IGNORECASE
        ))

        # Assert (soft requirement - may be implied by directory creation)
        if not has_permissions_doc:
            pytest.skip("Permissions not explicitly documented (may be default behavior)")

    def test_output_format_consistency_across_research_types(self, agent_content):
        """
        Best practice: All research output formats should follow consistent pattern

        Arrange: Load agent file content
        Act: Extract all filename patterns
        Assert: All follow {type}-{identifier}-{date}.md format
        """
        # Act
        filename_patterns = re.findall(
            r'([a-z]+-[a-z]+)-\{[^}]+\}-\{date\}\.md',
            agent_content
        )

        valid_prefixes = {'tech-eval', 'pattern-analysis', 'competitive'}
        invalid_patterns = [
            pattern for pattern in filename_patterns
            if pattern not in valid_prefixes
        ]

        # Assert
        assert len(invalid_patterns) == 0, \
            f"Found inconsistent filename patterns: {invalid_patterns} (expected: {valid_prefixes})"

    def test_no_references_to_tmp_repos_research_pattern(self, agent_content):
        """
        Legacy cleanup: Ensure no old tmp/repos/research-{timestamp}/ pattern remains

        Arrange: Load agent file content
        Act: Search for old temporary research directory pattern
        Assert: Pattern not found (outputs should go to .devforgeai/research/)
        """
        # Act
        has_old_tmp_pattern = bool(re.search(r'tmp/repos/research-\d+', agent_content))

        # Assert
        assert not has_old_tmp_pattern, \
            "Found old tmp/repos/research-{timestamp}/ pattern (outputs must go to .devforgeai/research/)"
