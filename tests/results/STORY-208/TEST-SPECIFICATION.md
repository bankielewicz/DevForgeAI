# TEST-SPECIFICATION: STORY-208 Workflow Completion Self-Check

**Story:** STORY-208-rca-018-workflow-completion-self-check
**Type:** Test Specification Document (Markdown validation, not executable code)
**Status:** RED (tests will fail - section does not exist yet)

---

## Test Target

**File:** `.claude/skills/devforgeai-development/SKILL.md`

---

## AC-1: Self-Check Section Exists

```bash
# test_ac1_selfcheck_section_exists_fail
grep -q "## Workflow Completion Self-Check" .claude/skills/devforgeai-development/SKILL.md
# Expected: Exit 0 (found)
# Current: Exit 1 (NOT FOUND - section missing)
```

---

## AC-2: Phase Count Validation Documented

```bash
# test_ac2_phase_count_validation_logic_documented_fail
grep -q "completed_count.*10" .claude/skills/devforgeai-development/SKILL.md
# Expected: Exit 0 (count == 10 logic present)
# Current: Exit 1 (NOT FOUND)
```

```bash
# test_ac2_halt_on_incomplete_documented_fail
grep -qE "count.*<.*10.*HALT|HALT.*count.*<.*10" .claude/skills/devforgeai-development/SKILL.md
# Expected: Exit 0 (HALT when <10)
# Current: Exit 1 (NOT FOUND)
```

---

## AC-3: Missing Phase Identification

```bash
# test_ac3_missing_phases_display_documented_fail
grep -qE "Missing phases|missing_phases" .claude/skills/devforgeai-development/SKILL.md
# Expected: Exit 0
# Current: Exit 1 (NOT FOUND)
```

---

## AC-4: Section Location After Phase 10

```bash
# test_ac4_selfcheck_after_phase10_fail
# Verify self-check section appears AFTER "Phase 10: Result Interpretation"
awk '/^## Phase 10: Result Interpretation/,/^## Workflow Completion Self-Check/' \
    .claude/skills/devforgeai-development/SKILL.md | grep -q "Self-Check"
# Expected: Exit 0 (section follows Phase 10)
# Current: Exit 1 (NOT FOUND)
```

```bash
# test_ac4_selfcheck_before_success_criteria_fail
# Verify self-check appears BEFORE "## Success Criteria" (final result equivalent)
LINE_SELFCHECK=$(grep -n "## Workflow Completion Self-Check" .claude/skills/devforgeai-development/SKILL.md | cut -d: -f1)
LINE_SUCCESS=$(grep -n "## Success Criteria" .claude/skills/devforgeai-development/SKILL.md | cut -d: -f1)
# Expected: LINE_SELFCHECK < LINE_SUCCESS
# Current: LINE_SELFCHECK is empty (section missing)
```

---

## Validation Summary

| Test ID | AC | Expected | Current | Status |
|---------|-----|----------|---------|--------|
| test_ac1_selfcheck_section_exists | AC-1 | Pass | Fail | RED |
| test_ac2_phase_count_validation_logic | AC-2 | Pass | Fail | RED |
| test_ac2_halt_on_incomplete | AC-2 | Pass | Fail | RED |
| test_ac3_missing_phases_display | AC-3 | Pass | Fail | RED |
| test_ac4_selfcheck_after_phase10 | AC-4 | Pass | Fail | RED |
| test_ac4_selfcheck_before_success | AC-4 | Pass | Fail | RED |

**Total:** 6 tests, 0 passing, 6 failing (TDD Red state achieved)
