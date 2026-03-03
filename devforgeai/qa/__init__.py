"""
DevForgeAI QA Module.

Provides quality assurance validation utilities including regression classification.
"""

from devforgeai.qa.regression_classifier import (
    # AC#1: Changed file detection
    get_changed_files,
    get_changed_files_safe,
    is_git_repository,
    is_first_commit,
    # AC#2: Classification
    classify_violation,
    classify_violations,
    classify_violations_with_fallback,
    # AC#3: Blocking status
    set_blocking_status,
    set_all_blocking_status,
    should_block_qa,
    count_blocking,
    count_non_blocking,
    # AC#4: Display
    format_breakdown,
    get_breakdown,
    count_regressions,
    count_pre_existing,
    generate_classification_summary,
    # Integration
    run_classification_workflow,
    generate_qa_report_section,
    generate_detailed_report,
)

__all__ = [
    # AC#1
    "get_changed_files",
    "get_changed_files_safe",
    "is_git_repository",
    "is_first_commit",
    # AC#2
    "classify_violation",
    "classify_violations",
    "classify_violations_with_fallback",
    # AC#3
    "set_blocking_status",
    "set_all_blocking_status",
    "should_block_qa",
    "count_blocking",
    "count_non_blocking",
    # AC#4
    "format_breakdown",
    "get_breakdown",
    "count_regressions",
    "count_pre_existing",
    "generate_classification_summary",
    # Integration
    "run_classification_workflow",
    "generate_qa_report_section",
    "generate_detailed_report",
]
