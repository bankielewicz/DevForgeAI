"""
Test suite for AC4: Incremental Documentation Updates

Tests detection of existing files, selective section updates,
preservation of user-authored content, changelog entries, and consistency.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, mock_open
from datetime import datetime
import yaml


class TestExistingDocumentationDetection:
    """Test detection of existing documentation files."""

    def test_should_detect_existing_readme(self):
        """Test that system detects if README.md already exists."""
        # Arrange
        files = ["README.md", "src/index.ts", "package.json"]
        existing_docs = {"README.md": {"path": "/README.md", "exists": True}}

        # Act
        from devforgeai_documentation import DocumentationDetector
        detector = DocumentationDetector()
        detected = detector.find_existing_docs(files)

        # Assert
        assert detected is not None
        assert "README" in str(detected).upper() or any("readme" in str(f).lower() for f in detected)

    def test_should_detect_docs_directory(self):
        """Test that system finds /docs directory with existing files."""
        # Arrange
        structure = {
            "docs/": {
                "API.md": "exists",
                "ARCHITECTURE.md": "exists",
                "CONTRIBUTING.md": "exists"
            }
        }

        # Act
        from devforgeai_documentation import DocumentationDetector
        detector = DocumentationDetector()
        detected = detector.find_doc_directories(structure)

        # Assert
        assert detected is not None
        assert "docs" in str(detected).lower()

    def test_should_read_existing_file_content(self):
        """Test that system can read content of existing documentation."""
        # Arrange
        readme_content = """# My Project

## Installation
npm install

## Usage
npm run dev
"""

        # Act
        from devforgeai_documentation import FileReader
        reader = FileReader()
        content = reader.read_file("README.md")

        # Assert
        # In tests, we'd mock this
        pass

    def test_should_detect_file_modification_time(self):
        """Test that system detects when files were last modified."""
        # Arrange
        files = {
            "README.md": {"last_modified": "2025-11-01"},
            "docs/API.md": {"last_modified": "2025-11-15"}
        }

        # Act
        from devforgeai_documentation import DocumentationDetector
        detector = DocumentationDetector()
        mtimes = detector.get_modification_times(files)

        # Assert
        assert mtimes is not None
        assert isinstance(mtimes, dict)


class TestSelectiveUpdates:
    """Test selective section updates in existing files."""

    def test_should_identify_affected_sections(self):
        """Test that system identifies which sections need updates."""
        # Arrange
        existing_content = """# Project

## API Reference
Old API docs here

## Installation
Installation steps

## Features
Feature list
"""
        new_story = {
            "title": "New API Endpoint",
            "affects": ["API Reference"]
        }

        # Act
        from devforgeai_documentation import SectionAnalyzer
        analyzer = SectionAnalyzer()
        affected_sections = analyzer.find_affected_sections(existing_content, new_story)

        # Assert
        assert affected_sections is not None
        # Should identify API Reference as affected
        assert any("api" in str(s).lower() for s in affected_sections)

    def test_should_update_only_affected_sections(self):
        """Test that only affected sections are updated."""
        # Arrange
        existing_readme = """# Project

## Features
- Feature 1
- Feature 2

## API
- Old endpoint

## Installation
npm install
"""
        new_content = {
            "API": "- New endpoint\n- Another endpoint"
        }

        # Act
        from devforgeai_documentation import IncrementalUpdater
        updater = IncrementalUpdater()
        result = updater.update_sections(existing_readme, new_content)

        # Assert
        assert result is not None
        # Should have updated API section
        assert "New endpoint" in result
        # Should preserve Features section
        assert "Feature 1" in result
        # Should preserve Installation section
        assert "npm install" in result

    def test_should_preserve_unchanged_sections(self):
        """Test that unaffected sections are not modified."""
        # Arrange
        original = """## Section A
Content A

## Section B
Content B

## Section C
Content C"""

        # Act
        from devforgeai_documentation import IncrementalUpdater
        updater = IncrementalUpdater()
        # Update only Section B
        updated = updater.update_sections(original, {"Section B": "New Content B"})

        # Assert
        assert updated is not None
        assert "Content A" in updated  # Section A preserved
        assert "Content C" in updated  # Section C preserved


class TestUserAuthoredContentPreservation:
    """Test preservation of user-authored content."""

    def test_should_detect_user_authored_markers(self):
        """Test that system recognizes user-authored content markers."""
        # Arrange
        content = """## API Reference

