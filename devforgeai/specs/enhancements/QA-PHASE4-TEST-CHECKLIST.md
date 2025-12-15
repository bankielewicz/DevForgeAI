# QA Phase 4 Enhancement - Test Validation Checklist

**Date:** 2025-11-06
**Enhancement:** Phase 4 Story File Update
**Command:** `/qa`
**Risk Level:** LOW

---

## Test Execution Status

### Unit Tests (15 test cases)

**Argument Validation (existing - verify unchanged):**
- [ ] Test 1: Valid story ID format (STORY-NNN)
- [ ] Test 2: Invalid story ID format → AskUserQuestion
- [ ] Test 3: Story file exists
- [ ] Test 4: Story file not found → AskUserQuestion
- [ ] Test 5: Mode parsing: explicit "deep"
- [ ] Test 6: Mode parsing: explicit "light"
- [ ] Test 7: Mode parsing: inferred from status "Dev Complete" → deep
- [ ] Test 8: Mode parsing: invalid value → AskUserQuestion

**Phase 4 New Tests:**
- [ ] Test 9: Deep mode PASS → Status updated to "QA Approved"
- [ ] Test 10: Deep mode PASS → Timestamp updated to current date
- [ ] Test 11: Deep mode PASS → QA Validation History section added
- [ ] Test 12: Deep mode PASS → Section inserted before "## Workflow History"
- [ ] Test 13: Deep mode FAIL → Status unchanged
- [ ] Test 14: Light mode PASS → Status unchanged (expected behavior)
- [ ] Test 15: Story file write failure → Warning displayed, validation results still shown

---

### Integration Tests (8 test cases)

**Full workflow with real stories:**
- [ ] Test 1: Story in "Dev Complete" status, deep mode → Status becomes "QA Approved"
- [ ] Test 2: Story in "In Development" status, deep mode → Status becomes "QA Approved" (if passes)
- [ ] Test 3: Story in "Backlog" status, deep mode → Error (cannot QA story not in development)
- [ ] Test 4: Story already "QA Approved", deep mode → Re-validation, append new history entry

**Mode variations:**
- [ ] Test 5: Default mode (inferred from status "Dev Complete") → Deep mode, status updated
- [ ] Test 6: Explicit light mode → No status update (as expected)

**Failure scenarios:**
- [ ] Test 7: Deep mode validation fails (coverage <80%) → Status unchanged, violations displayed
- [ ] Test 8: Deep mode validation fails (CRITICAL anti-pattern) → Status unchanged, error displayed

---

### Regression Tests (8 test cases)

**Verify behavior unchanged:**
- [ ] Test 1: Skill invocation still occurs (devforgeai-qa skill executed)
- [ ] Test 2: QA report still generated in `.devforgeai/qa/reports/`
- [ ] Test 3: qa-result-interpreter subagent still invoked
- [ ] Test 4: Display template still shown to user
- [ ] Test 5: Next steps still provided
- [ ] Test 6: Light mode still skips status update
- [ ] Test 7: Failed validation still blocks status update
- [ ] Test 8: Error messages still clear and actionable

---

### Performance Tests (4 test cases)

- [ ] Test 1: Character budget <12K chars (target) or <15K (limit)
  - **Expected:** ~11,060 chars (73% of 15K limit)
  - **Actual:** _________
  - **Status:** PASS / FAIL

- [ ] Test 2: Token budget <5K tokens in main conversation
  - **Expected:** ~3.5K-4K tokens
  - **Actual:** _________
  - **Status:** PASS / FAIL

- [ ] Test 3: Execution time deep mode <5 minutes (unchanged from current)
  - **Expected:** 3-5 minutes
  - **Actual:** _________
  - **Status:** PASS / FAIL

- [ ] Test 4: Story file update <1 second
  - **Expected:** <1 second for YAML edit + section append
  - **Actual:** _________
  - **Status:** PASS / FAIL

---

## Test Execution Notes

### Test Environment

- **Repository:** DevForgeAI2
- **Story used for testing:** STORY-006 (or create test story)
- **Git status:** Clean working directory recommended
- **Context files:** All 6 context files should exist

### Pre-Test Setup

1. Ensure backup exists:
   ```bash
   ls -la .claude/commands/qa.md.backup-pre-phase4
   ```

2. Verify character budget:
   ```bash
   wc -c .claude/commands/qa.md
   # Should show ~11,060 chars
   ```

3. Restart terminal to load updated command:
   ```bash
   # Restart Claude Code Terminal
   ```

### Test Execution Commands

```bash
# Unit Test 9: Deep mode PASS → Status updated
/qa STORY-006 deep

# Unit Test 14: Light mode PASS → Status unchanged
/qa STORY-006 light

# Integration Test 1: Full workflow
/qa STORY-006 deep
cat devforgeai/specs/Stories/STORY-006*.story.md | grep "status:"
# Should show: status: QA Approved

# Regression Test 1: Skill invocation
# Verify in output: "devforgeai-qa skill" execution visible

# Performance Test 1: Character budget
wc -c .claude/commands/qa.md
```

---

## Failure Handling

### If Any Test Fails

1. **Document failure:**
   - Test number
   - Expected behavior
   - Actual behavior
   - Error messages

2. **Check rollback criteria:**
   - Critical failures (skill bypass, data corruption) → Immediate rollback
   - Minor failures (formatting, display) → Fix and re-test

3. **Execute rollback if needed:**
   ```bash
   cp .claude/commands/qa.md.backup-pre-phase4 .claude/commands/qa.md
   # Restart terminal
   ```

4. **Create rollback report:**
   - File: `.devforgeai/specs/enhancements/QA-PHASE4-ROLLBACK-REPORT.md`
   - Include: RCA, fix approach, timeline

---

## Test Results Summary

**Date tested:** _________
**Tester:** _________

**Overall Status:** PASS / FAIL / PARTIAL

**Test counts:**
- Unit tests: ___/15 passed
- Integration tests: ___/8 passed
- Regression tests: ___/8 passed
- Performance tests: ___/4 passed

**Total: ___/35 passed**

**Critical issues found:** _________

**Non-critical issues found:** _________

**Recommendation:** DEPLOY / FIX / ROLLBACK

---

## Deployment Checklist

- [ ] All 35 tests passed (or acceptable pass rate ≥95%)
- [ ] Character budget verified (<15K hard limit)
- [ ] Token efficiency verified (~3.5K overhead)
- [ ] Backup exists and verified
- [ ] Documentation updated (commands-reference.md)
- [ ] Enhancement spec documented
- [ ] Rollback plan ready
- [ ] Terminal restarted
- [ ] Smoke tests completed

**Ready for deployment:** YES / NO

**Deployment date:** _________

---

## Post-Deployment Monitoring

### Week 1 Monitoring

- [ ] Monitor token usage per invocation
- [ ] Collect user feedback
- [ ] Track edge cases (malformed YAML, missing sections)
- [ ] Verify story file integrity
- [ ] Check for performance degradation

### Issues Log

| Date | Issue | Severity | Resolution |
|------|-------|----------|------------|
|      |       |          |            |
|      |       |          |            |

---

## Sign-Off

**Implementation completed by:** _________
**Date:** _________

**Testing completed by:** _________
**Date:** _________

**Approved for deployment by:** _________
**Date:** _________
