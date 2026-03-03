# Edge Case Identification

**Version**: 1.0
**Parent Agent**: requirements-analyst

This reference lists common edge cases to consider when writing acceptance criteria. Review this list for each story to ensure comprehensive test coverage.

---

## Common Edge Cases

1. **Empty State** - No data exists yet (first-time user, empty collection)
2. **Boundary Values** - Min/max values, null, empty string, zero
3. **Concurrency** - Multiple users editing same resource simultaneously
4. **Network Issues** - Timeout, connection lost, partial response
5. **Large Data Sets** - Pagination required, performance degradation
6. **Special Characters** - Unicode, SQL injection attempts, HTML entities
7. **Duplicate Data** - Unique constraint violations, idempotency
8. **Partial Updates** - Some fields succeed, others fail (atomicity)
9. **Stale Data** - Resource deleted or modified by another user
10. **Authorization** - Access to resource user does not own

---

## How to Apply

For each story, scan this list and ask:
- Does this edge case apply to the feature?
- Is there an acceptance criterion covering it?
- If not, add a scenario for it in the Acceptance Criteria section
