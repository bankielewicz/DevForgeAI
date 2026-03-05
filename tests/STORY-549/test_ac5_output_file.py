"""
Test: AC#5 - Output Written to pricing-model.md with Required Sections and Disclaimer
Story: STORY-549
Generated: 2026-03-04

Validates that output is written atomically to
devforgeai/specs/business/financial/pricing-model.md with all required sections.
"""
import os
import re
import pytest

FRAMEWORK_FILE = "src/claude/skills/managing-finances/references/pricing-strategy-framework.md"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUTPUT_FILE_PATH = "devforgeai/specs/business/financial/pricing-model.md"


@pytest.fixture
def framework_content():
    """Arrange: Read the pricing-strategy-framework.md file content."""
    path = os.path.join(PROJECT_ROOT, FRAMEWORK_FILE)
    assert os.path.exists(path), f"Source file does not exist: {FRAMEWORK_FILE}"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class TestOutputFilePath:
    """Tests that output is written to the correct path."""

    def test_should_reference_output_path_when_framework_loaded(self, framework_content):
        """AC5: pricing-model.md output path must be documented."""
        assert re.search(r"pricing-model\.md", framework_content, re.IGNORECASE), (
            "Output file path pricing-model.md not referenced in framework"
        )

    def test_should_reference_financial_directory_when_writing_output(self, framework_content):
        """AC5: Output path must include financial directory."""
        assert re.search(
            r"(business/financial|financial/pricing-model)",
            framework_content,
            re.IGNORECASE,
        ), (
            "Financial directory path not referenced in framework"
        )


class TestRequiredSections:
    """Tests that output file contains all required sections."""

    def test_should_include_strategy_name_header_when_output_written(self, framework_content):
        """AC5: Header with strategy name must be in output template."""
        assert re.search(
            r"(header|title|#).*strategy\s*(name|type|selected)",
            framework_content,
            re.IGNORECASE,
        ) or re.search(
            r"strategy\s*(name|type|selected).*(header|title|section)",
            framework_content,
            re.IGNORECASE,
        ), (
            "No strategy name header documented in output template"
        )

    def test_should_include_date_in_header_when_output_written(self, framework_content):
        """AC5: Date must be included in the output header."""
        assert re.search(r"date|timestamp|generated", framework_content, re.IGNORECASE), (
            "No date field documented in output template"
        )

    def test_should_include_inputs_summary_section_when_output_written(self, framework_content):
        """AC5: Inputs summary section must be in output."""
        assert re.search(r"inputs?\s*summary|summary\s*of\s*inputs", framework_content, re.IGNORECASE), (
            "No inputs summary section documented in output template"
        )

    def test_should_include_calculated_price_section_when_output_written(self, framework_content):
        """AC5: Calculated or selected price point must be in output."""
        assert re.search(
            r"(calculated|recommended|selected|final)\s*price",
            framework_content,
            re.IGNORECASE,
        ), (
            "No calculated/selected price point section documented in output template"
        )

    def test_should_include_rationale_section_when_output_written(self, framework_content):
        """AC5: Rationale section must be in output."""
        assert re.search(r"rationale", framework_content, re.IGNORECASE), (
            "No rationale section documented in output template"
        )

    def test_should_include_disclaimer_section_when_output_written(self, framework_content):
        """AC5: 'not financial advice' disclaimer must be in output file."""
        assert re.search(r"not\s+financial\s+advice", framework_content, re.IGNORECASE), (
            "Disclaimer 'not financial advice' not found in output template"
        )


class TestAtomicWrite:
    """Tests that file write is atomic."""

    def test_should_document_atomic_write_when_output_finalized(self, framework_content):
        """AC5: Atomic write mechanism must be documented."""
        assert re.search(r"atomic", framework_content, re.IGNORECASE), (
            "No atomic write mechanism documented in framework"
        )

    def test_should_handle_existing_file_when_overwriting(self, framework_content):
        """AC5: Existing file must be overwritten safely."""
        assert re.search(
            r"(overwrite|existing|backup|replace).*file",
            framework_content,
            re.IGNORECASE,
        ) or re.search(
            r"file.*(overwrite|existing|backup|replace)",
            framework_content,
            re.IGNORECASE,
        ), (
            "No handling for existing output file documented"
        )

    def test_should_prevent_partial_writes_on_failure_when_write_fails(self, framework_content):
        """AC5/NFR-003: No partial file on write failure."""
        assert re.search(
            r"(partial|incomplete).*(write|file).*(prevent|block|avoid|no)",
            framework_content,
            re.IGNORECASE,
        ) or re.search(
            r"(no|prevent|block|avoid).*(partial|incomplete).*(write|file)",
            framework_content,
            re.IGNORECASE,
        ) or re.search(
            r"atomic.*write", framework_content, re.IGNORECASE,
        ), (
            "No partial write prevention documented"
        )
