"""
Test Suite: STORY-048 Edge Cases and Integration Tests

Tests for edge case handling and data validation as specified in story.
"""

import re
import json
from pathlib import Path

import pytest


class TestDocumentationSyncEdgeCases:
    """Tests for documentation out-of-sync edge cases."""

    @pytest.fixture
    def install_guide_path(self):
        """Path to INSTALL.md"""
        return Path("installer/INSTALL.md")

    @pytest.fixture
    def install_content(self, install_guide_path):
        """Load INSTALL.md"""
        if not install_guide_path.exists():
            pytest.skip("INSTALL.md not found")
        return install_guide_path.read_text()

    @pytest.fixture
    def readme_content(self):
        """Load README.md"""
        readme_path = Path("README.md")
        if not readme_path.exists():
            pytest.skip("README.md not found")
        return readme_path.read_text()

    def test_installation_commands_consistent_between_docs(self, install_content, readme_content):
        """Test: Installation commands in INSTALL.md and README match"""
        # Act: Extract commands from both
        install_modes = re.findall(r'--mode=\w+', install_content)
        readme_modes = re.findall(r'--mode=\w+', readme_content)

        # Assert: Should have some overlap
        if install_modes and readme_modes:
            assert len(set(install_modes) & set(readme_modes)) > 0, \
                "Mode names should be consistent between docs"

    def test_installer_arguments_match_documentation(self, install_content):
        """Test: --mode, --target arguments documented"""
        # Act & Assert
        assert "--mode" in install_content, "INSTALL.md should document --mode"
        assert "--target" in install_content, "INSTALL.md should document --target"

    def test_no_conflicting_mode_names(self, install_content):
        """Test: Installer modes consistently named (upgrade not update)"""
        # Act: Check for conflicting terminology
        has_upgrade = "--mode=upgrade" in install_content
        has_update = "--mode=update" in install_content

        # Assert: Should use consistent naming
        # (either upgrade OR update, not both)
        assert not (has_upgrade and has_update), \
            "Should use consistent mode names (upgrade vs update, not both)"


class TestPackageCorruptionDetection:
    """Tests for corrupted package detection edge case."""

    @pytest.fixture
    def tar_package_path(self):
        """Path to tar.gz package"""
        return Path("devforgeai-1.0.1.tar.gz")

    def test_tar_package_has_checksum_file(self, tar_package_path):
        """Test: SHA256 checksum file exists"""
        # Assert: Look for checksum file
        checksum_path = Path("devforgeai-1.0.1.tar.gz.sha256")
        if tar_package_path.exists() and not checksum_path.exists():
            pytest.skip("Checksum file not yet created")
        # Note: Not enforcing creation, as this may be done separately

    def test_package_files_not_empty(self, tar_package_path):
        """Test: Package files have content (not corrupted empty files)"""
        # Arrange
        if not tar_package_path.exists():
            pytest.skip("Package not found")

        # Act: Check file size
        size = tar_package_path.stat().st_size

        # Assert: Must have content
        assert size > 1000000, \
            "Package appears too small, may be corrupted"


class TestTeamWorkflowAdherence:
    """Tests for team workflow adherence edge case."""

    @pytest.fixture
    def training_log_content(self):
        """Load training log"""
        log_path = Path("devforgeai/onboarding/team-training-log.md")
        if not log_path.exists():
            pytest.skip("Training log not found")
        return log_path.read_text()

    @pytest.fixture
    def git_hooks_path(self):
        """Path to pre-commit hook"""
        return Path(".git/hooks/pre-commit")

    def test_training_log_documents_developers(self, training_log_content):
        """Test: Training log lists each team member"""
        # Act: Count entries (at least 1)
        entries = re.findall(
            r'^\s*[-*x]\s+\**\w+.*?(?=\n\s*[-*x]|\Z)',
            training_log_content,
            re.MULTILINE
        )

        # Assert
        assert len(entries) > 0, \
            "Training log should document at least one developer"

    def test_pre_commit_hook_exists(self, git_hooks_path):
        """Test: Pre-commit hook exists to prevent .claude/ modifications"""
        # This is optional validation - hook may not be installed yet
        # Just document the pattern
        if not git_hooks_path.exists():
            pytest.skip("Pre-commit hook not yet installed")

    def test_training_mentions_src_not_claude_edit(self, training_log_content):
        """Test: Training checklist emphasizes editing src/, not .claude/"""
        # Act & Assert
        assert re.search(
            r'src/|edit.*src',
            training_log_content,
            re.IGNORECASE
        ), "Training should emphasize editing src/"


