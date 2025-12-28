# STORY-141: Quick Reference Guide

## At A Glance

**Story:** Remove duplicate questions from /ideate workflow
**Tests Generated:** 90 tests in 5 files
**Current Status:** 62/90 passing (68.9%)
**Needs Work:** AC#4 Context Markers (28 tests failing)

---

## Run Tests

```bash
# All tests
npm test -- tests/STORY-141/

# By AC
npm test -- tests/STORY-141/test_ac1_*.js  # AC#1
npm test -- tests/STORY-141/test_ac2_*.js  # AC#2
npm test -- tests/STORY-141/test_ac3_*.js  # AC#3
npm test -- tests/STORY-141/test_ac4_*.js  # AC#4 (28 failing)
npm test -- tests/STORY-141/test_ac5_*.js  # AC#5
```

---

## Test Results Summary

| AC | Title | Tests | Status |
|-----|-------|-------|--------|
| #1 | Remove Project Type | 9 | ✓ 100% |
| #2 | Remove All Discovery | 15 | ✓ 100% |
| #3 | Skill Owns Templates | 21 | ✓ 100% |
| #4 | Context Markers | 25 | ✗ 68% |
| #5 | No Duplicates | 20 | ✓ 100% |
| **TOTAL** | | **90** | **69%** |

---

## What's Working ✓

- [x] Project type question removed from command
- [x] All discovery questions in skill
- [x] Question templates in skill references
- [x] No duplicate questions in workflow
- [x] Clear responsibility boundaries

---

## What Needs Work ✗

- [ ] Context markers not documented
  - **Business Idea:** marker
  - **Brainstorm Context:** marker
  - **Brainstorm File:** marker
- [ ] Display statements for context missing
- [ ] Skill context summary not displayed

---

## Fix AC#4 (28 Tests)

Add to `.claude/commands/ideate.md` **Phase 2: Invoke Ideation Skill**:

```markdown
### 2.1 Set Context for Skill

**Prepare context markers for skill execution:**

**Business Idea:** $ARGUMENTS (or user-provided description)

**Brainstorm Context:** {brainstorm_id} (if selected)

**Brainstorm File:** {path} (if selected)

**Project Mode:** {greenfield|brownfield}
```

Then update skill Phase 1 to display/validate this context.

---

## Files to Review

### Tests (5 files)
- `test_ac1_remove_project_type_from_command.js` ✓ PASSING
- `test_ac2_remove_all_discovery_questions_from_command.js` ✓ PASSING
- `test_ac3_skill_owns_question_templates.js` ✓ PASSING
- `test_ac4_command_passes_context_to_skill.js` ✗ NEEDS WORK (8 tests)
- `test_ac5_zero_duplicate_questions_end_to_end.js` ✓ PASSING

### Documentation (3 files)
- `README.md` - Overview and quick start
- `STORY-141-TEST-GENERATION-SUMMARY.md` - Detailed documentation
- `TEST-EXECUTION-RESULTS.md` - Results and recommendations
- `QUICK-REFERENCE.md` - This file

---

## Key Failing Tests (AC#4)

```
✗ should_have_Business_Idea_context_marker
✗ should_have_Brainstorm_Context_marker_for_brainstorm_flow
✗ should_have_Brainstorm_File_marker_for_file_path
✗ should_display_context_markers_in_output
✗ should_NOT_re_ask_business_idea_if_provided_in_context
✗ should_document_context_markers_in_comment_or_description
✗ should_explain_why_context_prevents_duplicate_questions
✗ should_display_context_summary_before_proceeding
```

---

## What These Tests Check

### AC#1 ✓
- ✓ Project type NOT in command
- ✓ Project type IN skill
- ✓ No duplication

### AC#2 ✓
- ✓ Command has minimal questions (brainstorm only)
- ✓ Skill has all discovery questions
- ✓ Clear responsibility separation

### AC#3 ✓
- ✓ Templates in discovery-workflow.md
- ✓ Templates in requirements-elicitation-workflow.md
- ✓ Command has no templates

### AC#4 ✗
- ✗ **Business Idea:** marker documented
- ✗ **Brainstorm Context:** marker documented
- ✗ **Brainstorm File:** marker documented
- ✗ Context displayed before skill invocation
- ✗ Skill shows context received
- ✗ Skill skips questions when context provided

