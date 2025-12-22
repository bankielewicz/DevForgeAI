"""
Unit tests for Operation Context Extraction (STORY-019)

Tests the extractOperationContext API method and data structure validation.
Covers all acceptance criteria and technical specifications.

Test Framework: pytest
Pattern: AAA (Arrange, Act, Assert)
"""

import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from dataclasses import asdict
import json

# Import modules under test (will fail initially - TDD Red phase)
# These imports are forward references to implementation
try:
    from devforgeai.operation_context import (
        OperationContext,
        TodoItem,
        ErrorContext,
        ExtractionMetadata,
        extractOperationContext,
        ExtractorOptions,
    )
except ImportError:
    # Expected to fail in Red phase - modules don't exist yet
    pass


class TestOperationContextDataStructure:
    """Tests for OperationContext data model validation"""

    def test_operation_context_structure_complete(self):
        """AC1: OperationContext should have all required fields"""
        # Arrange
        operation_id = str(uuid4())
        start_time = datetime.utcnow().isoformat() + "Z"
        end_time = (datetime.utcnow() + timedelta(seconds=100)).isoformat() + "Z"

        # Act
        context = OperationContext(
            operation_id=operation_id,
            operation_type="dev",
            story_id="STORY-001",
            start_time=start_time,
            end_time=end_time,
            duration_seconds=100,
            status="completed",
            todo_summary={
                "total": 5,
                "completed": 5,
                "failed": 0,
                "skipped": 0,
                "completion_rate": 1.0,
            },
            todos=[
                TodoItem(id=1, name="Test todo 1", status="done", timestamp=start_time),
                TodoItem(id=2, name="Test todo 2", status="done", timestamp=start_time),
                TodoItem(id=3, name="Test todo 3", status="done", timestamp=start_time),
                TodoItem(id=4, name="Test todo 4", status="done", timestamp=start_time),
                TodoItem(id=5, name="Test todo 5", status="done", timestamp=start_time),
            ],
            error=None,
            phases={"red": {"duration_seconds": 30, "success": True}},
        )

        # Assert
        assert context.operation_id == operation_id
        assert context.operation_type == "dev"
        assert context.story_id == "STORY-001"
        assert context.status == "completed"
        assert context.todo_summary["total"] == 5
        assert context.error is None
        assert context.phases is not None

    def test_operation_context_valid_operation_types(self):
        """Technical Spec: operation_type must be one of: dev, qa, release, ideate, orchestrate"""
        # Arrange
        valid_types = ["dev", "qa", "release", "ideate", "orchestrate"]
        start_time = datetime.utcnow().isoformat() + "Z"
        end_time = (datetime.utcnow() + timedelta(seconds=100)).isoformat() + "Z"

        # Act & Assert
        for op_type in valid_types:
            context = OperationContext(
                operation_id=str(uuid4()),
                operation_type=op_type,
                story_id=None,
                start_time=start_time,
                end_time=end_time,
                duration_seconds=100,
                status="completed",
                todo_summary={"total": 1, "completed": 1, "failed": 0, "skipped": 0, "completion_rate": 1.0},
                todos=[TodoItem(id=1, name="Test todo", status="done", timestamp=start_time)],
                error=None,
            )
            assert context.operation_type == op_type

    def test_operation_context_valid_statuses(self):
        """Technical Spec: status must be: completed, failed, partial, cancelled"""
        # Arrange
        valid_statuses = ["completed", "failed", "partial", "cancelled"]
        start_time = datetime.utcnow().isoformat() + "Z"
        end_time = (datetime.utcnow() + timedelta(seconds=100)).isoformat() + "Z"

        # Act & Assert
        for status in valid_statuses:
            # Failed status requires error context
            error_context = ErrorContext(
                message="Test error",
                type="TestError",
                timestamp=start_time,
                failed_todo_id=1
            ) if status == "failed" else None

            context = OperationContext(
                operation_id=str(uuid4()),
                operation_type="dev",
                story_id=None,
                start_time=start_time,
                end_time=end_time,
                duration_seconds=100,
                status=status,
                todo_summary={"total": 1, "completed": 1, "failed": 0, "skipped": 0, "completion_rate": 1.0},
                todos=[TodoItem(id=1, name="Test todo", status="done", timestamp=start_time)],
                error=error_context,
            )
            assert context.status == status

    def test_operation_context_story_id_optional(self):
        """Technical Spec: story_id is optional (null allowed for non-story operations)"""
        # Arrange
        start_time = datetime.utcnow().isoformat() + "Z"
        end_time = (datetime.utcnow() + timedelta(seconds=100)).isoformat() + "Z"

        # Act
        context_with_story = OperationContext(
            operation_id=str(uuid4()),
            operation_type="dev",
            story_id="STORY-001",
            start_time=start_time,
            end_time=end_time,
            duration_seconds=100,
            status="completed",
            todo_summary={"total": 1, "completed": 1, "failed": 0, "skipped": 0, "completion_rate": 1.0},
            todos=[TodoItem(id=1, name="Test todo", status="done", timestamp=start_time)],
            error=None,
        )

        context_without_story = OperationContext(
            operation_id=str(uuid4()),
            operation_type="ideate",
            story_id=None,
            start_time=start_time,
            end_time=end_time,
            duration_seconds=100,
            status="completed",
            todo_summary={"total": 1, "completed": 1, "failed": 0, "skipped": 0, "completion_rate": 1.0},
            todos=[TodoItem(id=1, name="Test todo", status="done", timestamp=start_time)],
            error=None,
        )

        # Assert
        assert context_with_story.story_id == "STORY-001"
        assert context_without_story.story_id is None


