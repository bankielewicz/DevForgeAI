# STORY-165 Test Suite: RCA-012 Remove Checkbox Syntax from AC Headers

## Overview

This test suite validates the implementation of STORY-165, which removes checkbox syntax from Acceptance Criteria (AC) headers in the story template and all new stories.

**Story ID:** STORY-165
**Type:** Documentation/Template Enhancement
**Epic:** RCA-012 (Root Cause Analysis)
**Status:** Design Phase (Tests Written - TDD Red)

## Acceptance Criteria

### AC#1: Template AC Header Format Updated
- **Given:** `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`
- **When:** Review the Acceptance Criteria section
- **Then:** AC headers should use format `### AC#1: {Title}` instead of `### 1. [ ] {Title}`

**Test:** `test-ac1-template-format.sh`

### AC#2: New Stories Use Updated Format
- **Given:** Updated story template
- **When:** Run `/create-story "Test story"`
- **Then:** Generated story should have AC headers in `### AC#1:` format with no checkboxes

**Test:** `test-ac2-new-stories-format.sh`

### AC#3: No Breaking Changes for Existing Stories
- **Given:** Existing stories with old format
- **When:** Template is updated
- **Then:** Existing stories are unchanged (no automatic migration)

**Test:** `test-ac3-no-breaking-changes.sh`

### AC#4: Format Maintains Numbering Reference
- **Given:** New AC header format
- **When:** Documentation references acceptance criteria
- **Then:** References like "See AC#3" should still work logically

**Test:** `test-ac4-numbering-reference.sh`

## Test Files

| File | Purpose | Type |
|------|---------|------|
| `test-ac1-template-format.sh` | Verify template uses new AC header format | Unit Test |
| `test-ac2-new-stories-format.sh` | Verify new stories follow format | Unit Test |
| `test-ac3-no-breaking-changes.sh` | Verify old stories not auto-migrated | Validation Test |
| `test-ac4-numbering-reference.sh` | Verify AC#N numbering is referenceable | Format Test |
| `run-all-tests.sh` | Test suite orchestrator | Runner |

## Running Tests

### Run All Tests

```bash
bash devforgeai/tests/STORY-165/run-all-tests.sh
```

### Run Individual Test

```bash
# Test AC#1: Template format
bash devforgeai/tests/STORY-165/test-ac1-template-format.sh

# Test AC#2: New stories
bash devforgeai/tests/STORY-165/test-ac2-new-stories-format.sh

# Test AC#3: Backward compatibility
bash devforgeai/tests/STORY-165/test-ac3-no-breaking-changes.sh

# Test AC#4: Numbering reference
bash devforgeai/tests/STORY-165/test-ac4-numbering-reference.sh
```

## Expected Behavior (TDD Red Phase)

**IMPORTANT:** All tests SHOULD FAIL when initially run, because:
1. This is TDD Red phase (tests written before implementation)
2. The implementation hasn't been created yet
3. Tests verify requirements that don't yet exist

After implementation is complete:
1. All tests should PASS
2. Template file contains `### AC#1:` format
3. New story creation uses the updated template
4. Old stories remain unchanged
5. AC#N references are valid

## Test Strategy

### Test Pyramid

```
        E2E Tests (0)

    Integration Tests (1)
    - Story creation workflow

Unit Tests (3)
- Template format verification
- New story format validation
- Reference format validation
```

### Coverage Goals

- **Business Logic:** Template structure and format compliance (95%)
- **Integration:** Story creation with template (85%)
- **Format Validation:** AC numbering and referenceability (100%)

## Implementation Checklist

Use this checklist to track progress toward passing all tests:

- [ ] **AC#1 Implementation**
  - [ ] Update `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`
  - [ ] Change AC headers from `### 1. [ ] {Title}` to `### AC#1: {Title}`
  - [ ] Remove all checkbox syntax from example AC headers
  - [ ] Verify no old format appears in examples
  - [ ] Run: `bash devforgeai/tests/STORY-165/test-ac1-template-format.sh`

