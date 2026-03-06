"""
Test: AC#2 - Equity Funding Path Includes Dilution, Control, Timeline, and Referral Trigger
Story: STORY-552
Generated: 2026-03-06

Validates that VC and Angel Investment branches each contain all 4 required
elements: dilution explanation, board/control implications, timeline, and
professional referral trigger.
"""
import re
import pytest


def _extract_section(content, heading_pattern):
    """Extract a markdown section by heading pattern (## or ### level)."""
    pattern = re.compile(
        rf'^(##{{1,3}})\s+.*{heading_pattern}.*$',
        re.IGNORECASE | re.MULTILINE
    )
    match = pattern.search(content)
    if not match:
        return ""
    start = match.start()
    # Find next section at same or higher level
    level = len(match.group(1))
    next_section = re.compile(
        rf'^#{{1,{level}}}\s+', re.MULTILINE
    )
    remainder = content[match.end():]
    next_match = next_section.search(remainder)
    if next_match:
        return content[start:match.end() + next_match.start()]
    return content[start:]


class TestVCBranchElements:
    """Verify VC funding branch contains all 4 required elements."""

    def test_should_contain_dilution_explanation_when_vc_branch_loaded(self, guide_content):
        vc_section = _extract_section(guide_content, r'venture\s+capital')
        assert vc_section, "VC / Venture Capital section must exist"
        pattern = re.compile(r'dilution', re.IGNORECASE)
        assert pattern.search(vc_section), (
            "VC branch must include dilution explanation"
        )

    def test_should_contain_board_control_implications_when_vc_branch_loaded(self, guide_content):
        vc_section = _extract_section(guide_content, r'venture\s+capital')
        assert vc_section, "VC / Venture Capital section must exist"
        pattern = re.compile(r'board|control|governance', re.IGNORECASE)
        assert pattern.search(vc_section), (
            "VC branch must include board/control implications"
        )

    def test_should_contain_timeline_when_vc_branch_loaded(self, guide_content):
        vc_section = _extract_section(guide_content, r'venture\s+capital')
        assert vc_section, "VC / Venture Capital section must exist"
        pattern = re.compile(r'timeline|weeks|months', re.IGNORECASE)
        assert pattern.search(vc_section), (
            "VC branch must include funding timeline"
        )

    def test_should_contain_professional_referral_trigger_when_vc_branch_loaded(self, guide_content):
        vc_section = _extract_section(guide_content, r'venture\s+capital')
        assert vc_section, "VC / Venture Capital section must exist"
        pattern = re.compile(r'professional\s+referral|financial\s+advisor|attorney', re.IGNORECASE)
        assert pattern.search(vc_section), (
            "VC branch must include professional referral trigger"
        )


class TestAngelBranchElements:
    """Verify Angel Investment branch contains all 4 required elements."""

    def test_should_contain_dilution_explanation_when_angel_branch_loaded(self, guide_content):
        angel_section = _extract_section(guide_content, r'angel\s+investment')
        assert angel_section, "Angel Investment section must exist"
        pattern = re.compile(r'dilution', re.IGNORECASE)
        assert pattern.search(angel_section), (
            "Angel branch must include dilution explanation"
        )

    def test_should_contain_board_control_implications_when_angel_branch_loaded(self, guide_content):
        angel_section = _extract_section(guide_content, r'angel\s+investment')
        assert angel_section, "Angel Investment section must exist"
        pattern = re.compile(r'board|control|governance', re.IGNORECASE)
        assert pattern.search(angel_section), (
            "Angel branch must include board/control implications"
        )

    def test_should_contain_timeline_when_angel_branch_loaded(self, guide_content):
        angel_section = _extract_section(guide_content, r'angel\s+investment')
        assert angel_section, "Angel Investment section must exist"
        pattern = re.compile(r'timeline|weeks|months', re.IGNORECASE)
        assert pattern.search(angel_section), (
            "Angel branch must include funding timeline"
        )

    def test_should_contain_professional_referral_trigger_when_angel_branch_loaded(self, guide_content):
        angel_section = _extract_section(guide_content, r'angel\s+investment')
        assert angel_section, "Angel Investment section must exist"
        pattern = re.compile(r'professional\s+referral|financial\s+advisor|attorney', re.IGNORECASE)
        assert pattern.search(angel_section), (
            "Angel branch must include professional referral trigger"
        )
