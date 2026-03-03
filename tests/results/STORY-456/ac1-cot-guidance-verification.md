# AC#1 Verification: CoT Guidance in requirements-elicitation-workflow.md

**Story:** STORY-456
**AC:** AC#1 - Chain-of-Thought guidance added to requirements-elicitation-workflow.md
**Target File:** `src/claude/skills/discovering-requirements/references/requirements-elicitation-workflow.md`
**Generated:** 2026-02-19
**TDD Phase:** RED (tests must FAIL against unmodified src/ files)

---

## Test Specification

### Test 1: `<thinking>` opening tag present

**Arrange:**
- File: `src/claude/skills/discovering-requirements/references/requirements-elicitation-workflow.md`

**Act:**
```bash
grep -q "<thinking>" "$TARGET_FILE"
```

**Assert:** Exit code 0 (tag found)

**Expected RED failure:** File currently has 0 occurrences of `<thinking>` tag.

---

### Test 2: `</thinking>` closing tag present

**Arrange:**
- File: `src/claude/skills/discovering-requirements/references/requirements-elicitation-workflow.md`

**Act:**
```bash
grep -q "</thinking>" "$TARGET_FILE"
```

**Assert:** Exit code 0 (closing tag found)

**Expected RED failure:** File currently has 0 occurrences of `</thinking>` tag.

---

### Test 3: Prioritization factor - "Business value" present

**Arrange:**
- File: `src/claude/skills/discovering-requirements/references/requirements-elicitation-workflow.md`

**Act:**
```bash
grep -q "Business value" "$TARGET_FILE"
```

**Assert:** Exit code 0 (factor found)

**Expected RED failure:** File currently has 0 occurrences of "Business value".

---

### Test 4: Prioritization factor - "Technical feasibility" present

**Arrange:**
- File: `src/claude/skills/discovering-requirements/references/requirements-elicitation-workflow.md`

**Act:**
```bash
grep -q "Technical feasibility" "$TARGET_FILE"
```

**Assert:** Exit code 0 (factor found)

**Expected RED failure:** File currently has 0 occurrences of "Technical feasibility".

---

### Test 5: Prioritization factor - "Dependencies" present

**Arrange:**
- File: `src/claude/skills/discovering-requirements/references/requirements-elicitation-workflow.md`

**Act:**
```bash
grep -q "Dependencies" "$TARGET_FILE"
```

**Assert:** Exit code 0 (factor found)

**Expected RED failure:** File currently has 0 occurrences of "Dependencies" in prioritization context.

---

### Test 6: Prioritization factor - "User impact" present

**Arrange:**
- File: `src/claude/skills/discovering-requirements/references/requirements-elicitation-workflow.md`

**Act:**
```bash
grep -q "User impact" "$TARGET_FILE"
```

**Assert:** Exit code 0 (factor found)

**Expected RED failure:** File currently has 0 occurrences of "User impact".

---

### Test 7: MoSCoW instruction present (Must-Have)

**Arrange:**
- File: `src/claude/skills/discovering-requirements/references/requirements-elicitation-workflow.md`

**Act:**
```bash
grep -q "Must-Have" "$TARGET_FILE"
```

**Assert:** Exit code 0 (MoSCoW keyword found)

**Expected RED failure:** File currently has 0 occurrences of "Must-Have".

---

### Test 8: MoSCoW instruction present (Should-Have)

**Arrange:**
- File: `src/claude/skills/discovering-requirements/references/requirements-elicitation-workflow.md`

**Act:**
```bash
grep -q "Should-Have" "$TARGET_FILE"
```

**Assert:** Exit code 0 (MoSCoW keyword found)

**Expected RED failure:** File currently has 0 occurrences of "Should-Have".

---

### Test 9: MoSCoW instruction present (Could-Have)

**Arrange:**
- File: `src/claude/skills/discovering-requirements/references/requirements-elicitation-workflow.md`

**Act:**
```bash
grep -q "Could-Have" "$TARGET_FILE"
```

**Assert:** Exit code 0 (MoSCoW keyword found)

**Expected RED failure:** File currently has 0 occurrences of "Could-Have".

---

### Test 10: MoSCoW instruction present (Won't-Have)

**Arrange:**
- File: `src/claude/skills/discovering-requirements/references/requirements-elicitation-workflow.md`

**Act:**
```bash
grep -qE "Won.t-Have" "$TARGET_FILE"
```

**Assert:** Exit code 0 (MoSCoW keyword found)

**Expected RED failure:** File currently has 0 occurrences of "Won't-Have".

---

### Test 11: No existing content deleted (line count must not decrease)

**Arrange:**
- File: `src/claude/skills/discovering-requirements/references/requirements-elicitation-workflow.md`
- Baseline line count at RED phase: 395 lines

**Act:**
```bash
LINE_COUNT=$(wc -l < "$TARGET_FILE")
[ "$LINE_COUNT" -ge 395 ]
```

**Assert:** Exit code 0 (line count >= 395, additions only)

**Expected GREEN state:** File must retain all 395 original lines plus new additions.

---

## AC#1 GREEN Criteria Summary

All tests pass when:
1. `<thinking>` and `</thinking>` tags both present
2. All 4 prioritization factors present: "Business value", "Technical feasibility", "Dependencies", "User impact"
3. MoSCoW keywords present: "Must-Have", "Should-Have", "Could-Have", "Won't-Have" (or Won't-Have)
4. Line count >= 395 (no deletions)
