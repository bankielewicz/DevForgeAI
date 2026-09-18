# Architect Reviewer - Examples

### Example 1: Architecture Review Request

```
Task(
  subagent_type="architect-reviewer",
  description="Review architecture for STORY-123",
  prompt="Review the technical architecture proposed in STORY-123. Focus on scalability, maintainability, and alignment with context files. Read ADRs and architecture-constraints.md before providing recommendations."
)
```

**Expected Output:**
- Structured review report with findings categorized by severity
- Specific references to SOLID principles or patterns violated
- Alternative approaches with trade-offs for critical issues

### Example 2: ADR Validation

```
Task(
  subagent_type="architect-reviewer",
  description="Validate ADR-015",
  prompt="Validate ADR-015 against architecture-constraints.md and tech-stack.md. Ensure the decision is consistent with existing architectural patterns and does not introduce new dependencies without justification."
)
```

**Expected Output:**
- Validation status (APPROVED, CHANGES RECOMMENDED, or NEEDS REDESIGN)
- List of any conflicts with existing context files
- Recommendations for addressing conflicts if found
