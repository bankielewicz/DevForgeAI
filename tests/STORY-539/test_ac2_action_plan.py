"""
Test: AC#2 - 30-Day Launch Action Plan
Story: STORY-539
Generated: 2026-03-04

Tests validate that go-to-market-framework.md contains a 30-day action plan
template with minimum 10 items across 3 time windows, each tagged with roles.
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GTM_FRAMEWORK = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "marketing-business", "references", "go-to-market-framework.md")

VALID_ROLES = ["founder", "marketer", "engineer"]
TIME_WINDOWS = ["Days 1-7", "Days 8-21", "Days 22-30"]


class TestActionPlanSectionExists:
    """AC#2: Output must have '## 30-Day Launch Plan' section."""

    @pytest.fixture
    def framework_content(self):
        with open(GTM_FRAMEWORK, "r") as f:
            return f.read()

    def test_should_have_30_day_launch_plan_section(self, framework_content):
        # Arrange & Act
        has_section = bool(re.search(r"^## 30-Day Launch Plan", framework_content, re.MULTILINE))
        # Assert
        assert has_section, "Missing '## 30-Day Launch Plan' section"


class TestActionPlanItemCount:
    """BR-002: Minimum 10 discrete action items."""

    @pytest.fixture
    def plan_section(self):
        with open(GTM_FRAMEWORK, "r") as f:
            content = f.read()
        sections = re.split(r"^## ", content, flags=re.MULTILINE)
        for section in sections:
            if section.startswith("30-Day Launch Plan"):
                return section
        return ""

    def test_should_contain_minimum_10_action_items(self, plan_section):
        # Arrange & Act
        action_items = re.findall(r"^[\-\*]\s+.+", plan_section, re.MULTILINE)
        # Assert
        assert len(action_items) >= 10, f"Only {len(action_items)} action items found, minimum 10 required"


class TestTimeWindows:
    """AC#2: Items must span 3 time windows."""

    @pytest.fixture
    def plan_section(self):
        with open(GTM_FRAMEWORK, "r") as f:
            content = f.read()
        sections = re.split(r"^## ", content, flags=re.MULTILINE)
        for section in sections:
            if section.startswith("30-Day Launch Plan"):
                return section
        return ""

    @pytest.mark.parametrize("window", TIME_WINDOWS)
    def test_should_contain_time_window(self, plan_section, window):
        # Arrange & Act & Assert
        assert window.lower() in plan_section.lower(), f"Time window '{window}' not found in action plan"

    def test_should_have_all_3_time_windows(self, plan_section):
        # Arrange
        found = 0
        # Act
        for window in TIME_WINDOWS:
            if window.lower() in plan_section.lower():
                found += 1
        # Assert
        assert found == 3, f"Only {found}/3 time windows found"


class TestRoleTags:
    """AC#2: Each action item must be tagged with a responsible role."""

    @pytest.fixture
    def plan_section(self):
        with open(GTM_FRAMEWORK, "r") as f:
            content = f.read()
        sections = re.split(r"^## ", content, flags=re.MULTILINE)
        for section in sections:
            if section.startswith("30-Day Launch Plan"):
                return section
        return ""

    def test_should_have_role_tags_in_action_items(self, plan_section):
        # Arrange
        action_items = re.findall(r"^[\-\*]\s+.+", plan_section, re.MULTILINE)
        # Act
        tagged_count = 0
        for item in action_items:
            for role in VALID_ROLES:
                if role.lower() in item.lower():
                    tagged_count += 1
                    break
        # Assert
        assert tagged_count >= 10, f"Only {tagged_count} items have role tags, all 10+ items need roles"

    @pytest.mark.parametrize("role", VALID_ROLES)
    def test_should_use_valid_role(self, plan_section, role):
        # Arrange & Act & Assert
        assert role.lower() in plan_section.lower(), f"Role '{role}' not found in action plan"
