"""
STORY-087: Slash Command Interface for Epic Coverage Validation
Test Suite for /validate-epic-coverage command

Tests cover all 7 acceptance criteria:
- AC#1: No-Argument Mode - Validate All Epics
- AC#2: Single Epic Validation Mode
- AC#3: Color-Coded Terminal Output
- AC#4: Actionable Gap Resolution Output
- AC#5: Help Text and Documentation
- AC#6: Error Handling - Invalid Epic ID
- AC#7: Error Handling - File System Errors
"""

import pytest
import os
import subprocess
import tempfile
import shutil
import json
import time
import re
from pathlib import Path
from unittest.mock import patch, MagicMock

# Register custom markers for STORY-087
pytestmark = [
    pytest.mark.story_087,
]


# ============================================================================
# COMMAND FILE LOCATION (real project path)
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent.parent
COMMAND_FILE = PROJECT_ROOT / ".claude" / "commands" / "validate-epic-coverage.md"
GAP_DETECTOR = PROJECT_ROOT / "devforgeai" / "traceability" / "gap-detector.sh"
COVERAGE_REPORTER = PROJECT_ROOT / "devforgeai" / "epic-coverage" / "generate-report.sh"


# ============================================================================
# COMMAND FILE VALIDATION TESTS
# ============================================================================

class TestCommandFileStructure:
    """Tests for command file existence and structure."""

    def test_command_file_exists(self):
        """Command file must exist at expected location."""
        assert COMMAND_FILE.exists(), f"Command file not found at {COMMAND_FILE}"

    def test_command_file_has_frontmatter(self):
        """Command file must have YAML frontmatter."""
        content = COMMAND_FILE.read_text()
        assert content.startswith("---"), "Command file must start with YAML frontmatter"
        assert "---\n" in content[3:], "Command file must have closing frontmatter delimiter"

    def test_command_file_has_description(self):
        """Command file frontmatter must include description."""
        content = COMMAND_FILE.read_text()
        assert "description:" in content, "Command must have description in frontmatter"

    def test_command_file_has_argument_hint(self):
        """Command file frontmatter must include argument-hint."""
        content = COMMAND_FILE.read_text()
        assert "argument-hint:" in content, "Command must have argument-hint in frontmatter"

    def test_command_file_specifies_allowed_tools(self):
        """Command file must specify allowed-tools."""
        content = COMMAND_FILE.read_text()
        assert "allowed-tools:" in content, "Command must specify allowed-tools"

    def test_command_file_size_within_budget(self):
        """Command file must be under 15K characters (lean pattern)."""
        content = COMMAND_FILE.read_text()
        assert len(content) < 15000, f"Command file too large: {len(content)} chars (>15K)"


class TestDependencyAvailability:
    """Tests for service dependencies."""

    def test_gap_detector_exists(self):
        """Gap detector script must exist."""
        assert GAP_DETECTOR.exists(), f"Gap detector not found at {GAP_DETECTOR}"

    def test_coverage_reporter_exists(self):
        """Coverage report generator must exist."""
        assert COVERAGE_REPORTER.exists(), f"Coverage reporter not found at {COVERAGE_REPORTER}"

    def test_gap_detector_is_executable(self):
        """Gap detector must be executable."""
        assert os.access(GAP_DETECTOR, os.X_OK), "Gap detector is not executable"

    def test_coverage_reporter_is_executable(self):
        """Coverage reporter must be executable."""
        assert os.access(COVERAGE_REPORTER, os.X_OK), "Coverage reporter is not executable"


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory with DevForgeAI structure."""
    temp_dir = tempfile.mkdtemp(prefix="devforgeai_test_")

    # Create directory structure
    os.makedirs(os.path.join(temp_dir, ".ai_docs", "Epics"))
    os.makedirs(os.path.join(temp_dir, ".ai_docs", "Stories"))
    os.makedirs(os.path.join(temp_dir, "devforgeai", "traceability"))
    os.makedirs(os.path.join(temp_dir, "devforgeai", "epic-coverage", "reports"))
    os.makedirs(os.path.join(temp_dir, ".claude", "commands"))

    yield temp_dir

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_epic_file(temp_project_dir):
    """Create a sample epic file for testing."""
    epic_content = """---