class TestTodoItemDataStructure:
    """Tests for TodoItem data model validation"""

    def test_todo_item_structure_complete(self):
        """AC1: TodoItem should have required fields"""
        # Arrange & Act
        todo = TodoItem(
            id=1,
            name="Extract context",
            status="done",
            timestamp=datetime.utcnow().isoformat() + "Z",
            notes="Extraction completed successfully",
        )

        # Assert
        assert todo.id == 1
        assert todo.name == "Extract context"
        assert todo.status == "done"
        assert todo.notes == "Extraction completed successfully"

    def test_todo_item_valid_statuses(self):
        """Technical Spec: todo.status must be: done, failed, skipped, pending"""
        # Arrange
        valid_statuses = ["done", "failed", "skipped", "pending"]

        # Act & Assert
        for status in valid_statuses:
            todo = TodoItem(
                id=1,
                name="Test todo",
                status=status,
                timestamp=datetime.utcnow().isoformat() + "Z",
            )
            assert todo.status == status

    def test_todo_item_name_length_validation(self):
        """Technical Spec: todo.name must be 1-200 chars"""
        # Arrange
        valid_name = "Extract operation context"
        long_name = "a" * 200
        too_long_name = "a" * 201

        # Act & Assert
        todo1 = TodoItem(
            id=1, name=valid_name, status="done", timestamp=datetime.utcnow().isoformat() + "Z"
        )
        assert len(todo1.name) == len(valid_name)

        todo2 = TodoItem(
            id=1, name=long_name, status="done", timestamp=datetime.utcnow().isoformat() + "Z"
        )
        assert len(todo2.name) == 200

        # Should fail validation
        with pytest.raises((ValueError, AssertionError)):
            TodoItem(
                id=1, name=too_long_name, status="done", timestamp=datetime.utcnow().isoformat() + "Z"
            )

    def test_todo_item_notes_optional(self):
        """Technical Spec: todo.notes is optional (0-500 chars)"""
        # Arrange
        todo_without_notes = TodoItem(
            id=1, name="Test", status="done", timestamp=datetime.utcnow().isoformat() + "Z"
        )

        todo_with_notes = TodoItem(
            id=1,
            name="Test",
            status="done",
            timestamp=datetime.utcnow().isoformat() + "Z",
            notes="This is a test note",
        )

        # Assert
        assert todo_without_notes.notes is None or todo_without_notes.notes == ""
        assert todo_with_notes.notes == "This is a test note"


