# STORY-076 Test Suite - Quick Reference

## Test Files Quick Start

### Run All Tests (RED Phase - All Failing)
```bash
cd /mnt/c/Projects/DevForgeAI2
python3 -m pytest tests/installer/test_markdown_parser.py \
                   tests/installer/test_merge_backup_service.py \
                   tests/installer/test_merge_conflict_detection_service.py \
                   tests/installer/test_claudemd_merge_service.py \
                   tests/installer/test_claudemd_merge_integration.py \
                   -v
```

**Expected:** 150 FAILED (services don't exist yet)

---

## Test Module Overview

### 1. test_markdown_parser.py (32 tests)
**Purpose:** Parse CLAUDE.md into sections

**Key Tests:**
- ATX header parsing (##, ###)
- Setext header parsing (underlined)
- Section content extraction
- Code block handling
- Edge cases (unicode, long names, special chars)
- Performance: <500ms for 500KB

**Implements:** SVC-014, SVC-015

---

### 2. test_merge_backup_service.py (28 tests)
**Purpose:** Create and verify backups

**Key Tests:**
- Timestamped filename generation (YYYYMMDD-HHMMSS)
- Collision handling (-001 counter)
- Size verification
- SHA256 hash verification
- Permission preservation (644, 444, 755)
- Performance: <1s for 1MB files

**Implements:** SVC-006 through SVC-009

**Exception Types Required:**
- FileNotFoundError (missing file)
- PermissionError (access denied)
- OSError (disk/IO failure)

---

### 3. test_merge_conflict_detection_service.py (33 tests)
**Purpose:** Detect conflicts using similarity threshold

**Key Tests:**
- Framework section identification
- User section identification
- Similarity calculation (0.0 to 1.0)
- **Boundary:** 70% = NO conflict, 69% = CONFLICT
- Conflict detail generation
- Excerpt truncation (max 200 chars)

**Implements:** SVC-010 through SVC-013

**Critical Boundary:**
```python
similarity_ratio >= 0.70  # NO CONFLICT (user change ≤30%)
similarity_ratio < 0.70   # CONFLICT (user change >30%)
```

---

### 4. test_claudemd_merge_service.py (39 tests)
**Purpose:** Main orchestration - all 4 strategies

**Key Tests:**

**Strategy 1: auto_merge()**
- Preserve user sections verbatim
- Update framework sections
- Detect conflicts and escalate
- Return MergeResult (not string!)

**Strategy 2: replace()**
- Create backup first
- Overwrite with template
- Return success status

**Strategy 3: skip()**
- Don't modify file
- Preserve mtime
- No backup needed

**Strategy 4: manual()**
- Create backup
- Write template file
- Display instructions

**Implements:** SVC-001 through SVC-005

---

### 5. test_claudemd_merge_integration.py (19 tests)
**Purpose:** End-to-end workflows across all strategies

**Key Tests:**
- Complete auto-merge workflow
- Complete replace workflow
- Complete skip workflow
- Complete manual workflow
- Cross-service data flow
- All 4 strategies available
- Strategy selection and execution

---

## Critical Lessons Learned Applied

### 1. Consistent Return Types ✅

**WRONG:**
```python
def auto_merge():
    return "Success"  # String!

def auto_merge():
    return {"status": "ok"}  # Dict!
```

**CORRECT:**
```python
def auto_merge() -> MergeResult:
    return MergeResult(
        status="SUCCESS",
        strategy="auto-merge",
        merged_content="...",
        backup_path=Path("..."),
        conflicts=[],
        error_message=None,
        timestamp="2025-12-04T10:00:00Z"
    )
```

**Tests Enforcing:** `test_automerge_returns_merge_result_not_string()` and 3 more

---

### 2. Specific Exception Types ✅

**WRONG:**
```python
try:
    backup = read_file(path)
except Exception as e:  # Too generic!
    log(f"Error: {e}")
```

**CORRECT:**
```python
try:
    backup = read_file(path)
except FileNotFoundError:
    # Handle missing file
except PermissionError:
    # Handle access denied
except OSError:
    # Handle disk/IO error
```

**Tests Enforcing:** 8+ exception-specific tests

---

### 3. Clear Similarity Logic ✅

**WRONG:**
```python
if similarity > 0.69:  # Ambiguous!
    return no_conflict
```

**CORRECT:**
```python
# 70% similarity = ≤30% user change = acceptable
# 69% similarity = >30% user change = conflict
if similarity >= 0.70:
    return no_conflict
else:
    return conflict
```

**Tests Enforcing:**
- `test_should_not_detect_conflict_at_70_percent_similarity()`
- `test_should_detect_conflict_at_69_percent_similarity()`
- `test_boundary_70_percent_exact()`
- `test_boundary_69_percent_exact()`

---

### 4. Symlink Security ✅

**Tests Ready For:**
- Rejecting symlinks to system files (/etc/passwd)
- Rejecting symlinks outside project directory
- Path traversal prevention

---

### 5. Complete Type Contracts ✅

**Logger Protocol:**
```python
class ILogger(Protocol):
    def log(self, message: str) -> None:
        """Log a message."""
```

**Test:** `test_should_accept_logger_protocol()`

---

## Key Test Fixtures

### Most Useful for Development

```python
# Simple CLAUDE.md for basic testing
simple_claudemd  # 10 lines

# Complex CLAUDE.md with 15+ sections
complex_claudemd  # Realistic example

# CLAUDE.md with user modifications (>30% change)
conflicting_claudemd  # Conflict scenario

# DevForgeAI framework template
framework_template  # Fresh template

# Large 500KB+ file for performance testing
large_claudemd  # Performance baseline

# Mock logger following protocol
mock_logger  # Log interaction testing

# Various file permissions
file_permission_tests  # Permission scenarios

# Symlink test scenarios
symlink_test_files  # Security testing

# Boundary test cases
similarity_threshold_tests  # 70% boundary testing
excerpt_truncation_tests  # 200 char limit
timestamp_format_tests  # Format validation
```

---

## Implementation Checklist

### Phase 1: MarkdownParser
- [ ] Parse ATX headers (##, ###)
- [ ] Parse Setext headers (underlined)
- [ ] Extract section content
- [ ] Handle code blocks
- [ ] Return List[Section]
- [ ] Run: `pytest tests/installer/test_markdown_parser.py -v`
- [ ] Target: 32/32 passing

### Phase 2: MergeBackupService
- [ ] Generate timestamped filenames
- [ ] Handle collisions (-001, -002)
- [ ] Verify size/hash
- [ ] Preserve permissions
- [ ] Raise FileNotFoundError, PermissionError
- [ ] Run: `pytest tests/installer/test_merge_backup_service.py -v`
- [ ] Target: 28/28 passing

### Phase 3: MergeConflictDetectionService
- [ ] Identify framework sections
- [ ] Identify user sections
- [ ] Calculate similarity (0.0-1.0)
- [ ] Enforce 70% boundary
- [ ] Truncate excerpts to 200 chars
- [ ] Return ConflictDetail
- [ ] Run: `pytest tests/installer/test_merge_conflict_detection_service.py -v`
- [ ] Target: 33/33 passing

### Phase 4: Data Models
- [ ] MergeResult dataclass
- [ ] ConflictDetail dataclass
- [ ] Ensure all fields typed

### Phase 5: ClaudeMdMergeService
- [ ] Implement detect_existing()
- [ ] Implement select_strategy()
- [ ] Implement auto_merge()
- [ ] Implement replace()
- [ ] Implement skip()
- [ ] Implement manual()
- [ ] All return MergeResult
- [ ] Run: `pytest tests/installer/test_claudemd_merge_service.py -v`
- [ ] Target: 39/39 passing

### Phase 6: Integration
- [ ] End-to-end workflows
- [ ] Cross-service data flow
- [ ] Run: `pytest tests/installer/test_claudemd_merge_integration.py -v`
- [ ] Target: 19/19 passing

---

## Test Execution Order

For incremental development:

```bash
# Phase 1: Markdown Parser
python3 -m pytest tests/installer/test_markdown_parser.py -v
# Until: 32/32 passing

# Phase 2: Backup Service
python3 -m pytest tests/installer/test_merge_backup_service.py -v
# Until: 28/28 passing

# Phase 3: Conflict Detection
python3 -m pytest tests/installer/test_merge_conflict_detection_service.py -v
# Until: 33/33 passing

# Phase 4: Main Service
python3 -m pytest tests/installer/test_claudemd_merge_service.py -v
# Until: 39/39 passing

# Phase 5: Integration
python3 -m pytest tests/installer/test_claudemd_merge_integration.py -v
# Until: 19/19 passing

# All Green!
python3 -m pytest tests/installer/test_*.py -v
# Should see: 150 passed in X.XXs
```

---

## Coverage Targets

```bash
# After implementation is complete:
python3 -m pytest tests/installer/test_*.py \
    --cov=src/installer/services \
    --cov-report=html \
    -v

# Targets:
# MarkdownParser: 95% coverage
# MergeBackupService: 95% coverage
# MergeConflictDetectionService: 95% coverage
# ClaudeMdMergeService: 95% coverage
# Integration: 85% coverage
```

---

## Performance Benchmarks

After implementation, verify NFRs:

```bash
# Test performance requirements
python3 -m pytest tests/installer/test_markdown_parser.py::TestParserPerformance -v
# Target: <500ms for 500KB parse

python3 -m pytest tests/installer/test_claudemd_merge_service.py::TestMergePerformance -v
# Target: <2s for merge, <1s for backup

python3 -m pytest tests/installer/test_merge_backup_service.py::TestBackupPerformance -v
# Target: <1s for 1MB backup
```

---

## Acceptance Criteria Validation

```bash
# Run all AC-related tests
python3 -m pytest -k "ac_" -v

# Or specific ACs:
python3 -m pytest tests/installer/test_claudemd_merge_service.py::TestDetectExistingCLAUDEmd -v  # AC#1
python3 -m pytest tests/installer/test_claudemd_merge_service.py::TestAutoMergeStrategy -v  # AC#2
python3 -m pytest tests/installer/test_claudemd_merge_service.py::TestBackupCreation -v  # AC#3
python3 -m pytest tests/installer/test_claudemd_merge_service.py::TestAutoMergeWithConflicts -v  # AC#4
python3 -m pytest tests/installer/test_claudemd_merge_service.py::TestReplaceStrategy -v  # AC#5
python3 -m pytest tests/installer/test_claudemd_merge_service.py::TestSkipStrategy -v  # AC#6
python3 -m pytest tests/installer/test_claudemd_merge_service.py::TestManualStrategy -v  # AC#7
python3 -m pytest tests/installer/test_claudemd_merge_service.py::TestMergeLogging -v  # AC#8
```

---

## Troubleshooting

### ModuleNotFoundError: No module named 'src.installer.services.*'
**Expected** when running tests before implementation
**Action:** Implement the missing service file in `src/installer/services/`

### All tests still failing after implementation
**Check:**
1. Return types match MergeResult
2. Exception types are specific (not generic Exception)
3. Similarity threshold exactly 0.70
4. Methods exist with correct signatures

### Some tests passing, some failing
**Good sign!** Continue implementation until 150/150 passing

---

## Key Test Classes by Purpose

| Purpose | Class | File |
|---------|-------|------|
| Parsing | TestMarkdownParserInitialization | test_markdown_parser.py |
| Backup Creation | TestBackupFileCreation | test_merge_backup_service.py |
| Verification | TestBackupVerification | test_merge_backup_service.py |
| Collisions | TestBackupCollisionHandling | test_merge_backup_service.py |
| Conflict Detection | TestSectionParsing | test_merge_conflict_detection_service.py |
| Similarity | TestSimilarityCalculation | test_merge_conflict_detection_service.py |
| Boundary Conditions | TestConflictThresholdLogic | test_merge_conflict_detection_service.py |
| Auto-Merge | TestAutoMergeStrategy | test_claudemd_merge_service.py |
| Replace | TestReplaceStrategy | test_claudemd_merge_service.py |
| Skip | TestSkipStrategy | test_claudemd_merge_service.py |
| Manual | TestManualStrategy | test_claudemd_merge_service.py |
| End-to-End | TestAutoMergeIntegrationWorkflow | test_claudemd_merge_integration.py |

---

## Questions During Implementation?

Refer to:
1. **Specific failing test** - Read the test docstring
2. **Error details** - Check AssertionError message
3. **Expected behavior** - Read test_should_* description
4. **Fixture setup** - See conftest.py for data
5. **Strategy** - See Architecture sections in main story file

---

**Test Suite Status:** COMPLETE and READY
**Current Phase:** RED (All 150 tests failing)
**Next Phase:** GREEN (Implement services, tests pass)