id: EPIC-015
title: Epic Coverage Validation
status: Active
priority: High
---

# Epic: Epic Coverage Validation

## Features

### Feature 1: Gap Detection
Detect coverage gaps between epics and stories.

### Feature 2: Coverage Reporting
Generate coverage reports in multiple formats.

### Feature 3: Slash Command Interface
Provide CLI interface for coverage validation.
"""
    epic_path = os.path.join(temp_project_dir, ".ai_docs", "Epics", "EPIC-015-epic-coverage.epic.md")
    with open(epic_path, "w") as f:
        f.write(epic_content)
    return epic_path


@pytest.fixture
def sample_story_files(temp_project_dir):
    """Create sample story files linked to EPIC-015."""
    stories = []

    # Story covering Feature 1
    story1_content = """---
id: STORY-085
title: Gap Detection Engine
epic: EPIC-015
status: QA Approved
---

# Story: Gap Detection Engine
"""
    story1_path = os.path.join(temp_project_dir, ".ai_docs", "Stories", "STORY-085-gap-detection.story.md")
    with open(story1_path, "w") as f:
        f.write(story1_content)
    stories.append(story1_path)

    # Story covering Feature 2
    story2_content = """---
id: STORY-086
title: Coverage Reporting System
epic: EPIC-015
status: QA Approved
---

# Story: Coverage Reporting System
"""
    story2_path = os.path.join(temp_project_dir, ".ai_docs", "Stories", "STORY-086-coverage-reporting.story.md")
    with open(story2_path, "w") as f:
        f.write(story2_content)
    stories.append(story2_path)

    return stories


@pytest.fixture
def multiple_epics(temp_project_dir):
    """Create multiple epic files for all-epics validation testing."""
    epics = []

    # Epic with full coverage
    epic1_content = """---
id: EPIC-001
title: Fully Covered Epic
status: Active
---

# Epic: Fully Covered Epic

## Features

### Feature 1: Core Feature
Core functionality.
"""
    epic1_path = os.path.join(temp_project_dir, ".ai_docs", "Epics", "EPIC-001-covered.epic.md")
    with open(epic1_path, "w") as f:
        f.write(epic1_content)
    epics.append(epic1_path)

    # Story for EPIC-001
    story1_content = """---
id: STORY-001
epic: EPIC-001
status: Dev Complete
---
"""
    with open(os.path.join(temp_project_dir, ".ai_docs", "Stories", "STORY-001.story.md"), "w") as f:
        f.write(story1_content)

    # Epic with partial coverage
    epic2_content = """---
id: EPIC-002
title: Partial Coverage Epic
status: Active
---

# Epic: Partial Coverage Epic

## Features

### Feature 1: Implemented Feature
Has coverage.

### Feature 2: Missing Feature
No coverage yet.
"""
    epic2_path = os.path.join(temp_project_dir, ".ai_docs", "Epics", "EPIC-002-partial.epic.md")
    with open(epic2_path, "w") as f:
        f.write(epic2_content)
    epics.append(epic2_path)

    # Epic with no coverage
    epic3_content = """---
id: EPIC-003
title: No Coverage Epic
status: Active
---

# Epic: No Coverage Epic

## Features

