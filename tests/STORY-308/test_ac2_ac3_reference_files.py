"""
STORY-308 AC#2 & AC#3: Reference files use correct command name

Tests that Phase 01 preflight and reference files check for 'devforgeai-validate'.
These tests should FAIL before implementation (TDD Red phase).
"""
import pytest
from pathlib import Path


class TestPhasePreflightCliCheck:
    """Test suite for AC#2: Phase 01 preflight checks for correct command."""

    def test_preflight_checks_for_devforgeai_validate_command(self):
        """
        Test: Preflight uses 'command -v devforgeai-validate'
        Given: Phase 01 preflight check is running
        When: The CLI detection step executes
        Then: It checks for 'devforgeai-validate' command (not 'devforgeai')
        """
        # Arrange
        preflight_path = Path(__file__).parents[2] / "src" / "claude" / "skills" / \
            "devforgeai-development" / "references" / "preflight" / "01.0.5-cli-check.md"

        # Act
        content = preflight_path.read_text()

        # Assert
        assert "command -v devforgeai-validate" in content, (
            "Preflight should check for 'command -v devforgeai-validate'"
        )
        # Negative assertion: no bare 'command -v devforgeai' without '-validate'
        lines_with_command_v = [
            line for line in content.split('\n')
            if 'command -v devforgeai' in line and 'devforgeai-validate' not in line
        ]
        assert len(lines_with_command_v) == 0, (
            f"Found incorrect 'command -v devforgeai' without '-validate': {lines_with_command_v}"
        )

    def test_preflight_version_check_uses_devforgeai_validate(self):
        """
        Test: Preflight uses 'devforgeai-validate --version'
        Given: Phase 01 preflight CLI check reference
        When: Version check is performed
        Then: It uses 'devforgeai-validate --version' (not 'devforgeai --version')
        """
        # Arrange
        preflight_path = Path(__file__).parents[2] / "src" / "claude" / "skills" / \
            "devforgeai-development" / "references" / "preflight" / "01.0.5-cli-check.md"

        # Act
        content = preflight_path.read_text()

        # Assert
        assert "devforgeai-validate --version" in content, (
            "Preflight should use 'devforgeai-validate --version'"
        )


class TestReferenceFileConsistency:
    """Test suite for AC#3: All reference files use consistent command name."""

    def test_no_bare_devforgeai_command_in_reference_files(self):
        """
        Test: No reference files use bare 'devforgeai' command
        Given: All reference files that check for CLI existence
        When: They are searched for command patterns
        Then: They use 'devforgeai-validate' consistently
        """
        # Arrange
        skills_path = Path(__file__).parents[2] / "src" / "claude" / "skills"
        reference_files = list(skills_path.rglob("*.md"))

        # Act & Assert
        violations = []
        for ref_file in reference_files:
            content = ref_file.read_text()
            for i, line in enumerate(content.split('\n'), 1):
                # Check for 'devforgeai --' without '-validate'
                if 'devforgeai --' in line and 'devforgeai-validate' not in line:
                    violations.append(f"{ref_file.name}:{i}: {line.strip()}")
                # Check for 'command -v devforgeai' without '-validate'
                if 'command -v devforgeai' in line and 'devforgeai-validate' not in line:
                    violations.append(f"{ref_file.name}:{i}: {line.strip()}")

        assert len(violations) == 0, (
            f"Found {len(violations)} references to bare 'devforgeai' command:\n" +
            "\n".join(violations[:10])  # Show first 10
        )

    def test_cli_check_reference_uses_correct_binary_name(self):
        """
        Test: 01.0.5-cli-check.md uses 'devforgeai-validate' throughout
        Given: The CLI check reference file
        When: All devforgeai command references are examined
        Then: All use 'devforgeai-validate' consistently
        """
        import re
        # Arrange
        cli_check_path = Path(__file__).parents[2] / "src" / "claude" / "skills" / \
            "devforgeai-development" / "references" / "preflight" / "01.0.5-cli-check.md"

        # Act
        content = cli_check_path.read_text()

        # Assert
        # Count correct references (devforgeai-validate as command)
        correct_count = content.count('devforgeai-validate')

        # Count incorrect command references (devforgeai followed by space, --, or end of word)
        # Exclude directory paths like 'devforgeai/specs/' which are valid
        incorrect_patterns = [
            r'devforgeai\s+--',      # devforgeai --version (command with flags)
            r'command -v devforgeai(?!-validate)',  # command -v devforgeai (without -validate)
            r'devforgeai\s+\w+--',    # devforgeai <subcommand> (command usage)
        ]

        incorrect_count = 0
        for pattern in incorrect_patterns:
            incorrect_count += len(re.findall(pattern, content))

        assert incorrect_count == 0, (
            f"Found {incorrect_count} incorrect 'devforgeai' command references "
            f"(should all be 'devforgeai-validate')"
        )
        assert correct_count >= 2, (
            f"Expected at least 2 'devforgeai-validate' references, found {correct_count}"
        )
