"""
Platform Detection Module for DevForgeAI Installer (STORY-235)

Provides cross-platform detection for OS type, WSL environment,
filesystem type, and chmod support.

Usage:
    from installer.platform_detector import PlatformDetector, PlatformInfo

    info = PlatformDetector.detect()
    print(f"OS: {info.os_type}, WSL: {info.is_wsl}")

    # With specific path for cross-filesystem detection
    info = PlatformDetector.detect(path="/mnt/c/project")
    if info.is_cross_filesystem:
        print("Warning: chmod operations may not work")
"""

import platform
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union


@dataclass
class PlatformInfo:
    """
    Data structure containing platform detection results.

    Attributes:
        os_type: Operating system name ("Linux", "Darwin", "Windows")
        is_wsl: True if running in Windows Subsystem for Linux
        wsl_version: WSL version (1 or 2) if is_wsl, None otherwise
        filesystem: Detected filesystem type ("ext4", "ntfs-wsl", "apfs", etc.)
        is_cross_filesystem: True if path crosses filesystem boundary (WSL /mnt/)
        supports_chmod: True if filesystem supports Unix chmod operations
    """
    os_type: str
    is_wsl: bool
    wsl_version: Optional[int]
    filesystem: str
    is_cross_filesystem: bool
    supports_chmod: bool


class PlatformDetector:
    """
    Platform detection service for the DevForgeAI installer.

    Provides static methods to detect platform characteristics
    relevant to installation and file permission handling.
    """

    # Cache for detection results keyed by path
    _cache: dict[Optional[str], PlatformInfo] = {}

    @staticmethod
    def detect(path: Optional[Union[str, Path]] = None) -> PlatformInfo:
        """
        Detect platform characteristics for the current environment.

        Args:
            path: Optional path to check for cross-filesystem scenarios.
                  If None, uses current directory.

        Returns:
            PlatformInfo with all detection results populated.

        Business Rules:
            - BR-001: Gracefully handles missing /proc/version
            - BR-002: Cross-filesystem detection only applies in WSL
        """
        # Normalize path to string for caching
        path_str = str(path) if path is not None else None

        # Check cache first
        if path_str in PlatformDetector._cache:
            return PlatformDetector._cache[path_str]

        # Detect OS
        os_type = platform.system()

        # Detect WSL
        is_wsl, wsl_version = PlatformDetector._detect_wsl(os_type)

        # Detect filesystem
        filesystem = PlatformDetector._detect_filesystem(os_type, is_wsl, path_str)

        # Detect cross-filesystem
        is_cross_filesystem = PlatformDetector._detect_cross_filesystem(
            os_type, is_wsl, path_str
        )

        # Determine chmod support
        supports_chmod = PlatformDetector._detect_chmod_support(
            os_type, filesystem, is_cross_filesystem
        )

        result = PlatformInfo(
            os_type=os_type,
            is_wsl=is_wsl,
            wsl_version=wsl_version,
            filesystem=filesystem,
            is_cross_filesystem=is_cross_filesystem,
            supports_chmod=supports_chmod,
        )

        # Cache the result
        PlatformDetector._cache[path_str] = result

        return result

    @staticmethod
    def _detect_wsl(os_type: str) -> tuple[bool, Optional[int]]:
        """
        Detect if running in WSL and which version.

        Reads /proc/version and looks for "microsoft" (case-insensitive).
        Determines WSL version by looking for "wsl2" (case-insensitive).

        BR-001: Gracefully handles missing /proc/version by returning
                (False, None) instead of raising an exception.

        Returns:
            Tuple of (is_wsl, wsl_version)
        """
        # WSL only applies on Linux
        if os_type != "Linux":
            return False, None

        try:
            with open("/proc/version", "r") as f:
                version_content = f.read().lower()
        except (FileNotFoundError, PermissionError, OSError):
            # BR-001: Graceful handling of missing /proc/version
            return False, None

        # Check for microsoft (case-insensitive)
        if "microsoft" not in version_content:
            return False, None

        # Determine WSL version
        if "wsl2" in version_content:
            return True, 2
        else:
            # WSL1 - microsoft present but not wsl2
            return True, 1

    @staticmethod
    def _detect_filesystem(
        os_type: str,
        is_wsl: bool,
        path_str: Optional[str]
    ) -> str:
        """
        Detect the filesystem type for the given path.

        Returns filesystem identifier based on OS and path location.
        """
        # Windows native
        if os_type == "Windows":
            return "ntfs"

        # macOS
        if os_type == "Darwin":
            return "apfs"

        # Linux (including WSL)
        if os_type == "Linux":
            # Check if path is on Windows filesystem via WSL mount
            if is_wsl and path_str and path_str.startswith("/mnt/"):
                # Check if it's a drive letter mount (e.g., /mnt/c, /mnt/d)
                parts = path_str.split("/")
                if len(parts) >= 3 and len(parts[2]) == 1 and parts[2].isalpha():
                    return "ntfs-wsl"

            # Native Linux filesystem
            return "ext4"

        # Fallback for unknown OS
        return "unknown"

    @staticmethod
    def _detect_cross_filesystem(
        os_type: str,
        is_wsl: bool,
        path_str: Optional[str]
    ) -> bool:
        """
        Detect if the path crosses a filesystem boundary.

        BR-002: Cross-filesystem detection only applies in WSL.
        A path is considered cross-filesystem if:
        - Running in WSL (is_wsl=True)
        - Path starts with /mnt/ and has a drive letter (e.g., /mnt/c/)

        Native Linux /mnt/ paths (like /mnt/data) are NOT cross-filesystem.
        """
        # BR-002: Only applies in WSL
        if not is_wsl:
            return False

        if not path_str:
            return False

        # Check if path starts with /mnt/ (case-sensitive for Linux paths)
        if not path_str.startswith("/mnt/"):
            return False

        # Check if it's a Windows drive mount (single letter after /mnt/)
        parts = path_str.split("/")
        if len(parts) >= 3:
            potential_drive = parts[2]
            if len(potential_drive) == 1 and potential_drive.isalpha():
                return True

        return False

    @staticmethod
    def _detect_chmod_support(
        os_type: str,
        filesystem: str,
        is_cross_filesystem: bool
    ) -> bool:
        """
        Determine if the filesystem supports chmod operations.

        Unix-like filesystems (ext4, btrfs, xfs, apfs, hfs+) support chmod.
        NTFS and FAT32 do not support Unix permissions.
        Cross-filesystem in WSL (ntfs-wsl) does not support chmod.
        """
        # Cross-filesystem in WSL - chmod not supported
        if is_cross_filesystem:
            return False

        # NTFS filesystems don't support Unix chmod
        if filesystem in ("ntfs", "ntfs-wsl", "fat32"):
            return False

        # Native Windows doesn't use Unix chmod
        if os_type == "Windows":
            return False

        # Unix-like filesystems support chmod
        if filesystem in ("ext4", "btrfs", "xfs", "apfs", "hfs+"):
            return True

        # Default to True for unknown Linux/Darwin filesystems
        if os_type in ("Linux", "Darwin"):
            return True

        return False

    @staticmethod
    def clear_cache() -> None:
        """Clear the detection result cache."""
        PlatformDetector._cache.clear()