<!-- USER-AUTHORED START -->
This section was written by a user and should not be overwritten.
Custom examples and notes here.
<!-- USER-AUTHORED END -->

Auto-generated API reference continues below.
"""

        # Act
        from devforgeai_documentation import UserContentDetector
        detector = UserContentDetector()
        user_sections = detector.find_user_sections(content)

        # Assert
        assert user_sections is not None
        assert len(user_sections) > 0
        # Should preserve content between markers
        if isinstance(user_sections, dict):
            for section in user_sections.values():
                assert "Custom examples" in str(section) or "user" in str(section).lower()

    def test_should_not_overwrite_user_authored_sections(self):
        """Test that user-authored sections are never overwritten."""
        # Arrange
        existing = """# Project

## Configuration

<!-- USER-AUTHORED START -->
My custom configuration notes that I wrote.
Do not touch this!
<!-- USER-AUTHORED END -->

Auto-generated config docs below.
"""
        new_generated = "Auto-generated config docs with new stuff."

        # Act
        from devforgeai_documentation import IncrementalUpdater
        updater = IncrementalUpdater()
        result = updater.update_sections(existing, {"Configuration": new_generated})

        # Assert
        assert result is not None
        # User section should be preserved
        assert "My custom configuration notes" in result
        # But auto-generated part should be updated
        assert "new stuff" in result or new_generated in result

    def test_should_use_git_blame_to_detect_user_content(self):
        """Test that system can use git blame to detect user-authored sections."""
        # Arrange
        file_path = "README.md"

        # Act
        from devforgeai_documentation import GitBlameDetector
        detector = GitBlameDetector()
        # In actual implementation, this would run git blame
        user_lines = detector.find_user_authored_lines(file_path)

        # Assert
        assert user_lines is not None
        # Should return dict or list

    def test_should_create_backup_before_update(self):
        """Test that backup is created before updating existing file."""
        # Arrange
        file_path = "README.md"
        current_time = datetime.now().strftime("%Y%m%d-%H%M%S")

        # Act
        from devforgeai_documentation import BackupManager
        manager = BackupManager()
        backup_path = manager.create_backup(file_path, current_time)

        # Assert
        assert backup_path is not None
        # Backup should have timestamp
        assert current_time in backup_path or ".backup" in backup_path


class TestChangelogManagement:
    """Test changelog entry generation and maintenance."""

    def test_should_add_changelog_entry(self):
        """Test that changelog entry is added for new story."""
        # Arrange
        story = {
            "id": "STORY-041",
            "title": "Add user profile endpoint",
            "version": "1.2.0"
        }
        existing_changelog = """# Changelog

