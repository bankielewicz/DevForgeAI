# QA Result Interpreter -- Testing Checklist and Related Subagents

Reference content extracted from the core agent definition. Combined testing checklist and related subagent references.

---

## Testing Checklist

- [ ] Parse light mode pass report
- [ ] Parse deep mode pass report
- [ ] Parse deep mode fail with coverage violations
- [ ] Parse deep mode fail with anti-pattern violations
- [ ] Parse deep mode fail with deferral violations
- [ ] Parse report with mixed violation types
- [ ] Handle report with 0 violations
- [ ] Handle report with 50+ violations (aggregation)
- [ ] Generate each display template variant
- [ ] Recommend correct workflow for each result type
- [ ] Handle missing/malformed report gracefully

---

## Related Subagents

- **deferral-validator:** Creates deferral violations in report; result-interpreter displays them
- **context-validator:** Creates context-related violations; result-interpreter categorizes them
- **test-automator:** Generates coverage analysis; result-interpreter interprets results
- **code-reviewer:** Detects anti-patterns; result-interpreter displays findings