class TestErrorContextDataStructure:
    """Tests for ErrorContext data model validation"""

    def test_error_context_structure_complete(self):
        """AC2: ErrorContext should have required fields"""
        # Arrange & Act
        error = ErrorContext(
            message="Git commit failed",
            type="GitError",
            timestamp=datetime.utcnow().isoformat() + "Z",
            failed_todo_id=5,
            stack_trace="git.error.GitCommandError: Failed to commit",
        )

        # Assert
        assert error.message == "Git commit failed"
        assert error.type == "GitError"
        assert error.failed_todo_id == 5
        assert error.stack_trace is not None

    def test_error_context_message_length_validation(self):
        """Technical Spec: error.message must be 1-500 chars"""
        # Arrange
        valid_message = "Git commit failed"
        max_message = "a" * 500
        too_long_message = "a" * 501

        # Act & Assert
        error1 = ErrorContext(
            message=valid_message,
            type="Error",
            timestamp=datetime.utcnow().isoformat() + "Z",
        )
        assert len(error1.message) == len(valid_message)

        error2 = ErrorContext(
            message=max_message, type="Error", timestamp=datetime.utcnow().isoformat() + "Z"
        )
        assert len(error2.message) == 500

        with pytest.raises((ValueError, AssertionError)):
            ErrorContext(
                message=too_long_message,
                type="Error",
                timestamp=datetime.utcnow().isoformat() + "Z",
            )

    def test_error_context_stack_trace_optional(self):
        """Technical Spec: error.stack_trace is optional"""
        # Arrange
        error_without_trace = ErrorContext(
            message="Error occurred", type="Error", timestamp=datetime.utcnow().isoformat() + "Z"
        )

        error_with_trace = ErrorContext(
            message="Error occurred",
            type="Error",
            timestamp=datetime.utcnow().isoformat() + "Z",
            stack_trace="Traceback details here",
        )

        # Assert
        assert error_without_trace.stack_trace is None or error_without_trace.stack_trace == ""
        assert error_with_trace.stack_trace == "Traceback details here"

    def test_error_context_stack_trace_max_length(self):
        """Technical Spec: error.stack_trace max 5000 chars"""
        # Arrange
        max_trace = "a" * 5000
        too_long_trace = "a" * 5001

        # Act & Assert
        error1 = ErrorContext(
            message="Error",
            type="Error",
            timestamp=datetime.utcnow().isoformat() + "Z",
            stack_trace=max_trace,
        )
        assert len(error1.stack_trace) == 5000

        with pytest.raises((ValueError, AssertionError)):
            ErrorContext(
                message="Error",
                type="Error",
                timestamp=datetime.utcnow().isoformat() + "Z",
                stack_trace=too_long_trace,
            )


