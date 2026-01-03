# STORY-221 Test Suite - Parse and Normalize history.jsonl Data

**Quick Start:** Run `bash run-all-tests.sh` to execute all 28 tests

---

## Overview

This directory contains a comprehensive test suite for STORY-221, generated using Test-Driven Development (TDD) principles. The tests are designed to FAIL initially, driving the implementation of the `session-miner` subagent.

```
STORY-221: Parse and Normalize history.jsonl Data for Session Mining
Status: TDD Red Phase (Tests Generated, Implementation Pending)
Tests: 28 organized across 4 acceptance criteria
Framework: Bash scripting with native Claude Code tools
Expected Result: FAILING (no session-miner subagent exists yet)
```

---

## Files in This Directory

| File | Purpose | Status |
|------|---------|--------|
| **run-all-tests.sh** | Test orchestrator - runs all 4 test suites | Ready |
| **test-ac1-json-lines-parsing-error-tolerance.sh** | AC#1 tests (5 tests) | Ready |
| **test-ac2-structured-field-extraction.sh** | AC#2 tests (8 tests) | Ready |
| **test-ac3-streaming-pagination-large-files.sh** | AC#3 tests (7 tests) | Ready |
| **test-ac4-output-structure-normalization.sh** | AC#4 tests (8 tests) | Ready |
| **TEST-SUMMARY.md** | Detailed test documentation | Ready |
| **IMPLEMENTATION-GUIDE.md** | Step-by-step implementation guide | Ready |
| **README.md** | This file | Ready |

---

## Quick Start

### Run All Tests

```bash
cd /mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-221/
bash run-all-tests.sh
```

**Expected Output:**
```
[FAIL] test-ac1-json-lines-parsing-error-tolerance.sh
[FAIL] test-ac2-structured-field-extraction.sh
[FAIL] test-ac3-streaming-pagination-large-files.sh
[FAIL] test-ac4-output-structure-normalization.sh

Some test suites failed (expected in RED phase).
```

### Run Individual Test Suite

```bash
# Test AC#1
bash test-ac1-json-lines-parsing-error-tolerance.sh

# Test AC#2
bash test-ac2-structured-field-extraction.sh

# Test AC#3
bash test-ac3-streaming-pagination-large-files.sh

# Test AC#4
bash test-ac4-output-structure-normalization.sh
```

---

## Test Inventory

### AC#1: JSON Lines Parsing with Error Tolerance (5 Tests)

**File:** `test-ac1-json-lines-parsing-error-tolerance.sh`

Tests validate:
- Valid JSON entries are extracted (3+ entries)
- Malformed entries are logged but don't halt processing
- Processing continues after encountering malformed entries
- Valid entry structure is correct
- Error log includes line numbers and descriptions

**Key Scenario:** history.jsonl with mixed valid/malformed entries

### AC#2: Structured Field Extraction (8 Tests)

**File:** `test-ac2-structured-field-extraction.sh`

Tests validate extraction and normalization of 8 required fields:
1. timestamp (ISO8601 format)
2. command (string)
3. status (enum: success|error|partial)
4. duration_ms (numeric milliseconds)
5. user_input (string)
6. model (string)
7. session_id (identifier string)
8. project (string)

**Key Scenario:** Various entry formats with different field values

### AC#3: Streaming/Pagination Support (7 Tests)

**File:** `test-ac3-streaming-pagination-large-files.sh`

Tests validate:
- Pagination with offset parameter (skip N entries)
- Pagination with limit parameter (process max N entries)
- Combined offset+limit for chunked processing
- Batch metadata returned (has_more, next_offset)
- No context window exhaustion with multiple requests
- Streaming uses chunked reads (not full file load)
- Performance meets target (<30 seconds for 86MB)

**Key Scenario:** 1000+ entry file simulating large dataset

### AC#4: Output Structure Normalization (8 Tests)

**File:** `test-ac4-output-structure-normalization.sh`

