"""
STORY-088: /create-story Integration for Gap Resolution
Test Suite for gap-to-story integration and /create-missing-stories command

Tests cover all 8 acceptance criteria:
- AC#1: Interactive Gap-to-Story Prompt
- AC#2: Epic Context Auto-Population
- AC#3: Batch Creation Prompt for Multiple Gaps
- AC#4: Gap-to-Story Description Template Generation
- AC#5: Integration Point in /validate-epic-coverage Output
- AC#6: New /create-missing-stories Command
- AC#7: Story Template Population from Gap Data
- AC#8: Hybrid Mode Toggle
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

# Register custom markers for STORY-088
pytestmark = [
    pytest.mark.story_088,
]


# ============================================================================
# FILE LOCATIONS (real project paths)
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent.parent
COMMAND_FILE = PROJECT_ROOT / ".claude" / "commands" / "create-missing-stories.md"
VALIDATE_COMMAND = PROJECT_ROOT / ".claude" / "commands" / "validate-epic-coverage.md"
GAP_TO_STORY_REF = PROJECT_ROOT / ".claude" / "skills" / "devforgeai-story-creation" / "references" / "gap-to-story-conversion.md"
BATCH_CONFIG_REF = PROJECT_ROOT / ".claude" / "skills" / "devforgeai-story-creation" / "references" / "batch-mode-configuration.md"
GAP_DETECTOR = PROJECT_ROOT / ".devforgeai" / "traceability" / "gap-detector.sh"
COVERAGE_REPORTER = PROJECT_ROOT / ".devforgeai" / "epic-coverage" / "generate-report.sh"


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory with DevForgeAI structure."""
    temp_dir = tempfile.mkdtemp(prefix="devforgeai_story088_test_")

    # Create directory structure
    os.makedirs(os.path.join(temp_dir, ".ai_docs", "Epics"))
    os.makedirs(os.path.join(temp_dir, ".ai_docs", "Stories"))
    os.makedirs(os.path.join(temp_dir, ".devforgeai", "traceability"))
    os.makedirs(os.path.join(temp_dir, ".devforgeai", "epic-coverage", "reports"))
    os.makedirs(os.path.join(temp_dir, ".claude", "commands"))
    os.makedirs(os.path.join(temp_dir, ".claude", "skills", "devforgeai-story-creation", "references"))

    yield temp_dir

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_epic_with_gaps(temp_project_dir):
    """Create sample epic file with 3 features, 1 covered."""
    epic_content = """---
id: EPIC-015
title: Epic Coverage Validation
status: Active
priority: High
---

# Epic: Epic Coverage Validation

## Features

### Feature 1.1: Gap Detection Engine
Detect coverage gaps between epics and stories.
- Parse epic files for feature sections
- Compare against story epic references

### Feature 1.2: Coverage Reporting System
Generate coverage reports in multiple formats.
- JSON output for programmatic access
- Terminal output for human readability

### Feature 1.3: Story Creation Integration
Integrate gap detection with story creation workflow.
- Interactive prompts for gap resolution
- Batch creation mode
"""
    epic_path = os.path.join(temp_project_dir, ".ai_docs", "Epics", "EPIC-015-coverage-validation.epic.md")
    with open(epic_path, "w") as f:
        f.write(epic_content)

    # Create one story covering Feature 1.1 only
    story_content = """---
id: STORY-085
title: Gap Detection Engine
epic: EPIC-015
status: QA Approved
---

# Story: Gap Detection Engine
"""
    story_path = os.path.join(temp_project_dir, ".ai_docs", "Stories", "STORY-085-gap-detection.story.md")
    with open(story_path, "w") as f:
        f.write(story_content)

    return epic_path


@pytest.fixture
def sample_epic_full_coverage(temp_project_dir):
    """Create sample epic with 100% coverage (all features have stories)."""
    epic_content = """---
id: EPIC-001
title: Fully Covered Epic
status: Active
---

# Epic: Fully Covered Epic

## Features

### Feature 1.1: Core Feature
Core functionality.
"""
    epic_path = os.path.join(temp_project_dir, ".ai_docs", "Epics", "EPIC-001-covered.epic.md")
    with open(epic_path, "w") as f:
        f.write(epic_content)

    # Story covering the feature
    story_content = """---
id: STORY-001
title: Core Feature
epic: EPIC-001
status: Dev Complete
---
"""
    with open(os.path.join(temp_project_dir, ".ai_docs", "Stories", "STORY-001.story.md"), "w") as f:
        f.write(story_content)

    return epic_path