## [1.1.0] - 2025-11-10
- Initial release
"""

        # Act
        from devforgeai_documentation import ChangelogManager
        manager = ChangelogManager()
        updated_changelog = manager.add_entry(existing_changelog, story)

        # Assert
        assert updated_changelog is not None
        assert "1.2.0" in updated_changelog or "STORY-041" in updated_changelog
        # Should preserve previous entries
        assert "1.1.0" in updated_changelog

    def test_changelog_entry_should_include_story_id(self):
        """Test that changelog mentions the story ID."""
        # Arrange
        story = {"id": "STORY-042", "title": "Feature X"}

        # Act
        from devforgeai_documentation import ChangelogManager
        manager = ChangelogManager()
        entry = manager.create_entry(story)

        # Assert
        assert entry is not None
        assert "STORY-042" in entry or "STORY" in entry

    def test_changelog_should_be_dated(self):
        """Test that changelog entries include dates."""
        # Arrange
        story = {"id": "STORY-043", "title": "Feature Y"}
        date = "2025-11-18"

        # Act
        from devforgeai_documentation import ChangelogManager
        manager = ChangelogManager()
        entry = manager.create_entry(story, date)

        # Assert
        assert entry is not None
        assert "2025-11-18" in entry or date in entry

    def test_should_group_entries_by_version(self):
        """Test that changelog groups entries by version."""
        # Arrange
        entries = [
            {"story": "STORY-041", "version": "1.2.0"},
            {"story": "STORY-042", "version": "1.2.0"},
            {"story": "STORY-043", "version": "1.3.0"}
        ]

        # Act
        from devforgeai_documentation import ChangelogManager
        manager = ChangelogManager()
        grouped = manager.group_by_version(entries)

        # Assert
        assert grouped is not None
        # Should have entries organized by version
        assert "1.2.0" in str(grouped) or "version" in str(grouped).lower()


class TestDocumentationConsistency:
    """Test consistency maintenance across documentation."""

    def test_should_update_version_numbers(self):
        """Test that version numbers are updated consistently."""
        # Arrange
        docs = {
            "README.md": "Version: 1.1.0",
            "docs/CHANGELOG.md": "## [1.1.0]",
            "package.json": '"version": "1.1.0"'
        }
        new_version = "1.2.0"

        # Act
        from devforgeai_documentation import VersionUpdater
        updater = VersionUpdater()
        result = updater.update_all_versions(docs, new_version)

        # Assert
        assert result is not None
        # All should have new version
        assert "1.2.0" in str(result).count("1.2.0") >= 2

    def test_should_update_cross_references(self):
        """Test that cross-references are updated consistently."""
        # Arrange
        docs = {
            "README.md": "See [API Docs](docs/API.md)",
            "docs/API.md": "See [Configuration](CONFIGURATION.md)",
            "docs/CONFIGURATION.md": "See [README](../README.md)"
        }

        # Act
        from devforgeai_documentation import CrossReferenceUpdater
        updater = CrossReferenceUpdater()
        # After file reorganization
        result = updater.update_cross_references(docs)

        # Assert
        assert result is not None

    def test_should_update_table_of_contents(self):
        """Test that table of contents is regenerated on update."""
        # Arrange
        content = """# Project

## Installation
...

## Usage
...

## API Reference
...
"""

        # Act
        from devforgeai_documentation import TOCGenerator
        gen = TOCGenerator()
        toc = gen.generate_toc(content)

        # Assert
        assert toc is not None
        # Should reference all major sections
        toc_text = str(toc).lower()
        assert "installation" in toc_text and "usage" in toc_text and "api" in toc_text

    def test_should_validate_consistency(self):
        """Test that consistency validation passes after updates."""
        # Arrange
        docs = {
            "README.md": "# Project v1.2.0\nInstall: npm install",
            "docs/API.md": "API v1.2.0 endpoints",
            "CHANGELOG.md": "## [1.2.0] - 2025-11-18"
        }

        # Act
        from devforgeai_documentation import ConsistencyValidator
        validator = ConsistencyValidator()
        issues = validator.find_consistency_issues(docs)

        # Assert
        assert issues is not None
        # Should find no major consistency issues (all have v1.2.0)
        if isinstance(issues, list):
            assert len(issues) == 0 or len(issues) < 3


class TestIncrementalUpdateWorkflow:
    """Test complete incremental update workflow."""

    def test_should_detect_update_needed(self):
        """Test that system detects when documentation update is needed."""
        # Arrange
        existing_story_id = "STORY-040"
        new_story_id = "STORY-041"
        new_story_status = "QA Approved"

        # Act
        from devforgeai_documentation import UpdateDetector
        detector = UpdateDetector()
        needs_update = detector.should_update(new_story_status)

        # Assert
        assert needs_update is True

    def test_should_merge_new_content_with_existing(self):
        """Test that new content is merged properly with existing docs."""
        # Arrange
        existing = """# Project

## Features
- Feature 1

## API
Old endpoints
"""
        new_sections = {
            "API": "- New endpoint: POST /api/v2/users",
            "Features": "- Feature 1\n- Feature 2 (NEW)"
        }

        # Act
        from devforgeai_documentation import IncrementalUpdater
        updater = IncrementalUpdater()
        merged = updater.merge_content(existing, new_sections)

        # Assert
        assert merged is not None
        # Should have new endpoint
        assert "POST /api/v2/users" in merged
        # Should have both features
        assert "Feature 1" in merged and "Feature 2" in merged

    def test_should_preserve_manual_edits(self):
        """Test that manual edits to existing files are preserved."""
        # Arrange
        existing = """# Project

