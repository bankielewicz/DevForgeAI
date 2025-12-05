"""
Compatibility checker service for validating upgrade/downgrade safety.

Implements SVC-012 through SVC-014:
- Check if upgrade path is safe
- Return breaking changes for major upgrades
- Block unsafe downgrades without force flag
"""

from typing import Optional, Dict, Any

from installer.version_parser import Version
from installer.version_comparator import VersionComparator, CompareResult


class CompatibilityChecker:
    """Checks compatibility of version upgrade/downgrade paths."""

    def __init__(self) -> None:
        """Initialize compatibility checker."""
        self.comparator = VersionComparator()

    def _create_safe_result(
        self, is_breaking: bool = False, requires_confirmation: bool = False
    ) -> Dict[str, Any]:
        """
        Create a safe compatibility check result.

        Args:
            is_breaking: Whether this change has breaking changes
            requires_confirmation: Whether user confirmation is required

        Returns:
            Dict with safe result structure
        """
        return {
            "safe": True,
            "blocked": False,
            "warnings": [],
            "is_breaking": is_breaking,
            "requires_confirmation": requires_confirmation,
        }

    def _create_unsafe_result(
        self,
        warnings: Optional[list] = None,
        is_breaking: bool = False,
        blocked: bool = False,
        error_message: Optional[str] = None,
        exit_code: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Create an unsafe compatibility check result.

        Args:
            warnings: List of warning messages
            is_breaking: Whether this change has breaking changes
            blocked: Whether operation is blocked
            error_message: Error message if blocked
            exit_code: Exit code for blocked operations

        Returns:
            Dict with unsafe result structure
        """
        result: Dict[str, Any] = {
            "safe": False,
            "blocked": blocked,
            "warnings": warnings or [],
            "is_breaking": is_breaking,
            "requires_confirmation": True,
        }
        if error_message:
            result["error_message"] = error_message
        if exit_code is not None:
            result["exit_code"] = exit_code
        return result

    def check_compatibility(
        self, current: Optional[Version], target: Version, force: bool = False
    ) -> Dict[str, Any]:
        """
        Check if upgrade/downgrade is safe.

        Args:
            current: Current installed version (None for fresh install)
            target: Target version
            force: If True, allow unsafe downgrades

        Returns:
            Dict with keys:
            - safe: bool - Is this upgrade/downgrade safe?
            - warnings: list - List of warning messages
            - blocked: bool - Is operation blocked?
            - is_breaking: bool - Does this have breaking changes?
            - requires_confirmation: bool - Should user confirm?
            - error_message: str (optional) - Error message if blocked
            - exit_code: int (optional) - Exit code for blocked operations
        """
        # Fresh install is always safe
        if current is None:
            return self._create_safe_result()

        # Compare versions
        compare_result = self.comparator.compare(current, target)

        # Same version is safe (reinstall)
        if compare_result.relationship == "SAME":
            return self._create_safe_result()

        # Upgrade scenarios
        if compare_result.relationship == "UPGRADE":
            return self._check_upgrade(current, target, compare_result)

        # Downgrade scenarios
        if compare_result.relationship == "DOWNGRADE":
            return self._check_downgrade(current, target, force)

        # Default (shouldn't reach here)
        return self._create_safe_result()

    def _check_upgrade(
        self, current: Version, target: Version, compare_result: CompareResult
    ) -> Dict[str, Any]:
        """
        Check safety of upgrade path.

        Args:
            current: Current version
            target: Target version (guaranteed > current)
            compare_result: Result from version comparison

        Returns:
            Dict with upgrade compatibility info
        """
        # Patch and minor upgrades are always safe
        if compare_result.upgrade_type in ["PATCH", "MINOR"]:
            return self._create_safe_result()

        # Major upgrades from 0.x are safe (initial installation)
        if compare_result.upgrade_type == "MAJOR":
            # Upgrading from 0.x.x is considered safe (initial installation path)
            if current.major == 0:
                return self._create_safe_result()

            # Major upgrades from 1+ have breaking changes
            return self._create_unsafe_result(
                warnings=[
                    f"Major version upgrade from {current.major}.x to {target.major}.x",
                    "Breaking changes may have been introduced",
                    "Please review changelog before proceeding",
                ],
                is_breaking=True,
            )

        # Default: safe
        return self._create_safe_result()

    def _check_downgrade(
        self, current: Version, target: Version, force: bool
    ) -> Dict[str, Any]:
        """
        Check safety of downgrade path.

        Args:
            current: Current version (higher)
            target: Target version (lower)
            force: If True, allow downgrade

        Returns:
            Dict with downgrade compatibility info
        """
        # Block major downgrades unless force is True
        if target.major < current.major:
            if force:
                return self._create_unsafe_result(
                    warnings=[
                        f"Major version downgrade from {current.major}.x to {target.major}.x",
                        "Risk of data loss or incompatibility",
                        "Forced by --force flag",
                    ],
                    is_breaking=True,
                    blocked=False,
                )
            else:
                return self._create_unsafe_result(
                    warnings=[
                        f"Cannot downgrade from {current.major}.x to {target.major}.x",
                        "Major version downgrade may cause data loss",
                        "Incompatible configuration files",
                        "Missing required features",
                    ],
                    is_breaking=True,
                    blocked=True,
                    error_message=(
                        f"Downgrade blocked: {current} → {target}. "
                        "Use --force flag to override (use with caution)"
                    ),
                    exit_code=1,
                )

        # Minor/patch downgrades within same major version are not hard-blocked
        return {
            "safe": True,
            "blocked": False,
            "warnings": [
                f"Downgrade from {current.minor}.{current.patch} to {target.minor}.{target.patch}",
                "Some features may not be available after downgrade",
            ],
            "is_breaking": False,
            "requires_confirmation": False,
        }
