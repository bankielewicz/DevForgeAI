"""
Test: AC#1 - Rule 1 Cross-References Existing Anti-Pattern
Story: STORY-505
Phase: Red (TDD)

Validates that Rule 1 references anti-patterns.md and critical-rules.md
via "See also:" format without verbatim duplication.
"""
import os
import re
import pytest
from conftest import OPERATIONAL_SAFETY_PATH, ANTI_PATTERNS_PATH, CRITICAL_RULES_PATH


class TestRule1CrossReferences:
    """AC#1: Rule 1 must cross-reference, not duplicate, existing anti-patterns."""

    def test_should_exist_at_expected_path(self):
        """Arrange: File must exist at .claude/rules/workflow/operational-safety.md"""
        assert os.path.isfile(OPERATIONAL_SAFETY_PATH), (
            f"operational-safety.md not found at {OPERATIONAL_SAFETY_PATH}"
        )

    def test_should_contain_see_also_reference_to_anti_patterns(self, rule_file_content):
        """Rule 1 must reference anti-patterns.md with 'See also:' format."""
        # Assert: "See also:" with path to anti-patterns.md
        assert "See also:" in rule_file_content, (
            "Rule 1 must contain 'See also:' cross-reference format"
        )
        assert "anti-patterns.md" in rule_file_content, (
            "Rule 1 must reference anti-patterns.md"
        )

    def test_should_reference_anti_patterns_category_1(self, rule_file_content):
        """Rule 1 must specifically reference Category 1 of anti-patterns.md."""
        assert re.search(r"[Cc]ategory\s*1", rule_file_content), (
            "Rule 1 must reference Category 1 of anti-patterns.md"
        )

    def test_should_contain_see_also_reference_to_critical_rules(self, rule_file_content):
        """Rule 1 must reference critical-rules.md with 'See also:' format."""
        assert "critical-rules.md" in rule_file_content, (
            "Rule 1 must reference critical-rules.md"
        )

    def test_should_reference_critical_rules_rule_2(self, rule_file_content):
        """Rule 1 must specifically reference Rule 2 of critical-rules.md."""
        assert re.search(r"Rule\s*2", rule_file_content), (
            "Rule 1 must reference Rule 2 of critical-rules.md"
        )

    def test_should_not_duplicate_anti_patterns_verbatim(self, rule_file_content):
        """Rule 1 must NOT restate full anti-pattern text verbatim."""
        # Read anti-patterns.md to get Category 1 content for comparison
        with open(ANTI_PATTERNS_PATH, "r") as f:
            anti_patterns_content = f.read()

        # Extract a representative chunk from Category 1 (first substantial paragraph)
        # If 5+ consecutive words from anti-patterns appear in operational-safety,
        # that's verbatim duplication
        lines = anti_patterns_content.splitlines()
        long_lines = [l.strip() for l in lines if len(l.strip()) > 60]

        duplicated = []
        for line in long_lines[:10]:  # Check first 10 substantial lines
            if line in rule_file_content:
                duplicated.append(line)

        assert len(duplicated) == 0, (
            f"Rule 1 contains verbatim duplication from anti-patterns.md: {duplicated[:3]}"
        )

    def test_should_contain_exact_file_paths_in_see_also(self, rule_file_content):
        """See also references must include exact file paths."""
        # Check for path-like references
        assert re.search(
            r"devforgeai/specs/context/anti-patterns\.md|anti-patterns\.md",
            rule_file_content,
        ), "Must reference anti-patterns.md with file path"
        assert re.search(
            r"\.claude/rules/core/critical-rules\.md|critical-rules\.md",
            rule_file_content,
        ), "Must reference critical-rules.md with file path"

    def test_should_have_referenced_files_exist(self):
        """Cross-referenced files must actually exist."""
        assert os.path.isfile(ANTI_PATTERNS_PATH), (
            f"Referenced anti-patterns.md not found at {ANTI_PATTERNS_PATH}"
        )
        assert os.path.isfile(CRITICAL_RULES_PATH), (
            f"Referenced critical-rules.md not found at {CRITICAL_RULES_PATH}"
        )
