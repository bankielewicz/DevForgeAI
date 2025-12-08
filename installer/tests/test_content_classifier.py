"""
Unit tests for ContentClassifier service.
Tests file classification as framework, user content, or modified framework.
All tests FAIL until implementation complete (TDD Red phase).
"""
import pytest
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock


class TestContentClassifierInit:
    """Test ContentClassifier initialization."""

    def test_should_instantiate_with_manifest_manager(self, mock_manifest_manager):
        """Test: ContentClassifier initializes with dependency injection."""
        from installer.content_classifier import ContentClassifier

        classifier = ContentClassifier(manifest_manager=mock_manifest_manager)
        assert classifier is not None

    def test_should_load_manifest_on_init(self, mock_manifest_manager):
        """Test: ContentClassifier loads manifest during initialization."""
        from installer.content_classifier import ContentClassifier

        classifier = ContentClassifier(manifest_manager=mock_manifest_manager)
        mock_manifest_manager.load_manifest.assert_called()


class TestFrameworkFileClassification:
    """Test classification of framework files."""

    def test_should_classify_claude_skills_as_framework(self, mock_manifest_manager):
        """Test: .claude/skills/ files classified as FRAMEWORK."""
        from installer.content_classifier import ContentClassifier, ContentType

        # Set return value BEFORE creating classifier
        mock_manifest_manager.load_manifest.return_value = {
            "installed_files": [".claude/skills/test/SKILL.md"]
        }
        classifier = ContentClassifier(manifest_manager=mock_manifest_manager)

        result = classifier.classify(".claude/skills/test/SKILL.md")
        assert result == ContentType.FRAMEWORK

    def test_should_classify_devforgeai_config_as_framework(self, mock_manifest_manager):
        """Test: .devforgeai/context/ files classified as FRAMEWORK."""
        from installer.content_classifier import ContentClassifier, ContentType

        # Set return value BEFORE creating classifier
        mock_manifest_manager.load_manifest.return_value = {
            "installed_files": [".devforgeai/context/tech-stack.md"]
        }
        classifier = ContentClassifier(manifest_manager=mock_manifest_manager)

        result = classifier.classify(".devforgeai/context/tech-stack.md")
        assert result == ContentType.FRAMEWORK

    def test_should_classify_claude_md_as_framework(self, mock_manifest_manager):
        """Test: CLAUDE.md (unmodified) classified as FRAMEWORK."""
        from installer.content_classifier import ContentClassifier, ContentType

        # Set return value BEFORE creating classifier
        mock_manifest_manager.load_manifest.return_value = {
            "installed_files": ["CLAUDE.md"],
            "file_hashes": {"CLAUDE.md": "original_hash_123"}
        }
        classifier = ContentClassifier(manifest_manager=mock_manifest_manager)

        with patch.object(classifier, '_get_file_hash', return_value="original_hash_123"):
            result = classifier.classify("CLAUDE.md")
            assert result == ContentType.FRAMEWORK


class TestUserContentClassification:
    """Test classification of user-created content."""

    def test_should_classify_story_file_as_user_content(self, mock_manifest_manager):
        """Test: .ai_docs/Stories/ files classified as USER_CONTENT."""
        from installer.content_classifier import ContentClassifier, ContentType

        classifier = ContentClassifier(manifest_manager=mock_manifest_manager)
        mock_manifest_manager.load_manifest.return_value = {"installed_files": []}

        result = classifier.classify(".ai_docs/Stories/STORY-001.md")
        assert result == ContentType.USER_CONTENT

    def test_should_classify_epic_file_as_user_content(self, mock_manifest_manager):
        """Test: .ai_docs/Epics/ files classified as USER_CONTENT."""
        from installer.content_classifier import ContentClassifier, ContentType

        classifier = ContentClassifier(manifest_manager=mock_manifest_manager)
        mock_manifest_manager.load_manifest.return_value = {"installed_files": []}

        result = classifier.classify(".ai_docs/Epics/EPIC-001.md")
        assert result == ContentType.USER_CONTENT

    def test_should_classify_sprint_file_as_user_content(self, mock_manifest_manager):
        """Test: .ai_docs/Sprints/ files classified as USER_CONTENT."""
        from installer.content_classifier import ContentClassifier, ContentType

        classifier = ContentClassifier(manifest_manager=mock_manifest_manager)
        mock_manifest_manager.load_manifest.return_value = {"installed_files": []}

        result = classifier.classify(".ai_docs/Sprints/Sprint-1.md")
        assert result == ContentType.USER_CONTENT

    def test_should_classify_custom_adr_as_user_content(self, mock_manifest_manager):
        """Test: User-created ADRs classified as USER_CONTENT."""
        from installer.content_classifier import ContentClassifier, ContentType

        classifier = ContentClassifier(manifest_manager=mock_manifest_manager)
        mock_manifest_manager.load_manifest.return_value = {
            "installed_files": ["CUSTOM_ADR_NOT_IN_MANIFEST"]
        }

        result = classifier.classify(".devforgeai/adrs/ADR-999-custom.md")
        assert result == ContentType.USER_CONTENT


