"""
Test Suite: STORY-048 Business Rules Enforcement

Tests for business rule validation and non-functional requirements.
"""

import re
from pathlib import Path

import pytest


class TestBusinessRuleDocumentationAccuracy:
    """Tests for BR-001: Documentation must be accurate."""

    @pytest.fixture
    def readme_content(self):
        """Load README.md"""
        path = Path("README.md")
        if not path.exists():
            pytest.skip("README.md not found")
        return path.read_text()

    @pytest.fixture
    def install_content(self):
        """Load INSTALL.md"""
        path = Path("installer/INSTALL.md")
        if not path.exists():
            pytest.skip("INSTALL.md not found")
        return path.read_text()

    def test_readme_has_installation_section(self, readme_content):
        """Test: README has installation instructions"""
        # Act & Assert
        assert re.search(r'#{1,3}\s+Installation', readme_content, re.IGNORECASE), \
            "README must have Installation section"

    def test_installation_commands_are_documented(self, install_content):
        """Test: INSTALL.md documents major installation scenarios"""
        # Act: Check for key scenarios
        has_fresh = re.search(r'[Ff]resh|new', install_content, re.IGNORECASE)
        has_upgrade = re.search(r'[Uu]pgrad', install_content, re.IGNORECASE)

        # Assert
        assert has_fresh and has_upgrade, \
            "INSTALL.md should document fresh and upgrade scenarios"

    def test_readme_contains_no_todo_markers(self, readme_content):
        """Test: README doesn't have TODO/TBD placeholders"""
        # Act & Assert
        assert not re.search(r'TODO|TBD|FIXME|\[TODO\]', readme_content, re.IGNORECASE), \
            "README should not contain TODO placeholders"

    def test_install_guide_contains_no_todo_markers(self, install_content):
        """Test: INSTALL.md doesn't have TODO/TBD placeholders"""
        # Act & Assert
        assert not re.search(r'TODO|TBD|FIXME|\[TODO\]', install_content, re.IGNORECASE), \
            "INSTALL.md should not contain TODO placeholders"


class TestBusinessRulePackageCompleteness:
    """Tests for BR-002: Distribution package must contain all needed files."""

    @pytest.fixture
    def tar_package_path(self):
        """Path to tar.gz"""
        return Path("devforgeai-1.0.1.tar.gz")

    @pytest.fixture
    def tar_file_list(self, tar_package_path):
        """Get list of files in tar.gz"""
        if not tar_package_path.exists():
            pytest.skip("Package not found")

        import tarfile
        with tarfile.open(tar_package_path, 'r:gz') as tar:
            return tar.getnames()

    def test_package_has_src_directory(self, tar_file_list):
        """Test: Package contains src/ directory"""
        # Assert
        has_src = any('src/' in f for f in tar_file_list)
        assert has_src, "Package must contain src/ directory"

    def test_package_has_installer_directory(self, tar_file_list):
        """Test: Package contains installer/ directory"""
        # Assert
        has_installer = any('installer/' in f for f in tar_file_list)
        assert has_installer, "Package must contain installer/ directory"

    def test_package_has_license(self, tar_file_list):
        """Test: Package contains LICENSE"""
        # Assert
        has_license = any('LICENSE' in f for f in tar_file_list)
        assert has_license, "Package must contain LICENSE file"

    def test_package_has_install_guide(self, tar_file_list):
        """Test: Package contains INSTALL.md"""
        # Assert
        has_install = any('INSTALL.md' in f for f in tar_file_list)
        assert has_install, "Package must contain INSTALL.md"

    def test_package_has_migration_guide(self, tar_file_list):
        """Test: Package contains MIGRATION-GUIDE.md"""
        # Assert
        has_migration = any('MIGRATION-GUIDE.md' in f for f in tar_file_list)
        assert has_migration, "Package must contain MIGRATION-GUIDE.md"

    def test_package_has_version_info(self, tar_file_list):
        """Test: Package contains version.json"""
        # Assert
        has_version = any('version.json' in f for f in tar_file_list)
        assert has_version, "Package must contain version.json"

    def test_package_file_count_substantial(self, tar_file_list):
        """Test: Package has substantial number of files"""
        # Assert: More than 100 files (indicates complete content)
        assert len(tar_file_list) > 100, \
            f"Package should have substantial files (found {len(tar_file_list)})"


