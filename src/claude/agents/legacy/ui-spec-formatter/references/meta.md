## Success Criteria

- [ ] Reads UI spec file correctly (all sections extracted)
- [ ] Extracts component details accurately (type, framework, features)
- [ ] Validates against context files (tech-stack, source-tree, dependencies)
- [ ] Generates appropriate display template (matches mode, status, component count)
- [ ] Provides implementation guidance (specific order, time estimates)
- [ ] Recommends clear next steps (based on mode and status)
- [ ] Returns structured JSON (no unstructured text)
- [ ] Handles edge cases (missing spec, validation issues, partial generation)
- [ ] Token usage <10K (haiku model)
- [ ] Framework-aware (respects constraints, references context)

---

## Error Handling

**Spec File Missing:**
- Return error structure (not exception)
- Provide helpful guidance
- Suggest regeneration action

**Malformed Specification:**
- Attempt partial parsing (best effort)
- Log what could be parsed
- Return partial results with warnings

**Validation Issues:**
- Extract and categorize by severity
- Provide remediation guidance
- Mark as PARTIAL or FAILED based on severity

**Framework/Tech-Stack Mismatch:**
- Alert user to discrepancy
- Suggest verification or update to tech-stack.md
- Mark as warning (not blocker)

---

## Token Budget

**Haiku model (cost-effective):**
- Read UI spec file: ~2K tokens
- Extract and validate components: ~4K tokens
- Validate against context files: ~2K tokens
- Generate display template: ~1.5K tokens
- Format output JSON: ~0.5K tokens
- **Total: <10K tokens per invocation**

**Optimization:**
- Single file read (UI spec)
- Selective context file validation (only relevant sections)
- Focused pattern matching
- Deterministic output format

---

## Performance Targets

- **Execution time:** <30 seconds
- **Token usage:** <10,000 tokens
- **Output size:** <6,000 characters
- **Accuracy:** 100% on spec parsing, 99% on validation

---

## Testing Checklist

- [ ] Parse story mode success spec
- [ ] Parse standalone mode success spec
- [ ] Parse spec with validation warnings
- [ ] Parse spec with framework compatibility issues
- [ ] Parse spec with file structure violations
- [ ] Generate success template (story mode)
- [ ] Generate success template (standalone mode)
- [ ] Generate partial template (warnings)
- [ ] Generate failed template (critical issues)
- [ ] Recommend correct next steps for each result type
- [ ] Validate framework consistency with tech-stack.md
- [ ] Validate file structure with source-tree/
- [ ] Handle missing/malformed spec gracefully
- [ ] Extract component details correctly
- [ ] Calculate accurate implementation estimates

---

## Related Subagents

- **spec-driven-design:** Creates UI specs; formatter displays and validates results
- **test-automator:** Generates tests for UI components (referenced in implementation guidance)
- **context-validator:** Can validate UI code against constraints
- **code-reviewer:** Reviews final UI implementation

---
