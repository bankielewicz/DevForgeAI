# Error Handling Index

Redirect index for error handling in the spec-driven-ideation skill. Each error type has a dedicated reference file with detection logic, recovery procedures, and examples.

## Error Type Decision Tree

```
Error detected during workflow
├── Phase 2 (Elicitation): Vague/incomplete response?
│   └── → error-type-1-incomplete-answers.md
├── Phase 3.1 (Artifact Generation): File write/permission failure?
│   └── → error-type-2-artifact-failures.md
├── Phase 3 (Complexity): Assessment calculation error?
│   └── → error-type-3-complexity-errors.md
├── Phase 3.3 (Validation): Quality issues or missing fields?
│   └── → error-type-4-validation-failures.md
├── Phase 5-6 (Feasibility): Brownfield constraint conflict?
│   └── → error-type-5-constraint-conflicts.md
└── Phase 3.1 (Directory): Missing directory or permissions?
    └── → error-type-6-directory-issues.md
```

## Error Type Files

| # | File | Phase | Description |
|---|------|-------|-------------|
| 1 | [error-type-1-incomplete-answers.md](error-type-1-incomplete-answers.md) | Phase 2 | Vague/incomplete user responses during elicitation |
| 2 | [error-type-2-artifact-failures.md](error-type-2-artifact-failures.md) | Phase 3.1 | File write failures and permission errors |
| 3 | [error-type-3-complexity-errors.md](error-type-3-complexity-errors.md) | Phase 3 | Complexity assessment calculation errors |
| 4 | [error-type-4-validation-failures.md](error-type-4-validation-failures.md) | Phase 3.3 | Quality validation issues and missing fields |
| 5 | [error-type-5-constraint-conflicts.md](error-type-5-constraint-conflicts.md) | Phase 5-6 | Brownfield constraint conflicts |
| 6 | [error-type-6-directory-issues.md](error-type-6-directory-issues.md) | Phase 3.1 | Missing directories and permission issues |

## Recovery Strategy

All error types follow the same recovery pattern:

1. **Self-heal** — Attempt automatic fix (max 2 retries)
2. **Retry** — Re-attempt the failed operation
3. **Report** — Escalate to user with clear options

## Quick Reference

- **Index file:** [error-handling-index.md](error-handling-index.md) — Detailed decision tree
- **User patterns:** [user-interaction-patterns.md](user-interaction-patterns.md) — Error recovery conversation patterns

---

**Note:** This file replaces the original monolithic error-handling.md (1062 lines). Content has been split into individual error-type files for progressive disclosure.