- [ ] **AC#2 Implementation**
  - [ ] Verify devforgeai-story-creation skill uses updated template
  - [ ] Test `/create-story` command with updated template
  - [ ] Verify generated stories have new AC format
  - [ ] Run: `bash devforgeai/tests/STORY-165/test-ac2-new-stories-format.sh`

- [ ] **AC#3 Validation**
  - [ ] Confirm existing stories remain unchanged
  - [ ] Verify no auto-migration of old stories occurs
  - [ ] Check for mixed format (error condition)
  - [ ] Run: `bash devforgeai/tests/STORY-165/test-ac3-no-breaking-changes.sh`

- [ ] **AC#4 Validation**
  - [ ] Verify AC#N numbering is consistent
  - [ ] Test that references like "See AC#3" work
  - [ ] Confirm AC numbers are unambiguous
  - [ ] Run: `bash devforgeai/tests/STORY-165/test-ac4-numbering-reference.sh`

- [ ] **Final Verification**
  - [ ] Run: `bash devforgeai/tests/STORY-165/run-all-tests.sh`
  - [ ] All tests should PASS (green)
  - [ ] No failing tests remain

## Related Documentation

- **Story Template:** `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`
- **Changelog:** Template changelog section documents RCA-012 remediation (v2.1)
- **RCA Document:** `devforgeai/RCA/RCA-012/` (planned)
- **Migration Script:** `.claude/skills/devforgeai-story-creation/scripts/migrate-ac-headers.sh` (optional)

## Background: RCA-012

**Root Cause:** Vestigial checkbox syntax (`### 1. [ ] Title`) remained in story template from pre-RCA-011 design.

**Impact:**
- Users confused about unchecked AC headers
- False impression that AC is a completion checklist
- Inconsistent with actual tracking mechanisms (TodoWrite, Definition of Done)

**Solution:**
- Update template to use clear format: `### AC#1: Title`
- AC headers are DEFINITIONS, not completion trackers
- Three-layer tracking clarified:
  1. **TodoWrite:** Phase-level monitoring (AI uses)
  2. **AC Verification Checklist:** Granular sub-item tracking (user sees)
  3. **Definition of Done:** Official completion record (quality gate)

**References:**
- Story Template Changelog (v2.1): Lines 80-95 of story-template.md
- CLAUDE.md: Three-layer tracking system documentation

## Test Status

| Test | Status | Notes |
|------|--------|-------|
| AC#1: Template Format | ❌ FAIL (TDD Red) | Template format not yet updated |
| AC#2: New Stories | ❌ FAIL (TDD Red) | Story creation not yet updated |
| AC#3: No Breaking Changes | ⚠️ PENDING | Depends on AC#1 implementation |
| AC#4: Numbering Reference | ⚠️ PENDING | Depends on AC#1 implementation |

**Status Legend:**
- ❌ FAIL: Test fails as expected (TDD Red phase - implementation needed)
- ✅ PASS: Test passes (implementation complete)
- ⚠️ PENDING: Test outcome depends on other AC implementations

## Questions & Notes

**Q: Why test old stories remain unchanged?**
A: To ensure the template update doesn't break existing stories. Backward compatibility is critical - existing stories may be referenced in documentation and projects.

**Q: Do we need to migrate old stories?**
A: No. The template update only affects NEW stories. A migration script is available optionally for teams that want to update existing stories.

**Q: How does "See AC#3" reference work?**
A: The `AC#N` notation is explicit and unambiguous. Tools can easily parse and match references. Unlike the old checkbox format, AC#N is designed for cross-referencing.

**Q: What about story titles with colons?**
A: The format `### AC#1: [Title]` handles titles with colons correctly. Only the first colon after the AC number is the separator.

## Further Reading

- Story Template file: `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`
- Template Changelog: Lines 80-95 (RCA-012 v2.1 entry)
- Citation: (Source: .claude/skills/devforgeai-story-creation/assets/templates/story-template.md, lines 80-95)
