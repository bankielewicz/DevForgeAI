# STORY-056 Test Suite - Complete Reference

## Quick Links

**📋 Start Here:**
- [Test Execution Guide](STORY-056-TEST-EXECUTION-GUIDE.md) - How to run tests
- [Test Summary](STORY-056-TEST-SUMMARY.md) - Complete test specifications

**📁 Test Files:**
- [Unit Tests](test-story-creation-guidance-unit.sh) - 15 tests (file I/O, parsing)
- [Integration Tests](test-story-creation-guidance-integration.sh) - 12 tests (Phase 1 workflow)
- [Regression Tests](test-story-creation-regression.sh) - 10 tests (backward compatibility)
- [Performance Tests](test-story-creation-guidance-performance.py) - 8 tests (timing, tokens)

---

## Project Context

**Story ID:** STORY-056
**Title:** devforgeai-story-creation Skill Integration with User Input Guidance
**Epic:** EPIC-011 (User Input Guidance System)
**Sprint:** SPRINT-2
**Status:** Ready for Dev → Phase 1 (Test Generation)

**Story Focus:**
Integrate user-input-guidance.md patterns into devforgeai-story-creation skill to:
- Improve question quality (Explicit Classification, Bounded Choice, Fibonacci patterns)
- Reduce subagent re-invocations by ≥30%
- Maintain ≤1,000 token overhead in Step 0
- Preserve 100% backward compatibility

---

## Test Suite Overview

| Category | Count | Lines | Purpose |
|----------|-------|-------|---------|
| **Unit Tests** | 15 | 324 | File I/O, pattern extraction, mapping |
| **Integration Tests** | 12 | 312 | Phase 1 workflow, subagent impact |
| **Regression Tests** | 10 | 298 | Backward compatibility verification |
| **Performance Tests** | 8 | 597 | Timing, tokens, memory measurement |
| **TOTAL** | **45** | **1,531** | **Comprehensive coverage** |

**Success Criteria:** All 45 tests PASS (or verified)

---

## Test Execution Flow

### 1️⃣ Unit Tests (15 tests)
```bash
bash test-story-creation-guidance-unit.sh
```
**Duration:** ~30 seconds
**Result:** All 15/15 must PASS
**Covers:** AC#1-5, AC#10, Data Validation Rules

### 2️⃣ Regression Tests (10 tests)
```bash
bash test-story-creation-regression.sh
```
**Duration:** ~20 seconds
**Result:** All 10/10 must PASS
**Covers:** AC#9, backward compatibility, baseline behavior

### 3️⃣ Integration Tests (12 tests)
```bash
bash test-story-creation-guidance-integration.sh
```
**Duration:** ~2 minutes (automated) + ~1 hour (manual tests)
**Result:** All 12/12 must VERIFY (automated + manual)
**Covers:** AC#6-8, subagent impact, batch caching, token overhead

### 4️⃣ Performance Tests (8 tests)
```bash
python3 test-story-creation-guidance-performance.py
```
**Duration:** ~1 minute
**Result:** All 8/8 must PASS (within targets)
**Covers:** AC#7, NFRs (Performance, Resource Usage)

### 5️⃣ Regression with Guidance Disabled (30+ tests)
```bash
mv src/claude/skills/devforgeai-ideation/references/user-input-guidance.md \
   src/claude/skills/devforgeai-ideation/references/user-input-guidance.md.disabled
bash test-story-creation-existing.sh  # Run existing test suite
mv src/claude/skills/devforgeai-ideation/references/user-input-guidance.md.disabled \
   src/claude/skills/devforgeai-ideation/references/user-input-guidance.md
```
**Duration:** ~2 minutes
**Result:** All 30+ tests PASS (baseline)
**Covers:** AC#9, backward compatibility

### 6️⃣ Regression with Guidance Enabled (30+ tests)
```bash
bash test-story-creation-existing.sh  # Run existing test suite
```
**Duration:** ~2 minutes
**Result:** All 30+ tests PASS (with guidance)
**Covers:** AC#9, guidance integration

---

## Acceptance Criteria Coverage

| AC | Title | Tests | Status |
|----|-------|-------|--------|
| **AC#1** | Pre-Feature Guidance Loading | UT01-03, IT01, PT01-02 | ✓ Covered |
| **AC#2** | Epic Selection Pattern | UT04, UT11, IT01 | ✓ Covered |
| **AC#3** | Sprint Assignment Pattern | UT04, UT12, IT01 | ✓ Covered |
| **AC#4** | Priority Selection Pattern | UT04, UT13, IT01 | ✓ Covered |
| **AC#5** | Story Points Pattern | UT04, UT14, IT01 | ✓ Covered |
| **AC#6** | Enhanced Subagent Context | IT03, IT10, IT12 | ✓ Covered |
| **AC#7** | Token Overhead Constraint | UT08, PT05-08 | ✓ Covered |
| **AC#8** | Batch Mode Compatibility | UT10, IT06 | ✓ Covered |
| **AC#9** | Backward Compatibility | RT01-10, IT05 | ✓ Covered |
| **AC#10** | Reference Documentation | UT15 | ✓ Covered |

