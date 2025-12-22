# STORY-073 Quick Reference Card

## Test Execution

### Run All Tests
```bash
pytest tests/installer/services/ -v
```

### Run by Acceptance Criteria
```bash
pytest -m "ac('AC#1')" -v  # Version detection
pytest -m "ac('AC#2')" -v  # Version comparison
pytest -m "ac('AC#3')" -v  # CLAUDE.md detection
pytest -m "ac('AC#4')" -v  # Git detection
pytest -m "ac('AC#5')" -v  # File conflicts
pytest -m "ac('AC#6')" -v  # Summary formatting
```

### Run Single Service Tests
```bash
pytest tests/installer/services/test_version_detection_service.py -v
pytest tests/installer/services/test_claudemd_detection_service.py -v
pytest tests/installer/services/test_git_detection_service.py -v
pytest tests/installer/services/test_file_conflict_detection_service.py -v
pytest tests/installer/services/test_summary_formatter_service.py -v
pytest tests/installer/services/test_auto_detection_service.py -v
```

### Generate Coverage Report
```bash
pytest tests/installer/services/ \
  --cov=src/installer/services \
  --cov-report=html \
  --cov-report=term \
  -v
```

---

## Test Suite Overview

| File | Tests | Lines | Service |
|------|-------|-------|---------|
| test_version_detection_service.py | 28 | 554 | VersionDetectionService |
| test_claudemd_detection_service.py | 21 | 367 | ClaudeMdDetectionService |
| test_git_detection_service.py | 26 | 551 | GitDetectionService |
| test_file_conflict_detection_service.py | 24 | 545 | FileConflictDetectionService |
| test_summary_formatter_service.py | 19 | 513 | SummaryFormatterService |
| test_auto_detection_service.py | 22 | 491 | AutoDetectionService |
| **TOTAL** | **140** | **3,021** | **6 services** |

---

## Implementation Files to Create

### Data Models (src/installer/services/)
```
version_detection_service.py
├── VersionInfo (dataclass)
│   ├── installed_version: str
│   ├── installed_at: str
│   └── installation_source: str
└── VersionComparisonResult (dataclass)
    ├── action: str  # upgrade/downgrade/same/unknown
    └── message: str

claudemd_detection_service.py
└── ClaudeMdInfo (dataclass)
    ├── exists: bool
    ├── size: int | None
    ├── modified: float | None
    └── needs_backup: bool

git_detection_service.py
└── GitInfo (dataclass)
    ├── repository_root: Path | None
    └── is_submodule: bool

file_conflict_detection_service.py
└── ConflictInfo (dataclass)
    ├── conflicts: List[Path]
    ├── framework_count: int
    └── user_count: int

auto_detection_service.py
└── DetectionResult (dataclass)
    ├── version_info: VersionInfo | None
    ├── claudemd_info: ClaudeMdInfo | None
    ├── git_info: GitInfo | None
    └── conflicts: ConflictInfo
```

### Service Classes (src/installer/services/)
```
version_detection_service.py
└── VersionDetectionService
    ├── __init__(target_path: str)
    ├── read_version() -> VersionInfo | None
    └── compare_versions(installed: str, source: str) -> VersionComparisonResult

claudemd_detection_service.py
└── ClaudeMdDetectionService
    ├── __init__(target_path: str)
    ├── detect() -> ClaudeMdInfo
    └── generate_backup_name() -> str

git_detection_service.py
└── GitDetectionService
    ├── __init__(target_path: str)
    ├── detect_git_root() -> Path | None
    ├── is_git_available() -> bool
    └── is_submodule() -> bool

file_conflict_detection_service.py
└── FileConflictDetectionService
    ├── __init__(target_path: str, source_files: List[str])
    ├── detect_conflicts() -> ConflictInfo
    └── is_within_target(path: Path) -> bool

summary_formatter_service.py
└── SummaryFormatterService
    ├── __init__(use_colors: bool = True, source_version: str = "")
    └── format_summary(result: DetectionResult) -> str

auto_detection_service.py
└── AutoDetectionService
    ├── __init__(target_path: str, source_version: str, source_files: List[str])
    └── detect_all() -> DetectionResult
```