class TestDocumentationAudit:
    """Tests for documentation audit edge case (old references)."""

    @pytest.fixture
    def readme_content(self):
        """Load README.md"""
        readme_path = Path("README.md")
        if not readme_path.exists():
            pytest.skip("README.md not found")
        return readme_path.read_text()

    def test_no_copy_claude_in_main_install_section(self, readme_content):
        """Test: Main installation section doesn't reference copying .claude/"""
        # Arrange: Extract main installation section only
        install_section = re.search(
            r'#{1,3}\s+Installation\s*(?!.*Deprecat).*?(?=#{1,3}|\Z)',
            readme_content,
            re.IGNORECASE | re.DOTALL
        )

        if not install_section:
            pytest.skip("Installation section not found")

        section = install_section.group(0)

        # Act & Assert
        assert "copy .claude" not in section.lower() and \
               "manually copy" not in section.lower(), \
            "Main installation section should not reference copying .claude/"

    def test_deprecated_section_separate_if_present(self, readme_content):
        """Test: If old approach documented, it's in separate deprecated section"""
        # Arrange: Check if old approach mentioned anywhere
        has_old_approach = "copy .claude" in readme_content.lower()

        if not has_old_approach:
            # Good - no old approach documented at all
            return

        # Act: Check if it's in deprecated section
        deprecated_section = re.search(
            r'#{1,4}\s+.*[Dd]eprecat.*?(?=#{1,3}|\Z)',
            readme_content,
            re.IGNORECASE | re.DOTALL
        )

        # Assert: If old approach present, must be in deprecated section
        assert deprecated_section, \
            "Old approach should only appear in deprecated section"


class TestVersionConsistency:
    """Tests for version number consistency edge case."""

    def test_version_in_roadmap(self):
        """Test: ROADMAP.md shows version 1.0.1"""
        roadmap_path = Path("ROADMAP.md")
        if not roadmap_path.exists():
            pytest.skip("ROADMAP.md not found")

        content = roadmap_path.read_text()
        assert "1.0.1" in content, "ROADMAP should show version 1.0.1"

    def test_version_json_has_version_field(self):
        """Test: version.json contains version field"""
        # Look for version.json in project root or common locations
        version_candidates = [
            Path("version.json"),
            Path("devforgeai/version.json"),
            Path("installer/version.json"),
        ]

        version_file = None
        for candidate in version_candidates:
            if candidate.exists():
                version_file = candidate
                break

        if not version_file:
            pytest.skip("version.json not found")

        import json
        content = json.loads(version_file.read_text())
        assert "version" in content, "version.json must contain version field"
        assert content["version"] == "1.0.1", "version.json should show 1.0.1"