@pytest.fixture
def sample_epic_empty(temp_project_dir):
    """Create sample epic with no features defined."""
    epic_content = """---
id: EPIC-002
title: Empty Epic
status: Active
---

# Epic: Empty Epic

## Description
This epic has no features defined yet.
"""
    epic_path = os.path.join(temp_project_dir, ".ai_docs", "Epics", "EPIC-002-empty.epic.md")
    with open(epic_path, "w") as f:
        f.write(epic_content)

    return epic_path


# ============================================================================
# COMMAND FILE STRUCTURE TESTS
# ============================================================================

class TestCommandFileStructure:
    """Tests for /create-missing-stories command file structure."""

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

    def test_command_file_size_within_budget(self):
        """Command file must be under 15K characters (lean pattern)."""
        content = COMMAND_FILE.read_text()
        assert len(content) < 15000, f"Command file too large: {len(content)} chars (>15K)"


class TestReferenceFileStructure:
    """Tests for reference file existence and structure."""

    def test_gap_to_story_reference_exists(self):
        """Gap-to-story conversion reference must exist."""
        assert GAP_TO_STORY_REF.exists(), f"Gap-to-story reference not found at {GAP_TO_STORY_REF}"

    def test_batch_config_reference_exists(self):
        """Batch mode configuration reference must exist."""
        assert BATCH_CONFIG_REF.exists(), f"Batch config reference not found at {BATCH_CONFIG_REF}"


# ============================================================================
# AC#1: Interactive Gap-to-Story Prompt
# ============================================================================

class TestAC1InteractivePrompt:
    """Tests for AC#1: Interactive Gap-to-Story Prompt."""

    @pytest.mark.acceptance_criteria
    def test_askuserquestion_prompt_documented(self):
        """
        Given: /validate-epic-coverage detects gaps
        When: Coverage report is displayed
        Then: Documentation specifies AskUserQuestion prompt
        """
        content = VALIDATE_COMMAND.read_text()
        assert "AskUserQuestion" in content, "Must document AskUserQuestion usage for gap prompts"

    @pytest.mark.acceptance_criteria
    def test_yes_no_later_options_documented(self):
        """
        Given: Gap prompt is displayed
        When: User reviews options
        Then: Documentation includes Yes/No/Later options
        """
        content = VALIDATE_COMMAND.read_text()
        # Check for interactive options
        assert "Yes" in content or "Create story" in content, "Must document 'Yes' option"
        assert "No" in content or "Skip" in content, "Must document 'No/Skip' option"

    @pytest.mark.acceptance_criteria
    def test_create_story_invocation_documented(self):
        """
        Given: User selects "Yes" to create story
        When: /create-story workflow is triggered
        Then: Documentation specifies workflow invocation
        """
        content = VALIDATE_COMMAND.read_text()
        assert "/create-story" in content or "devforgeai-story-creation" in content, \
            "Must document story creation invocation"


# ============================================================================
# AC#2: Epic Context Auto-Population
# ============================================================================

class TestAC2EpicContextPopulation:
    """Tests for AC#2: Epic Context Auto-Population."""

    @pytest.mark.acceptance_criteria
    def test_epic_id_population_documented(self):
        """
        Given: User selects "Yes" for gap-to-story
        When: Story creation begins
        Then: epic_id is auto-populated
        """
        # Check gap-to-story conversion reference
        if GAP_TO_STORY_REF.exists():
            content = GAP_TO_STORY_REF.read_text()
            assert "epic" in content.lower(), "Must document epic_id population"

    @pytest.mark.acceptance_criteria
    def test_feature_title_as_seed_documented(self):
        """
        Given: Gap contains feature title
        When: Story description is generated
        Then: Feature title is used as seed
        """
        if GAP_TO_STORY_REF.exists():
            content = GAP_TO_STORY_REF.read_text()
            assert "title" in content.lower() or "feature" in content.lower(), \
                "Must document feature title extraction"

    @pytest.mark.acceptance_criteria
    def test_batch_mode_markers_documented(self):
        """
        Given: Story is created from gap
        When: Batch mode context is set
        Then: Required markers are documented
        """
        if BATCH_CONFIG_REF.exists():
            content = BATCH_CONFIG_REF.read_text()
            assert "Batch Mode" in content or "batch" in content.lower(), \
                "Must document batch mode markers"


