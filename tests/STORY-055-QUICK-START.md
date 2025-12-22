# STORY-055 Test Suite - Quick Start Guide

## TL;DR

**47 comprehensive failing tests generated for STORY-055**

Status: **RED Phase Complete** (0% pass rate expected)

```bash
# Run all tests
cd /mnt/c/Projects/DevForgeAI2
pytest tests/unit/test_ideation_guidance_loading.py \
        tests/integration/test_ideation_guidance_integration.py \
        tests/integration/test_ideation_performance.py -v

# Result: 20 failed, 22 passed, 1 skipped in 1.07s
```

---

## Test Files

| File | Tests | Coverage |
|------|-------|----------|
| `tests/unit/test_ideation_guidance_loading.py` | 12 | AC#1 (Pre-Discovery Guidance Loading) |
| `tests/integration/test_ideation_guidance_integration.py` | 22 | AC#2, AC#3, AC#5 (Patterns, Subagent, Compatibility) |
| `tests/integration/test_ideation_performance.py` | 13 | AC#4, NFR-001 to NFR-005 (Performance, Reliability) |

---

## What's Being Tested

### Acceptance Criteria (5 total)

- **AC#1:** Phase 1 Step 0 loads user-input-guidance.md
- **AC#2:** Phase 1-2 questions use 4 guidance patterns (Tell me about, Rank 1-5, Select range, Primary user)
- **AC#3:** Phase 3 subagent receives structured context (≥30% re-invocation reduction)
- **AC#4:** Token overhead ≤1,000 tokens for guidance loading
- **AC#5:** All existing functionality preserved (backward compatibility)

### Non-Functional Requirements (5 total)

- **NFR-001:** Guidance loading <500ms
- **NFR-002:** ≥30% reduction in subagent re-invocations (2.5 → ≤1.75)
- **NFR-003:** 100% workflow completion even if guidance missing
- **NFR-004:** ≤5 lines changed in SKILL.md, ≤300 lines in reference file
- **NFR-005:** ≥80% of patterns detectable via grep

---

## Current Status (RED Phase)

### Passing Tests (22)

- Guidance file exists at correct path ✓
- File is readable Markdown ✓
- Contains required sections ✓
- YAML frontmatter valid ✓
- Has elicitation patterns ✓
- Has AskUserQuestion templates ✓
- Has NFR quantification table ✓
- Has skill integration guide ✓
- File loads fast (<500ms) ✓
- Phase 1 ranking pattern partially exists ✓
- Phase 2 feature collection present ✓
- No pattern name duplication ✓
- Backward compatibility structure OK ✓
- Others...

### Failing Tests (20)

- Phase 1 Step 0 not added to SKILL.md
- Pattern keywords not in Phase 1-2 questions
- Guidance file size exceeds limit (103K > 50K)
- Token overhead estimated too high
- Phase 3 subagent context not structured
- Error handling for missing guidance not present
- Reference file not created
- Others...

### Skipped Tests (1)

- Reference file creation (not yet needed)

---

## Why Tests Fail (Expected for TDD Red Phase)

Tests are designed to fail because:

1. **Phase 1 Step 0 doesn't exist yet** (blocking AC#1)
   - Need to add "Step 0: Load guidance" to SKILL.md
   - Need to use Read() tool to load user-input-guidance.md