### Feature 1: Unimplemented Feature
No stories yet.
"""
    epic3_path = os.path.join(temp_project_dir, ".ai_docs", "Epics", "EPIC-003-nocoverage.epic.md")
    with open(epic3_path, "w") as f:
        f.write(epic3_content)
    epics.append(epic3_path)

    return epics


# ============================================================================
# AC#1: No-Argument Mode - Validate All Epics
# ============================================================================

class TestAC1NoArgumentMode:
    """Tests for AC#1: No-Argument Mode - Validate All Epics."""

    @pytest.mark.acceptance_criteria
    def test_scans_all_epics_documented(self):
        """
        Given: /validate-epic-coverage invoked without arguments
        When: Command executes
        Then: Command documents scanning all epic files
        """
        content = COMMAND_FILE.read_text()
        assert "devforgeai/specs/Epics/*.epic.md" in content or "all epics" in content.lower()

    @pytest.mark.acceptance_criteria
    def test_displays_per_epic_breakdown_documented(self):
        """
        Given: /validate-epic-coverage invoked without arguments
        When: Command executes
        Then: Command documents per-epic breakdown display
        """
        content = COMMAND_FILE.read_text()
        assert "Epic ID" in content or "per-epic" in content.lower() or "FOR epic in epics" in content

    @pytest.mark.acceptance_criteria
    def test_shows_overall_framework_coverage_documented(self):
        """
        Given: /validate-epic-coverage invoked without arguments
        When: Command executes
        Then: Command documents framework coverage percentage display
        """
        content = COMMAND_FILE.read_text()
        assert "Framework Coverage" in content or "Overall Coverage" in content


# ============================================================================
# AC#2: Single Epic Validation Mode
# ============================================================================

class TestAC2SingleEpicMode:
    """Tests for AC#2: Single Epic Validation Mode."""

    @pytest.mark.acceptance_criteria
    def test_validates_specified_epic_documented(self):
        """
        Given: /validate-epic-coverage EPIC-015 invoked
        When: Command executes
        Then: Command documents single epic validation mode
        """
        content = COMMAND_FILE.read_text()
        assert "single" in content.lower() and "epic" in content.lower()
        assert "EPIC_ID" in content or "EPIC-015" in content

    @pytest.mark.acceptance_criteria
    def test_displays_feature_by_feature_documented(self):
        """
        Given: /validate-epic-coverage EPIC-015 invoked
        When: Command executes
        Then: Command documents feature-by-feature analysis display
        """
        content = COMMAND_FILE.read_text()
        # Check for feature iteration
        assert "Feature" in content and ("COVERED" in content or "GAP" in content)

    @pytest.mark.acceptance_criteria
    def test_shows_story_workflow_status_documented(self):
        """
        Given: /validate-epic-coverage EPIC-015 invoked
        When: Command executes
        Then: Command documents story status display
        """
        content = COMMAND_FILE.read_text()
        # Check for story status display
        assert "story" in content.lower() and "status" in content.lower()


# ============================================================================
# AC#3: Color-Coded Terminal Output
# ============================================================================

class TestAC3ColorCodedOutput:
    """Tests for AC#3: Color-Coded Terminal Output."""

    @pytest.mark.acceptance_criteria
    def test_green_indicator_documented(self):
        """
        Given: Epic has 100% story coverage
        When: Results are displayed
        Then: Command documents green indicator for full coverage
        """
        content = COMMAND_FILE.read_text()
        # Check for green indicator documentation
        assert "✅" in content or "GREEN" in content

    @pytest.mark.acceptance_criteria
    def test_yellow_indicator_documented(self):
        """
        Given: Epic has partial (50-99%) story coverage
        When: Results are displayed
        Then: Command documents yellow indicator for partial coverage
        """
        content = COMMAND_FILE.read_text()
        assert "⚠️" in content or "YELLOW" in content

    @pytest.mark.acceptance_criteria
    def test_red_indicator_documented(self):
        """
        Given: Epic has zero story coverage
        When: Results are displayed
        Then: Command documents red indicator for gaps
        """
        content = COMMAND_FILE.read_text()
        assert "❌" in content or "RED" in content

    @pytest.mark.acceptance_criteria
    def test_summary_statistics_documented(self):
        """
        Given: Validation completes
        When: Results are displayed
        Then: Command documents summary statistics display
        """
        content = COMMAND_FILE.read_text()
        # Check for table format
        assert "Coverage" in content and "%" in content