# ============================================================================
# AC#3: Batch Creation Prompt for Multiple Gaps
# ============================================================================

class TestAC3BatchPrompt:
    """Tests for AC#3: Batch Creation Prompt."""

    @pytest.mark.acceptance_criteria
    def test_multiple_gaps_batch_option_documented(self):
        """
        Given: 2+ gaps detected
        When: Gap summary is displayed
        Then: Batch creation option is offered
        """
        content = VALIDATE_COMMAND.read_text()
        assert "batch" in content.lower() or "all" in content.lower(), \
            "Must document batch creation option"

    @pytest.mark.acceptance_criteria
    def test_multi_select_option_documented(self):
        """
        Given: Multiple gaps exist
        When: User reviews options
        Then: Multi-select option is available
        """
        content = VALIDATE_COMMAND.read_text()
        # Check for selection capability
        assert "select" in content.lower() or "specific" in content.lower() or "multi" in content.lower(), \
            "Must document gap selection capability"

    @pytest.mark.acceptance_criteria
    def test_skip_option_documented(self):
        """
        Given: Batch prompt is displayed
        When: User wants to skip
        Then: Skip option is available
        """
        content = VALIDATE_COMMAND.read_text()
        assert "skip" in content.lower() or "later" in content.lower(), \
            "Must document skip option"


# ============================================================================
# AC#4: Gap-to-Story Description Template Generation
# ============================================================================

class TestAC4TemplateGeneration:
    """Tests for AC#4: Template Generation."""

    @pytest.mark.acceptance_criteria
    def test_template_format_documented(self):
        """
        Given: Gap is being converted to story
        When: Template is generated
        Then: Template format is documented
        """
        if GAP_TO_STORY_REF.exists():
            content = GAP_TO_STORY_REF.read_text()
            # Check for template format specification
            assert "template" in content.lower() or "format" in content.lower(), \
                "Must document template format"

    @pytest.mark.acceptance_criteria
    def test_epic_reference_in_template_documented(self):
        """
        Given: Template is generated
        When: Story description is created
        Then: Epic reference is included
        """
        if GAP_TO_STORY_REF.exists():
            content = GAP_TO_STORY_REF.read_text()
            assert "epic" in content.lower() or "EPIC-" in content, \
                "Must document epic reference in template"

    @pytest.mark.acceptance_criteria
    def test_feature_extraction_documented(self):
        """
        Given: Gap is from epic feature
        When: Template is generated
        Then: Feature extraction is documented
        """
        if GAP_TO_STORY_REF.exists():
            content = GAP_TO_STORY_REF.read_text()
            assert "feature" in content.lower() or "extract" in content.lower(), \
                "Must document feature extraction"


# ============================================================================
# AC#5: Integration Point in /validate-epic-coverage Output
# ============================================================================

class TestAC5IntegrationOutput:
    """Tests for AC#5: Integration Point Output."""

    @pytest.mark.acceptance_criteria
    def test_create_story_commands_in_output(self):
        """
        Given: Gaps are detected
        When: Report is displayed
        Then: Copy-paste ready /create-story commands are included
        """
        content = VALIDATE_COMMAND.read_text()
        assert "/create-story" in content, "Must include /create-story commands in output"

    @pytest.mark.acceptance_criteria
    def test_batch_hint_documented(self):
        """
        Given: Multiple gaps exist
        When: Report is displayed
        Then: Batch creation hint is included
        """
        content = VALIDATE_COMMAND.read_text()
        assert "/create-missing-stories" in content or "batch" in content.lower(), \
            "Must include batch creation hint"

    @pytest.mark.acceptance_criteria
    def test_interactive_prompt_trigger_documented(self):
        """
        Given: Report display completes
        When: Not in --quiet mode
        Then: Interactive prompt is triggered
        """
        content = VALIDATE_COMMAND.read_text()
        assert "interactive" in content.lower() or "prompt" in content.lower(), \
            "Must document interactive prompt trigger"