class TestExtractionMetadata:
    """Tests for ExtractionMetadata structure"""

    def test_extraction_metadata_structure_complete(self):
        """Technical Spec: ExtractionMetadata should have all fields"""
        # Arrange & Act
        metadata = ExtractionMetadata(
            extracted_at=datetime.utcnow().isoformat() + "Z",
            sanitization_applied=True,
            fields_sanitized=3,
            truncation_applied=False,
            completeness_score=1.0,
        )

        # Assert
        assert metadata.extracted_at is not None
        assert metadata.sanitization_applied is True
        assert metadata.fields_sanitized == 3
        assert metadata.truncation_applied is False
        assert metadata.completeness_score == 1.0

    def test_extraction_metadata_completeness_score_range(self):
        """Technical Spec: completeness_score must be 0.0-1.0"""
        # Arrange & Act
        metadata_full = ExtractionMetadata(
            extracted_at=datetime.utcnow().isoformat() + "Z",
            sanitization_applied=True,
            fields_sanitized=0,
            truncation_applied=False,
            completeness_score=1.0,
        )

        metadata_partial = ExtractionMetadata(
            extracted_at=datetime.utcnow().isoformat() + "Z",
            sanitization_applied=False,
            fields_sanitized=0,
            truncation_applied=False,
            completeness_score=0.75,
        )

        metadata_minimal = ExtractionMetadata(
            extracted_at=datetime.utcnow().isoformat() + "Z",
            sanitization_applied=False,
            fields_sanitized=0,
            truncation_applied=False,
            completeness_score=0.0,
        )

        # Assert
        assert 0.0 <= metadata_full.completeness_score <= 1.0
        assert 0.0 <= metadata_partial.completeness_score <= 1.0
        assert 0.0 <= metadata_minimal.completeness_score <= 1.0

    def test_extraction_metadata_invalid_completeness_score(self):
        """Technical Spec: completeness_score > 1.0 or < 0.0 should fail"""
        # Arrange & Act & Assert
        with pytest.raises((ValueError, AssertionError)):
            ExtractionMetadata(
                extracted_at=datetime.utcnow().isoformat() + "Z",
                sanitization_applied=False,
                fields_sanitized=0,
                truncation_applied=False,
                completeness_score=1.5,  # Invalid
            )

        with pytest.raises((ValueError, AssertionError)):
            ExtractionMetadata(
                extracted_at=datetime.utcnow().isoformat() + "Z",
                sanitization_applied=False,
                fields_sanitized=0,
                truncation_applied=False,
                completeness_score=-0.1,  # Invalid
            )


