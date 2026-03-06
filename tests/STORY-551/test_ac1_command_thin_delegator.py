"""
Test: AC#1 - Command File Is a Thin Delegator Under 500 Lines
Story: STORY-551
Generated: 2026-03-05

Verifies the financial-model.md command file exists, is under 500 lines,
delegates to managing-finances skill, and contains no inline projection logic.
"""

import re


class TestCommandFileExists:
    """Verify command file exists at expected path."""

    def test_should_exist_at_src_claude_commands(self, command_file):
        """Command file must exist at src/claude/commands/financial-model.md."""
        assert command_file.exists(), (
            f"Command file not found at {command_file}. "
            "AC#1 requires financial-model.md in src/claude/commands/"
        )


class TestCommandLineCount:
    """Verify command file is under 500 lines (thin delegator constraint)."""

    def test_should_have_fewer_than_500_lines(self, command_lines):
        """Command file must be under 500 lines per BR-002."""
        line_count = len(command_lines)
        assert line_count < 500, (
            f"Command file has {line_count} lines (limit: 500). "
            "BR-002: Command must be a thin invoker."
        )

    def test_should_have_at_least_10_lines(self, command_lines):
        """Command file must have meaningful content (not empty stub)."""
        assert len(command_lines) >= 10, (
            "Command file has fewer than 10 lines. "
            "A valid command needs YAML frontmatter and delegation directives."
        )


class TestCommandDelegation:
    """Verify command delegates to managing-finances skill."""

    def test_should_reference_managing_finances_skill(self, command_content):
        """Command must delegate to managing-finances skill."""
        assert "managing-finances" in command_content.lower(), (
            "Command file does not reference 'managing-finances' skill. "
            "AC#1 requires delegation to managing-finances skill."
        )

    def test_should_contain_skill_invocation_directive(self, command_content):
        """Command must contain a skill invocation pattern."""
        # Match patterns like Skill(command="managing-finances" or
        # "Invoke managing-finances skill" or similar delegation directives
        has_skill_call = re.search(
            r'(?i)(skill\s*\(|invoke\s+.*managing-finances|delegates?\s+to\s+.*managing-finances)',
            command_content
        )
        assert has_skill_call, (
            "Command file lacks a skill invocation directive. "
            "Must explicitly delegate to managing-finances skill."
        )


class TestNoInlineProjectionLogic:
    """Verify command contains no inline projection algorithms."""

    PROJECTION_PATTERNS = [
        r'(?i)def\s+.*projection',
        r'(?i)def\s+.*calculate.*revenue',
        r'(?i)def\s+.*calculate.*cost',
        r'(?i)def\s+.*calculate.*runway',
        r'(?i)for\s+.*month\s+in\s+range',
        r'(?i)revenue\s*[\*\+\-\/]=',
        r'(?i)compound.*interest.*formula',
        r'(?i)net_present_value',
        r'(?i)discount_rate\s*\*',
    ]

    def test_should_not_contain_projection_algorithms(self, command_content):
        """Command must not implement projection logic inline (BR-002)."""
        for pattern in self.PROJECTION_PATTERNS:
            match = re.search(pattern, command_content)
            assert not match, (
                f"Command file contains inline projection logic: '{match.group()}'. "
                "BR-002: No projection algorithms in command file."
            )

    def test_should_not_contain_financial_calculations(self, command_content):
        """Command must not perform financial calculations."""
        calc_patterns = [
            r'(?i)break.?even\s*=',
            r'(?i)margin\s*=\s*\(',
            r'(?i)roi\s*=',
        ]
        for pattern in calc_patterns:
            match = re.search(pattern, command_content)
            assert not match, (
                f"Command contains financial calculation: '{match.group()}'. "
                "Thin delegator must not include financial math."
            )


class TestCommandYAMLFrontmatter:
    """Verify command has proper YAML frontmatter."""

    def test_should_start_with_yaml_frontmatter(self, command_content):
        """Command file must have YAML frontmatter per tech-stack.md."""
        assert command_content.startswith("---"), (
            "Command file must start with YAML frontmatter (---). "
            "Required by tech-stack.md for all slash commands."
        )

    def test_should_have_description_in_frontmatter(self, command_content):
        """Frontmatter must include description field."""
        frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', command_content, re.DOTALL)
        assert frontmatter_match, "Could not parse YAML frontmatter."
        frontmatter = frontmatter_match.group(1)
        assert "description:" in frontmatter.lower(), (
            "YAML frontmatter missing 'description' field."
        )
