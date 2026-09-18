# Checklists

**Purpose:** Success criteria and testing checklist for the dev-result-interpreter subagent. Loaded via `Read()` from the Success Criteria and Testing Checklist sections of the core agent file.

---

## Success Criteria

- [ ] Reads story file correctly (YAML + sections)
- [ ] Extracts workflow status accurately (phases, DoD items, tests)
- [ ] Determines correct overall result (SUCCESS/INCOMPLETE/FAILURE)
- [ ] Categorizes deferrals and incomplete items properly
- [ ] Generates appropriate display template (matches status)
- [ ] Provides actionable next steps (based on result and context)
- [ ] Returns structured JSON (no unstructured text)
- [ ] Handles edge cases (missing metrics, partial workflow, rollback)
- [ ] Token usage <8K (haiku model)
- [ ] Framework-aware (respects workflow states, quality gates)

---

## Testing Checklist

- [ ] Parse SUCCESS (Dev Complete) story
- [ ] Parse INCOMPLETE (In Development, high progress) story
- [ ] Parse INCOMPLETE (In Development, low progress) story
- [ ] Parse INCOMPLETE story with deferrals
- [ ] Parse FAILURE (workflow error) story
- [ ] Extract all TDD phases correctly
- [ ] Count DoD items accurately (completed/incomplete/deferred)
- [ ] Parse test results (passing/total/coverage)
- [ ] Generate success template
- [ ] Generate incomplete template (high/moderate/low progress)
- [ ] Generate deferral template
- [ ] Generate failure template
- [ ] Recommend correct next steps for each result
- [ ] Handle missing/partial Implementation Notes gracefully
- [ ] Validate status transitions make sense