**Coverage:** 100% (all 10 ACs tested)

---

## Test Status Dashboard

```
UNIT TESTS
├─ UT01: File loading (valid)           [ ] PASS
├─ UT02: File loading (missing)         [ ] PASS
├─ UT03: File loading (corrupted)       [ ] PASS
├─ UT04: Pattern extraction             [ ] PASS
├─ UT05: Pattern normalization          [ ] PASS
├─ UT06: Mapping lookup                 [ ] PASS
├─ UT07: Lookup miss handling           [ ] PASS
├─ UT08: Token documentation            [ ] PASS
├─ UT09: Fallback behavior              [ ] PASS
├─ UT10: Batch caching strategy         [ ] PASS
├─ UT11: Epic pattern                   [ ] PASS
├─ UT12: Sprint pattern                 [ ] PASS
├─ UT13: Priority pattern               [ ] PASS
├─ UT14: Points pattern                 [ ] PASS
└─ UT15: Reference completeness         [ ] PASS

REGRESSION TESTS
├─ RT01: Phase 1 unchanged              [ ] PASS
├─ RT02: Phases 2-8 unchanged           [ ] PASS
├─ RT03: Output format preserved        [ ] PASS
├─ RT04: AskUserQuestion signature      [ ] PASS
├─ RT05: Baseline logic preserved       [ ] PASS
├─ RT06: Phase execution order          [ ] PASS
├─ RT07: Epic/sprint linking            [ ] PASS
├─ RT08: Self-validation logic          [ ] PASS
├─ RT09: Skill output format            [ ] PASS
└─ RT10: Story file creation            [ ] PASS

INTEGRATION TESTS
├─ IT01: Full Phase 1 with guidance    [ ] PASS
├─ IT02: Phase 1 baseline              [ ] PASS
├─ IT03: Subagent re-invocation        [ ] VERIFY
├─ IT04: Phase 1 token overhead        [ ] VERIFY
├─ IT05: Backward compatibility        [ ] VERIFY
├─ IT06: Batch caching                 [ ] VERIFY
├─ IT07: Pattern conflict resolution   [ ] PASS
├─ IT08: Mid-execution changes         [ ] VERIFY
├─ IT09: Concurrent invocations        [ ] VERIFY
├─ IT10: Phase 6 epic/sprint           [ ] VERIFY
├─ IT11: End-to-end workflow           [ ] VERIFY
└─ IT12: AC completeness               [ ] VERIFY

PERFORMANCE TESTS
├─ PT01: Step 0 p95 execution time     [ ] PASS
├─ PT02: Step 0 p99 execution time     [ ] PASS
├─ PT03: Pattern extraction time       [ ] PASS
├─ PT04: Pattern lookup time           [ ] PASS
├─ PT05: Phase 1 execution increase    [ ] PASS
├─ PT06: Step 0 token overhead         [ ] PASS
├─ PT07: Phase 1 token increase        [ ] PASS
└─ PT08: Memory footprint              [ ] PASS
```

---

## Test Data Requirements

### Feature Descriptions (for manual testing)

Use these descriptions to verify story generation quality:

**Simple Feature:**
```
"Add user registration form with email validation."
```

**Moderate Feature:**
```
"Implement payment processing via Stripe with invoicing."
```

**Complex Feature:**
```
"Build real-time notification system with WebSocket support and retry logic."
```

**Ambiguous Feature (tests clarification):**
```
"Improve performance and make it scalable."
```

**Edge Cases Feature (tests error handling):**
```
"Handle user uploads with validation and storage."
```

---

## Performance Baselines

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Step 0 p95 time | <2s | [ ] | [ ] |
| Step 0 p99 time | <3s | [ ] | [ ] |
| Pattern extraction | <500ms | [ ] | [ ] |
| Pattern lookup | <50ms | [ ] | [ ] |
| Phase 1 time increase | ≤5% | [ ] | [ ] |
| Step 0 tokens | ≤1,000 | [ ] | [ ] |
| Phase 1 token increase | ≤5% | [ ] | [ ] |
| Memory footprint | <5MB | [ ] | [ ] |