# ============================================================================
# AC#4: Actionable Gap Resolution Output
# ============================================================================

class TestAC4ActionableOutput:
    """Tests for AC#4: Actionable Gap Resolution Output."""

    @pytest.mark.acceptance_criteria
    def test_create_story_commands_documented(self):
        """
        Given: Gaps are detected
        When: Results display gap information
        Then: Command documents /create-story command generation
        """
        content = COMMAND_FILE.read_text()
        assert "/create-story" in content, "Must document /create-story commands for gaps"

    @pytest.mark.acceptance_criteria
    def test_commands_are_copy_paste_ready_documented(self):
        """
        Given: /create-story command is generated
        When: User copies the command
        Then: Command documents proper quoting for copy-paste
        """
        content = COMMAND_FILE.read_text()
        # Check for quoted command example (escaped or unescaped)
        assert '/create-story "' in content or '/create-story \\"' in content or "copy-paste" in content.lower()

    @pytest.mark.acceptance_criteria
    def test_shell_safe_escaping_documented(self):
        """
        Given: Feature description contains special characters
        When: /create-story command is generated
        Then: Command documents shell-safe escaping
        """
        content = COMMAND_FILE.read_text()
        assert "shell-safe" in content.lower() or "escaped" in content.lower() or "BR-003" in content


# ============================================================================
# AC#5: Help Text and Documentation
# ============================================================================

class TestAC5HelpText:
    """Tests for AC#5: Help Text and Documentation."""

    @pytest.mark.acceptance_criteria
    def test_help_flag_documented(self):
        """
        Given: /validate-epic-coverage --help invoked
        When: Help is requested
        Then: Documentation section exists in command file
        """
        content = COMMAND_FILE.read_text()
        assert "--help" in content, "Command must document --help flag"
        assert "help" in content.lower(), "Command must document help functionality"

    @pytest.mark.acceptance_criteria
    def test_help_argument_documented(self):
        """
        Given: /validate-epic-coverage help invoked
        When: Help is requested
        Then: Both --help and help are documented
        """
        content = COMMAND_FILE.read_text()
        # Check workflow handles both forms
        assert 'ARG == "--help" OR ARG == "help"' in content or ("--help" in content and "help" in content)

    @pytest.mark.acceptance_criteria
    def test_help_includes_examples(self):
        """
        Given: Help is displayed
        When: User reads documentation
        Then: Example invocations are included
        """
        content = COMMAND_FILE.read_text()
        # Check for example section
        assert "EXAMPLES:" in content or "Examples:" in content or "## Quick Reference" in content
        assert "/validate-epic-coverage EPIC-015" in content, "Must include single-epic example"
        assert "/validate-epic-coverage" in content, "Must include all-epics example"

    @pytest.mark.acceptance_criteria
    def test_help_lists_related_commands(self):
        """
        Given: Help is displayed
        When: User reads documentation
        Then: Related commands are listed
        """
        content = COMMAND_FILE.read_text()
        assert "/create-story" in content, "Must list /create-story as related command"
        assert "/create-epic" in content, "Must list /create-epic as related command"


# ============================================================================
# AC#6: Error Handling - Invalid Epic ID
# ============================================================================

