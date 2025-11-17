"""DevForgeAI - Spec-Driven Development Framework."""

__version__ = "1.0.0"
__author__ = "DevForgeAI"

from devforgeai.operation_context import (
    OperationContext,
    TodoItem,
    ErrorContext,
    ExtractionMetadata,
    extractOperationContext,
    ExtractorOptions,
    registerOperation,
    clearOperationStore,
)

__all__ = [
    "OperationContext",
    "TodoItem",
    "ErrorContext",
    "ExtractionMetadata",
    "extractOperationContext",
    "ExtractorOptions",
    "registerOperation",
    "clearOperationStore",
]
