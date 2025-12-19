"""
Context Extraction for DevForgeAI Feedback Hook System.

Implements the context extraction patterns documented in STORY-103:
- Extract operation context from TodoWrite state
- Sanitize secrets and PII
- Apply size limits and summarization
- Support graceful degradation

Performance targets (NFR-P1):
- Extraction completes in <200ms
- Context size <= 50KB
- Summarization for >100 todos
"""

import json
import logging
import re
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# =============================================================================
# Data Models (from STORY-103 specification)
# =============================================================================

@dataclass
class TodoContext:
    """Represents a single todo item extracted from TodoWrite."""
    content: str
    status: str  # pending, in_progress, completed
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration_seconds: Optional[float] = None


@dataclass
class ErrorContext:
    """Represents error details when operation failed."""
    message: str
    failed_todo: Optional[str] = None
    stack_trace: Optional[str] = None
    error_type: Optional[str] = None


@dataclass
class OperationContext:
    """Represents extracted operation context for feedback."""
    operation_id: str
    operation_type: str  # dev, qa, release, orchestrate
    story_id: Optional[str]
    start_time: str
    end_time: str
    duration_seconds: float
    status: str  # success, failure, partial
    todos: List[TodoContext] = field(default_factory=list)
    error: Optional[ErrorContext] = None
    phases: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


# =============================================================================
# Sanitization Patterns (from STORY-103 context-sanitization.md)
# =============================================================================

# Secret patterns to remove
SECRET_PATTERNS = [
    r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\']?[\w-]+["\']?',
    r'(?i)(secret|password|passwd|pwd)\s*[=:]\s*["\']?[\w-]+["\']?',
    r'(?i)(token|auth[_-]?token)\s*[=:]\s*["\']?[\w-]+["\']?',
    r'(?i)(aws[_-]?access[_-]?key[_-]?id)\s*[=:]\s*["\']?[\w-]+["\']?',
    r'(?i)(aws[_-]?secret[_-]?access[_-]?key)\s*[=:]\s*["\']?[\w-]+["\']?',
    r'-----BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----[\s\S]*?-----END (RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----',
]

# PII patterns to remove
PII_PATTERNS = [
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
    r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # Phone (US format)
    r'\b\d{3}[-]?\d{2}[-]?\d{4}\b',  # SSN
]

# File path patterns that may contain credentials
CREDENTIAL_PATH_PATTERNS = [
    r'(?i)/\S*credential\S*',
    r'(?i)/\S*secret\S*',
    r'(?i)/\S*password\S*',
    r'(?i)/\.env\S*',
]


# =============================================================================
# Size and Performance Constants
# =============================================================================

MAX_CONTEXT_SIZE_KB = 50
MAX_TODOS_BEFORE_SUMMARY = 100
SUMMARY_FIRST_TODOS = 50
SUMMARY_LAST_TODOS = 10
MAX_STACK_TRACE_SIZE_KB = 5
STACK_TRACE_TRUNCATE_KB = 2
EXTRACTION_TIMEOUT_MS = 200


# =============================================================================
# Sanitization Functions
# =============================================================================

def sanitize_text(text: str) -> str:
    """
    Remove secrets and PII from text.

    Args:
        text: Input text to sanitize

    Returns:
        Sanitized text with secrets/PII replaced by [REDACTED]
    """
    if not text:
        return text

    sanitized = text
    redacted_count = 0

    # Remove secrets
    for pattern in SECRET_PATTERNS:
        matches = re.findall(pattern, sanitized)
        if matches:
            redacted_count += len(matches)
            sanitized = re.sub(pattern, '[REDACTED_SECRET]', sanitized)

    # Remove PII
    for pattern in PII_PATTERNS:
        matches = re.findall(pattern, sanitized)
        if matches:
            redacted_count += len(matches)
            sanitized = re.sub(pattern, '[REDACTED_PII]', sanitized)

    # Remove credential file paths
    for pattern in CREDENTIAL_PATH_PATTERNS:
        matches = re.findall(pattern, sanitized)
        if matches:
            redacted_count += len(matches)
            sanitized = re.sub(pattern, '[REDACTED_PATH]', sanitized)

    if redacted_count > 0:
        logger.debug(f"Sanitization: removed {redacted_count} sensitive patterns")

    return sanitized