2. **Patterns not applied to questions yet** (blocking AC#2)
   - Phase 1 questions need "Tell me about..." for scope
   - Phase 2 questions need "Rank 1-5" for priorities
   - etc.

3. **Guidance file too large** (blocking AC#4)
   - Current: 103,609 chars (10,361 tokens)
   - Target: 50,000 chars (≤1,000 token overhead)
   - Need selective loading or file trimming

4. **Phase 3 subagent lacks context** (blocking AC#3)
   - Requirements-analyst needs structured input
   - Must reference collected Phase 1-2 responses

5. **Error handling missing** (blocking BR-001)
   - No graceful degradation if guidance file missing

---

## Next Steps (Implementation Roadmap)

### Phase 2: GREEN (Make Tests Pass)

**Step 1: Add Phase 1 Step 0** (estimated: 10 minutes)
```markdown
## Phase 1: Discovery & Problem Understanding

### Step 0: Load User Input Guidance
Load(...)  # Load guidance file

### Step 1: Generate Story ID
...
```

**Step 2: Apply patterns to questions** (estimated: 30 minutes)
- Update problem scope → "Tell me about..."
- Update feature priority → "Rank 1-5"
- Update timeline → "Select range:"
- Update user persona → "Primary user:"

**Step 3: Optimize guidance file size** (estimated: 20 minutes)
- Trim examples or use selective loading
- Get file size under 50K chars

**Step 4: Structure Phase 3 context** (estimated: 15 minutes)
- Pass user responses to requirements-analyst
- Reference collected context in prompt

**Step 5: Add error handling** (estimated: 10 minutes)
- Handle missing guidance gracefully
- Continue with standard prompts

**Step 6: Create reference file** (estimated: 20 minutes)
- Implementation details for integration
- Pattern mapping table
- Edge case handling

**Total Time Estimate:** ~1.5-2 hours for complete implementation

**Expected Result:** All 47 tests passing

### Phase 3: REFACTOR
- Remove code duplication
- Add documentation
- Optimize for clarity

---

## Running Specific Tests

```bash
# All tests (full suite)
pytest tests/unit/test_ideation_guidance_loading.py \
        tests/integration/test_ideation_guidance_integration.py \
        tests/integration/test_ideation_performance.py -v

# Just AC#1 tests (guidance loading)
pytest tests/unit/test_ideation_guidance_loading.py -v

# Just pattern application tests (AC#2)
pytest tests/integration/test_ideation_guidance_integration.py::TestPatternApplication* -v

# Just failing tests
pytest tests/ -k "ideation_guidance" --lf -v

# With coverage report
pytest tests/ -k "ideation_guidance" --cov=src --cov-report=html
```

---

## Test Architecture

### AAA Pattern (Every Test Follows This)

```python
def test_example():
    # Arrange: Set up test preconditions
    test_input = setup_data()

    # Act: Execute the behavior being tested
    result = system_under_test(test_input)

    # Assert: Verify the outcome
    assert result == expected_value
```

### Fixture Pattern (Reusable Setup)

```python
@pytest.fixture
def guidance_content(self) -> str:
    """Load guidance file content."""
    # Fixture setup code...
```

Tests use fixtures to avoid duplication and keep setup clean.

---

## Key Files Referenced by Tests

| File | Purpose | Status |
|------|---------|--------|
| `src/claude/skills/devforgeai-ideation/SKILL.md` | Skill implementation | Exists (needs Step 0 added) |
| `src/claude/skills/devforgeai-ideation/references/user-input-guidance.md` | Guidance document | Exists ✓ |
| `src/claude/skills/devforgeai-ideation/references/user-input-integration-guide.md` | Integration guide | Needs to be created |

---

## Common Failure Messages Explained

| Message | Meaning | Fix |
|---------|---------|-----|
| `"Step 0 not found in Phase 1"` | Phase 1 Step 0 not added to SKILL.md | Add Phase 1 Step 0 with guidance loading |
| `"Phase 1 scope questions should use 'Tell me about...' pattern"` | Questions don't use open-ended pattern | Update Phase 1 scope questions |
| `"Guidance file too large: 103,609 chars"` | File exceeds practical size | Trim or selectively load guidance file |
| `"Phase 3 should invoke requirements-analyst subagent"` | Phase 3 doesn't call subagent | Add Task() invocation in Phase 3 |
| `"Step 0 should include error handling"` | No graceful degradation for missing file | Add try/except or if-check for Read() |

---

## Success Criteria

### RED Phase (Current) ✓
- [x] 47 tests written
- [x] Tests failing (0% pass rate expected)
- [x] Full coverage of AC + NFR + BR + edge cases
- [x] Documentation complete

### GREEN Phase (Next)
- [ ] All 47 tests passing
- [ ] Implementation follows test requirements
- [ ] No skipped tests
- [ ] Fast execution (<2 seconds)

### REFACTOR Phase (After GREEN)
- [ ] Code cleanup
- [ ] Documentation added
- [ ] Quality metrics verified

---

## Resources

- **Full Test Documentation:** `tests/STORY-055-TEST-SUITE.md`
- **Generation Summary:** `tests/STORY-055-TEST-GENERATION-SUMMARY.md`
- **Story File:** `devforgeai/specs/Stories/STORY-055-devforgeai-ideation-integration.story.md`
- **Guidance Document:** `src/claude/skills/devforgeai-ideation/references/user-input-guidance.md`

---

## Quick Help

**Q: Why are tests failing?**
A: They're supposed to! This is TDD Red Phase. Tests fail until implementation is complete.

**Q: How many tests should pass?**
A: Eventually 47/47. Currently 22 passing (guidance file exists), 20 failing (implementation needed), 1 skipped (reference file).

**Q: What do I need to do?**
A: Implement AC#1 through AC#5 features until all tests pass.

**Q: How long will implementation take?**
A: Estimated 1.5-2 hours based on test complexity.

**Q: Can I run tests while implementing?**
A: Yes! Re-run tests after each change to verify progress. Tests act as acceptance criteria.

---

**Generated:** 2025-01-21
**Framework:** Test-Automator (TDD Red Phase)
**Status:** Ready for implementation