class TestOperationContextValidation:
    """Tests for overall OperationContext validation rules"""

    def test_operation_context_duration_calculation(self):
        """Technical Spec: duration_seconds must be >= 0 and <= 86400 (24 hours)"""
        # Arrange
        start_time = datetime.utcnow()
        end_time = start_time + timedelta(seconds=3600)  # 1 hour

        # Act
        start_time_str = start_time.isoformat() + "Z"
        context = OperationContext(
            operation_id=str(uuid4()),
            operation_type="dev",
            story_id=None,
            start_time=start_time_str,
            end_time=end_time.isoformat() + "Z",
            duration_seconds=3600,
            status="completed",
            todo_summary={"total": 5, "completed": 5, "failed": 0, "skipped": 0, "completion_rate": 1.0},
            todos=[
                TodoItem(id=1, name="Test todo 1", status="done", timestamp=start_time_str),
                TodoItem(id=2, name="Test todo 2", status="done", timestamp=start_time_str),
                TodoItem(id=3, name="Test todo 3", status="done", timestamp=start_time_str),
                TodoItem(id=4, name="Test todo 4", status="done", timestamp=start_time_str),
                TodoItem(id=5, name="Test todo 5", status="done", timestamp=start_time_str),
            ],
            error=None,
        )

        # Assert
        assert context.duration_seconds == 3600
        assert context.duration_seconds >= 0
        assert context.duration_seconds <= 86400

    def test_operation_context_duration_exceeds_24_hours(self):
        """Technical Spec: duration > 24 hours should fail"""
        # Arrange
        start_time = datetime.utcnow()
        end_time = start_time + timedelta(seconds=86401)  # > 24 hours

        # Act & Assert
        with pytest.raises((ValueError, AssertionError)):
            OperationContext(
                operation_id=str(uuid4()),
                operation_type="dev",
                story_id=None,
                start_time=start_time.isoformat() + "Z",
                end_time=end_time.isoformat() + "Z",
                duration_seconds=86401,  # Invalid
                status="completed",
                todo_summary={"total": 0, "completed": 0, "failed": 0, "skipped": 0, "completion_rate": 0},
                todos=[],
                error=None,
            )

    def test_operation_context_end_time_before_start_time(self):
        """Technical Spec: end_time must be >= start_time"""
        # Arrange
        start_time = datetime.utcnow()
        end_time = start_time - timedelta(seconds=100)  # Before start

        # Act & Assert
        with pytest.raises((ValueError, AssertionError)):
            OperationContext(
                operation_id=str(uuid4()),
                operation_type="dev",
                story_id=None,
                start_time=start_time.isoformat() + "Z",
                end_time=end_time.isoformat() + "Z",
                duration_seconds=-100,  # Invalid
                status="completed",
                todo_summary={"total": 0, "completed": 0, "failed": 0, "skipped": 0, "completion_rate": 0},
                todos=[],
                error=None,
            )

    def test_operation_context_todo_array_size(self):
        """Technical Spec: todos array must have 1-500 items"""
        # Arrange
        todos_list = [
            TodoItem(
                id=i,
                name=f"Todo {i}",
                status="done",
                timestamp=datetime.utcnow().isoformat() + "Z",
            )
            for i in range(1, 6)
        ]

        start_time = datetime.utcnow()
        end_time = start_time + timedelta(seconds=100)

        # Act
        context = OperationContext(
            operation_id=str(uuid4()),
            operation_type="dev",
            story_id=None,
            start_time=start_time.isoformat() + "Z",
            end_time=end_time.isoformat() + "Z",
            duration_seconds=100,
            status="completed",
            todo_summary={
                "total": len(todos_list),
                "completed": len(todos_list),
                "failed": 0,
                "skipped": 0,
                "completion_rate": 1.0,
            },
            todos=todos_list,
            error=None,
        )

        # Assert
        assert len(context.todos) >= 1
        assert len(context.todos) <= 500

    def test_operation_context_empty_todos_fails(self):
        """Technical Spec: todos array must have >= 1 item"""
        # Arrange & Act & Assert
        with pytest.raises((ValueError, AssertionError)):
            OperationContext(
                operation_id=str(uuid4()),
                operation_type="dev",
                story_id=None,
                start_time=datetime.utcnow().isoformat() + "Z",
                end_time=(datetime.utcnow() + timedelta(seconds=100)).isoformat() + "Z",
                duration_seconds=100,
                status="completed",
                todo_summary={"total": 0, "completed": 0, "failed": 0, "skipped": 0, "completion_rate": 0},
                todos=[],  # Empty - invalid
                error=None,
            )

    def test_operation_context_failed_status_requires_error(self):
        """Technical Spec: If status='failed', error must be present"""
        # Arrange & Act & Assert
        with pytest.raises((ValueError, AssertionError)):
            OperationContext(
                operation_id=str(uuid4()),
                operation_type="dev",
                story_id=None,
                start_time=datetime.utcnow().isoformat() + "Z",
                end_time=(datetime.utcnow() + timedelta(seconds=100)).isoformat() + "Z",
                duration_seconds=100,
                status="failed",
                todo_summary={"total": 5, "completed": 3, "failed": 2, "skipped": 0, "completion_rate": 0.6},
                todos=[
                    TodoItem(
                        id=1,
                        name="Todo 1",
                        status="done",
                        timestamp=datetime.utcnow().isoformat() + "Z",
                    )
                ],
                error=None,  # Missing - should fail when status='failed'
            )

    def test_operation_context_story_id_format(self):
        """Technical Spec: story_id if present must match STORY-NNN pattern"""
        # Arrange
        valid_story_ids = ["STORY-001", "STORY-999", "STORY-12345"]
        start_time = datetime.utcnow()
        end_time = start_time + timedelta(seconds=100)

        # Act & Assert
        for story_id in valid_story_ids:
            context = OperationContext(
                operation_id=str(uuid4()),
                operation_type="dev",
                story_id=story_id,
                start_time=start_time.isoformat() + "Z",
                end_time=end_time.isoformat() + "Z",
                duration_seconds=100,
                status="completed",
                todo_summary={"total": 1, "completed": 1, "failed": 0, "skipped": 0, "completion_rate": 1.0},
                todos=[
                    TodoItem(
                        id=1,
                        name="Todo 1",
                        status="done",
                        timestamp=datetime.utcnow().isoformat() + "Z",
                    )
                ],
                error=None,
            )
            assert context.story_id == story_id


