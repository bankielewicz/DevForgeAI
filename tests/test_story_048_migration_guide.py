"""
Test Suite: STORY-048 AC-3 - MIGRATION-GUIDE.md Created

Tests validate that MIGRATION-GUIDE.md exists and provides comprehensive
migration instructions for existing users.
"""

import re
from pathlib import Path

import pytest


class TestMigrationGuideStructure:
    """Tests for MIGRATION-GUIDE.md structure and required content."""

    @pytest.fixture
    def migration_path(self):
        """Return path to MIGRATION-GUIDE.md"""
        # Try multiple possible locations
        candidates = [
            Path("MIGRATION-GUIDE.md"),
            Path("docs/MIGRATION-GUIDE.md"),
            Path("migration/MIGRATION-GUIDE.md"),
        ]
        for path in candidates:
            if path.exists():
                return path
        return candidates[0]  # Return first option for error message

    @pytest.fixture
    def migration_content(self, migration_path):
        """Load MIGRATION-GUIDE.md content"""
        if not migration_path.exists():
            pytest.skip(f"MIGRATION-GUIDE.md not found at {migration_path}")
        return migration_path.read_text()

    # AC-3 Tests

    def test_migration_file_exists(self, migration_path):
        """Test: File exists (at root or docs/)"""
        # Assert
        assert migration_path.exists(), \
            f"MIGRATION-GUIDE.md must exist at {migration_path}"

    def test_migration_has_workflow_section(self, migration_content):
        """Test: Contains migration workflow section"""
        # Act & Assert
        assert re.search(r'[Ww]orkflow|[Ss]tep|[Pp]rocess', migration_content), \
            "MIGRATION-GUIDE.md should describe migration workflow"

    def test_migration_workflow_has_7_steps(self, migration_content):
        """Test: Workflow contains 7 steps"""
        # Arrange: Find workflow section
        workflow_section = migration_content

        # Act: Count steps (numbered or bulleted)
        step_count = 0
        step_count += len(re.findall(r'^\s*\d+\.\s+', workflow_section, re.MULTILINE))
        step_count += len(re.findall(r'####\s+\d+', workflow_section))

        # Alternative: look for specific step keywords
        steps_found = []
        for keyword in ['Backup', 'Pull', 'Run installer', 'Verify', 'Update', 'Test', 'Cleanup']:
            if re.search(re.escape(keyword), migration_content, re.IGNORECASE):
                steps_found.append(keyword)

        # Assert: Must have 7 steps or keywords
        assert len(steps_found) >= 6 or step_count >= 7, \
            f"Migration workflow should have 7 steps (found {len(steps_found)} keywords)"

    def test_migration_mentions_backup(self, migration_content):
        """Test: Step 1 - Backup current installation"""
        # Act & Assert
        assert re.search(r'[Bb]ackup.*\.claude|\.claude.*[Bb]ackup', migration_content), \
            "Migration guide should mention backing up .claude folder"

    def test_migration_mentions_git_pull(self, migration_content):
        """Test: Step 2 - Pull latest DevForgeAI"""
        # Act & Assert
        assert re.search(r'git\s+pull|pull.*latest', migration_content, re.IGNORECASE), \
            "Migration guide should mention 'git pull'"

    def test_migration_mentions_installer(self, migration_content):
        """Test: Step 3 - Run installer"""
        # Act & Assert
        assert re.search(r'python.*install\.py|installer.*--mode=upgrade', migration_content, re.IGNORECASE), \
            "Migration guide should mention running installer"

    def test_migration_mentions_validation(self, migration_content):
        """Test: Step 4 - Verify installation"""
        # Act & Assert
        assert re.search(r'[Vv]alidat|--mode=validate|verify.*install', migration_content, re.IGNORECASE), \
            "Migration guide should mention validation step"

    def test_migration_mentions_workflow_changes(self, migration_content):
        """Test: Workflow changes documented (before vs after)"""
        # Act & Assert
        workflow_changes = re.search(
            r'[Ww]orkflow.*[Cc]hange|before.*after|Old.*[Nn]ew',
            migration_content,
            re.IGNORECASE
        )

        assert workflow_changes or migration_content.count('src/') > 0, \
            "Migration guide should document workflow changes (src/ vs .claude/)"

    def test_migration_has_safety_checklist(self, migration_content):
        """Test: Includes safety checklist"""
        # Act & Assert
        assert re.search(r'[Cc]heckl|[Ss]afety|[Bb]ackup.*verif|[Rr]ollback.*plan', migration_content, re.IGNORECASE), \
            "Migration guide should include safety checklist"

    def test_migration_documents_rollback(self, migration_content):
        """Test: Rollback procedure documented"""
        # Act & Assert
        assert re.search(r'[Rr]ollback|revert|restore.*[Bb]ackup|undo', migration_content, re.IGNORECASE), \
            "Migration guide should document rollback procedure"

    def test_migration_has_troubleshooting(self, migration_content):
        """Test: Troubleshooting migration issues covered"""
        # Act & Assert
        assert re.search(r'[Tt]roubleshoot|[Pp]roblem|[Ii]ssue', migration_content, re.IGNORECASE), \
            "Migration guide should include troubleshooting section"