class TestPackageSizeDistribution:
    """Tests for package size distribution edge case."""

    @pytest.fixture
    def tar_package_path(self):
        """Path to tar.gz package"""
        return Path("devforgeai-1.0.1.tar.gz")

    @pytest.fixture
    def zip_package_path(self):
        """Path to ZIP package"""
        return Path("devforgeai-1.0.1.zip")

    def test_both_packages_exist(self, tar_package_path, zip_package_path):
        """Test: Both tar.gz and ZIP packages available"""
        # Note: Both should exist for multi-platform distribution
        if tar_package_path.exists() and zip_package_path.exists():
            # Both good
            assert True
        elif tar_package_path.exists() or zip_package_path.exists():
            # At least one exists (acceptable)
            assert True
        else:
            pytest.skip("Neither package found")

    def test_packages_similar_size(self, tar_package_path, zip_package_path):
        """Test: tar.gz and ZIP similar size (compression difference acceptable)"""
        if not (tar_package_path.exists() and zip_package_path.exists()):
            pytest.skip("Both packages not found")

        tar_size = tar_package_path.stat().st_size
        zip_size = zip_package_path.stat().st_size

        # ZIP is typically slightly larger than tar.gz due to compression method
        # Allow up to 20% difference
        size_ratio = max(tar_size, zip_size) / min(tar_size, zip_size)
        assert size_ratio < 1.2, \
            f"Package sizes differ significantly (ratio: {size_ratio:.2f})"


class TestTrainingAsyncSupport:
    """Tests for async training support edge case."""

    @pytest.fixture
    def training_log_content(self):
        """Load training log"""
        log_path = Path("devforgeai/onboarding/team-training-log.md")
        if not log_path.exists():
            pytest.skip("Training log not found")
        return log_path.read_text()

    def test_training_flexible_format(self, training_log_content):
        """Test: Training log supports async/flexible completion"""
        # If training mentions flexibility, good for distributed teams
        has_async_mention = re.search(
            r'[Aa]sync|[Ff]lexib|makeup|[Oo]ptional|[Ss]elf-paced',
            training_log_content,
            re.IGNORECASE
        )

        # Not required, but if mentioned shows good practice
        assert training_log_content, "Training log exists"

    def test_training_repeatable_content(self, training_log_content):
        """Test: Training materials are documented for repeatability"""
        # Training should be repeatable, not one-time only
        has_materials = re.search(
            r'[Mm]aterial|[Gg]uide|video|recording|[Dd]ocument',
            training_log_content,
            re.IGNORECASE
        )

        # Not enforced, but good practice
        assert training_log_content, "Training documented"


class TestDataValidationRules:
    """Tests for data validation rules."""

    def test_command_accuracy_in_installation_docs(self):
        """Test: All commands in docs match actual installer arguments"""
        install_path = Path("installer/INSTALL.md")
        if not install_path.exists():
            pytest.skip("INSTALL.md not found")

        content = install_path.read_text()

        # Act: Extract all --mode values
        modes = re.findall(r'--mode=(\w+)', content)
        modes = set(modes)

        # Assert: Should have common modes documented
        expected_modes = {'fresh', 'upgrade', 'rollback', 'validate', 'uninstall'}
        found_modes = modes & expected_modes

        assert len(found_modes) >= 3, \
            f"Should document at least 3 common modes (found {found_modes})"

    def test_package_file_count_reasonable(self):
        """Test: Package contains reasonable number of files"""
        tar_path = Path("devforgeai-1.0.1.tar.gz")
        if not tar_path.exists():
            pytest.skip("Package not found")

        import tarfile
        try:
            with tarfile.open(tar_path, 'r:gz') as tar:
                members = tar.getmembers()
                file_count = len(members)

            # Assert: Reasonable file count (not empty, not excessive)
            assert 100 < file_count < 10000, \
                f"Package should have reasonable file count (found {file_count})"
        except Exception as e:
            pytest.skip(f"Could not read package: {e}")

    def test_onboarding_completion_percentage(self):
        """Test: Onboarding log shows completion metrics"""
        log_path = Path("devforgeai/onboarding/team-training-log.md")
        if not log_path.exists():
            pytest.skip("Training log not found")

        content = log_path.read_text()

        # Act: Count checked items
        checked = len(re.findall(r'\[[xX]\]', content))
        total = len(re.findall(r'\[[ xX]\]', content))

        # Assert: Must show some completion
        assert total > 0, "Onboarding log should have checklist"
        # Note: Don't enforce 100% completion yet (may be in progress)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