---

## Common Issues & Troubleshooting

### Issue: "File not found: user-input-guidance.md"
**Solution:** Ensure STORY-053 is completed (creates guidance file)
```bash
ls src/claude/skills/devforgeai-ideation/references/user-input-guidance.md
```

### Issue: Unit tests fail on pattern count
**Solution:** Verify guidance file has ≥4 pattern definitions
```bash
grep -c "^### Pattern" src/claude/skills/devforgeai-ideation/references/user-input-guidance.md
```

### Issue: Performance tests show high latency
**Solution:** Run tests in isolation on quiet system
```bash
python3 test-story-creation-guidance-performance.py
```

### Issue: Regression tests fail
**Solution:** Check SKILL.md for syntax errors, restore from git if needed
```bash
git checkout src/claude/skills/devforgeai-story-creation/
```

---

## Integration with DevForgeAI Framework

### Which Skill Uses These Tests?
- **devforgeai-story-creation** (tested)
- **devforgeai-ideation** (related - uses same guidance file)
- **devforgeai-development** (uses stories created by skill)
- **devforgeai-qa** (validates stories)

### When Are Tests Run?
- **Phase 1 (Red - Test First):** Tests generated (this document)
- **Phase 2 (Green - Implementation):** Tests run to verify implementation
- **Phase 3 (Refactor):** Tests re-run to ensure no regressions
- **Phase 5 (Commit):** All tests must pass before git commit
- **CI/CD:** Tests run on every commit to verify changes

### Test Failure = Deferral Blocker
Per RCA-006:
- Cannot defer unresolved test failures
- User approval required for any deferrals
- Three-layer validation: tests → AskUserQuestion → subagent audit

---

## Files Summary

### Test Scripts (4 files, 1,531 lines)
- **test-story-creation-guidance-unit.sh** (324 lines) - Unit tests
- **test-story-creation-guidance-integration.sh** (312 lines) - Integration tests
- **test-story-creation-regression.sh** (298 lines) - Regression tests
- **test-story-creation-guidance-performance.py** (597 lines) - Performance tests

### Documentation (3 files, ~2,500 lines)
- **STORY-056-TEST-EXECUTION-GUIDE.md** - Complete execution procedures
- **STORY-056-TEST-SUMMARY.md** - Detailed test specifications
- **README-STORY-056.md** - This file (quick reference)

---

## Key Metrics

- **Total Tests:** 45 (15 unit + 12 integration + 10 regression + 8 performance)
- **Code Coverage:** AC#1-10 (100% coverage)
- **Token Budget:** Step 0 ≤1,000, Phase 1 ≤5% increase
- **Performance:** p95 <2s, p99 <3s for Step 0
- **Backward Compatibility:** 30+ existing tests must pass
- **Subagent Improvement:** ≥30% reduction in re-invocations
- **Memory Usage:** <5 MB cache footprint

---

## Next Steps

### Phase 2 - Implementation
1. [ ] Implement Step 0 (guidance loading) in SKILL.md
2. [ ] Implement pattern application (Steps 3-5)
3. [ ] Create integration guide (user-input-integration-guide.md)
4. [ ] Run unit tests (verify core functionality)
5. [ ] Run regression tests (verify backward compatibility)
6. [ ] Run integration tests (verify Phase 1 workflow)
7. [ ] Run performance tests (verify NFRs met)
8. [ ] Complete all tests with 100% pass rate

### Phase 3 - Quality Assurance
1. [ ] Run /qa STORY-056 (light validation)
2. [ ] Run /qa STORY-056 deep (comprehensive validation)
3. [ ] Verify all 10 ACs satisfied
4. [ ] Verify no deferrals or approvals needed

### Phase 4 - Release
1. [ ] All tests passing
2. [ ] QA approved
3. [ ] Ready for /release STORY-056

---

## Support & References

- **Story File:** `/mnt/c/Projects/DevForgeAI2/.ai_docs/Stories/STORY-056-devforgeai-story-creation-integration.story.md`
- **Guidance File:** `/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-ideation/references/user-input-guidance.md`
- **Skill File:** `/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-story-creation/SKILL.md`
- **Framework:** `/mnt/c/Projects/DevForgeAI2/CLAUDE.md`

---

## Document Control

| Version | Date | Status | Author |
|---------|------|--------|--------|
| 1.0 | 2025-01-21 | Draft | Test Automator |
| 1.0 | 2025-01-21 | Complete | Test Automator |

**Status:** Ready for Phase 2 Implementation

---

**Questions?** See STORY-056-TEST-EXECUTION-GUIDE.md for detailed procedures
