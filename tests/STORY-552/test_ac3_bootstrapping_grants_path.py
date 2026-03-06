"""
Test: AC#3 - Bootstrapping and Grants Path Includes Pros/Cons and Grant
             Eligibility Signals Without Referral Trigger
Story: STORY-552
Generated: 2026-03-06

Validates that bootstrapping and grants branches contain pros/cons lists,
grants branch contains eligibility signals, and neither branch contains
a professional referral trigger.
"""
import re
import pytest


def _extract_section(content, heading_pattern):
    """Extract a markdown section by heading pattern."""
    pattern = re.compile(
        rf'^(##{{1,3}})\s+.*{heading_pattern}.*$',
        re.IGNORECASE | re.MULTILINE
    )
    match = pattern.search(content)
    if not match:
        return ""
    start = match.start()
    level = len(match.group(1))
    next_section = re.compile(rf'^#{{1,{level}}}\s+', re.MULTILINE)
    remainder = content[match.end():]
    next_match = next_section.search(remainder)
    if next_match:
        return content[start:match.end() + next_match.start()]
    return content[start:]


class TestBootstrappingProsCons:
    """Verify bootstrapping branch has pros/cons list."""

    def test_should_contain_pros_list_when_bootstrapping_branch_loaded(self, guide_content):
        section = _extract_section(guide_content, r'bootstrapping')
        assert section, "Bootstrapping section must exist"
        pattern = re.compile(r'pros|advantages|benefits', re.IGNORECASE)
        assert pattern.search(section), (
            "Bootstrapping branch must include pros/advantages list"
        )

    def test_should_contain_cons_list_when_bootstrapping_branch_loaded(self, guide_content):
        section = _extract_section(guide_content, r'bootstrapping')
        assert section, "Bootstrapping section must exist"
        pattern = re.compile(r'cons|disadvantages|drawbacks|limitations', re.IGNORECASE)
        assert pattern.search(section), (
            "Bootstrapping branch must include cons/disadvantages list"
        )


class TestGrantsProsCons:
    """Verify grants branch has pros/cons and eligibility signals."""

    def test_should_contain_pros_list_when_grants_branch_loaded(self, guide_content):
        section = _extract_section(guide_content, r'grants')
        assert section, "Grants section must exist"
        pattern = re.compile(r'pros|advantages|benefits', re.IGNORECASE)
        assert pattern.search(section), (
            "Grants branch must include pros/advantages list"
        )

    def test_should_contain_cons_list_when_grants_branch_loaded(self, guide_content):
        section = _extract_section(guide_content, r'grants')
        assert section, "Grants section must exist"
        pattern = re.compile(r'cons|disadvantages|drawbacks|limitations', re.IGNORECASE)
        assert pattern.search(section), (
            "Grants branch must include cons/disadvantages list"
        )

    def test_should_contain_eligibility_signals_when_grants_branch_loaded(self, guide_content):
        section = _extract_section(guide_content, r'grants')
        assert section, "Grants section must exist"
        pattern = re.compile(r'eligibility|eligible|qualify|sector|geography|demographics', re.IGNORECASE)
        assert pattern.search(section), (
            "Grants branch must include grant eligibility signals"
        )


class TestNoReferralTriggerInNonEquityPaths:
    """Verify bootstrapping and grants do NOT have professional referral triggers."""

    def test_should_not_contain_referral_trigger_when_bootstrapping_branch_loaded(self, guide_content):
        section = _extract_section(guide_content, r'bootstrapping')
        assert section, "Bootstrapping section must exist"
        pattern = re.compile(r'professional\s+referral', re.IGNORECASE)
        assert not pattern.search(section), (
            "Bootstrapping branch must NOT include professional referral trigger"
        )

    def test_should_not_contain_referral_trigger_when_grants_branch_loaded(self, guide_content):
        section = _extract_section(guide_content, r'grants')
        assert section, "Grants section must exist"
        pattern = re.compile(r'professional\s+referral', re.IGNORECASE)
        assert not pattern.search(section), (
            "Grants branch must NOT include professional referral trigger"
        )
