"""ManifestManager service (STORY-079, 150 lines).

Manages installation manifest with:
- Loading manifests (AC#8, SVC-011)
- Regenerating from current files (AC#8, SVC-012)
- Updating after repairs (AC#4, SVC-013)
- Atomic writes to prevent corruption
"""

import json
import hashlib
import tempfile
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional
from installer.models.fix_models import InstallManifest


class ManifestManager:
    """Manages installation manifest (SVC-011 to SVC-013)."""

    MANIFEST_FILENAME = ".install-manifest.json"
    VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+")

    def __init__(self, installation_root: str):
        """Initialize manifest manager.

        Args:
            installation_root: Path to installation directory
        """
        self.installation_root = Path(installation_root)
        self.manifest_path = self.installation_root / "devforgeai" / self.MANIFEST_FILENAME

    def load(self) -> Optional[InstallManifest]:
        """Load installation manifest from disk.

        SVC-011: Load installation manifest
        Returns None if manifest doesn't exist, raises error if invalid.

        Returns:
            InstallManifest: Loaded manifest or None if missing

        Raises:
            json.JSONDecodeError: If manifest JSON invalid
            ValueError: If manifest structure invalid
        """
        if not self.manifest_path.exists():
            return None

        try:
            data = json.loads(self.manifest_path.read_text())
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid manifest JSON: {e.msg}", e.doc, e.pos)

        # Validate structure
        required_fields = {"version", "created_at", "files", "schema_version"}
        if not required_fields.issubset(data.keys()):
            raise ValueError(f"Manifest missing required fields: {required_fields}")

        # Validate version format
        if not self.VERSION_PATTERN.match(data["version"]):
            raise ValueError(f"Invalid version format: {data['version']}")

        # Note: Checksum format validation happens in InstallationValidator
        # ManifestManager just loads whatever is in the manifest
        # (file may be corrupted, which is detected during validation)

        return InstallManifest(
            version=data["version"],
            created_at=data["created_at"],
            files=data["files"],
            schema_version=data.get("schema_version", 1),
        )

    def regenerate(self) -> InstallManifest:
        """Regenerate manifest from current files.

        SVC-012: Regenerate manifest from current files
        Scans installation directory and creates manifest with current file states.
        Marks user-modifiable files (devforgeai/specs/, devforgeai/specs/context/) accordingly.

        Returns:
            InstallManifest: Newly generated manifest

        Raises:
            OSError: If cannot read files
        """
        files = []

        # Scan for all files (excluding manifest and backups)
        for file_path in self.installation_root.rglob("*"):
            if not file_path.is_file():
                continue

            # Skip manifest file
            if file_path.name == self.MANIFEST_FILENAME:
                continue

            # Skip backup directory
            if ".backups" in file_path.parts:
                continue

            # Skip log files
            if file_path.parent.name == "logs":
                continue

            rel_path = str(file_path.relative_to(self.installation_root)).replace("\\", "/")

            # Determine if user-modifiable
            is_user_modifiable = any(rel_path.startswith(d) for d in ["devforgeai/specs/", "devforgeai/specs/context/"])

            # Calculate checksum
            checksum = self._calculate_sha256(file_path)

            files.append({
                "path": rel_path,
                "checksum": checksum,
                "size": file_path.stat().st_size,
                "is_user_modifiable": is_user_modifiable,
            })

        # Create manifest
        manifest = InstallManifest(
            version="1.0.0",
            created_at=datetime.now(timezone.utc).isoformat(),
            files=files,
            schema_version=1,
        )

        return manifest

    def update(self, manifest: InstallManifest, file_path: str,
               new_checksum: str, new_size: int) -> InstallManifest:
        """Update manifest after file repair.

        SVC-013: Update manifest after repair
        Updates checksum and size for a file entry, preserving is_user_modifiable flag.

        Args:
            manifest: Current manifest
            file_path: Relative path of file to update
            new_checksum: New SHA256 checksum
            new_size: New file size

        Returns:
            InstallManifest: Updated manifest
        """
        for file_entry in manifest.files:
            if file_entry["path"] == file_path:
                file_entry["checksum"] = new_checksum
                file_entry["size"] = new_size
                break

        return manifest

    def save(self, manifest: InstallManifest) -> None:
        """Save manifest to disk atomically.

        Uses atomic write pattern (temp file + rename) to prevent corruption.

        Args:
            manifest: Manifest to save

        Raises:
            OSError: If cannot write
        """
        manifest_data = {
            "version": manifest.version,
            "created_at": manifest.created_at,
            "files": manifest.files,
            "schema_version": manifest.schema_version,
        }

        self._write_atomic(self.manifest_path, json.dumps(manifest_data, indent=2))

    def _write_atomic(self, target_path: Path, content: str) -> None:
        """Write file atomically using temp file + rename.

        Prevents corruption if write fails partway through.

        Args:
            target_path: Target file path
            content: Content to write
        """
        # Ensure parent directory exists
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # Write to temp file in same directory (same filesystem)
        with tempfile.NamedTemporaryFile(
            mode='w',
            dir=target_path.parent,
            delete=False,
            suffix='.tmp',
        ) as tmp:
            tmp_path = Path(tmp.name)
            tmp.write(content)

        # Atomic rename
        tmp_path.replace(target_path)

    @staticmethod
    def _calculate_sha256(file_path: Path) -> str:
        """Calculate SHA256 checksum for file (delegates to checksum module).

        Args:
            file_path: Path to file

        Returns:
            str: SHA256 hash as 64-character hex string
        """
        from installer.checksum import calculate_sha256
        return calculate_sha256(file_path)