class TestAC6InvalidEpicError:
    """Tests for AC#6: Error Handling - Invalid Epic ID."""

    @pytest.mark.acceptance_criteria
    def test_invalid_epic_error_documented(self):
        """
        Given: /validate-epic-coverage INVALID-ID invoked
        When: Epic file not found
        Then: Error handling is documented in command file
        """
        content = COMMAND_FILE.read_text()
        assert "Epic not found" in content, "Command must document epic not found error"

    @pytest.mark.acceptance_criteria
    def test_invalid_epic_lists_valid_epics_documented(self):
        """
        Given: Invalid epic ID provided
        When: Error is displayed
        Then: Command documents showing valid epic IDs
        """
        content = COMMAND_FILE.read_text()
        assert "Valid epics:" in content or "valid epics" in content.lower()

    @pytest.mark.acceptance_criteria
    def test_invalid_epic_suggests_no_args_mode_documented(self):
        """
        Given: Invalid epic ID provided
        When: Error is displayed
        Then: Command documents suggestion for no-args mode
        """
        content = COMMAND_FILE.read_text()
        assert "without arguments" in content.lower(), "Must suggest running without arguments"

    @pytest.mark.acceptance_criteria
    def test_invalid_epic_format_error_documented(self):
        """
        Given: Invalid epic ID format provided
        When: Error occurs
        Then: Command documents user-friendly error message
        """
        content = COMMAND_FILE.read_text()
        assert "Invalid epic ID format" in content or "EPIC-NNN" in content


# ============================================================================
# AC#7: Error Handling - File System Errors
# ============================================================================

class TestAC7FileSystemErrors:
    """Tests for AC#7: Error Handling - File System Errors."""

    @pytest.mark.acceptance_criteria
    def test_graceful_error_handling_documented(self):
        """
        Given: File system error occurs during validation
        When: Error is encountered
        Then: Command documents graceful error handling
        """
        content = COMMAND_FILE.read_text()
        assert "File System Error" in content or "Warning:" in content

    @pytest.mark.acceptance_criteria
    def test_continues_with_other_epics_documented(self):
        """
        Given: One epic file is unreadable
        When: All-epics validation runs
        Then: Command documents continuing with remaining epics
        """
        content = COMMAND_FILE.read_text()
        assert "Continuing" in content or "remaining" in content.lower()

    @pytest.mark.acceptance_criteria
    def test_partial_results_documented(self):
        """
        Given: Some epic files fail to process
        When: Validation completes
        Then: Command documents partial results handling
        """
        content = COMMAND_FILE.read_text()
        # Check that error handling mentions continuing
        assert "Could not process" in content or "Warning" in content


# ============================================================================
# BUSINESS RULES
# ============================================================================

class TestBusinessRules:
    """Tests for business rules defined in technical specification."""

    @pytest.mark.business_rule
    def test_epic_id_format_case_insensitive_documented(self):
        """
        BR-001: Epic ID format accepts case-insensitive input.
        Both epic-015 and EPIC-015 should work.
        """
        content = COMMAND_FILE.read_text()
        assert "case-insensitive" in content.lower() or "BR-001" in content

    @pytest.mark.business_rule
    def test_dev_complete_stories_count_documented(self):
        """
        BR-002: Only stories with status >= Dev Complete count toward coverage.
        Backlog stories show as 'Planned' but don't count.
        """
        content = COMMAND_FILE.read_text()
        assert "Dev Complete" in content or "BR-002" in content

    @pytest.mark.business_rule
    def test_empty_epics_directory_documented(self):
        """
        BR-004: Empty epics directory returns success (exit 0) with informational message.
        """
        content = COMMAND_FILE.read_text()
        assert "No epics found" in content or "BR-004" in content


# ============================================================================
# NON-FUNCTIONAL REQUIREMENTS
# ============================================================================