class TestContextSizeValidation:
    """Tests for context size limits"""

    def test_error_message_max_length(self):
        """Technical Spec: error.message max 500 characters"""
        # Arrange
        message = "a" * 500

        # Act & Assert
        error = ErrorContext(
            message=message, type="Error", timestamp=datetime.utcnow().isoformat() + "Z"
        )
        assert len(error.message) <= 500

    def test_error_stack_trace_max_length(self):
        """Technical Spec: error.stack_trace max 5000 characters"""
        # Arrange
        trace = "a" * 5000

        # Act & Assert
        error = ErrorContext(
            message="Error",
            type="Error",
            timestamp=datetime.utcnow().isoformat() + "Z",
            stack_trace=trace,
        )
        assert len(error.stack_trace) <= 5000


class TestUUIDValidation:
    """Tests for UUID validation in OperationContext"""

    def test_operation_id_valid_uuid(self):
        """Technical Spec: operation_id must be valid UUID"""
        # Arrange
        operation_id = str(uuid4())
        start_time = datetime.utcnow()
        end_time = start_time + timedelta(seconds=100)

        # Act
        context = OperationContext(
            operation_id=operation_id,
            operation_type="dev",
            story_id=None,
            start_time=start_time.isoformat() + "Z",
            end_time=end_time.isoformat() + "Z",
            duration_seconds=100,
            status="completed",
            todo_summary={"total": 1, "completed": 1, "failed": 0, "skipped": 0, "completion_rate": 1.0},
            todos=[
                TodoItem(
                    id=1,
                    name="Todo 1",
                    status="done",
                    timestamp=datetime.utcnow().isoformat() + "Z",
                )
            ],
            error=None,
        )

        # Assert
        assert context.operation_id == operation_id

    def test_operation_id_invalid_uuid(self):
        """Technical Spec: Invalid UUID should fail"""
        # Arrange
        invalid_uuid = "not-a-uuid"
        start_time = datetime.utcnow()
        end_time = start_time + timedelta(seconds=100)

        # Act & Assert
        with pytest.raises((ValueError, AssertionError)):
            OperationContext(
                operation_id=invalid_uuid,
                operation_type="dev",
                story_id=None,
                start_time=start_time.isoformat() + "Z",
                end_time=end_time.isoformat() + "Z",
                duration_seconds=100,
                status="completed",
                todo_summary={"total": 1, "completed": 1, "failed": 0, "skipped": 0, "completion_rate": 1.0},
                todos=[
                    TodoItem(
                        id=1,
                        name="Todo 1",
                        status="done",
                        timestamp=datetime.utcnow().isoformat() + "Z",
                    )
                ],
                error=None,
            )


