# Partial Template (⚠️)
## ⚠️ UI Specification Generated (with warnings) - {STORY_OR_COMPONENT}

**Status:** Partial (generated with validation warnings)
**Generated:** ✓ Components: {COUNT}
**Validation:** ⚠️ {N} issues to address

### Generated Components

{Component list from above}

### Validation Issues

**Framework Consistency:**
{IF tech-stack issues:}
- ⚠️ {Framework} not explicitly listed in tech-stack.md
  - Action: Add to tech-stack.md or verify selection was correct
  - Impact: Development team should use approved framework

{IF dependency issues:}
- ⚠️ {Package} may require addition to dependencies.md
  - Action: Verify with team or add to approved list
  - Impact: Installation and updates

**File Structure:**
{IF source-tree issues:}
- ⚠️ Generated files follow {PATTERN} but source-tree/ specifies {REQUIRED}
  - Action: Move files to correct location per source-tree/
  - Impact: Project organization consistency

**Code Standards:**
{IF coding-standards issues:}
- ⚠️ {Detail} may not fully match coding-standards.md
  - Action: Review and adjust as needed
  - Impact: Code consistency and maintainability

### Recommended Actions

1. **Review Issues:** Address warnings above
2. **Regenerate (if needed):** `/create-design {STORY_ID}` with corrections
3. **Proceed with Implementation:** Issues are warnings, not blockers
4. **Validate During Dev:** Run `/dev {STORY_ID}` to catch issues

---