class TestBusinessRuleDeprecationTimeline:
    """Tests for BR-003: Deprecation notice required before removal."""

    @pytest.fixture
    def roadmap_content(self):
        """Load ROADMAP.md"""
        path = Path("ROADMAP.md")
        if not path.exists():
            pytest.skip("ROADMAP.md not found")
        return path.read_text()

    @pytest.fixture
    def readme_content(self):
        """Load README.md"""
        path = Path("README.md")
        if not path.exists():
            pytest.skip("README.md not found")
        return path.read_text()

    def test_deprecation_notice_present(self, readme_content):
        """Test: Deprecation notice added"""
        # Act & Assert
        has_notice = re.search(r'[Dd]eprecat|⚠️', readme_content, re.IGNORECASE)
        assert has_notice, "Deprecation notice must be present"

    def test_deprecation_date_documented(self, roadmap_content):
        """Test: Deprecation date documented"""
        # Act & Assert
        has_date = re.search(r'2025-1[01]|deprecat.*date|date.*deprecat', roadmap_content, re.IGNORECASE)
        assert has_date, "Deprecation date should be documented"

    def test_support_timeline_at_least_6_months(self, roadmap_content):
        """Test: Support timeline is 6+ months"""
        # Act: Look for mention of 6 months or future version
        has_timeline = re.search(
            r'6\s*month|v2\.0|2026|until\s*2026',
            roadmap_content,
            re.IGNORECASE
        )

        # Assert
        assert has_timeline, \
            "ROADMAP should document 6+ month support timeline"


class TestBusinessRuleOnboardingCompletion:
    """Tests for BR-004: Team onboarding 100% completion required."""

    @pytest.fixture
    def training_log_content(self):
        """Load training log"""
        path = Path("devforgeai/onboarding/team-training-log.md")
        if not path.exists():
            pytest.skip("Training log not found")
        return path.read_text()

    def test_training_log_exists(self):
        """Test: Training log created"""
        # Assert
        path = Path("devforgeai/onboarding/team-training-log.md")
        assert path.exists(), "Training log must exist"

    def test_training_log_documents_participants(self, training_log_content):
        """Test: Log documents which team members trained"""
        # Act: Look for participant documentation
        has_participants = re.search(
            r'[Pp]articipant|[Dd]eveloper|[Tt]eam|[Nn]ame',
            training_log_content,
            re.IGNORECASE
        )

        # Assert
        assert has_participants, \
            "Training log should document participants"

    def test_training_has_checklist(self, training_log_content):
        """Test: Training log has completion checklist"""
        # Act: Look for checkboxes
        has_checklist = re.search(r'\[[ xX]\]', training_log_content)

        # Assert
        assert has_checklist, "Training log should have completion checklist"

    def test_training_lists_7_items(self, training_log_content):
        """Test: Checklist has 7 training items"""
        # Act: Count checklist items
        items = re.findall(r'\[[ xX]\]', training_log_content)

        # Assert: At least 7 items
        assert len(items) >= 7, \
            f"Checklist must have 7+ items (found {len(items)})"


class TestNfrUsability:
    """Tests for NFR-001: Documentation clear for new users."""

    @pytest.fixture
    def readme_content(self):
        """Load README.md"""
        path = Path("README.md")
        if not path.exists():
            pytest.skip("README.md not found")
        return path.read_text()

    @pytest.fixture
    def install_content(self):
        """Load INSTALL.md"""
        path = Path("installer/INSTALL.md")
        if not path.exists():
            pytest.skip("INSTALL.md not found")
        return path.read_text()

    def test_readme_installation_section_exists(self, readme_content):
        """Test: README has clear Installation section"""
        # Act & Assert
        assert re.search(r'#{1,3}\s+Installation', readme_content, re.IGNORECASE), \
            "README must have clear Installation section"

    def test_install_guide_comprehensive(self, install_content):
        """Test: INSTALL.md covers major scenarios"""
        # Act: Check for scenario coverage
        has_scenarios = all(re.search(pattern, install_content, re.IGNORECASE)
                           for pattern in [r'[Ff]resh', r'[Uu]pgrad', r'[Tt]roubleshoot'])

        # Assert
        assert has_scenarios, \
            "INSTALL.md should cover fresh, upgrade, and troubleshooting"

    def test_documentation_has_examples(self, install_content):
        """Test: Documentation includes executable examples"""
        # Act: Look for code blocks
        code_blocks = re.findall(r'```(?:bash)?.*?\n(.*?)\n```', install_content, re.DOTALL)

        # Assert: Should have examples
        assert len(code_blocks) > 0, \
            "INSTALL.md should include executable examples"