Tests validate:
- Output is valid JSON
- Contains "entries" array field
- Includes metadata object
- Each entry has consistent structure
- Field types are consistent
- Null/missing values handled consistently
- Output consumable by downstream systems
- Error log structure is consistent

**Key Scenario:** Schema validation for downstream consumption

---

## What These Tests Require

### To Make Tests PASS, Create:

**File:** `.claude/agents/session-miner.md`

**Responsibilities:**
1. Parse JSON lines from history.jsonl file
2. Extract and normalize 8 metadata fields
3. Handle malformed entries gracefully (log, don't halt)
4. Support streaming/pagination with offset/limit
5. Return structured JSON output with entries + metadata

**Constraints:**
- Location: `.claude/agents/session-miner.md`
- Size: <500 lines
- Tools: Read, Glob, Grep (native only)
- Dependencies: Zero
- Performance: <30 seconds for 86MB file

---

## Test Execution Phases

### Phase 1: RED (Current)
- ✓ Tests generated
- ✓ Tests ready to run
- ✓ All tests FAIL (expected)
- **Status:** COMPLETE

### Phase 2: GREEN
- [ ] Create `.claude/agents/session-miner.md`
- [ ] Implement JSON parsing
- [ ] Implement field normalization
- [ ] Implement streaming/pagination
- [ ] Run tests → Target: 28/28 PASS

### Phase 3: REFACTOR
- [ ] Optimize performance
- [ ] Improve error messages
- [ ] Add documentation
- [ ] Update tests as needed

### Phase 4: QA
- [ ] Run `/qa STORY-221` validation
- [ ] Verify coverage thresholds
- [ ] Test with real history.jsonl data
- [ ] Performance benchmarking

---

## Test Data Reference

### Sample Valid Entry

```json
{"timestamp": "2025-01-01T10:00:00Z", "command": "dev", "status": "success", "duration_ms": 5000, "user_input": "STORY-001", "model": "claude-opus", "session_id": "sess-001", "project": "devforgeai"}
```

### Sample Malformed Entry

```
{MALFORMED_NO_CLOSING_BRACE "timestamp": "2025-01-01T10:10:00Z"
```

### Expected Output Structure

```json
{
  "entries": [
    {
      "timestamp": "2025-01-01T10:00:00Z",
      "command": "dev",
      "status": "success",
      "duration_ms": 5000,
      "user_input": "STORY-001",
      "model": "claude-opus",
      "session_id": "sess-001",
      "project": "devforgeai"
    }
  ],
  "metadata": {
    "total_count": 5,
    "processed_count": 4,
    "error_count": 1,
    "has_more": false,
    "next_offset": null,
    "errors": [
      {
        "line": 3,
        "error": "MALFORMED_JSON",
        "message": "Missing closing brace"
      }
    ]
  }
}
```

---

## Documentation Files

### [TEST-SUMMARY.md](TEST-SUMMARY.md)
Comprehensive test suite documentation including:
- Detailed test descriptions
- Coverage analysis by AC
- Test data reference
- Implementation requirements
- Next steps for each phase

**Read this if:** You want detailed understanding of what each test validates

### [IMPLEMENTATION-GUIDE.md](IMPLEMENTATION-GUIDE.md)
Step-by-step guide for implementing session-miner including:
- Minimum viable implementation
- AC#1-4 implementation checklists
- Test data for manual testing
- Development workflow
- Performance optimization tips
- Troubleshooting guide

**Read this if:** You're implementing the session-miner subagent

---

## Key Numbers

| Metric | Value |
|--------|-------|
| Total Tests | 28 |
| AC#1 Tests | 5 |
| AC#2 Tests | 8 |
| AC#3 Tests | 7 |
| AC#4 Tests | 8 |
| Test Files | 4 |
| Total Lines | ~840 |
| Expected Status | 28 FAIL (RED phase) |

---

## Directory Structure

```
/mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-221/
├── run-all-tests.sh                    (155 lines)
├── test-ac1-*.sh                       (180 lines)
├── test-ac2-*.sh                       (230 lines)
├── test-ac3-*.sh                       (205 lines)
├── test-ac4-*.sh                       (225 lines)
├── TEST-SUMMARY.md                     (Detailed docs)
├── IMPLEMENTATION-GUIDE.md             (Developer guide)
└── README.md                           (This file)
```

---

## Running Tests - Examples

### Example 1: Run All Tests
```bash
bash run-all-tests.sh
```

### Example 2: Run Only AC#1
```bash
bash test-ac1-json-lines-parsing-error-tolerance.sh
```

### Example 3: Run Multiple Tests
```bash
bash test-ac1-json-lines-parsing-error-tolerance.sh && \
bash test-ac2-structured-field-extraction.sh
```

---

## Integration with DevForgeAI Workflow

### This Test Suite Supports:

1. **TDD Red Phase**
   - Tests fail initially (no implementation)
   - Tests drive implementation requirements
   - Framework: Bash with native Claude Code tools

2. **Phase 2-3 Transition**
   - GREEN phase: Implement to make tests pass
   - REFACTOR phase: Improve implementation

3. **QA Validation**
   - Tests provide coverage evidence
   - `/qa STORY-221` will verify coverage thresholds
   - Tests can be re-run to validate quality

4. **Definition of Done (DoD)**
   - All tests passing ✓
   - Coverage thresholds met ✓
   - Acceptance criteria verified ✓

---

## References

### Story Documentation
- **Story File:** `devforgeai/specs/Stories/STORY-221-history-jsonl-parser.story.md`
- **Epic:** `devforgeai/specs/Epics/EPIC-034-session-data-mining.epic.md`
- **Tech Stack:** `devforgeai/specs/context/tech-stack.md`
- **Source Tree:** `devforgeai/specs/context/source-tree.md`

### Framework Documentation
- **Dev Skill:** `.claude/skills/devforgeai-development/SKILL.md`
- **Test-Automator:** `.claude/agents/test-automator.md`
- **Commands:** `.claude/commands/dev.md`

### Related Stories
- STORY-222: Plan File Knowledge Base
- STORY-223: Session File Catalog
- STORY-224: Insights Command
- STORY-225: Insights Skill

---

## Expected Test Results

### RED Phase (Current)
```
Status: All tests FAIL (expected)
Reason: session-miner.md does not exist
Tests Run: 28
Passed: 0
Failed: 28
Pass Rate: 0%
```

### GREEN Phase (After Implementation)
```
Status: All tests PASS (target)
Reason: session-miner properly implemented
Tests Run: 28
Passed: 28
Failed: 0
Pass Rate: 100%
```

---

## Troubleshooting

### Q: Tests fail with "session-miner subagent not found"
**A:** This is expected in RED phase. Create `.claude/agents/session-miner.md` in GREEN phase.

### Q: How do I implement the subagent?
**A:** Read `IMPLEMENTATION-GUIDE.md` for detailed step-by-step instructions.

### Q: Can I run individual tests?
**A:** Yes, each test file is standalone:
```bash
bash test-ac1-json-lines-parsing-error-tolerance.sh
```

### Q: What if a test times out?
**A:** Likely caused by context window exhaustion. Ensure streaming/pagination is implemented for large files.

### Q: How do I know if implementation is correct?
**A:** Run `bash run-all-tests.sh`. All 28 tests should PASS.

---

## Next Steps

1. **Read TEST-SUMMARY.md** for detailed test documentation
2. **Read IMPLEMENTATION-GUIDE.md** for development guidance
3. **Create `.claude/agents/session-miner.md`**
4. **Run tests:** `bash run-all-tests.sh`
5. **Iterate** until all 28 tests PASS

---

## TDD Reminder

> These tests are designed to FAIL in the RED phase. That's correct.
> Your job is to make them PASS by implementing the session-miner subagent.
> The tests define the requirements. The implementation satisfies them.

---

**Generated:** 2025-01-02
**TDD Phase:** Red (Test-First)
**Status:** Ready for Implementation
**Framework:** Bash scripting with native Claude Code tools