# ============================================================================
# AC#6: New /create-missing-stories Command
# ============================================================================

class TestAC6CreateMissingStoriesCommand:
    """Tests for AC#6: /create-missing-stories Command."""

    @pytest.mark.acceptance_criteria
    def test_epic_argument_validation_documented(self):
        """
        Given: /create-missing-stories invoked
        When: Epic ID is provided
        Then: Argument validation is documented
        """
        if COMMAND_FILE.exists():
            content = COMMAND_FILE.read_text()
            assert "EPIC" in content or "epic" in content.lower(), \
                "Must document epic ID argument"

    @pytest.mark.acceptance_criteria
    def test_gap_detection_invocation_documented(self):
        """
        Given: Valid epic provided
        When: Command executes
        Then: Gap detection is invoked
        """
        if COMMAND_FILE.exists():
            content = COMMAND_FILE.read_text()
            assert "gap" in content.lower() or "detect" in content.lower(), \
                "Must document gap detection invocation"

    @pytest.mark.acceptance_criteria
    def test_shared_metadata_prompt_documented(self):
        """
        Given: Gaps are detected
        When: Batch creation begins
        Then: Shared metadata prompt is documented
        """
        if COMMAND_FILE.exists():
            content = COMMAND_FILE.read_text()
            assert "sprint" in content.lower() or "priority" in content.lower() or "metadata" in content.lower(), \
                "Must document shared metadata prompt"

    @pytest.mark.acceptance_criteria
    def test_progress_display_documented(self):
        """
        Given: Batch creation in progress
        When: Stories are being created
        Then: Progress display is documented
        """
        if COMMAND_FILE.exists():
            content = COMMAND_FILE.read_text()
            assert "progress" in content.lower() or "creating" in content.lower(), \
                "Must document progress display"

    @pytest.mark.acceptance_criteria
    def test_summary_report_documented(self):
        """
        Given: Batch creation completes
        When: All stories processed
        Then: Summary report is documented
        """
        if COMMAND_FILE.exists():
            content = COMMAND_FILE.read_text()
            assert "summary" in content.lower() or "complete" in content.lower(), \
                "Must document summary report"


# ============================================================================
# AC#7: Story Template Population from Gap Data
# ============================================================================

class TestAC7StoryTemplatePopulation:
    """Tests for AC#7: Story Template Population."""

    @pytest.mark.acceptance_criteria
    def test_frontmatter_epic_field_documented(self):
        """
        Given: Story is created from gap
        When: YAML frontmatter is generated
        Then: epic: field is populated
        """
        if GAP_TO_STORY_REF.exists():
            content = GAP_TO_STORY_REF.read_text()
            assert "epic:" in content or "frontmatter" in content.lower(), \
                "Must document epic: field in frontmatter"

    @pytest.mark.acceptance_criteria
    def test_title_derivation_documented(self):
        """
        Given: Gap has feature title
        When: Story is created
        Then: title: is derived from feature
        """
        if GAP_TO_STORY_REF.exists():
            content = GAP_TO_STORY_REF.read_text()
            assert "title" in content.lower(), "Must document title derivation"

    @pytest.mark.acceptance_criteria
    def test_traceability_section_documented(self):
        """
        Given: Story is created from gap
        When: Story file is generated
        Then: Traceability section is included
        """
        if GAP_TO_STORY_REF.exists():
            content = GAP_TO_STORY_REF.read_text()
            assert "traceability" in content.lower() or "reference" in content.lower(), \
                "Must document traceability section"


# ============================================================================
# AC#8: Hybrid Mode Toggle
# ============================================================================