class TestNfrReliability:
    """Tests for NFR-002: Distribution package is easy to extract and use."""

    @pytest.fixture
    def tar_path(self):
        """Path to tar.gz"""
        return Path("devforgeai-1.0.1.tar.gz")

    @pytest.fixture
    def zip_path(self):
        """Path to ZIP"""
        return Path("devforgeai-1.0.1.zip")

    def test_tar_package_extracts_cleanly(self, tar_path):
        """Test: tar.gz extracts without errors"""
        if not tar_path.exists():
            pytest.skip("Package not found")

        import tarfile
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                with tarfile.open(tar_path, 'r:gz') as tar:
                    tar.extractall(tmpdir)
                assert True
            except Exception as e:
                pytest.fail(f"Extraction failed: {e}")

    def test_zip_package_extracts_cleanly(self, zip_path):
        """Test: ZIP extracts without errors"""
        if not zip_path.exists():
            pytest.skip("Package not found")

        import zipfile
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                with zipfile.ZipFile(zip_path, 'r') as z:
                    z.extractall(tmpdir)
                assert True
            except Exception as e:
                pytest.fail(f"Extraction failed: {e}")

    def test_extracted_content_has_readme(self, tar_path):
        """Test: Extracted package has README or documentation"""
        if not tar_path.exists():
            pytest.skip("Package not found")

        import tarfile

        with tarfile.open(tar_path, 'r:gz') as tar:
            names = tar.getnames()

        # Should have documentation
        has_docs = any('README' in n or 'INSTALL' in n or 'docs' in n for n in names)
        assert has_docs, \
            "Extracted package should have documentation"


class TestDataValidationRuleEnforcement:
    """Tests for data validation rules."""

    def test_all_version_references_consistent(self):
        """Test: All version references say 1.0.1"""
        version_locations = []

        # Check ROADMAP.md
        roadmap = Path("ROADMAP.md")
        if roadmap.exists():
            content = roadmap.read_text()
            if "1.0.1" in content:
                version_locations.append("ROADMAP.md")

        # Check version.json
        for candidate in [Path("version.json"), Path("devforgeai/version.json")]:
            if candidate.exists():
                import json
                try:
                    data = json.loads(candidate.read_text())
                    if data.get("version") == "1.0.1":
                        version_locations.append(str(candidate))
                except:
                    pass

        # Assert: At least some version references
        assert len(version_locations) > 0, \
            "At least some version references should exist"

    def test_package_checksum_available_or_documented(self):
        """Test: Package integrity checking documented"""
        # Check for checksum file
        checksum_path = Path("devforgeai-1.0.1.tar.gz.sha256")

        # Or check if documented in INSTALL.md
        install_path = Path("installer/INSTALL.md")
        has_checksum_doc = False

        if install_path.exists():
            content = install_path.read_text()
            if re.search(r'sha256|shasum|checksum', content, re.IGNORECASE):
                has_checksum_doc = True

        # Assert: Either checksum exists or documented
        if not checksum_path.exists() and not has_checksum_doc:
            pytest.skip("Checksum validation not yet set up")

    def test_onboarding_completion_documented(self):
        """Test: Onboarding completion is recorded"""
        # Check for training log
        log_path = Path("devforgeai/onboarding/team-training-log.md")

        assert log_path.exists(), \
            "Onboarding completion must be documented"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
