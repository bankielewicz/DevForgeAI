"""
ClaudeMdMergeService for orchestrating CLAUDE.md merge operations.

Requirements:
- SVC-001: Detect existing CLAUDE.md file presence
- SVC-002: Prompt user for merge strategy selection
- SVC-003: Execute auto-merge preserving user sections
- SVC-004: Detect merge conflicts
- SVC-005: Create timestamped backup before modification
- AC#1-AC#8: All acceptance criteria

CRITICAL REQUIREMENT: All methods MUST return MergeResult (never strings or dicts).
"""

from pathlib import Path
from datetime import datetime
from typing import Protocol, Optional, List

from ..models.merge_result import MergeResult, MergeStatus
from ..models.conflict_detail import ConflictDetail
from .markdown_parser import MarkdownParser
from .merge_backup_service import MergeBackupService
from .merge_conflict_detection_service import MergeConflictDetectionService
from ..config.merge_config import MergeConfig

# Placeholder for AskUserQuestion tool (real implementation in Claude)
def AskUserQuestion(*args, **kwargs):
    """Placeholder for AskUserQuestion tool invocation."""
    return "auto-merge"


class Logger(Protocol):
    """Logger protocol for dependency injection."""
    def log(self, message: str) -> None: ...


class ClaudeMdMergeService:
    """
    Orchestrate CLAUDE.md merge operations.

    Supports 4 strategies:
    1. auto-merge: Preserve user sections, update framework sections
    2. replace: Backup and overwrite with DevForgeAI template
    3. skip: Don't modify existing file
    4. manual: Create template file for manual merge
    """

    # Error message templates
    _ERROR_FILE_NOT_FOUND = "File not found: {}"
    _ERROR_MERGE_FAILED = "{} failed: {}"

    def __init__(self, logger: Optional[Logger] = None):
        """
        Initialize merge service with dependencies.

        Args:
            logger: Optional logger following ILogger protocol
        """
        self.logger = logger
        self.parser = MarkdownParser()
        self.backup_service = MergeBackupService(logger)
        self.conflict_service = MergeConflictDetectionService(logger)
        self._log = self.logger.log if logger else lambda msg: None

    def __getattr__(self, name: str):
        """
        Support strategy names with hyphens (e.g., "auto-merge" -> "auto_merge").

        Args:
            name: Attribute name (may contain hyphens for strategy names)

        Returns:
            Method reference or raises AttributeError
        """
        # Convert hyphenated strategy names to underscore method names
        strategy_name = name.replace("-", "_")
        if hasattr(type(self), strategy_name):
            return getattr(self, strategy_name)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def merge(
        self,
        claudemd_path: Path,
        framework_template: str,
        strategy: str = "auto-merge"
    ) -> MergeResult:
        """
        Orchestrate merge operation using specified strategy.

        Args:
            claudemd_path: Path to existing CLAUDE.md
            framework_template: DevForgeAI framework template content
            strategy: Merge strategy (auto-merge, replace, skip, manual)

        Returns:
            MergeResult with operation outcome

        Raises:
            ValueError: If strategy is invalid
        """
        self._validate_strategy(strategy)

        if strategy == "auto-merge":
            return self.auto_merge(claudemd_path, framework_template)
        elif strategy == "replace":
            return self.replace(claudemd_path, framework_template)
        elif strategy == "skip":
            return self.skip(claudemd_path)
        elif strategy == "manual":
            return self.manual(claudemd_path, framework_template)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

    def detect_existing(self, directory: Path) -> bool:
        """
        Detect if CLAUDE.md file exists.

        Requirement: SVC-001 - Detect existing CLAUDE.md file presence

        Args:
            directory: Directory to check

        Returns:
            True if CLAUDE.md exists, False otherwise
        """
        directory = Path(directory)
        claudemd_path = directory / "CLAUDE.md"
        exists = claudemd_path.exists()
        self._log(f"CLAUDE.md detection: exists={exists} at {claudemd_path}")
        return exists

    def select_strategy(self) -> str:
        """
        Prompt user to select merge strategy.

        Requirement: SVC-002 - Prompt user for merge strategy selection

        Returns:
            Strategy name: "auto-merge", "replace", "skip", or "manual"
        """
        # Call AskUserQuestion tool (can be mocked in tests)
        strategy = AskUserQuestion(
            question="Select merge strategy for existing CLAUDE.md:",
            options=[
                {"label": "auto-merge", "description": "Preserve user sections, update framework"},
                {"label": "replace", "description": "Backup and overwrite with template"},
                {"label": "skip", "description": "Don't modify existing file"},
                {"label": "manual", "description": "Manual merge with reference files"},
            ]
        )
        return strategy if strategy in {"auto-merge", "replace", "skip", "manual"} else "auto-merge"

    def _validate_strategy(self, strategy: str) -> bool:
        """
        Validate that strategy is one of the 4 supported strategies.

        Args:
            strategy: Strategy name to validate

        Returns:
            True if valid

        Raises:
            ValueError: If strategy not supported
        """
        valid = {"auto-merge", "replace", "skip", "manual"}
        if strategy not in valid:
            raise ValueError(f"Invalid strategy: {strategy}. Must be one of {valid}")
        return True

    def _create_error_result(
        self,
        strategy: str,
        timestamp: str,
        exception: Exception,
        operation_name: str = "Operation"
    ) -> MergeResult:
        """
        Create a MergeResult with error status for consistent error handling.

        Args:
            strategy: Strategy name for the result
            timestamp: ISO 8601 timestamp of operation
            exception: Exception that was raised
            operation_name: Name of operation that failed

        Returns:
            MergeResult with ERROR status
        """
        error_msg = self._ERROR_MERGE_FAILED.format(operation_name, str(exception))
        return MergeResult(
            status=MergeStatus.ERROR,
            strategy=strategy,
            error_message=error_msg,
            timestamp=timestamp
        )

    def auto_merge(self, claudemd_path: Path, framework_template: str) -> MergeResult:
        """
        Execute auto-merge strategy.

        Requirements:
        - SVC-003: Execute auto-merge preserving user sections
        - SVC-004: Detect merge conflicts
        - SVC-005: Create timestamped backup before modification
        - BR-001: Backup MUST be created before any file modification
        - BR-002: User sections preserved verbatim
        - BR-003: Conflicts trigger user escalation

        Args:
            claudemd_path: Path to existing CLAUDE.md
            framework_template: DevForgeAI framework template content

        Returns:
            MergeResult with status, merged_content, conflicts

        Raises:
            FileNotFoundError: If CLAUDE.md doesn't exist
            PermissionError: If no read/write permission
        """
        claudemd_path = Path(claudemd_path)
        timestamp = datetime.now().isoformat()

        # Validate file exists before attempting backup
        if not claudemd_path.exists():
            raise FileNotFoundError(f"CLAUDE.md not found: {claudemd_path}")

        # Check permissions early
        import os
        if not os.access(claudemd_path, os.R_OK):
            raise PermissionError(f"Cannot read CLAUDE.md: {claudemd_path}")
        if not os.access(claudemd_path.parent, os.W_OK):
            raise PermissionError(f"Cannot write to directory: {claudemd_path.parent}")

        try:
            # Step 1: Create backup before modification (BR-001)
            backup_path = self.backup_service.create_backup(claudemd_path, self.logger)

            # Verify backup
            if not self.backup_service.verify_backup(claudemd_path, backup_path):
                return MergeResult(
                    status=MergeStatus.ERROR,
                    strategy="auto-merge",
                    backup_path=backup_path,
                    error_message="Backup verification failed",
                    timestamp=timestamp
                )

            # Step 2: Read existing content
            existing_content = claudemd_path.read_text(encoding="utf-8")

            # Step 3: Detect conflicts
            conflict_result = self.conflict_service.detect_conflicts(existing_content, framework_template)

            if conflict_result["has_conflicts"]:
                # Conflicts found - return USER_INTERVENTION status
                return MergeResult(
                    status=MergeStatus.CONFLICT_DETECTED,
                    strategy="auto-merge",
                    backup_path=backup_path,
                    conflicts=conflict_result["conflicts"],
                    error_message="Conflicts detected during auto-merge",
                    timestamp=timestamp
                )

            # Step 4: Merge content (preserve user sections, update framework)
            merged_content = self._perform_merge(
                existing_content,
                framework_template,
                conflict_result["user_sections"],
                conflict_result["framework_sections"]
            )

            self._log(f"Auto-merge completed successfully for {claudemd_path}")

            return MergeResult(
                status=MergeStatus.SUCCESS,
                strategy="auto-merge",
                merged_content=merged_content,
                backup_path=backup_path,
                timestamp=timestamp
            )

        except FileNotFoundError as e:
            return MergeResult(
                status=MergeStatus.ERROR,
                strategy="auto-merge",
                error_message=self._ERROR_FILE_NOT_FOUND.format(str(e)),
                timestamp=timestamp
            )
        except (PermissionError, OSError, ValueError) as e:
            return self._create_error_result("auto-merge", timestamp, e, "Auto-merge")

    def replace(
        self,
        claudemd_path: Path,
        framework_template: str
    ) -> MergeResult:
        """
        Execute replace strategy.

        Requirements:
        - AC#5: Replace strategy with backup
        - SVC-005: Create timestamped backup before modification
        - BR-001: Backup MUST be created before any file modification

        Args:
            claudemd_path: Path to existing CLAUDE.md
            framework_template: DevForgeAI framework template content

        Returns:
            MergeResult with status and backup_path
        """
        claudemd_path = Path(claudemd_path)
        timestamp = datetime.now().isoformat()

        try:
            # Step 1: Create backup before modification
            backup_path = self.backup_service.create_backup(claudemd_path, self.logger)

            # Verify backup
            if not self.backup_service.verify_backup(claudemd_path, backup_path):
                return MergeResult(
                    status=MergeStatus.ERROR,
                    strategy="replace",
                    backup_path=backup_path,
                    error_message="Backup verification failed",
                    timestamp=timestamp
                )

            # Step 2: Overwrite with template
            claudemd_path.write_text(framework_template, encoding="utf-8")

            self._log(f"Replace completed for {claudemd_path}, backup: {backup_path}")

            return MergeResult(
                status=MergeStatus.SUCCESS,
                strategy="replace",
                merged_content=framework_template,
                backup_path=backup_path,
                timestamp=timestamp
            )

        except FileNotFoundError as e:
            return MergeResult(
                status=MergeStatus.ERROR,
                strategy="replace",
                error_message=self._ERROR_FILE_NOT_FOUND.format(str(e)),
                timestamp=timestamp
            )
        except (PermissionError, OSError, ValueError) as e:
            return self._create_error_result("replace", timestamp, e, "Replace")

    def skip(self, claudemd_path: Path) -> MergeResult:
        """
        Execute skip strategy.

        Requirements:
        - AC#6: Skip strategy preservation
        - BR-004: Skip strategy never modifies files

        Args:
            claudemd_path: Path to existing CLAUDE.md (not modified)

        Returns:
            MergeResult with SKIPPED status
        """
        claudemd_path = Path(claudemd_path)
        timestamp = datetime.now().isoformat()

        self._log(f"Skip strategy: CLAUDE.md not modified at {claudemd_path}")

        return MergeResult(
            status=MergeStatus.SKIPPED,
            strategy="skip",
            timestamp=timestamp
        )

    def manual(
        self,
        claudemd_path: Path,
        framework_template: str
    ) -> MergeResult:
        """
        Execute manual resolution workflow.

        Requirements:
        - AC#7: Manual resolution workflow
        - SVC-005: Create timestamped backup before modification

        Args:
            claudemd_path: Path to existing CLAUDE.md
            framework_template: DevForgeAI framework template content

        Returns:
            MergeResult with USER_INTERVENTION status
        """
        claudemd_path = Path(claudemd_path)
        timestamp = datetime.now().isoformat()

        try:
            # Step 1: Create backup
            backup_path = self.backup_service.create_backup(claudemd_path, self.logger)

            # Step 2: Create template reference file
            template_path = claudemd_path.parent / "CLAUDE.md.devforgeai-template"
            template_path.write_text(framework_template, encoding="utf-8")

            self._log(f"Manual merge workflow initiated: template written to {template_path}")

            return MergeResult(
                status=MergeStatus.USER_INTERVENTION,
                strategy="manual",
                backup_path=backup_path,
                error_message="User manual resolution required",
                timestamp=timestamp
            )

        except (FileNotFoundError, PermissionError, OSError, ValueError) as e:
            return self._create_error_result("manual", timestamp, e, "Manual workflow setup")

    def _perform_merge(
        self,
        user_content: str,
        framework_content: str,
        user_sections: List[dict],
        framework_sections: List[dict]
    ) -> str:
        """
        Perform actual merge (preserve user sections, update framework).

        Algorithm:
        1. Start with framework template
        2. Find user sections that aren't framework sections
        3. Insert user sections at their original positions (if exists in framework)
        4. Or append user sections at end if not in framework

        Args:
            user_content: Existing CLAUDE.md content
            framework_content: Framework template content
            user_sections: Parsed user sections
            framework_sections: Parsed framework sections

        Returns:
            Merged content string
        """
        # Start with framework as base
        merged = framework_content

        # For each user section that's not a framework section, preserve it
        for user_section in user_sections:
            section_name = user_section.get("title", "")
            is_framework = MergeConfig.is_framework_section(section_name)

            if not is_framework:
                # User-created section - preserve verbatim
                section_content = user_section.get("content", "")
                section_header = f"## {section_name}" if section_name else ""

                if section_header and section_content:
                    user_section_text = f"{section_header}\n\n{section_content}"
                    # Append user section if not already in merged content
                    if section_header not in merged:
                        merged += f"\n\n{user_section_text}"

        return merged
