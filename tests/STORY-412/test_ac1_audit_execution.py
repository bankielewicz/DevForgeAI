"""
Test: AC#1 - Audit Script Run Against Target Commands
Story: STORY-412
Generated: 2026-02-16

Validates that the audit results file exists and contains results
for all 4 target commands: /ideate, /dev, /qa, /create-epic.
"""
import os
import pytest

AUDIT_RESULTS_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..",
    "devforgeai", "specs", "analysis", "command-hybrid-audit-results.md"
)

TARGET_COMMANDS = ["/ideate", "/dev", "/qa", "/create-epic"]


class TestAuditExecution:
    """AC#1: Audit script run against target commands."""

    def test_should_create_audit_results_file_when_audit_executed(self):
        """Arrange: Audit has been executed.
        Act: Check for results file.
        Assert: File exists at expected path."""
        assert os.path.isfile(AUDIT_RESULTS_PATH), (
            f"Audit results file not found at {AUDIT_RESULTS_PATH}"
        )

    def test_should_contain_ideate_command_when_audit_executed(self):
        """Assert /ideate command is included in audit results."""
        with open(AUDIT_RESULTS_PATH, "r") as f:
            content = f.read()
        assert "/ideate" in content, "Audit results missing /ideate command"

    def test_should_contain_dev_command_when_audit_executed(self):
        """Assert /dev command is included in audit results."""
        with open(AUDIT_RESULTS_PATH, "r") as f:
            content = f.read()
        assert "/dev" in content, "Audit results missing /dev command"

    def test_should_contain_qa_command_when_audit_executed(self):
        """Assert /qa command is included in audit results."""
        with open(AUDIT_RESULTS_PATH, "r") as f:
            content = f.read()
        assert "/qa" in content, "Audit results missing /qa command"

    def test_should_contain_create_epic_command_when_audit_executed(self):
        """Assert /create-epic command is included in audit results."""
        with open(AUDIT_RESULTS_PATH, "r") as f:
            content = f.read()
        assert "/create-epic" in content, "Audit results missing /create-epic command"

    def test_should_audit_all_four_target_commands_when_executed(self):
        """Assert all 4 target commands appear in audit results."""
        with open(AUDIT_RESULTS_PATH, "r") as f:
            content = f.read()
        missing = [cmd for cmd in TARGET_COMMANDS if cmd not in content]
        assert not missing, f"Audit results missing commands: {missing}"