class TestMigrationGuideSafety:
    """Tests for safety-related content in migration guide."""

    @pytest.fixture
    def migration_content(self):
        """Load MIGRATION-GUIDE.md content"""
        migration_path = Path("MIGRATION-GUIDE.md")
        if not migration_path.exists():
            migration_path = Path("docs/MIGRATION-GUIDE.md")
        if not migration_path.exists():
            pytest.skip("MIGRATION-GUIDE.md not found")
        return migration_path.read_text()

    def test_migration_mentions_backup_verification(self, migration_content):
        """Test: Safety checklist mentions backup verification"""
        # Act & Assert
        assert re.search(
            r'[Bb]ackup.*verif|verif.*[Bb]ackup|check.*[Bb]ackup|test.*[Bb]ackup',
            migration_content,
            re.IGNORECASE
        ), "Safety checklist should mention backup verification"

    def test_migration_mentions_test_after_migration(self, migration_content):
        """Test: Workflow includes testing after migration"""
        # Act & Assert
        assert re.search(
            r'[Tt]est.*migrat|[Tt]est.*chang|[Cc]reate.*[Ss]tory|/dev',
            migration_content,
            re.IGNORECASE
        ), "Migration workflow should include testing step"

    def test_migration_mentions_cleanup(self, migration_content):
        """Test: Cleanup step documented"""
        # Act & Assert
        assert re.search(
            r'[Cc]leanup|remove.*[Bb]ackup|delete.*old',
            migration_content,
            re.IGNORECASE
        ), "Migration guide should mention cleanup step"


class TestMigrationGuideSimulation:
    """Tests for migration simulation and practical aspects."""

    @pytest.fixture
    def migration_content(self):
        """Load MIGRATION-GUIDE.md content"""
        migration_path = Path("MIGRATION-GUIDE.md")
        if not migration_path.exists():
            migration_path = Path("docs/MIGRATION-GUIDE.md")
        if not migration_path.exists():
            pytest.skip("MIGRATION-GUIDE.md not found")
        return migration_path.read_text()

    def test_migration_has_backup_command(self, migration_content):
        """Test: Backup command is documented"""
        # Act & Assert
        assert re.search(
            r'cp\s+-r\s+\.claude|backup|copy.*\.claude',
            migration_content,
            re.IGNORECASE
        ), "Migration guide should show backup command"

    def test_migration_has_installer_upgrade_command(self, migration_content):
        """Test: Installer upgrade command documented"""
        # Act & Assert
        assert re.search(
            r'python.*install\.py.*upgrade|--mode=upgrade',
            migration_content,
            re.IGNORECASE
        ), "Migration guide should show upgrade command"

    def test_migration_clarifies_before_and_after(self, migration_content):
        """Test: Before/after workflow clearly described"""
        # Act: Check for both old and new workflow descriptions
        has_old_workflow = re.search(
            r'before|old|original|manual.*copy|edit.*\.claude',
            migration_content,
            re.IGNORECASE
        )

        has_new_workflow = re.search(
            r'after|new|installer|edit.*src|deploy',
            migration_content,
            re.IGNORECASE
        )

        # Assert
        assert has_old_workflow and has_new_workflow, \
            "Migration guide should clearly show before/after workflow"


class TestMigrationGuideIntegration:
    """Integration tests for migration guide."""

    @pytest.fixture
    def migration_content(self):
        """Load MIGRATION-GUIDE.md content"""
        migration_path = Path("MIGRATION-GUIDE.md")
        if not migration_path.exists():
            migration_path = Path("docs/MIGRATION-GUIDE.md")
        if not migration_path.exists():
            pytest.skip("MIGRATION-GUIDE.md not found")
        return migration_path.read_text()

    def test_migration_is_well_formed_markdown(self, migration_content):
        """Test: MIGRATION-GUIDE.md is well-formed markdown"""
        # Arrange: Count headings
        h1_count = len(re.findall(r'^#\s+', migration_content, re.MULTILINE))
        h2_count = len(re.findall(r'^##\s+', migration_content, re.MULTILINE))

        # Assert
        assert h1_count > 0 or h2_count > 0, \
            "MIGRATION-GUIDE.md should have proper headings"

    def test_migration_has_code_blocks(self, migration_content):
        """Test: Migration guide includes example commands"""
        # Arrange: Look for code blocks
        code_blocks = re.findall(
            r'```(?:bash)?.*?\n(.*?)\n```',
            migration_content,
            re.DOTALL
        )

        # Assert
        assert len(code_blocks) > 0, \
            "Migration guide should include executable command examples"

    def test_migration_commands_have_valid_syntax(self, migration_content):
        """Test: Command examples have valid syntax"""
        # Arrange: Extract code blocks
        code_blocks = re.findall(
            r'```(?:bash)?.*?\n(.*?)\n```',
            migration_content,
            re.DOTALL
        )

        # Act: Check for syntax issues
        issues = []
        for i, block in enumerate(code_blocks):
            # Check for unclosed quotes
            if block.count('"') % 2 != 0:
                issues.append(f"Block {i}: unmatched double quotes")

        # Assert
        assert len(issues) == 0, f"Command syntax issues: {issues}"

    def test_migration_substantial_content(self, migration_content):
        """Test: MIGRATION-GUIDE.md has substantial content"""
        # Assert
        assert len(migration_content) > 1500, \
            "MIGRATION-GUIDE.md should have substantial content (>1500 chars)"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
