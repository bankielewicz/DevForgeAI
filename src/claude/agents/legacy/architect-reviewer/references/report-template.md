# Architect Reviewer - Review Report Format Template

```markdown
# Architecture Review: [Component/System Name]

**Reviewed By**: architect-reviewer
**Date**: [YYYY-MM-DD]
**Artifacts Reviewed**:
- ADR-XXX
- technical-spec.md
- architecture-constraints.md

**Overall Assessment**: [APPROVED | CHANGES RECOMMENDED | NEEDS REDESIGN]

---

## Critical Issues

### 1. [Issue Title]

**Severity**: CRITICAL
**Category**: Scalability | Security | Maintainability

**Issue**:
[Clear description of architectural concern]

**Impact**:
- [Consequence 1]
- [Consequence 2]

**Recommendation**:
[Specific architectural change needed]

**Alternative Approaches**:

**Option A**: [Approach 1]
- Pros: [Benefits]
- Cons: [Drawbacks]
- Complexity: High/Medium/Low

**Option B**: [Approach 2]
- Pros: [Benefits]
- Cons: [Drawbacks]
- Complexity: High/Medium/Low

**Recommended**: Option A because [rationale]

---

## Warnings

### 1. [Issue Title]

**Severity**: WARNING
**Category**: [Category]

**Issue**: [Description]

**Recommendation**: [Suggestion]

---

## Suggestions

### 1. [Enhancement Title]

**Category**: Optimization | Best Practice

**Suggestion**: [Description]

**Benefit**: [Why this would help]

---

## Positive Observations

- ✅ Well-separated concerns (Domain, Application, Infrastructure)
- ✅ Appropriate use of Repository pattern
- ✅ Clear dependency flow (follows Dependency Inversion)
- ✅ Scalability considered with caching strategy
- ✅ Technology choices well-justified in ADR-XXX

---

## Design Pattern Assessment

| Pattern | Usage | Assessment | Recommendation |
|---------|-------|------------|----------------|
| Repository | ✅ Used | Appropriate | None |
| Factory | ❌ Missing | Would benefit | Add for [X] creation |
| Strategy | ✅ Used | Over-engineered | Simplify for [Y] |

---

## Scalability Assessment

**Current Approach**: [Summary]

**Bottlenecks Identified**:
1. [Bottleneck 1] - Impact: High/Medium/Low
2. [Bottleneck 2] - Impact: High/Medium/Low

**Scaling Strategy**:
- Horizontal: [Feasible/Not Feasible] - [Reason]
- Vertical: [Feasible/Not Feasible] - [Reason]
- Recommended: [Strategy] because [rationale]

**Capacity Estimates**:
- Current design supports: [X] users/requests
- Target: [Y] users/requests
- Gap: [Analysis]

---

## Technology Validation

| Technology | Purpose | Assessment | Score (1-5) |
|------------|---------|------------|-------------|
| PostgreSQL | Database | Good fit | 4/5 |
| Redis | Cache | Appropriate | 5/5 |
| RabbitMQ | Message Queue | Over-engineered | 2/5 |

**Concerns**:
- RabbitMQ: Team lacks experience, consider simpler alternative (database queue)

---

## Recommended Actions

**Priority 1 (Must Address)**:
1. [Action 1] - Addresses [Critical Issue]
2. [Action 2] - Addresses [Critical Issue]

**Priority 2 (Should Address)**:
1. [Action 1] - Addresses [Warning]

**Priority 3 (Consider)**:
1. [Action 1] - Enhancement

---

## References

- [Best Practice Link]
- [Pattern Documentation]
- [Technology Comparison]

---

**Next Review**: After critical issues addressed
```
