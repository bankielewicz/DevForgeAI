"""ContentClassifier service for STORY-081.

Classifies files as framework, user content, or modified framework:
- FRAMEWORK: Files from DevForgeAI package (.claude/skills, .claude/agents, etc.)
- USER_CONTENT: User-created files (.ai_docs/, custom ADRs, etc.)
- MODIFIED_FRAMEWORK: Framework files modified by user
- USER_CREATED: New files in framework directories not in manifest
"""

import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any

from installer.uninstall_models import ContentType, ClassifiedFile


class ContentClassifier:
    """Classifies files for uninstall operation."""

    # Patterns for user content directories (always preserved in PRESERVE mode)
    USER_CONTENT_PATTERNS = [
        ".ai_docs/",
        ".devforgeai/adrs/",
        ".devforgeai/config/",
    ]

    # Patterns for framework directories
    FRAMEWORK_PATTERNS = [
        ".claude/skills/",
        ".claude/agents/",
        ".claude/commands/",
        ".claude/memory/",
        ".claude/scripts/",
        ".devforgeai/protocols/",
        ".devforgeai/qa/",
        ".devforgeai/context/",
    ]

    def __init__(self, manifest_manager: Any, installation_root: Optional[Path] = None, logger: Any = None):
        """Initialize classifier with manifest manager.

        Args:
            manifest_manager: Manager for installation manifest
            installation_root: Root directory of installation
            logger: Optional logger for debugging
        """
        self.manifest_manager = manifest_manager
        self.installation_root = installation_root or Path.cwd()
        self.logger = logger
        self._manifest_data: Optional[Dict] = None
        self._load_manifest()

    def _load_manifest(self) -> None:
        """Load manifest data from manager."""
        self._manifest_data = self.manifest_manager.load_manifest()

    def classify(self, rel_path: str) -> ContentType:
        """Classify a file by its relative path.

        Args:
            rel_path: Relative path from installation root

        Returns:
            ContentType classification
        """
        # Normalize path separators
        rel_path = rel_path.replace("\\", "/")

        # Resolve symlinks if needed
        try:
            resolved_path = self._resolve_symlink(rel_path)
        except Exception:
            resolved_path = rel_path

        # Check if file is user content (takes precedence)
        if self._is_user_content_path(resolved_path):
            return ContentType.USER_CONTENT

        # Check if file is in manifest (framework file)
        if self._is_in_manifest(resolved_path):
            # Check if file has been modified (content or permissions)
            if self._is_modified(resolved_path):
                return ContentType.MODIFIED_FRAMEWORK
            return ContentType.FRAMEWORK

        # File not in manifest but in framework directory
        # This is user-created file in a framework directory
        if self._is_framework_path(resolved_path):
            return ContentType.USER_CREATED

        # Default to user content for unknown files
        return ContentType.USER_CONTENT

    def classify_directory(self, directory: str) -> List[ClassifiedFile]:
        """Classify all files in a directory recursively.

        Args:
            directory: Directory path to scan

        Returns:
            List of ClassifiedFile objects
        """
        results = []
        dir_path = Path(directory)

        for file_path in dir_path.rglob("*"):
            if not file_path.is_file():
                continue

            rel_path = str(file_path.relative_to(dir_path)).replace("\\", "/")
            content_type = self.classify(rel_path)

            results.append(ClassifiedFile(
                path=rel_path,
                content_type=content_type,
                size_bytes=file_path.stat().st_size if file_path.exists() else 0,
            ))

        return results

    def is_file_modified(self, rel_path: str) -> bool:
        """Check if a file has been modified from original.

        Args:
            rel_path: Relative path to check

        Returns:
            True if file was modified from manifest hash
        """
        return self._is_modified(rel_path)

    def _is_user_content_path(self, rel_path: str) -> bool:
        """Check if path is in user content directory.

        Args:
            rel_path: Relative path to check

        Returns:
            True if path is in a user content directory
        """
        for pattern in self.USER_CONTENT_PATTERNS:
            if rel_path.startswith(pattern):
                return True
        return False

    def _is_framework_path(self, rel_path: str) -> bool:
        """Check if path is in framework directory.

        Args:
            rel_path: Relative path to check

        Returns:
            True if path is in a framework directory
        """
        for pattern in self.FRAMEWORK_PATTERNS:
            if rel_path.startswith(pattern):
                return True
        # Also check root framework files
        if rel_path == "CLAUDE.md":
            return True
        return False

    def _is_in_manifest(self, rel_path: str) -> bool:
        """Check if file is listed in installation manifest.

        Args:
            rel_path: Relative path to check

        Returns:
            True if file is in manifest
        """
        if not self._manifest_data:
            return False

        installed_files = self._manifest_data.get("installed_files", [])
        return rel_path in installed_files

    def _is_modified(self, rel_path: str) -> bool:
        """Check if file hash differs from manifest hash.

        Args:
            rel_path: Relative path to check

        Returns:
            True if file hash doesn't match manifest hash
        """
        if not self._manifest_data:
            return False

        file_hashes = self._manifest_data.get("file_hashes", {})
        original_hash = file_hashes.get(rel_path)

        if not original_hash:
            return False

        current_hash = self._get_file_hash(rel_path)
        return current_hash != original_hash

    def _resolve_symlink(self, rel_path: str) -> str:
        """Resolve symlink to its target.

        Args:
            rel_path: Relative path to file (may be symlink)

        Returns:
            Resolved path (or original if not a symlink)
        """
        file_path = self.installation_root / rel_path

        if file_path.is_symlink():
            try:
                resolved = file_path.resolve()
                # Return relative path from installation root
                return str(resolved.relative_to(self.installation_root)).replace("\\", "/")
            except (OSError, ValueError):
                # Broken symlink or outside installation root
                return rel_path

        return rel_path

    def _get_file_permissions(self, rel_path: str) -> Optional[str]:
        """Get file permissions in octal format.

        Args:
            rel_path: Relative path to file

        Returns:
            Octal permission string (e.g., '0644') or None
        """
        file_path = self.installation_root / rel_path

        if not file_path.exists():
            return None

        import stat
        mode = file_path.stat().st_mode
        return oct(stat.S_IMODE(mode))

    def _get_file_hash(self, rel_path: str) -> Optional[str]:
        """Calculate SHA256 hash of file.

        Args:
            rel_path: Relative path to file

        Returns:
            Hex string of SHA256 hash or None if file not found
        """
        file_path = self.installation_root / rel_path

        if not file_path.exists():
            return None

        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)

        return sha256.hexdigest()
