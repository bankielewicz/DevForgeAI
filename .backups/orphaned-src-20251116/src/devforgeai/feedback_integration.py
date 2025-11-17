"""
Feedback System Integration

Integrates operation context with feedback conversation system.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import asdict

from devforgeai.operation_context import OperationContext
from devforgeai.operation_history import OperationHistory, update_operation_history, updateOperationHistory
from devforgeai.sanitization import sanitize_context


def prepopulate_feedback_template(context: OperationContext) -> Dict[str, Any]:
    """
    Create feedback template pre-populated with operation metadata (snake_case preferred).

    Args:
        context: Operation context

    Returns:
        Feedback template dict with metadata and questions
    """
    # Build metadata section (read-only)
    metadata = {
        "operation_id": context.operation_id,
        "operation_type": context.operation_type,
        "status": context.status,
        "duration": context.duration_seconds,
        "todo_count": context.todo_summary.get("total", 0),
        "completion_rate": context.todo_summary.get("completion_rate", 0),
        "timestamp": context.start_time,
    }

    # Add error info if failed
    if context.status == "failed" and context.error:
        metadata["error"] = {
            "message": context.error.message,
            "type": context.error.type,
            "failed_todo_id": context.error.failed_todo_id,
        }

    # Generate questions based on status
    questions = []
    if context.status == "completed":
        questions = [
            "What went well during this operation?",
            "Were there any unexpected challenges?",
            "How confident are you in the results?",
        ]
        summary = f"Operation completed successfully in {context.duration_seconds} seconds with {context.todo_summary.get('total', 0)} todos."

    elif context.status == "failed":
        # Failed operation - focus on error
        failed_todo_id = context.error.failed_todo_id if context.error else None
        failed_todo_name = "unknown"
        if failed_todo_id:
            for todo in context.todos:
                if todo.id == failed_todo_id:
                    failed_todo_name = todo.name
                    break

        questions = [
            f"Tell us about the failure in '{failed_todo_name}' (todo #{failed_todo_id}).",
            "What was the root cause?",
            "What would you do differently next time?",
        ]
        summary = f"Operation failed during '{failed_todo_name}'. Error: {context.error.message if context.error else 'Unknown'}"

    elif context.status == "partial":
        questions = [
            "Which todos were completed successfully?",
            "Which todos failed and why?",
            "What impact does the partial completion have?",
        ]
        summary = f"Operation partially completed ({context.todo_summary.get('completion_rate', 0):.0%})."

    else:  # cancelled
        questions = [
            "Why was this operation cancelled?",
            "Can it be resumed?",
        ]
        summary = f"Operation was cancelled."

    # Build template
    template = {
        "metadata": metadata,
        "read_only": ["metadata"],
        "summary": summary,
        "questions": questions,
        "editable": True,
        "todo_context": {
            "total": context.todo_summary.get("total", 0),
            "completed": context.todo_summary.get("completed", 0),
            "failed": context.todo_summary.get("failed", 0),
            "skipped": context.todo_summary.get("skipped", 0),
        },
    }

    return template


def pass_context_to_feedback(context: OperationContext) -> Dict[str, Any]:
    """
    Convert and sanitize operation context for feedback system (snake_case preferred).

    Args:
        context: Operation context to pass

    Returns:
        Feedback-friendly context dict (with PII/secrets redacted)
    """
    # Convert context to dict
    context_dict = asdict(context)

    # Sanitize sensitive data
    sanitized_context, sanitization_metadata = sanitize_context(context_dict)

    # Convert todos to simpler format for feedback
    todos_for_feedback = []
    for todo in context.todos:
        todos_for_feedback.append({
            "id": todo.id,
            "name": todo.name,
            "status": todo.status,
            "timestamp": todo.timestamp,
            "notes": todo.notes,
        })

    # Build feedback context
    feedback_context = {
        "operation_id": sanitized_context["operation_id"],
        "operation_type": sanitized_context["operation_type"],
        "status": sanitized_context["status"],
        "story_id": sanitized_context.get("story_id"),
        "duration_seconds": sanitized_context["duration_seconds"],
        "todos": todos_for_feedback,
        "todo_summary": sanitized_context["todo_summary"],
        "timing": {
            "start": sanitized_context["start_time"],
            "end": sanitized_context["end_time"],
            "duration_seconds": sanitized_context["duration_seconds"],
        },
    }

    # Add error if present
    if sanitized_context.get("error"):
        feedback_context["error"] = sanitized_context["error"]

    # Add phases if present
    if sanitized_context.get("phases"):
        feedback_context["phases"] = sanitized_context["phases"]

    # Add sanitization notice if data was redacted
    if sanitization_metadata["sanitization_applied"]:
        feedback_context["_sanitization_notice"] = f"Sensitive data redacted from {sanitization_metadata['fields_sanitized']} field(s)"

    # Add completeness warning if partial
    if context.extraction_metadata and context.extraction_metadata.completeness_score < 1.0:
        feedback_context["warnings"] = [
            "Limited context available: Some operation data could not be fully extracted"
        ]

    return feedback_context


# Backward compatibility aliases (camelCase - deprecated)
prepopulateFeedbackTemplate = prepopulate_feedback_template
passContextToFeedback = pass_context_to_feedback