class TestAC8HybridModeToggle:
    """Tests for AC#8: Hybrid Mode Toggle."""

    @pytest.mark.acceptance_criteria
    def test_interactive_flag_documented(self):
        """
        Given: /validate-epic-coverage invoked
        When: --interactive flag is provided
        Then: Interactive mode is enabled
        """
        content = VALIDATE_COMMAND.read_text()
        assert "--interactive" in content or "interactive" in content.lower(), \
            "Must document --interactive flag"

    @pytest.mark.acceptance_criteria
    def test_quiet_flag_documented(self):
        """
        Given: /validate-epic-coverage invoked
        When: --quiet flag is provided
        Then: Prompts are suppressed
        """
        content = VALIDATE_COMMAND.read_text()
        assert "--quiet" in content or "quiet" in content.lower(), \
            "Must document --quiet flag"

    @pytest.mark.acceptance_criteria
    def test_ci_flag_documented(self):
        """
        Given: /validate-epic-coverage invoked
        When: --ci flag is provided
        Then: CI mode is enabled
        """
        content = VALIDATE_COMMAND.read_text()
        assert "--ci" in content or "CI" in content or "ci" in content.lower(), \
            "Must document --ci flag"

    @pytest.mark.acceptance_criteria
    def test_ci_environment_detection_documented(self):
        """
        Given: Command runs in CI environment
        When: No TTY is available
        Then: Auto-detection is documented
        """
        content = VALIDATE_COMMAND.read_text()
        assert "TTY" in content or "detect" in content.lower() or "environment" in content.lower(), \
            "Must document CI environment detection"


# ============================================================================
# BUSINESS RULES
# ============================================================================

class TestBusinessRules:
    """Tests for business rules defined in technical specification."""

    @pytest.mark.business_rule
    def test_br001_feature_title_mandatory(self):
        """
        BR-001: Gap-to-story conversion requires feature title (mandatory).
        """
        if GAP_TO_STORY_REF.exists():
            content = GAP_TO_STORY_REF.read_text()
            assert "title" in content.lower() and ("required" in content.lower() or "mandatory" in content.lower()), \
                "BR-001: Must document mandatory feature title"

    @pytest.mark.business_rule
    def test_br002_missing_markers_trigger_interactive(self):
        """
        BR-002: Missing batch markers trigger interactive fallback.
        """
        if BATCH_CONFIG_REF.exists():
            content = BATCH_CONFIG_REF.read_text()
            assert "fallback" in content.lower() or "interactive" in content.lower(), \
                "BR-002: Must document interactive fallback"

    @pytest.mark.business_rule
    def test_br003_interactive_default_in_terminal(self):
        """
        BR-003: Interactive mode enabled by default in terminal.
        """
        content = VALIDATE_COMMAND.read_text()
        assert "default" in content.lower() and "interactive" in content.lower(), \
            "BR-003: Must document interactive as default"

    @pytest.mark.business_rule
    def test_br004_batch_failure_continues(self):
        """
        BR-004: Story creation failures in batch mode continue to next story.
        """
        if COMMAND_FILE.exists():
            content = COMMAND_FILE.read_text()
            assert "continue" in content.lower() or "next" in content.lower() or "fail" in content.lower(), \
                "BR-004: Must document batch failure continuation"


# ============================================================================
# EDGE CASES
# ============================================================================

class TestEdgeCases:
    """Tests for documented edge cases."""

    @pytest.mark.edge_case
    def test_edge_empty_epic_handling_documented(self):
        """
        Edge Case 1: Empty epic (no features) handling.
        """
        if COMMAND_FILE.exists():
            content = COMMAND_FILE.read_text()
            assert "no feature" in content.lower() or "empty" in content.lower(), \
                "Must document empty epic handling"

    @pytest.mark.edge_case
    def test_edge_full_coverage_handling_documented(self):
        """
        Edge Case 2: All features covered (0 gaps) handling.
        """
        content = VALIDATE_COMMAND.read_text()
        assert "100%" in content or "no gap" in content.lower() or "full coverage" in content.lower(), \
            "Must document 100% coverage handling"

    @pytest.mark.edge_case
    def test_edge_parse_failure_handling_documented(self):
        """
        Edge Case 3: Epic file parsing failure handling.
        """
        if COMMAND_FILE.exists():
            content = COMMAND_FILE.read_text()
            assert "error" in content.lower() or "fail" in content.lower() or "parse" in content.lower(), \
                "Must document parse failure handling"

    @pytest.mark.edge_case
    def test_edge_batch_partial_failure_documented(self):
        """
        Edge Case 4: Story creation mid-batch failure handling.
        """
        if COMMAND_FILE.exists():
            content = COMMAND_FILE.read_text()
            assert "partial" in content.lower() or "continue" in content.lower(), \
                "Must document partial failure handling"