class TestModifiedFrameworkClassification:
    """Test classification of modified framework files."""

    def test_should_classify_modified_claude_md_as_modified_framework(self, mock_manifest_manager):
        """Test: Modified CLAUDE.md classified as MODIFIED_FRAMEWORK."""
        from installer.content_classifier import ContentClassifier, ContentType

        # Set return value BEFORE creating classifier
        mock_manifest_manager.load_manifest.return_value = {
            "installed_files": ["CLAUDE.md"],
            "file_hashes": {"CLAUDE.md": "original_hash"}
        }
        classifier = ContentClassifier(manifest_manager=mock_manifest_manager)

        with patch.object(classifier, '_get_file_hash', return_value="modified_hash"):
            result = classifier.classify("CLAUDE.md")
            assert result == ContentType.MODIFIED_FRAMEWORK

    def test_should_classify_modified_context_file_as_modified_framework(self, mock_manifest_manager):
        """Test: Modified tech-stack.md classified as MODIFIED_FRAMEWORK."""
        from installer.content_classifier import ContentClassifier, ContentType

        # Set return value BEFORE creating classifier
        mock_manifest_manager.load_manifest.return_value = {
            "installed_files": [".devforgeai/context/tech-stack.md"],
            "file_hashes": {".devforgeai/context/tech-stack.md": "hash_original"}
        }
        classifier = ContentClassifier(manifest_manager=mock_manifest_manager)

        with patch.object(classifier, '_get_file_hash', return_value="hash_modified"):
            result = classifier.classify(".devforgeai/context/tech-stack.md")
            assert result == ContentType.MODIFIED_FRAMEWORK


class TestUnknownFileClassification:
    """Test classification of files not in manifest."""

    def test_should_classify_new_file_in_devforgeai_as_user_created(self, mock_manifest_manager):
        """Test: New file in .devforgeai/protocols/ (framework dir) classified as USER_CREATED."""
        from installer.content_classifier import ContentClassifier, ContentType

        # Set return value BEFORE creating classifier
        mock_manifest_manager.load_manifest.return_value = {"installed_files": []}
        classifier = ContentClassifier(manifest_manager=mock_manifest_manager)

        # File in framework directory but not in manifest = USER_CREATED
        result = classifier.classify(".devforgeai/protocols/custom-file.txt")
        assert result == ContentType.USER_CREATED

    def test_should_classify_new_file_in_claude_as_user_created(self, mock_manifest_manager):
        """Test: New file in .claude/agents/ (framework dir) classified as USER_CREATED."""
        from installer.content_classifier import ContentClassifier, ContentType

        # Set return value BEFORE creating classifier
        mock_manifest_manager.load_manifest.return_value = {"installed_files": []}
        classifier = ContentClassifier(manifest_manager=mock_manifest_manager)

        # File in framework directory but not in manifest = USER_CREATED
        result = classifier.classify(".claude/agents/custom-agent.md")
        assert result == ContentType.USER_CREATED


class TestClassifyMultipleFiles:
    """Test batch classification of files."""

    def test_should_classify_directory_recursively(self, temp_install_dir, mock_manifest_manager):
        """Test: ContentClassifier can classify entire directory tree."""
        from installer.content_classifier import ContentClassifier

        classifier = ContentClassifier(manifest_manager=mock_manifest_manager)
        mock_manifest_manager.load_manifest.return_value = {
            "installed_files": [".claude/skills/test/SKILL.md"]
        }

        # Create test files
        (temp_install_dir / ".claude" / "skills" / "test").mkdir(parents=True, exist_ok=True)
        (temp_install_dir / ".claude" / "skills" / "test" / "SKILL.md").touch()
        (temp_install_dir / ".ai_docs" / "Stories").mkdir(parents=True, exist_ok=True)
        (temp_install_dir / ".ai_docs" / "Stories" / "STORY-001.md").touch()

        # This will require implementation of batch classification
        results = classifier.classify_directory(str(temp_install_dir))
        assert results is not None


class TestHashComparison:
    """Test hash comparison for detecting modifications."""

    def test_should_detect_file_modification_via_hash(self, mock_manifest_manager):
        """Test: File modification detected by comparing SHA256 hashes."""
        from installer.content_classifier import ContentClassifier

        # Set return value BEFORE creating classifier
        mock_manifest_manager.load_manifest.return_value = {
            "installed_files": ["CLAUDE.md"],
            "file_hashes": {"CLAUDE.md": "hash_abc123"}
        }
        classifier = ContentClassifier(manifest_manager=mock_manifest_manager)

        with patch.object(classifier, '_get_file_hash', return_value="hash_different"):
            is_modified = classifier.is_file_modified("CLAUDE.md")
            assert is_modified is True