### AC#5 ✓
- ✓ No question asked twice
- ✓ Each topic appears once
- ✓ Logical flow

---

## Implementation Steps

1. **Add context marker documentation** (5 min)
   - File: `.claude/commands/ideate.md`
   - Location: Phase 2: Invoke Ideation Skill
   - Add: **Business Idea:**, **Brainstorm Context:**, **Brainstorm File:** markers

2. **Add Display statements** (5 min)
   - Show context before Skill() invocation
   - Format: Clear, readable

3. **Update skill Phase 1** (10 min)
   - Add context detection logic
   - Add Display for context summary
   - Update conditional discovery questions

4. **Test** (5 min)
   - Run: `npm test -- tests/STORY-141/test_ac4_*.js`
   - Should see: 25/25 passing

5. **Verify all tests** (2 min)
   - Run: `npm test -- tests/STORY-141/`
   - Should see: 90/90 passing

---

## Files Changed by Story

**Source Files:**
- `.claude/commands/ideate.md` - Already mostly correct (add Phase 2 section)
- `.claude/skills/devforgeai-ideation/SKILL.md` - Already mostly correct (add Phase 1 context handling)

**Test Files (Generated):**
- `tests/STORY-141/test_ac1_*.js`
- `tests/STORY-141/test_ac2_*.js`
- `tests/STORY-141/test_ac3_*.js`
- `tests/STORY-141/test_ac4_*.js`
- `tests/STORY-141/test_ac5_*.js`

---

## Expected Output

### Before (Current)
```
Tests:  62 passed, 28 failed
Suites: 5 failed, 5 total
```

### After (Target)
```
Tests:  90 passed, 0 failed
Suites: 5 passed, 5 total
```

---

## Test Pattern Examples

### Example 1: Verify project type NOT in command
```javascript
expect(commandContent).not.toMatch(/project\s+type|greenfield|brownfield/i);
```

### Example 2: Verify brainstorm ONLY in Phase 0
```javascript
const phase0 = commandContent.match(/## Phase 0:[\s\S]*?(?=^## |$)/)[0];
expect(phase0).toMatch(/brainstorm/i);

const phase1 = commandContent.match(/## Phase 1:[\s\S]*?(?=^## |$)/)[0];
expect(phase1).not.toMatch(/brainstorm.*selection/i);
```

### Example 3: Verify skill Phase separation
```javascript
const phase1Questions = skillContent.match(/Phase 1[\s\S]*?(?=###|$)/)[0].match(/AskUserQuestion/g) || [];
const phase2Questions = skillContent.match(/Phase 2[\s\S]*?(?=###|$)/)[0].match(/AskUserQuestion/g) || [];
expect(phase1Questions.length).toBeLessThan(phase2Questions.length);
```

---

## Cheat Sheet

| Need | Command |
|------|---------|
| Run all tests | `npm test -- tests/STORY-141/` |
| Run AC#4 only | `npm test -- tests/STORY-141/test_ac4_*.js` |
| Watch mode | `npm test -- tests/STORY-141/ --watch` |
| Coverage | `npm test -- tests/STORY-141/ --coverage` |
| Verbose | `npm test -- tests/STORY-141/ --verbose` |
| Single test | `npm test -- tests/STORY-141/ --testNamePattern="should_have_Business_Idea"` |

---

## Acceptance Criteria Summary

```
AC#1: ✓ Remove project type from command
AC#2: ✓ Remove all discovery from command
AC#3: ✓ Skill owns question templates
AC#4: ✗ Command passes context to skill (IMPLEMENT THIS)
AC#5: ✓ Zero duplicate questions
```

---

## Priority

**HIGH:** Implement AC#4 (28 tests failing, straightforward fix)

**Estimated Time:** 20-30 minutes total

**Impact:** Makes 31% of tests pass (28/90) and completes story requirements

---

## More Info

- **Full Details:** See `STORY-141-TEST-GENERATION-SUMMARY.md`
- **Results:** See `TEST-EXECUTION-RESULTS.md`
- **Overview:** See `README.md`
- **Story File:** `devforgeai/specs/Stories/STORY-141-question-duplication-elimination.story.md`

---

**Version:** 1.0 | **Date:** 2025-12-28 | **Status:** Ready for AC#4 Implementation
