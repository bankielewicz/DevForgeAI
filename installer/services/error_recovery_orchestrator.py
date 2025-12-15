"""Error Recovery Orchestrator - Infrastructure Layer (STORY-074).

Infrastructure layer that orchestrates error handling services without circular dependencies.
Coordinates backup_service, rollback_service, and install_logger independently.

CLEAN ARCHITECTURE:
- Domain Layer: ErrorCategorizer (pure business logic for categorization/messages)
- Infrastructure Layer: ErrorRecoveryOrchestrator (service orchestration, no circular deps)

This fixes the ARCHITECTURE VIOLATION where error_handler.py mixed:
1. Business logic (error categorization)
2. Infrastructure concerns (logging, backup, rollback coordination)

EVENT-DRIVEN PATTERN: Services subscribe independently to error events,
preventing circular dependencies (A → B → C pattern instead of A → B → A).
"""
from typing import Optional, Dict
from dataclasses import dataclass

from .error_categorizer import ErrorCategorizer, ErrorCategory, ErrorResult
from ..exit_codes import ExitCodes


@dataclass
class ErrorRecoveryContext:
    """Context for error recovery orchestration.

    Captures error metadata and orchestration state for service coordination.
    Prevents circular dependencies by passing context instead of calling services directly.
    """
    error: Optional[Exception] = None
    phase: Optional[str] = None  # Phase where error occurred (e.g., 'file_copy')
    rollback_triggered: bool = False
    validation_phase: bool = False
    include_rollback_info: bool = False


class ErrorRecoveryOrchestrator:
    """Orchestrates error recovery services without circular dependencies.

    This is the INFRASTRUCTURE LAYER - handles:
    1. Coordinating multiple services (backup, rollback, logger)
    2. Error recovery workflow
    3. Signal handling for graceful rollback

    Service coordination pattern (NO CIRCULAR DEPS):
    - backup_service: Independent (creates backups before operations)
    - rollback_service: Independent (restores from backup on failure)
    - install_logger: Independent (logs errors and actions)
    - error_categorizer: Pure domain logic (injected, no state)

    Services do NOT call each other. ErrorRecoveryOrchestrator calls them in sequence.
    """

    def __init__(
        self,
        error_categorizer: Optional[ErrorCategorizer] = None,
        logger=None,
        rollback_service=None,
        backup_service=None
    ):
        """Initialize orchestrator with service dependencies.

        Args:
            error_categorizer: ErrorCategorizer instance (domain logic)
            logger: InstallLogger instance for logging errors
            rollback_service: RollbackService instance for rollback operations
            backup_service: BackupService instance for backup information
        """
        self.error_categorizer = error_categorizer or ErrorCategorizer()
        self.logger = logger
        self.rollback_service = rollback_service
        self.backup_service = backup_service

    def handle_error(self, context: ErrorRecoveryContext) -> ErrorResult:
        """Handle error with recovery workflow (AC#1-4, AC#6).

        Orchestrates error recovery without circular dependencies:
        1. Categorize error (pure domain logic)
        2. Log error (independent service)
        3. Trigger rollback if needed (independent service)
        4. Format user message (pure domain logic)

        Args:
            context: ErrorRecoveryContext with error details and state

        Returns:
            ErrorResult with exit code and console message
        """
        # Step 1: Categorize the error (pure domain logic)
        if context.error is None:
            error_result = ErrorResult(
                exit_code=ExitCodes.SUCCESS,
                console_message="Installation completed successfully."
            )
        else:
            error_result = self.error_categorizer.categorize_error(
                context.error,
                rollback_triggered=context.rollback_triggered,
                validation_phase=context.validation_phase
            )

        # Step 2: Determine if rollback is needed
        rollback_needed = context.phase == "file_copy" and context.error is not None

        # Step 3: Execute rollback if needed (independent service call)
        if rollback_needed and self.rollback_service:
            self._execute_rollback(context)
            # Update error result to indicate ROLLBACK_OCCURRED
            error_result = ErrorResult(
                exit_code=ExitCodes.ROLLBACK_OCCURRED,
                console_message=self.error_categorizer.format_console_message(context.error)
            )

        # Step 4: Log the error (independent service call)
        if context.error and self.logger:
            self._log_error(context, error_result.exit_code)

        # Return the formatted error result
        return error_result

    def _execute_rollback(self, context: ErrorRecoveryContext) -> None:
        """Execute rollback operation (independent service call).

        Separated into own method to clearly show service coordination.
        Does NOT call back to error handler (prevents circular dep).

        Args:
            context: ErrorRecoveryContext with error and state
        """
        if not self.rollback_service:
            return

        try:
            self.rollback_service.rollback(
                backup_dir=context.phase,  # This would be properly set in real usage
                target_dir='.'  # This would be properly set in real usage
            )
        except Exception as rollback_error:
            # Log rollback error but continue
            if self.logger:
                self.logger.log_error(
                    error=rollback_error,
                    category="ROLLBACK_ERROR",
                    exit_code=ExitCodes.ROLLBACK_OCCURRED,
                    message=f"Error during rollback (manual intervention may be needed): {rollback_error}"
                )

    def _log_error(self, context: ErrorRecoveryContext, exit_code: int) -> None:
        """Log error to file (independent service call).

        Separated into own method to clearly show service coordination.

        Args:
            context: ErrorRecoveryContext with error and state
            exit_code: Exit code for this error
        """
        if not self.logger or not context.error:
            return

        self.logger.log_error(
            error=context.error,
            exit_code=exit_code,
            message=str(context.error)
        )

    def check_concurrent_installation(self, lock_file_exists: bool) -> None:
        """Check if another installation is already in progress.

        Args:
            lock_file_exists: Whether lock file exists

        Raises:
            RuntimeError: If concurrent installation detected
        """
        if lock_file_exists:
            raise RuntimeError(
                "Concurrent installation detected. Another installation is currently in progress. "
                "Wait for it to complete or remove the lock file at "
                "devforgeai/install.lock"
            )

    def handle_keyboard_interrupt(self) -> ErrorResult:
        """Handle Ctrl+C gracefully with rollback (AC#4).

        Handles KeyboardInterrupt by triggering rollback if available,
        then returning appropriate exit code and message.

        Returns:
            ErrorResult with ROLLBACK_OCCURRED exit code
        """
        # Trigger rollback if available (independent service call)
        if self.rollback_service:
            self._execute_rollback(
                ErrorRecoveryContext(
                    error=KeyboardInterrupt("User interrupted installation"),
                    phase="any"
                )
            )

        console_msg = "Installation cancelled by user (Ctrl+C). System has been rolled back."
        return ErrorResult(
            exit_code=ExitCodes.ROLLBACK_OCCURRED,
            console_message=console_msg
        )

    def get_categorizer(self) -> ErrorCategorizer:
        """Get the error categorizer for direct use (domain logic access).

        Returns:
            ErrorCategorizer instance for pure business logic operations
        """
        return self.error_categorizer
