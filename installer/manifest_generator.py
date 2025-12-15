"""
Manifest Generator Service (STORY-075).

Handles:
- Installation manifest creation (AC#4)
- SHA256 checksum generation (SVC-009)
- File categorization (SVC-011)
- Atomic manifest writes (SVC-010)
"""

import json
import hashlib
import tempfile
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any


class ManifestGenerator:
    """
    Service for generating installation manifest files.

    Singleton lifecycle: One instance per installation session.
    Responsibilities:
    - Create .install-manifest.json with file metadata
    - Calculate SHA256 checksums for all files
    - Categorize files by type
    - Ensure atomic writes (no corruption on interrupt)
    """

    def generate_manifest(
        self,
        target_directory: str,
        installed_files: List[Path],
        version: str,
        installer_version: str,
    ) -> Path:
        """
        Generate installation manifest with checksums and metadata (AC#4).

        Args:
            target_directory: Installation target directory
            installed_files: List of Path objects for installed files
            version: Version of framework installed
            installer_version: Version of installer used

        Returns:
            Path object pointing to the generated manifest file
        """
        target_path = Path(target_directory)
        devforgeai_dir = target_path / ".devforgeai"
        manifest_path = devforgeai_dir / ".install-manifest.json"

        # Ensure .devforgeai directory exists
        devforgeai_dir.mkdir(parents=True, exist_ok=True)

        # Generate manifest data
        manifest_data = {
            "version": version,
            "timestamp": datetime.now(timezone.utc).isoformat().replace(
                "+00:00", "Z"
            ),
            "installer_version": installer_version,
            "files": [],
        }

        # Process each installed file
        for file_path in installed_files:
            entry = self._create_manifest_entry(file_path, target_path)
            manifest_data["files"].append(entry)

        # Write manifest atomically (to temp file, then rename)
        self._write_manifest_atomic(manifest_path, manifest_data)

        # Set file permissions to 644
        try:
            manifest_path.chmod(0o644)
        except (OSError, PermissionError):
            pass

        return manifest_path

    def _create_manifest_entry(
        self, file_path: Path, target_path: Path
    ) -> Dict[str, Any]:
        """
        Create a manifest entry for a single file.

        Args:
            file_path: Absolute path to the file
            target_path: Target installation root directory

        Returns:
            Dictionary with file metadata
        """
        # Calculate relative path (from target root)
        try:
            relative_path = file_path.relative_to(target_path)
        except ValueError:
            # If file is outside target, use its absolute path relative string
            relative_path = file_path

        # Calculate SHA256 checksum
        checksum = self._calculate_sha256(file_path)

        # Get file size
        size_bytes = file_path.stat().st_size

        # Determine category
        category = self._categorize_file(str(relative_path))

        entry = {
            "path": str(relative_path).replace("\\", "/"),  # Normalize to forward slashes
            "source": str(file_path),
            "checksum": checksum,
            "size_bytes": size_bytes,
            "category": category,
        }

        return entry

    def _calculate_sha256(self, file_path: Path) -> str:
        """
        Calculate SHA256 checksum of a file.

        Args:
            file_path: Path to file

        Returns:
            64-character hex string (SHA256 hash)
        """
        sha256_hash = hashlib.sha256()

        # Read file in chunks to handle large files
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)

        return sha256_hash.hexdigest()

    def _categorize_file(self, relative_path: str) -> str:
        """
        Categorize a file based on its path (SVC-011).

        Args:
            relative_path: Relative path from installation root

        Returns:
            One of: skill, agent, command, memory, script, config
        """
        path_lower = relative_path.lower()

        # Category patterns: (unix_pattern, windows_pattern) -> category
        categories = [
            ((".claude/skills/", ".claude\\skills\\"), "skill"),
            ((".claude/agents/", ".claude\\agents\\"), "agent"),
            ((".claude/commands/", ".claude\\commands\\"), "command"),
            ((".claude/memory/", ".claude\\memory\\"), "memory"),
            (("devforgeai/scripts/", ".devforgeai\\scripts\\"), "script"),
            (("devforgeai/specs/context/", ".devforgeai\\context\\"), "config"),
        ]

        for patterns, category in categories:
            if any(pattern in path_lower for pattern in patterns):
                return category

        # Default to config
        return "config"

    def _write_manifest_atomic(
        self, manifest_path: Path, manifest_data: Dict[str, Any]
    ) -> None:
        """
        Write manifest atomically to prevent corruption (SVC-010).

        Uses temporary file + rename pattern for atomic writes.

        Args:
            manifest_path: Target path for manifest file
            manifest_data: Data to write
        """
        # Write to temporary file
        temp_fd, temp_path = tempfile.mkstemp(
            dir=str(manifest_path.parent),
            prefix=".install-manifest.",
            suffix=".tmp",
        )

        try:
            # Write JSON to temp file
            with open(temp_fd, "w", encoding="utf-8") as f:
                json.dump(manifest_data, f, separators=(",", ":"))

            # Atomic rename (temp file → manifest file)
            Path(temp_path).rename(manifest_path)
        except Exception as e:
            # Clean up temp file on error
            try:
                Path(temp_path).unlink()
            except (OSError, FileNotFoundError):
                pass
            raise e