def truncate_stack_trace(stack_trace: str) -> str:
    """
    Truncate stack trace to 5KB limit.

    Pattern: Keep first 2KB + marker + last 2KB if over limit.

    Args:
        stack_trace: Full stack trace

    Returns:
        Truncated stack trace if needed
    """
    if not stack_trace:
        return stack_trace

    size_kb = len(stack_trace.encode('utf-8')) / 1024

    if size_kb <= MAX_STACK_TRACE_SIZE_KB:
        return stack_trace

    # Truncate to 2KB start + 2KB end
    bytes_limit = int(STACK_TRACE_TRUNCATE_KB * 1024)
    encoded = stack_trace.encode('utf-8')

    start_part = encoded[:bytes_limit].decode('utf-8', errors='ignore')
    end_part = encoded[-bytes_limit:].decode('utf-8', errors='ignore')

    truncated_bytes = len(encoded) - (bytes_limit * 2)
    marker = f"\n\n[... {truncated_bytes} bytes truncated ...]\n\n"

    return start_part + marker + end_part


# =============================================================================
# Summarization Functions
# =============================================================================

def summarize_todos(todos: List[Dict[str, Any]]) -> List[TodoContext]:
    """
    Summarize large todo lists (>100 items).

    Pattern: First 50 + summary marker + last 10.

    Args:
        todos: List of todo dicts from TodoWrite

    Returns:
        List of TodoContext with summarization applied
    """
    if len(todos) <= MAX_TODOS_BEFORE_SUMMARY:
        return [_dict_to_todo_context(t) for t in todos]

    # Keep first 50
    first_todos = [_dict_to_todo_context(t) for t in todos[:SUMMARY_FIRST_TODOS]]

    # Add summary marker
    omitted_count = len(todos) - SUMMARY_FIRST_TODOS - SUMMARY_LAST_TODOS
    completed_count = sum(1 for t in todos[SUMMARY_FIRST_TODOS:-SUMMARY_LAST_TODOS]
                         if t.get('status') == 'completed')

    summary = TodoContext(
        content=f"[SUMMARY: {omitted_count} todos omitted ({completed_count} completed)]",
        status="summary"
    )

    # Keep last 10
    last_todos = [_dict_to_todo_context(t) for t in todos[-SUMMARY_LAST_TODOS:]]

    logger.debug(f"Summarized {len(todos)} todos → {len(first_todos)} + 1 + {len(last_todos)}")

    return first_todos + [summary] + last_todos


def _dict_to_todo_context(todo_dict: Dict[str, Any]) -> TodoContext:
    """Convert todo dict to TodoContext dataclass."""
    return TodoContext(
        content=sanitize_text(str(todo_dict.get('content', ''))),
        status=todo_dict.get('status', 'pending'),
        start_time=todo_dict.get('start_time'),
        end_time=todo_dict.get('end_time'),
        duration_seconds=todo_dict.get('duration_seconds'),
    )


# =============================================================================
# Context Extraction
# =============================================================================