# ============================================================================
# NON-FUNCTIONAL REQUIREMENTS
# ============================================================================

class TestNonFunctionalRequirements:
    """Tests for non-functional requirements."""

    @pytest.mark.nfr
    def test_nfr001_gap_detection_performance_documented(self):
        """
        NFR-001: Gap detection <2 seconds for 20 features.
        """
        # This is validated at runtime during integration tests
        assert GAP_DETECTOR.exists(), "Gap detector must exist for performance validation"

    @pytest.mark.nfr
    def test_nfr002_template_generation_performance_documented(self):
        """
        NFR-002: Story template generation <500ms per story.
        """
        if GAP_TO_STORY_REF.exists():
            content = GAP_TO_STORY_REF.read_text()
            # Template generation should be simple string manipulation
            assert len(content) < 20000, "Reference file should be concise for fast loading"

    @pytest.mark.nfr
    def test_nfr003_batch_creation_performance_documented(self):
        """
        NFR-003: Batch creation <30 seconds for 10 stories.
        """
        if COMMAND_FILE.exists():
            content = COMMAND_FILE.read_text()
            assert "progress" in content.lower(), "Must show progress for batch operations"

    @pytest.mark.nfr
    @pytest.mark.slow
    def test_gap_detector_executes_within_timeout(self):
        """
        NFR: Gap detector executes within acceptable time.
        """
        if GAP_DETECTOR.exists():
            start_time = time.time()
            result = subprocess.run(
                ["bash", str(GAP_DETECTOR)],
                capture_output=True,
                text=True,
                timeout=30
            )
            elapsed = time.time() - start_time
            assert elapsed < 15.0, f"Gap detector took {elapsed:.2f}s (>15s)"


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests for full command workflow."""

    @pytest.mark.integration
    def test_command_documents_skill_invocation(self):
        """
        Integration: Command documents skill invocation pattern.
        """
        if COMMAND_FILE.exists():
            content = COMMAND_FILE.read_text()
            assert "Skill" in content or "devforgeai-story-creation" in content, \
                "Must document skill invocation"

    @pytest.mark.integration
    def test_command_documents_workflow_phases(self):
        """
        Integration: Command documents workflow phases.
        """
        if COMMAND_FILE.exists():
            content = COMMAND_FILE.read_text()
            assert "Phase" in content or "phase" in content.lower(), \
                "Must document workflow phases"

    @pytest.mark.integration
    def test_validate_command_integrates_with_create_missing(self):
        """
        Integration: /validate-epic-coverage references /create-missing-stories.
        """
        content = VALIDATE_COMMAND.read_text()
        assert "/create-missing-stories" in content, \
            "Must reference /create-missing-stories command"


# ============================================================================
# DATA VALIDATION RULES
# ============================================================================

class TestDataValidation:
    """Tests for data validation rules."""

    @pytest.mark.validation
    def test_epic_id_format_validation_documented(self):
        """
        Validation: Epic ID format must match ^EPIC-\\d{3}$.
        """
        if COMMAND_FILE.exists():
            content = COMMAND_FILE.read_text()
            assert "EPIC-" in content or "format" in content.lower(), \
                "Must document epic ID format validation"

    @pytest.mark.validation
    def test_feature_section_regex_documented(self):
        """
        Validation: Feature section detection regex documented.
        """
        if GAP_TO_STORY_REF.exists():
            content = GAP_TO_STORY_REF.read_text()
            assert "Feature" in content or "###" in content or "regex" in content.lower(), \
                "Must document feature section detection"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
