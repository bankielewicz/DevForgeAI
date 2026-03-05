"""
Integration Test: STORY-540 - Cross-AC Structural Completeness
Story: STORY-540 - Positioning & Messaging Framework
Phase: Integration (Phase 05)

Validates cross-cutting concerns that span multiple acceptance criteria:
- End-to-end workflow coherence (positioning -> messages -> output -> overwrite)
- Cross-reference consistency between sections
- YAML frontmatter + section headers form valid output template
- Output path referenced consistently across all relevant sections
"""
import os
import re

import pytest

from conftest import PROJECT_ROOT, POSITIONING_STRATEGY_FILE


@pytest.fixture
def content():
    """Load the full positioning-strategy.md content."""
    assert os.path.isfile(POSITIONING_STRATEGY_FILE), (
        f"File not found: {POSITIONING_STRATEGY_FILE}"
    )
    with open(POSITIONING_STRATEGY_FILE, "r", encoding="utf-8") as fh:
        return fh.read()


class TestEndToEndWorkflowCoherence:
    """Verify the document describes a complete workflow from positioning
    statement through key messages to output creation and overwrite."""

    def test_should_contain_all_four_workflow_sections_in_order(self, content):
        """The document must present sections in logical workflow order:
        Positioning Statement -> Key Messages -> Output Creation -> Overwrite."""
        pos_idx = content.find("## Positioning Statement")
        msg_idx = content.find("## Key Messages")
        out_idx = content.find("## Output Creation")
        ovr_idx = content.find("## Overwrite Behavior")

        assert pos_idx != -1, "Missing '## Positioning Statement' section"
        assert msg_idx != -1, "Missing '## Key Messages' section"
        assert out_idx != -1, "Missing '## Output Creation' section"
        assert ovr_idx != -1, "Missing '## Overwrite Behavior' section"

        assert pos_idx < msg_idx < out_idx < ovr_idx, (
            "Sections are not in expected workflow order: "
            "Positioning Statement -> Key Messages -> Output Creation -> Overwrite Behavior"
        )

    def test_should_have_yaml_frontmatter_with_required_fields(self, content):
        """YAML frontmatter must contain title, skill, and version fields."""
        frontmatter_match = re.search(r"^---\n(.*?)\n---", content, re.DOTALL)
        assert frontmatter_match, "Missing YAML frontmatter delimiters (---)"
        fm = frontmatter_match.group(1)
        assert "title:" in fm, "Frontmatter missing 'title' field"
        assert "skill:" in fm, "Frontmatter missing 'skill' field"
        assert "version:" in fm, "Frontmatter missing 'version' field"


class TestCrossReferenceConsistency:
    """Verify that output sections correctly reference elements defined
    in earlier sections (cross-AC integration)."""

    def test_output_sections_reference_positioning_statement(self, content):
        """Output Creation section must reference '## Positioning Statement'
        as a required output section (AC3 references AC1 output)."""
        output_section = content.split("## Output Creation")[1].split("## Overwrite")[0]
        assert "Positioning Statement" in output_section, (
            "Output Creation section does not reference Positioning Statement"
        )

    def test_output_sections_reference_key_messages(self, content):
        """Output Creation section must reference '## Key Messages'
        as a required output section (AC3 references AC2 output)."""
        output_section = content.split("## Output Creation")[1].split("## Overwrite")[0]
        assert "Key Messages" in output_section, (
            "Output Creation section does not reference Key Messages"
        )

    def test_output_path_consistent_across_document(self, content):
        """The output path 'devforgeai/specs/business/marketing/positioning.md'
        must appear in Output Creation section."""
        expected_path = "devforgeai/specs/business/marketing/positioning.md"
        assert expected_path in content, (
            f"Output path '{expected_path}' not found in document"
        )


class TestOutputTemplateValidity:
    """Verify that the documented output template (frontmatter + sections)
    forms a structurally valid Markdown document."""

    def test_example_output_contains_frontmatter_delimiters(self, content):
        """The example output block must show triple-dash YAML frontmatter."""
        # Find the example output section within Output Creation
        output_section = content.split("## Output Creation")[1].split("## Overwrite")[0]
        # Should contain an example with --- delimiters
        assert output_section.count("---") >= 2, (
            "Example output must show YAML frontmatter with --- delimiters"
        )

    def test_example_output_contains_all_three_frontmatter_keys(self, content):
        """Example output frontmatter must document story_id, generated_date, skill."""
        output_section = content.split("## Output Creation")[1].split("## Overwrite")[0]
        assert "story_id" in output_section, "Example missing 'story_id' frontmatter key"
        assert "generated_date" in output_section, "Example missing 'generated_date' key"
        assert "skill" in output_section, "Example missing 'skill' frontmatter key"

    def test_key_messages_rules_align_with_segment_structure(self, content):
        """Key Messages section must document both count rules (3-5) AND
        segment-based organization (cross-subsection coherence)."""
        msg_section = content.split("## Key Messages")[1].split("## Output Creation")[0]
        # Count rules
        assert "3" in msg_section and "5" in msg_section, (
            "Key Messages must document min 3, max 5 message count rules"
        )
        # Segment organization
        assert "segment" in msg_section.lower(), (
            "Key Messages must document segment-based organization"
        )


class TestBusinessRuleCrossReferences:
    """Verify business rules (BR-003, BR-004, BR-005) are documented
    and internally consistent."""

    def test_should_reference_all_three_business_rules(self, content):
        """Document must reference BR-003, BR-004, and BR-005."""
        assert "BR-003" in content, "Missing business rule reference BR-003"
        assert "BR-004" in content, "Missing business rule reference BR-004"
        assert "BR-005" in content, "Missing business rule reference BR-005"

    def test_br003_empty_audience_blocks_all_output(self, content):
        """BR-003 (empty audience) must explicitly state no partial output."""
        msg_section = content.split("## Key Messages")[1].split("## Output Creation")[0]
        assert "partial" in msg_section.lower() or "block" in msg_section.lower(), (
            "BR-003 must document that empty audience blocks output (no partial)"
        )

    def test_br004_truncation_documented_with_limit(self, content):
        """BR-004 (segment truncation) must state the limit of 5."""
        msg_section = content.split("## Key Messages")[1].split("## Output Creation")[0]
        assert "5" in msg_section and "truncat" in msg_section.lower(), (
            "BR-004 must document truncation to 5 segments"
        )

    def test_br005_deduplication_is_case_insensitive(self, content):
        """BR-005 (deduplication) must specify case-insensitive behavior."""
        msg_section = content.split("## Key Messages")[1].split("## Output Creation")[0]
        assert "case-insensitive" in msg_section.lower() or "case insensitive" in msg_section.lower(), (
            "BR-005 must document case-insensitive deduplication"
        )
