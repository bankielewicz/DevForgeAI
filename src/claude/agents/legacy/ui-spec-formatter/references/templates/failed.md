# Failed Template (❌)
## ❌ UI Specification Generation Failed - {STORY_OR_COMPONENT}

**Status:** Failed
**Reason:** {FAILURE_REASON}

### Issues Encountered

{IF critical validation failure:}
**Critical Issues** (blocks usage):
- ❌ {Issue1}
  - Reason: {Explanation}
  - Required fix: {What to do}

- ❌ {Issue2}
  - Reason: {Explanation}
  - Required fix: {What to do}

{IF generation error:}
**Generation Error:**
- {Error message}
- Check: Was story/component description provided?
- Check: Does your tech-stack.md have a framework defined?
- Check: Is source-tree/ properly configured?

### Recovery Steps

**Option 1: Retry Generation**
- Run: `/create-design {STORY_ID}` or `/create-design {COMPONENT_NAME}`
- Verify all required context is available
- Check skill output for detailed error messages

**Option 2: Manual Specification**
- If generation repeatedly fails, create spec manually:
  1. Document component structure
  2. List required features
  3. Define accessibility requirements
  4. Create test scenarios
  5. Proceed with implementation

**Option 3: Get Help**
- Review `devforgeai/specs/ui/` directory
- Check `devforgeai/specs/context/` files for configuration issues
- Review full skill output for detailed error context

---
