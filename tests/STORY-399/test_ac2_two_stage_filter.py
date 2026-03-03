"""
Test: AC#2 - Two-Stage Filtering (PE-060)
Story: STORY-399
Generated: 2026-02-14

Validates that two-stage-filter-patterns.md reference file exists
and documents Stage 1 (high-recall) and Stage 2 (high-precision) filtering.

Tests validate STRUCTURE and CONTENT of Markdown files (not executable code).
All tests MUST FAIL initially (TDD Red phase) since the file has not been created yet.
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def read_file(relative_path):
    """Read a file relative to the project root."""
    full_path = os.path.join(PROJECT_ROOT, relative_path)
    with open(full_path, 'r') as f:
        return f.read()


class TestAC2TwoStageFilter:
    """AC#2: Two-Stage Filtering reference file structure and content."""

    FILTER_PATH = 'src/claude/agents/anti-pattern-scanner/references/two-stage-filter-patterns.md'

    # --- Act & Assert ---

    def test_should_exist_at_correct_path(self):
        """Two-stage filter reference file must exist at the documented path."""
        full_path = os.path.join(PROJECT_ROOT, self.FILTER_PATH)
        assert os.path.isfile(full_path), \
            f"Reference file must exist at: {self.FILTER_PATH}"

    def test_should_contain_stage1_high_recall_description(self):
        """Must document Stage 1 as high-recall detection."""
        content = read_file(self.FILTER_PATH)
        assert re.search(r'stage\s*1.*high.?recall|high.?recall.*stage\s*1',
                         content, re.IGNORECASE), \
            "Must describe Stage 1 as 'high-recall' detection"

    def test_should_contain_stage2_high_precision_description(self):
        """Must document Stage 2 as high-precision LLM assessment."""
        content = read_file(self.FILTER_PATH)
        assert re.search(r'stage\s*2.*high.?precision|high.?precision.*stage\s*2',
                         content, re.IGNORECASE), \
            "Must describe Stage 2 as 'high-precision' LLM assessment"

    def test_should_document_confidence_threshold_07(self):
        """Must document confidence threshold of 0.7."""
        content = read_file(self.FILTER_PATH)
        assert '0.7' in content, \
            "Must document confidence threshold of 0.7"

    def test_should_contain_llm_prompt_template(self):
        """Must contain an LLM prompt template for class assessment."""
        content = read_file(self.FILTER_PATH)
        # Look for prompt template indicators
        has_prompt = (
            'prompt' in content.lower()
            and ('template' in content.lower() or 'assess' in content.lower())
        )
        assert has_prompt, \
            "Must contain an LLM prompt template for class assessment"

    def test_should_describe_stage2_reads_class_body(self):
        """Stage 2 must describe reading the class body for assessment."""
        content = read_file(self.FILTER_PATH)
        assert re.search(r'class\s+body|read.*class|class.*source|class.*code',
                         content, re.IGNORECASE), \
            "Stage 2 must describe reading the class body"

    def test_should_describe_report_vs_suppress_decision(self):
        """Must describe the REPORT vs SUPPRESS decision based on confidence."""
        content = read_file(self.FILTER_PATH)
        content_lower = content.lower()
        has_report = 'report' in content_lower
        has_suppress = 'suppress' in content_lower
        assert has_report and has_suppress, \
            "Must describe REPORT vs SUPPRESS decision logic"

    def test_should_reference_pe060_pattern(self):
        """Must reference the PE-060 pattern identifier."""
        content = read_file(self.FILTER_PATH)
        assert 'PE-060' in content, \
            "Must reference PE-060 (Two-Stage Filtering pattern)"