---

## Test Markers

```python
@pytest.mark.story("STORY-073")  # All tests
@pytest.mark.ac("AC#1")           # Specific acceptance criteria
```

---

## Expected Initial Results

### RED Phase (Before Implementation)
```
============================== test session starts ==============================
collected 140 items

tests/installer/services/test_version_detection_service.py::TestVersionDetectionService::test_should_read_version_json_successfully FAILED
...
============================== 140 failed in 2.50s ===============================

ModuleNotFoundError: No module named 'src.installer.services.version_detection_service'
```

### GREEN Phase (After Implementation)
```
============================== test session starts ==============================
collected 140 items

tests/installer/services/test_version_detection_service.py::TestVersionDetectionService::test_should_read_version_json_successfully PASSED
...
============================== 140 passed in 5.30s ================================

Coverage report:
src/installer/services/version_detection_service.py      96%
src/installer/services/claudemd_detection_service.py     97%
src/installer/services/git_detection_service.py          95%
src/installer/services/file_conflict_detection_service.py 96%
src/installer/services/summary_formatter_service.py      94%
src/installer/services/auto_detection_service.py         98%
TOTAL                                                     96%
```

---

## Key Performance Targets

| Service | Target | Test |
|---------|--------|------|
| Version detection | <10ms | test_should_complete_version_read_within_10ms |
| CLAUDE.md detection | <10ms | test_should_complete_detection_within_10ms |
| Git detection | <100ms | test_should_complete_git_detection_within_100ms |
| Conflict detection | ≥1000 files/sec | test_should_scan_at_1000_files_per_second |
| Summary formatting | <50ms | test_should_complete_summary_generation_within_50ms |
| **Overall** | **<500ms** | **test_should_complete_detection_within_500ms** |

---

## Common Test Patterns

### AAA Pattern
```python
def test_example(self, temp_dir):
    # Arrange
    service = MyService(target_path=str(temp_dir))

    # Act
    result = service.do_something()

    # Assert
    assert result is not None
```

### Mocking External Commands
```python
with patch('subprocess.run', return_value=mock_result) as mock_run:
    result = service.detect_git_root()
    mock_run.assert_called_once()
```

### Error Handling Tests
```python
with patch('builtins.open', side_effect=IOError("Cannot read")):
    result = service.read_version()
    assert result is None  # Graceful handling
```

---

## Coverage Thresholds

```ini
[coverage:report]
precision = 2
show_missing = true
skip_covered = false

[coverage:run]
branch = true
source = src/installer/services

[coverage:thresholds]
src/installer/services/version_detection_service.py = 95
src/installer/services/claudemd_detection_service.py = 95
src/installer/services/git_detection_service.py = 95
src/installer/services/file_conflict_detection_service.py = 95
src/installer/services/summary_formatter_service.py = 95
src/installer/services/auto_detection_service.py = 95
```

---

## Dependencies

### Required
```bash
pip install pytest packaging
```

### Optional (Development)
```bash
pip install pytest-cov pytest-xdist pytest-timeout
```

---

## Troubleshooting

### Issue: Tests hang during git detection
**Solution:** Check timeout parameter in subprocess.run()

### Issue: Permission errors on CI
**Solution:** Use mock_open or temporary directories with proper permissions

### Issue: Path tests fail on Windows
**Solution:** Use Path objects, not string concatenation

### Issue: Coverage too low
**Solution:** Add tests for edge cases and error paths

---

## Next Actions

1. ✅ Create directory structure: `src/installer/services/`
2. ✅ Implement data models (5 dataclasses)
3. ✅ Implement services (6 classes)
4. ✅ Run tests: `pytest tests/installer/services/ -v`
5. ✅ Fix failures until GREEN
6. ✅ Verify coverage: ≥95% per service
7. ✅ Refactor while keeping tests GREEN

---

**Generated:** 2025-12-03
**Story:** STORY-073
**Phase:** TDD RED
**Test Count:** 140
**Target Coverage:** 95%+