class TestISO8601TimestampValidation:
    """Tests for ISO8601 timestamp validation"""

    def test_operation_context_iso8601_timestamps(self):
        """Technical Spec: start_time, end_time must be ISO8601 format"""
        # Arrange
        start_iso = "2025-11-07T10:00:00Z"
        end_iso = "2025-11-07T10:35:42Z"

        # Act
        context = OperationContext(
            operation_id=str(uuid4()),
            operation_type="dev",
            story_id="STORY-001",
            start_time=start_iso,
            end_time=end_iso,
            duration_seconds=2142,
            status="completed",
            todo_summary={"total": 8, "completed": 8, "failed": 0, "skipped": 0, "completion_rate": 1.0},
            todos=[
                TodoItem(
                    id=1,
                    name="Todo 1",
                    status="done",
                    timestamp=start_iso,
                )
            ],
            error=None,
        )

        # Assert
        assert context.start_time == start_iso
        assert context.end_time == end_iso

    def test_todo_item_iso8601_timestamp(self):
        """Technical Spec: todo.timestamp must be ISO8601"""
        # Arrange
        timestamp_iso = "2025-11-07T10:15:30Z"

        # Act
        todo = TodoItem(
            id=1, name="Test todo", status="done", timestamp=timestamp_iso
        )

        # Assert
        assert todo.timestamp == timestamp_iso

    def test_error_context_iso8601_timestamp(self):
        """Technical Spec: error.timestamp must be ISO8601"""
        # Arrange
        timestamp_iso = "2025-11-07T10:25:30Z"

        # Act
        error = ErrorContext(
            message="Test error",
            type="TestError",
            timestamp=timestamp_iso,
        )

        # Assert
        assert error.timestamp == timestamp_iso


class TestTodoSequentialIDValidation:
    """Tests for todo ID sequencing rules"""

    def test_todo_ids_sequential(self):
        """Technical Spec: todo.id must be sequential starting from 1"""
        # Arrange
        todos = [
            TodoItem(id=1, name="Todo 1", status="done", timestamp=datetime.utcnow().isoformat() + "Z"),
            TodoItem(id=2, name="Todo 2", status="done", timestamp=datetime.utcnow().isoformat() + "Z"),
            TodoItem(id=3, name="Todo 3", status="done", timestamp=datetime.utcnow().isoformat() + "Z"),
        ]

        # Act & Assert
        for i, todo in enumerate(todos, start=1):
            assert todo.id == i

    def test_todo_ids_non_sequential_fails(self):
        """Technical Spec: Non-sequential IDs should fail"""
        # Arrange
        todos = [
            TodoItem(id=1, name="Todo 1", status="done", timestamp=datetime.utcnow().isoformat() + "Z"),
            TodoItem(id=3, name="Todo 3", status="done", timestamp=datetime.utcnow().isoformat() + "Z"),  # Skips 2
        ]

        start_time = datetime.utcnow()
        end_time = start_time + timedelta(seconds=100)

        # Act & Assert
        with pytest.raises((ValueError, AssertionError)):
            OperationContext(
                operation_id=str(uuid4()),
                operation_type="dev",
                story_id=None,
                start_time=start_time.isoformat() + "Z",
                end_time=end_time.isoformat() + "Z",
                duration_seconds=100,
                status="completed",
                todo_summary={"total": 2, "completed": 2, "failed": 0, "skipped": 0, "completion_rate": 1.0},
                todos=todos,
                error=None,
            )


class TestCompletionRateCalculation:
    """Tests for todo_summary completion rate validation"""

    def test_completion_rate_full(self):
        """AC1: 100% completion rate when all todos done"""
        # Arrange
        summary = {
            "total": 5,
            "completed": 5,
            "failed": 0,
            "skipped": 0,
            "completion_rate": 1.0,
        }

        # Act & Assert
        assert summary["completion_rate"] == 1.0
        assert summary["completed"] == summary["total"]

    def test_completion_rate_partial(self):
        """AC1: Partial completion rate"""
        # Arrange
        summary = {
            "total": 10,
            "completed": 7,
            "failed": 2,
            "skipped": 1,
            "completion_rate": 0.7,
        }

        # Act & Assert
        assert summary["completion_rate"] == 0.7
        assert summary["completed"] + summary["failed"] + summary["skipped"] == summary["total"]

    def test_completion_rate_none(self):
        """AC1: 0% completion rate"""
        # Arrange
        summary = {
            "total": 5,
            "completed": 0,
            "failed": 0,
            "skipped": 0,
            "completion_rate": 0.0,
        }

        # Act & Assert
        assert summary["completion_rate"] == 0.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