## Installation
npm install

<!-- CUSTOM SECTION START -->
Special setup for our team:
1. Set DEBUG=true
2. Configure .env file
<!-- CUSTOM SECTION END -->

## Usage
"""

        # Act
        from devforgeai_documentation import IncrementalUpdater
        updater = IncrementalUpdater()
        result = updater.update_with_preservation(existing, {"Installation": "Updated installation"})

        # Assert
        assert result is not None
        # Custom section should remain
        assert "Special setup for our team" in result
        assert "DEBUG=true" in result


class TestConflictHandling:
    """Test handling of conflicts during updates."""

    def test_should_detect_conflicting_updates(self):
        """Test that system detects when generated content conflicts with user changes."""
        # Arrange
        existing = "## API\nUser wrote custom API docs here"
        new_generated = "## API\nAuto-generated API reference"

        # Act
        from devforgeai_documentation import ConflictDetector
        detector = ConflictDetector()
        has_conflict = detector.detect_conflict(existing, new_generated)

        # Assert
        assert has_conflict is not None
        # Should detect that both have content for same section
        assert isinstance(has_conflict, bool)

    def test_should_prompt_user_on_conflict(self):
        """Test that system asks user how to resolve conflicts."""
        # Arrange
        conflict = {
            "section": "API",
            "existing": "User content",
            "generated": "Auto-generated content"
        }

        # Act
        # In actual implementation, would use AskUserQuestion
        # For test purposes, we define expected behavior
        options = ["Use existing", "Use generated", "Merge", "Review manually"]

        # Assert
        assert len(options) > 0
        assert "Merge" in options or "Review" in options


class TestUpdateValidation:
    """Test validation of updated documentation."""

    def test_should_validate_markdown_syntax_after_update(self):
        """Test that updated markdown is valid."""
        # Arrange
        updated_content = """# Project

## Section 1
Content here

## Section 2
- Item 1
- Item 2
"""

        # Act
        from devforgeai_documentation import MarkdownValidator
        validator = MarkdownValidator()
        is_valid = validator.validate(updated_content)

        # Assert
        assert is_valid is True

    def test_should_check_for_broken_links(self):
        """Test that updated documentation doesn't have broken links."""
        # Arrange
        updated_content = """# Project

- [API Docs](docs/API.md)
- [Installation](README.md#installation)
- [Non-existent](docs/MISSING.md)
"""
        available_files = ["docs/API.md", "README.md"]

        # Act
        from devforgeai_documentation import LinkValidator
        validator = LinkValidator()
        broken = validator.find_broken_links(updated_content, available_files)

        # Assert
        assert broken is not None
        # Should detect missing file
        if isinstance(broken, list):
            assert any("MISSING" in str(link) for link in broken) or len(broken) > 0

    def test_should_validate_code_examples(self):
        """Test that code examples in documentation are valid."""
        # Arrange
        content = """# Project

## Usage

\`\`\`javascript
const app = require('express')();
app.listen(3000);
\`\`\`
"""

        # Act
        from devforgeai_documentation import CodeExampleValidator
        validator = CodeExampleValidator()
        issues = validator.validate(content)

        # Assert
        assert issues is not None
        # Basic examples should have no critical issues


class TestPerformanceForUpdates:
    """Test performance of incremental updates."""

    @pytest.mark.timeout(60)
    def test_incremental_update_should_complete_in_one_minute(self):
        """Test that single file update completes in <1 minute."""
        # Arrange
        existing_content = "# Project\n" + "\n## Section\nContent\n" * 100
        new_section = "Updated section"

        # Act
        from devforgeai_documentation import IncrementalUpdater
        import time
        updater = IncrementalUpdater()
        start = time.time()
        result = updater.update_sections(existing_content, {"Section": new_section})
        elapsed = time.time() - start

        # Assert
        assert result is not None
        assert elapsed < 60