def extract_operation_context(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract operation context for feedback conversations.

    Implements 6-step pattern from STORY-103 context-extraction.md:
    1. Read TodoWrite state
    2. Extract todo items with timing
    3. Determine operation status
    4. Calculate timing
    5. Extract error context (if failure)
    6. Sanitize before return

    Args:
        raw_data: Dict containing operation data with keys:
            - todos: List of todo dicts
            - operation_type: str (dev, qa, release, orchestrate)
            - story_id: Optional[str]
            - error: Optional error info
            - phases: Optional list of phases

    Returns:
        Dict representation of OperationContext, safe for serialization.
        Returns empty dict on complete failure (graceful degradation).
    """
    start_time = time.perf_counter()

    try:
        # Step 1: Read TodoWrite state (simulated - data passed in)
        todos_raw = raw_data.get('todos', [])

        # Step 2: Extract todo items (with summarization if needed)
        todos = summarize_todos(todos_raw)

        # Step 3: Determine operation status
        status = _determine_status(todos_raw, raw_data.get('error'))

        # Step 4: Calculate timing
        timing = _calculate_timing(todos_raw, raw_data)

        # Step 5: Extract error context (if failure)
        error_context = None
        if status == 'failure' and raw_data.get('error'):
            error_context = _extract_error_context(raw_data['error'])

        # Construct OperationContext
        context = OperationContext(
            operation_id=raw_data.get('operation_id', str(uuid.uuid4())),
            operation_type=raw_data.get('operation_type', 'unknown'),
            story_id=raw_data.get('story_id'),
            start_time=timing['start_time'],
            end_time=timing['end_time'],
            duration_seconds=timing['duration_seconds'],
            status=status,
            todos=[asdict(t) for t in todos],
            error=asdict(error_context) if error_context else None,
            phases=raw_data.get('phases', []),
            metadata=raw_data.get('metadata', {}),
        )

        # Step 6: Sanitize and apply size limits
        result = _apply_size_limits(asdict(context))

        # Log performance
        duration_ms = (time.perf_counter() - start_time) * 1000
        if duration_ms > EXTRACTION_TIMEOUT_MS:
            logger.warning(f"Context extraction took {duration_ms:.2f}ms (target: {EXTRACTION_TIMEOUT_MS}ms)")
        else:
            logger.debug(f"Context extraction completed in {duration_ms:.2f}ms")

        return result

    except Exception as e:
        # Graceful degradation: return empty context on error
        logger.warning(f"Context extraction failed (graceful degradation): {e}")
        return {}


def _determine_status(todos: List[Dict], error: Optional[Dict]) -> str:
    """
    Determine operation status from todos and error info.

    Returns:
        'success' if all todos completed
        'failure' if error present or any todos failed
        'partial' if mixed results
    """
    if error:
        return 'failure'

    if not todos:
        return 'success'

    completed_count = sum(1 for t in todos if t.get('status') == 'completed')
    failed_count = sum(1 for t in todos if t.get('status') == 'failed')
    total = len(todos)

    if failed_count > 0:
        return 'failure'
    elif completed_count == total:
        return 'success'
    else:
        return 'partial'


def _calculate_timing(todos: List[Dict], raw_data: Dict) -> Dict[str, Any]:
    """
    Calculate start_time, end_time, duration from todos or raw_data.

    Returns:
        Dict with start_time, end_time, duration_seconds
    """
    utc_now = datetime.now(timezone.utc)
    iso_now = utc_now.isoformat(timespec='seconds').replace('+00:00', 'Z')

    # Try to get from raw_data first
    start_time = raw_data.get('start_time', iso_now)
    end_time = raw_data.get('end_time', iso_now)
    duration = raw_data.get('duration_seconds', 0)

    # If no explicit timing, calculate from todos
    if not raw_data.get('start_time') and todos:
        todo_starts = [t.get('start_time') for t in todos if t.get('start_time')]
        todo_ends = [t.get('end_time') for t in todos if t.get('end_time')]

        if todo_starts:
            start_time = min(todo_starts)
        if todo_ends:
            end_time = max(todo_ends)

        # Calculate duration from todo durations
        todo_durations = [t.get('duration_seconds', 0) for t in todos if t.get('duration_seconds')]
        if todo_durations:
            duration = sum(todo_durations)

    return {
        'start_time': start_time,
        'end_time': end_time,
        'duration_seconds': duration,
    }


def _extract_error_context(error_data: Dict) -> ErrorContext:
    """
    Extract error context from error data.

    Args:
        error_data: Dict with error info

    Returns:
        ErrorContext dataclass
    """
    message = sanitize_text(str(error_data.get('message', 'Unknown error')))
    failed_todo = sanitize_text(str(error_data.get('failed_todo', ''))) if error_data.get('failed_todo') else None
    stack_trace = error_data.get('stack_trace', '')

    # Sanitize and truncate stack trace
    if stack_trace:
        stack_trace = sanitize_text(stack_trace)
        stack_trace = truncate_stack_trace(stack_trace)

    return ErrorContext(
        message=message,
        failed_todo=failed_todo,
        stack_trace=stack_trace,
        error_type=error_data.get('error_type'),
    )


def _apply_size_limits(context: Dict) -> Dict:
    """
    Apply 50KB size limit to serialized context.

    If over limit, progressively remove data to fit.
    """
    serialized = json.dumps(context)
    size_kb = len(serialized.encode('utf-8')) / 1024

    if size_kb <= MAX_CONTEXT_SIZE_KB:
        return context

    logger.warning(f"Context size ({size_kb:.2f}KB) exceeds {MAX_CONTEXT_SIZE_KB}KB limit, truncating")

    # Progressive reduction:
    # 1. Truncate metadata
    if 'metadata' in context and context['metadata']:
        context['metadata'] = {'truncated': True}

    # 2. Reduce todo content length
    if 'todos' in context:
        for todo in context['todos']:
            if len(todo.get('content', '')) > 100:
                todo['content'] = todo['content'][:100] + '...'

    # 3. Truncate error stack trace further
    if context.get('error') and context['error'].get('stack_trace'):
        trace = context['error']['stack_trace']
        if len(trace) > 1000:
            context['error']['stack_trace'] = trace[:500] + '\n[truncated]\n' + trace[-500:]

    # Check final size
    final_serialized = json.dumps(context)
    final_size_kb = len(final_serialized.encode('utf-8')) / 1024

    if final_size_kb > MAX_CONTEXT_SIZE_KB:
        logger.error(f"Context still too large ({final_size_kb:.2f}KB) after truncation")

    return context
