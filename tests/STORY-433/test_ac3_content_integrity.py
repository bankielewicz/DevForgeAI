"""
Test: AC#3 - File Content Integrity Verified
Story: STORY-433
Generated: 2026-02-17

Validates that SHA-256 checksums of migrated files match the original
source files (byte-for-byte identical for whole-file copies).

These tests FAIL initially (TDD Red phase) because files have not been
migrated yet.
"""

import hashlib
from pathlib import Path

import pytest

# --- Constants (computed from file location) ---
PROJECT_ROOT = Path(__file__).resolve().parents[2]
IDEATION_REFS_DIR = PROJECT_ROOT / "src" / "claude" / "skills" / "devforgeai-ideation" / "references"
ARCHITECTURE_REFS_DIR = PROJECT_ROOT / "src" / "claude" / "skills" / "devforgeai-architecture" / "references"

WHOLE_FILE_MIGRATIONS = [
    "epic-decomposition-workflow.md",
    "feasibility-analysis-workflow.md",
    "feasibility-analysis-framework.md",
    "complexity-assessment-workflow.md",
    "complexity-assessment-matrix.md",
]


def compute_sha256(file_path: Path) -> str:
    """Compute SHA-256 checksum of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


class TestAC3ContentIntegrity:
    """AC#3: SHA-256 checksums match between source and target files."""

    # --- Individual File Integrity Tests ---

    def test_should_match_checksum_epic_decomposition_when_migrated(
        self, ideation_refs_dir, architecture_refs_dir
    ):
        """BR-001: epic-decomposition-workflow.md content byte-for-byte identical."""
        filename = "epic-decomposition-workflow.md"
        source = ideation_refs_dir / filename
        target = architecture_refs_dir / filename

        assert target.exists(), f"Target file {filename} not found in architecture."

        if source.exists():
            source_hash = compute_sha256(source)
            target_hash = compute_sha256(target)
            assert source_hash == target_hash, (
                f"SHA-256 mismatch for {filename}. "
                f"Source: {source_hash}, Target: {target_hash}. "
                "Files must be byte-for-byte identical."
            )

    def test_should_match_checksum_feasibility_analysis_workflow_when_migrated(
        self, ideation_refs_dir, architecture_refs_dir
    ):
        """BR-001: feasibility-analysis-workflow.md content byte-for-byte identical."""
        filename = "feasibility-analysis-workflow.md"
        source = ideation_refs_dir / filename
        target = architecture_refs_dir / filename

        assert target.exists(), f"Target file {filename} not found in architecture."

        if source.exists():
            source_hash = compute_sha256(source)
            target_hash = compute_sha256(target)
            assert source_hash == target_hash, (
                f"SHA-256 mismatch for {filename}. "
                f"Source: {source_hash}, Target: {target_hash}."
            )

    def test_should_match_checksum_feasibility_analysis_framework_when_migrated(
        self, ideation_refs_dir, architecture_refs_dir
    ):
        """BR-001: feasibility-analysis-framework.md content byte-for-byte identical."""
        filename = "feasibility-analysis-framework.md"
        source = ideation_refs_dir / filename
        target = architecture_refs_dir / filename

        assert target.exists(), f"Target file {filename} not found in architecture."

        if source.exists():
            source_hash = compute_sha256(source)
            target_hash = compute_sha256(target)
            assert source_hash == target_hash, (
                f"SHA-256 mismatch for {filename}. "
                f"Source: {source_hash}, Target: {target_hash}."
            )

    def test_should_match_checksum_complexity_assessment_workflow_when_migrated(
        self, ideation_refs_dir, architecture_refs_dir
    ):
        """BR-001: complexity-assessment-workflow.md content byte-for-byte identical."""
        filename = "complexity-assessment-workflow.md"
        source = ideation_refs_dir / filename
        target = architecture_refs_dir / filename

        assert target.exists(), f"Target file {filename} not found in architecture."

        if source.exists():
            source_hash = compute_sha256(source)
            target_hash = compute_sha256(target)
            assert source_hash == target_hash, (
                f"SHA-256 mismatch for {filename}. "
                f"Source: {source_hash}, Target: {target_hash}."
            )

    def test_should_match_checksum_complexity_assessment_matrix_when_migrated(
        self, ideation_refs_dir, architecture_refs_dir
    ):
        """BR-001: complexity-assessment-matrix.md content byte-for-byte identical."""
        filename = "complexity-assessment-matrix.md"
        source = ideation_refs_dir / filename
        target = architecture_refs_dir / filename

        assert target.exists(), f"Target file {filename} not found in architecture."

        if source.exists():
            source_hash = compute_sha256(source)
            target_hash = compute_sha256(target)
            assert source_hash == target_hash, (
                f"SHA-256 mismatch for {filename}. "
                f"Source: {source_hash}, Target: {target_hash}."
            )

    # --- Aggregate Integrity Test ---

    def test_should_match_all_checksums_for_whole_file_migrations_when_complete(
        self, ideation_refs_dir, architecture_refs_dir
    ):
        """BR-001: All 5 whole-file migrations have matching SHA-256 checksums."""
        mismatched = []
        missing_target = []

        for filename in WHOLE_FILE_MIGRATIONS:
            source = ideation_refs_dir / filename
            target = architecture_refs_dir / filename

            if not target.exists():
                missing_target.append(filename)
                continue

            if not source.exists():
                # Source removed after migration -- cannot compare
                continue

            source_hash = compute_sha256(source)
            target_hash = compute_sha256(target)
            if source_hash != target_hash:
                mismatched.append(
                    f"{filename}: source={source_hash[:16]}... target={target_hash[:16]}..."
                )

        assert len(missing_target) == 0, (
            f"Target files missing in architecture: {missing_target}"
        )
        assert len(mismatched) == 0, (
            f"Checksum mismatches detected: {mismatched}"
        )

    # --- File Size Sanity Check ---

    def test_should_have_nonzero_file_sizes_for_migrated_files_when_complete(
        self, architecture_refs_dir
    ):
        """Verify migrated files have reasonable sizes (not truncated or corrupt)."""
        for filename in WHOLE_FILE_MIGRATIONS:
            target = architecture_refs_dir / filename
            if target.exists():
                size = target.stat().st_size
                assert size > 100, (
                    f"{filename} is suspiciously small ({size} bytes). "
                    "File may be truncated or corrupt."
                )

    def test_should_preserve_line_count_for_migrated_files_when_complete(
        self, ideation_refs_dir, architecture_refs_dir
    ):
        """Verify migrated files have the same line count as source files."""
        for filename in WHOLE_FILE_MIGRATIONS:
            source = ideation_refs_dir / filename
            target = architecture_refs_dir / filename

            if source.exists() and target.exists():
                source_lines = len(source.read_text(encoding="utf-8").splitlines())
                target_lines = len(target.read_text(encoding="utf-8").splitlines())
                assert source_lines == target_lines, (
                    f"Line count mismatch for {filename}: "
                    f"source={source_lines}, target={target_lines}."
                )
