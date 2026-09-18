# Architect Reviewer - Output Format Reference

Architecture review reports follow a structured Markdown format with severity-categorized findings:

```markdown
# Architecture Review: [Component/System Name]

**Reviewed By**: architect-reviewer
**Date**: [YYYY-MM-DD]
**Overall Assessment**: [APPROVED | CHANGES RECOMMENDED | NEEDS REDESIGN]

## Critical Issues (blocking)
### 1. [Issue Title]
- **Severity**: CRITICAL
- **Issue**: [Description]
- **Impact**: [Consequences]
- **Recommendation**: [Specific change needed]

## Warnings (should address)
[...]

## Suggestions (consider)
[...]

## Positive Observations
- ✅ [What's working well]
```
