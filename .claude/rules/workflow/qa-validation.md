---
description: QA validation rules for story verification
version: "1.0"
created: 2025-12-10
---

# QA Validation Rules

## Validation Modes

### Light Mode (During Development)
- Run after each TDD phase
- Fast feedback on obvious issues
- Checks: syntax, imports, basic type safety

### Deep Mode (After Implementation)
- Comprehensive analysis
- Coverage verification
- Anti-pattern detection
- Security scanning

## Coverage Thresholds

| Layer | Minimum Coverage |
|-------|------------------|
| Business Logic | 95% |
| Application | 85% |
| Infrastructure | 80% |

## Blocking Violations

### Critical (Immediate Block)
- Security vulnerabilities
- Data exposure risks
- Authentication bypasses

### High (Block Before QA Approval)
- Coverage below thresholds
- Unhandled error paths
- Missing input validation

## Non-Blocking (Warning Only)
- Style inconsistencies
- Documentation gaps
- Minor complexity issues