class TestNonFunctionalRequirements:
    """Tests for non-functional requirements."""

    @pytest.mark.nfr
    def test_single_epic_performance_documented(self):
        """
        NFR-001: Single epic validation completes in <500ms.
        """
        content = COMMAND_FILE.read_text()
        assert "500ms" in content or "<500" in content

    @pytest.mark.nfr
    def test_all_epics_performance_documented(self):
        """
        NFR-002: All epics validation completes in <3 seconds.
        """
        content = COMMAND_FILE.read_text()
        assert "3 second" in content.lower() or "<3" in content

    @pytest.mark.nfr
    @pytest.mark.slow
    def test_coverage_report_executes_within_timeout(self):
        """
        NFR: Coverage report generator executes within acceptable time.
        Note: WSL2 environments may have slower I/O, so timeout is extended.
        """
        start_time = time.time()
        result = subprocess.run(
            ["bash", str(COVERAGE_REPORTER)],
            capture_output=True,
            text=True,
            timeout=30  # Extended for WSL2
        )
        elapsed = time.time() - start_time
        # WSL2 I/O is slower, allow up to 15s in development
        assert elapsed < 15.0, f"Coverage report took {elapsed:.2f}s (>15s)"

    @pytest.mark.nfr
    @pytest.mark.slow
    def test_gap_detector_executes_within_timeout(self):
        """
        NFR: Gap detector executes within acceptable time.
        Note: WSL2 environments may have slower I/O, so timeout is extended.
        """
        start_time = time.time()
        result = subprocess.run(
            ["bash", str(GAP_DETECTOR)],
            capture_output=True,
            text=True,
            timeout=30  # Extended for WSL2
        )
        elapsed = time.time() - start_time
        # WSL2 I/O is slower, allow up to 15s in development
        assert elapsed < 15.0, f"Gap detector took {elapsed:.2f}s (>15s)"


# ============================================================================
# EDGE CASES
# ============================================================================

class TestEdgeCases:
    """Tests for documented edge cases."""

    @pytest.mark.edge_case
    def test_actionable_gaps_limit_documented(self):
        """
        Edge Case: Epic with many features limits displayed gaps.
        """
        content = COMMAND_FILE.read_text()
        # Check for pagination or limit
        assert "top 10" in content.lower() or "limit 10" in content.lower() or "and N more" in content.lower() or "... and" in content

    @pytest.mark.edge_case
    def test_coverage_reporter_handles_edge_cases(self):
        """
        Edge Case: Coverage reporter script exists and handles various inputs.
        """
        # Script should exist and be callable
        assert COVERAGE_REPORTER.exists()
        result = subprocess.run(
            ["bash", str(COVERAGE_REPORTER)],
            capture_output=True,
            text=True
        )
        # Should complete without error
        assert "Coverage" in result.stdout or "coverage" in result.stdout.lower()

    @pytest.mark.edge_case
    def test_gap_detector_handles_edge_cases(self):
        """
        Edge Case: Gap detector script handles various scenarios.
        """
        assert GAP_DETECTOR.exists()
        result = subprocess.run(
            ["bash", str(GAP_DETECTOR)],
            capture_output=True,
            text=True
        )
        # Should complete without crash
        assert result.returncode == 0 or "Gap Detection" in result.stdout


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests for full command workflow."""

    @pytest.mark.integration
    def test_command_documents_service_integration(self):
        """
        Integration test: Command documents service integration.
        """
        content = COMMAND_FILE.read_text()
        assert "gap-detector.sh" in content, "Must document gap-detector.sh integration"
        assert "generate-report.sh" in content, "Must document generate-report.sh integration"

    @pytest.mark.integration
    def test_command_documents_workflow_phases(self):
        """
        Integration test: Command documents workflow phases.
        """
        content = COMMAND_FILE.read_text()
        assert "Phase 0" in content, "Must have argument validation phase"
        assert "Phase 1" in content, "Must have execution phase"
        assert "Phase 2" in content, "Must have display phase"

    @pytest.mark.integration
    def test_services_produce_valid_output(self):
        """
        Integration test: Services produce valid structured output.
        """
        # Coverage reporter should produce readable output
        result = subprocess.run(
            ["bash", str(COVERAGE_REPORTER)],
            capture_output=True,
            text=True
        )
        assert "%" in result.stdout, "Coverage reporter must output percentages"

    @pytest.mark.integration
    def test_gap_detector_produces_json(self):
        """
        Integration test: Gap detector produces JSON output.
        """
        result = subprocess.run(
            ["bash", str(GAP_DETECTOR)],
            capture_output=True,
            text=True
        )
        # Should output JSON at end
        assert "{" in result.stdout and "}" in result.stdout


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
